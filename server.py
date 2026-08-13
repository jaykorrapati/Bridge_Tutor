# server.py
"""
FastAPI Web Server for BridgeTutor AI Agent.
Provides REST API endpoints for curriculum graph, dynamic problem generator, real-time math engine verification, diagnostic hints, and student state tracker.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import curriculum as curr
import engine as eng
import generator as gen
import hints as hnt
import tracker as track

app = FastAPI(title="BridgeTutor AI Agent Server", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class VerifyRequest(BaseModel):
    student_id: str
    concept_id: str
    target_value: str
    student_answer: str
    question_text: str = ""
    eval_type: str = "numeric"

class HintRequest(BaseModel):
    eval_type: str
    target_value: str
    student_answer: str
    explanation: str = ""

class ResetRequest(BaseModel):
    student_id: str = "demo_student"

@app.on_event("startup")
def startup_event():
    track.init_db()

@app.get("/api/curriculum")
def get_curriculum(student_id: str = "demo_student"):
    """Returns the full curriculum DAG annotated with student progress state."""
    track.init_db()
    summary = track.get_student_summary(student_id)
    states_dict = {row[0]: row[1] for row in summary["states"]}

    graph = {}
    for concept_id, node in curr.ALGEBRA_GRAPH.items():
        prereqs = node.get("prerequisites", [])
        
        # Determine locked vs unlocked status
        all_prereqs_mastered = True
        for p in prereqs:
            if not track.is_mastered(student_id, p):
                all_prereqs_mastered = False
                break

        current_status = states_dict.get(concept_id, "unlocked" if all_prereqs_mastered else "locked")
        if current_status == "in_progress" and not all_prereqs_mastered:
            current_status = "locked"

        graph[concept_id] = {
            "concept_id": concept_id,
            "friendly_name": node["friendly_name"],
            "description": node.get("description", ""),
            "prerequisites": prereqs,
            "resources": node.get("resources", {}),
            "eval_type": node.get("eval_type", "numeric"),
            "status": current_status,
            "is_unlocked": all_prereqs_mastered
        }

    return {
        "student_id": student_id,
        "graph": graph,
        "ordered_concepts": curr.get_all_concepts()
    }

@app.get("/api/student/{student_id}")
def get_student(student_id: str):
    """Fetches student metrics, active gaps, and history."""
    summary = track.get_student_summary(student_id)
    states = summary["states"]
    total_topics = len(curr.ALGEBRA_GRAPH)
    mastered_count = sum(1 for row in states if row[1] == "mastered")
    
    gaps = []
    for row in states:
        concept_id, status, attempts, correct_count, last_tested = row
        if status == "in_progress":
            node = curr.ALGEBRA_GRAPH.get(concept_id, {})
            gaps.append({
                "concept_id": concept_id,
                "friendly_name": node.get("friendly_name", concept_id),
                "attempts": attempts,
                "correct_count": correct_count,
                "last_tested": last_tested,
                "resources": node.get("resources", {})
            })

    attempts_formatted = []
    for cid, q, ans, is_corr, ts in summary["recent_attempts"]:
        attempts_formatted.append({
            "concept_id": cid,
            "concept_name": curr.ALGEBRA_GRAPH.get(cid, {}).get("friendly_name", cid),
            "question": q,
            "student_answer": ans,
            "is_correct": bool(is_corr),
            "timestamp": ts
        })

    return {
        "student_id": student_id,
        "total_topics": total_topics,
        "mastered_count": mastered_count,
        "mastery_rate": round((mastered_count / total_topics) * 100, 1),
        "gaps": gaps,
        "recent_attempts": attempts_formatted
    }

@app.get("/api/problem/{concept_id}")
def get_problem(concept_id: str):
    """Generates a dynamic math problem with ground truth solution and explanation."""
    if concept_id not in curr.ALGEBRA_GRAPH:
        raise HTTPException(status_code=404, detail="Concept node not found.")
    problem = gen.generate_problem(concept_id)
    return problem

@app.post("/api/verify")
def verify_answer(req: VerifyRequest):
    """Validates student answer with SymPy and updates SQLite tracker."""
    is_correct, feedback = eng.check_answer_with_code(req.eval_type, req.target_value, req.student_answer)
    
    # Update tracker database
    track.update_student_state(
        student_id=req.student_id,
        concept_id=req.concept_id,
        was_correct=is_correct,
        question=req.question_text,
        student_answer=req.student_answer
    )

    # Diagnostic hints if incorrect
    diagnosis = None
    if not is_correct:
        diagnosis = hnt.diagnose_and_hint(req.eval_type, req.target_value, req.student_answer)

    is_concept_mastered = track.is_mastered(req.student_id, req.concept_id)

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "is_mastered": is_concept_mastered,
        "diagnosis": diagnosis
    }

@app.post("/api/hint")
def get_hint(req: HintRequest):
    """Returns tiered diagnostic hints for student raw input."""
    return hnt.diagnose_and_hint(req.eval_type, req.target_value, req.student_answer, req.explanation)

@app.post("/api/reset")
def reset_student(req: ResetRequest):
    """Resets student tracking history."""
    track.reset_student_data(req.student_id)
    return {"status": "success", "message": f"Data reset for student {req.student_id}"}

# Serve static web frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
