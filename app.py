import streamlit as st
from career_counselor import recommend_careers

# Set page configuration
st.set_page_config(
    page_title="AI Career Counselor",
    page_icon="🎓",
    layout="centered"
)

# Title
st.markdown("<h1 style='text-align: center;'>🎓 AI Career Counselor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Let AI analyze your resume and personality to suggest the top 3 career paths for you.</p>", unsafe_allow_html=True)
st.markdown("---")

# File uploader
st.subheader("📄 Step 1: Upload Your Resume")
resume_file = st.file_uploader("Upload a `.txt` file of your resume", type=["txt"])

# Text input
st.subheader("🧠 Step 2: Describe Yourself")
personality_text = st.text_area(
    "Tell us about your interests, strengths, and goals (3–5 lines)",
    height=150,
    placeholder="Example: I enjoy solving problems, love data analysis, and aim to work in tech that impacts society..."
)

# Suggest Button
st.markdown("")

if st.button("🔍 Suggest My Career"):
    if resume_file and personality_text.strip():
        with st.spinner("Analyzing your inputs with AI..."):
            resume_text = resume_file.read().decode("utf-8")
            results = recommend_careers(resume_text, personality_text)

        st.success("✅ Top 3 Career Recommendations:")

        for idx, (career, score) in enumerate(results, start=1):
            st.markdown(f"**{idx}. {career}** — `{score:.2%}` match")

        st.markdown("---")
        st.markdown("🎉 *These results are generated using NLP and similarity scoring. Explore, learn, and grow!*")
    else:
        st.warning("⚠️ Please upload your resume and write about yourself to get recommendations.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 13px;'>Made with ❤️ by Shreya Sawant</p>", unsafe_allow_html=True)

