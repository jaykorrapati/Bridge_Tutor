# main.py
import curriculum as curr
import engine as eng
import tracker as track

def run_agent_session(student_id, target_concept_id):
    track.init_db()
    current_concept = target_concept_id
    
    while current_concept is not None:
        node = curr.ALGEBRA_GRAPH[current_concept]
        
        unmastered_prereq = None
        for prereq in node.get("prerequisites", []):
            if not track.is_mastered(student_id, prereq):
                unmastered_prereq = prereq
                break
        
        if unmastered_prereq:
            print(f"\n[BridgeTutor]: Before we tackle '{node['friendly_name']}', "
                  f"let's check your foundation block in: '{curr.ALGEBRA_GRAPH[unmastered_prereq]['friendly_name']}'...")
            current_concept = unmastered_prereq
            continue

        question_text, target_value = curr.get_random_problem(current_concept)
        
        print(f"\n=========================================")
        print(f"Topic: {node['friendly_name']}")
        print(f"=========================================")
        print(f"[BridgeTutor]: {question_text}")
        
        student_input = input("\nYour Answer (or type 'exit'): ")
        if student_input.strip().lower() == 'exit':
            break
        
        is_correct, feedback = eng.check_answer_with_code(node["eval_type"], target_value, student_input)
        print(f"\n[System Engine]: {feedback}")
        
        track.update_student_state(student_id, current_concept, is_correct)
        
        if is_correct:
            print(f"\n[BridgeTutor]: Incredible work!")
            if current_concept == target_concept_id:
                print(f"[BridgeTutor]: Mastery path complete.")
                current_concept = None
            else:
                current_concept = target_concept_id
        else:
            print(f"\n[BridgeTutor]: Let's fix this gap.")
            prereqs = node.get("prerequisites", [])
            if prereqs:
                current_concept = prereqs[0]  # Extracts string from list cleanly
            else:
                video = node.get("resources", {"title": "Review Guide", "url": "N/A"})
                print(f"[BridgeTutor]: Base layer reached. Watch: {video['title']} at {video['url']}")
                input("\nPress Enter once you've finished watching to try again...")
