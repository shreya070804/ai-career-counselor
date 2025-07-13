import streamlit as st
from career_counselor import recommend_careers
import fitz  # For PDF text extraction
import matplotlib.pyplot as plt
from fpdf import FPDF
import openai

# ✅ Load OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ✅ PDF Extraction Function
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

# ✅ Resume Scoring Function
def calculate_resume_score(text):
    score = 0
    feedback = []

    if len(text) > 1000:
        score += 30
        feedback.append("✅ Sufficient content length")
    else:
        feedback.append("⚠️ Resume is too short")

    keywords = ["project", "intern", "python", "machine learning", "data", "development", "design", "analysis", "research"]
    matched_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    score += len(matched_keywords) * 5

    if matched_keywords:
        feedback.append(f"✅ Contains keywords: {', '.join(matched_keywords)}")
    else:
        feedback.append("⚠️ No strong keywords found")

    return min(score, 100), feedback

# ✅ PDF Report Generator
def generate_pdf(roles, scores, score=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Career Counselor Report", ln=True, align="C")
    pdf.ln(10)

    if score is not None:
        pdf.cell(200, 10, txt=f"Resume Score: {score}/100", ln=True)
        pdf.ln(5)

    for role, match in zip(roles, scores):
        pdf.cell(200, 10, txt=f"{role}: {match:.2f}% match", ln=True)

    output_path = "/tmp/career_report.pdf"
    pdf.output(output_path)
    return output_path

# ✅ Course Recommendation Function
def get_course_recommendations(top_career):
    career_courses = {
        "Data Scientist": [
            ("Data Science Specialization – Coursera", "https://www.coursera.org/specializations/jhu-data-science"),
            ("Intro to Machine Learning – Udacity", "https://www.udacity.com/course/intro-to-machine-learning--ud120")
        ],
        "Web Developer": [
            ("Meta Front-End Developer – Coursera", "https://www.coursera.org/professional-certificates/meta-front-end-developer"),
            ("The Odin Project – Free", "https://www.theodinproject.com/")
        ],
        "UI/UX Designer": [
            ("Google UX Design – Coursera", "https://www.coursera.org/professional-certificates/google-ux-design"),
            ("FreeCodeCamp UX Guide", "https://www.freecodecamp.org/news/learn-ui-ux-design/")
        ],
        "AI Engineer": [
            ("AI for Everyone – Andrew Ng", "https://www.coursera.org/learn/ai-for-everyone"),
            ("Deep Learning Specialization", "https://www.coursera.org/specializations/deep-learning")
        ],
        "Cybersecurity Analyst": [
            ("IBM Cybersecurity Analyst – Coursera", "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst"),
            ("Introduction to Cybersecurity – edX", "https://www.edx.org/course/introduction-to-cybersecurity")
        ]
    }
    return career_courses.get(top_career, [])

# ✅ Streamlit Setup
st.set_page_config(page_title="AI Career Counselor & Chatbot", page_icon="🎓")
st.title("🎓 AI Career Counselor")

# === Section 1: Resume Upload and Career Suggestions ===
st.header("📄 Career Recommendations")

resume_file = st.file_uploader("Upload your resume (.txt or .pdf)", type=["txt", "pdf"])
personality = st.text_area("Describe yourself (interests, goals, skills, etc.)")

if st.button("🔍 Suggest My Career"):
    if resume_file and personality:
        if resume_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = resume_file.read().decode("utf-8")

        resume_score, feedback = calculate_resume_score(resume_text)

        st.subheader("📈 Resume Score")
        st.metric("Score", f"{resume_score}/100")
        for fb in feedback:
            st.write(fb)

        recommendations = recommend_careers(resume_text, personality)
        st.success("✅ Top 3 Career Recommendations:")
        for role, score in recommendations:
            st.markdown(f"🎯 **{role}** — {score:.2%} match")

        roles, scores = zip(*recommendations)
        scores = [s * 100 for s in scores]

        st.subheader("📊 Career Match Breakdown")
        fig, ax = plt.subplots()
        ax.barh(roles, scores, color="skyblue")
        ax.set_xlabel("Match %")
        st.pyplot(fig)

        pdf_path = generate_pdf(roles, scores, score=resume_score)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download Report as PDF", data=f, file_name="career_report.pdf", mime="application/pdf")

        top_career = roles[0]
        courses = get_course_recommendations(top_career)
        if courses:
            st.subheader(f"📚 Courses for {top_career}")
            for name, link in courses:
                st.markdown(f"- [{name}]({link})")
        else:
            st.info("No course recommendations available for this role yet.")
    else:
        st.warning("⚠️ Upload a resume and describe yourself.")

# === Section 2: Chatbot ===
st.markdown("---")
st.header("💬 Career Chatbot")
user_input = st.text_input("👤 You:", placeholder="What job suits someone good at math and design?")

if user_input:
    with st.spinner("🤖 Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly AI career counselor."},
                {"role": "user", "content": user_input}
            ]
        )
        bot_reply = response.choices[0].message["content"]
        st.success("🤖 Chatbot:")
        st.write(bot_reply)
