# Provider capability evidence — external authorization deferred

Date: 2026-10-28

## Evidence states

Every explicit refresh creates one local request-level evidence record. `deferred` means no permitted key was configured; `failed` means the upstream request did not yield an accepted response; `observed-empty` means the upstream response succeeded but no complete selected-book pair survived normalization; and `observed` means one or more complete selected-book comparison markets were observed. All successful observations remain `provider-observed-not-revalidated`.

The dated current observation is recorded in `docs/evidence/2026-10-29-nhl-moneyline-provider-observation.md`. It is an `observed-empty` result with an explicitly documented partial-recovery caveat; it does not justify a canonical-book mapping change.

The application is otherwise in deterministic **fixture mode**. Calling `POST /v1/provider/refresh` without a key returns a controlled `409` and writes a dated `deferred` record to local `provider_capability_evidence`; it does not silently present fixture data as provider data.

## Implemented safety boundary

- Every explicit refresh attempt records provider, sport, market, region, receipt time, outcome, failure/defer reason, and unknowns. Each successful response records raw event/bookmaker/market counts, provider titles, canonical selected-book title matches, normalized/accepted counts, non-secret rejection diagnostics, source-timing availability, and quota when supplied. It never stores the API key or a full provider payload.
- Raw provider responses are **provider-observed-not-revalidated**. They do not replace the fixture comparison board or fixture arbitrage candidates.
- `persist_validated_provider_market` accepts only an exact two-outcome normalized market with event identity, period, line, settlement assumptions, outcome positions, active source status, source/receipt timestamps, and no unsupported fee/FX condition. Accepted samples use the existing versioned quote lifecycle; incomplete, mismatched, inactive, fee, FX, or ambiguous data is rejected.

## Exact next authorized action

Before any future request, confirm the provider’s permitted scope and use one explicit selected sport/market action from the already migrated local app. Then inspect the locally persisted evidence record and report: observed sport/market/books, raw versus accepted counts, rejection reasons, region, quota, source/receipt timing, request failure if any, and every remaining unknown.

That bounded result still cannot establish account access, accepted betting limits, display rights, profitability, Canadian availability, or Quebec eligibility.
