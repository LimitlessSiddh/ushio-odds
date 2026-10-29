# E2E Release Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the local browser suite self-contained, repeatable, and safe to use as release evidence.

**Architecture:** Playwright owns a dedicated local API and Vite process on fixed test-only ports. Each run deletes and migrates its explicit disposable SQLite database before the API starts, and the web server receives the matching API base URL.

**Tech Stack:** Playwright, Vite, FastAPI, Alembic, SQLite, TypeScript.

---

### Task 1: Isolate the browser runtime

**Files:**
- Modify: `apps/web/playwright.config.ts`
- Modify: `apps/web/e2e/fixture-workflows.spec.ts`

**Step 1: Write the failing test**

Run the browser suite while a stale local API is running. The current final summary assertion can disagree with the browser's API target.

**Step 2: Implement the minimal runtime contract**

Use dedicated ports (`4173` for Vite, `8100` for FastAPI), remove and migrate only `/tmp/ushio-e2e.db`, explicitly inject `VITE_API_BASE_URL=http://127.0.0.1:8100`, and forbid reuse of an existing server. Read the API base URL from one shared environment default in the browser spec.

**Step 3: Run the complete browser suite**

Run: `npm --prefix apps/web run test:e2e`

Expected: all six workflows pass without manually starting either service.

### Task 2: Correct the reproducibility documentation

**Files:**
- Modify: `README.md`

**Step 1: Update the local virtualenv instructions**

Activate the documented Python 3.12 virtual environment before commands that use `python3` indirectly through the Playwright runner.

**Step 2: Document the self-contained E2E command**

State that the command starts its own fixture-only API and web server and uses a disposable database.

### Task 3: Release verification and checkpoint

**Files:**
- Verify: `services/api/tests/`
- Verify: `apps/web/e2e/fixture-workflows.spec.ts`

**Step 1: Run clean backend suite**

Run: `USHIO_DATABASE_URL=sqlite:////tmp/ushio-release-audit.db PYTHONPATH=services/api <venv-python> -m pytest services/api/tests -q`

Expected: 26 passed.

**Step 2: Run frontend gates and E2E suite**

Run: `npm --prefix apps/web run check && npm --prefix apps/web run build && npm --prefix apps/web run test:e2e`

Expected: typecheck and build pass; six browser workflows pass.

**Step 3: Commit only intended release files**

Stage the application, tests, migrations, documentation, and browser test harness. Exclude `.DS_Store`, `.claude-flow/`, transient outputs, and unrelated notes. Push only after local verification succeeds.
