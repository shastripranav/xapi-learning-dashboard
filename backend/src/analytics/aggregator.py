"""Core aggregation from raw statement rows into analytics-ready DataFrames.

This is the workhorse — all other analytics modules pull from these aggregations.
"""

from datetime import datetime, timedelta, timezone

import pandas as pd

from ..db import get_all_statements

_df_cache: pd.DataFrame | None = None
_cache_ts: datetime | None = None
CACHE_TTL = timedelta(seconds=30)

COURSE_METADATA: dict[str, dict] = {}


def set_course_metadata(courses: list[dict]):
    global COURSE_METADATA
    for c in courses:
        COURSE_METADATA[c["id"]] = c


def get_statements_df() -> pd.DataFrame:
    """Cached DataFrame of all statements — refreshes every 30s."""
    global _df_cache, _cache_ts
    now = datetime.now(timezone.utc)

    if _df_cache is not None and _cache_ts and (now - _cache_ts) < CACHE_TTL:
        return _df_cache

    rows = get_all_statements()
    if not rows:
        _df_cache = pd.DataFrame(columns=[
            "actor_email", "actor_name", "verb", "activity_id",
            "activity_name", "score", "completion", "duration_minutes", "timestamp",
        ])
        _cache_ts = now
        return _df_cache

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")

    _df_cache = df
    _cache_ts = now
    return df


def invalidate_cache():
    global _df_cache, _cache_ts
    _df_cache = None
    _cache_ts = None


def get_unique_learners(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("actor_email").agg(
        name=("actor_name", "first"),
        statement_count=("verb", "count"),
        last_active=("timestamp", "max"),
    ).reset_index()


def get_unique_courses(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("activity_id").agg(
        name=("activity_name", "first"),
        statement_count=("verb", "count"),
    ).reset_index()


def daily_activity(df: pd.DataFrame, days: int = 90) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = df[df["timestamp"] >= cutoff].copy()
    recent["date"] = recent["timestamp"].dt.date
    counts = recent.groupby("date").size().reset_index(name="count")
    counts["date"] = counts["date"].astype(str)
    return counts.to_dict("records")
