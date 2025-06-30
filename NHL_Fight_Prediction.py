import asyncio
import json
import os
from playwright.async_api import async_playwright
import re
from datetime import datetime
import subprocess

OUTPUT_FILE = "recent_nhl_fights.json"
BASE_URL = "https://www.hockeyfights.com"
SEASON_LOG_PAGES = [f"{BASE_URL}/fightlog/1/reg2025/1"]


def parse_summary(summary):
    match = re.match(r"(.+?) \((.+?)\) vs\. (.+?) \((.+?)\)", summary)
    if match:
        return {
            "fighter1": match.group(1).strip(),
            "team1": match.group(2).strip(),
            "fighter2": match.group(3).strip(),
            "team2": match.group(4).strip()
        }
    return {"summary": summary}


def parse_date(raw_date):
    try:
        date_part = raw_date.split("•")[0].strip()
        return datetime.strptime(date_part, "%m/%d/%y").date().isoformat()
    except:
        return raw_date


def parse_percentage(text):
    match = re.search(r"(\d+)%", text)
    return int(match.group(1)) if match else None


def parse_float(text):
    match = re.search(r"([\d\.]+)", text)
    return float(match.group(1)) if match else None


def parse_int(text):
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else 0


async def get_fights_from_regular_season(page):
    fights = []
    visited_hrefs = set()

    while True:
        fight_articles = await page.query_selector_all("article")

        for article in fight_articles:
            try:
                summary_el = await article.query_selector("span.text-xl.font-bold")
                date_el = await article.query_selector("span.text-base.text-gray-400")
                winner_el = await article.query_selector("span.text-sm.text-gray-500:has-text('Voted winner')")
                rating_el = await article.query_selector("span.text-sm.text-gray-500:has-text('Voted rating')")
                votes_el = await article.query_selector("span.text-sm.text-gray-500:has-text('Vote count')")

                summary = await summary_el.inner_text() if summary_el else None
                date = await date_el.inner_text() if date_el else None
                winner = await winner_el.inner_text() if winner_el else ""
                rating = await rating_el.inner_text() if rating_el else ""
                votes = await votes_el.inner_text() if votes_el else ""

                if summary and date:
                    fight_data = parse_summary(summary.strip())
                    fight_data.update({
                        "date": parse_date(date.strip()),
                        "period_time": date.strip(),
                        "winner": re.sub(r"Voted winner:\s*", "", winner.strip()),
                        "winner_percent": parse_percentage(winner),
                        "rating": parse_float(rating),
                        "votes": parse_int(votes)
                    })
                    fights.append(fight_data)
            except:
                continue

        # Get all pagination links
        pagination_links = await page.query_selector_all("a[href^='/fightlog/1/reg2025/']")
        next_href = None
        for link in pagination_links:
            href = await link.get_attribute("href")
            if href and href not in visited_hrefs:
                next_href = href
                visited_hrefs.add(href)
                break

        if next_href:
            next_url = BASE_URL + next_href
            await page.goto(next_url, timeout=30000)
            await page.wait_for_timeout(1000)
        else:
            break

    return fights


async def main():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for season_url in SEASON_LOG_PAGES:
            print(f"Visiting season page: {season_url}")
            try:
                await page.goto(season_url, timeout=60000)
                await page.wait_for_timeout(1000)
                season_fights = await get_fights_from_regular_season(page)
                results.extend(season_fights)
            except Exception as e:
                print(f"Failed to visit season page {season_url}: {e}")

        seen = set()
        unique_fights = []
        for fight in results:
            key = (fight.get("fighter1"), fight.get("fighter2"), fight.get("date"))
            if key not in seen:
                seen.add(key)
                unique_fights.append(fight)
            if len(unique_fights) >= 250:
                break

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(unique_fights, f, indent=2)

        print(f"Saved {len(unique_fights)} recent NHL fights to JSON.")


if __name__ == "__main__":
    asyncio.run(main())
    subprocess.run(["python", "train_model.py"])
