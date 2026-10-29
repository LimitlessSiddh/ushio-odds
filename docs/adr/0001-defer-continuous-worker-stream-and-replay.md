# ADR-0001: Defer continuous worker, durable stream, and live replay from the local release

## Status

Accepted — 2026-10-28

## Context

The technical blueprint proposes a source-partitioned ingestion worker, transactional outbox, SSE delivery with durable cursors, and recovery/replay procedures. Those components are appropriate once Ushio continuously collects permitted live observations.

The current release is a local, operator-driven research application. It has deterministic fixtures, an explicit no-key fixture mode, versioned quote lifecycle records, expiry/invalidation logic, local persistence, and no scheduler or recurring collection. No provider key or display/retention authorization has been supplied. Adding a worker or stream now would create an always-on collection/delivery architecture whose value cannot be verified without that authorization, and would blur the project boundary into a live service.

## Decision drivers

- Keep the resume project locally reproducible with no paid service, deployment, polling, or wagering capability.
- Do not imply a live feed, sportsbook availability, Quebec eligibility, or revalidated opportunity without direct evidence.
- Preserve the existing quote lifecycle as the sole persistence path for fixtures and any future permitted observations.
- Avoid adding operational components that cannot be exercised honestly in fixture mode.

## Considered options

### Implement the full worker/outbox/SSE/replay stack now

This would match the blueprint sooner, but would be mostly unexercised without a permitted source and could be mistaken for active collection readiness.

### Add a fixture-only worker and stream

This would demonstrate some mechanics but would introduce concurrent state and delivery complexity without improving the required local research workflows or provider evidence.

### Defer the continuous architecture and retain a precise Phase 2 contract

This keeps the local release auditable while preserving the blueprint as the intended architecture once a permitted provider and retention policy exist.

## Decision

Defer the continuous worker, durable outbox/SSE stream, and live recovery/replay from the resume-ready local release. The product remains an on-demand fixture research application; its only external provider path is one explicitly initiated, authorized selected-market request.

This is not a claim that the blueprint is unnecessary. It is a scope boundary: the existing quote lifecycle and selected-version traces are retained as the future ingestion target, not replaced by a parallel store.

## Consequences

### Positive

- The local product remains reproducible without credentials, scheduled collection, or hosting.
- Fixture quotes, manual ledger records, and any future provider observations remain visibly distinct.
- The release can prove deterministic lifecycle and persistence behavior without overstating live-operational readiness.

### Negative and remaining risk

- No push updates, reconnect cursor handling, durable delivery history, or live recovery proof exists.
- An authorized provider observation is on-demand only; it cannot demonstrate continuous freshness or replay recovery.
- A future public/live service must not rely on this local-release architecture as sufficient.

## Phase 2 entry criteria and required work

Start only after written authorization establishes provider terms, display/retention rights, permitted region/market scope, quota limits, and a data-retention policy. Then:

1. Implement an opt-in, source-partitioned worker with no default schedule and bounded rate/backoff controls.
2. Persist observation, quote-version, opportunity-decision, and outbox rows atomically in PostgreSQL.
3. Add a cursor-based SSE endpoint with Last-Event-ID, heartbeat, expired-cursor resync, and authorization before any public exposure.
4. Add deterministic replay/recovery tests for stale partitions, suspended/missing quotes, database restart, out-of-order observations, and cursor loss.
5. Measure source-to-receipt and receipt-to-publish timing; record capability evidence and explicitly separate it from wagering eligibility and acceptance.

## References

- `02 Ushio Odds Technical Blueprint.md` — proposed worker, outbox, SSE, replay, and recovery design.
- `Ushio Odds Final E2E Resume-Ready Goal.md` — Phase G scope boundary and Definition of Done.
