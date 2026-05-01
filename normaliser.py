import sqlite3

def normalise(skill: str, db="skills.db") -> str:
    conn = sqlite3.connect(db)
    # Try exact preferredLabel match
    row = conn.execute(
        "SELECT preferredLabel FROM esco_skills "
        "WHERE lower(preferredLabel)=?", (skill.lower(),)).fetchone()
    if row:
        conn.close()
        return row[0]
    # Try altLabels
    rows = conn.execute(
        "SELECT preferredLabel, altLabels FROM esco_skills"
    ).fetchall()
    for pref, alts in rows:
        if alts and skill.lower() in alts.lower():
            conn.close()
            return pref
    conn.close()
    return skill