from app.Model.Text_summerizer1 import tweet_generator

def summarize_article(title: str, description: str):
    """
    Service wrapper for text summarization.
    Returns tweet-style summary and similarity score.
    """
    return tweet_generator(title, description)
