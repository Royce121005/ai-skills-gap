import sqlite3
import pandas as pd

def build_db(db_path="skills.db"):
    conn = sqlite3.connect(db_path)

    # ESCO skills
    esco = pd.read_csv("data/raw/skills_en.csv",
        usecols=["preferredLabel", "altLabels", "skillType"])
    esco.to_sql("esco_skills", conn, if_exists="replace", index=False)
    print(f"ESCO loaded: {len(esco)} rows")

    # O*NET Technology Skills
    onet = pd.read_csv("data/raw/Technology Skills.txt", sep="\t")
    print(f"O*NET columns: {onet.columns.tolist()}")
    onet.to_sql("onet_skills", conn, if_exists="replace", index=False)
    print(f"O*NET loaded: {len(onet)} rows")

    # LinkedIn frequency
    freq = pd.read_csv("data/raw/skill_counts.csv")
    freq.to_sql("linkedin_freq", conn, if_exists="replace", index=False)
    print(f"Frequency loaded: {len(freq)} rows")

    conn.close()
    print("\nskills.db built ✓")

if __name__ == "__main__":
    build_db()