# Requirement-to-evidence matrix

| Requirement | Implemented evidence | Current limitation |
| --- | --- | --- |
| Exact money calculations | `services/api/app/domain.py`, seven API/domain tests | Fees and book limits are not yet modelled per source |
| Source distinction | Fixture mode, provider status, and quote source/receipt timestamps with stale/suspended/missing state | No permitted key supplied; no revalidation implementation |
| Selected bookmaker universe | Fixture and provider normalisation use the owner's exact 11-book list; Ontario-only ToonieBet is disabled in pair selection and excluded from candidate detection | Source coverage and account eligibility remain unverified; TonyBet remains marked unresolved |
| Odds comparison | Local API-backed paired fixture grid; opportunities trace selected quote-version IDs and Decimal inputs | Fixture has NHL/NBA moneylines only; no live provider observation persistence |
| Quote lifecycle | Alembic revision `20261027_03`; deterministic lifecycle tests for duplicate/future/stale/out-of-order/suspended/mismatched inputs | Provider refresh remains deliberately non-persistent pending permitted capability scan |
| Watchlist / saved scenarios | Server-backed endpoints; UI loads/saves through local API; browser reload proof for a player-prop watchlist item | Saved-scenario restart assertion remains to add |
| Performance ledger | Separate UI plus `/v1/ledger` persistence contract | Corrections and per-leg audit trail remain incomplete |
| Quebec boundary | Explicit labels and documentation | Provider entitlement/eligibility unverified |
| UI fidelity | approved palette/density, dark/light mode, compact calculator, responsive grid | Formal screenshot-diff suite still pending |
| CI and reproducibility | Docker compose, Alembic revisions, pinned dependencies, GitHub workflow | Hosted run requires push/remote access |
