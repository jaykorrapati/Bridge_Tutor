# tracker.py
import sqlite3
from datetime import datetime

# Enforces a proper file URI scheme for precise macOS file permissions
DB_NAME = "file:student_tracker.db?mode=rw"

def init_db():
    """Initializes the database schema by explicitly creating the file if missing."""
    # We use a standard connection without flags just to generate the file blank first
    with sqlite3.connect("student_tracker.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_state (
                student_id TEXT,
                concept_id TEXT,
                status TEXT,
                attempts INTEGER,
                last_tested TEXT,
                PRIMARY KEY (student_id, concept_id)
            )
        """)
        conn.commit()

def is_mastered(student_id, concept_id):
    # URI=True ensures the mode=rw parameter is interpreted properly
    with sqlite3.connect(DB_NAME, uri=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM student_state WHERE student_id = ? AND concept_id = ?", 
            (student_id, concept_id)
        )
        row = cursor.fetchone()
        return row is not None and row[0] == "mastered"

def update_student_state(student_id, concept_id, was_correct):
    with sqlite3.connect(DB_NAME, uri=True) as conn:
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            "SELECT status, attempts FROM student_state WHERE student_id = ? AND concept_id = ?", 
            (student_id, concept_id)
        )
        row = cursor.fetchone()
        
        if row is None:
            status = "mastered" if was_correct else "in_progress"
            cursor.execute("""
                INSERT INTO student_state (student_id, concept_id, status, attempts, last_tested)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, concept_id, status, 1, current_time))
        else:
            current_status, current_attempts = row
            status = "mastered" if (was_correct or current_status == "mastered") else "in_progress"
            cursor.execute("""
                UPDATE student_state 
                SET status = ?, attempts = ?, last_tested = ?
                WHERE student_id = ? AND concept_id = ?
            """, (status, current_attempts + 1, current_time, student_id, concept_id))
        conn.commit()
