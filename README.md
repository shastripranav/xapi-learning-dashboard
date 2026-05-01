# xAPI Learning Analytics Dashboard

[![CI](https://github.com/shastripranav/xapi-learning-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/shastripranav/xapi-learning-dashboard/actions/workflows/ci.yml)

Purpose-built analytics dashboard for xAPI (Experience API) learning data. Connects to any xAPI-conformant LRS or loads data from JSON — gives L&D teams instant visualizations of learner progress, completion funnels, engagement patterns, skill maps, and at-risk identification.

## Why This Exists

SQL LRS (the leading open-source LRS) ships without a dashboard. Learning Locker's open-source dashboards have stalled. L&D teams need purpose-built visualizations — not generic BI tools. xAPI data has unique visualization needs (learning paths, completion funnels, skill heat maps) that don't map to standard chart types.

**Demo mode works out of the box** — 10,000 realistic xAPI statements load instantly. No LRS required.

## Quick Start

```bash
# Backend
cd backend
pip install fastapi uvicorn pydantic pydantic-settings pandas httpx python-dotenv aiosqlite python-multipart
python -m uvicorn src.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** — the dashboard loads with demo data automatically.

### Docker

```bash
docker-compose up --build
```

Backend at :8000, frontend at :5173.

## Architecture

```
┌─────────────┐     ┌──────────────────────────────────┐
│   React UI  │────▶│       FastAPI Backend             │
│  (Recharts) │     │                                    │
│  Port 5173  │     │  ┌──────────┐  ┌───────────────┐  │
│             │     │  │  xAPI    │  │   Analytics    │  │
│  5 Pages:   │     │  │  Parser  │  │   Engine       │  │
│  Overview   │     │  └──────────┘  │  - completion  │  │
│  Learners   │     │       ↓        │  - engagement  │  │
│  Courses    │     │  ┌──────────┐  │  - risk        │  │
│  Skills     │     │  │  SQLite  │──│  - skills      │  │
│  Engagement │     │  │  Cache   │  │  - time        │  │
│  Settings   │     │  └──────────┘  └───────────────┘  │
└─────────────┘     │       ↑                            │
                    │  ┌──────────┐                      │
                    │  │ LRS HTTP │  ← xAPI Basic Auth   │
                    │  │ Client   │                      │
                    │  └──────────┘                      │
                    └──────────────────────────────────┘
```

## Dashboard Pages

### Overview
KPI cards (total learners, active 30d, completion rate, avg score), completion funnel, activity timeline, top courses table.

### Learner Analytics
Searchable learner table with status indicators. Click a learner for skill radar chart with cohort overlay, course progress timeline, and recent activity feed.

### Course Analytics
All courses with enrollment, completion rates, and avg scores. Click a course for score distribution histogram, weekly completion trend, and module drop-off analysis.

### Skill Map
Learners × Skills heat map (red → yellow → green), box plot distributions per skill, and lowest-scoring skills bar chart.

### Engagement Analytics
Composite engagement scores (frequency + recency + duration), at-risk learner table with specific risk reasons, day-of-week × hour activity heat map, peak hours chart.

## Analytics Engine

| Metric | Formula |
|--------|---------|
| Completion Rate | `completed_learners / enrolled_learners` per course |
| Engagement Score | `frequency(40%) + recency(35%) + duration(25%)`, 0-100 |
| At-Risk Detection | Inactive 14+ days, OR scores declining, OR engagement < 30 |
| Skill Score | Weighted avg of course scores per skill, advanced courses weighted 2x |

## API Reference

```
GET  /api/overview                   # KPI summary
GET  /api/overview/funnel            # Completion funnel
GET  /api/overview/timeline          # Daily activity (30/60/90d)
GET  /api/overview/top-courses       # Top courses by enrollment

GET  /api/learners                   # Paginated list with search
GET  /api/learners/{email}           # Learner profile
GET  /api/learners/{email}/skills    # Skill radar + cohort avg
GET  /api/learners/{email}/activity  # Recent activity feed
GET  /api/learners/{email}/progress  # Course progress

GET  /api/courses                    # Course list with stats
GET  /api/courses/{id}               # Course detail
GET  /api/courses/{id}/scores        # Score histogram
GET  /api/courses/{id}/dropoff       # Module drop-off

GET  /api/skills                     # Org skill averages
GET  /api/skills/heatmap             # Learners × Skills matrix
GET  /api/skills/distribution        # Score distributions

GET  /api/engagement/scores          # Per-learner engagement
GET  /api/engagement/at-risk         # At-risk learners
GET  /api/engagement/time-of-day     # Day × Hour heatmap
GET  /api/engagement/time-on-task    # Time per course

POST /api/connect-lrs               # Connect to LRS
POST /api/upload                    # Upload JSON statements
POST /api/load-demo                 # Load demo dataset
GET  /api/data-source/status        # Connection status
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_MODE` | `demo` | `demo` auto-loads sample data on startup |
| `LRS_ENDPOINT` | — | xAPI LRS URL (e.g., `https://lrs.example.com/xapi/`) |
| `LRS_USERNAME` | — | Basic Auth key |
| `LRS_PASSWORD` | — | Basic Auth secret |
| `PORT` | `8000` | Backend port |
| `FRONTEND_URL` | `http://localhost:5173` | CORS origin |

## Demo Data

10,000 xAPI statements covering:
- **50 learners** across Engineering (20), Sales (15), Operations (15)
- **15 courses** across Technical, Compliance, Leadership, Product
- **90 days** of activity with realistic patterns
- Highly engaged, moderate, and at-risk learner profiles
- Score distributions that vary by course difficulty

## LRS Connection

Connect to any xAPI-conformant LRS (SQL LRS, Learning Locker, Watershed, etc.):

1. Go to **Settings** page
2. Enter your LRS endpoint, username, and password
3. Click **Connect & Sync**
4. Dashboard loads with your real data

Uses xAPI HTTP Basic Auth with version header `X-Experience-API-Version: 1.0.3`.

## Development

```bash
# Run tests
cd backend && python -m pytest tests/ -v

# Lint
ruff check src/

# Generate fresh demo data
python -c "from data.generate_demo_data import main; main()"
```

## Tech Stack

**Backend:** Python 3.10+, FastAPI, pandas, httpx, SQLite
**Frontend:** React 18, Recharts, Tailwind CSS, Vite, React Router
**Testing:** pytest (24 tests), Vite build verification

## License

MIT
