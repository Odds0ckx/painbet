# THE INTAKE (v11) — pain.bet restyle · handoff

_Deliverable: `painbet-intake-11-v2.html` (v2 of the uploaded `painbet_intake_11.html`).
One standalone file, no build step, opens straight off disk._

## What this is

A pure restyle of the uploaded intake app onto the pain.bet design system. Every
word of copy, every element ID, every handler, the synthesised audio engine and
both embedded base64 videos come through unchanged. The only things that moved
are the stylesheet, the webfont link, five brand motifs and two colour arrays
that happened to live in JS.

Nothing in the funnel logic was touched: the five-question exam and its scoring,
the diagnosis tiers, the PK locker roll and its weights, the wheel odds table,
the entry cap, the wallet and hash validation per chain, the credential issue and
login check, the Sunday countdown, the giveaway and task lists, the private ward,
the staff tracks. All of it is byte-identical to v11.

## What changed

**Palette.** Onto the real tokens from `index.html` / `painbet-arcade.html`:
`--bg:#232427`, `--card:#1b1d20`, `--card-2:#232529`, white-alpha ink ramp,
`--red:#E10600` / `--redhi:#FF3B33`, `--blue:#7FD6E8`, `--amber:#FFB84D`.

The brand rule from `index.html` decided the reassignments. Arterial red stays on
pain and action (CTAs, the diagnosis, the corruption meter, the exam progress).
Morphine blue took over everything to do with money, which retired the old gold
`#F2C14E` and mint `#5FE3A1`: prize pools, the $500 jackpot, PK amounts, entry
counts, payout confirmations, the paid-out feed. Amber is now reserved for the
private ward and the locker, so gold reads as tier rather than as cash. The PK
tag on the live site is already blue, which is what settled it.

**Shape.** No hard rules anywhere. Every 1px `#454A50` border became a hairline of
white (`inset 0 0 0 1px hsla(0,0%,100%,.07)`) over `--shadow` / `--shadow-lg`, on
the 16/12/8/pill radius scale. The old 3px left border bars became `inset 3px 0 0`
accent rails, the way the app sidebar marks its selected item. Buttons are pills,
Archivo 800, uppercase, with the red glow shadow off the live site. All transitions
moved onto `cubic-bezier(.22,1,.36,1)`.

**Type.** Archivo Black for display, Archivo (now including 800) for body and
controls, IBM Plex Mono replacing JetBrains Mono to match the arcade. Mono is
pulled back to where it earns its keep: hashes, countdowns, odds, IDs, amounts.

**Motifs added.** The wordmark triangle as a corner watermark on the hook, the
Sunday prize, the wheel, the VIP promise and the October card. The EKG trace from
the promo banners along the bottom of the cover hook. The liquid pain-scale bubble
from the app sidebar now sits on the diagnosis card, filling to the tier the exam
scored and labelled Numb / Sore / Chronic / Agony / Flatline.

**Atmosphere kept.** Grain, scanlines, vignette, the arc-flash on every state change
and the rust bloom that creeps in past 60% corruption are all still there, retuned
so the cards stay readable: scanlines .26 to .13 on a 4px period, grain .05 to .035,
rust .45 to .28 (in both the stylesheet and the inline set in `diagnose()`).

**Two JS colour arrays repointed**, because they were styling: the password meter
gradient and the hint colour token.

## Verified

Full Playwright pass at 420x900 and 1280x900 through every screen: intro, cover,
directory, exam, diagnosis, giveaway, entry logged, discharge, locker pried,
channels, dispensary with all five sections open and the odds table expanded, a
real wheel spin, the chart, the private ward, staff tracks, login. No console or
page errors. Zero horizontal overflow.

Screenshots in the session scratchpad, not committed. Fonts do not load in the
sandbox (no proxy for Chromium), so the shots show fallback faces; the real faces
resolve normally off the network.

## Files

- `painbet-intake-11-v2.html` — the deliverable.
- `scratch/intake-11-restyle/painbet-intake.css` — the stylesheet on its own.
- `scratch/intake-11-restyle/restyle.py` — regenerates the deliverable from the
  original upload plus the CSS. Every substitution asserts it hits exactly once,
  so if v11 is revised the script fails loudly rather than silently half-applying.
  It needs the original `painbet_intake_11.html`, which is not in the repo; point
  `SRC` at wherever it lives.
- `scratch/intake-11-restyle/screenshot-pass.js` — the Playwright walk.

## Open items

- Nobody has clicked through it on a real phone yet, only Chromium at phone size.
- The wheel and intro videos are still the base64 blobs from v11. If this page
  ends up on Pages next to `painbet-intake-scroll.html`, those are worth pulling
  out to files, as the scroll build already did with its frame sequence.
- The amber/blue split is a call, not a spec. If gold should stay on cash after
  all, it is one token: swap `--blue` for `--amber` in the money rules.
