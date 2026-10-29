# Provider Coverage Evidence Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make a bounded successful provider refresh auditable when it produces zero usable selected-book pairs.

**Architecture:** The adapter creates a non-secret coverage summary while it normalizes the bounded response. The refresh endpoint persists one request-level evidence row for every upstream success, including `observed-empty`, and returns it to a read-only evidence history panel. Fixture comparison data remains the only board used for calculations and opportunities.

**Tech Stack:** FastAPI, SQLAlchemy/Alembic, React/TypeScript, Playwright, pytest.

---

### Task 1: Add coverage-summary tests and adapter contract

**Files:**
- Modify: `services/api/tests/test_api.py`
- Modify: `services/api/app/provider.py`

1. Add synthetic normalizer tests for eligible pairs, unknown books, one-book markets, three-way outcomes, missing timestamps, and empty successes.
2. Ensure expected summaries contain only request/coverage metadata, never the API key.
3. Implement the smallest summary collector that passes those tests.

### Task 2: Persist successful request-level evidence

**Files:**
- Modify: `services/api/app/main.py`
- Modify: `services/api/tests/test_api.py`

1. Add route tests for mocked successful empty and paired observations.
2. Persist exactly one request-level row with `observed-empty` or `observed`, receipt time, quota, and coverage summary.
3. Return the evidence row and summary without passing observations into revalidation or opportunities.

### Task 3: Render a read-only provider evidence history

**Files:**
- Modify: `apps/web/src/types.ts`
- Modify: `apps/web/src/api.ts`
- Modify: `apps/web/src/App.tsx`
- Modify: `apps/web/src/styles.css`
- Modify: `apps/web/e2e/fixture-workflows.spec.ts`

1. Fetch evidence history on the odds view and after a refresh.
2. Render provider, requested scope, receipt/source timing availability, quota, raw/accepted counts, observed selected titles, rejection diagnostics, and unknowns.
3. Add browser coverage for deferred no-key and a mocked observed-empty success.

### Task 4: Document and verify

**Files:**
- Modify: `README.md`
- Modify: `docs/REQUIREMENTS_MATRIX.md`
- Modify: `docs/provider-capability-evidence.md`

1. Describe the coverage evidence states and the one-request boundary.
2. Run backend, TypeScript, build, browser, and migration/container checks.
3. Only after local checks pass, perform one explicitly bounded provider call if its configured credit floor permits it; record a dated, non-secret report.
