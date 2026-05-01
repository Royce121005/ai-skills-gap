import sqlite3

def rank_gap(gap: list, db="skills.db") -> list:
    if not gap:
        return []
    conn = sqlite3.connect(db)
    placeholders = ",".join("?" * len(gap))
    rows = conn.execute(
        f"SELECT skill_name, job_postings FROM linkedin_freq "
        f"WHERE lower(skill_name) IN ({placeholders}) "
        f"ORDER BY job_postings DESC",
        [s.lower() for s in gap]).fetchall()
    conn.close()
    found = {r[0].lower() for r in rows}
    extra = [{"skill": s, "postings": 0}
             for s in gap if s.lower() not in found]
    return [{"skill": r[0], "postings": r[1]} for r in rows] + extra