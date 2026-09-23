# index-v2.html — Session Handoff

_Last updated: 2026-09-23. Hand this file to a new chat to continue the `index-v2.html` lobby experiment with full context._

Read `HANDOFF.md` first for the overall project (brand rules, token system, how `index.html` is structured). This file only covers the **`index-v2.html`** workstream.

## What `index-v2.html` is

A **full copy of `index.html`** created as a layout sandbox for redesigning the lobby's "cockpit deck" area and, more recently, the site chrome. `index.html` itself is **untouched** — nothing here has been promoted to the live site yet.

- **Repo:** `Odds0ckx/painbet` · **Default branch:** `main`
- **Working branch:** `claude/optimistic-knuth-h3lvfc` (previous branch `claude/funny-goodall-71q6b4` is fully merged and retired — see Git workflow section)
- **Live-ish preview:** `https://github.com/Odds0ckx/painbet/blob/main/index-v2.html` (GitHub only shows source — download the raw file and open it locally to actually see it render)
- Also in this workstream: `concept-cockpit-deck.html` — a small standalone page that was the first layout test for the two cockpit boxes. Superseded by `index-v2.html`; kept for reference.

## What's been built (in order)

1. **Cockpit deck** — the old full-width "Lightning fast withdrawals" banner and the thin "AGONY" progress strip were merged into one side-by-side section (`.cockpit-deck`, a `7fr 5fr` grid that stacks under 900px).
2. **Withdrawals card** (`.cd-with`) — keeps the site's animated lightning bolt; its three stat tiles were rebuilt as **vault-terminal screens**. The card's own left-side static lightning icon (`.cd-with-ic`) was removed — the animated bolt on the right already carries that motif, the icon box CSS was dead-code-removed too.
3. **Terminal tiles** (`.cd-term` + `.cd-term-screen`) — frame/screen split: `.cd-term` is a beveled gradient frame, `.cd-term-screen` is the CRT glass (radial gradient, dot-matrix texture, scanlines, vignette). Values glitch via `.term-glitch`.
4. **Agony card** (`.cd-agony`) — header, a syringe/dosimeter gauge, tier labels, a centered "next reward" line, and a loss-buffer readout.
5. **Agony bar** (`.cd-agony-bar`) — sub-tick hashes `.1`–`.9`, red major tick at `.5`, white current tick + plunger-stopper line at the fill edge, glass sheen.
6. **Font** — JetBrains Mono replaced site-wide by the Google font **Huninn** (via the `--mono` token, so it's a one-line swap).
7. **Chrome** (`.topbar`, `.side`) — borderless "dashboard console" panels with clay/embossed controls.
8. **Sidebar group labels** (`.side .grp` — "Casino" / "Pain system" / "More") — switched from `--mono` to `--disp` (Archivo Black), recolored to `#ed2749`, and the colored dot markers (`.grp::before`) were removed entirely.
9. **Sidebar active-link color** — `.side a.on` text color changed to `#ed2749` in both places it's declared (base rule and the later clay-controls override — see gotcha below).
10. **Cockpit cards borderless** — `.cd-with` and `.cd-agony` both dropped their `border:1px solid var(--glass-border)` and now use a flat `background:#16191e` instead of `var(--glass)`.

## Page reworks — 2026-09-23 session (PRs #183–#193)

Every Pain-system page plus Affiliate and Triage was reworked, each through a screenshot → go-ahead → commit → PR loop. Full rationale lives in the shared doc "pain.bet index-v2 updates — what changed and why". Grep the class prefix to find each block; every page's new CSS is scoped to its view id.

| Page (view id) | What changed | CSS/JS prefix |
| --- | --- | --- |
| PainKillers (`#view-pk`) | Wallet drip → CSS-only syringe IV (10s seamless loop; standalone copy `painbet-syringe-drip.html`). Tolerance dial → calibrated 270° gauge ×1.0–×2.2 + 14-day capsule dose chart. Live relief feed → admissions log (time / patient / stake / result / relief), ~1 in 5 rows tagged YOU, only those move "You today". | `.pk-syr-*`, `.pk-dial`, `.pk-dose`, `.pk-frow`, `.pk-fcols` |
| Pain Scale (`#painPage`) | Replaced wholesale with `painbet-painscale-section.html`'s page: tube + tier bands at real heights, YOU marker, blue 9–10 glass, next-level breakdown, numbers-first unlock cards, console chrome. Ported with every selector scoped under `#painPage`, keyframes renamed `ps2-*`, ladder script in an IIFE. | `#painPage …` (ported block), `.nx`, `.spec .val` |
| Threshold Raid (`#view-synapse`) | Mechanic rebuilt: damage = USDT wagered during a timed window, no buy-in; boss level, countdown, HP bar with 75/50/25% phase breaks + PK drops; house-funded bounty split by √damage, 10% cap, 5% last hit; escape rolls 25% over and levels the boss up. Console chrome. | `.rd-*`, `.syn-*` (three.js neuron kept) |
| Anesthesia (`#view-anesthesia`) | One live readout (fixed −404/−412 mismatch), loss-to-fill bar removed, weekly cap per tier applied in the calc, RG line, 8-week dose history, next-rate chip. | `.ax-*` |
| Affiliate (`#view-affiliate`) | Standard deal 0.5% of wager → 25% of house edge; live referral dashboard (tiles, 30-day chart, top referrals); desk form behind "Apply for custom terms". | `.afd-*`, `.af-*`, `.afx-*`, `.aff2` |
| Triage (`#view-support`) | "What's hurting?" picker with instant answers, Live chat the only red route, cases with timeline + inline reply + per-case escalate, "Need a break?" limits panel. | `.tri-*`, `.tk-*` |

Up to #189 changes went into **both** `index.html` and `index-v2.html`; from #190 on, **index-v2 only** (standing rule in `CLAUDE.md`). `CLAUDE.md` also now requires the console chrome on any redone page and bans blue left-edge row accents.

Placeholder data to replace before launch: raid HP/bounty/tiers, Anesthesia caps (500 Agony / 1,000 Threshold), affiliate 2.5% blended edge, Triage staff/wait counts, dose-chart window (fixed 14 days).

## Key classes and where they live

All inline in `index-v2.html`'s single `<style>` block. Line numbers drift — **grep the class name**, don't trust these.

| Class | ~Line | What it is |
|---|---|---|
| `:root` tokens | 12 | `--panel-bg`, `--panel-weave`, `--clay-top`, `--clay-base`, `--milled-dark`, `--shadow-light` were added for this work |
| `.console-panel` | 36 | Flat panel fill applied to `.topbar` + `.side`. **Solid colour only, no texture** |
| `.ambient` | 43 | Fixed page backdrop — **this** carries the carbon-fibre micro-weave |
| clay controls | ~345 | Block comment `===== clay controls`; overrides `.btn`, `.balbtn`, `.notifbtn`, `.navburger`, `.navtabs`, `.search`, `.side a.on` |
| `.cockpit-deck` | 2351 | The 7fr/5fr grid |
| `.cd-with` | 2354 | Withdrawals card |
| `.cd-term` | 2372 | Terminal tile frame + `.cd-term-screen` glass |
| `.term-glitch` | 2394 | Two-layer `clip:rect()` glitch (`cdNoise` / `cdNoise2` keyframes) |
| `.cd-agony` | 2448 | Agony card |
| `.cd-agony-bar` | 2463 | Syringe/dosimeter gauge |

Markup for the cockpit deck: grep `<section class="cockpit-deck lobbyview"`.

## Design decisions worth not re-litigating

- **Brand colours over reference colours.** Reference designs got recoloured to the site palette: the vault terminal's green → `#7FD6E8` (morphine blue, correct here because the card is about withdrawals = relief), the dashboard's orange → `--blood` crimson. Per `HANDOFF.md`, blue is semantically reserved for relief/withdrawals — don't use it as a generic accent.
- **Texture belongs on the backdrop, not the panels.** In the dashboard reference the carbon weave is a `body` background *behind* a flat container. Putting it on `.topbar`/`.side` was wrong and was corrected — it lives on `.ambient` now, and you can see it peeking through the panels' rounded corners.
- **Don't invent copy from reference markup.** A `≡ NEEDLE HUB` label got copied verbatim out of the reference gauge and had to be removed. Port structure and styling, not flavour text.
- **Clay controls**: raised = 135deg `--clay-top`→`--clay-base` gradient + drop shadow + `inset 0 1px 2px rgba(255,255,255,.1)` top highlight. Pressed = shadow moves inside (`inset 0 3px 6px rgba(0,0,0,.7)`) + `scale(.96)`. Grouped tabs sit in a `--milled-dark` well with `inset 0 3px 6px`; the selected one lifts back out.

## Known gotchas

- **`Read` blows up on line 3436.** That line holds a huge base64 asset; any `Read` range covering it exceeds the token limit even with `limit:1`. Read around it, or use `sed -n 'A,Bp' index-v2.html | cut -c1-220`.
- **Class-name collisions leak styles.** The agony card kept `class="painchip"` (the old pain-scale strip's class, needed for existing JS click handlers) and silently inherited `align-items:center` and `margin-bottom:26px` from it — which is why the two cockpit boxes wouldn't line up. Shared utility classes (`bar`, `lvl`) also beat the new `.cd-agony-*` rules on specificity. **If something looks off, grep for every rule matching the element's classes before touching the new CSS.**
- **Source order matters.** New rules added near the top of the `<style>` block lose to the original rules further down. The clay-control block is deliberately placed *after* the chrome rules.
- **A merge race lost a commit once.** A colour change was pushed seconds before the PR merged, and the merge took the commit *before* it — `main` silently kept the old value. If a change "didn't apply", check `git log --format="%H %P"` on the merge commit to confirm what actually got merged.
- **Removing a property doesn't override a legacy class's border.** The agony card carries `class="cd-agony painchip"` for old JS click-handler compat. `.painchip` sets `border:1px solid var(--glass-border)`. When the border was first stripped from `.cd-agony` by deleting the `border` property entirely (rather than overriding it), the border stayed visible — `.cd-agony` no longer declared `border` at all, so nothing beat `.painchip`'s. Fix: explicitly set `border:none` on `.cd-agony`, don't just delete the declaration. General rule: when neutralizing a legacy-class style, override it explicitly, don't rely on "not setting the property."
- **`.side a.on`'s color is declared twice.** Once near the base `.side a` rules (~line 332, sets background too) and again later inside the clay-controls block (~line 375, sets the text-shadow/gradient/box-shadow for the "lifted segment" look). The later one wins on source order and is the one that actually renders — if a sidebar active-state color change doesn't seem to apply, you're probably only editing the first occurrence.
- Tag balance check after editing markup:
  ```bash
  python3 -c "
  c=open('index-v2.html').read()
  s=c.index('<section class=\"cockpit-deck lobbyview\"'); e=c.index('<div class=\"chainstrip lobbyview\"')
  x=c[s:e]; print(x.count('<div'),x.count('</div>'),x.count('<span'),x.count('</span>'))"
  ```

## How to preview / screenshot

`file://` fails — the page loads ES modules (three.js) that CORS blocks. Serve it:

```bash
cd /home/user/painbet && python3 -m http.server 8791   # then http://localhost:8791/index-v2.html
```

Playwright isn't in the project; use the global install and the preinstalled Chromium:

```bash
node -e "
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:1600,height:1000}, deviceScaleFactor:2});
  await p.goto('http://localhost:8791/index-v2.html');
  const el = await p.\$('.cockpit-deck');
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(1500);        // needed: content fades in, early shots come out dim
  await el.screenshot({path:'shot.png'});
  await b.close();   // don't forget, or the process hangs
})();"
```

Always `await b.close()`, and always wait ~1.5s before capturing.

## Git workflow used

One PR per change, opened as a **draft**; the user reviews screenshots (always send a screenshot and wait for explicit go-ahead before committing — this is a standing user preference, not a one-off), marks ready, and merges.

- `claude/funny-goodall-71q6b4` — PRs #161–#173, all merged. Branch is now fully merged and retired.
- `claude/optimistic-knuth-h3lvfc` — current branch. PR #174 (sidebar label font → Archivo Black) and PR #175 (label color/dots, withdrawals icon removal, borderless cockpit cards) both merged same session.

**Every PR from this branch so far has merged almost immediately after being marked ready for review**, which repeatedly orphaned the local branch mid-session. Pattern that worked both times: after a `pull_request.closed`/merged event, `git fetch origin main` then `git merge --ff-only origin/main` (safe here because the branch's own commit is always an ancestor of the merge commit — confirm with `git diff HEAD origin/main -- index-v2.html` coming back empty before relying on this) — this brings the local branch's content in sync without disturbing any uncommitted working-tree changes, then `git push origin <branch>` to sync the remote ref. Don't use `git checkout -B` for this even though it's tempting — it gets blocked by the auto-mode permission classifier as "Irreversible Local Destruction"; `merge --ff-only` accomplishes the same thing without tripping it.

If a PR merges with unmerged local commits still ahead of it (hasn't happened yet here, but per the standing instructions): restart the branch from latest `main`, rebase the unmerged commits on top, don't discard them.

## Blocked: third-party icon/asset connectors need a network policy change

Multiple attempts to source better sidebar icons than the current hand-drawn inline `<symbol>` sprite (grep `symbol id="i-` in `index-v2.html`) all hit the same wall:

- **Streamline** (MCP connector, already attached) — can search its catalog fine, but downloading actual SVG bytes fails: both a direct `curl` to `public-api.streamlinehq.com` and the `WebFetch` tool return `EGRESS_BLOCKED` / 403.
- **Icons8** (Claude Code plugin, `icons8/agent-skills` marketplace) — installs fine (`claude plugin marketplace add icons8/agent-skills && claude plugin install icons8@icons8`), but its MCP server needs `/mcp` → Authenticate in an **interactive** session, and even once authenticated its asset CDN (`mcp.icons8.com`) is likely blocked the same way.
- **better-icons** (`better-auth/better-icons`, works as a plain npm CLI via `npx better-icons search "..."` — no MCP setup needed) — its search backend calls `api.iconify.design`, confirmed blocked with a 403 at the CONNECT-tunnel level (same as Streamline).

**Root cause:** the Claude Code cloud environment's **Network access** setting was `Trusted` (an allowlist of registries like npm/PyPI/GitHub — no general icon/asset CDNs). Confirmed via `curl -sS "$HTTPS_PROXY/__agentproxy/status"`, which logs `recentRelayFailures` with the blocked host and a 403 on the CONNECT tunnel.

**Fix (account owner only):** claude.ai/code → the environment's settings (gear/edit icon on the environment) → **Network access** dropdown → switch from `Trusted` to `Full` (simplest) or `Custom` with the specific domains allowlisted (`streamlinehq.com`, `assets.streamlinehq.com`, `public-api.streamlinehq.com`, `mcp.icons8.com`, `api.icons8.com`, `api.iconify.design`). **Changes only apply to new sessions** — the session that was open while diagnosing this never picked up the change.

If this is still unresolved when picking this back up: check whether network access was widened, and if not, either nudge the user again or fall back to hand-drawing icon replacements directly in the existing inline-SVG stroke style (same viewBox 24x24, `currentColor`, `stroke-width` ~1.6–1.7 — see any existing `<symbol id="i-*">` for the pattern) rather than depending on an external asset source.

The icon concepts already agreed with the user (Option 2 mapping, Streamline "Plump Line - Free" set as reference, not necessarily verbatim once unblocked): Lobby→Home, Originals→Dice, Slots→**keep existing custom icon** (no free set had a real slot-machine glyph), Live casino→Signal/broadcast, Promotions→Gift, Pain scale→Gauge/dial, Threshold Raid→Target, PainKillers→Tablet capsule, Anesthesia→Pharmacy/medical-cross (not a water drop — no good drop icon existed in the free set checked), PainTracker→Bar graph, The Chart→User/profile, Affiliate→Share-link or hierarchy/network nodes, Triage→Chat bubble.

## Open / possible next steps

- **Sidebar icons still pending** — blocked on the network access fix above (or the hand-drawn fallback) before wiring in replacements for `i-lobby`, `i-originals`, `i-live`, `i-gift`, `i-gauge`, `i-target`, `i-pill`, `i-drop`, `i-track`, `i-user`, `i-network`, `i-chat` (grep `symbol id="i-` for exact current markup). `i-originals`'s current slot-machine-adjacent icon should stay as-is per above.
- **Promoting v2 is the user's call.** `index.html` is deliberately kept as the comparison baseline (see `CLAUDE.md`); it has the #183–#189 PainKillers/raid changes but not the cockpit deck, chrome, or the #190+ page reworks. The user will move v2 over themselves — don't do it unasked.
- The Pain Scale page is now built (`#painPage`, from `painbet-painscale-section.html`). Dropped from the old view and possibly wanted back: Booster wagering row, patient info band, per-tick Drop roll note.
- Not yet reworked: the lobby's Promotions page, PainTracker, The Chart, Arcade/Sports views. Apply the console chrome when they're redone.
- `.ambient`'s weave is mostly hidden behind opaque content; it currently only reads at the chrome's rounded corners and through the glass cards' `backdrop-filter`. If more texture is wanted, that's the layer to raise.
