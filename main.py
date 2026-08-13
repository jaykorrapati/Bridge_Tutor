# main.py
"""
BridgeTutor AI Agent CLI Orchestrator.
Manages user interactions, prerequisite diagnosis, math evaluation, dynamic problem generation, and hinting.
"""

import curriculum as curr
import engine as eng
import generator as gen
import hints as hnt
import tracker as track

def run_agent_session(student_id="default_student", target_concept_id="linear_slopes", use_dynamic=True):
    track.init_db()
    current_concept = target_concept_id
    
    print("\n==================================================")
    print("🎓 WELCOME TO BRIDGETUTOR AI AGENT")
    print(f"Student ID: {student_id} | Target Concept: {curr.ALGEBRA_GRAPH.get(target_concept_id, {}).get('friendly_name')}")
    print("==================================================")
    print("💡 Commands during practice: 'hint' for hints, 'exit' to stop.\n")

    while current_concept is not None:
        node = curr.ALGEBRA_GRAPH.get(current_concept)
        if not node:
            print(f"Error: Concept '{current_concept}' not found in curriculum graph.")
            break
        
        # Check prerequisite mastery chain
        unmastered_prereq = None
        for prereq in node.get("prerequisites", []):
            if not track.is_mastered(student_id, prereq):
                unmastered_prereq = prereq
                break
        
        if unmastered_prereq:
            prereq_node = curr.ALGEBRA_GRAPH[unmastered_prereq]
            print(f"\n[BridgeTutor]: Before we tackle '{node['friendly_name']}', "
                  f"let's check your foundation block in: '{prereq_node['friendly_name']}'...")
            current_concept = unmastered_prereq
            continue

        # Problem retrieval / dynamic generation
        if use_dynamic:
            problem_data = gen.generate_problem(current_concept)
            question_text = problem_data["question"]
            target_value = problem_data["target_value"]
            explanation = problem_data["explanation"]
        else:
            question_text, target_value = curr.get_random_problem(current_concept)
            explanation = f"Target value: {target_value}"

        print(f"\n=========================================")
        print(f"Topic: {node['friendly_name']}")
        print(f"=========================================")
        print(f"[BridgeTutor]: {question_text}")
        
        hint_requested = False
        while True:
            student_input = input("\nYour Answer (or type 'hint' / 'exit'): ").strip()
            
            if student_input.lower() == 'exit':
                print("\n[BridgeTutor]: Goodbye! Progress saved.")
                return
            
            if student_input.lower() == 'hint':
                hint_data = hnt.diagnose_and_hint(node["eval_type"], target_value, "", explanation)
                print(f"\n💡 [BridgeTutor Hint 1]: {hint_data['hint_level1']}")
                print(f"💡 [BridgeTutor Hint 2]: {hint_data['hint_level2']}")
                hint_requested = True
                continue
            
            break

        is_correct, feedback = eng.check_answer_with_code(node["eval_type"], target_value, student_input)
        print(f"\n[System Engine]: {feedback}")
        
        # Update SQLite database
        track.update_student_state(student_id, current_concept, is_correct, question_text, student_input)
        
        if is_correct:
            print(f"\n[BridgeTutor]: Incredible work!")
            if current_concept == target_concept_id:
                print(f"[BridgeTutor]: 🎉 Target concept '{node['friendly_name']}' mastered successfully!")
                current_concept = None
            else:
                current_concept = target_concept_id
        else:
            # Diagnostic hint on wrong answer
            diag = hnt.diagnose_and_hint(node["eval_type"], target_value, student_input, explanation)
            print(f"\n🔍 [Diagnostic Analysis]: {diag['diagnosis']}")
            print(f"💡 [Hint]: {diag['hint_level1']}")
            
            prereqs = node.get("prerequisites", [])
            if prereqs:
                current_concept = prereqs[0]
                print(f"[BridgeTutor]: Falling back to prerequisite: '{curr.ALGEBRA_GRAPH[current_concept]['friendly_name']}'")
            else:
                video = node.get("resources", {"title": "Review Guide", "url": "N/A"})
                print(f"\n[BridgeTutor]: Base layer reached. Recommended resource: {video['title']} at {video['url']}")
                print(f"Explanation: {explanation}")
                input_action = input("\nPress Enter to try another problem (or type 'exit'): ").strip()
                if input_action.lower() == 'exit':
                    break

if __name__ == "__main__":
    run_agent_session("student_cli_demo", "linear_slopes")
