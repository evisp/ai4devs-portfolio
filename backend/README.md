# Backend — Tirana Real Estate Companion

## Prerequisites

- Python 3.10 or later.
- pip.
- WSL on Windows (recommended).

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The server starts on `http://localhost:5000`.

## API endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/listings` | Browse listings with filters and pagination |
| `GET /api/listings/<id>` | Listing details |
| `GET /api/listings/<id>/estimate` | ML price estimate (Phase 4: real predictions) |
| `GET /api/listings/<id>/comps` | Comparable properties (stub until Phase 5) |

## Data

The app loads `data/tirana_house_prices.json` from the project root at startup.
Preprocessing rules are defined in `docs/concept/04-data-preprocessing.md`.
