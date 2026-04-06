from __future__ import annotations

from src.analytics.aggregator import get_statements_df
from src.analytics.engagement import calculate_engagement_scores


def test_engagement_scores_calculated(loaded_db):
    df = get_statements_df()
    scores = calculate_engagement_scores(df)

    assert len(scores) == 3
    for s in scores:
        assert 0 <= s["total_score"] <= 100
        assert "email" in s
        assert "name" in s


def test_engagement_components_sum(loaded_db):
    df = get_statements_df()
    scores = calculate_engagement_scores(df)

    for s in scores:
        expected = s["frequency_score"] + s["recency_score"] + s["duration_score"]
        assert abs(s["total_score"] - expected) < 0.2


def test_alice_higher_engagement_than_charlie(loaded_db):
    """Alice has recent activity, Charlie hasn't been active in ~35 days."""
    df = get_statements_df()
    scores = {s["email"]: s["total_score"] for s in calculate_engagement_scores(df)}

    assert scores["alice@co.com"] > scores["charlie@co.com"]
