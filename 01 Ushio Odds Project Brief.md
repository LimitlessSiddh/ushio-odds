# Ushio Odds Project Brief

Version 1.0 • 26 October 2026 • Owner Siddh Patel • Planning baseline

## What we are building

We are building a personal research platform that compares equivalent sports betting markets across supported sportsbooks, identifies theoretical arbitrage, and calculates the stakes and resulting profit for every outcome. Its first job is to make the data and arithmetic trustworthy and reviewable.

The product combines an opportunity scanner, a hedge calculator, and a journal that records how opportunities change. It is a separate project from PickPocket. The system is planned; software implementation and profitable live operation have not been established.

## Why this project matters

For personal use, it replaces repetitive comparison and calculation with a consistent workflow. For a computer science portfolio, it demonstrates data integration, precise calculations, database design, recovery from failures, and reproducible evaluation.

## Mission and longer term vision

Our mission is to find and explain market discrepancies with enough evidence to assess whether they can be acted on. Supported automated execution is a later research direction. We will first observe the manual workflow, measure failures and settlement outcomes, and determine which operators permit programmatic execution.

## What success means

 - A correct calculator and clear per-outcome profit display.

 - A scanner that distinguishes valid comparable prices from stale, suspended, or mismatched inputs.

 - A repeatable demonstration and documented measurements that can support honest resume claims.

# First release and user experience

## Initial scope

Begin with one sport and one game market while validating sources. Expand the pilot toward pregame NHL and NBA moneylines, spreads, and totals across three to five verified books in one defined jurisdiction. Book count is conditional on measured access and coverage.

## Core workflow

1. Choose supported books, sport, market, budget, and data mode.

1. Review prices alongside exact line, period, overtime rules, status, and source age.

1. Open a candidate and inspect its selected quotes and matching evidence.

1. Calculate stakes using a total budget or an existing first-leg stake.

1. Review every outcome and save the opportunity to the journal.

## Labels that keep results understandable

Synthetic and recorded data are labelled separately from live observations. Indicative means the calculation is based on observed prices. Revalidated means the selected prices were checked again through a supported mechanism. Neither label means a wager was accepted or a profit was earned.

## Outside the first release

Player props, alternate lines, live betting, public customer accounts, payments, public alerts, and automatic bet placement are outside the pilot. The user’s original player-prop example remains a calculator test case; it does not require a live prop feed in the first release.

## Location and coverage

A feed containing Ontario or other regional sportsbook prices does not establish that the user can place those bets from Quebec. Track feed jurisdiction, data-use permission, and personal betting eligibility separately. The product must not suggest that adding a location filter creates access.

# Delivery and decision boundaries

## Milestones

| Milestone | Evidence required |
| --- | --- |
| Source experiment | Named books, market coverage, timestamps, access terms, costs and recovery behaviour |
| Comparison and calculator | Correct stakes, reliable market identity and deterministic replay |
| Opportunity evaluation | Revalidation survival, lifetime, mismatch rates and simulated execution results |
| Expansion | Repeat the evidence checks for each new market or book |

## Budget

Aim for $0 incremental development cost on the existing computer using open-source tools and generated or permitted recorded data. Continuous relevant live data, an always-on host, and commercial distribution are not established as free. No paid vendor or infrastructure has been selected or purchased.

## Decisions that need Siddh

 - Whether to pay for a source after seeing measured coverage, freshness, terms and a concrete price.

 - Whether to move beyond local research into real-money manual testing or a public product.

 - Whether to investigate supported automated execution after the evidence gate passes.

## Risks and response

The largest risk is insufficient relevant data. We will test the feed before promising coverage. Other material risks are incorrect market matching, old prices, unavailable stake limits, and incompatible settlement. The system rejects uncertain inputs and retains reasons and evidence.

## Portfolio evidence

Publish only permitted datasets and measured results: connector coverage, replay reproducibility, rejected mismatches, recovery tests and calculation correctness. Describe simulated results as simulated. A profitable streak is not evidence of a reliable unattended strategy.
