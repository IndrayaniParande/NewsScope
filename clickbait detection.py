import streamlit as st
from app.Model.clickbait_detection.hybrid import HybridClickbaitDetector

st.title("📰 Clickbait Detection")

detector = HybridClickbaitDetector(model_path="models/clickbait_model.pkl")

title = st.text_input("Enter News Title")
content = st.text_area("Enter News Content")

if st.button("Analyze"):
    if title.strip() and content.strip():
        label, sim_score, clf_prob = detector.predict(title, content)

        if label == 1:
            st.error(f"🔴 Clickbait Detected (sim={sim_score:.2f}, prob={clf_prob:.2f})")
        else:
            st.success(f"🟢 Not Clickbait (sim={sim_score:.2f})")
    else:
        st.warning("⚠️ Please enter both title and content.")
