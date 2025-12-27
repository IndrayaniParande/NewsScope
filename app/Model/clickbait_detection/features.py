import re
import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/ASUS/Desktop/News_Analyzer/app/collector/final_data.csv")
pd.set_option('display.max_columns', None)
print(df.head(n = 10))

def extract_features(title: str):
    title = str(title)
    exclamations = title.count("!")
    questions = title.count("?")
    uppercase_ration = sum(1 for c in title if c.isupper()) / (len(title) +1)
    digit_count = sum(c.isdigit() for c in title)
    listicle = 1 if re.match(r"^\d+",title.strip()) else 0
    buzzwords = ["shocking","unbelievable","you won't believe","secret","amazing"]
    buzz_flag = 1 if any  (word.lower() in title.lower()for word in buzzwords) else 0

    return[
        exclamations,
        questions,
        uppercase_ration,
        digit_count,
        listicle,
        buzz_flag
    ]
feature_names = [
    "exclamations",
    "questions",
    "uppercase_ration",
    "digit_count",
    "listicle",
    "buzz_flag"
]


