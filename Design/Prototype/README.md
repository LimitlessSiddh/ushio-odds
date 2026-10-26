# Ushio Odds Interactive Prototype

First desktop prototype, 26 October 2026. Open `index.html` directly in a browser, or serve the Design folder and open `/Prototype/index.html`. This is a locally self-contained interface mockup (keep its assets folder beside index.html) with synthetic events and prices, not the React application or a live odds service.

## Screens and interactions

- Odds screen: paired outcome rows; pinned matchup column and headers; best price, average decimal price converted to the selected display format, and ten illustrative book columns.
- Filters: NBA/NHL, moneyline/spread/total, event day, team search, book visibility, American/decimal prices, and comfortable/compact row density.
- Selecting an outcome uses that quote and the best opposing quote from a different visible book. The calculator holds a snapshot; filtering or replay does not assert revalidation.
- Calculator: total budget or fixed first stake; editable American odds; cent-rounded allocation and conservatively rounded per-outcome payouts; minimum profit and ROI; invalid-input and non-profitable-result feedback.
- Arbitrage: synthetic two-way pairs ranked by theoretical unrounded ROI. The calculator shows rounded outcome profits for the selected pair.
- Watchlist and saved calculations persist in browser local storage. Theme preference persists too. A saved calculation is not a recorded wager.
- Manual calculator: explicitly user supplied; no source-verification claim.
- Replay update: deterministic sample change, not a network refresh. Affected selected snapshots show a warning until a new quote is selected.
- Keyboard: slash or Cmd/Ctrl K focuses search; Escape dismisses the book menu or prototype guide.
- Narrow-screen fallback: the table scrolls horizontally and the calculator remains a compact floating corner panel. Desktop is the primary design and validation target.

## Visual decisions

Uses the approved Ushio teal tokens from the colour palette. Black/white/grey surfaces carry most of the interface. Teal identifies selection and actions; positive profit is green; caution has a clear yellow treatment in light mode. American odds signs do not determine semantic colour. A provisional vector wave is the only brand symbol; book, team and league logos now use locally saved original artwork (see assets/logos/README.md).

The calculator now floats in the bottom-right corner, with both legs side by side, instead of reserving a full-height right column. Its default height is approximately 271px at the reviewed 1280 by 720 viewport, versus roughly 614px before this revision. A minimize button reduces it to a 41px header, revealing covered cells. Selecting a table quote expands it again. Outcome details and assumptions are available through a disclosure button. The comparison table fills the workspace, keeps the matchup column pinned, and offers previous/next-book arrows plus native horizontal scrolling. Selecting a quote preserves the table scroll position. Positive theoretical hedge pairs receive teal outlined, softly tinted price pills matching the supplied reference; non-hedge best prices remain plain. Additional illustrative books were added to make horizontal navigation testable, without establishing actual feed coverage.

Unjuiced's published comparison screenshot and PTO's public grid informed paired rows, aligned book columns, and best/average summaries. This is an original Ushio interface, not an authenticated reconstruction of Unjuiced.

## Scope boundaries

No sportsbook connection, authentication, feed access, wagering, verified settlement journal, or automatic execution. A separate sample/manual performance ledger is included. Book names and schedules are illustrative and do not establish regional availability. Props and futures are visibly disabled as later scope. No paid service or dependency was added.

Calculations use browser floating-point arithmetic for interaction review only. The production blueprint still requires shared Python Decimal logic, real source timestamps, quote identity, expiry/revalidation, exact settlement matching, fees and constraints. The prototype assumes supported exact two-outcome markets, CAD, no fees, matching settlement and acceptance of both legs. It does not model one-sided voids, bookmaker limits or FX. Its validation accepts conventional American odds with magnitude at least 100 and positive amounts up to CAD10M.

## Browser verification

Reviewed dark and light layouts at 1280 by 720. Tested:

- CAD250 allocation at -110/+115: CAD132.42 and CAD117.58; minimum conservative profit CAD2.79.
- Fixed CAD1000 at -110 against +115: opposing CAD887.95; minimum conservative profit CAD21.14.
- -110/-110 produces a negative-result warning.
- Invalid zero odds clears output and disables saving.
- Saved calculation appears and can be loaded.
- NHL totals search filters to the Montreal matchup.
- Book visibility updates its count; watchlist stores a starred game.
- Replay invalidation warning persists while editing budget.
- Both themes and the arbitrage screen render successfully.

The browser used for QA contains one demonstration saved scenario and one starred game. These remain local to that browser; a different browser starts fresh.

## Preview images

- `Previews/01 Odds Screen Light.png`
- `Previews/02 Odds Screen Dark.png`
- `Previews/03 Arbitrage Dark.png`

## Next design review

The user approved this UI as the implementation reference on 26 October 2026. Preserve the approved table density, compact floating calculator, theme and logo revision. Live timestamp/region details and feed-failure states still require production contracts. See ../UI Handoff/UI UX Reproduction Guide.md for the coding-agent handoff.

## Compact calculator revision verification

- Reviewed light/dark layouts and updated all preview images.
- Confirmed approximately 271px calculator height and 1176px full-width table at 1280 by 720.
- Horizontal navigation moved the table by 221px to its boundary; selecting a revealed BetRivers quote preserved that position and loaded the selected quote.
- Calculator minimizes to a 41px header and reopens on selection.
- Expanded details show both outcome profits; fixed-stake reference math remains unchanged.
- Floating panels intentionally overlay underlying rows. Minimize the calculator when accessing covered prices.

## Performance page

Open `index.html#performance`, or select Performance in the left navigation.

- Cumulative net-profit chart with 7-day, 30-day and all-time ranges. The series resets to zero for the selected period.
- Realised net profit, ROI on settled turnover, completed-pair record, open stake, average net per settled pair and recorded fees.
- Pair history with book names, total stake, combined returned amount, net profit, ROI, settlement status and expandable calculation details.
- Date-range controls affect chart and summary metrics. Status and search controls filter history only.
- A manual demo-pair form accepts pair totals and persists entries separately from saved calculator scenarios in browser storage.
- ROI = realised net profit / settled stake. Open stakes and voided/refunded stake are excluded from the denominator; refunds do not count as winnings. Profit = combined returned amount minus both stakes minus recorded fees. Returned amounts include returned winning stakes.
- Counts refer to whole pairs, not individual-leg wins. No account-balance, bankroll-return or sportsbook-sync claim is made.
- The seed ledger is synthetic: CAD57 net profit, CAD3,720 settled turnover, 12 settled pairs, 1 voided pair and CAD550 across 2 open pairs. The QA browser also contains one clearly named Demo tracking example: CAD100 stake, CAD102 returned, CAD0.25 fees, CAD1.75 net. With that entry the page shows CAD58.75 net and 1.54% ROI on CAD3,820 turnover.
- Browser checked range filtering, open-history exclusions, demo-entry save and expanded fee arithmetic. Both theme previews are saved.

## Official logo revision

Replaced placeholder team initials and book abbreviations with local original artwork. Added NBA/NHL marks to the league selector and heading; matching team/book marks to calculator, arbitrage, watchlist, saved identifiable scenarios and performance history. All displayed NBA/NHL images were checked for completed loads and nonzero natural size, with both theme previews refreshed. Provenance and display preparation are documented in assets/logos/README.md and manifest.json.
