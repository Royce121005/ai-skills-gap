from sentence_transformers import SentenceTransformer, util
import sqlite3

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_skill_embeddings(db="skills.db"):
    conn = sqlite3.connect(db)
    labels = [r[0] for r in conn.execute(
        "SELECT preferredLabel FROM esco_skills "
        "WHERE skillType='skill/competence'")]
    conn.close()
    embeddings = model.encode(labels, convert_to_tensor=True)
    return labels, embeddings

LABELS, EMBEDS = None, None

def get_embeddings():
    global LABELS, EMBEDS
    if LABELS is None:
        LABELS, EMBEDS = load_skill_embeddings()
    return LABELS, EMBEDS

def semantic_match(token: str, threshold=0.82):
    labels, embeds = get_embeddings()
    q = model.encode(token, convert_to_tensor=True)
    scores = util.cos_sim(q, embeds)[0]
    best = int(scores.argmax())
    if scores[best] >= threshold:
        return labels[best]
    return None