# Contributing to xapi-learning-dashboard

MIT licensed, full-stack analytics dashboard for xAPI learning data (FastAPI backend + React frontend). Contributions welcome — new dashboard pages, additional aggregation queries, and improved demo data generation are all useful.

## How to Contribute

1. Fork the repository on GitHub.
2. Create a topic branch off `main` (e.g. `feat/cohort-analysis-page`).
3. Make your changes, run the test suite, and verify both backend and frontend still build.
4. Open a pull request describing the change.

## Development setup

### Backend (Python)

```bash
cd backend
pip install -e ".[dev]"
```

Run the API:

```bash
uvicorn src.main:app --reload --port 8000
```

The default mode loads ~10,000 generated xAPI statements so the dashboard has data immediately. Configure a real LRS via `backend/.env` if you want to point at production data.

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

## Code style

Backend:

```bash
cd backend && ruff check src/ tests/
```

Frontend:

```bash
cd frontend && npm run lint
```

## Testing

Backend:

```bash
cd backend && pytest -v
```

Frontend:

```bash
cd frontend && npm test
```

When adding a new dashboard page, please include both a backend aggregation test and a frontend component test. The demo data generator under `backend/src/demo/` is a useful seed for fixture data.

## Questions

Open an issue with the `question` label.
