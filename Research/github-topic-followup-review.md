# Follow-up: user-supplied GitHub sources

Reviewed October 26, 2026. Research only; no direction selected.

## Scope

- Opened both supplied topic pages and read Scalper666/awesome-sports-betting in full. It is a curated resource directory, forked from ianalloway/awesome-sports-betting, not an odds collector.
- Refreshed topic membership through GitHub Search API to avoid stale cached topic pages: 193 odds repositories and 104 odds-api repositories, 288 unique. Screened metadata/descriptions across that inventory; did not source-audit all 288.
- Downloaded 13 additional repositories and inspected READMEs/file structure and relevant implementation code as described below. No third-party scripts executed or dependencies installed.
- Checked provider pricing where repository claims might be stale. Only bounded public/read-only data requests; no accounts, payments, credentials or bets.

## Key findings

The topic pages add InferSports as a limited hosted keyless feed candidate and two useful calculator/schema references. They do not establish an open-source, free, all-books/all-markets replacement for OddsJam data collection. Keep previous candidates under consideration; the direction decision remains open.

## Curated-list assessment

The supplied awesome list primarily links odds vendors, sportsbook sites, historical datasets, statistics libraries, prediction models, bankroll tools and reading. These may help later analytics, but historical results/model probabilities cannot supply simultaneously executable cross-book prices. Entries called DraftKings API and FanDuel API link sportsbook homepages, not maintained integration libraries. Kambi entry links the B2B provider homepage. Treat as discovery pointers, not access documentation or guarantees.

Source: https://github.com/Scalper666/awesome-sports-betting

## Additional repository review

### infersports/infersports-skill

- URL: https://github.com/infersports/infersports-skill
- Snapshot: `be079875b62a6af00fd9c16860cec6cb4168b654`; repository pushed timestamp 2026-06-11T15:22:58Z; detected license MIT.
- Assessment: **New limited hosted-data candidate**.
- Evidence and limits: Shell/Python clients for hosted InferSports REST/MCP. This repository does not contain the sportsbook collection backend. Read README, API reference, today.sh and common endpoint definitions. Ordinary keyless read-only API calls succeeded for today matches, bookmaker catalogue and one NBA event odds. Free catalogue returned Crown, Sbobet, Macau, M8bet, Nova88, HKJC; explicit note excludes Pinnacle. Returned odds have status and per-quote timestamps. Sample includes suspended zero prices and older quotes despite top-level stale=false; downstream freshness/status checks remain necessary. No North American book coverage established. MIT client code is not a blanket license for hosted data.

### 0xENTYPER/arbitrage-betting-engine

- URL: https://github.com/0xENTYPER/arbitrage-betting-engine
- Snapshot: `20aba01d77caad8fb9050d2baee1c7163e7596e4`; repository pushed timestamp 2026-10-06T18:48:31Z; detected license MIT.
- Assessment: **Useful calculator/validation reference**.
- Evidence and limits: MIT TypeScript pure analysis engine with freshness filtering, declared outcome coverage, best-price selection, integer stake increments and minimum-payout verification. Read engine.ts and types/example documentation. No live odds collection or execution. Does not independently establish settlement-rule equivalence; providers must supply that identity. Still uses JS number arithmetic in parts and needs our own edge-case/precision review before money use. Tests found, not run.

### jigonyoo/odds-consensus

- URL: https://github.com/jigonyoo/odds-consensus
- Snapshot: `c4260d0f154c3296265a0d8226ba37f144d6ca20`; repository pushed timestamp 2026-08-08T13:54:23Z; detected license MIT.
- Assessment: **Useful matching/schema reference; no live feed**.
- Evidence and limits: MIT Python pipeline for normalized rows, vig removal and consensus. Source adapter reads generated local fixtures in The Odds API response format. Five bookmaker names in a fixture are not five independently working collectors. Read adapter source and schema/readme. Appropriate for learning validation, not a solution to data access.

### PeterEkwere/OddsAfrica

- URL: https://github.com/PeterEkwere/OddsAfrica
- Snapshot: `d2bb6c5b0c5d1b5ee0bc18766fda13b67b1d59ee`; repository pushed timestamp 2026-10-06T20:31:40Z; detected license Not detected.
- Assessment: **Actual direct collector reference, wrong regional fit**.
- Evidence and limits: Multiple Python bookmaker modules and endpoint tables for African-market books, including SportyBet, Bet9ja, BetKing, NairaBet, 1xBet and others. Read module inventory, endpoint references and SportyBet implementation. Stronger collector evidence than a mere README list, but no current endpoint validation. README-referenced requirements.txt, config example and LICENSE are absent at inspected snapshot. No detected license; not a drop-in dependency. Some source includes fixed browser/session headers; no credentials used or repo code executed.

### enesmertcetin/surebet-scanner

- URL: https://github.com/enesmertcetin/surebet-scanner
- Snapshot: `c5c4c5a1e8e75dbb4b69e64ec570295a9566b9bc`; repository pushed timestamp 2026-03-12T17:11:01Z; detected license Not detected.
- Assessment: **Experimental endpoint-discovery toolkit**.
- Evidence and limits: Node/Playwright/WebSocket scripts for Digitain and brands such as Bilyoner, Holiganbet and Tempobet. Actual collector/formatter/comparison scripts, but many probes and hardcoded domains, no established Canadian/US coverage, no license detected. No scripts executed.

### erdieee/allusion

- URL: https://github.com/erdieee/allusion
- Snapshot: `05c9555ba42414e039d7465b354ad49b7283c6b1`; repository pushed timestamp 2024-03-11T20:50:21Z; detected license MIT.
- Assessment: **Older comparison-site alternative**.
- Evidence and limits: MIT Python/Playwright OddsPortal collector plus arbitrage analysis. Read scraper.py, README and file structure. Last pushed March 2024; no live validation. Adds another implementation to compare against OddsHarvester, not evidence of wider or fresher coverage.

### dave-mio1905w9/fanduel-odds-scraper

- URL: https://github.com/dave-mio1905w9/fanduel-odds-scraper
- Snapshot: `33b7c4c3a0e992b36120f535e57de2f3e5ec3f84`; repository pushed timestamp 2026-10-26T01:44:13Z; detected license Not detected.
- Assessment: **Not validated as working collector**.
- Evidence and limits: Tiny httpx FanDuel client, no license detected. Reads /api/sports and /api/event/{id}/markets under sportsbook.fanduel.com. Ordinary GET to listed sports route returned HTTP 403. update-docs workflow updates README last-checked marker and checks local documentation links, not sportsbook connectivity. Thus recent date cannot be taken as collector health proof.

### DoroninDobroCorp/pinnacle_streamer_full_table

- URL: https://github.com/DoroninDobroCorp/pinnacle_streamer_full_table
- Snapshot: `42e49a74b23363a09676795c2f014686aa9e9347`; repository pushed timestamp 2026-10-23T00:19:12Z; detected license Not detected.
- Assessment: **Storage consumer, not self-contained data source**.
- Evidence and limits: Python WebSocket ingestion to PostgreSQL with CSV/Mega archive pipeline. Requires WS_PINNACLE_URL and WS_ANALYZER_URL supplied by user; generic client sends filters to those URLs. Does not supply a public working Pinnacle feed itself. No license detected. Source read; not executed.

### 1pperalta/ScrapOddsAPI

- URL: https://github.com/1pperalta/ScrapOddsAPI
- Snapshot: `abfc13a28541acf4ef5c000859c167fc15e6ab73`; repository pushed timestamp 2026-04-16T01:13:33Z; detected license Not detected.
- Assessment: **Excluded for data sourcing**.
- Evidence and limits: Despite scraper name, README and scrapping layer use The Odds API, with Flask/LangGraph/React/RAG downstream. Does not solve rejected provider dependency. No detected standard license.

### cengizmandros/odds-arb-scanner

- URL: https://github.com/cengizmandros/odds-arb-scanner
- Snapshot: `aa586de26073835dac57e7f4ac4816c3f8f34a06`; repository pushed timestamp 2026-04-18T07:43:49Z; detected license Not detected.
- Assessment: **Excluded for data sourcing**.
- Evidence and limits: README and odds_client use the-odds-api.com. Also README formula (1-book_sum) is not ROI on total stake, which is 1/book_sum-1; example contains inconsistent arithmetic. No detected license. Not a trusted math foundation without independent review.

### odds-api-io/odds-api-python

- URL: https://github.com/odds-api-io/odds-api-python
- Snapshot: `081280bf061eb31447ffcfa0ffb80a2b8ebb810b`; repository pushed timestamp 2026-10-13T11:29:40Z; detected license MIT.
- Assessment: **Commercial feed SDK, not open collection backend**.
- Evidence and limits: MIT client for separate provider Odds-API.io (not The Odds API at the-odds-api.com). SDK README still advertises free keys; current provider pricing page says new free keys paused, Solo GBP49/month for 2 selected bookmakers, 5000 requests/hour. Source client does not grant self-hosting of backend or every bookmaker at $0. Coverage headline is provider catalogue, not plan entitlement.

### odds-api/odds-api

- URL: https://github.com/odds-api/odds-api
- Snapshot: `1b8d4bdddf01c610eb725dc610f12ab53a20dba8`; repository pushed timestamp 2026-09-27T03:48:53Z; detected license Apache-2.0.
- Assessment: **Hosted-service documentation/SDKs**.
- Evidence and limits: Apache-2.0 OpenAPI specs, clients, examples, MCP and mock mode for odds-api.net. API key required for live service. Open SDK/mock code does not provide the collection backend or establish free unlimited feeds. Distinct from the-odds-api.com and odds-api.io.

### edushinka/betbetter-python

- URL: https://github.com/edushinka/betbetter-python
- Snapshot: `d124afdc6e44fba11b3392977892f31f67fd9840`; repository pushed timestamp 2026-08-31T01:28:23Z; detected license MIT.
- Assessment: **Model outputs, not sportsbook odds**.
- Evidence and limits: MIT client for keyless Bet Better model feed. README explicitly says no bookmaker prices are republished; exposes model probabilities/fair odds/verdicts. Not suitable to detect cross-book arbitrage prices.

## Point-in-time public endpoint checks

- New FanDuel scraper listed sports endpoint: HTTP 403, not JSON. No bypass attempted.
- InferSports list_today_matches: HTTP 200, two NBA event records.
- InferSports list_bookmakers: HTTP 200, six names listed above, Pinnacle excluded on free tier.
- InferSports get_match_odds: HTTP 200 for returned event id evt_QNDN4QCS. Event labelled Hornets vs W.Wizards, NBA, scheduled. Actual sample included open and suspended quotes with per-quote as_of values. This verifies returned data, not its independent correctness or freshness against sportsbook screens.

## Pricing discrepancy checked

Odds-API.io official current pricing: https://odds-api.io/#pricing — new free keys paused; Solo GBP49/month includes two selected bookmakers, 5000 requests/hour. Its SDK README free-tier statement should not be used to budget the project. No paid plan purchased.

## Practical implications

No need to finalize a stack from this pass. Separate (a) working direct collection code, (b) clients for hosted providers, (c) fixture-only demos, (d) math/validation libraries, and (e) historical datasets. Only the first two can supply current input data, and their coverage/permissions/freshness still require validation.
