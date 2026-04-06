"""Completion rate calculations per course and per learner."""

import pandas as pd

from ..xapi.verbs import COMPLETION_VERBS, ENROLLMENT_VERBS


def course_completion_rates(df: pd.DataFrame) -> dict[str, dict]:
    """Calculate completion rate for each course.

    Rate = unique learners who completed / unique learners who enrolled or attempted.
    Handles the edge case where someone completed without an explicit enrollment.
    """
    results = {}

    for course_id, group in df.groupby("activity_id"):
        enrolled = set(
            group[group["verb"].isin(ENROLLMENT_VERBS)]["actor_email"]
        )
        completed = set(
            group[group["verb"].isin(COMPLETION_VERBS)]["actor_email"]
        )
        # count completers even if they didn't have an explicit enrollment
        enrolled = enrolled | completed

        rate = len(completed) / len(enrolled) if enrolled else 0.0
        results[course_id] = {
            "enrolled": len(enrolled),
            "completed": len(completed),
            "rate": round(rate, 4),
            "course_name": group["activity_name"].iloc[0],
        }

    return results


def learner_completion_summary(df: pd.DataFrame, email: str) -> list[dict]:
    """Per-course completion status for a specific learner."""
    learner_df = df[df["actor_email"] == email]
    out = []

    for course_id, group in learner_df.groupby("activity_id"):
        verbs = set(group["verb"])
        completed = bool(verbs & COMPLETION_VERBS)
        scores = group[group["score"].notna()]["score"]
        best_score = float(scores.max()) if len(scores) > 0 else None

        out.append({
            "course_id": course_id,
            "course_name": group["activity_name"].iloc[0],
            "completed": completed,
            "best_score": best_score,
            "statement_count": len(group),
            "last_activity": group["timestamp"].max().isoformat(),
        })

    return out


def completion_funnel(df: pd.DataFrame) -> dict:
    """Org-wide funnel: registered → initialized → in-progress → completed."""
    all_learners = set(df["actor_email"])
    registered = set(df[df["verb"] == "registered"]["actor_email"])
    verbs = {"initialized", "attempted", "experienced"}
    initialized = set(df[df["verb"].isin(verbs)]["actor_email"])
    completed = set(df[df["verb"].isin(COMPLETION_VERBS)]["actor_email"])

    # in-progress = started but not completed at least one course
    in_progress = initialized - completed

    return {
        "total_learners": len(all_learners),
        "registered": len(registered | all_learners),
        "started": len(initialized),
        "in_progress": len(in_progress),
        "completed": len(completed),
    }
