
# BridgeTutor AI Agent Blueprint
This document preserves the structural architecture, logic, and context for building the Mastery-Based Learning Agent for High School Algebra.
## 🏗️ Project Architecture

┌─────────────────────────────┐
│ main.py │
│ (The Orchestrator / Agent) │
└──────┬───────────────┬──────┘
│ │
┌──────────────────▼───┐ ┌───▼──────────────────┐
│ curriculum.py │ │ tracker.py │
│ (The Map & Videos) │ │ (The Database/Memory)│
└──────────────────────┘ └──────────────────────┘
│
┌──────────────────▼───┐
│ engine.py │
│ (The Math Solver) │
└──────────────────────┘


## 🧠 Core File Responsibilities

1. **`main.py` (The Heart):** Manages user text input/output loops. Coordinates data exchange between curriculum maps, the math execution layer, and the long-term memory engine.
2. **`curriculum.py` (The Hierarchy Graph):** Maps out Middle and High School Algebra concepts into a directed graph of nodes. Connects prerequisite tags and curated YouTube resource links (e.g., Gilbert Strang, Khan Academy) directly to specific concepts.
3. **`engine.py` (The Code Validator):** Uses the `SymPy` symbolic math library to process open-ended user text. Evaluates algebraic and numeric equivalence precisely (e.g., matches `0.5`, `1/2`, and `2/4` perfectly) to eliminate AI hallucinations.
4. **`tracker.py` (The Long-Term Memory):** Provisions an isolated local SQLite database (`student_tracker.db`). Manages user state properties (`unlocked`, `in_progress`, `mastered`) to instantly resume learning sessions and identify persistent knowledge gaps.

## ⚙️ Dependencies & Tech Stack
- **Language:** Python 3.8+
- **Database Engine:** SQLite (Native to Python)
- **Math Logic Engine:** SymPy (`pip install sympy`)

