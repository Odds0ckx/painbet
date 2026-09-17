# index-v2.html — Session Handoff

_Last updated: 2026-09-17. Hand this file to a new chat to continue the `index-v2.html` lobby experiment with full context._

Read `HANDOFF.md` first for the overall project (brand rules, token system, how `index.html` is structured). This file only covers the **`index-v2.html`** workstream.

## What `index-v2.html` is

A **full copy of `index.html`** created as a layout sandbox for redesigning the lobby's "cockpit deck" area and, more recently, the site chrome. `index.html` itself is **untouched** — nothing here has been promoted to the live site yet.

- **Repo:** `Odds0ckx/painbet` · **Default branch:** `main`
- **Working branch:** `claude/funny-goodall-71q6b4`
- **Live-ish preview:** `https://github.com/Odds0ckx/painbet/blob/main/index-v2.html` (GitHub only shows source — download the raw file and open it locally to actually see it render)
- Also in this workstream: `concept-cockpit-deck.html` — a small standalone page that was the first layout test for the two cockpit boxes. Superseded by `index-v2.html`; kept for reference.

## What's been built (in order)

1. **Cockpit deck** — the old full-width "Lightning fast withdrawals" banner and the thin "AGONY" progress strip were merged into one side-by-side section (`.cockpit-deck`, a `7fr 5fr` grid that stacks under 900px).
2. **Withdrawals card** (`.cd-with`) — keeps the site's animated lightning bolt; its three stat tiles were rebuilt as **vault-terminal screens**.
3. **Terminal tiles** (`.cd-term` + `.cd-term-screen`) — frame/screen split: `.cd-term` is a beveled gradient frame, `.cd-term-screen` is the CRT glass (radial gradient, dot-matrix texture, scanlines, vignette). Values glitch via `.term-glitch`.
4. **Agony card** (`.cd-agony`) — header, a syringe/dosimeter gauge, tier labels, a centered "next reward" line, and a loss-buffer readout.
5. **Agony bar** (`.cd-agony-bar`) — sub-tick hashes `.1`–`.9`, red major tick at `.5`, white current tick + plunger-stopper line at the fill edge, glass sheen.
6. **Font** — JetBrains Mono replaced site-wide by the Google font **Huninn** (via the `--mono` token, so it's a one-line swap).
7. **Chrome** (`.topbar`, `.side`) — borderless "dashboard console" panels with clay/embossed controls.

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

Work on `claude/funny-goodall-71q6b4`, one PR per change, opened as a **draft**; the user reviews screenshots, marks ready, and merges. PRs #161–#172 cover everything above, all merged.

After each merge, `git fetch origin main && git merge --ff-only origin/main` before starting the next change. If the branch has already-merged commits and main used a merge commit, `git rebase origin/main` then `git push --force-with-lease`.

## Open / possible next steps

- **Nothing is wired into the live site.** `index.html` still has the old banner + `.painchip` strip. Promoting this means porting the cockpit deck + chrome changes into `index.html` (or renaming `index-v2.html` over it), which nobody has agreed to yet — ask first.
- The bigger **"PAIN SCALE / WARD IV"** full-page mockup the user shared (patient dossier, dosage table, "what the climb buys" cards) was only mined for its gauge. The rest of that page is unbuilt.
- `.ambient`'s weave is mostly hidden behind opaque content; it currently only reads at the chrome's rounded corners and through the glass cards' `backdrop-filter`. If more texture is wanted, that's the layer to raise.
