#!/usr/bin/env python3
"""Generate 10,000 realistic xAPI statements for dashboard demo.

50 learners across 3 departments, 15 courses across 4 domains, 90 days of activity.
Produces patterns: highly engaged, at-risk, and moderate learners.
"""
from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

SHORTNAME_TO_IRI = {
    "registered": "http://adlnet.gov/expapi/verbs/registered",
    "initialized": "http://adlnet.gov/expapi/verbs/initialized",
    "attempted": "http://adlnet.gov/expapi/verbs/attempted",
    "experienced": "http://adlnet.gov/expapi/verbs/experienced",
    "completed": "http://adlnet.gov/expapi/verbs/completed",
    "passed": "http://adlnet.gov/expapi/verbs/passed",
    "failed": "http://adlnet.gov/expapi/verbs/failed",
    "scored": "http://adlnet.gov/expapi/verbs/scored",
}

DEPARTMENTS = {
    "Engineering": 20,
    "Sales": 15,
    "Operations": 15,
}

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Blake", "Drew", "Skyler", "Cameron", "Jamie", "Robin", "Sage", "Reese",
    "Parker", "Hayden", "Emery", "Dakota", "Finley", "Rowan", "Kai", "Arden",
    "Ellis", "Harper", "Logan", "Spencer", "Tatum", "Shiloh", "Remy", "Lane",
    "Devon", "Addison", "Charlie", "Frankie", "Jesse", "Kerry", "Lee", "Milan",
    "Nico", "Oakley", "Peyton", "Reed", "Sam", "Terry", "Val", "Winter",
    "Yael", "Zion",
]

LAST_NAMES = [
    "Chen", "Patel", "Singh", "Kim", "Nguyen", "Garcia", "Martinez", "Lopez",
    "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright", "Torres",
    "Hill", "Green", "Adams", "Nelson", "Baker", "Rivera", "Campbell", "Mitchell",
    "Roberts", "Carter", "Phillips", "Evans", "Turner", "Parker", "Collins",
    "Edwards", "Stewart", "Morris", "Murphy", "Cook", "Rogers", "Morgan",
    "Peterson", "Cooper", "Reed", "Bailey", "Bell", "Howard", "Ward", "Cox",
    "Diaz", "Richardson", "Wood", "Watson",
]

COURSES = [
    # Technical
    {"id": "course-python-101", "name": "Python Fundamentals", "domain": "Technical", "difficulty": "beginner", "modules": 8, "skills": ["Python", "Programming Basics"]},
    {"id": "course-cloud-arch", "name": "Cloud Architecture", "domain": "Technical", "difficulty": "advanced", "modules": 12, "skills": ["Cloud Computing", "System Design"]},
    {"id": "course-devops-ci", "name": "DevOps & CI/CD", "domain": "Technical", "difficulty": "intermediate", "modules": 10, "skills": ["DevOps", "Automation"]},
    {"id": "course-api-design", "name": "API Design Patterns", "domain": "Technical", "difficulty": "intermediate", "modules": 9, "skills": ["API Design", "System Design"]},
    {"id": "course-security", "name": "Application Security", "domain": "Technical", "difficulty": "advanced", "modules": 11, "skills": ["Security", "Risk Management"]},
    # Compliance
    {"id": "course-data-privacy", "name": "Data Privacy Essentials", "domain": "Compliance", "difficulty": "beginner", "modules": 6, "skills": ["Data Privacy", "Compliance"]},
    {"id": "course-soc2", "name": "SOC 2 Compliance", "domain": "Compliance", "difficulty": "intermediate", "modules": 8, "skills": ["Compliance", "Risk Management"]},
    {"id": "course-gdpr", "name": "GDPR for Practitioners", "domain": "Compliance", "difficulty": "intermediate", "modules": 7, "skills": ["Data Privacy", "Compliance"]},
    # Leadership
    {"id": "course-mgmt-101", "name": "Management Foundations", "domain": "Leadership", "difficulty": "beginner", "modules": 7, "skills": ["Leadership", "Communication"]},
    {"id": "course-communication", "name": "Business Communication", "domain": "Leadership", "difficulty": "beginner", "modules": 6, "skills": ["Communication", "Collaboration"]},
    {"id": "course-strategy", "name": "Strategic Thinking", "domain": "Leadership", "difficulty": "advanced", "modules": 10, "skills": ["Strategy", "Leadership"]},
    {"id": "course-coaching", "name": "Coaching Skills", "domain": "Leadership", "difficulty": "intermediate", "modules": 8, "skills": ["Leadership", "Communication"]},
    # Product
    {"id": "course-analytics", "name": "Product Analytics", "domain": "Product", "difficulty": "intermediate", "modules": 9, "skills": ["Analytics", "Data Privacy"]},
    {"id": "course-user-research", "name": "User Research Methods", "domain": "Product", "difficulty": "intermediate", "modules": 8, "skills": ["Research", "Communication"]},
    {"id": "course-roadmapping", "name": "Product Roadmapping", "domain": "Product", "difficulty": "advanced", "modules": 7, "skills": ["Strategy", "Collaboration"]},
]

DIFFICULTY_COMPLETION = {"beginner": 0.82, "intermediate": 0.58, "advanced": 0.38}
DIFFICULTY_SCORE_MEAN = {"beginner": 0.78, "intermediate": 0.68, "advanced": 0.58}

BASE_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)
END_DATE = BASE_DATE + timedelta(days=90)

HOUR_WEIGHTS = [
    0, 0, 0, 0, 0, 0,           # 0-5: no activity
    1, 3, 8, 12, 11, 8,         # 6-11: morning ramp
    5, 10, 11, 9, 6, 4,         # 12-17: afternoon
    2, 1, 0, 0, 0, 0,           # 18-23: evening drop
]

DOW_WEIGHTS = [5, 10, 12, 12, 10, 3, 1]  # Mon-Sun


def generate_learners() -> list[dict]:
    learners = []
    idx = 0
    for dept, count in DEPARTMENTS.items():
        for _ in range(count):
            fn = FIRST_NAMES[idx]
            ln = LAST_NAMES[idx]
            email = f"{fn.lower()}.{ln.lower()}@company.com"

            if idx < 12:
                engagement = "high"
            elif idx < 20:
                engagement = "at_risk"
            else:
                engagement = "moderate"

            learners.append({
                "email": email,
                "name": f"{fn} {ln}",
                "department": dept,
                "engagement": engagement,
            })
            idx += 1
    return learners


def pick_courses_for_learner(learner: dict) -> list[dict]:
    eng = learner["engagement"]
    if eng == "high":
        n = random.randint(8, 13)
    elif eng == "at_risk":
        n = random.randint(4, 7)
    else:
        n = random.randint(6, 10)
    return random.sample(COURSES, min(n, len(COURSES)))


def random_timestamp(start: datetime, end: datetime) -> datetime:
    """Pick a weighted-random timestamp favoring weekday business hours."""
    for _ in range(50):
        delta = (end - start).total_seconds()
        ts = start + timedelta(seconds=random.random() * delta)
        dow = ts.weekday()
        hour = ts.hour
        if random.random() < DOW_WEIGHTS[dow] / 12 and random.random() < HOUR_WEIGHTS[hour] / 12:
            return ts
    return start + timedelta(seconds=random.random() * (end - start).total_seconds())


def make_statement(actor: dict, verb: str, course: dict, ts: datetime,
                   score: float | None = None, completion: bool | None = None,
                   duration_min: float | None = None) -> dict:
    stmt: dict = {
        "actor": {
            "mbox": f"mailto:{actor['email']}",
            "name": actor["name"],
            "objectType": "Agent",
        },
        "verb": {
            "id": SHORTNAME_TO_IRI[verb],
            "display": {"en-US": verb},
        },
        "object": {
            "id": course["id"],
            "definition": {
                "name": {"en-US": course["name"]},
                "type": "http://adlnet.gov/expapi/activities/course",
            },
            "objectType": "Activity",
        },
        "timestamp": ts.isoformat(),
    }

    if score is not None or completion is not None or duration_min is not None:
        result: dict = {}
        if score is not None:
            result["score"] = {"scaled": round(score, 2), "raw": round(score * 100, 1), "max": 100}
        if completion is not None:
            result["completion"] = completion
        if duration_min is not None:
            h = int(duration_min // 60)
            m = int(duration_min % 60)
            s = int((duration_min % 1) * 60)
            result["duration"] = f"PT{h}H{m}M{s}S" if h else f"PT{m}M{s}S"
        stmt["result"] = result

    return stmt


def generate_course_journey(learner: dict, course: dict) -> list[dict]:
    """Generate a realistic sequence of statements for one learner in one course."""
    stmts = []
    eng = learner["engagement"]
    diff = course["difficulty"]

    # stagger start dates — high engagement starts early, at-risk starts later
    if eng == "high":
        start = BASE_DATE + timedelta(days=random.randint(0, 20))
    elif eng == "at_risk":
        start = BASE_DATE + timedelta(days=random.randint(30, 60))
    else:
        start = BASE_DATE + timedelta(days=random.randint(5, 40))

    ts = random_timestamp(start, min(start + timedelta(days=3), END_DATE))
    stmts.append(make_statement(learner, "registered", course, ts))

    ts = random_timestamp(ts + timedelta(hours=1), min(ts + timedelta(days=2), END_DATE))
    stmts.append(make_statement(learner, "initialized", course, ts))

    # module experiences — multiple interactions per module for realistic volume
    n_modules = course["modules"]
    completion_prob = DIFFICULTY_COMPLETION[diff]
    if eng == "high":
        completion_prob = min(completion_prob + 0.25, 0.95)
    elif eng == "at_risk":
        completion_prob = max(completion_prob - 0.2, 0.15)

    modules_completed = 0
    for mod_idx in range(n_modules):
        will_continue = random.random() < (completion_prob ** 0.25)
        if not will_continue and mod_idx > 1:
            break

        interactions = random.randint(3, 6) if eng == "high" else random.randint(2, 4)
        for _ in range(interactions):
            ts = random_timestamp(ts + timedelta(hours=1), min(ts + timedelta(days=3), END_DATE))
            if ts >= END_DATE:
                break
            dur = random.gauss(25, 10)
            dur = max(5, min(dur, 90))
            stmts.append(make_statement(learner, "experienced", course, ts, duration_min=dur))

        if random.random() < 0.5:
            ts2 = random_timestamp(ts + timedelta(minutes=5), min(ts + timedelta(hours=6), END_DATE))
            stmts.append(make_statement(learner, "attempted", course, ts2))

        modules_completed = mod_idx + 1

    # completion + scoring
    did_complete = modules_completed >= n_modules - 1 and random.random() < completion_prob
    if did_complete:
        ts = random_timestamp(ts + timedelta(hours=1), min(ts + timedelta(days=3), END_DATE))
        if ts < END_DATE:
            score_mean = DIFFICULTY_SCORE_MEAN[diff]
            if eng == "high":
                score_mean += 0.1
            elif eng == "at_risk":
                score_mean -= 0.1
            score = max(0.0, min(1.0, random.gauss(score_mean, 0.12)))

            dur = random.gauss(15, 5)
            stmts.append(make_statement(learner, "completed", course, ts,
                                       score=score, completion=True, duration_min=max(5, dur)))

            passed = score >= 0.6
            stmts.append(make_statement(
                learner, "passed" if passed else "failed", course,
                ts + timedelta(seconds=5), score=score,
            ))
    elif modules_completed > 0 and random.random() < 0.4:
        ts = random_timestamp(ts + timedelta(hours=1), min(ts + timedelta(days=2), END_DATE))
        if ts < END_DATE:
            score = max(0.0, min(1.0, random.gauss(0.45, 0.15)))
            stmts.append(make_statement(learner, "scored", course, ts, score=score))

    return stmts


def generate_all() -> list[dict]:
    learners = generate_learners()
    all_stmts: list[dict] = []

    for learner in learners:
        courses = pick_courses_for_learner(learner)
        for course in courses:
            journey = generate_course_journey(learner, course)
            all_stmts.extend(journey)

    all_stmts.sort(key=lambda s: s["timestamp"])

    # trim or pad to ~10000
    if len(all_stmts) > 11000:
        all_stmts = random.sample(all_stmts, 10000)
        all_stmts.sort(key=lambda s: s["timestamp"])

    return all_stmts


def main():
    stmts = generate_all()
    out_path = Path(__file__).parent / "demo_statements.json"
    with open(out_path, "w") as f:
        json.dump(stmts, f, indent=2)
    print(f"Generated {len(stmts)} statements → {out_path}")


if __name__ == "__main__":
    main()
