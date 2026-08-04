# Daily wheel plate — artwork spec

Describes `assets/wheel/plate.webp` and how the page maps prizes onto it. The
page draws the prize labels itself in canvas (`drawWheel` in
`painbet-intake-scroll.html`), so **the plate carries wedges and dividers
only, no text.**

## Ten prizes, fourteen wedges

The plate is painted with **14 wedges**. `WHEEL` holds **10 prizes**. Those are
deliberately different things:

- `WHEEL` — the ten prizes. This is what the published odds list and the result
  line talk about.
- `WEDGES` — the fourteen painted wedges, each pointing at a prize.

Prizes that appear on more than one wedge have their probability split evenly
between them, so **every prize's published odds are unchanged**. `+1 entry` is
still 30%; it is simply reachable via two wedges at 15% each.

The code used to step 36° (360/10) across artwork drawn on a 25.714° pitch
(360/14), so the wedge that stopped under the pointer was never the one that
had actually been won. That is fixed — `rollWheel()` now returns a *wedge*, and
its prize is `WHEEL[WEDGES[i].prize]`.

## Geometry

Canvas 2048 × 2048, transparent background, centre at (1024, 1024). `r/R` is
the fraction of the 1024 half-width the code works in.

| Feature | r/R | px |
|---|---|---|
| Painted band, inner edge | 0.455 | 466 |
| Painted band, outer edge | 0.759 | 777 |
| Steel rim + saw teeth | 0.759 → 1.000 | 777 → 1024 |

**Pitch 25.714° (360/14).** Wedge 0's centre is painted **12.59° clockwise of
12 o'clock** — fitted across all fourteen measured centres. The art is
hand-made and regular to within 2.4° on a ~22° wedge, which is well inside
tolerance. That figure is `PLATE_PHASE` in the page; labels are placed from it
and `spinWheelTo` subtracts it so a win stops dead under the pointer.

It cannot be folded into the canvas rotation that draws the plate and the
labels together — that turns both and cancels out.

## Wedges

Clockwise from 12 o'clock. Fills are sampled off the plate. Text colour is what
the code uses on that wedge, listed so contrast can be checked, not painted in.

| # | Centre | Fill | Text | Line 1 | Line 2 | This wedge | Prize total |
|---|---|---|---|---|---|---|---|
| 0 | 12.6° | `#F7F6F2` white | `#14100D` | **+1** | ENTRY | 15.000% | 30.000% |
| 1 | 38.3° | `#28282D` black | `#F7F8F8` | **NOTHING** | — | 43.738% | 43.738% |
| 2 | 64.0° | `#B90A12` red | `#F7F8F8` | **1,000** | PK | 1.000% | 1.000% |
| 3 | 89.7° | `#1061A3` blue | `#F7F8F8` | **$10** | USDT | 0.025% | 0.050% |
| 4 | 115.4° | `#1061A3` blue | `#F7F8F8` | **$500** | USDT | 0.002% | 0.002% |
| 5 | 141.2° | `#F7F6F2` white | `#14100D` | **+2** | ENTRIES | 7.500% | 15.000% |
| 6 | 166.9° | `#28282D` black | `#F7F8F8` | **500** | PK | 2.000% | 2.000% |
| 7 | 192.6° | `#1061A3` blue | `#F7F8F8` | **$50** | USDT | 0.005% | 0.010% |
| 8 | 218.3° | `#F7F6F2` white | `#14100D` | **+5** | ENTRIES | 8.000% | 8.000% |
| 9 | 244.0° | `#B90A12` red | `#F7F8F8` | **5,000** | PK | 0.200% | 0.200% |
| 10 | 269.7° | `#1061A3` blue | `#F7F8F8` | **$10** | USDT | 0.025% | 0.050% |
| 11 | 295.4° | `#F7F6F2` white | `#14100D` | **+1** | ENTRY | 15.000% | 30.000% |
| 12 | 321.2° | `#F7F6F2` white | `#14100D` | **+2** | ENTRIES | 7.500% | 15.000% |
| 13 | 346.9° | `#1061A3` blue | `#F7F8F8` | **$50** | USDT | 0.005% | 0.010% |

Wedge shares total 100.000%, and each prize's shares sum to its own published
figure. Both are asserted against `WHEEL` at runtime.

Colour follows prize type: **white = entries, blue = cash (USDT), red = PK,
black = nothing** — with one exception. The plate came back a red short of the
split the brief asked for, so `500 PK` sits on the second black wedge. If the
plate is ever repainted, make wedge 6 red and the convention is clean.

## Labels (drawn in code, not painted)

JetBrains Mono Bold, radially along each spoke, reading outward-in, on two
lines — value over unit, unit at 70% of the value's size. They occupy
`r/R 0.485 → 0.735` (497px → 753px) and auto-fit to the wedge, so they need
clear paint across that span. Wedges on the left half are turned 180° so every
label reads left-to-right.

## If anything changes

Keep these three in step, all in `painbet-intake-scroll.html`:

- `WHEEL` — the prizes and their published odds
- `WEDGES` — which prize each painted wedge points at, and that wedge's share
- `WEDGE_BG` — the painted colour of each wedge, used to pick the text colour

If the plate is repainted at a different wedge count, `WEDGES` and `WEDGE_BG`
both change length and `PLATE_PHASE` needs re-measuring. `rollWheel()` sums by
probability rather than index, so wedge order can be rearranged freely as long
as each prize's shares still add up to its `WHEEL` probability.
