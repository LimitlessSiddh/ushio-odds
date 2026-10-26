# Ushio Odds UI Acceptance Checklist

Use the approved HTML, assets and screenshots as the reference. Record evidence and any deviations; do not tick items based solely on reading the implementation.

## Visual fidelity

- [ ] Same reference viewport, theme and synthetic data state before comparing.
- [ ] Light/dark neutral surfaces, approved teal, green profit and yellow light caution.
- [ ] Matching typography, density, column alignment, borders and spacing.
- [ ] Full-width odds grid; pinned matchup and headers; usable native horizontal scrollbar.
- [ ] Compact bottom-right calculator; no reserved full-height right column.
- [ ] Side-by-side legs, visible result/action, working minimize and details disclosure.
- [ ] Teal outlined positive hedge pairs match the final reference.
- [ ] Correct original team, league and sportsbook logos with no broken assets or distortion.
- [ ] Responsive checks at 1280×720, a wider desktop, 1024px and a narrow mobile viewport.

## Interactions

- [ ] All nav views render and preserve intended theme/state.
- [ ] Sport, market, date, book visibility, format, density and search work.
- [ ] Quote selection uses a different opposing book and retains scroll position.
- [ ] Horizontal arrows, pinned cells and minimize permit access to covered/rightmost prices.
- [ ] Budget/fixed-stake modes, manual odds and invalid/error states work.
- [ ] Quote updates do not silently overwrite selected calculation inputs.
- [ ] Watchlist and saved scenarios work independently of recorded bets.
- [ ] Keyboard focus, shortcuts, Escape, input labels and dialog focus handling work.

## Calculation and performance correctness

- [ ] Production Decimal calculations match documented reference vectors.
- [ ] Cent rounding, unsupported fees/limits, missing outcomes and mismatched rules handled explicitly.
- [ ] Worst-outcome profit and ROI recomputed from actual rounded stakes.
- [ ] Performance seed: CAD57 net / CAD3,720 settled stake / 12 completed pairs / CAD550 open.
- [ ] Optional screenshot fixture: CAD58.75 net / CAD3,820 turnover / 1.54% displayed ROI.
- [ ] Open stake excluded from realised profit and ROI; void refunds not counted as winnings.
- [ ] Fees subtracted exactly once; returned amount includes returned winning stake.
- [ ] Range changes chart/metrics; history status/search changes table only.
- [ ] Record form saves and validates distinct books, amounts, dates and settlement state.
- [ ] Saved calculator scenarios never become settled performance without a separate record action.
- [ ] Unknown/manual sources, synthetic data and verified source records remain distinguishable.

## Engineering and delivery

- [ ] Approved reference preserved; implementation lives separately.
- [ ] Typed components, semantic tokens and shared domain/API contracts follow the technical blueprint.
- [ ] No hardcoded profitable demo outcomes presented as live results.
- [ ] No paid resources, production release or automatic wager implementation inferred from UI approval.
- [ ] Relevant tests pass; matching screenshots reviewed; limitations and deviations reported.
