# Bounded NHL moneyline provider observation

Date: 2026-10-29

## Scope

One explicit, on-demand The Odds API request was made for `icehockey_nhl` / `h2h` with region `ca`. No sportsbook was accessed. There was no polling, wagering, account action, or provider-plan change.

## Observed facts

- The upstream request returned successfully before local persistence, with 287 credits remaining.
- The bounded response had 11 raw events, 48 raw bookmaker entries, and 96 supplied source timestamps.
- Normalization yielded zero normalized events and zero complete selected-book markets, so the response is `observed-empty`.
- A durable local evidence row (`ed8562fa-997b-4214-8d41-f4851a76c84b`) was written to the migrated observation database with the recovered facts above.

## Evidence caveat

The first local evidence write failed after the upstream response because the ad-hoc SQLite target had not yet been migrated. The raw response was intentionally not retained, so its provider-title list, market-key list, and detailed rejection counts cannot be recovered without another request. No second request was made: this preserves the one-scan scope. The durable row is explicitly marked `partial-after-local-migration-error`.

## Inferences

The zero result is consistent with current selected-book coverage/mapping producing no complete two-leg pair for this NHL moneyline request. It is not evidence that the provider is broken, that no Canadian odds exist, or that any book/account is available in Quebec.

## Unknowns and next decision

Unknown: the exact returned titles, title-to-canonical mapping results, individual market identity/settlement semantics, source status, limits, fees, FX, display rights, account availability, Quebec eligibility, and revalidation status. Do not change the canonical book map from this partial record. The next external decision is whether the provider’s permitted scope supports one future, pre-approved observation with a migrated runtime so the full non-secret coverage summary can be retained.
