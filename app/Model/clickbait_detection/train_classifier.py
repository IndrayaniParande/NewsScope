import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from app.Model.clickbait_detection.features import extract_features
from app.Model.clickbait_detection.classifier import clickbaitClassifier

def load_dataset(path = "labeled_news.csv"):
    df = pd.read_csv(path)
    X = np.array([extract_features(t) for t in df["title"]])
    y = df["label"].values
    return X,y


if __name__ == "__main__":
    X,y = load_dataset()
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

    clf = clickbaitClassifier()
    clf.train(X_train,y_train)

    pred = [1 if p >= 0.5 else 0 for p in clf.model.predict_proba(X_test)[:, 1]]
    print(classification_report(y_test,pred))

    clf.save("clickbait_model.pkl")
    print("Model saved")



