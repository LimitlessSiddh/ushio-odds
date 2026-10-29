# Implementation progress

## Completed

- React/Vite dashboard with approved Ushio dark/light visual language, comparison grid, calculator, navigation, watchlist, saved scenarios, and separate manual performance ledger.
- FastAPI contract and Decimal hedge calculation engine with total-budget/fixed-leg modes.
- Deterministic fixture/replay board, provider status boundary, and controlled The Odds API adapter contract.
- PostgreSQL-ready server persistence models for saved calculations and pair-ledger records; SQLite is the local no-Docker fallback.
- Server-backed watchlist, saved-calculation, and ledger contracts, with Alembic revisions through `20261028_05`.
- Explicit selected-market provider refresh path; player-prop normalization includes player description and exact line.
- Docker compose local environment, pinned web/API dependencies, API tests, and local browser integration evidence.
- Durable fixture quote-lifecycle foundation: provider/feed/book/event/market/outcome/quote/version records, exact market identity, source and receipt timestamps, stale expiry, suspended/missing states, and selected quote-version IDs on fixture opportunities.
- Manual-ledger correction endpoint with append-only correction rows and an effective projection; original pair entries are never overwritten.
- Browser-verified fixture workflow through the local API, including local Vite fallback-port CORS and watchlist reload persistence.
- Clean Docker PostgreSQL migration verification through Alembic revision `20261028_05`; the containerized API health endpoint reports fixture mode with no provider key.
- Fresh Python 3.12 container verification: 26 backend tests pass; six Playwright fixture workflows pass against the local API/PostgreSQL stack for saved calculation, watchlist add/remove, calculator focus/scroll/minimize/restore behavior, immutable ledger correction reload evidence, correction-dialog Escape/focus behavior, and server-authoritative Performance summary presentation.
- Provider capability evidence is durable, and an exact normalized-provider contract persists permitted samples through the existing quote lifecycle while rejecting incomplete identity, inactive status, fees, or FX.
- Ledger records support explicit manual-source or validated two-leg sourced-pair provenance; server-side integer-minor-unit summaries exclude open/void rows from realised ROI and use only each record's effective correction projection.
- Current fixture-mode visual exports cover both themes at 1280×720, 1600×900, 1024×768, and 390×844; readback confirmed light mode, non-blank renders, local artwork, and native narrow-table scrolling.

## Current source state

No provider key is configured. The application is deliberately in fixture mode. The Odds API adapter will not fetch until a permitted key is supplied, and it uses a selected-market path plus a configurable credit floor. Canadian coverage remains distinct from Quebec eligibility. The exact normalized-provider contract proves local persistence and rejection behavior only; no external live observation has been persisted, replayed, or called revalidated.

The continuous worker, durable outbox/SSE stream, and live recovery/replay are deliberately deferred from this local release in `docs/adr/0001-defer-continuous-worker-stream-and-replay.md`. The next phase is conditional on provider authorization and retention/display rights; it is not silently omitted.

## Next required input

Add `USHIO_ODDS_API_KEY` only when ready to run one bounded capability scan before enabling any claimed live sports, books, markets, or props. Until then, the provider phase is deferred by external authorization as recorded in `docs/provider-capability-evidence.md`.
