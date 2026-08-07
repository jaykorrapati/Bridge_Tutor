# engine.py
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def check_answer_with_code(eval_type, target_value, student_raw_input):
    """
    Safely parses and validates student responses against a specific target solution.
    """
    # 1. Sanitize whitespaces
    clean_input = student_raw_input.strip().replace(" ", "")
    
    if not clean_input:
        return False, "It looks like you didn't enter an answer. Give it a try!"
        
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

    # 3. Configure transformations to auto-correct math shorthand (like 2x -> 2*x)
    transformations = standard_transformations + (implicit_multiplication_application,)

    try:
        # 4. Safe parsing configurations to prevent execution injection
        student_parsed = parse_expr(clean_input, local_dict={}, transformations=transformations, evaluate=False)
        target_parsed = parse_expr(str(target_value), local_dict={}, transformations=transformations, evaluate=False)

        # 5. Type-aware mathematical evaluation
        if eval_type == "numeric":
            if float(sp.N(student_parsed - target_parsed)) == 0.0:
                return True, f"Correct! {student_raw_input} matches the targeted answer."
                
        elif eval_type in ["symbolic", "equation_solve"]:
            difference = sp.simplify(student_parsed - target_parsed)
            if difference == 0:
                return True, "Correct! Your algebraic value resolves perfectly."
                
    except Exception:
        return False, "I couldn't quite read that format. Make sure to enter a valid number, fraction, or expression!"
        
    return False, "Not quite right. Double check your arithmetic steps and try again."
