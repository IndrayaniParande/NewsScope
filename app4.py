import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

from app.Model.clickbait_detection.hybrid import HybridClickbaitDetector
from app.collector.fetch_news1 import fetch_news1
from app.Model.Text_summerizer import tweet_generator

st.set_page_config(page_title="News Analyzer", layout="wide")

# --- Custom CSS for theming ---
page_bg = """
<style>
/* Page Background */
[data-testid="stAppViewContainer"] {
    background-color: rgb(255, 255, 255) !important; /* White background */
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
    background: rgba(0,0,0,0) !important; /* Transparent */
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
    color: red !important; /* Red */
    text-align: center !important;
}

/* Normal Markdown text (p, li) */
p, li {
    color: #3498db !important; /* Blue text */
    font-size: 16px !important;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)


detector = HybridClickbaitDetector()
data_dir = "newsapi_daily_data"
os.makedirs(data_dir, exist_ok=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Clickbait Detection", "Dashboard"])

# HOME PAGE
if page == "Home":
    st.title(" Welcome to News Analyzer")
    st.image("news_analyzer.png",  use_container_width=True)
    st.markdown("### Latest  News")
    col1, col2 = st.columns([2,1])

    with col1:
        st.info("This tool analyzes news headlines for clickbait and provides summaries.")
    with col2:
        if st.button("Refresh News!"):
            news_df = fetch_news1()
            if news_df is not None and not news_df.empty:
                st.session_state["home_news"] = news_df.head(10)

        if "home_news" in st.session_state:
            for _, row in st.session_state["home_news"].iterrows():
                st.markdown(f"**[{row['title']}]({row['url']})**")
                st.caption(f"Source: {row.get('source','unknown')}")
                st.divider()

# CLICKBAIT DETECTION
elif page == "Clickbait Detection":
    st.title("Clickbait Detection")

    tab1, tab2 = st.tabs(["Fetch & Analyze News", "Manual Check"])

    # TAB 1: Fetch & Analyze
    with tab1:
        st.subheader("Fetch Latest News and Detect Clickbait")
        limit = st.selectbox(
            "Select number of articles to analyze",
             options=[10,25,50,75,100]
        )

        if st.button("Fetch Latest News"):
            with st.spinner("Fetching news... please wait."):
                news_df = fetch_news1()

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
                        tweet_summary = tweet_generator(title, description)

                        results.append({
                            "title": title,
                            "content": content,
                            "is_clickbait": label,
                            "similarity_score": sim_score,
                            "clf_prob": clf_prob,
                            "tweet_summary": tweet_summary,
                        })

                    df_results = pd.DataFrame(results)
                    st.session_state['clickbait_results'] = df_results

            if 'clickbait_results' in st.session_state:
                df_results = st.session_state['clickbait_results']

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown('<div class="metric-purple">', unsafe_allow_html=True)
                    st.metric("Average similarity", f"{df_results['similarity_score'].mean():.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="metric-orange">', unsafe_allow_html=True)
                    st.metric("Clickbait", f"{df_results['is_clickbait'].sum()}/{len(df_results)}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="metric-teal">', unsafe_allow_html=True)
                    st.metric("Relevant", f"{len(df_results) - df_results['is_clickbait'].sum()}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # metrics CSS - updated colors
                st.markdown("""
                    <style> 
                    .metric-purple [data-testid="stMetricValue"] {
                        background-color: #9b59b6 !important; /* Purple */
                        padding: 10px;
                        border-radius: 8px;
                        color: white !important;
                    }
                    .metric-orange [data-testid="stMetricValue"] {
                        background-color: #e67e22 !important; /* Orange */
                        padding: 10px;
                        border-radius: 8px;
                        color: white !important;
                    }
                    .metric-teal [data-testid="stMetricValue"] {
                        background-color: #1abc9c !important; /* Teal */
                        padding: 10px;
                        border-radius: 8px;
                        color: white !important;
                    }
                    .metric-purple [data-testid="stMetricLabel"],
                    .metric-orange [data-testid="stMetricLabel"],
                    .metric-teal [data-testid="stMetricLabel"] {
                    color: #ffffffcc !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                st.subheader("Results with summaries")
                for _, row in df_results.iterrows():
                    with st.expander(row['title']):
                        st.write(f"{row['tweet_summary']}")
                        if row["is_clickbait"] == 1:
                            st.error( f"🔴 Misleading (sim={row['similarity_score']:.2f}, prob={row['clf_prob']:.2f})")
                        else:
                            st.success(f"🟢 Relevant (sim={row['similarity_score']:.2f})")

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
                summary = tweet_generator(title_input, content_input)
                tweet_summary = summary['tweet_summary']
                if label == 1:
                    st.error(f"🔴 Clickbait detected! (sim={sim_score:.2f}, prob={clf_prob:.2f})")
                else:
                    st.success(f"🟢 Relevant article (sim={sim_score:.2f})")
                st.markdown("Summary")
                st.write(tweet_summary)
            else:
                st.warning("Please enter a news title.")

# DASHBOARD
elif page == "Dashboard":
    st.title("News Dashboard")

    if 'clickbait_results' not in st.session_state:
        st.warning("Run clickbait detection first to generate data")
    else:
        df = st.session_state["clickbait_results"]

        ##Distribution chart
        st.subheader("Clickbait Distribution")
        fig, ax = plt.subplots()
        counts = df['is_clickbait'].value_counts().reindex([0, 1], fill_value=0)
        counts.plot(kind='bar', ax=ax, color=['teal', 'orange'])
        ax.set_xticklabels(['Relevant', 'Clickbait'], rotation=0)
        st.pyplot(fig)

        ##Clickbait wordcloud
        st.subheader("Common words in Clickbait Headlines")
        text =" ".join(df[df['is_clickbait'] == 1]['title'])
        if text.strip():
            wc = WordCloud(width=800, height=400,background_color="white").generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation= "bilinear")
            ax.axis("off")
            st.pyplot(fig)

        ##Non-clickbait wordcloud
        st.subheader("Common words in Relevant Headlines")
        text = " ".join(df[df['is_clickbait'] == 0]['title'])
        if text.strip():
            wc = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
