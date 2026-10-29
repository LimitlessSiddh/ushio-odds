# Provider capability evidence — external authorization deferred

Date: 2026-10-28

## Current result

No `USHIO_ODDS_API_KEY` was supplied for this release. No provider request was made, no sportsbook site was accessed, and no wager, account, Quebec eligibility, display right, limit, fee, or retention right was inferred.

The application is therefore in deterministic **fixture mode**. Calling `POST /v1/provider/refresh` without a key returns a controlled `409` and writes a dated `deferred` record to local `provider_capability_evidence`; it does not silently present fixture data as provider data.

## Implemented safety boundary

- Every explicit refresh attempt records provider, sport, market, region, receipt time, outcome, failure/defer reason, and unknowns. Successful future observations also record book, source time when supplied, quota, and raw-board details needed for review.
- Raw provider responses are **provider-observed-not-revalidated**. They do not replace the fixture comparison board or fixture arbitrage candidates.
- `persist_validated_provider_market` accepts only an exact two-outcome normalized market with event identity, period, line, settlement assumptions, outcome positions, active source status, source/receipt timestamps, and no unsupported fee/FX condition. Accepted samples use the existing versioned quote lifecycle; incomplete, mismatched, inactive, fee, FX, or ambiguous data is rejected.

## Exact next authorized action

Only after Siddh supplies a permitted `USHIO_ODDS_API_KEY` and confirms use under the provider’s terms, make one explicit selected sport/market request from the local app. Then inspect the locally persisted evidence record and report: observed sport/market/books, region, quota, source/receipt timing, request failure if any, and every remaining unknown.

That bounded result still cannot establish account access, accepted betting limits, display rights, profitability, Canadian availability, or Quebec eligibility.
