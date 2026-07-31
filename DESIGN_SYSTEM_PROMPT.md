# Prompt — generate the pain.bet design system

Paste the block below into the Claude session that has your design-system skill.

**Before you send it:** replace `<SKILL>` on the first line with your skill's actual
name (e.g. `/design-system`). If the skill isn't a slash command, replace that line
with `Use the <SKILL> skill for this.`

The session needs access to this repo so it can read `USER_JOURNEYS.md` and
`index.html`. If it can't, paste the contents of `USER_JOURNEYS.md` in place of the
line that references it.

---

```
/<SKILL>

Build the complete design system for pain.bet, a crypto casino and sportsbook.

## Read first

- `USER_JOURNEYS.md` — the complete map of every view, modal, journey, component,
  interaction state, breakpoint and existing token. This is your specification;
  cover everything in it.
- `index.html` — the live single-file build. Ground the system in what actually
  exists. Where the doc and the code disagree, the code wins — say so in the output.

## What this is for

Engineers are wiring a real backend into a built front end. They need one reference
that answers "what does this component look like in this state, at this width" without
reading the source. Designers need it to extend the product without drifting.

Treat it as documentation of a real system, not a moodboard.

## The brand, so you extend rather than replace it

pain.bet is a clinical / medical-horror casino. Patients, not players. Wards, charts,
admissions, discharge, anaesthesia. The tone is deadpan and precise, never jokey.

Two colours carry meaning and must not be used interchangeably:

- **Arterial red `#e0163c`** — pain, risk, action. Every primary CTA.
- **Morphine blue `#7FD6E8`** — money coming back. Rakeback, cashback, payouts,
  proof. Never used for an action.

Monospace carries the clinical voice: labels, IDs, amounts, timestamps, all
uppercase and letter-spaced. Display face is heavy condensed uppercase. Body is
plain sans.

Existing tokens are listed at the end of `USER_JOURNEYS.md`, including several known
inconsistencies (`--red` defined twice with different values, `--r-lg` both 16 and
18px, `--card`/`--glass` overlapping). Resolve those and say what you resolved and why.

## What the system must contain

**1. Foundations**
Colour — brand, semantic (success/warning/danger/info), surface, text, border — each
with a stated role and contrast ratio against its intended background. Flag anything
under 4.5:1 for body text. Type scale with weights, sizes, line heights, letter
spacing, and which face each step uses. Spacing scale. Radii. Elevation. Motion:
durations and easings, and the rule that ambient motion (ticker, EKG, marquee,
neuron) ignores `prefers-reduced-motion` by client direction while functional motion
(modals, drawers, toasts) respects it.

**2. Every component in the inventory** (§11 of the doc), each with:
- Anatomy and a visual spec
- All variants
- **Every applicable interaction state**: default, hover, active, focus-visible,
  selected, disabled, loading, error, success, empty. §12 lists which apply where.
  Loading and skeleton states are missing from the current build — design them.
- Desktop and mobile rendering
- Do / don't guidance where misuse is likely

**3. Every modal** (§10 — there are fifteen). Enter and exit, backdrop, close
affordances, internal states, and the mobile treatment. Most should become bottom
sheets under 900px — decide and document which.

**4. Navigation and layout**
Topbar in signed-out and signed-in states. Sidebar with its four grouped sections,
casino and sports modes, and its mobile drawer. Account menu. The eight-tab account
area. Bottom nav, mode switch, bet slip drawer. Grid and container widths.

**5. Flows**
Render each journey in §04–§09 as a visual flow — screens, decision points, failure
branches. Show the gate stack (§05) as a diagram, since every money action passes
through it. Include the states where a user is blocked, because those need as much
design attention as the happy path: locked account, limit reached, verification
required, insufficient balance.

**6. Responsive**
Consolidate the twelve ad hoc breakpoints currently in use down to four or five.
State what changes at each. The primary break is 900px (sidebar becomes a drawer,
bottom nav appears, topbar sheds tabs and search).

**7. Content and voice**
Button labels, empty states, error messages, confirmations. Errors say what went
wrong and how to fix it. Destructive and irreversible actions (self-exclusion,
account closure) get their own pattern with double confirmation.

## Deliverable

A single self-contained HTML page with:
- Sticky sidebar navigation between sections
- Live rendered examples of every component in every state — real markup, not
  screenshots — so a developer can inspect them
- Copyable code for each component
- A token table with swatches and values
- Light and dark rendering (the product is dark; the documentation should be readable
  in both)
- Responsive down to 390px

Include a short "open questions" section at the end for anything the source left
genuinely ambiguous. Don't invent an answer to a business decision — flag it.

Prioritise completeness and accuracy over decoration. This is a reference document.
```
