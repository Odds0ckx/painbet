---
name: html-to-figma-export
description: Prepare a standalone HTML file so it imports cleanly into Figma via an HTML-to-Figma plugin (html.to.design and similar). Use this whenever the user wants to export/import a component, modal, popup, form, or page into Figma from HTML, OR reports that an import "comes up blank", only shows the background, or drops part of the layout (e.g. a modal/popup subtree missing while surrounding text imported fine).
---

# HTML → Figma import (making a file import cleanly)

HTML-to-Figma plugins render your HTML in a headless sandbox and convert the
DOM into Figma layers. They are much dumber than a real browser and silently
drop content that a browser renders fine. When an import comes up blank or
missing a chunk, it is almost never a broken layout — it is one of the traps
below. A file can render perfectly in a browser (and in Playwright) and still
import blank.

## The #1 cause: overlay / popup detection (rename "modal" classes)

**This is the trap that bit pain.bet and the one to check first.** These
plugins have built-in heuristics that intentionally SKIP elements whose
class, id, or role signals a hidden overlay — because on a live page those
are pop-ups the tool shouldn't capture. Trigger words include:

`modal`, `popup`, `dialog`, `overlay`, `drawer`, `sheet`, `tooltip`,
`dropdown`, `lightbox`, `backdrop`, and `role="dialog"` / `aria-modal`.

Symptom: text/elements OUTSIDE the overlay import fine, but everything
INSIDE the `.modal` (and its children `.mhead`/`.mtabs`/`.mbody` etc.) is
discarded wholesale.

**Fix:** rename every overlay-flavored class/id to a neutral name and remove
`role="dialog"`/`aria-modal`. Use `card`, `panel`, `sheet`→`board`,
`card-head`, `card-body`, `tabs`, etc. Nothing in the markup should read as
"popup."

| Avoid            | Use instead        |
|------------------|--------------------|
| `.modal`         | `.card` / `.panel` |
| `.mhead`         | `.card-head`       |
| `.mbody`         | `.card-body`       |
| `.mtabs`         | `.tabs`            |
| `role="dialog"`  | (remove it)        |

## Other real causes (check in this order)

1. **`display:none` content is never imported.** Anything hidden
   (`display:none`, `visibility:hidden`, `opacity:0`) is skipped — the
   plugin does not run your JS to reveal tabs/panels. Lay every state out
   **statically and visibly**. For a multi-state UI (e.g. Register / Login /
   Wallet tabs), render each state as its own visible card stacked on the
   page instead of one card with hidden panels.

2. **Native `<input>` / `<button>` can abort a subtree.** Some importers
   choke on form controls and discard the containing subtree. If renaming
   classes isn't enough, replace `<input>` with a styled `<div>` showing the
   placeholder text, and `<button>` with a `<div>`. (Interactivity doesn't
   translate to Figma anyway.) Note: this is NOT always needed — the
   paintracker file uses native buttons and imports fine — so try the
   class-rename first and only strip controls if content still drops.

3. **Full-viewport flex centering can misplace/drop a single child.**
   `body{min-height:100vh; display:flex; align-items:center; justify-content:center}`
   with one centered child sometimes lands off-frame or gets pruned. Prefer
   normal block flow (`body{padding:40px}`) with content at the top-left.

4. **External resources (fonts).** An external Google Fonts `<link>` usually
   still imports (text falls back), but if glyphs vanish, install the fonts
   in Figma or inline them. Fonts affect glyph rendering, not layer
   structure — they are not why nodes get dropped.

## Reference that imports cleanly

`painbet-paintracker.html` at the repo root imports flawlessly. It uses
external Google Fonts, CSS custom properties, native `<button>`s, and flex
centering — proving none of those break import. Its one distinguishing trait
is a neutral top-level container class (`.app`, not `.modal`). When in doubt,
mirror its conventions.

## Checklist before handing a file off for import

- [ ] No class/id/role contains modal/popup/dialog/overlay/drawer/sheet/tooltip/dropdown
- [ ] Every state/tab/panel is statically visible (no `display:none`)
- [ ] Content is in normal flow (not a single viewport-centered child)
- [ ] If still dropping: replace `<input>`/`<button>` with styled `<div>`s
- [ ] Verify it renders in Playwright, then hand off — but remember a clean
      browser render does NOT guarantee a clean import; the traps above are
      import-only

## Fallback: build natively in Figma

If a file still imports badly after all of the above, stop fighting the
plugin and build the design natively with the Figma MCP integration
(`use_figma` — load `/figma-use` first) or export a flat SVG/PNG for
pixel-perfect (non-editable) placement.
