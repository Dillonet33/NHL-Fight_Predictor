import requests
from bs4 import BeautifulSoup

player = "tom-wilson"
url = f"https://www.hockeyfights.com/players/{player}"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())