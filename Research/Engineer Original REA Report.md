# Odds-comparison platform: feasibility and implementation blueprint

**Research date:** 2026-10-26 (America/Toronto)  
**Scope:** permitted public sources plus one controlled REA capture of a public OddsJam page. No login, subscription, purchase, bet placement, credential extraction, rate-limit bypass, or anti-bot bypass was attempted.

## 1. Decision in one page

**Verdict: feasible as an odds-comparison MVP; not yet proven feasible as an actionable-arbitrage product in Quebec.** The calculation is straightforward. The hard, business-critical problem is acquiring a licensed feed that is both sufficiently fresh and explicitly permitted for the intended customer-facing display, comparison, deep linking, alerting, and geography. A stale or mismatched quote converts a theoretical arb into a false signal.

**Recommended first release:** Ontario/Canada-capable source validation first, but ship the pilot narrowly: pre-match NHL/NBA moneyline, spread, and total; 3--5 explicitly covered books; no player props, alternate lines, in-play, or auto-betting. Use one licensed aggregation vendor with a push feed as primary, retain a second independent source only for monitoring/reconciliation (not silently to merge conflicting terms), and label every opportunity as *indicative until revalidated*.

**Recommended commercial sequence:**

1. Request written coverage, latency, quota, historical/replay, and redistribution terms from **OpticOdds** and **OddsJam API** for the exact Canadian/Quebec product, named books, and UI/deep-link use case. Both advertise broad real-time data, but the public pages do not establish the necessary Quebec availability or display rights. [OpticOdds API guide](https://developer.opticodds.com/docs/odds-api-getting-started-guide) and [OddsJam API page](https://dev.oddsjam.com/odds-api).
2. Run the two-week measurement POC below before promising arbitrage alerts. If a vendor cannot demonstrate fresh coverage for the selected books, use it for comparison only, not actionable arbs.
3. For a robust media-grade alternative, price Sportradar Odds Comparison (including the exact country/book configuration). Its public docs expose normalized markets and change-log workflows, but access and book coverage are key-specific and commercial. [Sportradar API basics](https://developer.sportradar.com/odds/docs/oc-ig-api-basics).

The largest unresolved bottleneck is therefore **contractual, source-specific Canadian/Quebec coverage plus measured end-to-end latency**, not implementation capacity.

## 2. Evidence labels used in this report

| Label | Meaning |
|---|---|
| Observed | Captured in this environment or explicitly stated in a primary source. |
| Inferred | A reasonable design inference, never a claim about OddsJam internals. |
| Unknown | Not available from authorized public observation, a captured artifact, or vendor documentation. |

Vendor speed, volume, and coverage marketing are vendor claims unless the POC measures them.

## 3. REA readiness and boundaries

### Confirmed in this environment — observed

REA is connected through MCP. Live tool inventory includes `capture_browser_scenario`, `analyze_web_bundle`, `analyze_javascript_application`, `export_web_scripts`, `inspect_web_page`, `observe_web_session`, and `export_evidence_bundle`, as well as native/managed-code tooling. The connected runtime reported JavaScript static analysis defaults of a 300,000 ms timeout and 1,024 MiB worker heap. This is current connected-server evidence, not an assumption from the repository.

One REA controlled browser scenario launched provider-owned Chrome (Chromium 155.0.8059.85) against `https://oddsjam.com/betting-calculators` on 2026-10-26. It captured DOM/accessibility/URL and network metadata with response bodies selected. The final DOM was Cloudflare's “Just a moment...” challenge; no OddsJam calculator app, authenticated screen, market request, WebSocket/SSE, or sportsbook payload was reached. The capture is therefore direct evidence of the access limitation only, not evidence of OddsJam implementation.

Exported evidence: `REA-OddsJam-REA-Evidence-2026-10-26.json` (74,712 bytes, one record, no unknown records at export). Its REA evidence ID is `ev_655f2e47573a15b4766fe35946d42cf2063dfe93f48d5ace9e2f8626153d4e0b`.

### What REA can do when access is authorized

* Launch a temporary provider-owned browser profile for a declared URL/action sequence, or attach only to an explicitly named loopback CDP target. It can retain DOM, accessibility, screenshots, and bounded network/WebSocket event evidence.
* Inspect already accessible browser scripts and use static bundle analysis to identify routes, endpoint candidates, module/chunk links, source-map availability, and value-free JSON/WebSocket shapes; exported scripts can be statically analyzed without execution.
* Export accumulated Evidence as a local bundle. REA documentation says its results include evidence and limitations; browser captures distinguish incomplete/truncated/missing observations rather than treating absence as evidence. [REA README](https://github.com/morluto/rea) and [browser observation contract](https://github.com/morluto/rea/blob/main/docs/browser-observation.md).

### Prerequisites and limits

* Browser capture needs an installed Chrome-family executable (launch) or a caller-owned Chrome-family browser exposed at a **loopback** CDP endpoint with a selected target (connect). Static app analysis needs an accessible local artifact. Native-analysis tools additionally require a configured provider such as Hopper/Ghidra/IDA, depending on target. [REA README](https://github.com/morluto/rea).
* REA does **not** bypass login, paywalls, anti-bot systems, origin restrictions, or sportsbook authorization. Do not use it to circumvent Cloudflare or access an OddsJam account not supplied and authorized by its owner.
* Client-visible endpoints, bundled strings, request timing, and payloads cannot establish an upstream sportsbook contract, licensed source, server-side matching/validation, caching topology, or calculation implementation. They establish only what was observed at the client boundary.

### Authorized follow-up capture protocol

If an authorized OddsJam account/session and permission to inspect it are provided, capture a small declared workflow: load screen → select one known event/market → wait for data → open calculator → change a permitted filter. Retain only needed network metadata/body shapes; redact tokens and secret fields. Record: URL/origin, capture time, user-visible filter state, request method/path, response shape, event/book/market/selection IDs, source timestamps, protocol (poll/SSE/WS), and update sequence. Export Evidence immediately and cite IDs in a separate appendix. This should not be confused with discovering OddsJam's upstream data sources.

## 4. OddsJam map: documented vs unknown

### Documented public product claims — observed from official pages

| Area | Publicly documented evidence | Confidence |
|---|---|---|
| Odds API / screen | OddsJam advertises real-time pre-match and in-play odds, main/alternate/prop markets, futures, deep links, schedules, injury data, results, push feeds, and an auto-grader. It says JSON/XML are supported and promotes 100+ sportsbooks. [Official API page](https://dev.oddsjam.com/odds-api) | Observed claim; coverage/latency not independently measured |
| Arbitrage | OddsJam markets an arbitrage tool ordered by “guaranteed profit percentage”; its public tools page claims real-time data and more than 10K arbitrage bets monthly. [Tools page](https://oddsjam.com/betting-tools) | Observed claim |
| Filters / controls | The official FAQ indexes sportsbook and sport/league exclusion questions, and arbitrage email alerts. [FAQ](https://oddsjam.com/faq) | Observed feature category; exact UI/semantics unknown |
| Calculators | Public calculator index lists Arbitrage, EV, hold, implied probability, no-vig, odds conversion, parlay, vig, and related calculators. [Calculator index](https://oddsjam.com/betting-calculators) | Observed |
| Commercial API | OddsJam asks prospects to contact sales for API access/pricing; public pricing for API and data rights was not found. [API page](https://dev.oddsjam.com/odds-api) | Observed: quote required |

### Client technology and request map

* **Observed:** the only REA web capture encountered Cloudflare challenge resources, not OddsJam application assets.
* **Unknown:** authenticated app URLs, API hosts, request/response schema, event/market/selection/book IDs, polling/WS/SSE use, snapshot versus delta semantics, caching headers, server/client calculation division, filter behavior, expiry behavior, and bet-link construction.
* **Not a safe inference:** no conclusion about OddsJam's upstream providers can be drawn from public UI claims or a client endpoint even if one becomes visible.

## 5. Provider comparison and coverage matrix

The rows below are a decision shortlist, not a claim that every source has rights for a public Canadian product. “Quote required” includes pricing and rights not publicly documented for this exact use.

| Rank / role | Feed and evidence | Delivery / documented freshness | Canada / Quebec relevance | Props / historical | Commercial conclusion |
|---|---|---|---|---|---|
| 1 — primary POC candidate | **OpticOdds**: documented discovery, current snapshots, SSE odds streams, locked-odds events, results/grading, futures, full price history, and 100+ books. [Guide](https://developer.opticodds.com/docs/odds-api-getting-started-guide), [book list](https://developer.opticodds.com/docs/sportsbooks) | SSE (not WebSocket/webhook); public limits: 2,500 normal req/15 s, 250 streaming connections/15 s, historical 10 req/15 s. | Static catalog explicitly includes Quebec-relevant brands such as Mise-o-jeu, PlayNow, PointsBet Ontario, Proline, Sports Interaction, BET99, BetMGM, BetRivers, and Betano; **not proof that each is available for your account/market or Quebec**. | Current/active market discovery; alternate/main flag; full history per odds ID; broad markets claimed. | Strongest transparent startup candidate. Pricing and redistribution/display/deep-link rights: **quote required**. Require written Canadian/Quebec confirmation and measured source freshness. |
| 2 — quality / enterprise alternative | **Sportradar Odds Comparison v2**: normalized event→market→book→outcome model, four product families (prematch, live, props, futures), mappings and change logs. [Overview](https://developer.sportradar.com/odds/docs/oc-ig-overview), [fundamentals](https://developer.sportradar.com/odds/docs/oc-ig-fundamentals) | REST; live documentation says refresh 15–30 seconds, and recommends change-log driven refresh for changed events. [Live overview](https://developer.sportradar.com/odds/reference/oc-live-odds-overview) | Its books endpoint returns only books configured for the key. Global Core advertises 140+ global books but public docs do not verify Quebec book entitlement. | US tier has extensive player props; Core global player props are documented as limited largely to soccer goalscorer markets. Market and history entitlement must be quoted. | Appropriate for mature/regulated media architecture, likely higher commercial/integration bar. **Quote required**. Not suitable for sub-second actionable claims based on public 15–30 sec documentation. |
| 3 — incumbent / benchmark / possible primary | **OddsJam API** advertises 100+ books, JSON/XML, push feed, main/alternate/prop/live/futures, deep links and historical data. [Official API page](https://dev.oddsjam.com/odds-api) | “Push stream” and “real-time” are documented; numerical SLA/update cadence is not public. | No public, verifiable book-by-region entitlement found in reviewed page; Canada/Quebec **unknown**. | Claims props, alternates and full historical database; formats/rate limits/details **unknown publicly**. | Technically plausible, commercially attractive given stated product; all pricing, rights, coverage and latency: **quote required**. Do not copy/derive their private implementation. |
| 4 — lower-cost comparison baseline, not live arb primary | **The Odds API** documents snapshot REST, market `last_update`, bookmaker/source IDs option, historical snapshots, and Canadian bookmaker list. [V4 docs](https://the-odds-api.com/liveapi/guides/v4/), [Canada book list](https://the-odds-api.com/sports-odds-data/bookmaker-apis.html) | Published intervals: featured pre-match 60 sec / in-play 40 sec, additional markets 60 sec, exchanges 20/10 sec. [Intervals](https://the-odds-api.com/sports-odds-data/update-intervals.html) | Explicit `ca` entries include BET99 ON, Betano ON, BetMGM ON, BetRivers ON, PlayNow, PointsBet CA, Proline ON, Sports Interaction ON. Quebec availability still must be confirmed per operator/terms. | Extra markets via per-event endpoints; historical snapshots 5 min from Sep-2022 (paid), which is useful replay but not tick history. | Great benchmark and simple comparison MVP source; its documented cadence makes it **not** a primary actionable-arb feed. Public plans exist, but exact current plan/redistribution rights should be confirmed before launch. |

### Coverage facts and release boundary

Verified from current public docs: The Odds API names eight Canada-region book entries (some Ontario-specific, plus PlayNow and Sports Interaction), while OpticOdds’ static list contains several Canadian brands but does not present a jurisdiction guarantee. No reviewed primary source verified a complete Quebec coverage set, pricing, or display/redistribution rights for the proposed product. Therefore, the initial “coverage matrix” must remain *vendor-validated*, not marketing-derived.

**Release gate matrix to obtain from every finalist, signed or written:**

| Requirement | Required proof |
|---|---|
| Geographic and book coverage | Exact book IDs + regulated jurisdiction + legal display/deep-link permission for Canada and Quebec, supplied by vendor. |
| Market coverage | Per-book table for NHL/NBA moneyline/spread/total, periods, alternates, player props, live. |
| Freshness | Source timestamp semantics; 24 h sample of source/receipt/publish latency and percentiles. |
| Delivery/recovery | Snapshot + delta/SSE contract, cursor/replay/sequence semantics, reconnect behavior and connection quotas. |
| Commercial | Written permission for customer-facing display, comparison, derived alerts, storage/replay, and any affiliate/deep-link use. |
| Limits | Rate/connection quotas, overage pricing, retention duration, availability/SLA, incident process. |

### Why direct sportsbook scraping is not a launch strategy

It is potentially lawful only where the source terms, jurisdiction, robots/rate limits, and intended use permit it; it remains operationally brittle due to bot controls, login state, locale pricing, frequent UI/API changes, market suspensions, and rights. It also does not solve redistribution licensing. Do not depend on it for a commercial product. If a sportsbook offers an official partner API/feed, integrate only after written permission and treat it as a provider adapter with its own canonical mapping and contract tests.

## 6. Correct arbitrage and hedge math

### Odds conversion

For American odds `a`:

```text
decimal(a) = 1 + a/100       when a > 0
decimal(a) = 1 + 100/abs(a)  when a < 0
```

For mutually exclusive and collectively exhaustive outcomes with decimal odds `d_i`:

```text
overround_inverse_sum = Σ (1/d_i)
arbitrage exists only if overround_inverse_sum < 1
```

With budget `B`, equal gross payout allocation is:

```text
S_i = B × (1/d_i) / Σ(1/d_j)
gross_payout = B / Σ(1/d_j)
profit_i = gross_payout - B                 # before fees / rounding
```

This applies only after market equivalence and settlement compatibility are proven. A middle is not arb because outcomes can both lose/one side can push depending on score interval. Positive EV is a probability/model claim, not a guaranteed cross-book payoff.

### Required matching key before calculation

An eligible group needs the same canonical:

```text
sport, league, event (participants + start time), market family,
period, line value and units, overtime/extra-inning treatment,
selection/outcome semantics, player identity (when a prop),
currency, settlement/void rules, and active state.
```

Do **not** match just strings such as “Over 6.5.” NHL “total incl. overtime” and a regulation-only market are different contracts. A three-way soccer 1X2 market requires home/draw/away; pairing home/away alone is invalid. Store provider-specific IDs but derive a versioned canonical key with an explainable mapping record and review queue for ambiguous entities.

### Incremental detection pseudocode

```text
on_quote(q):
  assert provider contract + schema validates
  record raw quote immutably (source_at, received_at, processed_at)
  canonical = map(q)                         # may return ambiguous/rejected
  if canonical is not exact and settlement-compatible: return
  if q.suspended or q.price invalid or q.out_of_order: expire(q); return

  replace current_quote[(canonical.selection_key, q.book)] only if
      q.source_sequence is newer OR q.source_at is newer
  group = market_group(canonical.market_key) # all outcomes for one exact market
  best[outcome] = best active quote across allowed books satisfying max_age
  if any required outcome missing: invalidate(group); return
  if same book prohibited by product rule: enumerate valid book combinations

  inv = sum(1 / best[outcome].decimal for outcome in outcomes)
  candidate = inv < 1 - safety_margin
  if not candidate: invalidate(group); return
  if max(source_at)-min(source_at) > max_cross_book_skew: return
  if any now - received_at > max_quote_age: return
  if not limits/stake_increment/fees/currency make all profits > 0: return

  revalidate both/all selected quotes with a fresh snapshot or stream sequence
  if still active, exact key matches and post-rounding min_profit > threshold:
      upsert opportunity with selected quote IDs + evidence fields; publish once
  else invalidate with reason
```

For 2–3 outcome MVP groups, recomputing only the changed group is O(number of books × outcomes), cheap and safe. At scale, maintain per-outcome top-k active quotes and re-evaluate combinations only when the top-k changes; preserve a full audit trace rather than optimizing away correctness. Never publish on a quote whose clock, sequence, or state is unknown.

### Tests that must exist

1. Exact two-way, same line, fresh quotes produces correct stakes/profits.
2. `Over 6.5` versus `Under 7.0`, regulation versus including OT, player name collision, wrong period, and 1X2 missing draw are rejected.
3. Out-of-order delta, duplicate delta, suspended/locked quote, feed disconnect, null source timestamp, and stale quote invalidate.
4. 3-way outcome math works; unavailable third leg does not create an arb.
5. Stake cap, $0.01/$0.05 increments, fees/commission, FX, and available-balance constraints can eliminate theoretical arb.
6. Revalidation price drift/leg rejection invalidates display and emits a reason.
7. Deterministic replay of recorded raw quotes yields the same opportunity decisions/versioned mappings.

### Hedge calculator validation

Given first leg stake `S1` at decimal `d1`, equal gross payouts for the other two-way outcome at `d2` use:

```text
S2 = S1 × d1 / d2
```

Example:

```text
Over −110: d1 = 1 + 100/110 = 1.9090909091; S1 = 1000.00
Under +115: d2 = 1 + 115/100 = 2.15
S2 exact = 1000 × 1.9090909091 / 2.15 = 887.9492600...
S2 rounded to cents = 887.95
Total staked = 1887.95

Over wins: 1000 × 1.9090909091 − 1887.95 = 21.1409091... => $21.14
Under wins: 887.95 × 2.15 − 1887.95 = 21.1425000... => $21.14
```

So the requested approximately $887.95 and $21.14 are correct before fees. The output must show **rounded** stake and recomputed per-outcome profits, not just a theoretical equal-profit number. For push/void, present a separate settlement row using the applicable bookmaker rules; do not assume a void is a loss or a push refunds every leg equally. A calculator cannot ensure the hedge price/limit remains available after the first leg is accepted.

## 7. Practical architecture

### MVP flow

```text
licensed provider adapters
  -> raw immutable event log + schema validation
  -> normalization/mapping service
  -> current quote store (Redis) + relational source of truth (Postgres)
  -> incremental arb engine + revalidator
  -> REST/SSE API
  -> comparison/opportunity UI + hedge calculator
```

**Adapter:** one process per provider, one provider contract. It authenticates server-side, reads snapshot/delta, captures provider source sequence/time, and writes raw facts. It does no cross-book business logic.

**Ingestion:** idempotency key `(provider, feed_partition, source_sequence)` when available, else payload digest plus source/receipt time. Persist raw provider payload in encrypted object storage or compressed Postgres partition only if licensed retention permits it.

**Normalization:** maps provider IDs to canonical entities with mapping version, confidence and reviewer provenance. It must model market period, line, settlement terms, live state, and player identity separately—not concatenate display names.

**Current state:** Redis (or Postgres in early MVP) holds latest active quote per `(selection_id, book_id)`, expiry/deadline, provider sequence, and source/receipt/processed timestamps. PostgreSQL retains event/market/selection identity, mapping history, quote history, and opportunity audit records.

**Engine:** consumes normalized quote updates, recomputes only affected market groups, applies hard eligibility gates, persists the selected quote IDs, and revalidates before publish. It has no betting credentials and never places bets.

**Delivery/UI:** REST for initial state and authenticated SSE for deltas. The client treats an opportunity as provisional and shows book, exact line/period, timestamps, probability/arb margin, limits caveat, and expiry reason. Deep links are enabled only where vendor/book terms authorize them.

### Core relational model (abbreviated)

```sql
providers(id, name, contract_version, region_scope, enabled)
provider_books(provider_id, provider_book_id, canonical_book_id, jurisdiction, active)
events(id, sport, league, start_at, home_participant_id, away_participant_id, status)
provider_events(provider_id, provider_event_id, event_id, mapping_version, confidence)
markets(id, event_id, family, period, includes_overtime, line_value, settlement_key)
provider_markets(provider_id, provider_market_id, market_id, mapping_version)
selections(id, market_id, outcome_key, participant_id nullable, player_id nullable)
provider_selections(provider_id, provider_selection_id, selection_id, mapping_version)
quotes(id, provider_id, provider_quote_id, selection_id, canonical_book_id,
       decimal_odds, american_odds, status, max_stake nullable, currency,
       source_at, received_at, processed_at, published_at nullable,
       source_sequence nullable, raw_payload_ref, expires_at)
opportunities(id, market_id, state, inverse_sum, min_profit, currency,
              detected_at, revalidated_at nullable, expires_at, invalid_reason nullable)
opportunity_legs(opportunity_id, quote_id, selection_id, stake, rounded_stake,
                 gross_payout, outcome_profit)
```

Add unique indexes for provider identifiers; current quote lookup by `(selection_id, canonical_book_id, status)`; time partitions for `quotes`; and immutable mapping/opportunity decision audit records. Store monetary amounts as integer minor units or decimal—not floating point.

### Example normalized quote payload

```json
{
  "quoteId": "q_01J...",
  "provider": "opticodds",
  "providerQuoteId": "...",
  "eventId": "evt_nhl_...",
  "market": {"family":"total","period":"full_game","line":"6.5","includesOvertime":true},
  "selection": {"outcome":"over"},
  "book": {"id":"book_x", "jurisdiction":"CA-ON"},
  "odds": {"american":-110,"decimal":"1.9090909091"},
  "status":"open",
  "sourceAt":"2026-10-26T15:12:00.120Z",
  "receivedAt":"2026-10-26T15:12:00.340Z",
  "processedAt":"2026-10-26T15:12:00.345Z",
  "sourceSequence":"provider-stream-..."
}
```

### API contracts

```text
GET /v1/odds?eventId=&market=&book=&maxAgeMs=
GET /v1/opportunities?region=CA-ON&sport=ice_hockey&minProfitCents=&state=active
GET /v1/opportunities/{id}              # legs, timestamps, mapping and invalidation reason
POST /v1/calculators/hedge              # input: existing leg or budget; outputs all outcome rows
GET /v1/stream                          # SSE: quote.updated, opportunity.upserted, opportunity.invalidated
```

Responses should include a schema version, exact quote IDs, source/receipt timestamps, source-age and cross-book skew, canonical matching attributes, and `indicative`/`revalidated` status. Never expose provider API keys or raw private vendor payloads to browsers.

### Recovery, monitoring, and security

* Snapshot first, then apply delta only from a documented cursor/sequence. On gap/reconnect: mark partition stale, recover from fresh snapshot/cursor, and suppress opportunities until coherent.
* Expire quotes by conservative provider-/market-specific age; invalidate opportunities immediately on any selected-leg suspension/removal/expiry.
* Deduplicate alerts on a stable fingerprint: market key + selected quote IDs/versions + rounded stake plan. Alert only when material improvement or cooldown expiration occurs.
* Measure p50/p95/p99 source→receipt, receipt→publish, cross-book skew, no-quote coverage, reconnects, mapping rejects, invalidation reasons, and post-alert false-positive reports.
* Use a secret manager, least-privilege service identities, encrypted raw evidence, tenant authorization, redacted logs, audit trails, rate limits, and vendor-rights configuration gates.

### Fit to the inspected codebase

`/Users/siddhpatel/Development/PickPocket` is a TypeScript React/Vite frontend plus TypeScript/Express backend with PostgreSQL, Redis, BullMQ, WebSocket and existing The Odds API references. It currently looks like a social/picks product; the inspected search did not establish an existing cross-book normalization, stream ingestion, quote history, arb engine, or arb UI. Integrate this as a bounded backend domain/worker and API surface; do not proxy provider APIs or keys through Vite. Existing Redis/BullMQ/Postgres/WebSocket dependencies can support the MVP, but the streaming semantics and table migrations must be designed/tested rather than assumed.

## 8. Feasibility POC and phases

### Phase 0 — commercial/data validation (1–2 weeks)

**Inputs:** two vendor trials/quotes, explicit named Canadian books, written rights answer, and a small live or recorded sample.  
**Build:** adapter harness; raw timestamp logger; source/receipt/skew dashboard; no customer-facing alerts.  
**Acceptance:** 95%+ expected selected-market coverage during sample windows, declared timestamp semantics, measured p95 source-to-receipt, known disconnect recovery behavior, and a written right to display/store/derive the intended use. Fail closed if any one is absent.  
**Cost:** vendor pricing and rights are quote required; engineering cost is one backend engineer plus QA/ops time. Do not create a public cost number from marketing claims.

### Phase 1 — comparison MVP (2–4 weeks after data approval)

**Scope:** NHL/NBA pre-match, moneyline/spread/total, 3–5 confirmed books, one jurisdiction. No props/alternates/live/affiliate links initially.  
**Acceptance:** mapping accuracy >=99.5% on manually audited sample; all current quotes show source age; stale/locked/out-of-order data is hidden; deterministic replay passes; key/provider failure tests pass.  
**Output:** comparison board and hedge calculator labelled indicative.

### Phase 2 — guarded arb beta (2–3 weeks)

**Scope:** same markets, max quote age/skew based on Phase 0 measurements, revalidation and opportunity audit.  
**Acceptance:** every displayed arb traces to exact legs, matching version, timestamps, rounded stakes and post-rounding profit; all invalidations have a reason; manual audit finds zero settlement/line mismatch false positives over pre-agreed sample size.  
**Output:** opt-in alerts, no automatic bet execution.

### Phase 3 — expand only on evidence

Add verified books, player props, alternates, in-play, deep links, second provider/reconciliation, and historical analytics one bounded segment at a time. Each expansion repeats coverage, mapping, latency, terms, and false-positive gates.

### POC measurement specification

Log each quote as live/recorded/synthetic. For live data, measure:

* `source_at → received_at → processed_at → UI published_at` latency distributions;
* maximum/p50/p95 cross-book source and receipt skew for selected candidate legs;
* expected events/markets/books versus observed coverage;
* mapping accuracy via manually reviewed stratified sample;
* theoretical candidates, post-rounding candidates, revalidation survivors, lifetime, and invalidation reason;
* estimated false positives: rejected revalidations + manual mismatch findings / initially displayed candidates;
* API calls, stream connections, bytes, storage, and vendor projected bill under actual cadence.

No live result exists yet. Credentials/licenses are the only missing inputs for this measurement plan; the architecture and offline replay tests can proceed without them.

## 9. Evidence appendix

| Source / observation | Date checked | What it supports | Confidence / remaining unknown |
|---|---:|---|---|
| [REA repository README](https://github.com/morluto/rea) | 2026-10-26 | REA MCP/CLI positioning, local analysis, setup/provider prerequisites, static JS capability | High for documented release surface; specific connected tools verified separately |
| [REA browser scenario contract](https://github.com/morluto/rea/blob/main/docs/browser-scenario-contract.md) | 2026-10-26 | declarative launch/connect capture, network artifacts, cleanup and limits | High; not evidence of OddsJam behavior |
| Local REA Evidence `ev_655f…d4e0b` | 2026-10-26 | public calculator URL hit Cloudflare challenge, no app traffic was available | High for this attempt; cannot generalize to a logged-in authorized session |
| [OddsJam API](https://dev.oddsjam.com/odds-api) | 2026-10-26 | official advertised data/API/screen features, 100+ book claim, push claim, contact-sales posture | High as a claim; latency, pricing, rights and book-by-region unknown |
| [OddsJam calculators](https://oddsjam.com/betting-calculators), [tools](https://oddsjam.com/betting-tools), [FAQ](https://oddsjam.com/faq) | 2026-10-26 | public calculator/tool/alert/filter categories | High for page content; exact workflow and calculations unknown |
| [OpticOdds guide](https://developer.opticodds.com/docs/odds-api-getting-started-guide), [sportsbooks](https://developer.opticodds.com/docs/sportsbooks), [FAQ](https://developer.opticodds.com/page/faq-page) | 2026-10-26 | SSE, endpoints, limits, locks, historical data, static book catalog | High for docs; precise customer entitlement/pricing/rights/latency must be contracted/measured |
| [Sportradar overview](https://developer.sportradar.com/odds/docs/oc-ig-overview), [fundamentals](https://developer.sportradar.com/odds/docs/oc-ig-fundamentals), [live overview](https://developer.sportradar.com/odds/reference/oc-live-odds-overview) | 2026-10-26 | normalized model, tiers, change logs and advertised live refresh | High for docs; exact books/pricing/Quebec rights are key-specific |
| [The Odds API v4](https://the-odds-api.com/liveapi/guides/v4/), [book list](https://the-odds-api.com/sports-odds-data/bookmaker-apis.html), [intervals](https://the-odds-api.com/sports-odds-data/update-intervals.html) | 2026-10-26 | Canada entries, source last-update semantics, published polling cadence, historical snapshots | High for docs; suitability for exact product rights and live quote acceptance remains unproven |

### Explicit unknowns to resolve before committing

1. Which books can legally and contractually be displayed/compared/deep-linked to for Quebec users.
2. Vendor source origin, source timestamp meaning, real observed latency and failure behavior for the target books/markets.
3. OddsJam authenticated client schema and behavior, if an authorized inspection is ever requested.
4. Stake limit availability/accuracy and book-specific settlement differences—neither can be assumed from odds alone.
5. Current product legal/compliance posture, age-gating, responsible-gambling, affiliate disclosure, and data redistribution requirements. Obtain qualified local legal/commercial advice before public launch.
