import streamlit as st
import pandas as pd
import glob

# --- Load all CSVs dynamically ---
csv_files = glob.glob("newsapi_daily_data/*.csv")
df_list = [pd.read_csv(file) for file in csv_files]
if df_list:
    news_df = pd.concat(df_list, ignore_index=True)
    news_df.drop_duplicates(subset='url', inplace=True)
else:
    st.warning("No news articles found. Run fetch_news first.")
    st.stop()

# --- Define your domains ---
DOMAINS = ['technology','sports','business','health','politics','climate']

# --- Streamlit UI ---
st.set_page_config(page_title="News Recommendation System", layout="wide")
st.title("News Recommendation System")

selected_domain = st.sidebar.radio("Select a Domain", DOMAINS)

# Filter articles by selected domain
domain_articles = news_df[news_df['topic'] == selected_domain]

st.subheader(f"Showing articles for: {selected_domain} ({len(domain_articles)})")

# Stream articles with thumbnails
for idx, row in domain_articles.iterrows():
    st.markdown(f"### [{row['title']}]({row['url']})")
    if pd.notna(row.get('urlToImage')):
        st.image(row['urlToImage'], width=400)
    if pd.notna(row.get('description')):
        st.write(row['description'])
    st.markdown("---")

