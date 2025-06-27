import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

#Mock Dataset (will be replaced soon with hockeyfights API for current futureproof data)
data = {
    "player": [
        "Tom Wilson", "Ryan Reaves", "Brad Marchand", "Connor McDavid", "Auston Matthews",
        "Matthew Tkachuk", "Pat Maroon", "Nikita Kucherov", "Leon Draisaitl", "Milan Lucic",
        "Sidney Crosby", "Evander Kane", "Brady Tkachuk", "Nazem Kadri", "Josh Anderson",
        "David Pastrnak", "Jacob Trouba", "Mark Scheifele", "Wayne Simmonds", "Corey Perry",
        "Artemi Panarin", "Brendan Lemieux", "Zach Kassian", "Trevor Zegras", "Claude Giroux"
    ],
    "fights_last_season": [
        10, 12, 5, 0, 1,
        8, 9, 0, 0, 7,
        0, 4, 6, 3, 5,
        1, 4, 0, 8, 6,
        0, 7, 6, 0, 2
    ]
}

df = pd.DataFrame(data)

# Fight likeliness
df["will_fight_this_season"] = (df["fights_last_season"] >= 5).astype(int)

#training the AI model
X = df[["fights_last_season"]]
y = df["will_fight_this_season"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

#Predictions happen here
y_pred = model.predict(X_test)
print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

df["predicted_will_fight"] = model.predict(X)

#Results
print("\n🧠 Fight Predictions for This Season:\n")
for _, row in df.iterrows():
    status = "🟥 Likely to Fight" if row["predicted_will_fight"] == 1 else "🟩 Unlikely to Fight"
    print(f"{row['player']}: {status} ({row['fights_last_season']} fights last season)")