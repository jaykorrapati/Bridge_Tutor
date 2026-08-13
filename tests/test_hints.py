# tests/test_hints.py
import pytest
import hints as hnt

def test_sign_error_diagnosis():
    diag = hnt.diagnose_and_hint("numeric", "5", "-5")
    assert diag["is_valid_format"] is True
    assert "sign" in diag["diagnosis"].lower()

def test_unparseable_input_diagnosis():
    diag = hnt.diagnose_and_hint("numeric", "5", "((5 + 3")
    assert diag["is_valid_format"] is False

def test_coordinate_format_diagnosis():
    diag = hnt.diagnose_and_hint("coordinate", "(3, 2)", "3, 2")
    assert diag["is_valid_format"] is False
    assert "format" in diag["diagnosis"].lower()
