# hints.py
"""
Diagnostic Hint Engine for BridgeTutor AI Agent.
Analyzes student errors using SymPy mathematical structure comparison to output intelligent hints.
"""

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def diagnose_and_hint(eval_type, target_value, student_raw_input, step_explanation=None):
    """
    Analyzes student answer against target solution and produces tiered feedback & diagnostic guidance.
    
    Returns:
    {
        "is_valid_format": bool,
        "diagnosis": str,
        "hint_level1": str,  # Conceptual Strategy
        "hint_level2": str,  # Specific Actionable Hint
        "hint_level3": str   # Worked Solution Step
    }
    """
    clean_input = str(student_raw_input).strip()
    if not clean_input:
        return {
            "is_valid_format": False,
            "diagnosis": "Empty input submitted.",
            "hint_level1": "Don't be afraid to take a guess! Try working out the first step.",
            "hint_level2": "Look at the numbers given in the problem and identify what operation to apply.",
            "hint_level3": f"Target solution: {target_value}"
        }

    # Handle equation inputs (e.g. x = 4)
    extracted_val = clean_input
    if "=" in clean_input:
        parts = clean_input.split("=")
        if len(parts) == 2:
            left, right = parts[0].strip().lower(), parts[1].strip().lower()
            if left in ['x', 'y', 'z']:
                extracted_val = parts[1]
            elif right in ['x', 'y', 'z']:
                extracted_val = parts[0]
            else:
                extracted_val = parts[1]

    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

    try:
        if eval_type == "coordinate":
            # Parsing (x, y) coordinates
            target_str = str(target_value).replace(" ", "")
            student_str = clean_input.replace(" ", "")
            
            if not (student_str.startswith("(") and student_str.endswith(")")):
                return {
                    "is_valid_format": False,
                    "diagnosis": "Coordinate format issue.",
                    "hint_level1": "Format your answer as an ordered pair: (x, y).",
                    "hint_level2": "Include parentheses around the two numbers separated by a comma, e.g. (3, 2).",
                    "hint_level3": f"Full Solution: {step_explanation or target_value}"
                }
            
            return {
                "is_valid_format": True,
                "diagnosis": "Coordinate mismatch.",
                "hint_level1": "Check your calculations for both the x and y values.",
                "hint_level2": "Try plugging one variable into the second equation to double check.",
                "hint_level3": f"Full Solution: {step_explanation or target_value}"
            }

        target_parsed = parse_expr(str(target_value).replace(" ", ""), local_dict={}, transformations=transformations, evaluate=False)
        student_parsed = parse_expr(extracted_val.replace(" ", ""), local_dict={}, transformations=transformations, evaluate=False)

        diff = sp.simplify(student_parsed - target_parsed)
        sum_check = sp.simplify(student_parsed + target_parsed)

        # Check for sign error
        if sum_check == 0:
            return {
                "is_valid_format": True,
                "diagnosis": "Sign error detected!",
                "hint_level1": "You are very close! Your magnitude is correct, but check your plus/minus sign.",
                "hint_level2": "Remember: subtracting a negative makes a positive, or check which term had the larger magnitude.",
                "hint_level3": f"Full Solution: {step_explanation or target_value}"
            }

        # Check for inverted slope / fraction flip
        try:
            if float(target_parsed) != 0 and float(student_parsed) != 0:
                inv_check = sp.simplify(student_parsed - (1 / target_parsed))
                if inv_check == 0:
                    return {
                        "is_valid_format": True,
                        "diagnosis": "Reciprocal / Inverted Fraction Error.",
                        "hint_level1": "It looks like your fraction is flipped upside down!",
                        "hint_level2": "For slope m = (y2 - y1) / (x2 - x1), make sure y (rise) is in the numerator and x (run) is in the denominator.",
                        "hint_level3": f"Full Solution: {step_explanation or target_value}"
                    }
        except Exception:
            pass

    except Exception:
        return {
            "is_valid_format": False,
            "diagnosis": "Unparseable math expression.",
            "hint_level1": "Double check your math syntax. Use standard numbers, fractions like 3/2, or equations like x = 4.",
            "hint_level2": "Avoid special symbols or unclosed parentheses.",
            "hint_level3": f"Target Solution: {target_value}"
        }

    return {
        "is_valid_format": True,
        "diagnosis": "Arithmetic or algebraic step error.",
        "hint_level1": "Review the inverse operations applied step-by-step.",
        "hint_level2": "Try working backward from your result or plugging your answer back into the original expression.",
        "hint_level3": f"Step-by-Step Solution:\n{step_explanation or target_value}"
    }
