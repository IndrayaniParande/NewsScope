from app.Model.clickbait_detection.hybrid import HybridClickbaitDetector


_detector = HybridClickbaitDetector()

def analyze_article(title: str, content: str):
    """
    Service wrapper for clickbait detection.
    """
    label, sim_score, clf_prob = _detector.predict(title, content)

    return {
        "is_clickbait": label,
        "similarity_score": sim_score,
        "clf_prob": clf_prob
    }
