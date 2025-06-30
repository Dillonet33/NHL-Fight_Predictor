import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import re


def clean_name(name):
    return re.sub(r'[^A-Za-z]', '', name).lower()


def extract_features_and_labels(data):
    df = pd.DataFrame(data)

    # Drop fights with missing winners or low votes
    df = df[df['votes'] > 0].dropna(subset=['winner'])

    # Create features
    df['fighter1_clean'] = df['fighter1'].apply(clean_name)
    df['fighter2_clean'] = df['fighter2'].apply(clean_name)
    df['winner_clean'] = df['winner'].apply(lambda w: clean_name(w.split('(')[0]))

    df['fighter1_is_winner'] = (df['fighter1_clean'] == df['winner_clean']).astype(int)
    df['fighter2_is_winner'] = (df['fighter2_clean'] == df['winner_clean']).astype(int)

    # Label: who won (1 = fighter1, 0 = fighter2)
    df['label'] = df['fighter1_is_winner']

    # Features: rating, vote count, win %
    X = df[['rating', 'votes', 'winner_percent']].fillna(0)
    y = df['label']

    return X, y, df


def train_model(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    X, y, df = extract_features_and_labels(data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return clf


if __name__ == "__main__":
    model = train_model("recent_nhl_fights.json")
