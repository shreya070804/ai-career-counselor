def recommend_careers(resume_text, personality_text):
    # Define example roles and their keyword matches
    careers = {
        "Data Scientist": ["python", "machine learning", "data", "pandas", "numpy", "analysis"],
        "Software Developer": ["java", "c++", "javascript", "git", "development", "debugging"],
        "UI/UX Designer": ["design", "figma", "user", "interface", "prototype", "adobe"],
        "Product Manager": ["strategy", "leadership", "communication", "planning", "roadmap"],
        "Cybersecurity Analyst": ["security", "network", "vulnerability", "firewall", "encryption"]
    }

    # Combine inputs and lowercase
    full_text = (resume_text + " " + personality_text).lower()

    # Score each role
    scores = []
    for role, keywords in careers.items():
        match_count = sum(1 for kw in keywords if kw in full_text)
        score = match_count / len(keywords)
        scores.append((role, score))

    # Return top 3 roles
    return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
