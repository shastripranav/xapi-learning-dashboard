from __future__ import annotations

from src.analytics.aggregator import get_statements_df
from src.analytics.skills import learner_skill_scores, org_skill_averages


def test_learner_skill_scores(loaded_db):
    df = get_statements_df()
    skills = learner_skill_scores(df, "alice@co.com")

    assert len(skills) > 0
    python_skill = next((s for s in skills if s["skill"] == "Python"), None)
    if python_skill:
        assert python_skill["score"] > 0
        assert python_skill["sample_size"] >= 1


def test_org_skill_averages(loaded_db):
    df = get_statements_df()
    avgs = org_skill_averages(df)

    assert len(avgs) > 0
    for a in avgs:
        assert "skill" in a
        assert 0 <= a["avg_score"] <= 1


# TODO: add edge case tests for learners with no scored statements
