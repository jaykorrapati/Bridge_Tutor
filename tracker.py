# tracker.py
"""
Long-Term Memory Engine & Student Mastery Tracker using SQLite.
Stores concept state, attempt histories, and performance analytics.
"""

import os
import sqlite3
from datetime import datetime

DB_FILE = "student_tracker.db"

def get_db_connection():
    """Returns a SQLite connection object with proper timeout settings."""
    conn = sqlite3.connect(DB_FILE, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes SQLite schema for student state tracking and attempt logs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_state (
                student_id TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('in_progress', 'mastered')),
                attempts INTEGER NOT NULL DEFAULT 0,
                correct_count INTEGER NOT NULL DEFAULT 0,
                last_tested TEXT NOT NULL,
                PRIMARY KEY (student_id, concept_id)
            )
        """)
        
        # Schema migration check for existing databases
        cursor.execute("PRAGMA table_info(student_state)")
        cols = [c[1] for c in cursor.fetchall()]
        if cols and "correct_count" not in cols:
            cursor.execute("ALTER TABLE student_state ADD COLUMN correct_count INTEGER NOT NULL DEFAULT 0;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                question TEXT NOT NULL,
                student_answer TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def is_mastered(student_id, concept_id):
    """Checks if a student has achieved mastery status for a given concept."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM student_state WHERE student_id = ? AND concept_id = ?", 
            (student_id, concept_id)
        )
        row = cursor.fetchone()
        return row is not None and row[0] == "mastered"

def update_student_state(student_id, concept_id, was_correct, question="", student_answer="", mastery_threshold=2):
    """
    Updates student record. Requires 'mastery_threshold' correct attempts (or past mastery) to unlock 'mastered'.
    """
    init_db()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Log granular attempt
        cursor.execute("""
            INSERT INTO attempt_history (student_id, concept_id, question, student_answer, is_correct, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, concept_id, str(question), str(student_answer), 1 if was_correct else 0, current_time))
        
        # Query current state
        cursor.execute(
            "SELECT status, attempts, correct_count FROM student_state WHERE student_id = ? AND concept_id = ?", 
            (student_id, concept_id)
        )
        row = cursor.fetchone()

        if row is None:
            new_correct = 1 if was_correct else 0
            new_status = "mastered" if new_correct >= mastery_threshold else "in_progress"
            cursor.execute("""
                INSERT INTO student_state (student_id, concept_id, status, attempts, correct_count, last_tested)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student_id, concept_id, new_status, 1, new_correct, current_time))
        else:
            current_status, attempts, correct_count = row
            new_attempts = attempts + 1
            new_correct = (correct_count + 1) if was_correct else correct_count
            
            # Mastered if already mastered or reached threshold
            new_status = "mastered" if (current_status == "mastered" or new_correct >= mastery_threshold) else "in_progress"
            
            cursor.execute("""
                UPDATE student_state 
                SET status = ?, attempts = ?, correct_count = ?, last_tested = ?
                WHERE student_id = ? AND concept_id = ?
            """, (new_status, new_attempts, new_correct, current_time, student_id, concept_id))
            
        conn.commit()

def get_student_summary(student_id):
    """Fetches full state summary and attempts data for a specific student."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT concept_id, status, attempts, correct_count, last_tested
            FROM student_state
            WHERE student_id = ?
        """, (student_id,))
        state_rows = cursor.fetchall()

        cursor.execute("""
            SELECT concept_id, question, student_answer, is_correct, timestamp
            FROM attempt_history
            WHERE student_id = ?
            ORDER BY id DESC LIMIT 10
        """, (student_id,))
        recent_attempts = cursor.fetchall()

    return {
        "student_id": student_id,
        "states": state_rows,
        "recent_attempts": recent_attempts
    }

def reset_student_data(student_id=None):
    """Resets tracking database for testing or specific student."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if student_id:
            cursor.execute("DELETE FROM student_state WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM attempt_history WHERE student_id = ?", (student_id,))
        else:
            cursor.execute("DELETE FROM student_state")
            cursor.execute("DELETE FROM attempt_history")
        conn.commit()
