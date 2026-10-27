# Requirement-to-evidence matrix

| Requirement | Implemented evidence | Current limitation |
| --- | --- | --- |
| Exact money calculations | `services/api/app/domain.py`, seven API/domain tests | Fees and book limits are not yet modelled per source |
| Source distinction | Fixture mode and provider status responses | No permitted key supplied |
| Odds comparison | Real API-backed paired odds grid | Fixture has NHL/NBA moneylines only |
| Watchlist / saved scenarios | Server-backed endpoints; UI loads/saves through local API | Watchlist UI needs a restart/reload E2E assertion |
| Performance ledger | Separate UI plus `/v1/ledger` persistence contract | Corrections and per-leg audit trail remain incomplete |
| Quebec boundary | Explicit labels and documentation | Provider entitlement/eligibility unverified |
| UI fidelity | approved palette/density, dark/light mode, compact calculator, responsive grid | Formal screenshot-diff suite still pending |
| CI and reproducibility | Docker compose, Alembic revisions, pinned dependencies, GitHub workflow | Hosted run requires push/remote access |
