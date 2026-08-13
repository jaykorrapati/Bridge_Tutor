# dashboard.py
"""
CLI Analytics Dashboard for BridgeTutor AI Agent.
Generates terminal reports on student progress, mastery rates, active knowledge gaps, and attempt logs.
"""

import sqlite3
import curriculum as curr
import tracker as track

def generate_student_report(student_id="student_cli_demo"):
    """Fetches state and attempt logs from SQLite to print a visual terminal dashboard."""
    data = track.get_student_summary(student_id)
    state_rows = data["states"]
    recent_attempts = data["recent_attempts"]

    if not state_rows:
        print(f"\n📊 [Dashboard Error]: No learning history found for Student ID: '{student_id}'.")
        print("💡 Tip: Play through a practice session in main.py first to populate tracker data.")
        return

    total_topics = len(curr.ALGEBRA_GRAPH)
    attempted_topics = len(state_rows)
    mastered_count = sum(1 for row in state_rows if row[1] == "mastered")
    mastery_rate = (mastered_count / total_topics) * 100

    # Progress bar rendering
    bar_length = 20
    filled_length = int(bar_length * mastered_count // total_topics)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)

    print(f"\n==================================================")
    print(f"📈 LEARNING ANALYTICS DASHBOARD FOR: {student_id}")
    print(f"==================================================")
    print(f"• Overall Mastery Progress: [{bar}] {mastery_rate:.1f}% ({mastered_count}/{total_topics} Topics Mastered)")
    print(f"• Topics Attempted: {attempted_topics} of {total_topics} curriculum nodes")
    print(f"--------------------------------------------------")

    print("\n🔍 ACTIVE KNOWLEDGE GAPS (In Progress):")
    gaps_found = False
    for row in state_rows:
        concept_id, status, attempts, correct_count, last_tested = row
        if status == "in_progress":
            gaps_found = True
            node = curr.ALGEBRA_GRAPH.get(concept_id, {})
            friendly = node.get("friendly_name", concept_id)
            video = node.get("resources", {"title": "Resource Guide", "url": "N/A"})
            print(f"  ❌ {friendly} ({concept_id})")
            print(f"     ├─ Score: {correct_count}/{attempts} correct | Last active: {last_tested}")
            print(f"     └─ Recommended Resource: {video['title']} -> {video['url']}\n")

    if not gaps_found:
        print("  ✅ Great job! No active knowledge gaps detected.")

    print("\n🏆 MASTERED CURRICULUM BLOCKS:")
    mastered_found = False
    for row in state_rows:
        concept_id, status, attempts, correct_count, _ = row
        if status == "mastered":
            mastered_found = True
            friendly = curr.ALGEBRA_GRAPH.get(concept_id, {}).get("friendly_name", concept_id)
            print(f"  ⭐ {friendly} ({correct_count}/{attempts} correct - Solid understanding)")

    if not mastered_found:
        print("  (No mastered modules recorded yet.)")

    if recent_attempts:
        print("\n📜 RECENT PRACTICE ATTEMPTS:")
        for concept_id, question, student_ans, is_corr, ts in recent_attempts[:5]:
            icon = "✅" if is_corr else "❌"
            print(f"  {icon} [{ts}] {concept_id}: '{student_ans}' on question '{question[:40]}...'")

    print(f"==================================================\n")

if __name__ == "__main__":
    generate_student_report("student_cli_demo")
