"""FastAPI application — xAPI Learning Analytics Dashboard backend."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import courses, data_source, engagement, learners, overview, skills
from .config import settings
from .db import close_db

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Starting xAPI Analytics Dashboard (mode={settings.data_mode})")
    _init_metadata()
    if settings.data_mode == "demo":
        _auto_load_demo()
    yield
    close_db()


app = FastAPI(
    title="xAPI Learning Analytics",
    description="Analytics API for xAPI learning data",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(overview.router)
app.include_router(learners.router)
app.include_router(courses.router)
app.include_router(skills.router)
app.include_router(engagement.router)
app.include_router(data_source.router)


@app.get("/health")
def health():
    from .db import get_statement_count
    return {"status": "ok", "statements": get_statement_count()}


def _init_metadata():
    """Always load course catalog into the aggregator for skill mapping."""
    from .analytics.aggregator import set_course_metadata
    from .course_catalog import COURSES
    set_course_metadata(COURSES)


def _auto_load_demo():
    from .db import get_statement_count
    if get_statement_count() == 0:
        try:
            data_source.load_demo()
            log.info("Demo data loaded automatically")
        except Exception as e:
            log.warning(f"Could not auto-load demo data: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=settings.host, port=settings.port, reload=settings.debug)
