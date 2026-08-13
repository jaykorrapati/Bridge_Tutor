# curriculum.py
"""
Curriculum DAG (Directed Acyclic Graph) for Middle and High School Algebra.
Defines concept nodes, prerequisites, curated learning resources, and default problem banks.
"""

import random

ALGEBRA_GRAPH = {
    "negative_numbers": {
        "friendly_name": "Negative Numbers & Absolute Value",
        "description": "Operations with positive and negative integers, absolute value calculations.",
        "prerequisites": [],
        "resources": {"title": "Math Antics - Negative Numbers", "url": "https://www.youtube.com/watch?v=OAoLcXijh6E"},
        "eval_type": "numeric",
        "problem_bank": [
            {"question": "What is the value of -15 + (-7)?", "target_value": "-22", "explanation": "-15 + (-7) = -22"},
            {"question": "What is the value of -9 - (-4)?", "target_value": "-5", "explanation": "-9 - (-4) = -9 + 4 = -5"},
            {"question": "Evaluate the absolute value expression: |-12| + (-3)", "target_value": "9", "explanation": "|-12| = 12, so 12 + (-3) = 9"}
        ]
    },
    "order_of_operations": {
        "friendly_name": "Order of Operations (PEMDAS)",
        "description": "Evaluating numerical expressions following parentheses, exponents, multiplication, division, addition, and subtraction.",
        "prerequisites": ["negative_numbers"],
        "resources": {"title": "Khan Academy - Intro to Order of Operations", "url": "https://www.youtube.com/watch?v=dAgfnKK577U"},
        "eval_type": "numeric",
        "problem_bank": [
            {"question": "Evaluate: 3 + 4 * (2 - 5)", "target_value": "-9", "explanation": "2 - 5 = -3; 4 * (-3) = -12; 3 + (-12) = -9"},
            {"question": "Evaluate: (-2)^3 + 5 * 3", "target_value": "7", "explanation": "(-2)^3 = -8; 5 * 3 = 15; -8 + 15 = 7"},
            {"question": "Evaluate: 18 / (3 + 3) - 7", "target_value": "-4", "explanation": "3 + 3 = 6; 18 / 6 = 3; 3 - 7 = -4"}
        ]
    },
    "combining_like_terms": {
        "friendly_name": "Combining Like Terms & Simplifying",
        "description": "Simplifying algebraic expressions by grouping terms with matching variable powers.",
        "prerequisites": ["order_of_operations"],
        "resources": {"title": "Math Antics - Simplifying Algebraic Expressions", "url": "https://www.youtube.com/watch?v=352B1gVvNxs"},
        "eval_type": "symbolic",
        "problem_bank": [
            {"question": "Simplify: 4x + 7 - 2x + 3", "target_value": "2*x + 10", "explanation": "(4x - 2x) + (7 + 3) = 2x + 10"},
            {"question": "Simplify: 3(x + 4) - 5x", "target_value": "-2*x + 12", "explanation": "3x + 12 - 5x = -2x + 12"},
            {"question": "Simplify: 5y - 2(3 - 2y)", "target_value": "9*y - 6", "explanation": "5y - 6 + 4y = 9y - 6"}
        ]
    },
    "variable_isolation": {
        "friendly_name": "Solving One-Variable Equations",
        "description": "Using inverse operations to isolate a variable on one side of an equation.",
        "prerequisites": ["combining_like_terms"],
        "resources": {"title": "Khan Academy - Solving 2-Step Equations", "url": "https://www.youtube.com/watch?v=LDIiYKYvvdA"},
        "eval_type": "equation_solve",
        "problem_bank": [
            {"question": "Solve for x: 4x - 5 = 11", "target_value": "4", "explanation": "4x = 16 => x = 4"},
            {"question": "Solve for x: 3x + 7 = -2", "target_value": "-3", "explanation": "3x = -9 => x = -3"},
            {"question": "Solve for x: 5x - 12 = 18", "target_value": "6", "explanation": "5x = 30 => x = 6"}
        ]
    },
    "multi_step_equations": {
        "friendly_name": "Multi-Step & Distributive Equations",
        "description": "Solving equations with variables on both sides and parenthetical terms.",
        "prerequisites": ["variable_isolation"],
        "resources": {"title": "Brian McLogan - Multi-Step Equations", "url": "https://www.youtube.com/watch?v=1c5HY3z4k8Q"},
        "eval_type": "equation_solve",
        "problem_bank": [
            {"question": "Solve for x: 2(x + 3) = 4x - 2", "target_value": "4", "explanation": "2x + 6 = 4x - 2 => 8 = 2x => x = 4"},
            {"question": "Solve for x: 3(2x - 1) = 3x + 9", "target_value": "4", "explanation": "6x - 3 = 3x + 9 => 3x = 12 => x = 4"},
            {"question": "Solve for x: 5 - 2(x - 1) = x + 1", "target_value": "2", "explanation": "5 - 2x + 2 = x + 1 => 7 - 2x = x + 1 => 6 = 3x => x = 2"}
        ]
    },
    "linear_slopes": {
        "friendly_name": "Calculating Slopes from Two Points",
        "description": "Finding the rate of change m = (y2 - y1) / (x2 - x1) between Cartesian coordinate pairs.",
        "prerequisites": ["multi_step_equations"],
        "resources": {"title": "Brian McLogan - Finding Slope", "url": "https://www.youtube.com/watch?v=R948Tsyq4vA"},
        "eval_type": "numeric",
        "problem_bank": [
            {"question": "Find the slope of a line passing through (1, 2) and (3, 5). Write as a fraction or decimal.", "target_value": "3/2", "explanation": "m = (5 - 2)/(3 - 1) = 3/2"},
            {"question": "Find the slope of a line passing through (0, 0) and (2, -4).", "target_value": "-2", "explanation": "m = (-4 - 0)/(2 - 0) = -4/2 = -2"},
            {"question": "Find the slope of a line passing through (-1, 3) and (2, 5). Write as a fraction.", "target_value": "2/3", "explanation": "m = (5 - 3)/(2 - (-1)) = 2/3"}
        ]
    },
    "slope_intercept_form": {
        "friendly_name": "Linear Equations in Slope-Intercept Form (y = mx + b)",
        "description": "Identifying and converting equations to y = mx + b to find slope m and y-intercept b.",
        "prerequisites": ["linear_slopes"],
        "resources": {"title": "Khan Academy - Slope-Intercept Form", "url": "https://www.youtube.com/watch?v=uk7gS3cZNqc"},
        "eval_type": "symbolic",
        "problem_bank": [
            {"question": "Convert 2x + y = 5 into slope-intercept form (y = ...). What is the expression for y?", "target_value": "-2*x + 5", "explanation": "Subtract 2x: y = -2x + 5"},
            {"question": "What is the y-intercept b of the line 3x - 2y = 8? (Enter a number or fraction)", "target_value": "-4", "explanation": "Set x = 0 => -2y = 8 => y = -4"},
            {"question": "Write the line expression y for slope m = 3 and y-intercept b = -2.", "target_value": "3*x - 2", "explanation": "y = 3x - 2"}
        ]
    },
    "systems_of_equations": {
        "friendly_name": "Systems of Two Linear Equations",
        "description": "Solving two simultaneous linear equations for intersection point (x, y) using substitution or elimination.",
        "prerequisites": ["slope_intercept_form"],
        "resources": {"title": "The Organic Chemistry Tutor - Systems of Equations", "url": "https://www.youtube.com/watch?v=vA-55wIs5yU"},
        "eval_type": "coordinate",
        "problem_bank": [
            {"question": "Solve the system: x + y = 5 and x - y = 1. Enter answer as (x, y).", "target_value": "(3, 2)", "explanation": "Adding equations gives 2x = 6 => x = 3; then 3 + y = 5 => y = 2"},
            {"question": "Solve the system: 2x + y = 7 and y = x + 1. Enter answer as (x, y).", "target_value": "(2, 3)", "explanation": "Substitute: 2x + (x + 1) = 7 => 3x = 6 => x = 2, y = 3"},
            {"question": "Solve the system: 3x + 2y = 12 and x = 2. Enter answer as (x, y).", "target_value": "(2, 3)", "explanation": "3(2) + 2y = 12 => 6 + 2y = 12 => y = 3"}
        ]
    },
    "factoring_quadratics": {
        "friendly_name": "Factoring Quadratic Expressions",
        "description": "Factoring trinomials x^2 + bx + c into binomial products (x + p)(x + q).",
        "prerequisites": ["multi_step_equations"],
        "resources": {"title": "Math Antics - Factoring Quadratics", "url": "https://www.youtube.com/watch?v=r3yd_4V375I"},
        "eval_type": "symbolic",
        "problem_bank": [
            {"question": "Factor the quadratic expression: x^2 + 5x + 6", "target_value": "(x + 2)*(x + 3)", "explanation": "2 * 3 = 6 and 2 + 3 = 5, so (x + 2)(x + 3)"},
            {"question": "Factor the quadratic expression: x^2 - 7x + 12", "target_value": "(x - 3)*(x - 4)", "explanation": "-3 * -4 = 12 and -3 + -4 = -7, so (x - 3)(x - 4)"},
            {"question": "Factor the difference of squares: x^2 - 16", "target_value": "(x - 4)*(x + 4)", "explanation": "x^2 - 4^2 = (x - 4)(x + 4)"}
        ]
    },
    "quadratic_formula": {
        "friendly_name": "Solving Quadratics with Quadratic Formula",
        "description": "Solving ax^2 + bx + c = 0 using x = (-b +- sqrt(b^2 - 4ac)) / (2a).",
        "prerequisites": ["factoring_quadratics"],
        "resources": {"title": "Khan Academy - Quadratic Formula", "url": "https://www.youtube.com/watch?v=i7idZfS8t0w"},
        "eval_type": "equation_solve",
        "problem_bank": [
            {"question": "Find the positive root of x^2 - 4x - 5 = 0.", "target_value": "5", "explanation": "(x - 5)(x + 1) = 0 => x = 5 or x = -1. Positive root is 5."},
            {"question": "Solve for x: x^2 - 9 = 0 (Enter either root: 3 or -3).", "target_value": "3", "explanation": "x^2 = 9 => x = 3 or x = -3"},
            {"question": "What is the discriminant (b^2 - 4ac) of 2x^2 + 3x - 2 = 0?", "target_value": "25", "explanation": "b^2 - 4ac = 3^2 - 4(2)(-2) = 9 + 16 = 25"}
        ]
    }
}

def get_all_concepts():
    """Returns a list of all concept identifiers in topological/logical order."""
    return list(ALGEBRA_GRAPH.keys())

def get_concept_node(concept_id):
    """Retrieves metadata dict for a given concept ID."""
    return ALGEBRA_GRAPH.get(concept_id)

def get_random_problem(concept_id):
    """Fallback static problem getter from curated problem bank."""
    node = ALGEBRA_GRAPH.get(concept_id)
    if not node or not node.get("problem_bank"):
        raise ValueError(f"Concept '{concept_id}' not found in curriculum.")
    problem = random.choice(node["problem_bank"])
    return problem["question"], problem["target_value"]

def validate_curriculum_dag():
    """Validates that all prerequisites exist and there are no cycles in the graph."""
    visited = set()
    rec_stack = set()

    def dfs(node_id):
        visited.add(node_id)
        rec_stack.add(node_id)

        node = ALGEBRA_GRAPH.get(node_id)
        if not node:
            raise ValueError(f"Prerequisite node '{node_id}' missing in ALGEBRA_GRAPH.")

        for prereq in node.get("prerequisites", []):
            if prereq not in visited:
                dfs(prereq)
            elif prereq in rec_stack:
                raise ValueError(f"Cycle detected in curriculum graph involving node '{prereq}'!")

        rec_stack.remove(node_id)

    for concept_id in ALGEBRA_GRAPH:
        if concept_id not in visited:
            dfs(concept_id)

    return True
