# Ushio Odds prototype logo assets

Downloaded 26 October 2026 for the local design prototype. Original artwork is retained in this folder. Logos are not recoloured or redrawn. Nine sportsbook display SVGs wrap the original bitmap with a viewBox removing blank canvas, preserving the logo pixels and aspect ratio. Pinnacle uses the native 16px favicon at native size.

## Sources

- NBA/NHL team and league logo artwork: ESPN team/scoreboard API metadata and the referenced ESPN logo CDN. Exact source URLs, team names, and local files are recorded in manifest.json, NBA-sources.json and NHL-sources.json.
- Bet365, FanDuel, DraftKings, BetMGM, Caesars, BetRivers and Fanatics: logo images published on the Pennsylvania Gaming Control Board official operator directory: https://gamingcontrolboard.pa.gov/online-sports-wagering-licensed-operators . These are visual assets only; the PA directory does not establish Quebec eligibility or data coverage.
- Pinnacle, PointsBet and Betway: favicon/app-icon artwork linked by their official homepages. Exact asset URLs and homepage sources are recorded in manifest.json and sportsbook-sources.json.

## Coverage and handling

All teams appearing in the NBA/NHL sample fixtures resolve to local official-logo artwork. ESPN abbreviation differences are mapped explicitly: NYK to NY, GSW to GS, NJD to NJ, and TBL to TB. Local assets include the full 30-team NBA and 32-team NHL catalogues to avoid missing marks during further prototype work.

The grid, league selector, best-price summaries, calculator legs, arbitrage list, watchlist, book picker, saved scenarios with identifiable events, and performance history use the matching assets. Unknown manually typed matchups retain text; the interface does not guess a team logo.

The Ushio wave remains the provisional symbol previously approved as part of the local palette; navigation icons and the user's initials are interface elements, not third-party logos. Third-party marks remain owned by their respective organisations. Their inclusion does not establish endorsement or a redistribution licence for a public release.
