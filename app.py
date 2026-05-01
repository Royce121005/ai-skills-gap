import streamlit as st
import tempfile
import os

from extractor import load_patterns, extract_skills
from normaliser import normalise
from scorer import score
from ranker import rank_gap
from parse_pdf import parse_pdf
from parse_docx import parse_docx

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillLens · AI Gap Analyser",
    page_icon="🎯",
    layout="wide"
)

# ── Load Patterns Once ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init():
    load_patterns()
    return True

init()

# ── Learning Resources ────────────────────────────────────────────────────────
LEARNING_LINKS = {
    "python":            [("Coursera", "https://www.coursera.org/learn/python"),
                          ("freeCodeCamp", "https://www.freecodecamp.org/learn/scientific-computing-with-python/")],
    "sql":               [("SQLZoo", "https://sqlzoo.net"),
                          ("W3Schools", "https://www.w3schools.com/sql/")],
    "machine learning":  [("Coursera", "https://www.coursera.org/learn/machine-learning"),
                          ("fast.ai", "https://www.fast.ai")],
    "deep learning":     [("fast.ai", "https://www.fast.ai"),
                          ("DeepLearning.AI", "https://www.deeplearning.ai")],
    "docker":            [("Docker Docs", "https://docs.docker.com/get-started/"),
                          ("KodeKloud", "https://kodekloud.com/courses/docker-for-the-absolute-beginner/")],
    "kubernetes":        [("K8s Docs", "https://kubernetes.io/docs/tutorials/"),
                          ("KodeKloud", "https://kodekloud.com/courses/kubernetes-for-the-absolute-beginners/")],
    "git":               [("Pro Git", "https://git-scm.com/book/en/v2"),
                          ("GitHub Skills", "https://skills.github.com")],
    "java":              [("Codecademy", "https://www.codecademy.com/learn/learn-java"),
                          ("MOOC.fi", "https://java-programming.mooc.fi")],
    "javascript":        [("javascript.info", "https://javascript.info"),
                          ("freeCodeCamp", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")],
    "agile":             [("Atlassian", "https://www.atlassian.com/agile"),
                          ("Scrum.org", "https://www.scrum.org/resources/what-is-scrum")],
    "communication":     [("Coursera", "https://www.coursera.org/learn/communication-skills"),
                          ("LinkedIn Learning", "https://www.linkedin.com/learning/topics/communication")],
    "flask":             [("Flask Docs", "https://flask.palletsprojects.com/en/stable/tutorial/"),
                          ("freeCodeCamp", "https://www.freecodecamp.org/news/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine/")],
    "django":            [("Django Docs", "https://docs.djangoproject.com/en/5.2/intro/tutorial01/"),
                          ("MDN", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django")],
    "data analysis":     [("Kaggle", "https://www.kaggle.com/learn/pandas"),
                          ("DataCamp", "https://www.datacamp.com/courses/data-analysis-with-python")],
    "cloud computing":   [("AWS Free Tier", "https://aws.amazon.com/free/"),
                          ("Google Cloud", "https://cloud.google.com/training/free-labs")],
    "statistics":        [("Khan Academy", "https://www.khanacademy.org/math/statistics-probability"),
                          ("StatQuest", "https://www.youtube.com/@statquest")],
    "nlp":               [("Hugging Face", "https://huggingface.co/learn/nlp-course/"),
                          ("Coursera", "https://www.coursera.org/specializations/natural-language-processing")],
    "rest api":          [("REST API Tutorial", "https://restfulapi.net/"),
                          ("Postman Learning", "https://learning.postman.com/docs/getting-started/introduction/")],
    "project management":[("PMI", "https://www.pmi.org/learning/training-development/online-courses"),
                          ("Coursera", "https://www.coursera.org/learn/project-management-foundations")],
}

def get_links(skill):
    key = skill.lower().strip()
    if key in LEARNING_LINKS:
        return LEARNING_LINKS[key]
    for k, v in LEARNING_LINKS.items():
        if k in key or key in k:
            return v
    q = skill.replace(" ", "+")
    return [("YouTube", f"https://www.youtube.com/results?search_query={q}+tutorial"),
            ("Coursera", f"https://www.coursera.org/search?query={q}")]

# ── Section Keywords ──────────────────────────────────────────────────────────
SECTIONS = {
    "Technical Skills": [
        "python","java","javascript","sql","html","css","c++","scala","flask","django",
        "pandas","machine learning","deep learning","tensorflow","pytorch","docker",
        "kubernetes","git","linux","aws","azure","gcp","nlp","mysql","wordpress",
        "database","algorithms","cloud computing","web development","agile","jira",
        "scrum","rest api","microservices","devops","automation","spark","hadoop",
        "power bi","tableau","data analysis","data science"
    ],
    "Soft Skills": [
        "communication","collaboration","time management","project management",
        "leadership","teamwork","analytical","problem solving","creativity",
        "adaptability","critical thinking","negotiation","presentation","responsible"
    ],
    "Domain Knowledge": [
        "data visualization","cybersecurity","networking","product management",
        "business analysis","computer vision","natural language processing",
        "android development","cloud computing","web development","ui design","ux design",
        "google cloud","reinforcement learning"
    ]
}

def get_breakdown(resume_skills, job_skills):
    results = {}
    for section, keywords in SECTIONS.items():
        r = [s for s in resume_skills if any(k in s.lower() for k in keywords)]
        j = [s for s in job_skills  if any(k in s.lower() for k in keywords)]
        pct = round((len(set(r) & set(j)) / len(j)) * 100) if j else 0
        results[section] = {"resume": len(r), "job": len(j), "pct": pct}
    return results

def score_color(pct):
    if pct >= 70: return "green"
    if pct >= 40: return "orange"
    return "red"

# ── UI ────────────────────────────────────────────────────────────────────────
st.title(" SkillLens — AI Skills Gap Analyser")
st.caption("Upload your resume and paste a job description to find your skill gaps instantly.")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader(" Your Resume")
    resume_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.subheader(" Job Description")
    jd_text = st.text_area("Paste the job description here", height=200)

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    analyse = st.button(" Analyse My Skills", use_container_width=True, type="primary")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyse:
    if not resume_file:
        st.warning(" Please upload your resume.")
        st.stop()
    if not jd_text.strip():
        st.warning(" Please paste a job description.")
        st.stop()

    with st.spinner("Analysing your skills..."):

        # 1. Parse resume
        suffix = ".pdf" if resume_file.name.endswith(".pdf") else ".docx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(resume_file.read())
            tmp_path = tmp.name
        r_text = parse_pdf(tmp_path) if suffix == ".pdf" else parse_docx(tmp_path)
        os.unlink(tmp_path)

        # 2. Extract skills
        r_raw = extract_skills(r_text)
        j_raw = extract_skills(jd_text)

        # 3. Semantic fallback
        try:
            import re
            from semantic import semantic_match
            jd_words = list(set(re.findall(r'\b[a-zA-Z][a-zA-Z\+\#\.]{2,}\b', jd_text.lower())))
            existing = [s.lower() for s in j_raw]
            for word in jd_words:
                if word not in existing:
                    match = semantic_match(word, threshold=0.82)
                    if match and match.lower() not in existing:
                        j_raw.append(match)
        except Exception:
            pass

        # 4. Normalise
        r_skills = [normalise(s) for s in r_raw]
        j_skills = [normalise(s) for s in j_raw]

        if not r_skills:
            st.error(" No skills found in resume. Make sure it's a text-based PDF.")
            st.stop()
        if not j_skills:
            st.error(" No skills found in job description. Try adding more technical terms.")
            st.stop()

        # 5. Score + rank
        result    = score(r_skills, j_skills)
        ranked    = rank_gap(result["gap"])
        breakdown = get_breakdown(r_skills, j_skills)
        pct       = int(result["similarity"] * 100)

    # ── Results ───────────────────────────────────────────────────────────────
    st.divider()
    st.subheader(" Analysis Results")

    # Top metrics
    m1, m2, m3 = st.columns(3)
    m1.metric(" Overall Match",   f"{pct}%")
    m2.metric(" Skills Matched",  len(result["matched"]))
    m3.metric(" Skills Missing",  len(result["gap"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Matched skills + Section breakdown
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.subheader(" Matched Skills")
        if result["matched"]:
            # Display as colored badges
            badges = " ".join(
                f'<span style="background:#1a3a2a;border:1px solid #00cc66;'
                f'color:#00cc66;padding:4px 10px;border-radius:4px;'
                f'font-size:12px;margin:3px;display:inline-block">{s}</span>'
                for s in sorted(result["matched"])
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No direct skill matches found.")

    with col_b:
        st.subheader(" Score by Section")
        for section, data in breakdown.items():
            color = score_color(data["pct"])
            st.markdown(f"**{section}** — `{data['resume']} resume · {data['job']} required`")
            st.progress(data["pct"] / 100)
            st.caption(f"{data['pct']}% match")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Skill gaps + Learning recommendations
    col_c, col_d = st.columns(2, gap="large")

    with col_c:
        st.subheader(" Skill Gaps — Ranked by Demand")
        if ranked:
            for item in ranked:
                demand = f"{item['postings']:,} postings" if item["postings"] > 0 else "in demand"
                st.markdown(
                    f'<div style="background:#2a1a1a;border:1px solid #cc3333;'
                    f'border-radius:4px;padding:8px 12px;margin-bottom:6px">'
                    f'<span style="color:#ff6666;font-weight:500">{item["skill"]}</span>'
                    f'<span style="color:#666;font-size:12px;float:right">{demand}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.success(" No skill gaps — you're a strong match!")

    with col_d:
        st.subheader(" Learning Recommendations")
        if ranked:
            for item in ranked[:6]:
                links = get_links(item["skill"])
                with st.expander(f" {item['skill']}"):
                    for name, url in links:
                        st.markdown(f"→ [{name}]({url})")
        else:
            st.success("No gaps to fill!")

    # Debug expander
    with st.expander("Debug — show extracted skills"):
        st.write("**Resume skills:**", sorted(r_skills))
        st.write("**JD skills:**", sorted(j_skills))

    st.divider()
    st.caption("SkillLens · Built with ESCO v1.1 · O*NET 28.0 · Sentence Transformers · SpaCy")