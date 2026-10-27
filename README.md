# Ushio Odds

Local, single-user odds research software. It ships with deterministic fixtures and does not place bets, claim execution availability, or bypass source controls.

## Run locally

1. Copy `.env.example` to `.env` and optionally add a permitted The Odds API key.
2. For the container runtime, run `docker compose up --build`; the API image includes Alembic and applies the local database schema before it starts.
3. Open `http://localhost:5173`.

Without a key, the API deliberately stays in fixture mode. With a key, the provider adapter is still quota guarded and only refreshes an explicitly selected sport/market.

## Verify locally without Docker

The API image uses Python 3.12. For a local test environment, use Python 3.12 where available:

```bash
cd services/api
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
USHIO_DATABASE_URL=sqlite:////tmp/ushio-migration.db PYTHONPATH=. .venv/bin/alembic -c alembic.ini upgrade head
USHIO_DATABASE_URL=sqlite:////tmp/ushio-tests.db PYTHONPATH=. .venv/bin/pytest -q
cd ../../apps/web
npm ci
npm run check
npm run build
```

The SQLite commands use disposable files. The production-equivalent PostgreSQL migration remains a Docker verification step.

## Boundaries

- Canadian feed coverage is not evidence of Quebec betting eligibility.
- Saved calculations and the manual pair ledger are separate records.
- Fixture/recorded/indicative/revalidated states are visually distinct.
- Fixture opportunities are persisted through a quote lifecycle and trace exact selected quote-version IDs. They remain **indicative** fixture calculations, not live or revalidated opportunities.
- No sportsbook credentials, automatic wagering, public hosting, or paid provider usage is included.
