---
name: ak-design
description: AK Crackers's own design system and UX rules for the Angular web app (apps/web) and the React Native mobile app. Use whenever building, restyling or reviewing any AK Crackers screen, page or component, on web or mobile, so both apps look and behave as one brand. Use together with taste-skill (web art direction), react-native-skills (mobile engineering) and web-design-guidelines (audits).
---

# AK Crackers design

The source of truth is `apps/web/src/styles.css` (tokens). If a token changes, change it there first, then mirror
it in `apps/mobile/src/ui/theme.ts`.

## Idea
"Diwali night": the shop is the sky on Diwali night. A deep night-violet ground with soft gold and red glows like
fireworks, gold light for type and actions, and warm cream panels where products and forms sit. Category pictures
(`backend/data/art/`) show the cracker against the same sky. Festive, warm and easy to read, never noisy.

## Tokens (same values on both platforms)
| Token | Value | Use |
|---|---|---|
| bg | `#1c0a2e` | night-violet ground (web adds gold/red/violet radial glows) |
| bg-deep | `#12061f` | phone tab bar |
| surface / surface-soft | `#2c1546` / `#3d1f5e` | one step off the sky; back tabs |
| ink / accent (mobile: gold) | `#ffc93c` | gold: type on the sky, and the action colour |
| accent-ink | `#1c0a2e` | text on gold |
| muted (mobile: skyMuted) | `#e9cfa3` | soft type on the sky |
| red | `#e8432e` | cracker red: "% off", badges, chart highlight |
| paper / paper-ink / paper-muted | `#fff8ec` / `#2a1230` / `#6e5a68` | the cream field |
| paper-step | `#f5e9d4` | one step off cream |
| ink-soft | `#cdbfe0` | soft light type on the dark tab bar |

On mobile `color.ink` is the dark plum text on panels; anything on the sky uses `color.gold` / `color.skyMuted`
(the `sky` prop on `Title` and `Body`).

- **Font:** Baloo 2, weights 400–800. Headings 700–800, letter-spacing -0.01em, line-height ~1.0.
  Prices and order numbers use tabular numbers.
- **Type steps:** small 13–14, body 17–19, lead 20–26, title 28–40, head 32–64, display 72–160 (px).
- **Space:** side margin 16–32 (mobile 16), gutter 16–28.
- **Corners:** panels 18px, inputs 10px, buttons and chips are pills. Trapezoid tabs keep their slanted shape.
- **Motion:** ease `cubic-bezier(0.22, 1, 0.36, 1)`; hover/press 160ms. Respect reduced motion.

## Components
- **Button:** a gold pill with dark text and a soft gold glow, height ≥ 52. Secondary action = underlined text link.
- **Tabs:** trapezoid tabs on the sky; the current tab is cream with dark text.
- **Stamp:** a small gold block, slightly rotated (-2°), for "% off", order numbers and status.
- **Status steps:** confirmed → packed → shipped → delivered, shown as a row of ticks.
- **Focus:** 3px gold outline, 3px offset.

## UX rules (both apps)
- Money is shown as `₹1,299` or `₹19.80` (paise shown as two digits), with Indian digit grouping (`en-IN`).
  Show the MRP crossed out next to the offer price, and the "% off".
- Every product shows its price-list code; buyers and the shop quote crackers by code.
- Read delivery fees and limits from `/api/v1/shop/`; never hard-code them.
- Payment: cash on delivery or UPI QR. Say plainly that a person checks UPI payments.
- Every screen has loading, empty and error states: short, plain and human.
- Touch targets ≥ 44×44 (iOS) / 48×48 (Android). Gold on night-violet and plum on cream both pass 4.5:1 easily;
  never put light text on gold or gold text on cream.

## Workflow
1. Web page or screen → build inside these tokens; screenshot it and look.
2. Mobile screen → build to this skill + react-native-skills; screenshot on the emulator and compare with the web page.
3. Before calling UI done → run web-design-guidelines on the changed web files, and check the UX rules above.
