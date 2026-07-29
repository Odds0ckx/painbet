# pain.bet — Developer Handoff & Site Audit

_Audit date: 2026-07-29. Audited build: `index.html` at commit `bbf9f3e`._

This document is written for an incoming development team that will connect this
front end to a live casino platform. It covers what was tested, what passed, what
must be fixed, and the recommended integration route.

---

## 1. Verdict

**The front end is structurally sound and safe to hand over.** Across every page
and both breakpoints there were zero JavaScript runtime errors, zero failed
network requests, zero broken images, and zero horizontal overflow.

**It is not yet functional as a casino.** The single largest gap is that
**game tiles are decorative** — no game on the site can be launched. That is the
primary integration task and it is described in detail in section 5.

There is also one **presentation-level defect that affects every visitor**: two of
the three brand fonts are never actually loaded (section 4, P0-2).

---

## 2. How this was tested

Served locally (`python3 -m http.server 8931`) and driven with Playwright
(Chromium) at **1440×900** and **390×844**, exercising:

- All 12 sidebar destinations, plus Sports, Arcade, and the three "View all" pages
- Both embedded iframes (Arcade, PainTracker)
- Auth modal (register + sign in), deposit modal, promo detail modal, legal modal
- Sports odds → bet slip interaction
- Rail pagination arrows and horizontal scroll behaviour
- Every `<a>` on the page, checked for a real destination or handler
- Computed font resolution, measured by canvas text metrics

Raw results: `audit-report.json` (not committed; regenerate with the scripts in
section 7).

---

## 3. What passed

| Area | Result |
|---|---|
| JS runtime errors | **0** across 16 views × 2 viewports |
| Failed network requests | **0** |
| HTTP responses ≥ 400 | **0** (except `/favicon.ico`, see P1-3) |
| Broken images | **0** of 50 resolved background/img assets |
| Horizontal overflow @ 390px | **None** on any page (`scrollWidth == clientWidth`) |
| Horizontal overflow @ 1440px | **None** on any page |
| Sidebar destinations | 12/12 render with correct headings |
| Arcade iframe | Loads, 9 playable games present |
| PainTracker iframe | Loads at both breakpoints |
| Sports bet slip | Works — clicking odds increments the slip (0 → 1) |
| Rail pagination | All 3 rails scroll correctly (originals/slots/live) |
| "View all" pages | Populate correctly (9 / 11 / 27 tiles) |
| Promo detail modal | Opens with correct title, detail, and rules |
| Footer legal modal | All 4 tabs wired (Terms, Privacy, AML, Responsible gaming) |
| Auth + deposit modals | Both open from the topbar; register reaches success state |
| Path portability | **No absolute URLs** — deploys correctly to any domain or subpath |

The portability point is worth emphasising: every asset, iframe, and import map
uses a relative path, so the site can be dropped at a domain root, a subpath, or
a CDN origin without modification.

---

## 4. Findings, prioritised

### P0 — blocks launch

**P0-1 · Game tiles are not interactive.**
All 47 tiles are plain `<div class="tile">` elements. They carry no click handler,
no `href`, no game ID, and no provider reference. The only listeners bound to
`.tile` are cosmetic (hover splatter canvas, video preview). Clicking a tile
produces no navigation, no modal, and no state change — verified at runtime.

This is expected for a design build, and it is the main work item. See section 5.

**P0-2 · Two of the three brand fonts never load.**
Only `Archivo Black` is embedded (as a base64 `@font-face`). There is **no**
`@font-face` for `Archivo` (regular) or `JetBrains Mono`, and no webfont `<link>`.
Measured by canvas metrics on a clean machine:

```
Archivo Black ....... 480px  ← genuinely loaded
Archivo ............. 361px  ┐
JetBrains Mono ...... 361px  ├─ identical to a nonexistent font
Inter ............... 361px  │  → all falling back
(nonexistent font) .. 361px  ┘
```

Impact: **913 elements** declare `Archivo` and **435** declare `JetBrains Mono`.
For any visitor without those fonts installed locally — i.e. effectively all real
users — body copy and every tabular number renders in a system fallback. This was
almost certainly invisible during design because the fonts are installed on the
design machine.

Fix: embed `Archivo` (400/500/600/700) and `JetBrains Mono` the same way
`Archivo Black` is already embedded, or self-host WOFF2 files under `assets/fonts/`.
Also note `--sans` is currently set to `'Inter'`, which is both unloaded and off-brand;
it should point at Archivo.

### P1 — fix before public launch

**P1-1 · No signed-in state.** After a successful registration the success panel
appears, but the topbar still shows "Sign in / Deposit". There is no account UI,
no `body` state class, and `window.markSignedIn` is `undefined`. The platform's
real session handling will replace this, but the dev team needs to know no
front-end hook exists yet.

**P1-2 · `drops` promo has no destination.** Its Go button closes the modal and
nothing else. Either build the page or remove the promo.

**P1-3 · No favicon.** `/favicon.ico` 404s on every page load.

**P1-4 · Game titles are not unique keys.** The Live rail contains four duplicate
titles — `Roulette` ×2, `Baccarat` ×2, `Blackjack` ×2, `Dragon Tiger` ×2 —
distinguished only by provider in the art filename (`-evolution` vs `-pp`). Any
mapping built on title alone will collide. Key on provider + game ID.

**P1-5 · No SEO or social metadata.** No `description`, no Open Graph tags, no
canonical URL. `<title>` is present.

### P2 — cleanup, non-blocking

- **4 dead legal links** in modal body copy (the `<a>Terms</a>` / `<a>Privacy Policy</a>`
  inside the admissions and affiliate modals have no handler). The *footer* legal
  links work correctly — only the in-modal ones are inert.
- **`apply-modal` is unreachable.** The affiliate application modal exists in the DOM
  but nothing calls `openModal('apply-modal')`.
- **`.tile .splat` is dead CSS.** No element uses it; the real hover effect is the
  `.fx` canvas.
- **Two `showView` routers coexist.** The earlier one is dead code. Only the later
  one is live and exposed as `window.showView`. Delete the dead copy to avoid
  confusing a new developer.

---

## 5. Integration guide — connecting live games

This is the section that matters most for efficiency. **Do not hand the dev team a
2.1 MB HTML file and ask them to wire up 47 tiles.** Give them one seam instead.

### 5.1 Recommended approach

Add two data attributes to each tile and one launch function. The dev team then
replaces exactly one function body, and every tile on the site works — including
the "View all" pages, which clone tile markup and would otherwise need separate
handling.

```html
<!-- from -->
<div class="tile" title="Gates of Olympus 1000">

<!-- to -->
<div class="tile" data-game="gates-of-olympus-1000" data-provider="pragmatic" title="Gates of Olympus 1000">
```

```js
// Single delegated handler — survives cloning into the "View all" grids.
document.addEventListener('click', function (e) {
  const tile = e.target.closest('.tile[data-game]');
  if (!tile) return;
  launchGame(tile.dataset.game, tile.dataset.provider);
});

// The ONLY function the platform team needs to implement.
function launchGame(gameId, provider) {
  // e.g. window.location = `/play/${provider}/${gameId}`
  // or open the aggregator's iframe in a full-screen container
}
```

Because `fillAllGrid()` clones the rail's tile markup, the delegated listener and
the data attributes propagate to the "View all" pages automatically. No second
integration is needed.

### 5.2 Game inventory to map

47 tiles. Names live in the `title` attribute; art paths are in the inline
`background-image`. Full mapping table:

**Pain Originals (9)** — these correspond to the playable games already built in
`painbet-arcade.html`, so they may not need an external provider at all:

| Tile label | Mechanic (from `title`) | Art |
|---|---|---|
| FLATLINE | Crash · 10,000x | `assets/originals/flatline-bg.png` |
| NERVE | Mines · 24 cells | `assets/originals/nerve-bg.png` |
| BONESAW | Plinko · 16 rows | `assets/originals/bonesaw-bg.png` |
| DOSAGE | Dice · 98% RTP | `assets/originals/dosage-bg.png` |
| SPIKE | Limbo · 1,000,000x | `assets/originals/tolerance-bg.png` |
| PULSE | Keno · 10 picks | `assets/originals/threshold-bg.png` |
| BLACKOUT | Blackjack · sedate to 21 | `assets/originals/blackout-bg.png` |
| RIGOR | Dice duel · one reroll | `assets/originals/rigor-bg.png` |
| RELAPSE | Ward hold · commit | `assets/originals/relapse-bg.png` |

**Slots (11)** — Wanted Dead or a Wild, Gates of Olympus 1000, Le Bandit,
Sweet Bonanza 1000, Zeus vs Hades, RIP City, The Dog House, Sugar Rush 1000,
Starlight Princess 1000, Hand of Anubis, Fire Portals.

**Live casino (27)** — Crazy Time, Lightning Roulette, Stock Market, Funky Time,
Monopoly Live, Mega Roulette 3000, Mega Roulette, Gates of Olympus Roulette,
Crazy Balls, XXXtreme Lightning Roulette, Ice Fishing, Red Door Roulette,
Monopoly Big Baller, Amazing Baccarat, Dragon Tiger (×2), Roulette (×2),
Fortune Roulette, Baccarat (×2), Mega Sic Bo, Blackjack (×2),
Extreme Texas Hold'em, Mega Baccarat, One Blackjack.

Note the duplicates flagged in P1-4 — the art filename suffix (`-evolution`, `-pp`)
is the only thing distinguishing them in the current markup.

**Providers displayed (17):** Pragmatic Play, Evolution, Hacksaw, Nolimit City,
Push Gaming, BGaming, Games Global, BetGames, SmartSoft, Betsoft, Vivo Gaming,
Microgaming, Spribe, Habanero, OneTouch, Fugaso, plus a "+116 studios" modal.

### 5.3 Other seams the platform will need

| Feature | Current state | Hook to add |
|---|---|---|
| Session / auth | Mock modal, success panel only | `markSignedIn(user)` — swap topbar, set a `body` class |
| Balance | Hardcoded `USDT 2,840 · PK 1,250` | Single `updateBalance()` writing to the topbar pill |
| Deposit | Modal UI complete, no backend | Submit handler on `#depVeil` |
| Sports | Bet slip works client-side | Feed `#view-sports` from the odds provider |
| PainTracker | Static iframe | Pass real user stats into `painbet-paintracker.html` |

---

## 6. Recommended handoff method

**Hand over the repository, not the file.** Specifically:

1. **Give them the Git repo** (`Odds0ckx/painbet`) with this document at the root.
   The commit history is meaningful — it shows why the build is shaped the way it is.

2. **Point them at `HANDOFF.md` first, then this file.** `HANDOFF.md` explains the
   architecture and brand rules; `DEV_HANDOFF.md` explains what to build.

3. **Agree the data contract before they start.** The single highest-leverage
   decision is the shape of `data-game` / `data-provider` and the signature of
   `launchGame()`. Once that is fixed, the design side and the platform side can
   work in parallel without blocking each other.

4. **Set the expectation that `index.html` stays a single file, or plan the split
   deliberately.** A 2.1 MB single file is unusual for a production site. Two
   defensible routes:
   - **Keep it.** It works, it is portable, it has no build step. Extract the
     base64 assets to files to get it under ~300 KB.
     *Best if the timeline is short.*
   - **Split it.** Move CSS and JS to separate files, componentise the views.
     *Better long-term, but it is a rewrite and will re-introduce bugs that are
     currently fixed.*

   Recommendation: **keep the single file for launch**, extract the base64 assets,
   and revisit the split after the platform integration is stable.

5. **Tell the dev team what else is in this repo, so they don't touch it by mistake.**
   `painbet-intake-scroll.html` and `painbet-intake-11-v2.html` are **not** part of
   this site — they're a separate prelaunch project ("THE INTAKE," a scroll-driven
   capture/giveaway funnel), each with its own handoff doc and, for the scroll build,
   its own live Pages URL. `assets/seq/` (81 MB) and `assets/wheel/` (13 MB) belong
   to that project, not to `index.html` — leave them alone.

   `painbet-synapse.html`, `concepts-pk-anesthesia.html`, `painbet-design-system.html`,
   and `index-depreciated.html` genuinely are unwired concept scraps (confirmed: no
   other file references them). Those are safe to archive or remove if you want a
   cleaner repo for the incoming team, but that's a nice-to-have, not a blocker.

6. **Fix P0-2 (the fonts) before handover.** It is a small change and it means the
   dev team sees the site as it is meant to look, rather than reporting the fallback
   rendering back to you as a bug.

---

## 7. Reproducing the audit

```bash
python3 -m http.server 8931          # from repo root
# then drive http://localhost:8931/index.html with Playwright
```

Checks worth keeping in CI:

- No page errors on load for each view
- `document.documentElement.scrollWidth === clientWidth` at 390px on every page
- No `img` with `naturalWidth === 0`
- `document.fonts` contains every declared brand family
