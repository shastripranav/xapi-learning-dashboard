from __future__ import annotations

from src.analytics.aggregator import get_statements_df
from src.analytics.completion import completion_funnel, course_completion_rates


def test_completion_rate_python_course(loaded_db):
    df = get_statements_df()
    rates = course_completion_rates(df)
    python_rate = rates.get("course-python-101")

    assert python_rate is not None
    assert python_rate["enrolled"] >= 2
    assert python_rate["completed"] == 1
    assert 0 < python_rate["rate"] < 1


def test_completion_funnel_counts(loaded_db):
    df = get_statements_df()
    funnel = completion_funnel(df)

    assert funnel["total_learners"] == 3
    assert funnel["registered"] >= 3
    assert funnel["started"] >= 2
    assert funnel["completed"] >= 1


def test_empty_df_returns_zero():
    import pandas as pd

    cols = [
        "actor_email", "verb", "activity_id",
        "activity_name", "timestamp", "score",
    ]
    df = pd.DataFrame(columns=cols)
    rates = course_completion_rates(df)
    assert rates == {}
