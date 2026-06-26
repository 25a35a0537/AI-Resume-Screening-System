import sqlite3

DATABASE = "resumes.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT,
        score REAL,
        job_title TEXT,
        required_education TEXT,
        required_experience TEXT,
        required_skills TEXT,
        resume TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_candidate(candidate):

    conn = get_connection()

    conn.execute("""
    INSERT OR REPLACE INTO candidates
    (
        name,
        email,
        phone,
        skills,
        education,
        experience,
        score,
        job_title,
        required_education,
        required_experience,
        required_skills,
        resume
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        candidate["name"],
        candidate["email"],
        candidate["phone"],
        ", ".join(candidate["skills"]),
        ", ".join(candidate["education"]),
        str(candidate["experience"]),
        candidate["score"],
        candidate["job_title"],
        candidate["required_education"],
        candidate["required_experience"],
        ", ".join(candidate["required_skills"]),
        candidate["resume"]
    ))

    conn.commit()
    conn.close()


def get_candidates():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM candidates ORDER BY score DESC"
    ).fetchall()

    conn.close()

    return rows


def delete_candidate(candidate_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM candidates WHERE id=?",
        (candidate_id,)
    )

    conn.commit()
    conn.close()
