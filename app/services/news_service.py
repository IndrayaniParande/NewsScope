import pandas as pd
from app.collector.fetch_news1 import fetch_news1

def get_latest_news() -> pd.DataFrame:
    """
    Service layer for fetching news.
    Streamlit / API must call only this function

    """
    df = fetch_news1()
    if df is None or df.empty:
        return pd.DataFrame()
    return df


