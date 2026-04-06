"""Time-on-task analysis and activity time patterns."""

import pandas as pd


def time_of_day_heatmap(df: pd.DataFrame) -> list[dict]:
    """Activity counts by day-of-week × hour for the heat map."""
    ts = df["timestamp"].copy()
    dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    data = []
    for dow in range(7):
        for hour in range(24):
            mask = (ts.dt.dayofweek == dow) & (ts.dt.hour == hour)
            count = int(mask.sum())
            data.append({
                "day": dow_names[dow],
                "hour": hour,
                "count": count,
            })

    return data


def peak_activity_hours(df: pd.DataFrame) -> list[dict]:
    counts = df["timestamp"].dt.hour.value_counts().sort_index()
    return [{"hour": int(h), "count": int(c)} for h, c in counts.items()]


def time_on_task_by_course(df: pd.DataFrame) -> list[dict]:
    """Distribution of total time spent per course per learner."""
    with_dur = df[df["duration_minutes"].notna()].copy()
    if with_dur.empty:
        return []

    grouped = with_dur.groupby(["activity_id", "activity_name", "actor_email"]).agg(
        total_minutes=("duration_minutes", "sum"),
    ).reset_index()

    results = []
    for course_id, group in grouped.groupby("activity_id"):
        mins = group["total_minutes"]
        results.append({
            "course_id": course_id,
            "course_name": group["activity_name"].iloc[0],
            "avg_minutes": round(float(mins.mean()), 1),
            "median_minutes": round(float(mins.median()), 1),
            "min_minutes": round(float(mins.min()), 1),
            "max_minutes": round(float(mins.max()), 1),
            "learner_count": len(group),
        })

    return sorted(results, key=lambda x: x["avg_minutes"], reverse=True)
