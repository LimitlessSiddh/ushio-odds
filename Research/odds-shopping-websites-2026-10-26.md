# Free odds-shopping websites — 26 October 2026

## Decision
Keep data vendor selection open. Free consumer odds screens can support personal line shopping, but none examined establishes a free, reusable automated feed for this project. Do not implement connectors against these sites based on public visibility alone.

## PickTheOdds
https://picktheodds.app/en/arbitrages
Direct logged-out browser observation: arbitrage results limited to 10 and maximum 2% ROI; player-prop examples visible. Separate NBA odds screen displayed multiple sportsbook columns and a banner specifying a 60-second refresh for logged-out visitors. Book catalogue size does not establish coverage for a particular market or region. Actual bookmaker prices were not checked.
https://picktheodds.app/en/terms-of-service
Rendered terms expressly restrict automated collection, competitive analysis and building a competing product without authorization. Not recommended as a project data backend without authorization.

## Alternatives
- 4C Odds: https://4codds.com/ . Public browser showed a book-by-book screen and CSV export control; export contents were not tested. FAQ https://4codds.com/faq says screen is free, with sign-in for automatic updates. Terms https://4codds.com/terms.html specify signed-out delay around 30 seconds plus manual refresh, personal noncommercial browser use, no automated extraction or incorporation of data into another application. CSV visibility does not override these restrictions. Terms say intended for US users despite UI showing Quebec/offshore filtering. Do not assume regional availability means authorization to wager.
- Unjuiced: https://unjuiced.bet/features/odds-screen advertises a free odds screen with 20+ sportsbooks, game lines, player props and alternate lines, live/pregame and automatic refresh. App odds URL redirected to login; authenticated coverage and latency not validated. No reusable feed or data rights established.
- Betstamp: https://www.betstamp.com/tracking advertises free comparison across 50+ sportsbooks and prediction markets. PRO prop grid is a separate paid product. No claim that all catalogued books serve Quebec, or that API access is free.
- Betwatch: https://betwatch.io/ advertises a free account for its Live Board, full +EV board and movement tools; 44 mixed sources includes 29 sportsbooks, 9 prediction/exchange sources and 6 pick-em apps. Claims props, alternates and period lines. These are vendor claims; authenticated screen, latency and source-specific coverage not tested. +EV is not equivalent to arbitrage.

## Proposed next step
For personal shopping, try Unjuiced and Betstamp against relevant books and exact matching markets; 4C is another screen subject to its eligibility and terms. For our platform, build source-independent fixtures, market matching and Decimal stake calculation now. Evaluate a permitted feed/export separately by exact region, market depth, source timestamp, suspension status, access rights and cost. A consumer subscription does not automatically include API or reuse rights.

Arbitrage detection needs prices for all mutually exclusive, exhaustive outcomes under matching settlement rules. A two-outcome decimal market has a mathematical arb when 1/d1 + 1/d2 < 1, before fees and execution constraints. Three-way markets require all three outcomes. Price visibility alone does not prove executable profit.
