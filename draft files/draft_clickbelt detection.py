import pandas as pd

data1 = pd.read_csv("C:/Users./ASUS/Desktop/News_Analyzer/app/collector/final_data.csv")
final_data = data1[['title','description','content']]


print(final_data.info())
print(final_data.describe())
print(final_data.shape)
print(final_data.isnull().sum().sum())
print(final_data.duplicated().sum().sum())

## clickbait detection function

def clickbait_detect(title,content, threshold = 0.3):
    texts = [str(title), str(content)]
    vectorizer = TfidfVectorizer(stop_words= 'english')
    vectors = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return similarity < threshold, similarity

results = final_data.apply(lambda row : clickbait_detect(row['title'], row['description']), axis =1)

pd.set_option('display.max_columns', None)
final_data['is_clickbait'], final_data['similarity_score'] = zip(*results)
print(final_data[['title', 'is_clickbait','similarity_score']].head(10))
print("All done :)))))))))))")






import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.collector.fetch_news import fetch_news


def clickbait_detect(title, content, threshold=0.3):
    texts = [str(title), str(content)]
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return similarity < threshold, similarity


def run_clickbait_detection():
    final_data = fetch_news()[['title', 'description', 'content']]

    results = final_data.apply(
        lambda row: clickbait_detect(row['title'], row['description']), axis=1
    )
    final_data['is_clickbait'], final_data['similarity_score'] = zip(*results)
    return final_data[['title', 'is_clickbait', 'similarity_score']]

df_results = run_clickbait_detection()
pd.set_option('display.max_columns', None)
print(df_results.head(10))





