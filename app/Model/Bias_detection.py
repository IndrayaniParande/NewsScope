import numpy as np
import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv(r"C:/Users/ASUS/Desktop/News_Analyzer/app/collector/final_data.csv")

def get_text(row):
    content = row.get('content') or ""
    desc = row.get('description') or ""
    title = row.get('title') or ""
    text = content if len(content.strip()) > 50 else f"{title}.{desc}"
    return str(text)

def clean_text(s):
    s = re.sub(r'http\S+', '', s)
    s = re.sub(r'\s+', '',s).strip()
    return s

analyzer = SentimentIntensityAnalyzer()

def vader_score(text):
    text = clean_text(text)
    if not text or pd.isna(text):
        return None
    return analyzer.polarity_scores(text)['compound']

df['analysis'] = df.apply(get_text, axis=1)
df['sentiment_score'] = df['analysis'].apply(vader_score)

def bias_label(score):
    if score is None:
        return 'No_data'
    if score >= 0.05:
        return 'positive slant'
    if score <= -0.05:
        return 'negative slant'
    return 'neutral'

df['bias_label'] = df['sentiment_score'].apply(bias_label)

print(df[['analysis', 'sentiment_score', 'bias_label']].head())

print(df['bias_label'].unique())
