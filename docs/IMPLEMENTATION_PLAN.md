# Ushio Odds implementation plan

## Completed foundation

1. Fixture-backed React/FastAPI vertical slice with a shared Decimal calculation authority.
2. Local persistence for saved calculations, watchlist entries, and manually recorded pair-ledger records.
3. Alembic migrations, Docker PostgreSQL runtime, SQLite local fallback, CI, deterministic fixtures, and explicit provider status.

## Active build slices

1. **Provider capability scan** — after a permitted key is supplied, discover actual sport/book/market coverage and persist an evidence matrix. Do not treat the provider catalogue as observed account coverage.
2. **Quote lifecycle** — introduce quote IDs, source/receipt timestamps, expiry sweeps, provider/region namespaces, current state/history, and opportunity invalidation traces.
3. **UI/API integration** — finish server-backed watchlist/scenario/ledger reload checks; add source freshness, exact line/period, and revalidation status to the comparison UI.
4. **Ledger lifecycle** — support corrections and immutable audit history; record actual two-leg stakes/returns, fees, refunds, and settlement provenance.
5. **Verification** — add UI interaction tests, screenshot comparisons, migration/restart tests on PostgreSQL, and authorized adapter-contract tests.

## External gates

- A permitted The Odds API key is required before any live capability or freshness claim.
- Quebec book eligibility, display rights, and market coverage remain independent evidence gates.
- Paid data, public deployment, sportsbook credentials, and wager execution require separate authorization.
