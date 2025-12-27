import requests
import time
from datetime import datetime, timedelta
import pandas as pd
import os


API_KEY = '14d523e1b9334f54804d9dbe1c1c3b87'
url = 'https://newsapi.org/v2/everything'

TOPICS = ['technology', 'sports', 'business', 'health', 'politics', 'climate']
data_dir = '../app/collector/newsapi_daily_data'
os.makedirs(data_dir, exist_ok=True)
USE_VERSIONING = True

def fetch_news(max_pages=3, page_size=100):
    print(f"\nFetching news for the last 24 hours ({datetime.now() - timedelta(days=1)} to {datetime.now()})...\n")
    all_articles = []

    from_time = (datetime.now() - timedelta(days=1)).isoformat()
    to_time = datetime.now().isoformat()


    for topic in TOPICS:
        for page in range(1, max_pages + 1):
            params = {
                'q': topic,
                'from': from_time,
                'to': to_time,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': page_size,
                'page': page,
                'apikey': API_KEY
            }
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break

            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                if not articles:
                    break
                for article in articles:
                    article['topic'] = topic
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} articles for topic '{topic}' (page {page})")
            else:
                print("API Error: {data}")
                break

            time.sleep(1.5)

    df = pd.DataFrame(all_articles)
    if not df.empty:
        df.drop_duplicates(subset='url', inplace=True)

        filename = f"{data_dir}/newsapi_data_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
        if USE_VERSIONING:
            i = 1
            while os.path.exists(f"{filename}_v{i}.csv"):
                i += 1
            filename = f"{filename}_v{i}.csv"
        else:
            filename = f"{filename}.csv"

        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} articles to {filename}")
    else:
        print("No articles found in the last 24 hours.")

    return df

if __name__ == "__main__":
    fetch_news()


