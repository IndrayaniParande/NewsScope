from .similarity import compute_similarity
from .classifier import clickbaitClassifier

class HybridClickbaitDetector:
    def __init__(self, sim_thresh = 0.4, clf_thresh = 0.5, model_path = "clickbait_model.pkl"):
        self.sim_thresh = sim_thresh
        self.clf_thresh = clf_thresh
        self.classifier = clickbaitClassifier().load(model_path)

    def predict(self, title: str, content: str):
        sim_score = compute_similarity(title, content)
        clf_prob = self.classifier.predict(title)

        if sim_score >= self.sim_thresh and clf_prob < self.clf_thresh:
            label = 0

        elif clf_prob >= self.clf_thresh:
            label = 1

        else:
            hybrid_score = (1 - sim_score) * clf_prob
            label = 1 if hybrid_score >= 0.45 else 0

        return label,sim_score,clf_prob


