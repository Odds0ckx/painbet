# pain.bet Sportsbook — Implementation Spec

Hand this file to the implementer. Everything lives in **`index.html`** (single-file static site, GitHub Pages, no build step). Work top-to-bottom; each numbered task is roughly one edit. **Verify with Playwright after each major step** (see `HANDOFF.md` for the environment's Playwright invocation). Do NOT use em-dashes in any copy. Never use blue for risk/odds — blue (`--blue #7FD6E8`) is money-back/payout/cashout only.

---

## 0. Context: how this site works (read first)

- **Views:** every page is `<div class="view" id="view-X">…</div>`. Only one has class `on` at a time. All views are siblings inside `<div class="main">`, alongside `<footer>`.
- **Navigation:** `show('X')` (defined ~line 2145) removes `.on` from all `.view`, adds it to `#view-X`, updates the selected sidebar item, scrolls to top, and runs per-view init hooks:
  ```js
  function show(v){
    document.querySelectorAll('.view').forEach(el=>el.classList.remove('on'));
    document.getElementById('view-'+v).classList.add('on');
    document.querySelectorAll('.sb-item[data-view]').forEach(a=>{
      a.classList.toggle('sel',a.dataset.view===v && !a.dataset.scroll);
    });
    window.scrollTo(0,0);
    if(v==='games') buildGames();
    if(v==='arcade'){ … }
  }
  ```
  You will add one line here: `if(v==='sports') buildSports();`
- **Click routing:** a delegated handler on `[data-view]` calls `show(el.dataset.view)`. So any `<button data-view="sports">` just works — no per-button wiring.
- **Hash router** (~line 2160): `if(h && document.getElementById('view-'+h)) show(h);` — `#sports` will deep-link automatically once the view exists.
- **View-gating for animations (MANDATORY pattern):** any `requestAnimationFrame` / `setInterval` loop must check the view is visible so off-screen work pauses. Canonical form already used by PainKillers/Anesthesia/Pain Scale:
  ```js
  const view = document.getElementById('view-sports');
  const isOn = () => view.classList.contains('on');
  // inside the loop: if(!isOn()) return; (for rAF, re-request next frame but skip work)
  ```
- **Design tokens** (in `:root`, ~line 24) — use these, never hardcode hex:
  `--bg #232427` · `--card #1b1d20` · `--card-2 #232529` · `--card-hi hsla(0,0%,100%,.04)` · `--card-hi2 hsla(0,0%,100%,.07)` · `--ink` (55% white) / `--ink-hi` (75%) / `--ink-lo` (25%) · `--white #fff` · `--red #E10600` · `--redhi #FF3B33` · `--red-dim #8f0400` · `--red-deep #520703` · `--blue #7FD6E8` · radii `--r-lg`(16) `--r-md`(12) `--r-sm`(8) `--r-pill` · `--ease-out` · `--shadow` / `--shadow-lg` · fonts `--disp` (Archivo Black) / `--sans` (Archivo).

---

## 1. Provider-swap design principle (why we build it this way)

The real sportsbook will be a **third-party provider widget** (same provider as RioDeOro — a hosted iframe/JS mount you re-skin). painbet is a static mockup, so we build a **native mock** whose DOM mirrors the provider's structure and whose theme = the values we'll later paste into the provider's back office.

- Build the mock content inside a wrapper: `<div class="content" id="sports-mount"> … mock markup … </div>`.
- Leave this exact comment at the top of `#sports-mount` so the swap is obvious later:
  ```html
  <!-- PROVIDER SWAP POINT: replace the mock markup below with the provider's
       iframe/JS mount when the account is live. Everything else (sidebar toggle,
       view routing, betslip shell, theme tokens) stays. -->
  ```
- This mirrors how `view-arcade` already embeds `painbet-arcade.html` via iframe — same concept.

---

## 2. Casino | Sports mode toggle (sidebar)

**Goal:** a two-segment pill at the top of the sidebar. "Casino" (default) shows the Casino nav group; "Sports" shows a new Sports nav group. The **Pain system group stays visible in both modes** (it's painbet's identity). Topbar, search, balance, Deposit are shared and unchanged.

**Mechanism — use a `data-mode` attribute on `<body>`; no rewrite of `show()`:**
```js
function setMode(m){
  document.body.dataset.mode = m;               // 'casino' | 'sports'
  try{ localStorage.setItem('pb-mode', m); }catch(e){}
  show(m === 'sports' ? 'sports' : 'home');
}
// restore on load, default casino:
try{ document.body.dataset.mode = localStorage.getItem('pb-mode')==='sports' ? 'sports':'casino'; }catch(e){ document.body.dataset.mode='casino'; }
```

**HTML** — insert immediately *inside* `<aside class="sidebar">`, before the `sb-logo` or right after it (implementer: place directly above `<nav class="sb-group" aria-label="Casino">`):
```html
<div class="mode-toggle" role="tablist" aria-label="Casino or Sports">
  <button class="mode-seg" data-mode="casino" onclick="setMode('casino')">Casino</button>
  <button class="mode-seg" data-mode="sports" onclick="setMode('sports')">Sports</button>
</div>
```

**Wrap the two casino-only nav groups** so CSS can toggle them. Give the existing Casino `<nav class="sb-group" aria-label="Casino">` an added class `sb-casino`. Add the new Sports nav group (task 3) with class `sb-sports`. Leave the Pain system group and `sb-foot` untouched (always visible).

**CSS:**
```css
.mode-toggle{display:flex;gap:4px;background:var(--card-hi);border-radius:var(--r-pill);padding:4px;margin:0 10px 12px}
.mode-seg{flex:1;padding:9px 0;border-radius:var(--r-pill);font:800 11px var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-lo);transition:background .2s,color .2s}
.mode-seg:hover{color:var(--ink)}
body[data-mode="casino"] .mode-seg[data-mode="casino"],
body[data-mode="sports"] .mode-seg[data-mode="sports"]{background:var(--red);color:#fff}
body[data-mode="sports"] .sb-casino{display:none}
body:not([data-mode="sports"]) .sb-sports{display:none}
body.navmin .mode-toggle{display:none}   /* collapsed desktop rail: hide toggle */
```
(In `navmin` collapsed mode the toggle hides; that's acceptable for v1. Do not spend time on a mini variant.)

---

## 3. Sports nav group (sidebar)

Add after the Casino group, class `sb-group sb-sports`. Same `sb-item` markup pattern as existing items: `<button class="sb-item" data-view="X"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">…</svg><span class="lbl">Label</span></button>`.

Items (data-view targets in parens — only `sports` needs a real view; the sport categories can all point to `sports` and set a filter via `onclick`, see task 5):
- **Live** — `data-view="sports"` + `onclick="setSport('live')"`, red LIVE dot
- **Starting soon** — `onclick="setSport('soon')"`
- **My bets** — `onclick="openBetslip()"` (reuse betslip panel, "My bets" tab)
- divider (`sb-title` "Sports")
- **Soccer** `onclick="setSport('soccer')"` · **Basketball** `('basketball')` · **Tennis** `('tennis')` · **MMA** `('mma')` · **eSports** `('esports')` · **American Football** `('nfl')`

All sport-category buttons: `<button class="sb-item" data-view="sports" onclick="setSport('soccer')">`. The `data-view="sports"` makes them switch to the sports view; `setSport()` sets the active filter and re-renders. Reuse the existing 2px-stroke line-icon style. Grab icons from any open icon set (Lucide-style single-path). Keep each SVG inline.

---

## 4. `view-sports` skeleton

Insert a new `<div class="view" id="view-sports">` as a sibling of the other views — put it immediately **before `<footer`** inside `.main` (that anchor is unique). Structure:

```html
<div class="view" id="view-sports">
  <div class="content" id="sports-mount">
    <!-- PROVIDER SWAP POINT: replace the mock markup below … (see task 1) -->

    <!-- 4a sport icon rail -->
    <div class="sb-iconrail" id="sports-iconrail"></div>

    <!-- 4b Live / Prematch / My bets tabs -->
    <div class="sp-tabs">
      <button class="sp-tab active" data-sptab="live" onclick="setSpTab('live')">Live</button>
      <button class="sp-tab" data-sptab="prematch" onclick="setSpTab('prematch')">Prematch</button>
      <button class="sp-tab" data-sptab="mybets" onclick="openBetslip('mybets')">My bets</button>
    </div>

    <!-- 4c Top matches carousel (3-up) -->
    <section class="blk"><div class="sec-head"><h2>Top matches</h2>
      <span class="railnav">…‹ ›…</span></div>
      <div class="rail rx" id="sp-topmatches"></div>
    </section>

    <!-- 4d Live now, grouped rows -->
    <section class="blk"><div class="sec-head"><h2>Live now</h2></div>
      <div id="sp-live"></div>
    </section>

    <!-- 4e big bets strip (reuse ticker vibe, static list) -->
    <section class="blk"><div class="sec-head"><h2>Big bets</h2></div>
      <div id="sp-bigbets"></div>
    </section>
  </div>
</div>
```
Reuse existing `.blk`, `.sec-head h2`, `.rail.rx`, `.railnav`, `.rbtn` classes (they already style the casino rails/scroll arrows).

---

## 5. Mock data + render engine (JS)

All JS goes in the existing `<script>` block near the other view builders (`buildGames`, `openProvider`). No network calls (GitHub Pages + sandbox block external APIs).

**Fixture data** — one array, ~18-24 matches spanning the 6 sports:
```js
const SPORT_FIXTURES = [
  {id:'m1', sport:'soccer', league:'Premier League', home:'Arsenal', away:'Chelsea',
   start:'Today 20:00', live:false, score:null, odds:{h:2.10, d:3.40, a:3.05}},
  {id:'m2', sport:'soccer', league:'La Liga', home:'Sevilla', away:'Valencia',
   live:true, score:'1 - 0', minute:"63'", odds:{h:1.72, d:3.60, a:4.80}},
  // …tennis/mma/esports have no draw: odds:{h:…, a:…} (omit d)
];
```
- `sport` values must match the `setSport()` keys from task 3.
- Two-way sports (tennis, MMA, some esports) omit `d`; render only H/A columns.

**State + renderers:**
```js
let spSport = 'all';       // active sport filter ('live' and 'soon' are pseudo-filters)
let spTab = 'live';        // Live | Prematch
function setSport(s){ spSport = s; if(document.body.dataset.mode!=='sports') setMode('sports'); renderSports(); }
function setSpTab(t){ spTab = t; document.querySelectorAll('.sp-tab').forEach(b=>b.classList.toggle('active',b.dataset.sptab===t)); renderSports(); }

let sportsBuilt=false;
function buildSports(){ if(sportsBuilt) return; sportsBuilt=true; buildIconRail(); renderSports(); startOddsDrift(); }
```
- `renderSports()` filters `SPORT_FIXTURES` by `spSport`/`spTab`, then paints `#sp-topmatches` (top 3-4 as cards), `#sp-live` (live matches as league-grouped rows), `#sp-bigbets` (a few static "whale bet" rows like the Live Relief ticker items). Called by `buildSports()` and whenever filter changes.
- `buildIconRail()` fills `#sports-iconrail` with a chip per sport + event count (count = fixtures of that sport).

**Odds drift (view-gated):**
```js
function startOddsDrift(){
  const view=document.getElementById('view-sports');
  setInterval(()=>{
    if(!view.classList.contains('on')) return;      // pause off-screen
    // nudge a random fixture's odds ±0.02-0.05, clamp >1.01, flag direction
    // re-render only the changed odds chips; flash them (see task 6 .odds.up/.down)
  }, 2500);
}
```
Never call this before `buildSports()`; never remove the `isOn` guard.

---

## 6. Odds button = the core interactive unit

Every selectable price is:
```html
<button class="odds" data-match="m2" data-pick="h" data-odds="1.72"
        onclick="togglePick(this)"><span class="ol">1</span><span class="ov">1.72</span></button>
```
CSS:
```css
.odds{display:flex;align-items:center;justify-content:space-between;gap:8px;min-width:64px;
  padding:10px 12px;background:var(--card-hi);border-radius:var(--r-sm);
  font:700 13px var(--sans);color:var(--white);transition:background .2s,box-shadow .2s}
.odds .ol{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-lo)}
.odds:hover{background:var(--card-hi2)}
.odds.sel{background:var(--red);box-shadow:0 0 0 1px var(--redhi) inset}
.odds.sel .ol{color:hsla(0,100%,100%,.7)}
/* drift flash — RED for up, GREY for down. NEVER blue. */
@keyframes oddsUp{0%{box-shadow:0 0 0 2px var(--red)}100%{box-shadow:0 0 0 2px transparent}}
@keyframes oddsDn{0%{box-shadow:0 0 0 2px var(--ink-lo)}100%{box-shadow:0 0 0 2px transparent}}
.odds.up{animation:oddsUp .6s var(--ease-out)}
.odds.dn{animation:oddsDn .6s var(--ease-out)}
```

---

## 7. Betslip (floating panel)

RioDeOro's yellow edge tab → painbet's arterial red. One panel, toggled open. Selections held in a JS array.

**HTML** — place near the mobile sheets (sibling of `#sheet-more`), so it's outside `.main`:
```html
<button class="betslip-tab" id="betslip-tab" onclick="openBetslip()">
  <span class="bt-label">Betslip</span><span class="bt-count" id="bt-count">0</span></button>
<aside class="betslip" id="betslip" aria-label="Betslip">
  <div class="bs-head"><h3>Betslip</h3><button class="x" onclick="closeBetslip()">✕</button></div>
  <div class="bs-tabs">
    <button class="bs-tab active" data-bstab="slip" onclick="setBsTab('slip')">Slip <span id="bs-slip-n">0</span></button>
    <button class="bs-tab" data-bstab="mybets" onclick="setBsTab('mybets')">My bets</button>
  </div>
  <div class="bs-body" id="bs-body"><!-- selections or empty state --></div>
  <div class="bs-foot" id="bs-foot"><!-- stake input, combined odds, payout, Place bet --></div>
</aside>
```

**JS:**
```js
let betslip=[];   // [{match,pick,odds,label}]
function togglePick(btn){
  const key=btn.dataset.match+'-'+btn.dataset.pick;
  const i=betslip.findIndex(s=>s.key===key);
  if(i>=0){ betslip.splice(i,1); btn.classList.remove('sel'); }
  else{
    // enforce one pick per match (deselect sibling picks of same match)
    betslip=betslip.filter(s=>s.match!==btn.dataset.match);
    document.querySelectorAll(`.odds[data-match="${btn.dataset.match}"]`).forEach(o=>o.classList.remove('sel'));
    betslip.push({key, match:btn.dataset.match, pick:btn.dataset.pick, odds:+btn.dataset.odds});
    btn.classList.add('sel');
  }
  renderBetslip();
}
function renderBetslip(){ /* paint #bs-body rows, combined odds = product of odds,
    payout = stake * combined; update #bt-count and #bs-slip-n; toggle .has-picks on tab */ }
function openBetslip(tab){ document.body.classList.add('betslip-open'); if(tab) setBsTab(tab); }
function closeBetslip(){ document.body.classList.remove('betslip-open'); }
function setBsTab(t){ … }
function placeBet(){ /* fake: decrement mock USDT balance shown in topbar/wallet,
    move slip to "My bets" as settled-pending, clear betslip, toast */ }
```
- **Balance:** reuse the existing balance display. USDT is shown in the topbar `.balance` button and wallet modal. PK balance has a sync helper (`syncPkBalance()` / `.js-pk-bal`); USDT is currently static text. For the fake `placeBet()`, just update the topbar USDT number directly (grep the `2,840` USDT node). Keep it simple; do not build a full ledger.
- **Empty state:** "Tap any odds to start a bet slip."
- **Mobile:** at `<=860px` the betslip becomes a bottom sheet, same mechanism as `#sheet-more` (reuse `.sheet-bg`/`.sheet` styling or mirror it). The edge tab stays visible.

**CSS (desktop panel + red edge tab):**
```css
.betslip-tab{position:fixed;right:0;top:50%;transform:translateY(-50%);z-index:80;
  background:var(--red);color:#fff;border-radius:var(--r-md) 0 0 var(--r-md);
  padding:14px 10px;writing-mode:vertical-rl;font:800 11px var(--sans);letter-spacing:.14em;text-transform:uppercase}
.bt-count{display:block;margin-top:6px;background:#fff;color:var(--red);border-radius:var(--r-pill);
  font-size:10px;padding:1px 6px;writing-mode:horizontal-tb}
.betslip{position:fixed;right:-360px;top:0;bottom:0;width:340px;background:var(--card);z-index:95;
  display:flex;flex-direction:column;box-shadow:var(--shadow-lg);transition:right .3s var(--ease-out)}
body.betslip-open .betslip{right:0}
body.betslip-open .betslip-tab{display:none}
@media(max-width:860px){ .betslip{right:0;left:0;top:auto;width:auto;height:70vh;bottom:-100%;
  border-radius:var(--r-lg) var(--r-lg) 0 0;transition:bottom .3s var(--ease-out)} body.betslip-open .betslip{bottom:0} }
```

---

## 8. Mobile entry point

Add "Sports" to the **More sheet** (`#sheet-more`, ~line 1790), same button pattern as the other sheet items:
```html
<button onclick="closeSheet('more');setMode('sports')"><svg class="ic" …>…</svg>Sports</button>
```
Do NOT change the 5 bottom-bar slots in v1 (Lobby / Arcade / Pain / Wallet / More) — least disruptive. Betslip edge tab covers in-sports slip access on mobile.

---

## 9. Theme spec block (paste as an HTML comment near `:root`)

Leave this in the file verbatim — it's the provider back-office config sheet:
```
<!-- SPORTSBOOK PROVIDER THEME MAP (paste into provider config when live)
 primary/active .......... #E10600  (hover #FF3B33)
 background/panel ........ #232427 / #1b1d20
 odds chip / chip-hover .. rgba(255,255,255,.04) / .07
 odds selected ........... #E10600 fill, #FF3B33 inner ring
 odds up / down flash .... #E10600 / rgba(255,255,255,.25)   (never blue)
 positive/payout/cashout . #7FD6E8  (blue = money-back only)
 text ..... 55% / 75% / 25% white
 fonts .... Archivo Black (headers), Archivo (body + odds)
 radii .... 16 / 12 / 8 ; pill for chips/tabs
 LIVE dot . #E10600 pulse
-->
```

---

## 10. Verification checklist (Playwright, after build)

1. `setMode('sports')` / clicking the Sports segment → `#view-sports` gets `.on`, Casino nav group hidden, Sports nav group shown, Pain system group still visible.
2. `setMode('casino')` returns to `#view-home`; localStorage persists mode across reload.
3. `#sports` hash deep-links straight to the sports view.
4. Icon rail renders one chip per sport with correct event counts.
5. Clicking an odds button adds a selection, betslip count increments, panel opens; clicking a sibling pick on the same match swaps (one pick per match); clicking again deselects.
6. Combined odds = product of selected odds; payout = stake × combined; `placeBet()` decrements the topbar USDT number and clears the slip.
7. Odds drift only animates while the sports view is `on` (check it pauses on another view — read the drift interval does nothing when `#view-home` is active).
8. Mobile (390px): More sheet has "Sports"; betslip is a bottom sheet; no horizontal overflow.
9. No console errors on any view. Verify real DOM/computed state, not just screenshots (a card's own glow can look like rendered content).

## 11. Scope / PR
- One PR, branch `claude/handoff-8h673z`, base `main`, **draft**. All changes in `index.html` (plus inline SVGs). No new files except this plan.
- Owner merges fast; if the branch's PR is already merged, restart the branch from latest `main` (`git fetch origin main && git checkout -B claude/handoff-8h673z origin/main`) before new work.
- Do not put any model identifier in commits/PRs. No em-dashes in copy.
