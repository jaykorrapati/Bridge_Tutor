# test_runner.py
import os
import sqlite3
import curriculum as curr
import main as mn
import tracker as track

def setup_mock_student_session():
    if os.path.exists(track.DB_NAME):
        os.remove(track.DB_NAME)
    track.init_db()

class DeterministicStudentSimulator:
    def __init__(self):
        self.step_counter = 0

    def generate_simulated_input(self, prompt=""):
        self.step_counter += 1
        if self.step_counter == 1: return "incorrect slope math"
        if self.step_counter == 2: return "bad equation input"
        if self.step_counter == 3: return ""  # Presses enter at video
        if self.step_counter == 4: return "-22" # Matches custom curriculum change variant
        if self.step_counter == 5: return "x = 4"
        if self.step_counter == 6: return "3/2"
        return "0"

if __name__ == "__main__":
    setup_mock_student_session()
    simulator = DeterministicStudentSimulator()
    mn.input = simulator.generate_simulated_input
    
    try:
        mn.run_agent_session("dynamic_test_user", "linear_slopes")
    except Exception as e:
        print(f"\n❌ Pipeline failure: {str(e)}")

    print("\n=========================================\n📊 DB PERSISTENCE REPORT\n=========================================")
    with sqlite3.connect(track.DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT concept_id, status, attempts FROM student_state")
        for row in cursor.fetchall():
            concept, status, attempts = row
            print(f"Concept: {concept:<25} | Status: {status:<12} | Total Attempts: {attempts}")
