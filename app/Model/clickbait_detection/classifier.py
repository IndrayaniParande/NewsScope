import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .features import extract_features,feature_names

class clickbaitClassifier:
    def __init__(self, model=None):
        self.model = model or LogisticRegression(max_iter=500, class_weight="balanced")

    def train(self,X,y):
        self.model.fit(X,y)

    def predict(self, title: str):
        features =  np.array(extract_features(title)).reshape(1, -1)
        prob = self.model.predict_proba(features)[0][1]
        return prob

    def save(self, path = "clickbait_model.pkl"):
        joblib.dump((self.model, feature_names), path)

    @staticmethod
    def load(path = "clickbait_model.pkl"):
        model, _ = joblib.load(path)
        return clickbaitClassifier(model = model)


