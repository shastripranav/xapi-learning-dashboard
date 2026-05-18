# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-18

### Added

#### Backend (FastAPI)

- Aggregation API over xAPI statements with endpoints for overview/KPI, learner, course, skill, and engagement breakdowns
- Analytics engine modules for completion funnels, engagement scoring, at-risk detection, skill aggregation, and time-of-day analysis
- Multiple data sources supported: demo data (default), JSON statement upload, or live connection to any xAPI-conformant LRS via Basic Auth (`X-Experience-API-Version: 1.0.3`)
- SQLite analytics cache that holds parsed statements for fast querying
- Demo mode that generates 10,000 realistic xAPI statements (50 learners, 15 courses, 90 days of activity) for a friction-free first-run
- xAPI statement parser and internal models built on Pydantic
- REST API documented via OpenAPI / Swagger UI (FastAPI auto-docs)

#### Frontend (React + Vite)

- Five dashboard pages: Overview, Learner Analytics, Course Analytics, Skill Map, and Engagement Analytics
- Drill-down detail pages for individual learners and courses
- Settings page for configuring LRS connection or uploading JSON statement batches
- Interactive charts (recharts) including KPI cards, completion funnel, skill radar, skill heat map, score histograms, and day-of-week × hour activity heat map
- TailwindCSS responsive design with React Router 6 navigation
- Built with Vite 5 for fast HMR

#### Infrastructure

- Docker Compose stack bundling the FastAPI backend and an nginx-served React build
- Python 3.11 backend image, Node 20 frontend build
