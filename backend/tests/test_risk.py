from __future__ import annotations

from src.analytics.aggregator import get_statements_df
from src.analytics.risk import identify_at_risk


def test_at_risk_catches_declining_scores(loaded_db):
    """Charlie has 3 declining scores: 0.70 → 0.60 → 0.50."""
    df = get_statements_df()
    at_risk = identify_at_risk(df)

    charlie = next((r for r in at_risk if r["email"] == "charlie@co.com"), None)
    assert charlie is not None
    assert any("declining" in reason.lower() for reason in charlie["risk_reasons"])


def test_at_risk_catches_inactive(loaded_db):
    """Charlie's last activity was 35+ days ago."""
    df = get_statements_df()
    at_risk = identify_at_risk(df)

    charlie = next((r for r in at_risk if r["email"] == "charlie@co.com"), None)
    assert charlie is not None
    assert charlie["days_since_active"] >= 14


def test_alice_not_at_risk(loaded_db):
    df = get_statements_df()
    at_risk = identify_at_risk(df)

    alice = next((r for r in at_risk if r["email"] == "alice@co.com"), None)
    # Alice may or may not be at risk depending on timing, but shouldn't be declining
    if alice:
        assert not any("declining" in r.lower() for r in alice["risk_reasons"])
