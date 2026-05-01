from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score(resume_skills: list, job_skills: list) -> dict:
    if not resume_skills or not job_skills:
        return {"similarity": 0.0, "matched": [], "gap": job_skills}
    
    docs = [" ".join(resume_skills), " ".join(job_skills)]
    vec = TfidfVectorizer().fit_transform(docs)
    sim = cosine_similarity(vec[0], vec[1])[0][0]
    matched = list(set(resume_skills) & set(job_skills))
    gap = list(set(job_skills) - set(resume_skills))
    return {"similarity": round(float(sim), 3),
            "matched": matched,
            "gap": gap}