def recommend_careers(resume_text, personality_text):
    careers = {
        "Data Scientist": ["python", "machine learning", "data", "pandas", "numpy", "analysis"],
        "Software Developer": ["java", "c++", "javascript", "git", "development", "debugging"],
        "UI/UX Designer": ["design", "figma", "user", "prototype", "adobe"],
        "Product Manager": ["strategy", "leadership", "communication", "planning", "roadmap"],
        "Cybersecurity Analyst": ["security", "network", "vulnerability", "firewall", "encryption"]
    }
    full_text = (resume_text + " " + personality_text).lower()
    scores = []
    for role, keywords in careers.items():
        match_count = sum(1 for kw in keywords if kw in full_text)
        score = match_count / len(keywords)
        scores.append((role, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:3]

