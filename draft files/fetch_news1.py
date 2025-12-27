import requests
import time
from datetime import datetime,timedelta
import pandas as pd
import os

API_KEY = '14d523e1b9334f54804d9dbe1c1c3b87'
url = 'https://newsapi.org/v2/everything'

TOPICS = ['technology','sports','business','health','politics','climate']

Directory = 'newsapi_daily_data'
os.makedirs(Directory, exist_ok=True)

def fetch_news():
    print(f"\n Fetching news for {datetime.now().strftime('%Y-%m-%d')}..\n")
    all_articles = []
    today = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

    for topic in TOPICS:
        for page in range(1,6):
            params = {
                'q': topic,
                'from': today,
                'to': today,
                'language' : 'en',
                'sortBy' : 'publishedAt',
                'pageSize': 100,
                'page' : page,
                'apikey' : API_KEY
             }

            response = requests.get(url, params=params)
            data = response.json()

            if data['status'] == 'ok':
                articles = data.get('articles',[])
                if not articles:
                    break
                for article in articles:
                    article['topic'] = topic
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} articles for topic '{topic}' (page{page})")
            else:
                print("Error: ",data)
                break

            time.sleep(1.5)
    if all_articles:
        df = pd.DataFrame(all_articles)
        df.drop_duplicates(subset = 'url', inplace=True)
        filename = f"{Directory}/newsapi_data_{today}"
        i = 1
        while os.path.exists(f"{filename}_v{i}.csv"):
            i += 1
        filename = f"{filename}_v{i}.csv"
        df.to_csv(filename, index=False)
        print(f"saved {len(df)} articles to {filename}")
    else:
        print("No articles found today.")

fetch_news()



