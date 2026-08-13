# tests/test_curriculum.py
import pytest
import curriculum as curr

def test_validate_curriculum_dag():
    assert curr.validate_curriculum_dag() is True

def test_get_all_concepts():
    concepts = curr.get_all_concepts()
    assert "negative_numbers" in concepts
    assert "linear_slopes" in concepts
    assert "systems_of_equations" in concepts
    assert len(concepts) >= 10

def test_get_random_problem():
    q, ans = curr.get_random_problem("negative_numbers")
    assert isinstance(q, str) and len(q) > 0
    assert isinstance(ans, str) and len(ans) > 0
