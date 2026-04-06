from __future__ import annotations

from src.analytics.aggregator import daily_activity, get_statements_df, get_unique_learners
from src.xapi.parser import _parse_duration, parse_statement


def test_parse_iso_duration():
    assert _parse_duration("PT1H30M") == 90.0
    assert _parse_duration("PT45M") == 45.0
    assert _parse_duration("PT2H") == 120.0
    assert _parse_duration("PT0M30S") == 0.5
    assert _parse_duration(None) is None
    assert _parse_duration("invalid") is None


def test_parse_statement_basic():
    raw = {
        "actor": {"mbox": "mailto:test@example.com", "name": "Test User"},
        "verb": {"id": "http://adlnet.gov/expapi/verbs/completed"},
        "object": {
            "id": "course-1",
            "definition": {"name": {"en-US": "Test Course"}},
        },
        "timestamp": "2026-01-15T10:00:00Z",
        "result": {"score": {"scaled": 0.85}, "completion": True},
    }
    stmt = parse_statement(raw)
    assert stmt is not None
    assert stmt.actor_email == "test@example.com"
    assert stmt.verb == "completed"
    assert stmt.score == 0.85
    assert stmt.completion is True


def test_parse_skips_unknown_verbs():
    raw = {
        "actor": {"mbox": "mailto:test@example.com"},
        "verb": {"id": "http://example.com/verbs/custom"},
        "object": {"id": "course-1"},
        "timestamp": "2026-01-15T10:00:00Z",
    }
    assert parse_statement(raw) is None


def test_unique_learners(loaded_db):
    df = get_statements_df()
    learners = get_unique_learners(df)
    assert len(learners) == 3


def test_daily_activity(loaded_db):
    df = get_statements_df()
    activity = daily_activity(df, days=90)
    assert len(activity) > 0
    total = sum(d["count"] for d in activity)
    assert total > 0
