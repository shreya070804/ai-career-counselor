import streamlit as st
from career_counselor import recommend_careers
import fitz  # PyMuPDF for PDF extraction

# PDF extractor
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

st.set_page_config(page_title="AI Career Counselor", page_icon="🎓")
st.title("🎓 AI Career Counselor")
st.write("Upload your resume (in .txt or .pdf format) and describe yourself to get career recommendations.")

resume_file = st.file_uploader("📄 Upload Resume (.txt or .pdf)", type=["txt", "pdf"])
personality = st.text_area("🧠 Describe yourself (interests, goals, skills, etc.)")

if st.button("🔍 Suggest My Career"):
    if resume_file and personality:
        # Check file type
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8")

        recommendations = recommend_careers(resume_text, personality)

        st.success("✅ Top 3 Career Recommendations:")
        for role, score in recommendations:
            st.markdown(f"🎯 **{role}** — {score:.2%} match")
    else:
        st.warning("⚠️ Please upload your resume and fill in the description.")




