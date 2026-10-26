# Arbitrage project — reconciliation with the engineer’s blueprint

Date: October 26, 2026.
Status: proposed alignment for discussion, not implementation authorization or a finalized vendor/stack decision.

## Baseline and source hierarchy

Use /Users/siddhpatel/Downloads/REA-OddsJam-Research-Report-2026-10-26.md as the primary engineering blueprint. Preserve the original file unchanged. Incorporate this conversation’s two GitHub research reports as evidence about candidate components and point-in-time source access. Neither source establishes a profitable live system.

The REA report says the public OddsJam capture stopped at Cloudflare. That supports an access limitation, not discovery of OddsJam’s private architecture. This review reads the report; it does not independently authenticate the exported REA evidence bundle or re-audit the PickPocket codebase.

## Product intent to preserve

The user wants a personal software/resume project with an odds-opportunity scanner and integrated hedge calculator. $0 incremental development cost is a preference. Eventual automated betting is a long-term vision, after measuring and understanding the manual workflow. A commercial service, vendor purchase, PickPocket integration, public launch, and automatic betting are not current decisions.

## Common ground to retain from the engineer

1. Correctness depends on data quality and market identity before arbitrage mathematics.
2. Canonical entities must capture event, sport/league, market family, period, line, units, overtime treatment, outcome semantics and settlement compatibility.
3. Keep raw observations and source/receipt/processing timestamps with provenance.
4. Normalize through provider adapters; isolate collection from calculation.
5. Keep current quote state separate from history and opportunity decision records.
6. Recompute affected groups on updates; expire and invalidate stale/suspended/removed inputs.
7. Calculate rounded stakes and every outcome’s resulting profit, including applicable constraints/costs.
8. Revalidate selected legs before publishing an opportunity as revalidated.
9. Use deterministic replay, failure tests, and auditable rejection/invalidation reasons.
10. Begin with limited pregame markets and no automatic execution. Support later expansion through adapters and explicit gates.

## Changes needed to match this project

| Engineer’s assumption | Reconciled treatment |
|---|---|
| Commercial display/alerts/deep links as the immediate use case | Personal/local research first. Keep a distinct public/commercial release gate if that goal is later adopted. Personal use does not waive source terms or access restrictions. |
| Licensed paid push vendor is the first implementation dependency | Retain as a serious option, but compare with permitted direct feeds and recorded/synthetic development before spending money. |
| Integrate into PickPocket | Treat this as a separate project. Reuse general knowledge, not PickPocket code or infrastructure by default. |
| Two vendor trials required before any progress | Vendor trials are one data-validation route. Calculator, schema, replay and source harness can progress offline; realistic source validation still needs actual relevant data. |
| All Canadian brands treated as useful coverage | Separate visible data coverage, exact regional feed identity, source-use rights, and the user’s ability to execute bets in their location. Ontario data is not Quebec execution access. |
| Fixed multiweek phase durations | Use engineering estimates conditional on source access and observed scope; do not promise calendar delivery based on a vendor-dependent schedule. |

## Where our repository research fits

- **oddswrap**: most relevant direct North American multi-book collector candidate from our review. Adapter pattern, four sports, six book modules and some prop methods are useful. NJ defaults, mocked tests, matching heuristics and access failures require validation. Do not adopt as a proven complete data service.
- **OddsHarvester**: comparison-site collection/replay candidate with MIT license. Its collection timestamps are not proof of underlying book quote freshness. No validated low-latency execution role yet.
- **declanwalpole/sportsbook-odds-scraper**: event-level parser research. Does not provide complete discovery/matching; no detected license in inspected snapshot.
- **InferSports**: bounded hosted keyless feed candidate. Calls returned six Asian book names and sample NBA prices. Not a solution to Canadian/US coverage or source-use permissions; payload contains suspended/older quote rows.
- **0xENTYPER/arbitrage-betting-engine**: MIT calculator/validation reference. No ingestion or settlement-normalization layer. Needs independent precision and edge-case checks.
- **jigonyoo/odds-consensus**: MIT schema/validation reference using generated fixtures, not five working live collectors.
- **OddsAfrica / surebet-scanner**: collector patterns from other regions; not immediate local book coverage. Missing/unclear licensing and experimental implementation limit reuse.
- API SDKs and marketing catalogues do not supply self-hostable collection backends. Historical datasets do not establish simultaneous executable prices. Document actual availability separately.

Our previous successful requests were limited: BetRivers NJ listing (13 NBA events), one event detail (three markets), Sunbet listing, and InferSports requests. DraftKings and the additional FanDuel endpoint returned 403. These establish point-in-time access only. Do not convert them into sustained coverage, freshness, or profit claims.

## Merged architecture

Provider adapter -> raw observation log -> schema validation -> canonical matching -> current quote state -> arbitrage engine -> calculator/revalidation -> API/dashboard -> opportunity journal/replay.

Adopt the engineer’s boundaries and data model. Preserve source-specific identity and permission metadata. A second provider initially reconciles/monitors rather than silently replacing primary prices.

For a small local prototype, Postgres alone can hold current quotes and history, as the engineer explicitly permits. Add Redis/queues only when measured throughput/recovery needs justify them. Do not make the whole PickPocket deployment stack a prerequisite.

Language/framework remain a proposal: Python is attractive for collection and reusable research code; TypeScript suits the UI and potentially domain engine. Validate the source route before choosing whether the backend should be Python or TypeScript. Avoid duplicated independent financial logic across languages; choose one authoritative calculation implementation and shared test vectors.

Use decimal arithmetic for odds/money and integer currency increments with an explicit rounding policy. Provider secrets stay server-side. No sportsbook account credentials are needed for the scanner/calculator phases.

## Data-source experiment before commitment

Compare three routes against the same target-book and market matrix:

A. A licensed vendor trial/sample (the engineer’s OpticOdds/OddsJam API candidates; entitlement and cost unconfirmed).
B. Permitted direct collection informed by the reviewed repositories.
C. Recorded/synthetic data for unlimited deterministic development; explicitly unable to establish current betting feasibility.

For each relevant source record: exact book and jurisdiction, events/markets offered, source timestamp semantics, observed/source age, cross-book time skew, suspensions, disconnect recovery, request quotas, data-use permission, projected costs, and mapping failures. One relevant sport/market is enough for the first harness measurement; expand the pilot toward the engineer’s NHL/NBA moneyline/spread/total scope only after it works.

Decision: select sources based on measurements and permitted use. If free sources cannot provide the relevant books/freshness, keep the free artifact a research/demo tool and explicitly decide whether paid data is worthwhile. Do not promise broad real-time coverage at $0.

## Proposed milestones aligned to the engineer’s phases

### 0. Source feasibility and offline foundation

Create source-validation harness, canonical quote contract, fixture/replay format, and provider evidence matrix. Validate calculator on supplied examples. Record live/recorded/synthetic provenance. No vendor purchase implied.

Exit: credible target-book/market coverage assessment; source-age definitions; sampled update and recovery behavior; licensing/access status; explicit remaining gaps. Measured coverage requires a defined expected inventory and sample window, not just a percentage target.

### 1. Local comparison and calculator

Limited pregame NHL/NBA game markets, 3–5 books only if actually validated. Comparison board, source timestamps, local journal, budget/fixed-leg calculator, stake rounding/limits and all-outcome profit table. No props/alternates/live/execution in pilot.

Exit: deterministic math/replay checks, auditable matching, and tested stale/suspended/missing-input behavior. No quote lacking eligibility evidence is presented as executable.

### 2. Measured opportunity beta

Revalidation, invalidation reasons, opportunity lifetime, alert deduplication, simulated acceptance delays/rejections and balance effects. Manual execution records only if the user separately opts into lawful personal testing.

Exit: measured revalidation survivors, rejection/mismatch rates, source coverage and recovery. Simulated returns are labelled as simulated. A displayed opportunity or profitable streak is not proof of realizable profitability.

### 3. Controlled expansion

Add books/props/live/deep links one segment at a time, repeating coverage, permissions, matching and freshness checks. Public sharing/commercial launch has its own vendor-rights, security, deployment and applicable regulatory review.

### Future: execution feasibility, not a promised release

Investigate eligible operators’ permitted execution interfaces. Require idempotency, balance/exposure limits, duplicate prevention, acceptance/settlement reconciliation, a kill switch and explicit handling of a first accepted leg followed by a rejected second leg. No atomic transaction exists across separate books; design cannot eliminate that execution exposure. Overnight execution requires separate review after supported access and measured workflow are established.

## Technical clarifications to carry back to the engineer

- Enforce source quote age as well as receipt age and cross-book skew. A just-received stale quote can pass a receipt-age-only check; shared ancient source timestamps can pass skew alone. Define clock offset/tolerance and future timestamp handling.
- Maintain quote state in a provider/region-aware namespace. Do not let different regional variants or reconciliation sources overwrite each other under only selection/book identity.
- A stream proves timely delivery of vendor messages, not necessarily freshness at the originating sportsbook or acceptance availability. Measure both where evidence permits it.
- Matching/coverage targets need denominators, audit sample sizes, time windows and severity categories. Zero observed mismatch in a bounded sample is not a guarantee of zero future mismatch.
- Revalidation rejection rate and audited semantic mismatch rate are different measurements. Many failed revalidations are normal market movement; do not conflate them with inaccurate market matching or report an unexplained combined false-positive metric.
- Equal exact lines are a conservative MVP eligibility rule. More general differing-line combinations can require explicit payoff-state analysis; excluding them initially is a scope choice, not proof every differing-line hedge is invalid.
- Missing stake-limit data must remain unknown. A revalidated price is still not an accepted wager.

## Research files

- Original engineer report: /Users/siddhpatel/Downloads/REA-OddsJam-Research-Report-2026-10-26.md
- First repository review: outputs/arbitrage-research/github-data-source-review.md
- Topic follow-up review: outputs/arbitrage-research/github-topic-followup-review.md

No implementation, purchase, external outreach, PickPocket edit or bet was performed as part of this reconciliation.
