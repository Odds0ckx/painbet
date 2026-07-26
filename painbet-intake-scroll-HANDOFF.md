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

### The 60s film (live)

`assets/seq/film/` - **1444 frames**, `frame_0001.webp` to `frame_1444.webp`,
800x1450, 24fps, 60.2s. The page runs on this and nothing else; the three
original clips have been deleted.

Built from four 15s segments (1068x1936, 24fps, 361 frames each) concatenated
losslessly with the ffmpeg concat demuxer, then:

```
ffmpeg -i intake-master.mp4 -vf "scale=800:-2" \
  -c:v libwebp -quality 78 -compression_level 5 -vsync 0 \
  assets/seq/film/frame_%04d.webp
```

Note `-c:v libwebp` and `-quality`, not `-q:v`. With `-q:v` ffmpeg writes a
single animated webp instead of a frame sequence.

| Segment | Frames | Beat |
|---|---|---|
| S1 | 1-361 | burst in, nurse stares, she turns and leads, the rot begins |
| S2 | 362-722 | corridor, the lights stutter, silhouettes |
| S3 | 723-1083 | she opens the doors, you pass through, she shuts you in |
| S4 | 1084-1444 | the room |

The joins are invisible: measured frame-to-frame motion at each of the three
joins is 0.5-0.9 against a film mean of 3.1, so every segment does end on the
stillness the brief asked for.

**Where the camera holds still** (measured, not taken from the prompt timings -
the shot order differs from the brief). These are the candidate station markers:

| Frames | Time | What is on screen |
|---|---|---|
| 699-722 | 29.1-30.1s | end of the corridor, before the doors |
| 1063-1177 | 44.3-49.0s | the room wide: gurney, caged bulb, x-ray lightbox |
| 1289-1315 | 53.7-54.8s | the wall of x-ray lightboxes |
| 1324-1350 | 55.2-56.2s | the locker, in passing |
| 1352-1388 | 56.3-57.8s | the desk, patient chart on a clipboard |
| 1414-1444 | 58.9-60.2s | the locker, held to the end |

Regenerate this table with a frame-difference pass over the sequence; the run
that produced it is in the session history.

### How the page uses it

There are no per-scene clips any more. Every scene draws from one shared
`FilmSource` using **absolute frame numbers**:

- a **run** (`type:'scrub'`) scrubs a frame range, `from` to `to`
- a **stop** (`type:'form'`) pins the playhead to `at`, a frame where the
  camera measurably holds still, and opens its form there

`FPVH` (56 frames per viewport-height) sets every run's scroll length from its
frame span, so the dolly speed never changes between scenes, and `runMs()`
sets each auto-play to the real duration of the film it covers.

| Station | Frame | What is on screen |
|---|---|---|
| `quiz` | 710 | end of the corridor, before the doors |
| `wallet` | 1120 | the room, wide |
| `discharge` | 1370 | the desk and the patient chart |
| `reveal` | 1430 | the locker |

Two new runs had to be inserted: `ward` (1177-1352) and a reworked `locker07`
(1388-1414), because `wallet`, `discharge` and `reveal` used to sit back to
back with no film between them.

Everything past `reveal` holds on a still frame of the film, which is what the
page already did once the old footage ran out.

**Loading:** 1444 frames is 81 MB, far too much to preload. `FilmSource.ensure()`
loads a window around the playhead and caches what it fetches; a draw for a
frame that has not arrived falls back to the nearest decoded neighbour, so the
canvas never flashes empty mid-scrub.

## Where it was left off

The film is shot, extracted and wired in. The page runs on one continuous
sequence with the four stations landing on measured holds.

### Next steps
1. **Walk it end to end by hand.** Automated checks cover load, paint, the
   station opening after the run, and no console errors. They do not cover
   completing every form in sequence, because each gate blocks until it is
   satisfied. Worth one manual pass.
2. **The stencil sweep.** The doors were shot without the stencilled 07 and
   without the triangle above it, so twelve of the fifteen prompts still
   describe geometry that is not in the footage, and the `_tri` reference
   plates still have a stencil triangle composited onto the doors. F2, F3 and
   Segment 2 are already updated.
3. Optional: an outro run for the tail rooms, which currently hold on a still.

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
