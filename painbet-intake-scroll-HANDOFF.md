# THE INTAKE — session handoff

_Hand this file to a new chat to continue with full context._
_Companion files: `painbet-intake-scroll.html` (the build),
`painbet-intake-scroll-PROMPTS.md` (all video/image prompts),
`painbet-intake-scroll-BUILD.md` (engine spec for a lighter model)._

## What this is

A scroll-and-click cinematic front end for pain.bet, built from three sources:

- **`painbet_intake_7.html` / `painbet_intake_11.html`** (uploaded by the user) —
  the original single-page intake app. All content and capture logic comes from
  here. v11 is the newer one and added the Private Ward (VIP) room.
- **`3d_organ_cooler_crate_v2.html`** (uploaded) — a teammate's 3D CSS crate,
  reworked into the pry-open prize modal.
- **Higgsfield-generated video** of a decayed hospital ward.

Deliverable: **`painbet-intake-scroll.html`** — one standalone file, no build
step, vanilla JS + canvas, in the style of the rest of this repo.

## Current state

- **Branch:** `claude/scrolling-animation-redesign-rl1l09`
- **Open PR:** #55. PRs #51-54 already merged to `main`.
- Working, verified end to end in Chromium at phone and desktop sizes.

## How it works

**Film between stations.** The journey is a film; the forms are popups.

1. Lands on a **PAIN.BET title card** with a `Check in` button.
2. Pressing it **auto-plays the footage** (scroll position is driven
   programmatically) all the way to the next station, ~7-11s.
3. At a station a **form rises as a bottom-sheet popup** (the "clipboard").
   Page scroll locks while it is open — the popup *is* the gate, nothing can be
   skipped. Scrolling **inside** the card still works.
4. Submitting closes it and auto-plays on to the next station.
5. Scroll still scrubs the footage manually at any time; a deliberate scroll
   cancels an auto-play, a stray notch does not. A floating **Continue** button
   appears if the viewer ends up between rooms with nothing to press.

**Rendering:** each scene is a fixed full-screen `<canvas>`; scroll position maps
to a frame of a WebP image sequence in `assets/seq/<scene>/`. Frame sequences are
used rather than `<video>` because reverse scrubbing is smooth and it avoids iOS
Safari seek stutter.

### Scene order (13 scenes, `SCENES` array)
`admissions` (film) → `quiz` → `intake` (film) → `wallet` → `discharge` →
`locker07` (film) → `reveal` → `channels` → `dispensary` → `dashboard` → `vip` →
`staff` → `login`

This matches the original app's real order (quiz and diagnosis come **before**
the wallet room, not after).

### Capture stations (logic ported verbatim from intake_7/11)
| Station | What it does |
|---|---|
| `quiz` | Intro screen → 5 questions → scored diagnosis (`DX`) → "Claim this chart" |
| `wallet` | Chain chips, `parseInput` wallet/tx validation with mis-chain detection, entry tally. **Skippable** — "Skip the giveaway, just send my chart", which is also the way out once entries are logged |
| `discharge` | Telegram/email, handle validation, 8-char password meter, VIP toggle |
| `reveal` | Opens the **3D crate modal**: tap repeatedly to ratchet the seal, latch breaks, lid swings, weighted `rollPk()` prize |
| `dispensary` | **Real 10-segment canvas wheel** that spins and lands on the weighted roll, published odds, drop-code redeem, giveaways, payout feed |
| `dashboard` | Chart summary reading live state, Sunday countdown |
| `vip` | Tier-match pitch, 6-row upgrade table, host request |
| `staff` | Four tracks; Streaming reveals exclusive / non-exclusive affiliate terms |
| `login` | Return sign-in against handle / patient number / password |

Plus a **directory menu** (MENU, top right): My chart 07, Dispensary 08, Private
ward VIP, Staff entrance, Channels. Jumping past an unfinished station unlocks
the gates for browsing (matches the original's "have a look around" behaviour).

## Footage

| Scene | Frames | Source |
|---|---|---|
| `admissions` | 169 | corridor descent, nurse leads to the 07 doors |
| `intake` | 169 | through the doors into the exam room |
| `locker07` | 145 | exam room to the locker, opens on a glowing red triangle |

Extracted from the user's mp4s with ffmpeg (`scale=800:-2`, WebP q78). Form rooms
without their own film use a **still backdrop** (`still:` in the scene config)
taken from a nearby frame, so nothing falls back to the procedural placeholder.

`scratch/refs/` holds full-res stills pulled from the footage, to be uploaded to
Higgsfield as `@ward_clean`, `@ward_decayed`, `@examroom`, `@locker`. **Upload
the `_tri` versions** - same plates with the brand geometry composited in (EXIT
lettering replaced by a red triangle, stencil triangles above the 07, the
biohazard trefoil on the locker replaced by a glowing triangle seal). The
originals are kept beside them, and `scratch/triangle-composite/` regenerates
the composites.

## Where it was left off

The user wants to **replace the three clips with one continuous ~60s film**,
shot as 4 x 15s segments (Higgsfield's per-generation limit). The full brief,
asset prompts, 5 keyframes and 4 motion prompts are in
`painbet-intake-scroll-PROMPTS.md`. Nothing is blocked on it — the page works on
the current footage.

### Next steps
1. User generates the assets, 5 keyframes and 4 segments.
2. Concatenate to one master mp4, extract frames.
3. **Build the single-sequence engine:** one frame set plus station markers at
   the four holds in Segment 4, easing to a stop at each. This is a small change
   — the push already eases; it just needs to target frame numbers within one
   sequence rather than separate scenes.
4. Optional: `discharge.mp4` outro (retreat down the corridor) — never shot.

### Questions now settled (see PROMPTS section 0 for the reasoning)
- The sign is **triangle-only**, no word. The shot footage renders EXIT cleanly,
  so this was a story call rather than a technical one: a sign that should
  promise a way out showing the house mark instead is the film in one frame.
- The triangle is **composited onto the existing stills**, not regenerated, so
  the grade of the shot footage survives. Done, in `scratch/refs/*_tri.jpg`.
- Every prompt's negatives used to read `text, lettering, words` while asking
  for a stencilled 07. They now read `words, letterforms, signage text`.
  **Numerals are never negative-prompted.**

## Gotchas worth knowing

- **`classList.toggle(name, undefined)` flips the class** rather than clearing
  it. This caused invisible cards to keep regaining pointer events and swallow
  clicks. Always coerce with `Boolean(...)`.
- **Scroll-locking a modal must not lock the card.** The first version
  `preventDefault`ed every scroll, so a form taller than the sheet could not
  reach its own buttons — the wallet room became impossible to leave.
- **A card mounted in the popup must not be styled by the scroll loop**, or the
  modal's transition fights inline opacity/transform and the arrival stutters.
- **`.scene canvas` must be `.scene > canvas`**, otherwise the rule captures
  canvases inside cards (the wheel) and absolutely-positions them.
- Auto-play cancel needs a **threshold**, or trackpad momentum strands the
  viewer mid-corridor.
- Higgsfield: **max 3 `@` references per prompt** (extras are silently dropped)
  and an `@` only binds if picked from the dropdown so it becomes a chip.
- **ffmpeg is not installed** in the web session container, though it was in an
  earlier one. Step 2 (extracting frames from the master mp4) needs it, so
  install it before starting that, or extract locally. Pillow is available and
  is what the compositing tool uses.
- Testing: Playwright is available globally, not in the repo — import from
  `` `${npm root -g}/playwright/index.mjs` ``, browser at
  `/opt/pw-browsers/chromium`. Reading canvas pixels over `file://` throws a
  tainted-canvas error; screenshot instead.

## Brand rules (from the repo's HANDOFF.md)

Arterial red `#E10600` / `#FF4A42` = pain, risk, CTAs. Morphine blue `#7FD6E8` =
relief and credit **only**. Cash green `#5FE3A1` for money. Ground `#232427`,
card `#1B1D20`, sunk `#131517`. Archivo Black + Archivo + JetBrains Mono.
**No em-dashes in copy.** No hard white flashes.
In the footage: **the triangle goes in the world, the wordmark stays on the
page** — AI video garbles rendered text, so the mark is always described as
geometry and text is negative-prompted.

## Previewing

The page needs a web server for the frame sequences (`python3 -m http.server`),
or use the self-contained preview: rebuild it by embedding downsampled frames as
data URIs and patching `FrameSource` — the build script used each time is in the
session history, roughly:
extract at `fps=11,scale=420:-2` q46, base64 into `window.EMBED`, then patch the
`FrameSource` constructor, its `preload` src line, and the `stillImg.src` line.
