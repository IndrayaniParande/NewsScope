import requests
import time
from datetime import datetime, timedelta
import pandas as pd
import os

API_KEY = os.getenv("NEWS_API_KEY")
URL = 'https://newsapi.org/v2/everything'

if not API_KEY:
    raise ValueError('NEWS_API_KEY not found in environment variables')

TOPICS = ['technology', 'sports', 'business', 'health', 'politics', 'climate']
DIRECTORY = 'newsapi_daily_data'
os.makedirs(DIRECTORY, exist_ok=True)
USE_VERSIONING = True

def fetch_news1() -> pd.DataFrame:
    all_articles = []
    from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    for topic in TOPICS:
        for page in range(1, 6):
            params = {
                'q': topic,
                'from': from_date,
                'to': to_date,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 100,
                'page': page,
                'apiKey': API_KEY
            }

            response = requests.get(URL, params=params)
            if response.status_code != 200:
                break


            articles = response.json().get('articles', [])
            if not articles:
                break

            for article in articles:
                article['topic'] = topic

            all_articles.extend(articles)
            time.sleep(1.5)


    if not all_articles:
        for topic in TOPICS:
            for page in range(1, 6):
                params = {
                    'q': topic,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 100,
                    'page': page,
                    'apiKey': API_KEY
                }
                response = requests.get(URL, params=params)
                if response.status_code != 200:
                    break

                data = response.json()
                articles = data.get('articles', [])
                if not articles:
                    break

                for article in articles:
                    article['topic'] = topic

                all_articles.extend(articles)
                time.sleep(1.5)

    if not all_articles:
        return pd.DataFrame()

    df = pd.DataFrame(all_articles)
    df.drop_duplicates(subset="url", inplace=True)

    filename = f"{DIRECTORY}/newsapi_data_{datetime.now().strftime('%Y-%m-%d')}"
    if USE_VERSIONING:
        i = 1
        while os.path.exists(f"{filename}_v{i}.csv"):
            i += 1
        filename = f"{filename}_v{i}.csv"
    else:
        filename = f"{filename}.csv"

    df.to_csv(filename, index=False)
    return df
