# Implementation progress

## Completed

- React/Vite dashboard with approved Ushio dark/light visual language, comparison grid, calculator, navigation, watchlist, saved scenarios, and separate manual performance ledger.
- FastAPI contract and Decimal hedge calculation engine with total-budget/fixed-leg modes.
- Deterministic fixture/replay board, provider status boundary, and controlled The Odds API adapter contract.
- PostgreSQL-ready server persistence models for saved calculations and pair-ledger records; SQLite is the local no-Docker fallback.
- Server-backed watchlist, saved-calculation, and ledger contracts, with Alembic revisions through `20261026_02`.
- Explicit selected-market provider refresh path; player-prop normalization includes player description and exact line.
- Docker compose local environment, pinned web/API dependencies, API tests, and local browser integration evidence.
- Durable fixture quote-lifecycle foundation: provider/feed/book/event/market/outcome/quote/version records, exact market identity, source and receipt timestamps, stale expiry, suspended/missing states, and selected quote-version IDs on fixture opportunities.
- Manual-ledger correction endpoint with append-only correction rows and an effective projection; original pair entries are never overwritten.
- Browser-verified fixture workflow through the local API, including local Vite fallback-port CORS and watchlist reload persistence.

## Current source state

No provider key is configured. The application is deliberately in fixture mode. The Odds API adapter will not fetch until a permitted key is supplied, and it uses a selected-market path plus a configurable credit floor. Canadian coverage remains distinct from Quebec eligibility. Fixture lifecycle persistence proves the local state machine only; no live observation is persisted, replayed, or called revalidated.

## Next required input

Complete the ledger correction/audit lifecycle and browser workflow evidence. Add `USHIO_ODDS_API_KEY` only when ready to run a bounded capability scan before enabling any claimed live sports, books, markets, or props.
