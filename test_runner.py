# test_runner.py
"""
Automated CLI Integration Test Runner.
Executes a deterministic simulated student session through main.py and prints SQLite DB persistence metrics.
"""

import os
import sqlite3
import curriculum as curr
import main as mn
import tracker as track

def setup_mock_student_session():
    if os.path.exists("student_tracker.db"):
        try:
            os.remove("student_tracker.db")
        except Exception:
            pass
    track.init_db()

class DeterministicStudentSimulator:
    def __init__(self):
        self.step_counter = 0

    def generate_simulated_input(self, prompt=""):
        self.step_counter += 1
        # Step 1: Wrong answer on base layer (negative_numbers)
        if self.step_counter == 1: return "wrong negative"
        # Step 2: Press enter after video resource prompt
        if self.step_counter == 2: return ""
        # Step 3: Correct negative_numbers answer 1
        if self.step_counter == 3: return "-22"
        # Step 4: Correct negative_numbers answer 2 -> achieve mastery
        if self.step_counter == 4: return "-5"
        return "exit"

if __name__ == "__main__":
    setup_mock_student_session()
    simulator = DeterministicStudentSimulator()
    mn.input = simulator.generate_simulated_input
    
    print("▶️ Running Deterministic Student Session Simulation...")
    try:
        mn.run_agent_session("dynamic_test_user", "negative_numbers", use_dynamic=False)
        print("\n✅ Simulation completed cleanly!")
    except Exception as e:
        print(f"\n❌ Pipeline failure: {str(e)}")

    print("\n=========================================\n📊 DB PERSISTENCE REPORT\n=========================================")
    with sqlite3.connect("student_tracker.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT concept_id, status, attempts, correct_count FROM student_state WHERE student_id = 'dynamic_test_user'")
        for row in cursor.fetchall():
            concept, status, attempts, correct = row
            print(f"Concept: {concept:<25} | Status: {status:<12} | Score: {correct}/{attempts}")
