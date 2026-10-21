import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


def get_connection():
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )
    return conn


def fetch_questions():
    try:
        conn = get_connection()
    except Exception:
        return []

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, question, answer, category, keywords, source_url, last_verified_at
                FROM questions
                ORDER BY id
                """
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except Exception:
        return []
    finally:
        conn.close()


def fetch_suggested_questions(limit: int = 5):
    rows = fetch_questions()
    if not rows:
        return []
    return rows[:limit]
