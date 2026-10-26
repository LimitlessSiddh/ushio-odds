# Sportsbook data-source GitHub review

Reviewed: October 26, 2026 (America/Toronto).

## Conclusion

Direct sportsbook collection is worth a proof of concept. No reviewed repository demonstrates reliable free coverage of every sportsbook and every market. The best direct multi-book candidate is oddswrap; the strongest comparison-site candidate is OddsHarvester. Keep source freshness, market depth, jurisdiction and reuse licensing separate.

## Scope and evidence boundaries

- Searched GitHub repository API across 14 query families plus web searches for direct sportsbook, arb, comparison-site, Kambi, Bet365, North American and Canadian collectors. Downloaded 21 selected repositories for read-only inspection. This is a broad targeted search, not an exhaustive review of all GitHub repositories.
- Inspected READMEs/file trees across the selection and implementation code in the strongest candidates; inspected recent commits/open issues for six central candidates. Did not execute third-party repositories, install their dependencies, provide credentials, or place bets.
- Tested four ordinary public GET requests: BetRivers listing; BetRivers one-event detail; Sunbet listing; DraftKings listing. No proxy, session cookies, anti-bot bypass or fingerprint impersonation was used.
- A single HTTP 200 proves point-in-time data access, not data rights, freshness, sustained reliability, complete markets, or betting eligibility.

## Independent endpoint checks

| Feed | Result | Observed payload | Limitation |
|---|---|---|---|
| BetRivers NJ/Kambi NBA listing | HTTP 200 | 13 event records, 13 offers, 26 outcomes | NJ prices; main listing only |
| BetRivers NJ one NBA event | HTTP 200 | 3 offers / 6 outcomes: Moneyline, Point Spread, Total Points Including Overtime | No deep props in this sampled payload |
| Sunbet/Kambi football listing | HTTP 200 | 152 event entries, 150 offers, 450 outcomes | South African feed; football bucket can contain simulated fixtures |
| DraftKings NJ sportscontent NBA | HTTP 403 | Access denied/non-JSON response | No attempt to bypass; connector not validated |

The sampled BetRivers event was CLE Cavaliers vs MIN Timberwolves, start 2026-10-26T23:00:00Z. No bet availability or settlement-rule equivalence was verified.

## Prioritized repository findings

### sjhouston23/oddswrap

- Repository: https://github.com/sjhouston23/oddswrap
- Reviewed default-branch snapshot: `370291c8bfcc0f2032a40cda366d76604f3a29dc`
- Repository pushed timestamp: 2026-06-03T13:51:07Z (not proof of collector maintenance).
- Verdict: **Priority 1: direct adapters**.
- Findings: Six adapters: DraftKings, FanDuel, BetMGM, Caesars, BetRivers, Bovada. Four sport enum values: NBA, NFL, MLB, NHL. Dedicated prop methods in DraftKings/FanDuel/Bovada/BetRivers. Read client.py, base.py, adapter source, models/schema documentation, and mocked DraftKings tests. DK/FD default to NJ; BetRivers defaults rsiusnj; others have state/operator configuration. get_all collects markets separately; merge uses team names, UTC date, and 3-hour clusters. This needs stricter identity validation for arbitrage. Package metadata declares MIT, but no standalone LICENSE found. No end-to-end six-book runtime validation.

### jordantete/OddsHarvester

- Repository: https://github.com/jordantete/OddsHarvester
- Reviewed default-branch snapshot: `b401809986762f0690d2a976c1d63a6b12e3e60e`
- Repository pushed timestamp: 2026-10-15T07:31:27Z (not proof of collector maintenance).
- Verdict: **Priority 2: comparison-site collection**.
- Findings: Python/Playwright OddsPortal collector, with actual market extraction, bookmaker-name resolution, blocked-outcome handling and scrape timestamps in source. Upcoming/historical/live snapshot commands. MIT. README reports narrower live coverage (often 2–4 versus 15–20 prematch), regional variation, and at least 60 seconds between live samples. Those are maintainer descriptions, not independently measured performance. Aggregator collection time does not establish sportsbook price age. Open issue #96 reports history/filter inaccuracies. Not runtime-tested.

### declanwalpole/sportsbook-odds-scraper

- Repository: https://github.com/declanwalpole/sportsbook-odds-scraper
- Reviewed default-branch snapshot: `8e791fc31a3b118936dd2f2b02e1919aaa4daeb3`
- Repository pushed timestamp: 2025-04-15T03:52:29Z (not proof of collector maintenance).
- Verdict: **Priority 3: event-level reference**.
- Findings: Python requests-based EventScraper + ten sportsbook implementations, including DraftKings, BetMGM, Caesars, BetRivers, Bovada and Australian books. Takes an event URL; does not by itself solve discovery and matching across every book. Read event_scraper.py and BetMGM/BetRivers implementations. No license detected. Last default-branch commit April 2025; open Ladbrokes parsing issue. Not runtime-tested.

### MadunaCapital/scanner-ingestion-sunbet

- Repository: https://github.com/MadunaCapital/scanner-ingestion-sunbet
- Reviewed default-branch snapshot: `cfa7457641caa95c56b860eb04ad2bdcdfabaff9`
- Repository pushed timestamp: 2026-10-05T13:06:21Z (not proof of collector maintenance).
- Verdict: **Priority 4: Kambi reference**.
- Findings: Python httpx Kambi adapter. Source supports football, rugby_union, cricket, tennis, basketball, although README primarily discusses soccer. Explicit event/outcome mapping and suspended-market handling. Depends on sibling ingestion/schema repos. Relevant as protocol/architecture research; Sunbet is a South African feed, not a substitute for a Quebec sportsbook. No license detected. Plain endpoint GET was successful independently; did not execute adapter code.

### M3MONs/FlashscoreScraper

- Repository: https://github.com/M3MONs/FlashscoreScraper
- Reviewed default-branch snapshot: `bcd27e3f03c5be7336fc4388b3af941acbb9f581`
- Repository pushed timestamp: 2026-10-24T09:26:59Z (not proof of collector maintenance).
- Verdict: **Secondary comparison-site candidate**.
- Findings: Python/Playwright + HTML parsers, bookmaker IDs/names/links, football-specific market classes and a generic parser for other sports. MIT. Recent activity October 2026. Inspected README, file structure and base_odds_parser.py. No independent live validation or proof of North American player-prop depth.

### kaarme01/kaarme-bet-scraper

- Repository: https://github.com/kaarme01/kaarme-bet-scraper
- Reviewed default-branch snapshot: `8e284c060783a8c39be8b8455f398ae1a9652ee4`
- Repository pushed timestamp: 2025-11-04T01:30:29Z (not proof of collector maintenance).
- Verdict: **Architecture/reference candidate**.
- Findings: MIT Python/PostgreSQL prototype with Pinnacle, Coolbet, Veikkaus and Polymarket wrappers. Source includes event/market traversal. Author explicitly calls it a prototype and identifies team/player matching and manual intervention as unresolved. Inspected wrappers and schema/file structure. Not production-ready evidence.

### Ken-Mutisya/sports-odds-scraper

- Repository: https://github.com/Ken-Mutisya/sports-odds-scraper
- Reviewed default-branch snapshot: `aba744d2f9c823cfa59ce37a176979ae92e610ac`
- Repository pushed timestamp: 2026-04-29T11:15:01Z (not proof of collector maintenance).
- Verdict: **Do not trust headline coverage**.
- Findings: MIT JavaScript Apify actor. Source league loops implement DraftKings/Pinnacle, not six dedicated sportsbook collectors. Other event URLs use a generic JSON-LD fallback. Pinnacle direct-event branch returns null. README headline coverage exceeds demonstrated source implementation. No full-board/prop coverage established. Apify-hosted usage is separate from code licensing/cost.

### personal-coding/Live-Sports-Arbitrage-Bet-Finder

- Repository: https://github.com/personal-coding/Live-Sports-Arbitrage-Bet-Finder
- Reviewed default-branch snapshot: `1e6984e026d65f45706d206c50c1938f338c5a94`
- Repository pushed timestamp: 2023-11-25T00:26:13Z (not proof of collector maintenance).
- Verdict: **Historical execution reference**.
- Findings: FanDuel/DraftKings/William Hill browser automation, payoff-matrix module and large Python scripts. Default-branch activity 2023; no license detected. README warns of acceptance delays and unmatched legs; automatic submission is commented out according to documentation. Claims of 10ms scraping are not measured end-to-end data freshness. No software executed.

### eric-barch/betbot

- Repository: https://github.com/eric-barch/betbot
- Reviewed default-branch snapshot: `d09d7af6ecc39f3986721aaf530ef91bd2958cae`
- Repository pushed timestamp: 2024-05-23T03:39:02Z (not proof of collector maintenance).
- Verdict: **Historical storage/parser reference**.
- Findings: TypeScript browser collection, FanDuel/DraftKings parser trees, Prisma/PostgreSQL/Supabase. README claims ~100ms collection; not independently measured. Setup attaches to a running Chrome instance. No license detected. Not a ready broad-coverage SDK.

### pretrehr/Sports-betting

- Repository: https://github.com/pretrehr/Sports-betting
- Reviewed default-branch snapshot: `9f96cf4e0020249a05617ab414b800ce7c058aef`
- Repository pushed timestamp: 2023-12-21T08:29:03Z (not proof of collector maintenance).
- Verdict: **Older European reference**.
- Findings: MIT French/European bookmaker assistant. Main-branch last commit retrieved is October 2021 despite newer repository pushed metadata. Open issues include installation/Chrome failures and an active-fork pointer. Book list is not North American coverage. No current functionality established.

### davccavalcante/bet365-api-scraper

- Repository: https://github.com/davccavalcante/bet365-api-scraper
- Reviewed default-branch snapshot: `164976141ec00d7471e0e531cd06066274a7c969`
- Repository pushed timestamp: 2025-08-01T09:07:31Z (not proof of collector maintenance).
- Verdict: **Do not select as Bet365 solution**.
- Findings: BSD-3-Clause. Main API script calls inplaydiary schedule collector; headers/cookies and WebSocket scripts require configuration. Open issues include 403, 526, WebSocket failures and a question asking how to obtain handicaps/odds. Recent 2025 changes in retrieved history are README changes. Does not establish a maintained complete price feed.

### S1M0N38/soccerapi

- Repository: https://github.com/S1M0N38/soccerapi
- Reviewed default-branch snapshot: `88c6733cf65f55145d7d07910756241f7710786f`
- Repository pushed timestamp: 2022-12-08T08:48:45Z (not proof of collector maintenance).
- Verdict: **Historical reference only**.
- Findings: MIT adapters for 888sport/Unibet/Kambi/Bet365. README explicitly states not actively developed and functionality may be broken. Not a maintained foundation.

### gingeleski/odds-portal-scraper

- Repository: https://github.com/gingeleski/odds-portal-scraper
- Reviewed default-branch snapshot: `a7985d7498c812ecab1b4572a210a819ecfd61eb`
- Repository pushed timestamp: 2026-07-10T20:53:44Z (not proof of collector maintenance).
- Verdict: **Older OddsPortal alternative**.
- Findings: Unlicense. Full scraper, soccer-to-SQL and prediction modules. Recent retrieved default-branch commits are dependency maintenance; old open issues include page changes/login failures. Prefer evaluating OddsHarvester first.

### Mg30/odds-portal-scraper

- Repository: https://github.com/Mg30/odds-portal-scraper
- Reviewed default-branch snapshot: `fc5c1b560019164a450caffde9295d4364e0f621`
- Repository pushed timestamp: 2025-11-24T15:19:53Z (not proof of collector maintenance).
- Verdict: **Secondary JavaScript option**.
- Findings: Node/Playwright OddsPortal CLI for soccer historical/upcoming moneyline/totals collection; local JSON or optional S3, tests. No standalone license detected in metadata. Not runtime-tested.

### flancast90/sportsbookreview-scraper

- Repository: https://github.com/flancast90/sportsbookreview-scraper
- Reviewed default-branch snapshot: `1a820e50c6fbd0276cde073c22bfffae78930868`
- Repository pushed timestamp: 2024-07-12T20:56:14Z (not proof of collector maintenance).
- Verdict: **Historical data only for this purpose**.
- Findings: MIT Python collector plus ten-year NBA/NFL/MLB/NHL archives. Source reads sportsbookreviewsonline.com seasonal HTML archives with opening/closing columns. Not a simultaneous multi-book live scanner.

### DeliciousPipe1326/edge-scanner

- Repository: https://github.com/DeliciousPipe1326/edge-scanner
- Reviewed default-branch snapshot: `e1ce082325579e62b5b95c1c0f81f8502c666ecd`
- Repository pushed timestamp: 2025-12-13T08:07:52Z (not proof of collector maintenance).
- Verdict: **Excluded: provider wrapper**.
- Findings: MIT Flask scanner. README and scanner use The Odds API. Useful scanner reference but does not remove the data-source dependency.

### ryankrumenacker/sports-betting-arbitrage-project

- Repository: https://github.com/ryankrumenacker/sports-betting-arbitrage-project
- Reviewed default-branch snapshot: `6d42f85a4b61a1fa149476c59a5bb39bc024df09`
- Repository pushed timestamp: 2024-02-27T21:55:35Z (not proof of collector maintenance).
- Verdict: **Excluded: provider wrapper**.
- Findings: Notebook using The Odds API, originally March 2022. Not a new data collector. No license detected.

### dos-2/oddshub

- Repository: https://github.com/dos-2/oddshub
- Reviewed default-branch snapshot: `7dc69a453c72c615210e47b9055a0780b7c10555`
- Repository pushed timestamp: 2025-09-16T03:10:53Z (not proof of collector maintenance).
- Verdict: **Excluded: provider wrapper**.
- Findings: Apache-2.0 Go terminal interface using The Odds API. UI reference, no independent sportsbook feed.

### l-portet/surebet-finder

- Repository: https://github.com/l-portet/surebet-finder
- Reviewed default-branch snapshot: `4909361b0abc47a10d2f1985a9c1e250e32154a0`
- Repository pushed timestamp: 2024-10-04T11:58:11Z (not proof of collector maintenance).
- Verdict: **Excluded: another aggregator API**.
- Findings: JavaScript surebet finder requiring oddsapi.io API_KEY. Does not solve direct data access. No license detected.

### ratsam3474/autoarbitrage

- Repository: https://github.com/ratsam3474/autoarbitrage
- Reviewed default-branch snapshot: `4800d952861a825e476dc306029ae51999c3c03e`
- Repository pushed timestamp: 2025-07-05T22:01:06Z (not proof of collector maintenance).
- Verdict: **Excluded as data foundation**.
- Findings: Documentation says opportunities are scraped from breaking-bet.com; browser modules place wagers on several mostly non-North-American books. This is downstream of another arb service, not an independent full sportsbook market collector. No license detected; not executed or given credentials.

### nickth3man/odds-scraper

- Repository: https://github.com/nickth3man/odds-scraper
- Reviewed default-branch snapshot: `aa28473103c3ff75f21fe0f6902ec9aa723f4cef`
- Repository pushed timestamp: 2026-08-04T20:29:29Z (not proof of collector maintenance).
- Verdict: **Narrow reference only**.
- Findings: Python NBA tool with ESPN JSON/DraftKings collection, UI/tests and sample data. README lists BetMGM/PointsBet as future work. MIT declaration in package metadata; no standalone license detected. Not broad sportsbook coverage.

## Next experiment before choosing the stack

1. Start with two or three relevant book feeds, not an all-books promise. Research feeds may be broader than books available to a particular user.
2. For each connector, record discovery success, event count, market count, props, source update timestamps, observed timestamps, suspended outcomes and jurisdiction.
3. Use low-frequency bounded samples permitted by source terms. Treat access-denied responses as unsupported until authorized access exists.
4. Compare the exact same market against the corresponding sportsbook display; distinguish fetched-at time from source-price update time.
5. Save raw snapshots and test matching/calculations with replay. Do not mistake independent opening/closing archive columns for prices simultaneously offered.
6. Score sustained reliability and actual matching across the relevant books before committing to a production data plan.

## Stack implication

Research shifts the likely collection layer toward Python because oddswrap, OddsHarvester, and most useful direct parsers are Python. A TypeScript dashboard remains viable, with Python ingestion producing a shared normalized schema. This is a recommendation, not a finalized architecture.

## Cost and reuse

Source code and a small local experiment can cost $0 incrementally. This does not establish free continuous global data or free hosted browser automation. Bookmaker terms/data permissions and dependency licensing must be checked before integration or redistribution. Several repositories have no detected license; treat them as research references until permission is established.

## Bet365 and Quebec gaps

No reviewed Bet365 repository established a current, complete, reliable market feed. Direct Canadian/Quebec-specific searches did not produce a suitable Mise-o-jeu+/SportsInteraction/BET99 foundation in this search. Absence from these results is not proof that none exists. US NJ or South African feeds cannot establish Quebec execution availability.
