# Requirement-to-evidence matrix

| Requirement | Implemented evidence | Current limitation |
| --- | --- | --- |
| Exact money calculations | `services/api/app/domain.py`, seven API/domain tests | Fees and book limits are not yet modelled per source |
| Source distinction | Fixture mode and provider status responses | No permitted key supplied |
| Odds comparison | Real API-backed paired odds grid | Fixture has NHL/NBA moneylines only |
| Watchlist / saved scenarios | Browser-persisted UI flows; server persistence endpoints prepared | UI save sync to server is the next integration slice |
| Performance ledger | Separate UI records plus `/v1/ledger` server contract | Browser UI still uses local records pending server sync |
| Quebec boundary | Explicit labels and documentation | Provider entitlement/eligibility unverified |
| UI fidelity | approved palette/density, dark/light mode, compact calculator, responsive grid | Formal screenshot-diff suite still pending |
| CI and reproducibility | Docker compose, pinned dependencies, GitHub workflow | Hosted run requires push/remote access |
