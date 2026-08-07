# dashboard.py
import sqlite3
import curriculum as curr

DB_NAME = "student_tracker.db"

def generate_student_report(student_id):
    """Fetches tracking data from SQLite and prints a learning gap report."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch all records for the targeted student
    cursor.execute("""
        SELECT concept_id, status, attempts, last_tested 
        FROM student_state 
        WHERE student_id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print(f"\n📊 [Dashboard Error]: No learning history found for Student ID: '{student_id}'.")
        print("💡 Tip: Try playing through a module in main.py first to populate the database.")
        return

    # Calculate metrics using basic loop computation
    total_modules_tracked = len(rows)
    mastered_count = sum(1 for row in rows if row[1] == "mastered")
    mastery_rate = (mastered_count / total_modules_tracked) * 100
    
    print(f"\n==================================================")
    print(f"📈 LEARNING ANALYTICS DASHBOARD FOR: {student_id}")
    print(f"==================================================")
    print(f"• Curriculum Coverage: {total_modules_tracked} topics attempted")
    print(f"• Mastery Progress Score: {mastery_rate:.1f}%")
    print(f"--------------------------------------------------")
    
    print("\n🔍 ACTIVE KNOWLEDGE GAPS (Needs Review):")
    gaps_found = False
    for row in rows:
        concept_id, status, attempts, last_tested = row
        if status == "in_progress":
            gaps_found = True
            friendly = curr.ALGEBRA_GRAPH[concept_id]["friendly_name"]
            video = curr.ALGEBRA_GRAPH[concept_id]["resources"]
            print(f"  ❌ {friendly} ({concept_id})")
            print(f"     └─ Status: Stuck after {attempts} attempt(s) | Last active: {last_tested}")
            print(f"     └─ Recommended Resource: {video['title']} -> {video['url']}\n")
            
    if not gaps_found:
        print("  ✅ Amazing! No current knowledge gaps detected. Keep moving forward!")

    print("\n🏆 COMPLETED MASTERY BLOCKS:")
    mastered_found = False
    for row in rows:
        concept_id, status, attempts, _ = row
        if status == "mastered":
            mastered_found = True
            friendly = curr.ALGEBRA_GRAPH[concept_id]["friendly_name"]
            print(f"  ⭐ {friendly} (Solid understanding after {attempts} attempt(s))")
            
    if not mastered_found:
        print("  (No mastered modules recorded yet.)")
    print(f"==================================================\n")

if __name__ == "__main__":
    # Runs a report on our standard test student ID
    generate_student_report(student_id="highschool_student_1")
