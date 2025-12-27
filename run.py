import streamlit as st
import pandas as pd
from app.collector.fetch_news import fetch_news
from app.Model.clickbait_detection1 import run_clickbait_detection

# Streamlit Page Setup
st.set_page_config(page_title="News Analyzer", layout="wide")

st.title("📰 News Analyzer")
st.markdown("Detect clickbait headlines from daily collected news articles.")

# Sidebar Options
st.sidebar.header("Options")
fetch_option = st.sidebar.checkbox("Fetch fresh news", value=True)

if fetch_option:
    st.info("Fetching the latest news from NewsAPI...")
    df_results = run_clickbait_detection()
else:
    st.warning("Using last fetched dataset instead.")
    df_results = pd.read_csv("app/collector/final_data.csv")  # fallback

# Show results
st.subheader("🔍 Clickbait Detection Results")
st.dataframe(df_results.head(20), use_container_width=True)

# Filters
st.sidebar.subheader("Filters")
clickbait_only = st.sidebar.checkbox("Show only Clickbait")

if clickbait_only:
    df_results = df_results[df_results["is_clickbait"] == True]

# Similarity Score Range
min_score, max_score = st.sidebar.slider(
    "Filter by similarity score", 0.0, 1.0, (0.0, 1.0), 0.01
)
df_results = df_results[
    (df_results["similarity_score"] >= min_score) &
    (df_results["similarity_score"] <= max_score)
]

# Display Filtered Data
st.subheader("📊 Filtered Results")
st.dataframe(df_results, use_container_width=True)

# Download option
st.download_button(
    label="Download Results as CSV",
    data=df_results.to_csv(index=False).encode("utf-8"),
    file_name="clickbait_results.csv",
    mime="text/csv"
)
