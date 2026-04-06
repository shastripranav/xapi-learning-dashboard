"""Skill score mapping — maps course scores to skill dimensions.

Each course covers 2-5 skills. A learner's skill score is a weighted average
of their scores in courses that teach that skill, with advanced courses
weighted higher.
"""

import pandas as pd

from .aggregator import COURSE_METADATA

DIFFICULTY_WEIGHT = {"beginner": 1.0, "intermediate": 1.5, "advanced": 2.0}


def get_skill_course_map() -> dict[str, list[dict]]:
    """Build a reverse map: skill → list of courses that teach it."""
    skill_map: dict[str, list[dict]] = {}
    for cid, meta in COURSE_METADATA.items():
        for skill in meta.get("skills", []):
            if skill not in skill_map:
                skill_map[skill] = []
            skill_map[skill].append({
                "course_id": cid,
                "weight": DIFFICULTY_WEIGHT.get(meta.get("difficulty", "intermediate"), 1.0),
            })
    return skill_map


def learner_skill_scores(df: pd.DataFrame, email: str) -> list[dict]:
    """Compute skill scores for one learner based on their course scores."""
    skill_map = get_skill_course_map()
    learner_df = df[df["actor_email"] == email]

    course_scores = {}
    for cid, group in learner_df.groupby("activity_id"):
        scores = group[group["score"].notna()]["score"]
        if len(scores) > 0:
            course_scores[cid] = float(scores.max())

    results = []
    for skill, courses in skill_map.items():
        weighted_sum = 0.0
        weight_total = 0.0
        count = 0

        for c in courses:
            if c["course_id"] in course_scores:
                weighted_sum += course_scores[c["course_id"]] * c["weight"]
                weight_total += c["weight"]
                count += 1

        if weight_total > 0:
            score = weighted_sum / weight_total
        else:
            score = 0.0

        results.append({
            "skill": skill,
            "score": round(score, 3),
            "sample_size": count,
        })

    return sorted(results, key=lambda x: x["skill"])


def org_skill_averages(df: pd.DataFrame) -> list[dict]:
    """Average skill score across all learners."""
    skill_map = get_skill_course_map()
    all_emails = df["actor_email"].unique()

    skill_totals: dict[str, list[float]] = {s: [] for s in skill_map}

    for email in all_emails:
        for entry in learner_skill_scores(df, email):
            if entry["score"] > 0:
                skill_totals[entry["skill"]].append(entry["score"])

    results = []
    for skill, scores in skill_totals.items():
        results.append({
            "skill": skill,
            "avg_score": round(sum(scores) / len(scores), 3) if scores else 0,
            "learner_count": len(scores),
            "min_score": round(min(scores), 3) if scores else 0,
            "max_score": round(max(scores), 3) if scores else 0,
        })

    return sorted(results, key=lambda x: x["avg_score"])


def skill_heatmap_data(df: pd.DataFrame) -> dict:
    """Build the learners × skills matrix for the heat map visualization."""
    skill_map = get_skill_course_map()
    skills = sorted(skill_map.keys())
    learners = df.groupby("actor_email").agg(name=("actor_name", "first")).reset_index()

    matrix = []
    for _, row in learners.iterrows():
        scores = learner_skill_scores(df, row["actor_email"])
        score_map = {s["skill"]: s["score"] for s in scores}
        matrix.append({
            "email": row["actor_email"],
            "name": row["name"],
            "scores": {s: score_map.get(s, 0) for s in skills},
        })

    return {"skills": skills, "learners": matrix}
