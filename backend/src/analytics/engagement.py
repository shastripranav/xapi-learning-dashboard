"""Engagement scoring — composite metric from frequency, recency, and duration."""

from datetime import datetime, timezone

import pandas as pd

TARGET_ACTIVITIES_PER_WEEK = 5.0
TARGET_SESSION_MINUTES = 30.0


def calculate_engagement_scores(df: pd.DataFrame) -> list[dict]:
    """Compute engagement score for each learner.

    Score is 0-100 from three weighted signals:
      - frequency (40%): activities per week vs target
      - recency (35%): days since last activity
      - duration (25%): avg session time vs target
    """
    now = datetime.now(timezone.utc)
    results = []

    for email, group in df.groupby("actor_email"):
        name = group["actor_name"].iloc[0]
        first_ts = group["timestamp"].min()
        last_ts = group["timestamp"].max()

        weeks_active = max((now - first_ts).days / 7, 1)
        activities_per_week = len(group) / weeks_active
        frequency_score = min(activities_per_week / TARGET_ACTIVITIES_PER_WEEK, 1.0) * 40

        days_since = (now - last_ts).days
        recency_score = max(0, 1 - (days_since / 30)) * 35

        durations = group["duration_minutes"].dropna()
        avg_dur = float(durations.mean()) if len(durations) > 0 else 0
        duration_score = min(avg_dur / TARGET_SESSION_MINUTES, 1.0) * 25

        total = round(frequency_score + recency_score + duration_score, 1)

        results.append({
            "email": email,
            "name": name,
            "frequency_score": round(frequency_score, 1),
            "recency_score": round(recency_score, 1),
            "duration_score": round(duration_score, 1),
            "total_score": total,
        })

    results.sort(key=lambda x: x["total_score"], reverse=True)
    return results
