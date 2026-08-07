# curriculum.py
import random

ALGEBRA_GRAPH = {
    "negative_numbers": {
        "friendly_name": "Negative Numbers & Absolute Value",
        "prerequisites": [],
        "resources": {"title": "Math Antics - Negative Numbers", "url": "https://youtu.be"},
        "eval_type": "numeric",
        "problem_bank": [
            {"question": "What is the value of -15 + (-7)?", "target_value": "-22"},
            {"question": "What is the value of -9 - (-4)?", "target_value": "-5"},
            {"question": "Evaluate the absolute value expression: |-12| + (-3)", "target_value": "9"}
        ]
    },
    "variable_isolation": {
        "friendly_name": "Solving One-Variable Equations",
        "prerequisites": ["negative_numbers"],
        "resources": {"title": "Khan Academy - Isolation of Variables", "url": "https://youtu.be"},
        "eval_type": "equation_solve",
        "problem_bank": [
            {"question": "Solve for x: 4x - 5 = 11", "target_value": "4"},
            {"question": "Solve for x: 3x + 7 = -2", "target_value": "-3"},
            {"question": "Solve for x: 5x - 12 = 18", "target_value": "6"}
        ]
    },
    "linear_slopes": {
        "friendly_name": "Calculating Slopes from Two Points",
        "prerequisites": ["variable_isolation"],
        "resources": {"title": "Brian McLogan - Finding Slope", "url": "https://youtu.be"},
        "eval_type": "numeric",
        "problem_bank": [
            {"question": "Find the slope of a line passing through (1, 2) and (3, 5). Write as a decimal or fraction.", "target_value": "3/2"},
            {"question": "Find the slope of a line passing through (0, 0) and (2, -4).", "target_value": "-2"},
            {"question": "Find the slope of a line passing through (-1, 3) and (2, 5). Write as a fraction.", "target_value": "2/3"}
        ]
    }
}

def get_random_problem(concept_id):
    node = ALGEBRA_GRAPH[concept_id]
    problem = random.choice(node["problem_bank"])
    return problem["question"], problem["target_value"]
