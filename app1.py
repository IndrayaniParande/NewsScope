import streamlit as st
import pandas as pd
import os

from app.Model.clickbait_detection.hybrid import HybridClickbaitDetector
from app.collector.fetch_news import fetch_news


st.set_page_config(page_title="News Analyzer", layout="wide")
st.title(" News Analyzer")
st.markdown("Detect **clickbait headlines** using a hybrid ML + similarity approach.")

# Directory where results will be saved
DATA_DIR = "app/collector/newsapi_daily_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize hybrid detector
detector = HybridClickbaitDetector()

# -------------------
# Sidebar Options
# -------------------
st.sidebar.header("Options")

# 1. Fetch Latest News
if st.sidebar.button("🔄 Fetch Latest News"):
    with st.spinner("Fetching fresh news... please wait."):
        news_df = fetch_news()

        # Apply hybrid detection
        results = []
        for _, row in news_df.iterrows():
            title = row["title"]
            content = row.get("content", "")

            label, sim_score, clf_prob = detector.predict(title, content)
            results.append({
                "title": title,
                "is_clickbait": label,
                "similarity_score": sim_score,
                "clf_prob": clf_prob
            })

        df_results = pd.DataFrame(results)

        # Save results
        latest_file = os.path.join(DATA_DIR, "latest_results.csv")
        df_results.to_csv(latest_file, index=False)
        st.success(f"✅ Fetched {len(df_results)} articles and saved to {latest_file}")
else:
    # 2. Load saved results
    latest_file = os.path.join(DATA_DIR, "latest_results.csv")
    if os.path.exists(latest_file):
        df_results = pd.read_csv(latest_file)
        st.info("📂 Loaded previously saved results.")
    else:
        st.warning("⚠️ No data found. Please fetch latest news first.")
        df_results = pd.DataFrame(columns=["title", "is_clickbait", "similarity_score", "clf_prob"])

# -------------------
# Display Results
# -------------------
if not df_results.empty:
    st.subheader("🔍 Hybrid Clickbait Detection Results")

    # --- Metrics ---
    avg_similarity = df_results["similarity_score"].mean()
    total_clickbait = df_results["is_clickbait"].sum()
    total_articles = len(df_results)

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Avg Similarity Score", f"{avg_similarity:.2f}")
    col2.metric("⚠️ Clickbait Articles", f"{total_clickbait}/{total_articles}")
    col3.metric("✅ Relevant Articles", f"{total_articles - total_clickbait}")

    # --- Label Column ---
    def label_row(row):
        if row["is_clickbait"] == 1:
            return f"🔴 Clickbait (sim={row['similarity_score']:.2f}, prob={row['clf_prob']:.2f})"
        else:
            return f"🟢 Relevant (sim={row['similarity_score']:.2f})"

    df_results["Label"] = df_results.apply(label_row, axis=1)

    # -------------------
    # Filters
    # -------------------
    st.sidebar.subheader("Filters")
    clickbait_only = st.sidebar.checkbox("Show only Clickbait")

    filtered_df = df_results.copy()
    if clickbait_only:
        filtered_df = filtered_df[filtered_df["is_clickbait"] == 1]

    # Similarity filter
    min_score, max_score = st.sidebar.slider(
        "Filter by similarity score", 0.0, 1.0, (0.0, 1.0), 0.01
    )
    filtered_df = filtered_df[
        (filtered_df["similarity_score"] >= min_score) &
        (filtered_df["similarity_score"] <= max_score)
    ]

    # -------------------
    # Display Table
    # -------------------
    st.subheader("📊 Filtered Results")
    st.dataframe(filtered_df[["title", "Label"]], use_container_width=True)

    # Download Option
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="clickbait_results.csv",
        mime="text/csv"
    )


st.set_page_config(page_title="News Analyzer", layout="wide")


page_bg = """
<style>
/* Page Background */
[data-testid="stAppViewContainer"] {
    background-color: #f4f7fc;  /* Light grayish-blue background */
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #0d1b2a; /* Dark Blue */
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Title (h1) */
h1 {
    color: #0d1b2a !important;  /* Dark Blue */
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

/* Subheadings (h2, h3, h4) */
h2, h3, h4 {
    color: #1a3e72 !important; /* Medium Dark Blue */
    text-align: center;
}

/* Normal Markdown text (p) */
p, li {
    color: #0d1b2a !important; /* Dark Blue */
    font-size: 16px;
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


page_bg = """
<style>
/* Page Background */
[data-testid="stAppViewContainer"] {
    background-color: #f4f7fc;  /* Light grayish-blue background */
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #0d1b2a; /* Dark Blue */
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Title (h1) */
h1 {
    color: #0d1b2a !important;  /* Dark Blue */
    text-align: center;
    font-size: 40px;
    font-weight: bold;
}

/* Subheadings (h2, h3, h4) */
h2, h3, h4 {
    color: #1a3e72 !important; /* Medium Dark Blue */
    text-align: center;
}

/* Normal Markdown text (p) */
p, li {
    color: #0d1b2a !important; /* Dark Blue */
    font-size: 16px;
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
# ---------------- CLICKBAIT DETECTION ----------------
elif page == "Clickbait Detection":
    st.title("Clickbait Detection")

    tab1, tab2 = st.tabs(["Fetch & Analyze News", " Manual Check"])

    # ----------- TAB 1: Fetch & Analyze -----------
    with tab1:
        st.subheader("Fetch Latest News and Detect Clickbait")

        if st.button("Fetch Latest News"):
            with st.spinner("Fetching news... please wait."):
                news_df = fetch_news()

                results = []
                for _, row in news_df.iterrows():
                    title = row["title"]
                    content = row.get("content", "")
                    label, sim_score, clf_prob = detector.predict(title,content)

                    results.append({
                        "title": title,
                        "is_clickbait": label,
                        "similarity_score": sim_score,
                        "clf_prob": clf_prob
                    })

                df_results = pd.DataFrame(results)

                # Save results
                latest_file = os.path.join(Data_dir, "latest_results.csv")
                df_results.to_csv(latest_file, index=False)
                st.success(f" Fetched {len(df_results)} articles and saved to {latest_file}")

        # Load saved results if available
        latest_file = os.path.join(Data_dir, "latest_results.csv")
        if os.path.exists(latest_file):
            df_results = pd.read_csv(latest_file)
            st.info("Loaded latest results.")

            # Metrics
            avg_similarity = df_results["similarity_score"].mean()
            total_clickbait = df_results["is_clickbait"].sum()
            total_articles = len(df_results)

            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Similarity", f"{avg_similarity:.2f}")
            col2.metric("Clickbait", f"{total_clickbait}/{total_articles}")
            col3.metric("Relevant", f"{total_articles - total_clickbait}")

            # Label Column
            def label_row(row):
                if row["is_clickbait"] == 1:
                    return f"🔴 Misleading (sim={row['similarity_score']:.2f}, prob={row['clf_prob']:.2f})"
                else:
                    return f"🟢 Relevant (sim={row['similarity_score']:.2f})"

            df_results["Label"] = df_results.apply(label_row, axis=1)

            # Show filtered table
            st.subheader("Results")
            st.dataframe(df_results[["title", "Label"]], use_container_width=True)

            # Download option
            st.download_button(
                label="⬇ Download Results as CSV",
                data=df_results.to_csv(index=False).encode("utf-8"),
                file_name="clickbait_results.csv",
                mime="text/csv"
            )

    # ----------- TAB 2: Manual Check -----------
    with tab2:
        st.subheader("Check a Custom News Article")

        title_input = st.text_input("Enter News Title")
        content_input = st.text_area("Enter News Content (optional)")

        if st.button("Detect Clickbait"):
            if title_input.strip():
                label, sim_score, clf_prob = detector.predict(title_input, content_input)

                if label == 1:
                    st.error(f"🔴 Clickbait detected! (sim={sim_score:.2f}, prob={clf_prob:.2f})")
                else:
                    st.success(f"🟢 Relevant article (sim={sim_score:.2f})")
            else:
                st.warning("Please enter a news title.")




                # Metrics
                avg_similarity = df_results["similarity_score"].mean()
                total_clickbait = df_results["is_clickbait"].sum()
                total_articles = len(df_results)

                col1, col2, col3 = st.columns(3)
                col1.metric("Avg Similarity", f"{avg_similarity:.2f}")
                col2.metric("Clickbait", f"{total_clickbait}/{total_articles}")
                col3.metric("Relevant", f"{total_articles - total_clickbait}")