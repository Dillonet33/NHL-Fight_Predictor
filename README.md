# NHL_Fight_Predictor



# NHL Fight Scraper & ML Predictor



This is a project I built to collect and analyze hockey fight data. It scrapes recent NHL fights from HockeyFights.com and trains a machine learning model to predict the outcome of fights based on things like fan vote percentage, rating, and number of votes. The long-term goal is to be able to take an upcoming schedule and use historical behavior to predict which players are likely to fight and who would win.



---



## Features



- Scrapes all NHL regular season fights from the current season

- Pulls fighter names, teams, date, period, winner, win %, fan rating, and vote count

- Cleans and parses the data into a usable format

- Trains a random forest classifier to predict the winner (fighter1 or fighter2)

- Outputs a classification report so I can track how accurate the model is



---



## How to Run



1. Scrape the fight data

*  python nhl_fight_scraper.py



*  This will generate a file called recent_nhl_fights.json.



2. Train the model

*  This happens automatically after scraping, or you can run it on its own:

*  python train_model.py



*  It will load the data, train a model, and print out accuracy stats.



## Dependencies



Install everything with:
pip install -r requirements.txt



This project uses:



* playwright for web scraping
* pandas for data manipulation
* scikit-learn for training the model





What's Next

* Predicting fights (when they will occur, players involved, and the winner) based on next season’s schedule



* Adding rivalry detection between players and teams



* Including penalty minutes and historical fight behavior



* Building a simple interface or dashboard to view predictions



About Me



I'm a full stack software developer with a background in ASP.NET, React, SQL, and Python. This project started as a fun way to mix coding with my love of hockey and has turned into a practical ML exploration in sports analytics.

