import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from app.services.news_service import get_latest_news
from app.services.clickbait_service import analyze_article
from app.services.summarization_service import summarize_article

st.set_page_config(page_title="News Analyzer", layout="wide")

# --- Custom CSS for theme ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] { background-color: white !important; }
[data-testid="stSidebar"] { background-color: #0d1b2a !important; }
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }

h1 {
    color: #0d1b2a !important;
    text-align: center !important;
    font-size: 40px !important;
    font-weight: bold !important;
}

h2, h3, h4 {
    color: red !important;
    text-align: center !important;
}

p, li {
    color: #3498db !important;
    font-size: 16px !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Clickbait Detection", "Dashboard"])

# ================= HOME =================
if page == "Home":
    st.title("Welcome to News Analyzer")
    st.image("news_analyzer.png", use_container_width=True)
    st.markdown("### Latest News")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info("This tool analyzes news headlines for clickbait and provides summaries.")

    with col2:
        if st.button("Refresh News!"):
            news_df = get_latest_news()
            if not news_df.empty:
                st.session_state["home_news"] = news_df.head(10)

        if "home_news" in st.session_state:
            for _, row in st.session_state["home_news"].iterrows():
                st.markdown(f"**[{row['title']}]({row['url']})**")
                st.caption(f"Source: {row.get('source', 'unknown')}")
                st.divider()

# ================= CLICKBAIT =================
elif page == "Clickbait Detection":
    st.title("Clickbait Detection")

    tab1, tab2 = st.tabs(["Fetch & Analyze News", "Manual Check"])

    # ---------- TAB 1 ----------
    with tab1:
        limit = st.selectbox("Select number of articles", [10, 25, 50, 75, 100])

        if st.button("Fetch Latest News"):
            with st.spinner("Fetching news..."):
                news_df = get_latest_news()

            if news_df.empty:
                st.warning("No articles found.")
            else:
                news_df = news_df.head(limit)
                results = []

                for _, row in news_df.iterrows():
                    title = row["title"]
                    description = row.get("description", "")
                    content = row.get("content", "")

                    result = analyze_article(title, content)
                    summary = summarize_article(title, description)

                    results.append({
                        "title": title,
                        "is_clickbait": result["is_clickbait"],
                        "similarity_score": result["similarity_score"],
                        "clf_prob": result["clf_prob"],
                        "tweet_summary": summary["tweet_summary"]
                    })

                st.session_state["clickbait_results"] = pd.DataFrame(results)

        if "clickbait_results" in st.session_state:
            df = st.session_state["clickbait_results"]

            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Similarity", f"{df['similarity_score'].mean():.2f}")
            col2.metric("Clickbait", f"{df['is_clickbait'].sum()}")
            col3.metric("Relevant", f"{len(df) - df['is_clickbait'].sum()}")

            for _, row in df.iterrows():
                with st.expander(row["title"]):
                    st.write(row["tweet_summary"])
                    if row["is_clickbait"]:
                        st.error(f"🔴 Clickbait (prob={row['clf_prob']:.2f})")
                    else:
                        st.success("🟢 Relevant")

    # ---------- TAB 2 ----------
    with tab2:
        title_input = st.text_input("Enter News Title")
        content_input = st.text_area("Enter News Content (optional)")

        if st.button("Detect Clickbait"):
            if title_input.strip():
                result = analyze_article(title_input, content_input)
                summary = summarize_article(title_input, content_input)

                if result["is_clickbait"]:
                    st.error("🔴 Clickbait detected")
                else:
                    st.success("🟢 Relevant article")

                st.markdown("### Summary")
                st.write(summary["tweet_summary"])
            else:
                st.warning("Please enter a title.")

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("News Dashboard")

    if "clickbait_results" not in st.session_state:
        st.warning("Run clickbait detection first.")
    else:
        df = st.session_state["clickbait_results"]

        st.subheader("Clickbait Distribution")
        fig, ax = plt.subplots()
        df["is_clickbait"].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.subheader("Clickbait WordCloud")
        text = " ".join(df[df["is_clickbait"] == 1]["title"])
        if text:
            wc = WordCloud(width=800, height=400).generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)
