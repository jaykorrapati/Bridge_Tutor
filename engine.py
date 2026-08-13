# engine.py
"""
Math Evaluation Engine using SymPy.
Safely parses and validates student answers for numeric, symbolic, equation, and coordinate types.
"""

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def check_answer_with_code(eval_type, target_value, student_raw_input):
    """
    Safely parses and validates student responses against a specific target solution.
    
    Returns:
        is_correct (bool): True if mathematically equivalent, False otherwise.
        feedback (str): Descriptive string detailing validation outcome.
    """
    clean_input = str(student_raw_input).strip().replace(" ", "")
    
    if not clean_input:
        return False, "It looks like you didn't enter an answer. Give it a try!"

    # 1. Coordinate check (x, y)
    if eval_type == "coordinate":
        target_str = str(target_value).replace(" ", "")
        if clean_input == target_str:
            return True, f"Correct! {student_raw_input} matches the targeted coordinate pair."
        
        # Try tuple comparison
        try:
            if clean_input.startswith("(") and clean_input.endswith(")"):
                sp_student = sp.sympify(clean_input)
                sp_target = sp.sympify(target_str)
                if sp_student == sp_target:
                    return True, "Correct! Your coordinate pair is exact."
        except Exception:
            pass
        return False, "Not quite. Check your (x, y) values or format as '(x, y)'."

    # 2. Extract right or left-hand value if input as an equation (e.g. x = 4 or 4 = x)
    if "=" in clean_input:
        parts = clean_input.split("=")
        if len(parts) == 2:
            left, right = parts[0].lower(), parts[1].lower()
            if left in ['x', 'y', 'z']:
                clean_input = parts[1]
            elif right in ['x', 'y', 'z']:
                clean_input = parts[0]
            else:
                clean_input = parts[1]

    # 3. Configure transformations to auto-correct math shorthand (like 2x -> 2*x and x^2 -> x**2)
    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

    try:
        # Safe parsing configurations
        student_parsed = parse_expr(clean_input, local_dict={}, transformations=transformations, evaluate=False)
        target_parsed = parse_expr(str(target_value).replace(" ", ""), local_dict={}, transformations=transformations, evaluate=False)

        # 4. Type-aware mathematical evaluation
        if eval_type == "numeric":
            diff = float(sp.N(student_parsed - target_parsed))
            if abs(diff) < 1e-6:
                return True, f"Correct! {student_raw_input} matches the targeted answer."
                
        elif eval_type in ["symbolic", "equation_solve"]:
            difference = sp.simplify(student_parsed - target_parsed)
            if difference == 0:
                return True, "Correct! Your algebraic value resolves perfectly."
            
            # Alternative expanded check for factored forms
            expanded_diff = sp.simplify(sp.expand(student_parsed) - sp.expand(target_parsed))
            if expanded_diff == 0:
                return True, "Correct! Equivalent algebraic form."

    except Exception:
        return False, "I couldn't quite read that format. Make sure to enter a valid number, fraction (e.g. 3/2), or expression!"
        
    return False, "Not quite right. Double check your steps and try again."
