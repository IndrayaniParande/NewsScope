import streamlit as st
import pandas as pd
import os


from app.Model.clickbait_detection.hybrid import HybridClickbaitDetector
from app.collector.fetch_news1 import fetch_news1
from app.Model.Text_summerizer import tweet_generator

@st.cache_data(show_spinner=False)
def generate_tweet(title, description):
    result = tweet_generator(title, description, max_len=80, min_len=30)
    return result.get("tweet_summary", "")

detector = HybridClickbaitDetector()
data_dir = "newsapi_daily_data"
os.makedirs(data_dir, exist_ok=True)

# Cache function
@st.cache_data(show_spinner=False)
def get_latest_news():
    today_file_pattern = os.path.join(data_dir, f"newsapi_data_{(pd.Timestamp.now() - pd.Timedelta(1, unit='d')).strftime('%Y-%m-%d')}*.csv")
    existing_files = [f for f in os.listdir(data_dir) if f.startswith(f"newsapi_data_{(pd.Timestamp.now() - pd.Timedelta(1, unit='d')).strftime('%Y-%m-%d')}")]

    if existing_files:
        latest_file = max(existing_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
        df = pd.read_csv(os.path.join(data_dir, latest_file))
        return df
    else:
        df = fetch_news1()
        return df


st.set_page_config(page_title="News Analyzer", layout="wide")

page_bg = """
<style>
/* Page Background */
[data-testid="stAppViewContainer"] {
    background-color: rgb(255, 255, 255) !important; /* Light grayish-blue background */
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #0d1b2a !important; /* Dark Blue */
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}

/* Title (h1) */
h1 {
    color: #0d1b2a !important;  /* Dark Blue */
    text-align: center !important;
    font-size: 40px !important;
    font-weight: bold !important;
}

/* Subheadings (h2, h3, h4) */
h2, h3, h4 {
    color: red !important; /* Changed to Red */
    text-align: center !important;
}

/* Normal Markdown text (p) */
p, li {
    color: #3498db !important; /* green */
    font-size: 16px !important;
}

</style>
"""


st.markdown(page_bg, unsafe_allow_html=True)
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Clickbait Detection"])

# HOME PAGE
if page == "Home":
    st.title(" Welcome to News Analyzer")
    st.image("news_analyzer.png", use_container_width=True)
# clickbait detection
elif page == "Clickbait Detection":
    st.title("Clickbait Detection")

    tab1, tab2 = st.tabs(["Fetch & Analyze News", "Manual Check"])

    # TAB 1: Fetch & Analyze
    with tab1:
        st.subheader("Fetch Latest News and Detect Clickbait")
        limit = st.selectbox(
            "Select number of articles to analyze",
            options=[10,25,50,75,100],
            index=0
        )

        if st.button("Fetch Latest News"):
            with st.spinner("Fetching news... please wait."):
                news_df = get_latest_news()

                if news_df is None or news_df.empty:
                    st.warning("No articles found today.")
                else:
                    news_df = news_df.head(limit)

                    results = []
                    for _, row in news_df.iterrows():
                        title = row["title"]
                        description = row.get("description", "")
                        content = row.get("content", "")
                        label, sim_score, clf_prob = detector.predict(title,content)
                        tweet_summary = generate_tweet(title, description)

                        results.append({
                            "title": title,
                            "description": description,
                            "content": content,
                            "is_clickbait": label,
                            "similarity_score": sim_score,
                            "clf_prob": clf_prob,
                            "tweet_summary": tweet_summary,
                        })

                    df_results = pd.DataFrame(results)

                    latest_file = os.path.join(data_dir, "latest_results.csv")
                    df_results.to_csv(latest_file, index=False)
                    st.success(f" Fetched {len(df_results)} articles and saved to {latest_file}")

            latest_file = os.path.join(data_dir, "latest_results.csv")
            if os.path.exists(latest_file):
                df_results = pd.read_csv(latest_file)
                st.info("Loaded latest results.")

                avg_similarity = df_results["similarity_score"].mean()
                total_clickbait = df_results["is_clickbait"].sum()
                total_articles = len(df_results)

                st.markdown("""
                    <style>
                    .metric-container {
                        display: flex;
                        justify-content: space-around;
                        margin-top: 20px;
                        margin-bottom: 20px;
                    }
                    .metric-box {
                        flex: 1;
                        margin: 0 10px;
                        padding: 20px;
                        border-radius: 12px;
                        text-align: center;
                        font-weight: bold;
                        font-size: 26px;
                        color: white;
                        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
                    }
                    .blue {background-color: #3498db;}
                    .red {background-color: #e74c3c;}
                    .green {background-color: #2ecc71;}
                    .label {
                        font-size: 16px;
                        font-weight: normal;
                        display: block;
                        margin-bottom: 8px;
                        color: #ffffffcc;
                    }
                    </style>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-box blue">
                        <span class="label">Avg Similarity</span>
                        {avg_similarity:.2f}
                    </div>
                    <div class="metric-box red">
                        <span class="label">Clickbait</span>
                        {total_clickbait}/{total_articles}
                    </div>
                    <div class="metric-box green">
                        <span class="label">Relevant</span>
                        {total_articles - total_clickbait}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                def label_row(row):
                    if row["is_clickbait"] == 1:
                        return f"🔴 Misleading (sim={row['similarity_score']:.2f}, prob={row['clf_prob']:.2f})"
                    else:
                        return f"🟢 Relevant (sim={row['similarity_score']:.2f})"
                df_results["Label"] = df_results.apply(label_row, axis=1)

                st.subheader("Results with tweet Summaries")
                st.dataframe(df_results[["title", "tweet_summary", "Label"]], use_container_width=True)
                st.download_button(
                    label="⬇ Download Results as CSV",
                    data=df_results.to_csv(index=False).encode("utf-8"),
                    file_name="clickbait_results.csv",
                    mime="text/csv"
                )

    # TAB 2: Manual Check
    with tab2:
        st.subheader("Check a Custom News Article")
        title_input = st.text_input("Enter News Title").strip()
        content_input = st.text_area("Enter News Content (optional)").strip()

        if st.button("Detect Clickbait"):
            if title_input.strip():
                label, sim_score, clf_prob = detector.predict(title_input, content_input)
                print(f"{label}: {sim_score:.2f}, {clf_prob}")

                if label == 1:
                    st.error(f"🔴 Clickbait detected! (sim={sim_score:.2f}, prob={clf_prob:.2f})")
                else:
                    st.success(f"🟢 Relevant article (sim={sim_score:.2f})")
            else:
                st.warning("Please enter a news title.")


