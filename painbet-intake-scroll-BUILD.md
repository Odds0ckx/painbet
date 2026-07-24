# THE INTAKE — scroll-scrub build handoff

Standalone scroll-scrubbing cinematic front for pain.bet that hands off into the
existing intake_7 app. File: **`painbet-intake-scroll.html`** (single file, no
build, vanilla JS + canvas). This doc is written so a lighter model can finish
the **mechanical** work without touching the engine.

## What the engine already does (DONE — do not rewrite)
- Scroll position -> video frame scrubbing, painted to a per-scene `<canvas>`.
- Forward + reverse scrub (scroll up rewinds the footage).
- Seamless crossfade between clips (`FADE` band) + a shared grade / film-grain /
  vignette overlay so every clip reads as one film.
- Two scene TYPES: `scrub` (video) and `form` (interactive capture card pinned
  over a dimmed static frame). Content + order live in the `SCENES` array.
- **Woven capture forms — the intake_7 logic, ported and wired:**
  - `wallet`  — chain chips + wallet/tx capture, `parseInput` validation +
    mis-chain detection, entry tally (`ST.entries`).
  - `quiz`    — the 5 questions, scoring, and inline diagnosis stamp (`DX`).
  - `discharge` — Telegram/Email channel, handle validation, password meter
    (8-char min), VIP switch. Sets `ST.handle`/`ST.pw`/`ST.chan`.
  - `reveal`  — locker pry -> weighted PK prize roll (`rollPk`/`PK`).
  These share one `ST` state object so entries/diagnosis/prize carry through.
- The translucent **specimen card** shell for both text and forms.
- Reveal timing per scene, top "vitals" progress bar, active-room HUD tag, toast.
- Lazy frame preloading, DPR-aware canvas sizing with the `0x0` guard, rAF-
  throttled scroll. Placeholder frames render procedurally so it runs with zero
  assets today.

Verified in Chromium: canvases size correctly, and every form station captures
with intake_7's real validation (entry increments, mis-chain warning, quiz ->
diagnosis, password gate, prize roll). Google Fonts is CDN-loaded; harmless if
blocked.

## Your job (MECHANICAL — safe for a lighter model)

### 1. Drop in real Higgsfield frames
For each scene, put the exported frames here and update the `SCENES` entry:
```
assets/seq/<scene id>/frame_0001.webp ... frame_0120.webp   (i = 1..count)
```
Then in `painbet-intake-scroll.html`, in the `SCENES` array, set on that scene:
```js
dir:'assets/seq/admissions', count:120, ext:'webp'
```
Leaving `dir:null` keeps the procedural placeholder. Nothing else changes — the
loader builds `${dir}/frame_${i padded to 4}.${ext}` automatically.

**Getting frames from an mp4** (do this per clip, keep ~120 frames):
```
ffmpeg -i 01-admissions.mp4 -vf "scale=1080:-1" assets/seq/admissions/frame_%04d.webp
```
Match `count` to the number of files produced.

### 2. Fill copy
All headline/body/kicker/metric text lives in the `SCENES` array. Source copy is
in `intake_7`/`index.html`. Rules: no em-dashes; red only for pain/risk; blue
(`--blue`) only for relief/credit; cash green (`--cash`) for money figures.

### 3. Wire the handoff + remaining stations
`#handoff` section, `REPLACE(handoff)` marker. The post-capture intake_7 stations
(dispensary/wheel `s10`, dashboard `s9`, login `s8`, staff `s7`) are NOT yet in
this file. Port each by copying the form-station pattern: add a builder like
`buildWheel(card)` to the `FORMS` map, add a `{type:'form', form:'wheel'}` entry
to `SCENES`, and lift the matching handlers from intake_7's script (they use the
same `ST`/`WHEEL`/`GIVE`/`TASKS` structures). Or link out via the handoff button.

### 4. Add/reorder scenes
Add an object to `SCENES` — canvas, card, and spacer are generated from it. No
HTML editing. `type:'scrub'` for video, `type:'form'` + `form:'<name>'` for a
capture station. `vh` sets that scene's scroll length.

## Tuning knobs (top of the `<script>`)
- `SCRUB_VH` (default 3.2) — scroll length per scene in viewport-heights. Higher =
  slower, more deliberate scrub.
- `FADE` (default 0.06) — crossfade band between clips.
- Each scene's `reveal:[inStart,inEnd,outStart,outEnd]` — when its card fades
  in/out across that scene's progress 0..1.

## Do NOT touch (the quality-critical engine)
`FrameSource`, `coverDraw`, `drawPlaceholder`, `sizeCanvas`, `render`, the boot
retry loop. These carry the scrub math, crossfade, and the `0x0`-canvas fix.

---

## Higgsfield asset spec (for whoever renders the videos)

**Global:** 9:16, 1080x1920, 24fps, ~5s (~120 frames/clip). Motion = slow linear
**Dolly In** (Robo Arm for the locker). Same seed across clips. Generate keyframe
stills first (Soul), then use Start/End frame in DoP. Grade: teal shadows +
arterial-red glow, heavy 35mm grain, soft bloom, volumetric haze.

**Seamless chaining:** a clip's first frame = previous clip's last frame — reuse
the same still image, don't regenerate.

Clip list, motion prompts, and the first/last **keyframe image prompts** (with the
shared STYLE / SETTING / CHARACTER lock block) are in the chat handoff; keep them
alongside this file if regenerating.
