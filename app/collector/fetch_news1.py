import requests
import time
from datetime import datetime, timedelta
import pandas as pd
import os

API_KEY = 'dfcc612c50cb47448c05cbde55b4a604'
URL = 'https://newsapi.org/v2/everything'

TOPICS = ['technology', 'sports', 'business', 'health', 'politics', 'climate']
Directory = 'newsapi_daily_data'
os.makedirs(Directory, exist_ok=True)
USE_VERSIONING = True

def fetch_news1():
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
                print(f"API error {response.status_code}: {response.text}")
                break

            data = response.json()
            articles = data.get('articles', [])
            if not articles:
                break  # No more articles for this topic
            for article in articles:
                article['topic'] = topic
            all_articles.extend(articles)
            print(f"Fetched {len(articles)} articles for topic '{topic}' (page {page})")
            time.sleep(1.5)

    # Fallback: if no articles in last 24h, fetch latest available
    if not all_articles:
        print("No articles found in the last 24 hours. Fetching latest available articles...\n")
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
                    print(f"API error {response.status_code}: {response.text}")
                    break
                data = response.json()
                articles = data.get('articles', [])
                if not articles:
                    break
                for article in articles:
                    article['topic'] = topic
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} latest articles for topic '{topic}' (page {page})")
                time.sleep(1.5)


    # Create DataFrame
    if all_articles:
        df = pd.DataFrame(all_articles)
        df.drop_duplicates(subset='url', inplace=True)
        filename = f"{Directory}/newsapi_data_{datetime.now().strftime('%Y-%m-%d')}"
        if USE_VERSIONING:
            i = 1
            while os.path.exists(f"{filename}_v{i}.csv"):
                i += 1
            filename = f"{filename}_v{i}.csv"
        else:
            filename = f"{filename}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} articles to {filename}")
        return df
    else:
        print("No articles found at all.")
        return pd.DataFrame()
print(f"\nFetching news for the last 24 hours ({datetime.now() - timedelta(days=1)} to {datetime.now()})...\n")


if __name__ == "__main__":
    fetch_news1()
