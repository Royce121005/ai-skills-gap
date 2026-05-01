import spacy
import sqlite3
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

SOFT_SKILLS = [
    "communication", "collaboration", "time management", "analytical",
    "problem solving", "teamwork", "leadership", "creativity",
    "adaptability", "critical thinking", "project management",
    "presentation", "negotiation", "responsible", "organised"
]

DOMAIN_SKILLS = [
    "data visualization", "cybersecurity", "networking", "product management",
    "business analysis", "computer vision", "natural language processing",
    "reinforcement learning", "android development", "cloud computing",
    "web development", "mobile development", "ui design", "ux design",
    "google cloud", "rest api", "restful api"
]

TECH_SKILLS = [
    "python", "java", "flask", "django", "pandas", "git", "agile",
    "docker", "kubernetes", "sql", "mysql", "javascript", "html", "css",
    "tensorflow", "pytorch", "scikit-learn", "numpy", "jira", "scrum",
    "linux", "aws", "azure", "gcp", "mongodb", "postgresql", "redis",
    "spark", "hadoop", "tableau", "power bi", "excel", "r", "scala",
    "kotlin", "swift", "react", "nodejs", "spring", "hibernate",
    "selenium", "jenkins", "ansible", "terraform", "bash", "c++", "c#",
    "machine learning", "deep learning", "nlp", "data analysis",
    "data science", "automation", "api", "microservices", "devops"
]

def load_patterns(db="skills.db"):
    conn = sqlite3.connect(db)
    labels = conn.execute(
        "SELECT preferredLabel FROM esco_skills").fetchall()
    esco_patterns = [nlp.make_doc(r[0]) for r in labels]
    extra = SOFT_SKILLS + DOMAIN_SKILLS + TECH_SKILLS
    extra_patterns = [nlp.make_doc(s) for s in extra]
    all_patterns = esco_patterns + extra_patterns
    matcher.add("SKILL", all_patterns)
    conn.close()
    print(f"Loaded {len(all_patterns)} skill patterns")

def extract_skills(text: str) -> list:
    doc = nlp(text)
    matches = matcher(doc)
    return list({doc[s:e].text.lower() for _, s, e in matches})