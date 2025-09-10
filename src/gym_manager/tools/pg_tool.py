import os
import psycopg2
from psycopg2.extras import DictCursor
from crewai.tools import tool
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

DB_URL = os.getenv("DATABASE_URL")

def _get_db_connection():
    """Establishes and returns a database connection."""
    if not DB_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    return psycopg2.connect(DB_URL)

@tool("insert_summary_tool")
def insert_summary_tool(summary: dict) -> str:
    """
    Insert a workout summary into the Postgres workout_summaries table.
    Expected keys: date, gym, muscle_trained, summary, pain_experienced, pain_details
    """
    conn = _get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO workout_summaries (date, gym, muscle_trained, summary, pain_experienced, pain_details)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO UPDATE
                SET gym = EXCLUDED.gym,
                    muscle_trained = EXCLUDED.muscle_trained,
                    summary = EXCLUDED.summary,
                    pain_experienced = EXCLUDED.pain_experienced,
                    pain_details = EXCLUDED.pain_details;
            """, (
                summary.get("date"),
                summary.get("gym"),
                summary.get("muscle_trained"),
                summary.get("summary"),
                summary.get("pain_experienced"),
                summary.get("pain_details"),
            ))
            conn.commit()
        return f"Inserted/Updated summary for {summary.get('date')}"
    finally:
        conn.close()

@tool("fetch_latest_summary_tool")
def fetch_latest_summary_tool(placeholder: str = "") -> str:
    """
    Fetch the most recent workout summary from Postgres.
    """
    conn = _get_db_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM workout_summaries ORDER BY date DESC LIMIT 1;")
            row = cur.fetchone()
            if not row:
                return "No summaries found."
            return dict(row)
    finally:
        conn.close()
