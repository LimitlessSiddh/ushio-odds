# Ushio Odds Colour Palette

Approved brand direction, 26 October 2026. Ushio teal was selected by Siddh after reviewing the alternatives. This palette precedes UI mockups; it does not change the technical scope or establish live data access.

The identity uses ocean teal against neutral black and white surfaces. It connects to Ushio's tide inspiration while keeping a dense odds table readable. Use semantic tokens rather than hardcoded component colours. Both themes are first-class; the user's preferred default remains open.

| Token | Light | Dark | Purpose |
|---|---|---|---|
| canvas | #FAFAFA | #111111 | App background |
| surface | #FFFFFF | #191919 | Table, calculator and navigation surfaces |
| surface-raised | #F5F5F5 | #242424 | Hover, filter fields and grouped controls |
| border-subtle | #E5E5E5 | #363636 | Decorative dividers; not sufficient alone for essential control boundaries |
| text-primary | #171717 | #FAFAFA | Main text and odds |
| text-secondary | #525252 | #A3A3A3 | Metadata and secondary labels |
| accent | #0F766E | #5EEAD4 | Main actions, selected odds, active controls, keyboard focus |
| on-accent | #FFFFFF | #111111 | Text on solid accent buttons |
| positive | #15803D | #86EFAC | Positive calculated profit |
| caution-signal | #EAB308 | #FCD34D | Yellow status stripe or icon; not small text on white |
| caution-background | #FEF3C7 | #191919 | Warning surface |
| caution-text | #713F12 | #FCD34D | Readable warning labels |
| caution-border | #A16207 | #363636 | Warning boundary; dark theme also uses yellow signal and label |
| negative | #B91C1C | #FCA5A5 | Errors, invalidation and negative calculation outcomes |

## Usage

- Keep most of the screen neutral. Use teal sparingly to guide actions and selection.
- Use green for calculated positive returns, not every positive American odds number. A +115 quote is not itself a profit.
- Red does not mean a minus-sign American price is bad; reserve it for meaningful error/loss states.
- Selected prices use an outline and a text/shape indicator as well as colour. Pair status colours with readable labels or icons.
- Use the primary text colour or an appropriately contrasting control-border token for essential input boundaries; subtle dividers are decorative.
- A focus outline uses the theme accent, 2px with 2px offset. Check adjacent colours in the actual component.
- Tint backgrounds require separate contrast checks; do not assume a text colour passing on the main surface passes everywhere.
- No gradients, glow, or gold/casino decoration. No bright colour-filled market grid.
- Monochrome wordmark with an optional teal symbol. The wave shown on the palette board is provisional.
- System sans-serif for interface labels; tabular numerals for aligned odds, stakes and profit. The database's initial landing-page recommendations were rejected in favour of its financial/data-dense dashboard patterns and the user's references.

## Measured contrast

Ratios use WCAG relative luminance calculation, rounded to two decimals. These checks cover specified pairs, not full interface accessibility.

| Pair | Light | Dark |
|---|---|---|
| Accent and on-accent | 5.47:1 | 12.76:1 |
| Primary text on canvas | 17.18:1 | 18.09:1 |
| Secondary text on surface | 7.81:1 | 6.97:1 |
| Positive text on surface | 5.02:1 | 12.52:1 |
| Caution text on warning background | 7.79:1 | 12.19:1 |
| Negative text on surface | 6.47:1 | 9.26:1 |

## Confirmed UI decisions

- Desktop odds grid is the initial screen, inspired by Unjuiced's paired outcome rows and PTO's comparison grid.
- Calculator stays docked on the right while the table remains visible.
- Support light and dark themes with accent colour reserved for meaningful signals.
- Prototype uses labelled synthetic data, no wagering or live source claim.

## References inspected

- Unjuiced's published odds-screen screenshot and feature page: https://unjuiced.bet/features/odds-screen . Its app required login in this browser, so no claim of a full authenticated review is made.
- PTO's rendered public NBA board: https://picktheodds.app/en/odds-screen/NBA . Reviewed table structure, best/average columns, stacked outcomes and compact filters.

## Approved light-mode caution treatment

A visible yellow signal (#EAB308), pale yellow background (#FEF3C7), dark readable text (#713F12), and contrasting border (#A16207). Do not use bright yellow as small text on white. This keeps the warning visibly yellow while preserving legibility. The alternative palette study remains exploration only; the teal palette is the selected direction.
