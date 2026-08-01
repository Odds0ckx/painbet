# pain.bet — Session Handoff

_Last updated: 2026-08-01. Hand this file to a new chat to continue work with full context._

## What this project is

**pain.bet** is a crypto-casino concept site. It is a **single-file static site**: everything (markup, CSS, JS) lives in **`index.html`** at the repo root (~2.1 MB, mostly inline base64 image/video assets). It is deployed via **GitHub Pages** from `main`. No build step, no framework — plain HTML/CSS/vanilla JS.

- **Repo:** `Odds0ckx/painbet`
- **Working branch:** `claude/design-system-doc` (open as PR #101 as of this handoff — see Git workflow below; the older `claude/handoff-documentation-review-vm3mvf` is merged history, don't reuse it)
- **Default branch:** `main`
- **Live URL:** `https://odds0ckx.github.io/painbet/`

### How `index.html` is structured today
The current `index.html` is a **literal rebuild on top of an uploaded mockup file** (internally referred to as "B71" / `painbet_brand_mockup_27.html`), not a hand-written site. That history matters because bugs sometimes come from the mockup's own source file (corrupted embedded images, hardcoded absolute URLs, dead CSS) rather than from any edit made in a session — see "Known gotchas" below.

Two page systems coexist in the same file:
- **B71-native lobby pages** — Home, Promotions (`#promoPage`), Pain Scale (`#painPage`), Proof (`#proofPage`), The Chart (`#chartPage`), Sports (`#view-sports`, `.v5m`). Use `.tile` / `.banner` / `.pcard` / `.pscard` / `.row-head` card patterns, styled with the top-of-file `:root` tokens (`--blood`, `--glass`, `--glass-border`, `--tile-r`).
- **"v5m ported module" pages** — Threshold Raid, PainKillers, Anesthesia, Affiliate, Triage/Support, Arcade, plus modals (chat, apply/admissions, legal, providers). Marked `class="view v5m syspage"` / `class="modal-bg v5m"`, toggled via `.on`, styled under a **second, `.v5m`-scoped `:root` token set** (`--card`, `--ink-hi`, `--red` remapped to `var(--blood)`). `.v5m .blk` is the card wrapper for these pages — it needs `padding` set explicitly (was `padding:0` for a while, a real bug, now fixed at `28px 32px`).

### Other files at repo root (not the live site)
- `painbet-arcade.html` — The Arcade's 9 playable Originals, loaded via iframe (`?embed=1`) from the "Arcade" nav. Has its own `:root` token set; was restyled this session to match the main site (see changelog).
- `painbet-paintracker.html` — PainTracker drawer content, loaded via iframe (`?embed=1`).
- `painbet-synapse.html`, `concepts-pk-anesthesia.html`, `painbet-intake-11-v2.html`, `painbet-intake-scroll.html`, `painbet-design-system.html` — older standalone concept pages, not wired into the live site.
- `painbet-design-system-v2.html` — **new (this handoff, PR #101).** The real design-system reference doc, built per `DESIGN_SYSTEM_PROMPT.md` from `USER_JOURNEYS.md` + `index.html` via the Hallmark skill: full component/modal/flow inventory, resolved token conflicts, WCAG contrast audit, responsive down to 390px. `painbet-design-system.html` (no `-v2`) is a different, older artifact — a raw Figma-export extraction — left untouched per the never-delete-overwrite rule. Open in a browser directly, no build step.
- `index-depreciated.html` — the pre-mockup version of the site (kept for reference; had the neuron WebGL sign-in cinematic that got ported back into the new `index.html`).

## Brand rules (non-negotiable — apply to everything)

- **Arterial red** = pain / risk / primary CTAs. Current token: `--blood:#e0163c` (top-level `:root`), remapped inside `.v5m` as `--red:var(--blood)`, with `--redhi:#ff2450` as the brighter hover/accent shade.
- **Morphine blue** = money-back / relief / withdrawals ONLY. Token: `--blue:#7FD6E8` (inside `.v5m`) / literal `#7FD6E8` on B71-native pages. **Never use blue for a generic "success" or generic accent** — it's semantically reserved. (Caught a real instance of this: the "Lightning fast withdrawals" panel is blue-themed because withdrawals = relief; when replacing its zap-emoji icon with a custom bolt animation, it was recolored to `--blue`, not red, to keep the convention.)
- No em-dashes anywhere in copy.
- Fonts: **Archivo Black** (display) and **Archivo** (body) only. IBM Plex Mono / JetBrains Mono for tabular numbers, tags, and mono labels.
- Page background `--bg:#07080a`, but **the actual visible background is `.ambient{background:#101114}`**, a fixed full-viewport layer painted on top of `body`. Any gradient/overlay meant to fade to "the page background" must target `#101114`, not `var(--bg)` — got this wrong once (hero vignette faded to the wrong color, visible as a grey seam) before fixing it.
- Card glass tokens: `--glass:rgba(15,17,22,.70)`, `--glass-border:rgba(255,255,255,.10)`, `--tile-r:18px`.

## Architecture patterns to know

- **Two router/view systems, both live, confusingly similar.** There are two separate `showView`/`VIEWS`-map IIFEs in the file (one earlier, effectively dead code left over from an older pass; one later, actually wired to the sidebar and exposed as `window.showView`). If you need to programmatically switch views from new code, always use `window.showView(key, null)` — grep for `window.showView = showView` to confirm which block is live before editing router logic.
- **Home page game rails** (`Pain Originals` / `Pick your poison` / `Live`, ids `secOriginals`/`secSlots`/`secLive`): horizontal-scroll rails (`.rail.originals/.slots/.live`) with pagination arrows (`.railnav .rbtn`, wired via `homeRailScroll(btn,dir)`) and a **"View all"** button (`showAllGames(cat)`) that populates a dedicated full-grid page (`view-originals-all` / `view-slots-all` / `view-live-all`, `.v5m syspage`) by cloning the rail's `.tile` markup into an empty grid on first click (`fillAllGrid`), then calls `window.showView`. These dedicated pages are cheap to extend — same pattern for any future "view all" needs.
- **Provider row** (`Browse by provider`): `.provmarquee` wrapping `.provrow`, an infinite auto-scroll marquee (duplicated content once, `translateX(-50%)` keyframe loop, pauses on hover). Edge-faded via `mask-image` gradient, not an overlay div. `.prov` cards carry a persistent (not hover-only) arterial-red glow.
- **Promo detail modal system:** any element with `data-promo="key"` (except `#pdGo` itself) opens `openDetail(key)`, which reads from a `PROMOS` JS object (keys: `welcome`, `anesthesia`, `raid`, `drops`, `quests`, `arcade`) and shows `#pdVeil`. The modal's Go button (`#pdGo`) routes per-key: `welcome`→deposit modal, `anesthesia`/`raid`/`arcade`→`window.showView(...)`, `quests`→`openTracker()`, `drops`→closes only (no dedicated page exists yet for Drops — a real, still-open gap, not a bug).
- **Mobile navigation (rebuilt this session, read this before touching topbar/sidebar CSS):**
  - The hamburger button (`#navBurger`) is **hidden on mobile** (`@media max-width:900px`). Desktop-only now.
  - In its place: a sticky **Casino/Sports segmented toggle** (`.mobmode`, buttons `#mobModeCasino`/`#mobModeSports`) right under the topbar. Clicking Sports calls `window.__enterSports()`; clicking Casino re-clicks the sidebar's "Lobby" link programmatically. A helper `syncMobMode(mode)` keeps the `.on` class in sync and is called from every mode-changing bottom-nav action too.
  - The sidebar (`.side`) becomes a **slide-in drawer** on mobile instead of `display:none` — `position:fixed`, `transform:translateX(-100%)` by default, `body.mobnav-open .side{transform:translateX(0)}`. A scrim (`#sideScrim`) dims the page and closes the drawer on click; Escape also closes it; clicking any link inside the drawer both navigates (existing behavior, untouched) and closes the drawer.
  - Bottom nav (`.bottomnav`, ids `#bnLobby`/`#bnArcade`/`#bnPain`/`#bnWallet`/`#bnMore`) was previously all dead `href="#"` links with zero JS — now fully wired: Lobby scrolls home + resets mode, Arcade/Pain route via the sidebar's own links or `showView`, Wallet opens the deposit modal, More opens the same drawer as before.
  - All of this JS lives in one IIFE near the bottom of the file (search for `getElementById('navBurger')`) — extend it there, don't create a third copy elsewhere.
- **View-gating:** animation loops check `document.getElementById('view-X').classList.contains('on')` inside `requestAnimationFrame` so off-screen widgets pause (Threshold Raid neuron, PainKillers/Anesthesia widgets).
- **Canvas 0×0 sizing bug (recurring gotcha):** a canvas initialized while its view is `display:none` sizes to 0×0 and never re-measures. Fix pattern: measure via `el.getBoundingClientRect()` at the moment of use, not at attach-time, and don't assume a single `resize` listener is enough.
- **Blood-splatter hover effect (`.fx`):** on `.tile`/`.banner`/`.pcard`/`.promo-hero`/`.pscard`, a **canvas-drawn** particle splatter (not an image — see `attach(el)`/`burst()`/`draw()` in the script block with the comment "Blood splatter on hover"), triggered on real `:hover` and, on coarse-pointer devices, on `touchstart` via a `.touch-lit` class with a 1200ms auto-clear. Note: `.tile .splat` (a *different*, older CSS class expecting a `<div class="splat">` child) is **dead CSS** — no HTML element ever uses it. Don't waste time tuning `.splat` opacity values; the real hover effect is the `.fx` canvas.

### Verification discipline
- Always test with a local server (`python3 -m http.server 8931` from the repo root) + Playwright, not just by reading CSS. Several bugs this session were invisible from source (a corrupted image baked into the mockup's own base64 data; a card that was 840px tall for a legitimate reason, not a bug) and only obvious once rendered.
- **Absolute GitHub Pages URLs break in sandboxed testing and in production off that exact path.** Always use relative paths for Three.js import maps, iframe `src`, asset URLs.
- **Playwright quirks specific to this repo:**
  - `fullPage: true` screenshots visually duplicate `position:fixed` elements (topbar, bottomnav, drawers) at intervals of one viewport-height — this is a screenshot-capture artifact, not a real bug. Don't chase phantom "duplicate panel" issues in full-page screenshots; use scrolled non-fullPage captures to confirm.
  - Clicking a `.side a` link while the mobile drawer is closed (`transform:translateX(-100%)`) sometimes hangs Playwright's actionability wait far longer than expected. Open the drawer first (`#bnMore` or, on old code before this session's changes, `#navBurger`) before clicking sidebar links in mobile tests.
  - `min-width:0` is required on flex/grid children that contain `overflow:hidden;text-overflow:ellipsis` text (e.g. wallet addresses) — otherwise flexbox/grid's implicit `min-width:auto` prevents the browser from ever shrinking the element below its content's natural width, and it overflows the viewport instead of truncating. Caught and fixed once on the Proof page; watch for the same pattern elsewhere.

## Session changelog (2026-07-29, this thread, PRs #79–#93)

Starting point: user uploaded a newer, more complete mockup file (`painbet_brand_mockup_27.html`, "B71") and asked to overwrite `index.html` with it exactly, then backfill real data/functionality. Everything below shipped and merged, in order:

1. **B71 mockup adopted wholesale** (PR #79) — real game inventory/provider list backfilled over the mockup's placeholder set, all absolute GitHub Pages URLs converted to relative, dev-only debug leftovers removed (stray ECG-trace canvas, hidden diagnostics panel), modal tab-switch vertical-jump bug fixed, neuron WebGL sign-in cinematic ported back from `index-depreciated.html`, Legal/Providers modals restored and footer links wired.
2. **Card padding + corrupted art + game rails** (PR #80) — `.v5m .blk` cards had `padding:0` (headers touching borders); an earlier "dedupe vs breadcrumb" pass had hidden several page `<h2>`s via `display:none`, leaving pages with no visible title (reversed). Three of the mockup's own embedded promo images were **corrupted at the source** (truncated JPEG data, confirmed byte-identical to the original upload) — cropped above the corruption point and re-encoded. Pain Originals/Slots/Live converted from wrapping grids to horizontal-scroll rails.
3. **Arcade restyle + rail pagination + View all pages** (PR #81) — `painbet-arcade.html` was still on the pre-redesign flat-red/solid-panel palette; retokenized to match. Added pagination arrows and dedicated "View all" pages for the three home rails.
4. **Hero vignette** (PR #82, 2 commits) — blended the hero video's hard edges into the page background (mint.io-style radial/linear mask), then fixed the color to target `#101114` (the real `.ambient` background) instead of `var(--bg)`, which had been a slightly-off near-black causing a visible seam.
5. **Mobile footer dead space** (PR #83) — `.main`'s and the footer's mobile bottom padding were both independently sized to clear the fixed bottom nav, stacking into two oversized gaps. Trimmed both.
6. **Provider marquee** (PR #84, #85) — converted the static provider grid into an infinite auto-scroll marquee with edge fade and persistent red glow; follow-up added vertical padding so the hover glow/lift stopped clipping against the marquee's own `overflow:hidden`.
7. **Tile glow clipping + opacity + splatter** (PR #86, #87) — rails had no top padding so the tile hover glow clipped flat; fixed with padding + a matching negative margin (twice — first pass wasn't enough, second pass tripled it and also deepened the glow's saturation). Game tile art moved from `opacity:.55` resting / `.92` hover to a flat `opacity:1` always, per explicit feedback. Discovered `.tile .splat` is dead CSS (see Architecture notes above) — the real "blood splatter" effect is the `.fx` canvas, which got a stronger/more saturated glow instead.
8. **Promo banners linked + CTAs wired** (PR #88, #90) — the three home banners had no click handler at all; added `data-promo` attributes to reuse the existing detail-modal system. A later pass found only the "welcome" promo's Go button actually did anything — wired Anesthesia/raid/Arcade to `showView`, Quests to `openTracker()`.
9. **Custom bolt icon** (PR #89) — replaced the "Lightning fast withdrawals" panel's `⚡` emoji with a bolt-drop-and-strike animation adapted from a user-supplied reference (originally yellow/white, jQuery+GSAP-dependent), reimplemented in pure CSS keyframes (no new JS deps), recolored to `--blue` per the money-back/relief brand rule.
10. **Proof page mobile overflow** (PR #91) — wallet address `<code>` elements overflowed the viewport on mobile; root cause was missing `min-width:0` on a `flex:1` + ellipsis-truncated element (see Verification discipline above). Also ran a full 390px-width overflow audit across all pages/modals — this was the only bug found.
11. **Mobile menu was fully broken, then redesigned** (PR #92, #93) — discovered the hamburger was `display:none` on mobile with nothing replacing it, AND all 5 bottom nav links were dead placeholders: **the entire sidebar (Slots, Promotions, Threshold Raid, PainKillers, Anesthesia, The Chart, Affiliate, Triage, Sports…) was unreachable on mobile.** Built a slide-in drawer + wired the bottom nav (PR #92), added a Sports entry point (also PR #92). Then, per follow-up feedback that a plain-text "Sports betting" link didn't read as a control, replaced the hamburger entirely with the Casino/Sports segmented toggle described in Architecture notes above (PR #93) — the drawer is still there, just now opened via "More" instead of a hamburger icon.
12. **Written report delivered as an Artifact** — a build-log style document explaining everything found broken/fixed vs. the raw mockup, for the user to show why the rebuild took as long as it did. Not part of the codebase; mentioned here in case a similar report is wanted for this later batch of work (items 1–11 above, i.e. the mobile-focused pass) — it wasn't generated for that half yet.

## Session changelog (2026-08-01, this thread, PR #101)

Starting point: user asked to resume "the design system task" — `DESIGN_SYSTEM_PROMPT.md` and `USER_JOURNEYS.md` had been added in PR #100 but the actual generation was never run.

1. **Generated `painbet-design-system-v2.html`** via a background agent running the Documents-scoped Hallmark skill (`Documents:hallmark`), reading `USER_JOURNEYS.md` + `index.html` as spec/ground-truth. Took three session-limit/stream-stall interruptions to complete (resumed each time from the same agent transcript, not restarted) — final file is 179KB, one self-contained page. Covers: foundations with real WCAG contrast numbers, every §11 component in every interaction state, all 15 modals (+1 undocumented one found in code) with bottom-sheet decisions, nav/layout, journeys J1–J23 as flow diagrams including the full gate-stack and a dedicated blocked-states section, breakpoints consolidated 12→4/5, content/voice rules, a full copyable token table.
2. **Resolved real token conflicts** found in the live code, documented inline with rationale rather than silently picked: duplicate `--red` values (`#e0163c` vs `#E10600`), `--r-lg` (16px vs 18px), `--bg` token vs the actual visible `#101114` ground colour, `--card`/`--glass` overlap.
3. **Local review caught a real bug** (Playwright, desktop 1440px + mobile 390px) before anything was shipped: `.doc-card{overflow:hidden}` was silently clipping wide component demos (topbar, sidebar) on mobile — the search box and sign-in button were invisible, not just visually cramped. Fixed by adding `overflow-x:auto` to `.doc-demo` so wide demos scroll within their own card instead of being clipped. Re-verified: mobile `body.scrollWidth` now matches viewport exactly (was 706px against a 390px viewport before the fix).
4. **Opened PR #101** (`claude/design-system-doc` → `main`), still **open, not merged** as of this handoff.
5. **Walked the doc's own "Open questions" section with the user and got real decisions**, then pushed a second commit recording them in the doc itself (so a future session doesn't re-litigate):
   - Drops promo dead end → confirmed, stays a documented dead end, no page planned
   - Sign-in → account routing → confirmed, stays on current page, no post-auth redirect
   - Demo mode → left unresolved, not currently planned
   - PainKillers redemption → left intentionally undefined pending a loyalty-economy decision
   - Support escalation → confirmed leave as-is, blocked on support tooling that doesn't exist yet
   - Hover-red button contrast (3.74:1, below 4.5:1 body-text AA) → confirmed gap accepted, treated as large text (clears 3:1)
   - Mobile balance pill wrap → confirmed leave as-is, cosmetic only
   - Breakpoint consolidation → not actually a question; already correctly scoped in the doc as future engineering work, not a completed migration

## Known gaps / things intentionally left alone

- **`drops` promo has no destination page.** Its Go button just closes the modal — there's genuinely no "Dispensary/Drops" feature page built anywhere in the site. Either build one or leave as-is; not treated as a bug.
- **`markSignedIn()` / topbar Sign In → Account swap** has not been re-verified against the current B71 build's "The Chart" account page. This was flagged as an open question early in the mockof-adoption work and never revisited — worth checking if sign-in should route somewhere specific post-auth.
- **Mobile balance pill** (`USDT 2,840 · PK 1,250`) is 147px wide and the text needs slightly more, so it wraps to 2 lines inside its own pill on some mobile widths. Not overflow, not broken, just not perfectly tight. Freed up a little space when the hamburger was removed but not fully investigated/resolved.
- **`.tile .splat` dead CSS** (see Architecture notes) is still in the stylesheet, just unused. Harmless; could be deleted in a cleanup pass but low priority.

## Git workflow (important, recurring — confirmed via repeated use this session)

- All work → branch **`claude/handoff-documentation-review-vm3mvf`**. Never push elsewhere without permission.
- The repo owner (`Odds0ckx`) **merges PRs within minutes**, essentially every time. Standing instruction from the user: **open a new PR automatically whenever a batch of changes is complete, without asking first.**
- Before starting *any* new work, check whether the branch's last PR is already merged: `git fetch origin main`, then `git merge-base --is-ancestor HEAD origin/main`. If true, **restart the branch from latest `main`** (`git checkout -B claude/handoff-documentation-review-vm3mvf origin/main`) before making new edits — never stack new commits on already-merged history. If the branch has *unmerged* commits beyond the merged history, rebase them onto the new base instead of discarding them.
- Commit messages: heredoc form (`git commit -m "$(cat <<'EOF' … EOF)"`). Never put the model identifier in commits/PRs/code comments.
- **Stop-hook false positive:** GitHub's own "Merge pull request #N" commits (committer `noreply@github.com`) get flagged as "Unverified." These are not authored by us — do not amend/rewrite merged shared history to fix this; it's expected/normal GitHub behavior, not a real problem.
- **Do schedule check-ins** (`send_later`) after opening a PR — roughly an hour out, re-checking CI/review/merge state, re-arming silently if nothing changed. This is the current standing instruction (opposite of an older, outdated note that used to say not to schedule check-ins — that guidance no longer applies).
- A GitHub webhook subscription is active for PR activity; merge notifications arrive automatically and the trigger should be deleted once a PR merges.

## Current state at handoff

- **PR #101 is open, not merged.** Branch `claude/design-system-doc`, 3 commits: add `painbet-design-system-v2.html`, record the open-questions decisions, this `HANDOFF.md` update. Check `gh pr view 101 --json state,mergedAt` before assuming it's live — the repo owner tends to merge fast but it may still be sitting there.
- No other open PRs, no open tasks. Nothing else uncommitted beyond what's on this branch.
- `index.html` (the live site) was **not touched** this session — this was a documentation-only pass. No changes to verify against the live URL.
- Local dev loop used this session: `python3 -m http.server 8093` from the `July 2026` parent folder (matches the "Painbet July" launch config), Playwright via the Homebrew `/usr/local/bin/python3` (not the sandboxed node/playwright path used in some earlier sessions), Chromium via `channel='chrome'`.
