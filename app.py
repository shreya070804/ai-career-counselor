

import streamlit as st
from career_counselor import recommend_careers
import fitz  # PyMuPDF for PDF
import matplotlib.pyplot as plt
from fpdf import FPDF  # ✅ PDF generator

# ✅ PDF extractor
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

# ✅ PDF report generator
def generate_pdf(roles, scores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Career Counselor Report", ln=True, align="C")
    pdf.ln(10)

    for role, score in zip(roles, scores):
        pdf.cell(200, 10, txt=f"{role}: {score:.2f}% match", ln=True)

    output_path = "/tmp/career_report.pdf"
    pdf.output(output_path)
    return output_path


# Streamlit UI
st.set_page_config(page_title="AI Career Counselor", page_icon="🎓")
st.title("🎓 AI Career Counselor")
st.write("Upload your resume (in .txt or .pdf format) and describe yourself to get career recommendations.")

resume_file = st.file_uploader("📄 Upload Resume (.txt or .pdf)", type=["txt", "pdf"])
personality = st.text_area("🧠 Describe yourself (interests, goals, skills, etc.)")

# Button Logic
if st.button("🔍 Suggest My Career"):
    if resume_file and personality:
        # Extract resume text
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8")

        # Recommend careers
        recommendations = recommend_careers(resume_text, personality)

        # Show results
        st.success("✅ Top 3 Career Recommendations:")
        for role, score in recommendations:
            st.markdown(f"🎯 **{role}** — {score:.2%} match")

        # Show bar chart
        roles, scores = zip(*recommendations)
        scores = [s * 100 for s in scores]

        fig, ax = plt.subplots()
        ax.barh(roles, scores, color="skyblue")
        ax.set_xlabel("Match %")
        ax.set_title("Career Match Breakdown")
        st.pyplot(fig)

        # ✅ 📄 PDF Download (Indented correctly)
        pdf_path = generate_pdf(roles, scores)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_file,
                file_name="career_report.pdf",
                mime="application/pdf"
            )

    else:
        st.warning("⚠️ Please upload your resume and fill in the description.")
