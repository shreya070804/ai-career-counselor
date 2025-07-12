
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

career_profiles = {
    "Data Scientist": "statistics machine learning python pandas data visualization",
    "Software Developer": "programming algorithms web development backend frontend debugging",
    "UI/UX Designer": "design creativity figma wireframes user experience branding",
    "Business Analyst": "analysis business models finance market strategy communication",
    "Cybersecurity Specialist": "security networks cryptography penetration testing firewalls"
}

def recommend_careers(resume_text, personality_text):
    combined_input = resume_text + " " + personality_text

    vectorizer = TfidfVectorizer()
    all_texts = [combined_input] + list(career_profiles.values())
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    user_vector = tfidf_matrix[0]
    career_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(user_vector, career_vectors)[0]

    career_scores = list(zip(career_profiles.keys(), similarities))
    top_3 = sorted(career_scores, key=lambda x: x[1], reverse=True)[:3]

    return top_3
