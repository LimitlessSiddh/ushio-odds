# Ushio Odds

Local, single-user odds research software. It ships with deterministic fixtures and does not place bets, claim execution availability, or bypass source controls.

## Run locally

1. Copy `.env.example` to `.env` and optionally add a permitted The Odds API key.
2. Run `docker compose up --build`.
3. Open `http://localhost:5173`.

Without a key, the API deliberately stays in fixture mode. With a key, the provider adapter is still quota guarded and only refreshes an explicitly selected sport/market.

## Boundaries

- Canadian feed coverage is not evidence of Quebec betting eligibility.
- Saved calculations and the manual pair ledger are separate records.
- Fixture/recorded/indicative/revalidated states are visually distinct.
- No sportsbook credentials, automatic wagering, public hosting, or paid provider usage is included.
