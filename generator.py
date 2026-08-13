# generator.py
"""
Procedural Math Problem Generator using SymPy & Python Random.
Generates endless unique algebraic problems with ground-truth solutions and step-by-step derivations.
"""

import random
import sympy as sp
from curriculum import ALGEBRA_GRAPH, get_random_problem

def generate_problem(concept_id, seed=None):
    """
    Generates a dynamic math problem dictionary for a specific concept node.
    Returns: {
        "question": str,
        "tex_question": str,
        "target_value": str,
        "explanation": str,
        "eval_type": str
    }
    """
    if seed is not None:
        random.seed(seed)

    node = ALGEBRA_GRAPH.get(concept_id)
    if not node:
        raise ValueError(f"Unknown concept_id: {concept_id}")

    eval_type = node.get("eval_type", "numeric")

    try:
        if concept_id == "negative_numbers":
            op_type = random.choice(["add", "sub", "abs"])
            if op_type == "add":
                a = random.randint(-20, -1)
                b = random.randint(-20, 15)
                val = a + b
                q = f"What is the value of {a} + ({b})?"
                tex_q = f"\\text{{Evaluate: }} {a} + ({b})"
                exp = f"{a} + ({b}) = {val}"
                ans = str(val)
            elif op_type == "sub":
                a = random.randint(-20, 10)
                b = random.randint(-20, -1)
                val = a - b
                q = f"What is the value of {a} - ({b})?"
                tex_q = f"\\text{{Evaluate: }} {a} - ({b})"
                exp = f"{a} - ({b}) = {a} + ({-b}) = {val}"
                ans = str(val)
            else:
                a = random.randint(-25, -5)
                b = random.randint(-15, 15)
                val = abs(a) + b
                q = f"Evaluate the absolute value expression: |{a}| + ({b})"
                tex_q = f"\\text{{Evaluate: }} |{a}| + ({b})"
                exp = f"|{a}| = {-a}, so {-a} + ({b}) = {val}"
                ans = str(val)

        elif concept_id == "order_of_operations":
            a = random.randint(2, 6)
            b = random.randint(2, 5)
            c = random.randint(1, 8)
            d = random.randint(2, 10)
            val = a + b * (c - d)
            q = f"Evaluate: {a} + {b} * ({c} - {d})"
            tex_q = f"\\text{{Evaluate: }} {a} + {b} \\cdot ({c} - {d})"
            exp = f"1. Parentheses: {c} - {d} = {c - d}\n2. Multiply: {b} * ({c - d}) = {b * (c - d)}\n3. Add: {a} + ({b * (c - d)}) = {val}"
            ans = str(val)

        elif concept_id == "combining_like_terms":
            x = sp.Symbol('x')
            a = random.randint(2, 8)
            b = random.randint(1, 10) * random.choice([1, -1])
            c = random.randint(2, 6) * random.choice([1, -1])
            d = random.randint(1, 10) * random.choice([1, -1])
            
            expr = a * x + b + c * x + d
            simplified = sp.simplify(expr)
            
            q = f"Simplify the algebraic expression: {a}x + ({b}) + ({c}x) + ({d})"
            tex_q = f"\\text{{Simplify: }} {sp.latex(expr)}"
            exp = f"Group x terms ({a}x + {c}x) and constants ({b} + {d}) => {sp.pretty(simplified)}"
            ans = str(simplified)

        elif concept_id == "variable_isolation":
            x = sp.Symbol('x')
            solution = random.randint(-10, 10)
            a = random.randint(2, 9) * random.choice([1, -1])
            b = random.randint(1, 15) * random.choice([1, -1])
            rhs = a * solution + b

            q = f"Solve for x: {a}x + ({b}) = {rhs}"
            tex_q = f"\\text{{Solve for }} x: {a}x + ({b}) = {rhs}"
            exp = f"1. Subtract ({b}) from both sides: {a}x = {rhs - b}\n2. Divide by {a}: x = {solution}"
            ans = str(solution)

        elif concept_id == "multi_step_equations":
            x = sp.Symbol('x')
            solution = random.randint(-8, 8)
            a = random.randint(2, 5)
            b = random.randint(1, 6) * random.choice([1, -1])
            c = random.randint(1, 4)
            if c == a: c += 1
            
            # a(x + b) = c*x + rhs_const
            # a*x + a*b = c*x + rhs_const => (a - c)*solution + a*b = rhs_const
            rhs_const = (a - c) * solution + a * b

            q = f"Solve for x: {a}(x + ({b})) = {c}x + ({rhs_const})"
            tex_q = f"\\text{{Solve for }} x: {a}(x + ({b})) = {c}x + ({rhs_const})"
            exp = f"1. Expand: {a}x + ({a*b}) = {c}x + ({rhs_const})\n2. Subtract {c}x: {(a-c)}x + ({a*b}) = {rhs_const}\n3. Solve: x = {solution}"
            ans = str(solution)

        elif concept_id == "linear_slopes":
            x1 = random.randint(-6, 6)
            y1 = random.randint(-6, 6)
            dx = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            dy = random.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            x2 = x1 + dx
            y2 = y1 + dy
            
            slope = sp.Rational(dy, dx)
            q = f"Find the slope of a line passing through ({x1}, {y1}) and ({x2}, {y2})."
            tex_q = f"\\text{{Find slope }} m \\text{{ through }} ({x1}, {y1}) \\text{{ and }} ({x2}, {y2})"
            exp = f"m = (y2 - y1) / (x2 - x1) = ({y2} - ({y1})) / ({x2} - ({x1})) = {dy}/{dx} = {slope}"
            ans = str(slope)

        elif concept_id == "slope_intercept_form":
            x = sp.Symbol('x')
            m = random.randint(-5, 5)
            b = random.randint(-8, 8)
            # y = m*x + b
            expr = m * x + b
            q = f"Write the slope-intercept expression for y with slope m = {m} and y-intercept b = {b}."
            tex_q = f"\\text{{Write }} y \\text{{ for }} m = {m}, b = {b}"
            exp = f"y = mx + b => y = {m}x + ({b}) = {expr}"
            ans = str(expr)

        elif concept_id == "systems_of_equations":
            x_val = random.randint(-5, 5)
            y_val = random.randint(-5, 5)
            a1, b1 = random.randint(1, 4), random.randint(1, 4)
            c1 = a1 * x_val + b1 * y_val
            a2, b2 = random.randint(1, 4), random.randint(-4, -1)
            c2 = a2 * x_val + b2 * y_val

            q = f"Solve the system of equations: Line 1: {a1}x + {b1}y = {c1}, Line 2: {a2}x + ({b2})y = {c2}. Enter answer as (x, y)."
            tex_q = f"\\begin{{cases}} {a1}x + {b1}y = {c1} \\\\ {a2}x + ({b2})y = {c2} \\end{{cases}}"
            exp = f"Intersection point is (x, y) = ({x_val}, {y_val})"
            ans = f"({x_val}, {y_val})"

        elif concept_id == "factoring_quadratics":
            x = sp.Symbol('x')
            p = random.randint(-6, 6)
            q_val = random.randint(-6, 6)
            if p == 0: p = 2
            if q_val == 0: q_val = 3
            
            quad_expr = sp.expand((x + p) * (x + q_val))
            factored = (x + p) * (x + q_val)

            q = f"Factor the quadratic expression: {sp.pretty(quad_expr)}"
            tex_q = f"\\text{{Factor: }} {sp.latex(quad_expr)}"
            exp = f"Find numbers that multiply to {p * q_val} and add to {p + q_val}: {p} and {q_val} => {factored}"
            ans = str(factored)

        elif concept_id == "quadratic_formula":
            r1 = random.randint(-6, 6)
            r2 = random.randint(-6, 6)
            if r1 == r2: r2 += 2
            pos_root = max(r1, r2)
            
            q = f"Find the larger root of the quadratic equation x^2 - ({r1 + r2})x + ({r1 * r2}) = 0."
            tex_q = f"\\text{{Find larger root of }} x^2 - ({r1 + r2})x + ({r1 * r2}) = 0"
            exp = f"Roots are x = {r1} and x = {r2}. The larger root is {pos_root}."
            ans = str(pos_root)

        else:
            q, ans = get_random_problem(concept_id)
            tex_q = q
            exp = f"Target solution: {ans}"

        return {
            "question": q,
            "tex_question": tex_q,
            "target_value": ans,
            "explanation": exp,
            "eval_type": eval_type
        }

    except Exception:
        # Graceful fallback to static problem bank if dynamic generation hits edge case
        q, ans = get_random_problem(concept_id)
        return {
            "question": q,
            "tex_question": q,
            "target_value": ans,
            "explanation": f"Target answer: {ans}",
            "eval_type": eval_type
        }
