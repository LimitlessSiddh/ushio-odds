# Quote Lifecycle and Reproducibility Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Ushio's local fixture research workflow reproducible, then add traceable, expiry-safe quote lifecycle foundations that do not imply live wagering availability.

**Architecture:** Keep FastAPI, SQLAlchemy/Alembic, React, and Decimal. Add durable quote-domain tables alongside the existing manual records, use an explicit service layer to ingest deterministic quote observations, and make the opportunity detector consume only currently valid quote versions. Fixtures remain fixtures: they can exercise lifecycle behaviour but never become live/revalidated evidence.

**Tech Stack:** Python 3.12, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL/SQLite, pytest/Hypothesis, React/TypeScript/Vite.

---

### Task 1: Repair reproducible API startup

**Files:**
- Modify: `services/api/Dockerfile`
- Modify: `README.md`
- Test: `services/api/tests/test_migrations.py`

**Step 1: Write the failing image-context assertion**

Add a migration smoke test that runs `alembic upgrade head` against a fresh SQLite database from the API working directory.

**Step 2: Run the test to verify it fails**

Run: `pytest tests/test_migrations.py -q`

Expected: an actionable missing-runtime or migration failure before setup is repaired.

**Step 3: Copy the migration configuration into the API image**

Copy `alembic.ini` and the full `alembic/` directory after dependencies; retain the existing explicit `alembic upgrade head` entrypoint.

**Step 4: Add documented local test bootstrap**

Document Python 3.12 virtualenv creation, dependency installation, fresh SQLite migration, backend tests, frontend `check`, and build commands. Do not claim Docker runtime proof until it is run.

**Step 5: Run the targeted test and compose config check**

Run: `USHIO_DATABASE_URL=sqlite:////tmp/ushio-migration.db PYTHONPATH=. alembic -c alembic.ini upgrade head` and `docker compose config --quiet`.

**Step 6: Commit**

```bash
git add services/api/Dockerfile README.md services/api/tests/test_migrations.py
git commit -m "fix: make API migrations reproducible"
```

### Task 2: Model durable quote identity and version state

**Files:**
- Modify: `services/api/app/persistence.py`
- Create: `services/api/alembic/versions/20261027_03_quote_lifecycle.py`
- Create: `services/api/app/quote_lifecycle.py`
- Test: `services/api/tests/test_quote_lifecycle.py`

**Step 1: Write failing deterministic lifecycle tests**

Cover duplicate observations, source time in the future, stale receipt time, out-of-order data, suspension, identity mismatch, and expiry. Assert each accepted quote version has an immutable ID, source/receipt timestamps, exact market identity, and a reasoned current state.

**Step 2: Run the lifecycle test module to verify it fails**

Run: `pytest tests/test_quote_lifecycle.py -q`

Expected: import or contract failures because no lifecycle service exists.

**Step 3: Add minimal relational schema**

Create provider, regional feed, book, canonical event, market, outcome, quote, and quote-version models. Store all money/price identity as exact strings or integers; include source timestamp, received timestamp, status, invalidation reason, and a deterministic unique observation key.

**Step 4: Add a lifecycle service**

Normalize only already-valid exact two-outcome observations. Reject future timestamps and malformed/mismatched identities; mark missing/suspended/stale records inactive; deduplicate same observations; prevent an older version replacing a newer current version.

**Step 5: Add migration**

Create a forward-only Alembic revision that exactly matches the models and adds useful unique/index constraints.

**Step 6: Run lifecycle tests and fresh migration**

Run: `pytest tests/test_quote_lifecycle.py -q` and a fresh SQLite migration smoke test.

**Step 7: Commit**

```bash
git add services/api/app/persistence.py services/api/app/quote_lifecycle.py services/api/alembic/versions/20261027_03_quote_lifecycle.py services/api/tests/test_quote_lifecycle.py
git commit -m "feat: add durable quote lifecycle"
```

### Task 3: Trace fixture opportunities to selected quote versions

**Files:**
- Modify: `services/api/app/opportunities.py`
- Modify: `services/api/app/main.py`
- Modify: `services/api/app/fixtures.py`
- Test: `services/api/tests/test_api.py`

**Step 1: Write failing API tests**

Assert fixture opportunities expose two selected quote-version IDs, exact outcome/line/period identity, freshness status, and `indicative` source state. Add a negative test that expired or suspended supporting quotes produce no active opportunity.

**Step 2: Run the focused API tests to verify failure**

Run: `pytest tests/test_api.py -q`

Expected: response is missing trace fields and lifecycle filtering.

**Step 3: Ingest fixtures on demand into the local lifecycle store**

Use a stable `fixture` provider/feed namespace and bounded fixture TTL. Do not change `/v1/provider/refresh` into an ingestion endpoint; it remains an observed response only until provider scan authorization exists.

**Step 4: Detect only active matched quote versions**

Build pairs from the same canonical event/market/outcome group and use Decimal hedge calculation exactly as today. Include the selected quote-version IDs and calculation input in every returned opportunity.

**Step 5: Run focused tests**

Run: `pytest tests/test_api.py tests/test_quote_lifecycle.py -q`

**Step 6: Commit**

```bash
git add services/api/app/opportunities.py services/api/app/main.py services/api/app/fixtures.py services/api/tests/test_api.py
git commit -m "feat: trace fixture opportunities to quote versions"
```

### Task 4: Make current limits discoverable and verify the slice

**Files:**
- Modify: `docs/PROGRESS.md`
- Modify: `docs/REQUIREMENTS_MATRIX.md`
- Modify: `README.md`
- Modify: `.github/workflows/ci.yml`

**Step 1: Update factual state**

Clearly distinguish fixture lifecycle tests from live ingestion/revalidation. State that no API key or Quebec eligibility evidence is present, and that capability scans are still gated.

**Step 2: Add CI migration coverage**

Keep SQLite migration smoke coverage and ensure all backend tests use an isolated test database.

**Step 3: Run milestone verification**

Run backend tests in a Python 3.12 environment, Alembic against fresh SQLite and PostgreSQL when Docker is available, `npm run check`, `npm run build`, and a local API workflow check.

**Step 4: Review and commit**

Inspect `git diff --check`, preserve the user's untracked handoff files, and make a focused commit only if all relevant checks pass.
