# THE INTAKE — session handoff

_Hand this file to a new chat to continue with full context._
_Companion files: `painbet-intake-scroll.html` (the build),
`painbet-intake-scroll-PROMPTS.md` (all video/image prompts)._

## What this is

A scroll-and-click cinematic front end for pain.bet, built from three sources:

- **`painbet_intake_7.html` / `painbet_intake_11.html`** (uploaded by the user) —
  the original single-page intake app. All content and capture logic comes from
  here. v11 is the newer one and added the Private Ward (VIP) room.
- **`3d_organ_cooler_crate_v2.html`** (uploaded) — a teammate's 3D CSS crate,
  reworked into the pry-open prize modal.
- **Higgsfield-generated video** of a decayed hospital ward — the finished film,
  shot as four 15s segments and now live in the page (see Footage, below).

Deliverable: **`painbet-intake-scroll.html`** — one standalone file, no build
step, vanilla JS + canvas, in the style of the rest of this repo.

## Current state — live and working

- **Branch:** `claude/painbet-intake-scroll-21zij3`. No open PR right now —
  everything through PR #65 is merged to `main`.
- **Live:** `https://odds0ckx.github.io/painbet/painbet-intake-scroll.html`
  (GitHub Pages, source = `main` branch root, redeploys automatically a
  minute or two after every merge to `main`).
- Verified end to end in Chromium via Playwright at phone size, and the user
  has been testing the live Pages URL directly and reporting bugs from it —
  several real ones got fixed this way (see "Fixed this session," below).
  **Nobody has done a full manual pass through all ten capture stations in
  one sitting** — see Next steps.

## How it works

**Film between stations.** The journey is one continuous ~60s film; the forms
are popups that arm at specific held frames.

1. Lands on a **PAIN.BET title card** with a `Check in` button.
2. Pressing it **auto-plays the footage** (scroll position is driven
   programmatically, eased) forward to the next station.
3. At a station, its form's card — which has been fading in, centred over the
   held frame, the whole approach — **becomes interactive and scroll locks**.
   The card **does not move or reparent** when this happens; arming the gate
   only toggles the scroll lock. This used to lift the card into a separate
   bottom-sheet modal, which caused a visible jump every time — see the fixed
   bugs below before touching this again.
4. Submitting closes the gate (unlocks scroll) and auto-plays on to the next
   station. The exit is the same scroll-driven fade that brought the card in,
   now running in reverse — there is no separate exit animation.
5. Scroll still scrubs the footage manually at any time; a deliberate scroll
   cancels an auto-play, a stray notch does not. A floating **Continue**
   button appears if the viewer ends up between rooms with nothing to press.

**Rendering:** one fixed full-screen `<canvas>` per scene; scroll position maps
to an absolute frame number in the single shared film sequence,
`assets/seq/film/`. Frame sequences are used rather than `<video>` because
reverse scrubbing is smooth and it avoids iOS Safari seek stutter.

### Scene order (14 scenes, `SCENES` array)
`admissions` (run) → `quiz` → `intake` (run) → `wallet` → `ward` (run) →
`discharge` → `locker07` (run) → `reveal` → `channels` → `dispensary` →
`dashboard` → `vip` → `staff` → `login`

This matches the original app's real order (quiz and diagnosis come **before**
the wallet room, not after). `ward` and the reworked `locker07` are short film
runs inserted between the capture stations so the camera has somewhere to
walk between them — see Footage below for why.

### Capture stations (logic ported verbatim from intake_7/11)
| Station | What it does |
|---|---|
| `quiz` | Intro screen → 5 questions → scored diagnosis (`DX`) → "Claim this chart" |
| `wallet` | Chain chips, `parseInput` wallet/tx validation with mis-chain detection, entry tally. **Skippable** — "Skip the giveaway, just send my chart", which now toasts a confirmation either way (entries logged or not) |
| `discharge` | Telegram/email, handle validation, 8-char password meter, VIP toggle |
| `reveal` | Opens the **3D crate modal** on button press (no longer auto-opens — see fixed bugs): tap repeatedly to ratchet the seal, latch breaks, lid swings, weighted `rollPk()` prize |
| `dispensary` | **Real 10-segment canvas wheel** that spins and lands on the weighted roll, published odds, drop-code redeem, giveaways, payout feed |
| `dashboard` | Chart summary reading live state, Sunday countdown |
| `vip` | Tier-match pitch, 6-row upgrade table, host request |
| `staff` | Four tracks; Streaming reveals exclusive / non-exclusive affiliate terms |
| `login` | Return sign-in against handle / patient number / password |

Plus a **directory menu** (MENU, top right): My chart 07, Dispensary 08, Private
ward VIP, Staff entrance, Channels. Jumping past an unfinished station unlocks
the gates for browsing (matches the original's "have a look around" behaviour).

## Footage

`assets/seq/film/` — **1444 frames**, `frame_0001.webp` to `frame_1444.webp`,
800x1450, 24fps, 60.2s. The page runs on this and nothing else. Built from four
15s segments (1068x1936, 24fps, 361 frames each) concatenated losslessly, then:

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

The segment joins are invisible: measured frame-to-frame motion at each of the
three joins is 0.5-0.9 against a film mean of 3.1.

**Where the camera holds still** (measured, not taken from the prompt timings —
the shot order differs from the brief):

| Frames | Time | What is on screen |
|---|---|---|
| 699-722 | 29.1-30.1s | end of the corridor, before the doors |
| 1063-1177 | 44.3-49.0s | the room wide: gurney, caged bulb, x-ray lightbox |
| 1289-1315 | 53.7-54.8s | the wall of x-ray lightboxes |
| 1324-1350 | 55.2-56.2s | the locker, in passing |
| 1352-1388 | 56.3-57.8s | the desk, patient chart on a clipboard |
| 1414-1444 | 58.9-60.2s | the locker, held to the end |

### How the page uses it

Every scene draws from one shared `FilmSource` using **absolute frame
numbers**, not per-scene clips:

- a **run** (`type:'scrub'`) scrubs a frame range, `from` to `to`
- a **stop** (`type:'form'`) pins the playhead to `at`, a frame where the
  camera measurably holds still, and arms its gate there

`FPVH` (56 frames per viewport-height) sets every run's scroll length from its
frame span, so the dolly speed never changes between scenes. `runMs()` sets an
auto-play's duration from the real frame-time of the film it covers — **but
only when the walk actually ends at the very next scene** (see the `pushMs`
bug below for what goes wrong otherwise; `push()`'s own distance-based
fallback duration is the safe default when in doubt).

| Station | Frame | What is on screen |
|---|---|---|
| `quiz` | 710 | end of the corridor, before the doors |
| `wallet` | 1120 | the room, wide |
| `discharge` | 1370 | the desk and the patient chart |
| `reveal` | 1430 | the locker |

`ward` (1177-1352) and a reworked `locker07` (1388-1414) are short film runs
inserted between `wallet`/`discharge`/`reveal`, which would otherwise sit back
to back with no film between them.

Everything past `reveal` holds on a still frame of the film — the tail rooms
(`channels` onward) have no film of their own.

**Loading:** 1444 frames is 81 MB, far too much to preload. `FilmSource.ensure()`
loads a window around the playhead and caches what it fetches; a draw for a
frame that has not arrived falls back to the nearest decoded neighbour, so the
canvas never flashes empty mid-scrub.

## Fixed this session (read before touching the engine again)

These were all found by the user testing the **live Pages site**, not in
review — worth remembering that's a real, fast feedback loop for this project.

- **The film wasn't drawing at all.** `FilmSource.draw()` returned whatever
  `coverDraw()` gave back, and `coverDraw` returns nothing — so `draw()` always
  evaluated falsy and the procedural placeholder silently covered every frame
  of the film for an entire merged PR before anyone noticed. Every automated
  check up to that point only confirmed a canvas existed and had the right
  size, never that real pixels were on it. **If you write a check for this
  page, sample actual pixel colour, not just canvas existence/size.**
- **Cold-start blank backdrop.** A scroll position landing past a gate's
  threshold on the very first `render()` call (a reload mid-station, for one)
  used to skip painting the canvas entirely, because that logic sat after an
  early-return keyed on where the card currently lived. Fixed alongside the
  point below by making canvas drawing unconditional on visibility.
- **The popup jumping between centre and the bottom of the screen, glitchily,
  and a "vanish then pop back up" flash on skip/submit.** The card used to be
  reparented into a separate fixed, bottom-anchored `#station` modal the
  instant its gate armed, and reparented back out 320ms after closing. Two
  incompatible layout systems for what is visually the same card, with a
  discrete DOM move and no shared coordinate system between them. **Fixed by
  never moving the card at all** — arming/disarming a gate now only toggles
  the scroll lock; the same scroll-driven opacity fade that brings the card in
  is what takes it back out. Verified with Playwright by sampling the card's
  DOM parent and computed opacity 10-40 times a second across full transitions:
  zero pixel jump, and opacity moves as a smooth monotonic ramp, never a jump
  or a drop-then-rise.
- **The walk after submitting `discharge` was way too fast.** Its `pushMs`
  (~1.1s) was sized to match `locker07`'s frame span, the same pattern that
  correctly governs `quiz`'s and `wallet`'s `pushMs` against the scrub scene
  right after *them* (`intake`, `ward`). It doesn't work for `discharge`
  because `locker07` has no `gate` — the auto-play's `nextStop()` walks past
  it to `reveal`, so the real distance covered was three-plus screens, not
  the one short scrub scene the duration was sized for. **If you add or
  reorder a `pushMs` override, check whether the scene immediately after the
  one you're setting it on actually has a `gate`** — if not, the walk goes
  farther than that scene's frame span and the duration is wrong. When in
  doubt, leave `pushMs` unset and let `push()`'s distance-based fallback
  (`Math.max(3200, Math.min(9000, dist*1.35))`) size it — it measures the
  real distance at push time regardless of what gets skipped.
- **The crate auto-opened itself 450ms after the reveal gate armed**, before
  the button was ever pressed — so pressing "Pry it open" just replayed a
  crate that had already opened, which read as the button doing nothing.
  Removed the auto-click entirely.
- **The title card used plain text "PAIN.BET"** instead of the site's real
  wordmark (a red triangle standing in for the missing letter, `.BET` set
  smaller and muted beside it — the same mark used in `index.html` and
  `painbet-design-system.html`, class names `mk`/`tri`/`tld`). Now reused
  verbatim, scaled up for the hero.

## Where it was left off

The film is shot, extracted, and wired in. Every reported interaction bug has
been fixed and verified. The page is live.

### Next steps
1. **Walk it end to end by hand**, once, start to finish — quiz through
   login. Still hasn't happened as a single continuous pass; only individual
   stations have been spot-checked while chasing specific bug reports.
2. **The stencil sweep.** The doors were shot without the stencilled 07 and
   without the triangle above it, so twelve of the fifteen prompts in
   `painbet-intake-scroll-PROMPTS.md` still describe geometry that isn't in
   the footage, and the `_tri` reference plates in `scratch/refs/` still have
   a stencil triangle composited onto the doors that the real footage doesn't
   have. Only F2, F3 and Segment 2's prompts were ever updated to match.
3. Optional: an outro run for the tail rooms (`channels` onward), which
   currently just hold on a still frame of the film.

## Gotchas worth knowing

- **`classList.toggle(name, undefined)` flips the class** rather than clearing
  it. This caused invisible cards to keep regaining pointer events and swallow
  clicks. Always coerce with `Boolean(...)`.
- **Don't gate canvas drawing on where a card currently lives in the DOM** —
  see the cold-start blank-backdrop bug above. Canvas paint should depend only
  on visibility, never on an element's parent.
- **Don't reparent a card to change its layout between two visual states.**
  See the popup-jump bug above. If a card needs to look different once
  "active," change it in place (classes, CSS) — moving it in the DOM is what
  caused every glitch reported this session.
- **A `pushMs` override is only correct if the very next scene has a `gate`.**
  See the discharge timing bug above. `push()`'s own distance-based fallback
  is safer than a hand-computed number whenever a scrub-only scene might sit
  between the two gated stations.
- **`.scene canvas` must be `.scene > canvas`**, otherwise the rule captures
  canvases inside cards (the wheel) and absolutely-positions them.
- Auto-play cancel needs a **threshold**, or trackpad momentum strands the
  viewer mid-corridor.
- Higgsfield: **max 3 `@` references per prompt** (extras are silently dropped)
  and an `@` only binds if picked from the dropdown so it becomes a chip.
- **ffmpeg is not always installed** in a fresh web session container — check
  before relying on it, install if missing. Pillow is generally available and
  is what the compositing tool (`scratch/triangle-composite/`) uses.
- Testing: Playwright is available globally, not in the repo — import from
  `` `${npm root -g}/playwright/index.mjs` ``, browser at
  `/opt/pw-browsers/chromium`. Reading canvas pixels over `file://` throws a
  tainted-canvas error; screenshot instead, or serve the page over
  `http://` (`python3 -m http.server`) where `getImageData` works fine.
  **Sample actual pixel colour when verifying anything visual** — a check
  that only confirms a canvas is sized correctly would have missed the
  film-not-drawing bug above entirely, and it did, for a whole PR.
- **Background `python3 -m http.server` processes can silently die between
  tool calls in this environment.** Start it with `nohup ... & disown` and
  verify with a `curl` before trusting it's still up; a bare `&` in the same
  compound command that also backgrounds other work has been unreliable here.

## Brand rules (from the repo's HANDOFF.md)

Arterial red `#E10600` / `#FF4A42` = pain, risk, CTAs. Morphine blue `#7FD6E8` =
relief and credit **only**. Cash green `#5FE3A1` for money. Ground `#232427`,
card `#1B1D20`, sunk `#131517`. Archivo Black + Archivo + JetBrains Mono.
**No em-dashes in copy.** No hard white flashes.
In the footage: **the triangle goes in the world, the wordmark stays on the
page** — AI video garbles rendered text, so the mark is always described as
geometry and text is negative-prompted. On the page itself, the real wordmark
(`P` + triangle + `IN` + `.BET`, see `index.html`) is what "the wordmark" means
— reuse its exact markup/class names rather than re-deriving it.

## Previewing

**The real thing, full quality:** needs a web server for the frame sequences —
`python3 -m http.server` from the repo root, then open
`painbet-intake-scroll.html`. This is what the live Pages site actually runs.

**Standalone, no server, for quick pixel-level inspection:**
`python3 scratch/preview-page/build.py` writes `scratch/preview-page.html` — the
real page with a downsampled proxy of the film (every 4th frame, 240px wide)
embedded as data URIs, so it opens over `file://` with no server. This is the
tool that caught the film-not-drawing bug — good for confirming *something*
paints and *layout* is right; too soft to judge grain or grade. The generated
file is gitignored; the builder script is tracked. Needs ffmpeg + Pillow.

**A scrubbable timeline of just the film** (not the page), for reviewing pacing
and hold points in isolation: `python3 scratch/preview-film/build.py` writes
`scratch/preview-film.html`. Same proxy-frame approach, plus a measured
motion-trace timeline with the hold table above marked on it.

## Wheel PNG replacement (done, live in the page)

`painbet-intake-scroll-WHEEL-PROMPTS.md` holds the image prompts this came
from (sections 3E/3F, the cutting-wheel/saw-blade direction). Nathan generated
a plate from those and it's wired in:

- `assets/wheel/plate.png` and `assets/wheel/plate.webp` (2048x2048, real
  alpha), added straight to `main` and merged into this branch. The page loads
  the `.webp`.
- `drawWheel()` (`painbet-intake-scroll.html:880`) now draws `WHEEL_PLATE`
  with a single `drawImage()` instead of the old vector wedge-fill loop, then
  draws the ten prize labels on top exactly as before. `spinWheelTo()`
  (`:919`) targets `-(idx*step)+2π*6` rather than the old formula, since wedge
  0 sits at 12 o'clock at `rot=0` on this plate (the vector version started
  wedge 0 at 3 o'clock).
- The plate actually came back with 3 white / 3 blue / 2 red / 2 black wedges
  (one short of the even 3/3/2/2 red/black split the brief asked for). The
  `WHEEL` array (`:523`) is reordered, not the odds, to fit: money always
  lands on blue, entries always on white, PK always on red, and "Pain Scale
  +1" takes the second black wedge alongside "Nothing" since there wasn't a
  third red to give it. `rollWheel()` sums by probability so this reorder
  doesn't touch odds, and `renderOdds()`'s sorted list is unaffected.
- Sparks: `SPARKS`/`spawnSparks()`/`drawSparks()` (`:895-913`) throw a shower
  off the pointer position, spawn rate tied to actual angular speed each
  frame so it's heaviest at full spin and tapers to nothing as the plate
  grinds to a stop, palette-locked white fading to arterial red. This is
  diegetic (a cutting wheel throwing sparks), not a win celebration, so it
  doesn't conflict with the "no confetti/particles on a win" rule in section
  10 of the prompts file — it only ever fires during the spin itself.
- Verified in a standalone Playwright harness (not part of the repo) pulling
  the real `WHEEL`/`drawWheel`/`spinWheelTo` code: correct wedge lands under
  the pointer, label ink is legible against every wedge colour, sparks read
  clearly against the page's dark background.

If the plate ever gets regenerated, re-check the wedge colour order first
(section "0/2" of the prompts file) — this wiring assumes the specific
clockwise sequence white/black/red/blue/white/black/blue/red/white/blue that
this particular plate came back with, not the sequence the brief asked for.
