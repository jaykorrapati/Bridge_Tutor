# tests/test_engine.py
import pytest
import engine as eng

def test_numeric_evaluation():
    is_corr, _ = eng.check_answer_with_code("numeric", "-22", "-22")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("numeric", "1.5", "3/2")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("numeric", "10", "12")
    assert is_corr is False

def test_equation_evaluation():
    is_corr, _ = eng.check_answer_with_code("equation_solve", "4", "x = 4")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("equation_solve", "4", "4 = x")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("equation_solve", "4", "x = 5")
    assert is_corr is False

def test_symbolic_evaluation():
    is_corr, _ = eng.check_answer_with_code("symbolic", "2*x + 10", "10 + 2x")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("symbolic", "(x + 2)*(x + 3)", "x^2 + 5x + 6")
    assert is_corr is True

def test_coordinate_evaluation():
    is_corr, _ = eng.check_answer_with_code("coordinate", "(3, 2)", "(3, 2)")
    assert is_corr is True

    is_corr, _ = eng.check_answer_with_code("coordinate", "(3, 2)", "(2, 3)")
    assert is_corr is False
