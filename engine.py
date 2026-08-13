# engine.py
"""
Math Evaluation Engine using SymPy.
Safely parses and validates student answers for numeric, symbolic, equation, and coordinate types.
Enforces strict mathematical character sanitization and keyword blocking to eliminate code injection risks.
"""

import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# Allowed characters regex: digits, math variables (x, y, z), operators +, -, *, /, ^, parens, equals, comma, dot, spaces
SAFE_MATH_REGEX = re.compile(r'^[0-9a-zA-Z\s\+\-\*\/\^\(\)\=\,\.]+$')

# Forbidden keywords to prevent python injection tricks
BLOCKED_KEYWORDS = {'import', 'exec', 'eval', 'lambda', 'open', 'system', 'os', 'sys', '__', 'builtins', 'globals', 'locals', 'getattr', 'setattr'}

def sanitize_and_validate_input(raw_input):
    """Sanitizes raw user input and ensures it contains strictly safe mathematical syntax."""
    clean_input = str(raw_input).strip()
    if not clean_input:
        return None, "It looks like you didn't enter an answer. Give it a try!"

    # Check for forbidden keywords or dunder symbols
    lower_input = clean_input.lower()
    if any(keyword in lower_input for keyword in BLOCKED_KEYWORDS):
        return None, "Invalid character or format detected. Please enter standard mathematical numbers or expressions."

    # Check regex pattern
    if not SAFE_MATH_REGEX.match(clean_input):
        return None, "Invalid character detected. Use standard numbers, variables (x, y, z), or mathematical operators."

    return clean_input, None

def check_answer_with_code(eval_type, target_value, student_raw_input):
    """
    Safely parses and validates student responses against a specific target solution.
    
    Returns:
        is_correct (bool): True if mathematically equivalent, False otherwise.
        feedback (str): Descriptive string detailing validation outcome.
    """
    clean_input, err_msg = sanitize_and_validate_input(student_raw_input)
    if err_msg:
        return False, err_msg

    # Sanitize space for equation parsing
    compact_input = clean_input.replace(" ", "")

    # 1. Coordinate check (x, y)
    if eval_type == "coordinate":
        target_str = str(target_value).replace(" ", "")
        if compact_input == target_str:
            return True, f"Correct! {student_raw_input} matches the targeted coordinate pair."
        
        # Try tuple comparison
        try:
            if compact_input.startswith("(") and compact_input.endswith(")"):
                sp_student = sp.sympify(compact_input)
                sp_target = sp.sympify(target_str)
                if sp_student == sp_target:
                    return True, "Correct! Your coordinate pair is exact."
        except Exception:
            pass
        return False, "Not quite. Check your (x, y) values or format as '(x, y)'."

    # 2. Extract right or left-hand value if input as an equation (e.g. x = 4 or 4 = x)
    if "=" in compact_input:
        parts = compact_input.split("=")
        if len(parts) == 2:
            left, right = parts[0].lower(), parts[1].lower()
            if left in ['x', 'y', 'z']:
                compact_input = parts[1]
            elif right in ['x', 'y', 'z']:
                compact_input = parts[0]
            else:
                compact_input = parts[1]

    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

    try:
        # Safe parsing configuration
        student_parsed = parse_expr(compact_input, transformations=transformations, evaluate=False)
        target_parsed = parse_expr(str(target_value).replace(" ", ""), transformations=transformations, evaluate=False)

        # 3. Type-aware mathematical evaluation
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
