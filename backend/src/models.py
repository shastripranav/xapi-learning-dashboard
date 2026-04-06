"""Pydantic models for the analytics dashboard.

These are internal representations — the xAPI parser converts raw
statements into these before they hit the analytics engine.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ParsedStatement(BaseModel):
    actor_email: str
    actor_name: str
    verb: str
    activity_id: str
    activity_name: str
    score: float | None = None
    completion: bool | None = None
    duration_minutes: float | None = None
    timestamp: datetime
    raw: dict | None = Field(default=None, exclude=True)


class LearnerProfile(BaseModel):
    email: str
    name: str
    department: str = ""
    courses_completed: int = 0
    courses_in_progress: int = 0
    avg_score: float = 0.0
    last_active: datetime | None = None
    engagement_score: float = 0.0
    status: str = "active"


class CourseStats(BaseModel):
    course_id: str
    course_name: str
    domain: str = ""
    enrollment_count: int = 0
    completion_count: int = 0
    completion_rate: float = 0.0
    avg_score: float = 0.0
    avg_duration_minutes: float = 0.0
    difficulty: str = "intermediate"


class SkillScore(BaseModel):
    skill: str
    score: float
    sample_size: int = 0


class EngagementMetrics(BaseModel):
    email: str
    name: str
    frequency_score: float = 0.0
    recency_score: float = 0.0
    duration_score: float = 0.0
    total_score: float = 0.0


class AtRiskLearner(BaseModel):
    email: str
    name: str
    days_since_active: int
    score_trend: str = "stable"
    engagement_score: float = 0.0
    risk_reasons: list[str] = Field(default_factory=list)


class LRSConnection(BaseModel):
    endpoint: str
    username: str
    password: str


class DataSourceStatus(BaseModel):
    mode: str
    connected: bool = False
    statement_count: int = 0
    last_sync: datetime | None = None
    lrs_endpoint: str | None = None
