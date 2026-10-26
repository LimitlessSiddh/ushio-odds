# Ushio Odds Technical Blueprint

Version 1.0 • 26 October 2026 • Proposed implementation baseline

## Design authority

The engineer’s REA OddsJam report is the primary blueprint. This document retains its adapter, normalization, quote-state, revalidation and replay design, adapted to a separate local project. Our GitHub reviews supply candidates and limitations. Neither source is evidence of OddsJam’s private implementation.

## Deployment model

Use a modular Python backend with a separate ingestion worker, a PostgreSQL database, and a React web dashboard. The API and worker import the same domain calculation package. They can run independently without introducing microservices or a message broker.

| Layer | Recommended baseline |
| --- | --- |
| Dashboard | React and TypeScript with Vite |
| API and contracts | FastAPI and Pydantic with OpenAPI |
| Collection | Python worker using HTTPX and provider-specific adapters |
| Database | PostgreSQL with SQLAlchemy and Alembic migrations |
| Financial logic | Python Decimal and integer currency increments |
| Verification | pytest and Hypothesis; frontend tests for interaction and state |
| Local tooling | uv lockfile, JavaScript lockfile, reproducible local database setup |

## Version policy

Select supported stable runtime and package releases at repository bootstrap and pin them in lockfiles. Verify compatibility before adoption. These choices are recommendations for implementation, not a claim that dependencies or infrastructure already exist.

# System boundaries and source selection

## Source adapters

Define snapshot retrieval, optional stream subscription, optional revalidation, capability discovery and health reporting. Unsupported capabilities must be explicit. Each adapter records provider identity, exact book and regional feed, permission status, timestamp semantics and quota limits.

## Candidate routes

| Route | Role and limitation |
| --- | --- |
| Licensed vendor trial | Engineer’s preferred commercial route; coverage, cost and rights require confirmation |
| Direct permitted collection | Evaluate oddswrap and individual parsers; no verified all-books guarantee |
| Comparison sites | Evaluate OddsHarvester for research; aggregator timestamp is not source quote freshness |
| Limited hosted feeds | InferSports returned sample data; free catalogue is not Canadian book coverage |
| Fixtures and replay | Deterministic development at no data cost; cannot prove live profitability |

## Evidence from our review

Point-in-time requests returned BetRivers NJ listings and a three-market event detail, Sunbet listings and InferSports data. DraftKings and an additional FanDuel route returned access denied. These results establish limited access only. Do not label a connector healthy based solely on a README, recent commit, or mocked test.

## Storage and access permissions

Verify source terms before collection, retained raw payloads, replay, derived alerts or redistribution. Code licenses do not grant data rights. Stop on access-denied responses; no bypass is part of the implementation plan. A future commercial release requires a separate source-rights review.

# Domain model and durable storage

## Canonical market identity

The matching key includes sport, league, event participants and start time, market family, period, exact line and units, overtime or extra-inning treatment, outcome semantics and settlement policy. Prop identity is reserved for future player markets. Ambiguous mappings go to a review queue and cannot generate an eligible opportunity.

| Record | Essential fields |
| --- | --- |
| Provider and book | Provider ID, source book ID, canonical book ID, jurisdiction, terms version |
| Event and market | Canonical IDs, participants, UTC start, family, period, line, settlement key |
| Quote | Source quote ID, selection ID, Decimal odds, state, source and receipt times, sequence |
| Mapping | Provider IDs, canonical IDs, mapping version, reason, reviewer or rule provenance |
| Opportunity | State, selected quote IDs, min profit, calculation and mapping versions, expiry |
| Leg | Quote ID, integer stake units, currency, payout, per-outcome profit |
| Decision and stream outbox | Monotonic local cursor, record version, rejection or invalidation reason |

## Partition and transaction rules

Namespace current quotes by provider, regional book, selection and market identity. Do not let a reconciliation source overwrite the primary feed. In one transaction persist the observation reference, current quote change, affected decisions and delivery outbox event. Enforce provider ID uniqueness and indexes for current-market lookups.

## Representation and retention

Use timezone-aware UTC timestamps, NUMERIC odds, and integer minor units or exact decimal money. JSON serializes decimal values as strings. Retain raw source observations only where permitted; record retention limits in configuration. Partition large quote history only when measured volume justifies it.

# Ingestion matching and recovery

## Processing sequence

1. Fetch a permitted snapshot or resume a documented source cursor.

1. Validate schema, timestamp semantics, odds format, jurisdiction and status.

1. Normalize entities with a versioned mapping and explicit settlement identity.

1. Reject duplicates or out-of-order updates using documented sequence scope; do not compare opaque cursors numerically.

1. Persist observations and update current state atomically.

1. Recompute only affected complete market groups and save the decision.

## Freshness checks

Check source quote age, receipt age, cross-book source skew and feed heartbeat independently. A newly received old quote is still old. Reject unknown or implausibly future source times for revalidated status. Configure age/skew limits per source and market after measurement; there is no universal threshold supplied by this plan.

## Disconnect behaviour

A gap or uncertain reconnect invalidates the affected provider partition. Recover a coherent snapshot and resume only after establishing ordering. A separate expiry sweep invalidates quotes even when no new messages arrive. Current-state reads enforce expiry again, so a stalled worker cannot keep old opportunities active.

## Delivery recovery

The API serves an initial snapshot and SSE deltas from the durable outbox. Use a local event cursor, support Last-Event-ID, send heartbeats and return a snapshot-required signal when the cursor has expired. PostgreSQL polling is sufficient initially; notifications may wake readers but are not the durable event log.

# Arbitrage and hedge calculations

## Exact formulas

Decimal odds d = 1 + a/100 for positive American odds a
d = 1 + 100/abs(a) for negative a
p = sum(1/d_i) over every exclusive exhaustive outcome
Theoretical arb requires p < 1
Stake_i = Budget * (1/d_i) / p
ROI on total stake = 1/p - 1
Two-way fixed first leg: S2 = S1 * d1 / d2

## Allocation and eligibility

Reject missing outcomes, non-finite or invalid odds, unknown market identity and incompatible settlement. Restrict the initial detector to exact-line two-way markets with established rules. Reject unsupported fees, commissions, FX or settlement models rather than silently assuming zero. Store fees and balance/limit assumptions in the result.

Round to each book’s permitted stake increment, respect stated balance/min/max constraints and recompute every outcome’s profit. Do not assume equal-payout allocation remains valid when limits bind; return infeasible or evaluate supported constrained combinations explicitly. Compute conservative payout rounding under the applicable rules. The displayed minimum profit must remain positive after all supported costs.

## Reference example

| Input or outcome | Value |
| --- | --- |
| First leg | 1000.00 at -110 |
| Opposing price | +115 |
| Second stake rounded | 887.95 |
| Combined stake | 1887.95 |
| Over net profit | 21.140909… before payout rounding |
| Under net profit | 21.142500 before payout rounding |

Approximately $21.14 remains either way under the example’s assumptions. This is a mathematical test vector, not a live available bet. A fresh quote is not an accepted wager; one-sided voids require separate settlement rows.

# Application interfaces and opportunity state

| Endpoint | Contract |
| --- | --- |
| GET /v1/odds | Filter event, book, region, market and age; return exact quote IDs |
| GET /v1/opportunities | Return current state, assumptions, legs, timestamps and expiry |
| GET /v1/opportunities/{id} | Decision trace, mapping and calculation versions |
| POST /v1/calculators/hedge | Budget or fixed leg; decimal strings; all outcome rows |
| GET /v1/stream | Snapshot-linked SSE with durable cursor and resync handling |
| GET /v1/health | Feed status, last receipt, backlog and clock warnings |

## States

A theoretical candidate is initially indicative. It becomes revalidated only after a supported new observation or source sequence confirms its selected legs remain eligible. Unsupported revalidation leaves it indicative. Any price change, expiry, suspension, missing outcome or incompatible mapping invalidates the prior result and triggers reevaluation.

## Manual calculator separation

Manually entered odds are explicitly user supplied, with no source-freshness claim. The API uses the same calculation package as the scanner, but never upgrades user input to a verified live opportunity. Record the input, parameters and calculation version for saved results.

## UI requirements

Show the exact line, period, overtime policy, each source time, feed region, status, minimum outcome profit and unknown stake limits. Filter available evidence without implying betting eligibility. Make rejection/invalidation explanations readable. No provider secret or private raw payload is exposed to the browser.

# Verification security and operation

## Required tests

 - Two-way reference math, budget conservation, min-profit recomputation and monotonic rounding constraints.

 - Wrong period, regulation versus overtime, line mismatch, duplicate events, ambiguous names and missing draw outcomes.

 - Stale/future/null timestamps, suspended odds, duplicate/out-of-order messages and disconnected feeds.

 - Limit-bound and infeasible stakes, unsupported fees/FX, replay repeatability and concurrent updates.

 - Expiry with no incoming updates, SSE cursor loss, database restart, secret redaction and malformed payloads.

## Measurement

Measure coverage against a declared event/book/market inventory and time window. Report source-to-receipt and receipt-to-publish distributions where timestamp semantics permit. Track source skew, mapping rejects, candidate lifetime, revalidation survival, reconnect recovery and cost. Keep semantic mismatch rate separate from normal price movement. State audit sample size and confidence limits.

## Local security

Bind the local pilot to loopback with an explicit origin allowlist. Keep provider keys in environment configuration or the operating system keychain; redact request headers and raw secret fields. Use database parameterization and a least-privilege application role. Schema validation and response-size/time limits apply to every source.

## Runtime and scaling

Run one worker per source partition with graceful shutdown, backoff, provider rate limits and health reporting. Use PostgreSQL first; add Redis, queues or object storage only after measurements support the need. Public exposure requires authentication, authorization, TLS, abuse controls and a separate deployment review. An always-on host and its costs are future decisions.

# Implementation layout and technical references

apps/web/               React dashboard
services/api/           FastAPI transport and SSE
services/worker/        Collection and expiry loop
packages/domain/        Identity rules and Decimal calculations
packages/providers/     SourceAdapter implementations
packages/persistence/   SQLAlchemy models and outbox
fixtures/               Permitted samples and synthetic cases
tests/                  Unit integration replay and failure tests
docs/                   Decisions contracts and measured results

## Design references

SourceAdapter, worker, normalizer, repository, calculation engine, API and domain records are shown in the coloured UML class model. The sequence view shows request and observation flow. Both describe proposed responsibilities rather than implemented classes.

Editable FigJam board: https://www.figma.com/board/aKWex1r82c2rxTFqPIekMG

## Primary documentation checked

FastAPI streaming and SSE: https://fastapi.tiangolo.com/tutorial/server-sent-events/
Vite setup and runtime requirements: https://vite.dev/guide/
SQLAlchemy asynchronous sessions: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
PostgreSQL exact numeric types: https://www.postgresql.org/docs/current/datatype-numeric.html
Python decimal arithmetic: https://docs.python.org/3/library/decimal.html

## Reference and implementation boundary

The engineer’s original report and our dated repository reviews are included in Research. Repository code may be reused only after licence and security review; preserve required attribution. No feed, package version, SLA or data entitlement is implied by a diagram or example. No bet-execution implementation is included.
