# tests/test_tracker.py
import os
import pytest
import tracker as track

@pytest.fixture(autouse=True)
def clean_db():
    track.reset_student_data("pytest_user")
    yield
    track.reset_student_data("pytest_user")

def test_initial_state_not_mastered():
    assert track.is_mastered("pytest_user", "negative_numbers") is False

def test_state_update_and_mastery():
    # 1st attempt correct -> threshold 2
    track.update_student_state("pytest_user", "negative_numbers", True, mastery_threshold=2)
    assert track.is_mastered("pytest_user", "negative_numbers") is False

    # 2nd attempt correct -> mastered
    track.update_student_state("pytest_user", "negative_numbers", True, mastery_threshold=2)
    assert track.is_mastered("pytest_user", "negative_numbers") is True

def test_get_student_summary():
    track.update_student_state("pytest_user", "negative_numbers", True, question="Q1", student_answer="-22")
    summary = track.get_student_summary("pytest_user")
    assert summary["student_id"] == "pytest_user"
    assert len(summary["states"]) == 1
    assert len(summary["recent_attempts"]) == 1
