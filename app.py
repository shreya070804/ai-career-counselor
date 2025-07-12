
import streamlit as st
from career_counselor import recommend_careers

st.title("🎓 AI Career Counselor")
st.write("Upload your resume and describe yourself to get your top 3 career matches!")

resume_file = st.file_uploader("📄 Upload Resume (.txt)", type=["txt"])
personality_text = st.text_area("🧠 Describe Yourself (strengths, interests, goals)", height=150)

if st.button("🔍 Suggest My Career"):
    if resume_file and personality_text:
        resume_text = resume_file.read().decode("utf-8")
        results = recommend_careers(resume_text, personality_text)

        st.success("✅ Top 3 Career Recommendations:")
        for career, score in results:
            st.write(f"🎯 **{career}** — {score:.2%} confidence")
    else:
        st.warning("⚠️ Please upload a resume and describe yourself.")
