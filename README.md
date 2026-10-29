# Ushio Odds

Local, single-user odds research software. It ships with deterministic fixtures and does not place bets, claim execution availability, or bypass source controls.

## Run locally

1. Copy `.env.example` to `.env` and optionally add a permitted The Odds API key.
2. For the container runtime, run `docker compose up --build`; the API image includes Alembic and applies the local database schema before it starts.
3. Open `http://localhost:5173`.

Without a key, the API deliberately stays in fixture mode. With a key, the provider adapter is still quota guarded and only refreshes an explicitly selected sport/market.

After adding a permitted key, use **Record provider observation** once. The fixture comparison remains intact while the returned provider board, requested region, remaining credits, coverage summary, rejection diagnostics, and revalidation boundary are displayed separately. A successful request with no usable pair is saved as `observed-empty`; it is an auditable coverage/mapping result, not a broken feed or live arbitrage claim.

## Verify locally without Docker

The API image uses Python 3.12. For a local test environment, use Python 3.12 where available:

```bash
cd services/api
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
. .venv/bin/activate
USHIO_DATABASE_URL=sqlite:////tmp/ushio-migration.db PYTHONPATH=. .venv/bin/alembic -c alembic.ini upgrade head
USHIO_DATABASE_URL=sqlite:////tmp/ushio-tests.db PYTHONPATH=. .venv/bin/pytest -q
cd ../../apps/web
npm ci
npm run check
npm run build
npm run test:e2e
```

The SQLite commands use disposable files. `npm run test:e2e` starts its own fixture-only API and Vite processes on dedicated test ports with a freshly migrated disposable database; it does not reuse a manually running local server. The production-equivalent PostgreSQL migration remains a Docker verification step.

## Boundaries

- Canadian feed coverage is not evidence of Quebec betting eligibility.
- Saved calculations and the manual pair ledger are separate records.
- Fixture, provider-observed, indicative, and revalidated are separate states. A fetch is capability evidence only and does not replace the fixture board until exact identity, settlement, status, and freshness checks support revalidation.
- Fixture opportunities are persisted through a quote lifecycle and trace exact selected quote-version IDs. They remain **indicative** fixture calculations, not live or revalidated opportunities.
- No sportsbook credentials, automatic wagering, public hosting, or paid provider usage is included.

## Resume-ready verification and evidence

- Browser workflows: `apps/web/e2e/fixture-workflows.spec.ts` runs against a real local API/database and covers saved-calculation reload, watchlist add/remove reload, calculator focus/scroll/minimize/restore behavior, immutable ledger correction history, a required-reason negative case, correction-dialog keyboard dismissal, and server-authoritative Performance summary presentation.
- Visual review: `output/visual-qa.md` and `output/playwright/` retain current fixture-mode dark/light screenshots for 1280×720, 1600×900, 1024×768, and 390×844. The capture waits for the intended persisted theme and rendered fixture state.
- Provider boundary: `docs/provider-capability-evidence.md` explains the bounded request and coverage states; `GET /v1/provider/evidence` exposes locally persisted request-level evidence without secrets, including raw/accepted counts, observed canonical-title matches, rejection reasons, source-timing availability, and quota when supplied.
- Deferred continuous architecture: `docs/adr/0001-defer-continuous-worker-stream-and-replay.md` records why worker/outbox/SSE/replay are Phase 2 work.
