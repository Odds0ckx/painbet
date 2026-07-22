# pain.bet — Session Handoff

_Last updated: 2026-07-22. Hand this file to a new chat to continue work with full context._

## What this project is

**pain.bet** is a crypto-casino mockup / concept site. It is a **single-file static site**: everything (markup, CSS, JS) lives in **`index.html`** at the repo root (~600 KB). It is deployed via **GitHub Pages**. There is no build step, no framework — plain HTML/CSS/vanilla JS.

- **Repo:** `Odds0ckx/painbet`
- **Working branch:** `claude/handoff-8h673z` (all work happens here; see Git workflow below)
- **Default branch:** `main`

### Other files at repo root (standalone HTML explorations, not the live site)
- `painbet-paintracker.html` — a standalone "PainTracker" app mockup. **Important reference:** it imports into Figma cleanly; used to diagnose the Figma-import bug (see skill below).
- `painbet-arcade.html`, `painbet-synapse.html`, `concepts-pk-anesthesia.html` — other standalone concept pages.
- `scratch/` — throwaway explorations, all committed (the repo's stop-hook complains about untracked files, so commit new scratch files):
  - `painscale-breakthrough.html` — preview of the Pain Scale level-up effect (now shipped in index.html)
  - `drip-badge.html`, `drip-canvas.html` — Halloween drip visual explorations
  - `signup-form*.html` — four standalone signup-form exports (see "Most recent work")

## Brand rules (non-negotiable — apply to everything)

- **Arterial red** (`--red:#E10600`, `--redhi:#FF3B33`) = pain / risk / primary CTAs.
- **Morphine blue** (`--blue:#7FD6E8`) = money-back / credit / relief ONLY. Never use blue for risk.
- **Never** blend red directly into flat grey or white. No hard white flashes.
- **No em-dashes** anywhere in copy.
- Fonts: **Archivo Black** (display, `--disp`) and **Archivo** (body, `--sans`) only. Sometimes IBM Plex Mono for tabular numbers on standalone pages.
- Background `--bg:#232427`, cards `--card:#1b1d20`.
- **Ambient motion always plays** regardless of `prefers-reduced-motion` (deliberate brand choice).

### Key `:root` tokens (in index.html)
`--bg --card --card-hi --ink/--ink-hi/--ink-lo --red/--redhi --blue --disp --sans --r-lg(16) --r-md(12) --r-sm(8) --ease-out(cubic-bezier(.22,1,.36,1)) --shadow-lg`

## Architecture patterns to know

- **View-gating:** animation loops check `document.getElementById('view-X').classList.contains('on')` inside `requestAnimationFrame` so off-screen widgets pause. Applies to Threshold Raid neuron, PainKillers/Anesthesia widgets, and the Pain Scale breakthrough engine.
- **Canvas 0×0 sizing bug (recurring gotcha):** a canvas initialized while its view is `display:none` sizes to 0×0 and never re-measures (only a `window resize` fires `resizeCanvas()`). Fix pattern: a `sized` flag + guard `if (w<2||h<2) return;` + lazy retry on the first active render-loop frame. Used by the Pain Scale engine and Threshold Raid neuron.
- **Balance sync:** `pkBalance` JS var → `syncPkBalance()` updates every `.js-pk-bal` element (sidebar, topbar, hero, mobile sheet, wallet modal, `#pk-wallet-num`).
- **Custom checkbox/radio:** `<label><input hidden><span class="box"></span>…</label>` with `input:checked ~ .box` sibling selector. Requires true DOM siblinghood.
- **Verification discipline:** confirm real DOM state with Playwright (`getBoundingClientRect`, `getComputedStyle`, `getImageData` alpha sampling) — screenshots can look deceptively correct (a card's own CSS glow was once mistaken for rendered canvas particles).

### Running Playwright in this environment
Playwright lives at `/opt/node22/lib/node_modules/playwright`. Use a CommonJS script that `require`s it by absolute path; Chromium is pre-installed (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`). Do not run `playwright install`. External Google Fonts requests fail behind the sandbox proxy — this is harmless (fonts fall back).

## Features shipped this session (in index.html)

- **PainKillers page** rebuilt: Tolerance Dial (250×250, `×1.6` text 45px, "TOLERANCE" caption 12.5px) first, then a merged **Wallet + IV drip** card, then **Live Relief Feed** + a "how relief arrives" info card. Cards use `.pk-row{display:flex;align-items:stretch}` with each `.promo` as a flex column so heights match.
- **Gooey/metaball IV drip** (SVG + `feColorMatrix` alpha-threshold), recolored from neon cyan to morphine blue, flipped horizontally, cropped (`viewBox="60 0 130 500"`), placed beside the wallet balance.
- **Anesthesia page:** countdown + blood-loss gauge concepts.
- **Pain Scale breakthrough effect:** ambient sparks, click bursts, unlock animation. Two tweaks the user required: (1) only the **active tier card** shakes, not the whole scale; (2) the hard white flash was replaced with a **soft glow-pulse** (`psbFlash`/`psb-flash` keyframes), not a flat white block.
- **Auth modal:** the Email tab gained **Register / Login** sub-tabs (Username, Password+eye, Email, Promo code, two consent checkboxes, Google/Telegram social buttons). The crypto **Wallet tab was left unchanged** (user: "crypto wallet is there so good"). Adapted the yellow reference screenshots to the site's red/black/grey brand.

## Most recent work (this session's tail)

The user wanted the **signup form as a standalone HTML file** (no neuron WebGL background) and then to **import it into Figma via an HTML-to-Figma plugin**. It kept importing blank. Four iterations in `scratch/`:
1. `signup-form.html` — single centered modal, full styling, flat bg.
2. `signup-form-figma.html` — all states visible, no `display:none`, normal flow.
3. `signup-form-figma-safe.html` — `<input>`/`<button>` replaced with divs, CSS vars resolved to literals.
4. **`signup-form-figma-v2.html` — THE ONE THAT WORKED.**

**Root cause (now captured as a skill):** HTML-to-Figma importers **skip elements whose class/id/role signals a hidden overlay** (`modal`, `popup`, `dialog`, `overlay`, `role="dialog"`…). The fix was renaming `.modal`/`.mhead`/`.mbody`/`.mtabs` → `.card`/`.card-head`/`.card-body`/`.tabs`. Confirmed working by comparison with `painbet-paintracker.html`, which uses a neutral `.app` container and imports fine.

### New skill created
**`.claude/skills/html-to-figma-export/SKILL.md`** — a **project skill** (committed to the repo, so it persists and auto-triggers in future sessions). It documents the overlay-detection fix plus the `display:none`, native-form-control, and viewport-centering traps, with a pre-handoff checklist.

## Git workflow (important, recurring)

- All work → branch **`claude/handoff-8h673z`**. Never push elsewhere without permission.
- The repo owner (`Odds0ckx`) **merges PRs very quickly**, often within minutes. So each new round of work needs: `git fetch origin main`, confirm state, then a **new draft PR** — never reopen a merged one.
- If the branch's PR is already merged: restart the branch from latest `main` (`git fetch origin main && git checkout -B claude/handoff-8h673z origin/main`), keep the same branch name, push follow-up as a new PR.
- Commit messages: use heredoc form (`git commit -m "$(cat <<'EOF' … EOF)"`) to avoid quote-escaping breakage. Do NOT put the model identifier in commits/PRs.
- **Stop-hook false positives:** GitHub's own "Merge pull request #N" commits (committer `noreply@github.com`) get flagged as "Unverified." These are NOT authored by us — do not amend/rewrite merged shared history.
- **Do not schedule proactive check-ins.** The user has repeatedly rejected `send_later`/`ScheduleWakeup` calls. Only check the PR on demand.

## Current state at handoff

- **PR #30** ("Add standalone signup/login form preview") is **open, draft, mergeable, clean.** Head commit `10c99b9`. Contains: the 4 `signup-form*.html` files + the `html-to-figma-export` skill. Awaiting owner merge.
- Working tree is clean (before this handoff file). **This `HANDOFF.md` is new/uncommitted** — commit it if you want it tracked.
- No open tasks. The signup-form/Figma thread is fully resolved (v2 worked, user confirmed "YES that worked perfectly").

## Note on the user's standing request

The user asked to be **prompted to move to a new chat (with a fresh handoff file) once the conversation grows long / token-heavy.** There is no automated token-count trigger available, so watch for it conversationally and proactively suggest a handoff when the thread gets long.
