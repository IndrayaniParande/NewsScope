import re
import pandas as pd

df = pd.read_csv("C:/Users/ASUS/Desktop/News_Analyzer/app/collector/final_data.csv")
print(df.head())

BUZZWORDS = ["shocking","unbelievable","you won’t believe","secret","amazing"]

def label_clickbait(title: str):
    title = str(title)
    listicle = 1 if re.match(r"^\d+", title.strip()) else 0
    buzz = 1 if any(word.lower() in title.lower() for word in BUZZWORDS) else 0
    exclam = 1 if "!" in title else 0
    return 1 if listicle or buzz or exclam else 0


df["label"] = df["title"].apply(label_clickbait)
df.to_csv("labeled_news.csv", index=False)
print("labeled_news.csv created with 0=yes 1=no labels")
