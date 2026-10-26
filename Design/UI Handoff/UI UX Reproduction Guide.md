# Ushio Odds UI UX Reproduction Guide

Approved reference handoff — 26 October 2026.

## Objective and authority

Build the app to visually and behaviourally reproduce the approved local prototype. Siddh approved the final interface, Ushio teal palette, compact bottom-right calculator, full-width odds grid, performance page and official-logo revision. This is an implementation handoff, not a new design exercise.

Use this order of authority:

1. `../Prototype/index.html` with its sibling `assets/` directory: authoritative rendering and interaction reference. Read the entire CSS cascade, including late overrides.
2. `../Prototype/Previews/`: approved screenshots at 1280 × 720, documenting particular sample states.
3. `../Ushio Odds Colour Palette.html` and `.md`: approved branding, theme roles and light-mode yellow caution treatment.
4. This guide and `Acceptance Checklist.md`: reproduction requirements and interpretation.
5. `../../02 Ushio Odds Technical Blueprint.md`: application architecture, financial precision, data contracts and source validation.

The Accent Options files are rejected explorations, not the brand authority. Unjuiced and PTO inspired earlier research; do not substitute their current interfaces for the approved Ushio prototype. Preserve existing reference files while building in a separate implementation directory or repository.

## Run the reference

No build step or dependency installation is required. Open `../Prototype/index.html` in a browser, retaining its assets folder, or serve the Design directory:

```sh
python3 -m http.server 8767 --bind 127.0.0.1 --directory "/Users/siddhpatel/Desktop/Ushio Odds/Design"
```

If that port is occupied, use another local port. Do not start a duplicate server. Visit `/Prototype/index.html#grid` and `/Prototype/index.html#performance`. Other prototype hashes are `#arb`, `#watch`, and `#journal`. The localhost link itself is not the deliverable; the saved files and assets are.

## Stack and suggested decomposition

Retain the existing technical baseline: React, TypeScript and Vite for the frontend; FastAPI/Pydantic transport; shared Python Decimal financial/domain logic; PostgreSQL persistence with the planned worker and source adapters. Resolve current stable compatible package versions during repository bootstrap and pin them. This handoff does not select a new framework, live-data vendor or paid service.

Suggested components: AppShell, NavigationRail, WorkspaceHeader, ThemeToggle, OddsFilters, BookPicker, OddsComparisonTable, PairedOutcomeRow, OddsCell, ArbitrageTable, FloatingHedgeCalculator, CalculatorLeg, OutcomeDetails, Watchlist, SavedCalculations, PerformanceDashboard, ProfitChart, PairHistoryTable, RecordPairDialog and Logo components.

Start with typed synthetic fixtures behind a data adapter so visual parity is independent of live-feed availability. Extract prototype structure and styles into maintainable components. Do not simply ship the monolithic HTML as the production app, and do not redesign it during extraction.

## Global appearance

Use the approved semantic colour tokens; an export from the actual prototype is included as `approved-theme-tokens.json`. Both light and dark themes are required. Dark is the initial default; respect a saved user preference. Backgrounds, navigation and tables are neutral. Teal identifies actions and selected/theoretical hedge prices. Green indicates positive calculated or recorded profit. A plus-sign American quote is not automatically green and a minus-sign quote is not automatically red.

Light caution uses yellow `#EAB308`, pale yellow `#FEF3C7`, dark readable text `#713F12`, and the contrasting warning border. Do not use bright yellow small text on white. Dark warning text is `#FCD34D`. Retain symbols/labels alongside state colours. Keep visible keyboard focus rings. Use the system sans-serif stack and tabular/monospaced odds and money typography shown in the reference. No decorative gradients, glass, oversized marketing cards or extra accent colours.

Match density, text sizes, spacing, borders, rounding and alignment from the actual page. System-font rendering can differ slightly across operating systems; establish visual comparisons on the same environment.

## Layout and responsive behaviour

The main odds table uses the full available workspace width. Do not reserve a full-height right sidebar for the calculator. At the 1280 × 720 reference size the navigation rail is collapsed to icons. It expands at larger widths according to the reference CSS. Relevant breakpoints are 760, 1000, 1050, 1450 and 1700 pixels; the exact component rules are in the source.

The calculator floats in the bottom-right corner, about 388px wide on desktop. Its default compact height is roughly 270–290px depending on logo/text rendering; source styles and screenshots govern. Both legs sit side by side. Budget/mode controls share a row. Minimum profit and save action remain immediately visible. Secondary outcome rows and assumptions are disclosed on demand. A minimize button reduces the panel to a short header, revealing covered prices. Selecting a quote expands it again. Retain the bottom/right offsets and viewport-aware maximum sizing. On narrow screens, use the reference's constrained floating width and horizontally scrollable table. Desktop is the primary approved layout; verify narrow-screen behaviour rather than treating it as fully validated production mobile UX.

## Odds screen

- Pair both outcomes within each matchup row group, aligned horizontally against each book.
- Keep matchup labels pinned on horizontal scroll and column headers pinned on vertical scroll.
- Include time, best price and average-price columns, followed by ten illustrative sportsbook columns. Production columns must reflect actual supported source coverage.
- Include NBA/NHL, moneyline/spread/total, date, book visibility, American/decimal format, density and team search controls.
- Preserve horizontal/vertical scroll position when selecting a price. Previous/next-book arrows pan horizontally. Shift plus wheel/native trackpad scrolling remains available.
- Use teal outlined, tinted pills for the two prices forming a positive theoretical hedge pair, matching the final reference. Do not give every quote a coloured background. Selection of a non-arbitrage price must remain visually distinguishable from an actual hedge candidate.
- Clicking a quote populates that outcome and the best opposing quote from a different visible book, under supported matching rules. Never silently compare different lines, periods, overtime policies or regions.
- Total and spread rows must expose the exact threshold/side. Disabled props/futures reflect later scope; do not imply live support.
- Replay update is a synthetic demonstration control. Replace it with real feed-state behaviour only when the backend contract exists. Do not market sample prices as live.

## Calculator and state

Support total-budget allocation, fixed first stake, editable American odds, CAD stakes, per-outcome profit, worst-outcome profit, ROI and saving a scenario. Calculator odds remain labelled American even when the table display is decimal. The prototype accepts conventional American odds with absolute magnitude at least 100; document production validation deliberately.

Keep selected snapshots stable while the table changes. The prototype warns when replay affects the selected snapshot. Production must use quote IDs, source timestamps and proper invalidation/revalidation from the technical blueprint. Manual edits remain user supplied and cannot become verified live prices.

Reference arithmetic after conservative cent payout rounding:

| Inputs | Expected outcome |
|---|---|
| CAD250 total, -110 / +115 | CAD132.42 and CAD117.58 stakes; at least CAD2.79 minimum net profit |
| Fixed CAD1000 at -110, opposing +115 | CAD887.95 second stake; approximately CAD21.14 net in either outcome |
| -110 / -110 | Negative result and caution, not a positive-arbitrage claim |
| Zero/invalid odds | Clear invalid output, visible error and saving disabled |

Production must use the shared Decimal domain engine, integer currency increments, supported fees, limits and settlement rules. Browser Number arithmetic is a prototype convenience, not the production financial authority. Preserve the UI while replacing that implementation.

## Other working views

Arbitrage: rank complete supported pairs by theoretical ROI; inspect a pair in the compact calculator. Preserve the distinction between unrounded theoretical rankings and rounded outcome results. Watchlist: star/unstar a game and show the selected games with the same comparison layout. Saved calculations: save and reload calculation scenarios. These are not bets and must never automatically enter realised performance.

Search focuses with slash or Cmd/Ctrl K. Escape dismisses popovers/dialogs. Preserve keyboard reachability, input labels, modal focus handling, reduced-motion support, table semantics and descriptive control names.

## Performance and pair ledger

The approved Performance page extends the earlier planning documents with a prototype of a manually recorded pair ledger. Keep it separate from quote calculations, feed observations and actual sportsbook account sync.

Show cumulative net profit, realised net profit, ROI on settled stake, settled turnover, completed pairs, open stake, average net per settled pair, recorded fees and positive/negative/voided pair counts. Count complete pairs, not individual-leg wins. Include 7-day, 30-day and all-time controls. The chart resets to zero at the beginning of the selected period and includes negative results. Date ranges affect summary metrics and chart; status/search filters affect the history table only.

Pair history contains date, event/market, both books, status, total stake, combined returned amount, net profit, ROI and expandable details. Return includes any winning stake returned. Net profit equals returned amount minus all pair stakes minus fees. Open records do not contribute realised profit. ROI excludes open and voided stake. Refunded principal is not winnings. Deposits and withdrawals are not profit. Do not invent bankroll return, cash balances or verified sportsbook results.

The demo form records local pair totals with settled/open/voided states. Production requires durable records, explicit source, settlement provenance and auditable corrections; the simple prototype is not a full accounting ledger. Design those data requirements without silently changing the approved page.

## Assets and logos

Copy the entire prototype assets folder. `assets/logos/manifest.json` records team, league and sportsbook file mappings and source URLs; its README documents preparation. Team aliases are NYK→NY, GSW→GS, NJD→NJ and TBL→TB. Preserve logos' colours and aspect ratios. Existing SVG wrappers remove blank canvas only; originals remain included. Use the light backing plates where shown for readable brand artwork in both themes. Do not substitute guessed logos, initials or recoloured approximations. Unknown manual matchups retain text rather than guessed branding. The Ushio wave remains provisional brand artwork used in the approved prototype.

## Visual state and screenshots

Use 1280 × 720 as the initial comparison viewport, then verify wider desktop and narrow layouts. All six previews are included. The Performance screenshot includes a manual QA example in addition to the synthetic seed ledger: a fresh browser therefore differs. `visual-review-state.json` records the exact additional sample entry and expected metrics. Use only in a demo/test fixture. Saved footer count and watchlist stars can also depend on local browser state.

Compare the implementation with the reference in matching theme, viewport, data, filters, scroll, selected quote, calculator mode and expanded/minimized state. Capture matching screenshots. Review alignment and interaction fidelity; passing a build alone is not acceptance. Do not silently regenerate the reference images to make a changed implementation look approved.

## Build sequence and finish line

1. Inspect the implementation repository and its instructions; read the project blueprint and this reference.
2. Build the shell, tokens, assets and synthetic fixtures. Confirm static parity in both themes.
3. Implement the grid, filters, scroll preservation and compact calculator interactions.
4. Implement arbitrage/watchlist/saved views, then Performance and its separate record model.
5. Integrate the Decimal calculation/API boundaries and real source states only where contracts exist. Keep a clearly labelled fixture mode when data access is unresolved.
6. Run meaningful interaction/domain tests and screenshot comparisons using the acceptance checklist.
7. Report implemented features, screenshots, test results, remaining data/integration gaps and any intentional deviations.

No live data vendor, public deployment, paid service, sportsbook account action or automatic wagering is authorised by this UI handoff. Source access remains an independent engineering decision. UI approval is approval of the interface, not evidence of profitable operation.
