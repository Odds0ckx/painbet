# Daily wheel plate — artwork spec

Source of truth for redrawing `assets/wheel/plate.webp`. The page draws the
prize labels itself in canvas (`drawWheel` in `painbet-intake-scroll.html`),
so **the plate should be painted with wedges and dividers only, no text.**

## The problem this fixes

The current plate is painted with **14 wedges**. `WHEEL` holds **10 prizes**,
and the code steps in 36° increments. Measured off the current art, the paint
sits on a 25.7° pitch (360/14), so labels drift across dividers and the pointer
never lands mid-wedge. The band has to be repainted at ten.

## Geometry

Canvas 2048 × 2048, transparent background, centre at (1024, 1024).
Radii below are px from centre; `r/R` is the fraction of the 1024 half-width
the code works in.

| Feature | r/R | px |
|---|---|---|
| Hub / steel centre disc, outer edge | 0.455 | 466 |
| Painted band, inner edge | 0.455 | 466 |
| Painted band, outer edge | 0.759 | 777 |
| Steel rim + saw teeth | 0.759 → 1.000 | 777 → 1024 |

Keep the existing hub, rim and teeth exactly as they are — only the painted
band between 466px and 777px changes.

**Ten wedges, 36.0° pitch.** Wedge `i` is **centred at `i × 36°` measured
clockwise from 12 o'clock**, so wedge 0 is centred straight up under the
pointer. Paint each wedge ~31° wide, leaving a ~5° steel divider slot between
them (matches the proportion on the current art).

## Wedges

Fill colours are sampled from the existing plate so the repaint keeps the same
palette. Text colour is what the code uses for that wedge — it is listed so the
contrast can be checked, not so it can be painted in.

| # | Centre (CW from 12) | Fill | Text | Line 1 | Line 2 | Odds |
|---|---|---|---|---|---|---|
| 0 | 0° | `#F7F6F2` white | `#14100D` | **+2** | ENTRIES | 15.000% |
| 1 | 36° | `#28282D` black | `#F7F8F8` | **NOTHING** | — | 43.738% |
| 2 | 72° | `#B90A12` red | `#F7F8F8` | **1,000** | PK | 1.000% |
| 3 | 108° | `#1061A3` blue | `#F7F8F8` | **$500** | USDT | 0.002% |
| 4 | 144° | `#F7F6F2` white | `#14100D` | **+1** | ENTRY | 30.000% |
| 5 | 180° | `#28282D` black | `#F7F8F8` | **500** | PK | 2.000% |
| 6 | 216° | `#1061A3` blue | `#F7F8F8` | **$50** | USDT | 0.010% |
| 7 | 252° | `#B90A12` red | `#F7F8F8` | **5,000** | PK | 0.200% |
| 8 | 288° | `#F7F6F2` white | `#14100D` | **+5** | ENTRIES | 8.000% |
| 9 | 324° | `#1061A3` blue | `#F7F8F8` | **$10** | USDT | 0.050% |

Odds total 100.000%. `Nothing` is the remainder and is computed at runtime, not
stored — the other nine are fixed in the `WHEEL` array.

Colour follows prize type, per the existing convention: **white = entries,
blue = cash (USDT), red = PK, black = nothing.** Wedge 5 is the one exception,
a PK prize on black, because the plate came back one red short of the split the
brief asked for. If the repaint corrects that, make wedge 5 red and update
`WEDGE_BG` in the page to match.

## Labels (drawn in code, not painted)

Set in JetBrains Mono Bold, radially along each spoke, reading outward-in, on
two lines — value over unit, unit at 70% of the value's size. They occupy
`r/R 0.485 → 0.735` (497px → 753px) and auto-fit to the wedge, so they need
clear paint across that whole span.

Wedges on the left half are turned 180° so every label reads left-to-right.

## If the wedge order changes

`WEDGE_BG` in `painbet-intake-scroll.html` lists the fill colour per wedge and
must be kept in step with the paint. Prize order and odds live in the `WHEEL`
array in the same file; `rollWheel()` sums by probability rather than index, so
the order can be rearranged without touching the odds.
