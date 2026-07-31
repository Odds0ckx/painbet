<!-- Generated reference. Source of truth is index.html.
Companion docs: competitive gap audit, logic & journey spec. -->

# pain.bet — every journey, screen and state

A complete map of the built product: every view, every modal, every user journey with its branches, and every component that needs a designed state. Written to be handed to a design-system generator and to serve as the engineering reference afterwards. Tokens at the end are extracted from the live build, not invented — a new system should extend them, not replace them.

## 01 Site map

Fourteen routed views plus the lobby. Everything is a single page — views swap, they don't navigate.

| View | Route id | Reached from | Purpose |
|---|---|---|---|
| Lobby | (default) | Logo · sidebar Lobby · Casino tab | Hero, promos, game rails, proof strip, ticker |
| Sports | view-sports | Sports tab · sidebar sport links · mobile mode switch | Live/prematch markets, bet slip |
| Arcade | view-arcade | Arcade tab · promo CTA | Nine Originals in an iframe |
| Promotions | promoPage | Sidebar Promotions | Offer grid → promo detail modal |
| Pain scale | painPage | Sidebar Pain scale · pain chip | Level ladder, rates by level |
| Threshold Raid | view-synapse | Sidebar Threshold Raid · promo | Shared-pool community boss raid |
| PainKillers | view-pk | Sidebar PainKillers | Reward currency, tolerance dial |
| Anesthesia | view-anesthesia | Sidebar Anesthesia · promo | Weekly loss payback |
| PainTracker | (drawer) | Sidebar PainTracker | Session/loss analytics drawer |
| The Chart | chartPage | Sidebar The Chart · account menu | Account area — eight tabs |
| Affiliate | view-affiliate | Sidebar Affiliate | Referral programme |
| Triage | view-support | Sidebar Triage · account menu · footer | Support channels |
| Proof of reserves | proofPage | Chain cap in lobby | On-chain wallet balances |
| All games | view-originals-all / view-slots-all / view-live-all | Rail "see all" buttons | Full category grids |

## 02 Global chrome

Persistent furniture. Each has state variants that must all be designed.

| Element | Desktop | Mobile | State variants |
|---|---|---|---|
| Topbar | Logo, Casino/Sports/Arcade tabs, search, balance, auth control, Deposit | Burger, logo, balance, avatar, Deposit — tabs and search hidden | signed out signed in balance w/ bonus |
| Sidebar | Sticky rail, 4 groups with coloured dots + icons | Off-canvas drawer + scrim | casino mode sports mode active item |
| Account menu | Dropdown from avatar chip | Same, avatar only, width-clamped | closed · open |
| Bottom nav | — | Lobby / Arcade / Pain / Wallet / More | active item |
| Mode switch | — | Casino ⇄ Sports pill pair | two states |
| Email bar | Sticky under topbar, site-wide, amber | shown only when unverified |
| Lock bar | Fixed bottom, dark red, carries a withdraw action | cool-off exclusion |
| Bet slip | Right drawer | Bottom sheet | empty · slip · my bets |
| Footer | Legal text + link row | static |
| Toast | Transient confirmation, e.g. "Bet placed" | enter · exit |

> Ordering noteWhen both the email bar and the lock bar are present the page has furniture top and bottom. The lock bar wins attention — it is the more urgent state — so the email bar should visually recede while a lock is active.

## 03 Account states

A user is in exactly one. Every journey below assumes one of these as its entry condition.

```mermaid stateDiagram-v2
    [*] --> Anonymous
Anonymous --> Active: registers
Active --> VerifyPending: submits documents
VerifyPending --> Verified: approved
VerifyPending --> VerifyRejected: rejected
VerifyRejected --> VerifyPending: resubmits
Active --> CoolingOff: takes a break
CoolingOff --> Active: period expires
Active --> SelfExcluded: self-excludes
SelfExcluded --> Active: expires plus opt-in
Active --> Suspended: operator action
Active --> Closed: closes account
```

| State | Browse | Deposit | Play | Withdraw | UI signal |
|---|---|---|---|---|---|
| Anonymous | Yes | — | — | — | Sign in button |
| Active | Yes | Yes | Yes | To threshold | Avatar chip |
| VerifyPending | Yes | Yes | Yes | Queued | Amber "In review" |
| Verified | Yes | Yes | Yes | Yes | Green "Verified" |
| VerifyRejected | Yes | Yes | Yes | No | Red + reason + resubmit |
| CoolingOff | Yes | No | No | Yes | Lock bar, amber |
| SelfExcluded | Yes | No | No | Yes | Lock bar, red |
| Suspended | No | No | No | No | Contact support |
| Closed | — | — | — | — | Signed out |

## 04 Journeys — access

Getting in, and getting back in when something has gone wrong.

### J1 First visit, anonymous

- Land on lobby. Hero, promos, rails, ticker, proof strip all visible. Nothing gated.

- Browse or search. Search filters all 47 tiles live by title, category or provider. Empty-result state required.

- Tap a game. Gate returns anonymous → admissions modal opens rather than a dead end.
DecisionDemo mode is unresolved. If offered, it needs a persistent DEMO marker and must never touch balance, loyalty or history.

### J2 Register

- Choose method. Telegram (one tap) or Email. Method switcher drives which fields show.

- Fill. Email, password with live strength meter, optional referral, 18+ and terms checkbox. Submit stays disabled until valid.

- Cinematic. WebGL neuron activation plays over the form. Must degrade gracefully — the modal has to stay legible if WebGL fails.

- Success panel. Patient ID assigned, pain level 0, status ADMITTED. Seed pair committed here, before any bet is possible.

- Enter the ward. Modal closes; topbar switches to signed-in; email-confirmation bar appears.

> BranchEmail already registered → offer sign-in, without confirming the address exists.

### J3 Sign in

- Credentials or a linked provider.

- 2FA challenge if enabled — before a session is issued. Alternatives in the same dialog: backup code, or "lost both".

- Signed in. Topbar, balance and account menu update.

> BranchBackup code is consumed single-use. Six remaining after one use should be surfaced somewhere.

### J4 Password recovery

- "Forgot password?" from the sign-in tab. Prefills whatever was typed.

- Request. Email field → send.

- Sent state. Deliberately does not reveal whether the address is registered — the copy says so explicitly, so the design must give that line room.

- New password (arriving from the emailed link). Strength meter. Setting it ends all other sessions.

- Signed in.

### J5 Lost password and authenticator

- "Lost both?" from either the 2FA challenge or recovery.

- Three-step explainer — write from the account email, send ID + selfie, we reset within a day.

- Mail Triage. Deliberately slower than the normal route; the design should read as considered, not broken.

### J6 Confirm email

- Site-wide amber bar appears while unverified, on every view.

- Resend → transient "Sent — check your inbox" on the button itself.

- Confirmed → bar disappears everywhere.

## 05 Journeys — money

The most gated flows. Every one runs the gate stack first.

```mermaid flowchart TD
A[Money action] --> B{Suspended?}
B -->|Yes| X1[Contact support]
B -->|No| C{Locked?}
C -->|Yes, play or deposit| X2[Show unlock date]
C -->|No, or withdrawing| D{RG limit hit?}
D -->|Yes| X3[Limit + reset time]
D -->|No| E{Funds in right bucket?}
E -->|No| X4[Offer deposit]
E -->|Yes| F{Withdrawal?}
F -->|No| G[Execute]
F -->|Yes| H{2FA passed?}
H -->|No| X5[Challenge]
H -->|Yes| I{Past KYC threshold?}
I -->|Yes| X6[Route to verification]
I -->|No| G
```

### J7 Deposit

- Open Transfusion from the Deposit button. Three tabs: Transfusion, Discharge, Buy crypto.

- Pick a coin from seven. Each row shows balance and minimum.

- Pick a network — mandatory, never defaulted. This is the single biggest source of lost funds, so it needs the strongest treatment on the screen.

- Address + QR. Network name repeated adjacent to the address. Copy button with copied state.

- Detected → credited at one confirmation. Pending row appears in Transactions immediately with the tx hash.

> Failure states to designBelow minimum · wrong network · deposit lands while the account is locked (credit it, keep play blocked).

### J8 Buy crypto

- Amount and fiat currency (USD/EUR), live rate line.

- Coin selection → live "you get" quote.

- Partner terms checkbox gates the button.

- Hand off to the licensed third party.

### J9 Withdraw

- Discharge tab. Coin, destination address, amount. Saved addresses selectable from the address book.

- Show the arriving amount explicitly — the network fee comes out of the amount, so the net figure must be stated, not implied.

- Gate stack. Each failure routes somewhere useful: no 2FA → security settings; past threshold → verification tab; limit → shows reset time.

- 2FA challenge.

- Pending. Appears in Wallet → In flight, cancellable until signed.

- Cancel returns funds clean — out of locked, back to withdrawable, KYC counter wound back. No re-wagering penalty.

> Also designDeclined state with a reason. Queued state while verification is in review.

### J10 Verification

- Threshold meter — withdrawn to date against the cap, colour-shifting as it fills.

- Warning at 80%, before the wall rather than at it.

- Upload ID + selfie. Dashed drop targets, filled state, filename shown.

- In review — withdrawals queue rather than fail.

- Verified, or rejected with a reason and a resubmit path.

## 06 Journeys — play

### J11 Casino round

- Tile → launch. Tiles carry data-game, data-cat, data-provider. Hover shows a play affordance.

- Stake validated against balance, RG wager limit, and any Booster max-bet — blocked at entry, never punished retroactively.

- Outcome is server-authoritative.

- Settle. Winnings return to whichever bucket funded the stake. Loyalty accrues. One immutable row in Game activity.

> Design neededLoading, provider-unavailable, and disconnect-recovery states. A round in progress must never silently lose a stake.

### J12 Verify a round

- Seed panel in Security — server seed hash, nonce, editable client seed, rotate.

- Rotate reveals the previous server seed and prefills the verifier with it.

- Verifier recomputes the outcome in-browser and checks the seed against the published hash. Works with no account.

> Gap worth closingGame activity rows should each deep-link into the verifier prefilled with that round's seeds and nonce. Copying by hand is friction on the one feature that has to feel effortless.

### J13 Sports bet

- Browse live or prematch; sport filter rail.

- Tap odds → selection enters the slip; odds drift live.

- Slip — stake input, combined odds, projected payout.

- Odds change honours the user's preference: improve-only, any, or ask.

- Place → toast, balance debits, row in My bets and in Sportsbook activity.

- Settle — won / lost / void. A void leg in an accumulator recalculates rather than killing the bet.

### J14 Threshold Raid

- Live shared pool with a WebGL neuron that charges as the pool fills.

- Stake in → your share and projected payout update live; leaderboard reorders.

- Critical at 85% — visual escalation.

- Flatline at target: house-funded bounty splits by contribution share, then a fresh boss spawns.

## 07 Journeys — rewards

Four linked products. The loyalty concept is the most differentiated thing in the product and deserves the most distinctive treatment.

| Journey | Product | Mechanic | Key screen |
|---|---|---|---|
| J15 | Pain scale | Lifetime wagered drives 0→10, fractional levels, named tiers MILD→AGONY | Ladder + rates-by-level table + ECG vitals card |
| J16 | Relief | Rakeback 1→9% per level, pays per bet, no wagering | Live drip line |
| J17 | Anesthesia | 0→10% of weekly net loss, paid Monday 00:00 UTC, no wagering | Weekly payback card |
| J18 | PainKillers | 8→42 PK per 100 USDT wagered, never expires, tolerance-dial streak multiplier | Dial + wallet + live feed |
| J19 | Affiliate | 0.5% of referred wager, live stats, payout to wallet | Link row, stat grid, commission table |

> UnresolvedPainKillers accrue but have nothing to spend them on. A currency that only accumulates is not a currency — the redemption surface does not exist yet and will need designing.

## 08 Journeys — account

The Chart, eight tabs. Deep-linkable from the account menu.

| Tab | Contains | Notable states |
|---|---|---|
| Profile | Details (edit/save), linked accounts, data export, close account | view ⇄ edit · linked ⇄ unlinked · close blocked while funds remain |
| Security | Password change, reset link, 2FA, provably-fair seeds, active sessions | 2FA on/off · enrolment 2 steps · current vs other device |
| Verification | KYC tiers, threshold meter, uploads | unverified · in review · verified · rejected |
| Preferences | Notifications, display, betting defaults, Boosters | toggle on/off/locked · empty Booster state |
| Limits & breaks | Limits grid, session reminder, cool-off, self-exclusion | pending increase · limit active · danger zone |
| Wallet | In-flight withdrawals, address book, transactions | pending · declined · empty address book |
| Activity | Game rounds, sportsbook bets | win/loss/pending pills · empty state |
| Referral | Link, stats, commission table, payout | copied state · unpaid balance |

## 09 Journeys — safety

Licence-required. These need to feel like considered features, not compliance furniture — that framing is a deliberate brand position.

### J20 Set a limit

- Grid — deposit / loss / wager × daily / weekly / monthly.

- Save. Decreases apply instantly; increases queue for 24 hours.

- Pending banner lists queued increases with the effective time and a cancel action, while the old limit still holds.

- Limit reached → the action is blocked with the reset time, wherever it was attempted.

### J21 Take a break / self-exclude

- Choose duration. Break: 24h/7d/30d. Exclusion: 6mo/1yr/permanent, in a visually distinct danger zone.

- Confirm — twice for exclusion, because it is irreversible.

- Locked. Fixed bar appears site-wide with the unlock date and a withdraw action.

- Play and deposit blocked everywhere; withdrawal stays open throughout.

### J22 Reality check

- Set an interval — off / 15 / 30 / 60 minutes.

- Fires with elapsed time, net position, wagered, balance. Net is colour-coded up or down.

- Continue or take a break — the second routes straight to the break controls.

### J23 Support

- Triage — four channels with response-time expectations: live chat, Telegram, Discord, email.

- Chat modal with agent/user message states.

> GapNo ticket history or escalation path. A user with an ongoing issue has nowhere to see it.

## 10 Modal inventory

Fifteen. Each needs enter/exit, backdrop, close affordance, mobile treatment (most become bottom sheets), and its own internal states.

| Modal | Trigger | Internal states |
|---|---|---|
| Admissions | Sign in · hero CTA · gated tile | register ⇄ sign in · method switch · telegram flow · wallet list · success |
| Auth cinematic | Behind admissions on submit | idle · pulse · activation · mark |
| Recovery | Forgot password · lost 2FA | 4 steps: request · sent · new password · lost-both |
| Login 2FA | Sign-in with 2FA on | code · backup-code · error |
| 2FA enrolment | Security toggle | QR + key + confirm · backup codes |
| 2FA challenge | Withdrawal | code · error |
| Transfusion | Deposit button · lock bar | 3 tabs · coin list · coin detail · network select |
| Connect wallet | Wallet link options | list · searching · connecting |
| Provably fair | Footer · seed panel | empty · result · commitment ok/mismatch · how-it-works |
| Reality check | Session timer | single, with net up/down |
| Promo detail | Promo card | art · rules · CTA routing |
| Legal | Footer links | 4 panes: terms · privacy · AML · responsible gaming |
| Chat | Triage · footer | log · agent msg · user msg · input |
| Providers | Provider marquee | grid |
| Game launch | Any tile | loading · error · demo — seam, not yet designed |

## 11 Component inventory

Everything that needs a spec. Grouped by kind.

| Group | Components |
|---|---|
| Actions | Primary (red) · secondary (outline) · ghost · danger · chip/pill button · icon button · toggle switch · segmented control · tab · copy-to-clipboard · file drop |
| Inputs | Text · email · password (+ strength meter) · number · search · select · checkbox · radio · file · code entry (6-digit, letter-spaced) · address field · amount field with unit |
| Surfaces | Card (pscard) · glass panel (blk) · promo card · game tile · stat tile · band/callout · inset well · dashed empty state |
| Data | Table (+ sticky header, right-aligned numerics) · leaderboard row · transaction row · activity row · key-value row · meter/progress bar · dial · sparkline/ECG · ticker · marquee |
| Status | Pill (win/loss/pending/deposit/withdrawal/confirmed) · badge (tier) · severity chip · toast · inline note (info/error/success) · banner (email/lock) · live dot |
| Navigation | Topbar · sidebar group + item · account menu · tab bar · bottom nav · mode switch · breadcrumb · rail scroller · "see all" |
| Overlays | Modal · bottom sheet · drawer (bet slip, tracker) · scrim · dropdown · tooltip |
| Domain | Odds button (+ drift up/down) · bet slip row · coin row · network selector · seed row · limit grid row · KYC threshold meter · pain-level ladder · raid stage |

## 12 Interaction states

The matrix a design system has to cover. Missing states are where implementations diverge.

| State | Applies to | Requirement |
|---|---|---|
| default | all | — |
| hover | interactive | Pointer only — must not stick on touch |
| active / pressed | buttons, tiles | Distinct from hover |
| focus-visible | all interactive | Keyboard only, never suppressed |
| selected / on | tabs, toggles, odds, chips | Distinguishable without colour alone |
| disabled | buttons, inputs | Plus a reason nearby where the cause isn't obvious |
| loading | async actions | Missing throughout the current build |
| error | inputs, forms | Message states the fix, not just the fault |
| success | forms, copy | Transient, self-clearing |
| empty | tables, lists, search | Says what would fill it |
| locked | play, deposit | Reason + unlock time + a route onward |
| skeleton | rails, tables | Not yet designed |

> MotionAll ambient motion (ticker, EKG, liquid, marquee, neuron) plays regardless of
OS reduce-motion by explicit client direction. Functional motion — modal enter, drawer slide, toast — should still respect prefers-reduced-motion. Keep those two categories separate in the system.

## 13 Breakpoints

Currently ad hoc — twelve distinct widths in use. A system should consolidate to four or five and say what changes at each.

| Width | In use | What changes |
|---|---|---|
| ≤1100 | 3× | Support grid 4→2 |
| ≤960 | 5× | Chart grid collapses |
| ≤900 | 11× | Primary break — sidebar → drawer, bottom nav appears, topbar sheds tabs and search, mode switch appears |
| ≤820 / 760 / 700 | 6× | Various two-column collapses |
| ≤640 / 600 | 14× | Secondary break — rails to 2-up, padding reduces, tables scroll |
| ≤420 | 2× | Smallest adjustments |

## 14 Existing tokens

Extracted from the live build. A new system should absorb these rather than start over — the red and the morphine blue in particular carry brand meaning.

### Colour

| Token | Value | Meaning |
|---|---|---|
| --blood | #e0163c | Arterial red. Pain, action, primary CTA. The brand colour |
| --redhi | #ff2450 | Hover/emphasis red |
| --red-deep | #8f0e26 | Gradient anchor, triangles |
| --blue | #7FD6E8 | Morphine blue. Money coming back — relief, cashback, payouts. Never used for action |
| --bg | #07080a | Page ground |
| --glass | rgba(15,17,22,.70) | Card surface, with blur |
| --glass-border | rgba(255,255,255,.10) | Hairline |
| --ink | #e8eaee | Primary text |
| --ink-dim | #9aa0aa | Secondary text |
| --veil | rgba(0,0,0,.42) | Backdrop |

Semantic colours are additionally in use but untokenised — success #3ecf6a, warning #e0a13e, danger reuses --blood. These should become proper tokens.

### Type

| Token | Stack | Role |
|---|---|---|
| --disp | 'Archivo Black', Archivo, sans-serif | Display — headings, uppercase, tight |
| --sans | 'Inter', system-ui | Body |
| --mono | 'JetBrains Mono', 'SF Mono' | Carries the clinical voice — labels, data, IDs, amounts. Heavily letter-spaced and uppercased for labels |

### Shape, depth, motion

| Token | Value |
|---|---|
| --r-sm / --r-md / --r-lg / --r-pill | 8px · 12px · 16–18px · 999px |
| --tile-r | 18px |
| --shadow | 0 10px 28px rgba(0,0,0,.35) |
| --shadow-lg | 0 18px 44px rgba(0,0,0,.5) |
| --ease-out | cubic-bezier(.22,1,.36,1) |
| --nav-w | 240px (sidebar 220px in shell grid) |

> Known inconsistencies to resolve
--red is defined twice with different values (#E10600 in one scope, var(--blood) in another) and --r-lg is both 16px and 18px depending on scope.
--card, --card-2, --card-hi overlap with --glass.
Consolidating these is one of the more useful things a design system pass can do.

pain.bet · journey & UI reference v1 · companion to the gap audit and the logic spec
