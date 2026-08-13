# tests/test_generator.py
import pytest
import generator as gen
import curriculum as curr

def test_generate_problem_all_concepts():
    for concept_id in curr.get_all_concepts():
        prob = gen.generate_problem(concept_id, seed=42)
        assert "question" in prob
        assert "target_value" in prob
        assert "explanation" in prob
        assert "eval_type" in prob
        assert len(prob["question"]) > 0
        assert len(prob["target_value"]) > 0
