from transformers import pipeline
import re
from sentence_transformers import SentenceTransformer, util

summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_description(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    seen = set()
    cleaned = []
    for s in sentences:
        s_clean = s.strip()
        if s_clean not in seen and s_clean != "":
            seen.add(s_clean)
            cleaned.append(s_clean)
    return " ".join(cleaned)

def tweet_generator(title, description, max_len = None, min_len = None, sim_threshold=0.8):
    description = preprocess_description(description)
    input_len = len(description.split())
    if max_len is None:
        max_len = max(25, min(50, input_len - 5))
    if min_len is None:
        min_len = max(15, min(30, input_len // 2))

    summary = summarizer(
        description,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )[0]['summary_text']

    embedding = similarity_model.encode([title, summary], convert_to_tensor=True)
    similarity_score = float(util.pytorch_cos_sim(embedding[0], embedding[1]))

    if similarity_score < sim_threshold and input_len > 50:
        summary = summarizer(
            description,
            max_length=max_len + 5,
            min_length=min_len,
            do_sample=True
        )[0]['summary_text']
        embedding = similarity_model.encode([title, summary], convert_to_tensor=True)
        similarity_score = float(util.pytorch_cos_sim(embedding[0], embedding[1]))

    tweet_summary = summary.split(". ")[0]
    tweet_summary = tweet_summary[:277] + "..." if len(tweet_summary) > 280 else tweet_summary

    return {
        'tweet_summary': tweet_summary.strip(),
        'similarity_score': round(similarity_score, 3)
    }

def clean_summary(summary, max_length=300):
    summary = " ".join(tweet_summary.split())

    if len(summary) <= max_length:
        if summary[-1] not in ".!?":
            summary += "."
        return summary

    sentences = re.split(r'(?<=[.!?]) +', summary)
    tweet = ""
    for sent in sentences:
        if len(tweet) + len(sent) + 1 > max_length:
            break
        tweet += sent + " "
    tweet = tweet.strip()

    if tweet and tweet[-1] not in ".!?":
        tweet += "..."

    return tweet

