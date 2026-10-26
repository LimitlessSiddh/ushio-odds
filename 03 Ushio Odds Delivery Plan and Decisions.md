# Ushio Odds Delivery Plan

Version 1.0 • 26 October 2026 • Engineering handoff and decision register

## How to use this plan

Build the smallest offline foundation while measuring relevant source access. Treat the project brief as product scope and the technical blueprint as the recommended engineering design. The original REA report remains the primary research blueprint; the reconciliation explains deliberate changes. No application code has been delivered in this package.

## Milestone zero

Create a separate repository, shared domain package, schema, source capability contract and synthetic fixtures. Implement both calculator input modes and the original -110/+115 example. Create a bounded source harness that logs observations and produces a book/market coverage matrix. Do not buy a vendor subscription as part of setup.

Exit evidence: reproducible offline run; validated arithmetic; named source and regional feed; observed market depth; timestamp definitions; access/licence status; failure and quota notes; explicit unknowns. Record synthetic, recorded and live mode separately.

## Milestone one

Add durable storage, migrations, event matching, quote expiry, a comparison board and the calculator UI. Start with one sport/market before broadening to the pilot scope. Display unsupported and unknown cases rather than silently dropping them.

Exit evidence: end-to-end fixture replay, audit of exact market identity, no stale quote shown as active after expiry, saved calculation results, and documented setup that another developer can reproduce.

# Evaluation and expansion gates

## Milestone two

Add candidate detection, supported revalidation, invalidation events, durable streaming delivery and a journal. Simulate price movement, one-leg rejection and per-book balances. Record what survived revalidation and why other opportunities disappeared.

Exit evidence: every result traces to exact quote IDs, versions, rounded stakes and assumptions. Audit a predeclared stratified sample and publish the denominator and mismatch severity. Repeat recovery/replay tests. No profitability claim follows from fixtures or theoretical candidates.

## Milestone three

Expand a single dimension at a time: book, sport, market, props, alternate lines or in-play. Each addition repeats source coverage, matching, freshness, rights and failure checks. Public release and actual execution have separate approval gates.

## Priority order

1. Correct calculation and exact market identity.

1. Relevant source access and honest timestamps.

1. Recoverable ingestion and deterministic replay.

1. Clear comparison and calculator interface.

1. Evidence-based opportunity evaluation and later expansion.

## Execution research gate

Before investigating unattended wagering, establish legally eligible operators with permitted execution interfaces. Specify idempotency, accepted-bet reconciliation, balance/exposure caps, duplicate prevention, kill switch, settlement and unmatched-leg handling. Separate books cannot provide one atomic transaction. No overnight execution promise is part of the delivery plan.

# Decisions costs and handoff

| Decision | Current baseline or trigger |
| --- | --- |
| Project identity | Ushio Odds is the confirmed project name; separate from PickPocket |
| Stack | Recommended Python/FastAPI plus PostgreSQL and React/TypeScript |
| Data source | Pending measured coverage, freshness, permitted use and price |
| Spending | No paid services without a concrete choice from Siddh |
| Scope | Personal local pilot; commercial service deferred |
| Initial market | One relevant game market; expand toward pregame NHL/NBA |
| Stake and latency limits | Set from supported book constraints and source measurements |
| Hosting | Existing computer for prototype; continuous operation undecided |

## Budget and ownership

Siddh owns product priorities and decisions involving spend, real-money use, public release and execution research. The coding agent implements contracts, tests and measurements; these roles do not imply staffing commitments. Local open-source development can have $0 incremental software cost. Live feeds, retention rights, continuous hosting and paid trials remain unpriced until inspected.

## Required completion evidence

 - Demo shows all data modes and a clear source-health state.

 - Tests and replay produce repeatable decisions and failure reasons.

 - Coverage and latency results include sample window and limitations.

 - Source licences and permitted data use are documented.

 - README distinguishes built behaviour, measured results and future work.

## Next decision request

No blocking founder decision is needed to start the offline foundation and source assessment. Bring back a source matrix and concrete price/options if relevant free data fails the required coverage or freshness tests.
