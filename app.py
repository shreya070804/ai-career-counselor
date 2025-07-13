import streamlit as st
from career_counselor import recommend_careers

st.set_page_config(page_title="AI Career Counselor", page_icon="🎓")
st.title("🎓 AI Career Counselor")

st.write("Upload your resume (in .txt format) and describe yourself to get career recommendations.")

resume_file = st.file_uploader("📄 Upload Resume (.txt)", type=["txt"])
personality = st.text_area("🧠 Describe yourself (interests, goals, skills, etc.)")

if st.button("🔍 Suggest My Career"):
    if resume_file and personality:
        resume_text = resume_file.read().decode("utf-8")
        recommendations = recommend_careers(resume_text, personality)

        st.success("✅ Top 3 Career Recommendations:")
        for role, score in recommendations:
            st.markdown(f"🎯 **{role}** — {score:.2%} match")
    else:
        st.warning("⚠️ Please upload your resume and fill in the description.")


