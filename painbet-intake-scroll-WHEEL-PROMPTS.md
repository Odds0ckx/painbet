# THE INTAKE · daily pain wheel, image prompts (v1)

Prompts for generating a **PNG replacement for the canvas wheel** in
`painbet-intake-scroll.html`, Room 08 / DISPENSARY.

Palette is locked to four values. Nothing else enters frame.

| Role | Hex | Used for |
|---|---|---|
| Arterial red | `#E10600` | pain, action, house currency (PK), the perk |
| Morphine blue | `#7FD6E8` | money, and only money |
| White | `#F7F8F8` | entries, chart paper, hairlines |
| Black | `#131517` | ground, the Nothing wedge |

Neutral greys are allowed **only** as straight black-to-white mixes for edge
work and wear. No warm greys, no blue-greys, no gold, no green, no purple.
The current canvas wheel uses gold, green and purple for prize tiers, so that
colour coding is being retired. The replacement mapping is in section 2.

---

## 0. READ THIS FIRST: generate the plate, not the labels

The wheel is a spinning element. `spinWheelTo()` rotates it 6 full turns and
lands the centre of a weighted segment under a fixed pointer at 12 o'clock.
Two consequences that decide which prompt you use:

**1. Do not bake the ten prize labels into the image.** No generator places ten
short strings around a disc at exact 36 degree intervals without mangling at
least three of them, and the prize table is still moving (odds, amounts and
segment order have all changed once already). Generate the **plate**, keep the
labels in canvas where they stay correct and stay editable. Section 3 is the
plate prompt and it is the one to use.

**2. Do not bake in directional light.** A specular hotspot or a drop shadow
painted at the top of the disc will spin with the disc and read as broken. Ask
for flat, even, frontal light. The page already adds the shadow in CSS
(`.wheelwrap canvas { filter: drop-shadow(...) }`).

Section 6 has a full-face prompt with labels for anyone who wants to try it
anyway, and section 7 is the cheap version: a bezel ring that frames the
existing canvas wheel and changes nothing else.

---

## 1. GEOMETRY SPEC (the same in every prompt)

- Square canvas, **2048 x 2048**, disc centred, **transparent** outside the rim.
- Disc fills **97%** of the frame width. It renders at 280 CSS px, so nothing
  thinner than about 7 image px survives. No hairlines under 8 px.
- **Exactly ten identical wedges, 36 degrees each**, ten radial dividers,
  perfect rotational symmetry.
- A **wedge centre sits at 12 o'clock**, dividers 18 degrees either side. This
  matters only if labels are baked in, but keep it true so the plate can be
  checked against a screenshot.
- **Hub**: circle at 12% of the disc radius, black, thin red ring.
- **No pointer, no pin, no stand, no base, no arrow.** The pointer is a
  separate DOM element that must not rotate with the plate.

---

## 2. WEDGE COLOUR MAPPING

Index order matches the `WHEEL` array in `painbet-intake-scroll.html`, running
**clockwise from 3 o'clock**.

| # | Prize | Kind | Wedge | Label ink |
|---|---|---|---|---|
| 0 | 500 USDT | jack | morphine blue, full strength, thin white inner glow ring | black |
| 1 | +2 entries | ent | white | black |
| 2 | 50 USDT | cash | morphine blue at ~60% over black | black |
| 3 | +1 entry | ent | white | black |
| 4 | 1,000 PK | pk | arterial red | white |
| 5 | Nothing | none | black | 40% white |
| 6 | 10 USDT | cash | morphine blue at ~60% over black | black |
| 7 | +5 entries | ent | white | black |
| 8 | 5,000 PK | pk | arterial red | white |
| 9 | Pain Scale +1 | perk | arterial red, outline only, black fill | red |

Blue is money, red is the house, white is a chart entry, black is nothing. That
holds the brand rule (`morphine blue = money back only, never risk`) without
needing a fifth colour.

Two reds land next to each other at 8 and 9. Making index 9 an outline wedge
instead of a solid separates them, which is why it is drawn that way. If you
would rather have clean alternation, the `WHEEL` array can be reordered freely:
`rollWheel()` walks cumulative probability so order does not affect odds, and
the published odds list sorts itself.

---

## 3. THE PLATE (recommended)

Three art directions. Same geometry, same palette, different surface. **A** is
the default. Generate square, 1:1.

### 3A. ENAMEL DIAL

```
A flat top-down product photograph of a circular ten-segment dial plate from a
1960s anaesthesia machine, shot straight on, perfectly centred, filling the
frame. The disc is divided into exactly ten identical wedge segments of thirty
six degrees each by ten straight radial dividers of even weight, in perfect
rotational symmetry. The segments are vitreous enamel in only four colours,
arranged in this order clockwise: pale surgical blue, chalk white, pale
surgical blue, chalk white, deep arterial red, matte black, pale surgical blue,
chalk white, deep arterial red, matte black with a red enamel outline. The
enamel is chipped and hairline crazed at the segment edges with bare steel
showing through in places, faint chemical staining, decades of handling.
Encircling the whole plate is a machined steel bezel ring, brushed and scuffed,
with a thin arterial red inner line. At the exact centre is a small black
circular hub cap with a thin red ring and a small red equilateral triangle
embossed on it. Flat even frontal studio lighting, completely uniform across
the disc, no hotspot, no directional shadow, no vignette. Transparent
background outside the bezel. Absolutely no text, no numbers, no letters, no
markings inside the segments, no pointer, no arrow, no stand.
Avoid: words, letterforms, numerals, watermark, logos, pointer, arrow, needle,
stand, base, tripod, hand, drop shadow, cast shadow, specular highlight,
gradient background, perspective, tilt, angled view, gold, yellow, green,
purple, orange, brown, teal, warm tones, more than four colours, uneven
segments, nine segments, eleven segments, decorative flourishes, gemstones,
casino glitz.
```

### 3B. STENCILLED STEEL

```
A flat top-down photograph of a heavy circular steel plate divided into exactly
ten identical wedge segments of thirty six degrees each by ten deep sandblasted
radial grooves, perfect rotational symmetry, filling the frame, shot straight
on and perfectly centred. Each segment is painted with thick stencil-applied
industrial paint in only four colours, arranged in this order clockwise: pale
surgical blue, chalk white, pale surgical blue, chalk white, arterial red, bare
dark steel, pale surgical blue, chalk white, arterial red, bare dark steel with
a sprayed red border. The paint is worn thin at the outer edge, scuffed and
scratched down to grey metal in the traffic areas, overspray bleeding slightly
past the stencil lines. A thick raw steel rim runs around the outside with
eight countersunk bolts set into it. At the centre is a black hub cap with a
thin red ring and a small red equilateral triangle. Flat even frontal light,
uniform exposure, no hotspot, no shadow. Transparent background outside the
rim. No text of any kind, no numbers, no pointer.
Avoid: words, letterforms, numerals, watermark, logos, pointer, arrow, needle,
stand, base, hand, drop shadow, cast shadow, specular highlight, perspective,
tilt, angled view, rust orange, gold, green, purple, brown, warm tones, more
than four colours, uneven segments, decorative flourishes, casino glitz.
```

### 3C. X-RAY LIGHTBOX

```
A circular radiograph film disc mounted on a lightbox, photographed flat on and
perfectly centred, filling the frame. The disc is divided into exactly ten
identical wedge segments of thirty six degrees each by ten fine bright dividing
lines, perfect rotational symmetry. Light passes through the film unevenly by
segment, in only four values, arranged clockwise: bright cold morphine blue
glow, blown out white, dimmer blue glow, blown out white, saturated arterial
red glow, completely opaque black, dimmer blue glow, blown out white, saturated
arterial red glow, opaque black with a thin glowing red edge. Ghosted anatomy
is faintly visible through the film across the whole disc, vertebrae and rib
shadows, scan lines, dust and emulsion scratches, film grain. A thin machined
steel ring holds the film at the outer edge. At the centre is an opaque black
hub with a thin red ring and a small red equilateral triangle. The glow is even
across the whole disc with no falloff toward any edge, no hotspot, no vignette.
Transparent background outside the steel ring. No text, no numbers, no
measurement markings, no pointer.
Avoid: words, letterforms, numerals, patient data, watermark, logos, pointer,
arrow, needle, stand, hand, drop shadow, specular highlight, perspective, tilt,
angled view, green, gold, purple, cyan neon, warm tones, more than four
colours, uneven segments, skull, face, casino glitz.
```

### 3D. SHARP EDGE

Hard vector, zero wear. Same geometry and same clockwise colour order as the
others, but every boundary is a razor and nothing is photographed. This is the
direction that stays cleanest at 280 px and the only one that survives being
scaled up later.

Two changes specific to it. The dividers are **white, not grey**, because grey
dividers on a black wedge vanish at render size. And the Nothing wedge is
**near-black, not pure black**, or it dissolves into the `#131517` sunk panel
behind the wheel and the disc looks like it has a bite out of it.

```
A hard-edged flat vector illustration of a circular ten-segment dial, dead
centre, filling the frame, viewed perfectly straight on with no perspective.
The disc is divided into exactly ten identical wedge segments of thirty six
degrees each by ten razor-sharp straight radial divider lines of uniform
weight, in perfect rotational symmetry. Every colour boundary is a clean crisp
hard edge with no blur, no feathering, no gradient and no bevel. The segments
are solid flat colour fills in only four colours, arranged in this order
clockwise: pale surgical blue, pure white, pale surgical blue, pure white,
saturated arterial red, near-black, pale surgical blue, pure white, saturated
arterial red, near-black with a crisp arterial red keyline border. The dividers
between segments are thin pure white lines. A single crisp concentric ring runs
around the outer edge of the disc, a thin arterial red line inset just inside
it. At the exact centre is a small solid near-black circular hub with a thin
crisp red ring, and a single sharp red equilateral triangle at its centre,
point upward, with perfectly straight edges and clean corners. Absolutely flat,
no lighting, no shading, no shadow, no highlight, no texture, no grain, no
noise. Transparent background outside the outer ring. No text, no numbers, no
letters, no markings inside the segments, no pointer, no arrow, no stand.
Avoid: words, letterforms, numerals, watermark, logos, pointer, arrow, needle,
stand, base, hand, texture, grain, noise, chipped paint, scratches, wear,
distressing, rust, dirt, photograph, photorealism, metal, bevel, emboss, gloss,
reflection, gradient, glow, drop shadow, cast shadow, specular highlight, soft
edge, blur, anti-aliased mush, perspective, tilt, angled view, gold, yellow,
green, purple, orange, brown, teal, warm tones, more than four colours, uneven
segments, nine segments, eleven segments, decorative flourishes, casino glitz.
```

Matching pointer, since the enamel one in section 4 clashes with this plate:

```
A single downward pointing triangular pointer for a prize wheel, hard-edged
flat vector illustration, isolated on a transparent background, filling the
frame, viewed perfectly straight on. A narrow isosceles triangle in solid
saturated arterial red with a razor-sharp point at the bottom, perfectly
straight edges, clean sharp corners, and a thin crisp white keyline running
around its outline. Absolutely flat, no lighting, no shading, no texture, no
gradient, no shadow. Nothing else in frame.
Avoid: words, letterforms, numerals, watermark, texture, grain, noise, metal,
bevel, emboss, gloss, gradient, glow, drop shadow, cast shadow, soft edge,
blur, rounded corners, perspective, tilt, wheel, disc, hand, gold, green,
purple, warm tones.
```

---

## 4. THE POINTER

The current pointer is a CSS triangle in `.wpin`. Only replace it if the plate
is heavily textured, otherwise the flat triangle sits fine on top. If the plate
is 3D, use the sharp-edge pointer in that section instead of this one.

```
A single downward pointing pointer for a prize wheel, shot flat on, isolated on
a transparent background, filling the frame. A narrow machined steel arm with a
sharp tapered tip, the tip and the leading half painted arterial red in worn
enamel, the steel scuffed and chipped, a single countersunk bolt at the wide
end. Flat even frontal light, no shadow. Nothing else in frame.
Avoid: words, letterforms, numerals, watermark, drop shadow, cast shadow,
gradient background, perspective, tilt, wheel, disc, hand, gold, green, purple,
warm tones.
```

Export **512 x 1024**, tip at the bottom edge, transparent.

---

## 5. THE HUB CAP (optional, layer on top)

Useful if the generator keeps softening the centre of the plate. Drop this over
the middle as a second `<img>` so the house mark stays crisp.

```
A small circular metal hub cap photographed flat on, isolated on a transparent
background, filling the frame. Black enamel face, a thin arterial red ring
running just inside the edge, and a single red equilateral triangle embossed at
the exact centre, point upward. The enamel is chipped at the rim showing bare
steel, faint scratches across the face. Flat even frontal light, no shadow.
Avoid: words, letterforms, numerals, watermark, logos, drop shadow, cast
shadow, perspective, tilt, gradient background, gold, green, purple, warm
tones, more than one triangle.
```

Export **512 x 512**, transparent.

---

## 6. FULL FACE WITH LABELS (only if you insist)

Read section 0 first. If the text comes back mangled, do not try to fix it with
another generation, take the clean plate from section 3 and typeset the ten
labels over it in Figma. Both routes give you a PNG, one of them takes ten
minutes and is correct.

```
A flat top-down product photograph of a circular ten-segment prize dial from a
1960s hospital, shot straight on, perfectly centred, filling the frame, divided
into exactly ten identical wedge segments of thirty six degrees each in perfect
rotational symmetry, with a wedge centre pointing straight up at twelve
o'clock. Reading clockwise starting from the segment whose centre is at twelve
o'clock, the segments are: pale surgical blue enamel with the black stencilled
text "+5 entries", arterial red enamel with the white stencilled text "5,000
PK", black with a red border and red stencilled text "Pain Scale +1", pale
surgical blue enamel with the black stencilled text "500 USDT", chalk white
enamel with the black stencilled text "+2 entries", pale surgical blue enamel
with the black stencilled text "50 USDT", chalk white enamel with the black
stencilled text "+1 entry", arterial red enamel with the white stencilled text
"1,000 PK", matte black with the grey stencilled text "Nothing", pale surgical
blue enamel with the black stencilled text "10 USDT". Every label is set in a
condensed industrial monospace stencil face, all on one line, reading outward
along its own wedge, the same size in every wedge, sitting near the outer edge.
A machined steel bezel ring encircles the plate. At the centre is a black hub
cap with a thin red ring and a small red equilateral triangle. Flat even
frontal studio lighting, no hotspot, no shadow. Transparent background outside
the bezel. Only four colours: arterial red, pale surgical blue, chalk white,
black.
Avoid: extra text, invented words, misspelled words, duplicated labels, curved
text, vertical text, watermark, logos, pointer, arrow, needle, stand, hand,
drop shadow, specular highlight, perspective, tilt, gold, green, purple,
orange, warm tones, more than four colours, uneven segments, casino glitz.
```

Segment order above is rotated so that the twelve o'clock wedge is listed
first, which is how these models read a dial. It is the same `WHEEL` order,
starting at index 7.

---

## 7. BEZEL ONLY, the cheap win

Changes nothing in the drawing code. The canvas keeps drawing wedges and
labels, and a PNG ring sits over its outer edge, hiding the flat `#454A50`
stroke that currently rims it.

```
A circular metal bezel ring photographed flat on, isolated on a fully
transparent background, the centre of the ring completely empty and
transparent. Brushed machined steel, scuffed and scratched, chipped white
enamel on the outer face, a thin arterial red line running around the inner
edge, eight countersunk bolts set evenly around the ring. The ring wall is
about seven percent of the overall diameter. Flat even frontal light, no
shadow, perfectly circular, no distortion. Nothing inside the ring.
Avoid: words, letterforms, numerals, watermark, logos, wheel, segments, spokes,
hub, pointer, hand, drop shadow, cast shadow, gradient background, perspective,
tilt, oval, gold, brass, green, purple, warm tones.
```

Export **2048 x 2048**, transparent inside and out.

---

## 8. WIRING THE PLATE IN

For section 3 output. `drawWheel()` is at `painbet-intake-scroll.html:872`,
`spinWheelTo()` at `:893`.

1. Save as `assets/wheel/plate.png`, and preload it next to the frame
   sequences so the first spin is not a blank disc.
2. In `drawWheel()`, replace the wedge fill loop with one `ctx.drawImage()` of
   the plate at the current rotation. Keep the label loop exactly as it is, and
   keep `SEG_COL` only for the label ink colour, remapped to the section 2
   table: white ink on red wedges, black on blue and white, 40% white on the
   Nothing wedge.
3. Delete the outer ring stroke and the hub circle at the end of `drawWheel()`
   if the plate already carries them, otherwise they double up.
4. The `.wpin` pointer and the CSS drop shadow both stay as they are.

The plate is a single square image drawn at `R * 2`, so nothing about
`spinWheelTo()`, the easing or the weighted landing changes.

---

## 9. EXPORT CHECKLIST

- [ ] PNG with real alpha, not a white or black square
- [ ] Square, 2048 x 2048, disc centred to within a pixel or two
- [ ] Exactly ten wedges, counted, not assumed
- [ ] Four colours only, sampled with a picker, greys neutral
- [ ] No baked drop shadow, no baked hotspot
- [ ] No pointer, no stand, no text unless section 6 was used
- [ ] Viewed at 280 px wide: dividers still visible, hub still reads

---

## 10. REBRANDING A CODED 3D WHEEL (brief for another model)

Not an image prompt. This is the brand briefing to paste into another AI when
handing it an existing HTML/CSS/JS 3D wheel to restyle. Paste the block, then
paste the component's code after it.

Two failure modes to check for in whatever comes back. It will almost always
introduce a gold or amber win state, because every model's training equates
jackpot with gold, and it will want to add a pulsing glow loop on the pointer
or hub. Both are banned in the brief and both get through anyway.

```
You are restyling an existing 3D wheel component (HTML + CSS + JS) into the
pain.bet brand. Do not rewrite it. Keep the existing rendering approach,
markup structure, class names, event handlers, spin logic, easing hooks and
public API exactly as they are. Change appearance only. If a value is not
covered below, derive it from the tokens rather than inventing a new one.

## THE BRAND IN ONE LINE

pain.bet is a hospital, not a casino. Cold, clinical, expensive, slightly
wrong. Think an anaesthesia machine in a decommissioned ward, not a Vegas
floor. Every instinct that says "make it fun" is wrong. Restraint reads as
money here.

## PALETTE (hard limit, four colours plus neutral structure)

--red:      #E10600   arterial red
--red-hot:  #FF3B33   red on hover / active only
--red-deep: #520703   deep red for large flat masses
--blue:     #7FD6E8   morphine blue
--blue-dim: #16333a   blue on dark fills
--white:    #F7F8F8
--ground:   #232427   page behind the wheel
--card:     #1B1D20   panel the wheel sits on
--sunk:     #131517   recessed wells, the darkest surface
--line:     #454A50   borders
--ink:      hsla(0,0%,100%,.55)  body text
--ink-hi:   hsla(0,0%,100%,.75)  emphasis text
--ink-lo:   hsla(0,0%,100%,.25)  muted text

COLOUR LAW, this is not decorative:
- Arterial red means pain, risk, the house, and calls to action. Never money.
- Morphine blue means money, credit, relief and payout. Only money. Never
  risk, never a warning, never a generic accent.
- White is neutral, chart paper, entries, hairlines.
- Near-black is absence, the losing outcome, recessed surfaces.
- Greys are strictly black-to-white neutrals for structure. No warm grey,
  no blue grey, no gunmetal tint.
- Banned outright: gold, brass, yellow, green, purple, orange, teal, pink,
  neon cyan, any rainbow or multi-hue gradient, any colour not listed above.

If the wheel currently colour-codes segments by prize tier, remap it:
cash payouts go morphine blue, house currency and perks go arterial red,
entries go white, the losing segment goes near-black.

## TYPE

--disp: 'Archivo Black', 'Archivo', sans-serif   headings, prize values, the
        big result readout. Tight tracking, uppercase where it fits.
--sans: 'Archivo', sans-serif                    body, 14.5px/1.5
--mono: 'JetBrains Mono', ui-monospace, monospace

Labels, odds, counters, timers, meta lines and anything numeric go mono,
10.5px to 11px, uppercase, letter-spacing .16em to .22em, colour --ink-lo.
That spaced mono micro-label is the single most recognisable thing about the
brand. Use it on every small label on the component.

Buttons: --disp or 800 weight, 11.5px, uppercase, letter-spacing .08em,
padding 10px 20px, border-radius 999px. Primary is red on white text with
box-shadow 0 6px 18px rgba(225,6,0,.35). Secondary is transparent with a
1px --line border and --ink-hi text. Never a blue primary button unless the
action is literally withdrawing or receiving money.

## SHAPE AND SURFACE

--r-lg:16px  --r-md:12px  --r-sm:8px  --r-pill:999px
--shadow:    0 10px 28px rgba(0,0,0,.35)
--shadow-lg: 0 18px 44px rgba(0,0,0,.5)
--ease-out:  cubic-bezier(.22,1,.36,1)

Panels are flat --card fills with --r-lg corners and a soft black shadow. No
borders unless a hairline is needed for separation, in which case 1px --line
or an inset 0 0 0 1px hsla(0,0%,100%,.04) ring. Recessed areas use --sunk.

The house mark is a solid red equilateral triangle, point up, made with
clip-path: polygon(50% 0, 100% 100%, 0 100%). Use it as the hub cap face, as
an oversized low-opacity background mass bleeding off a corner, and nowhere
else. Never outline it, never round it, never rotate it off axis.

## THE 3D WHEEL SPECIFICALLY

Keep whatever technique the code already uses, CSS 3D transforms or WebGL.
Restyle the materials, not the maths.

- Read the wheel as machined hospital equipment: a heavy dial plate seated in
  a steel bezel, mounted flat. Not a carnival wheel, not a lottery drum.
- The rim / side wall is the thickest visual element. Give it real depth,
  neutral dark grey stepping to near-black at the back edge, with a single
  thin arterial red line running around its circumference. That red line is
  the only chrome-equivalent flourish permitted.
- Segment faces are flat matte fills. No gloss, no plastic sheen, no
  metallic reflection, no environment map, no fresnel rim glow in any colour
  other than red or blue.
- Segment dividers are thin white lines, not grey. Grey dividers disappear
  against the dark segments at small render sizes.
- Hub is a small near-black disc with a thin red ring and the red triangle
  at its centre, point up.
- Lighting: one soft key from slightly above front, one very dim fill, a
  black background. Low overall exposure. Shadows are black, never coloured.
  Nothing in the scene should be brighter than the white segments.
- Depth of field, bloom and glow stay off, except an optional tight red glow
  under the pointer.
- If there is a pointer, it is a solid arterial red triangle at 12 o'clock
  with a razor point, and it must not rotate with the wheel.
- If the wheel tilts, keep the tilt shallow, under 20 degrees. A steeply
  raked wheel reads as a game show.

## MOTION

- All transitions use cubic-bezier(.22,1,.36,1), 300ms for state changes.
- The spin decelerates on a long ease-out and stops dead. No overshoot, no
  elastic settle, no bounce, no wobble.
- Hover lifts an element by translateY(-1px), active pushes it down 1px.
  That is the entire hover vocabulary.
- No confetti, no particles, no fireworks, no coin showers, no screen shake,
  no flashing, no pulsing glow loops. A win is announced by the result text
  changing colour and weight, nothing else.
- No hard white flashes anywhere, at any time.

## COPY TONE

Clinical and flat, delivered deadpan. "Ready." "Nothing today." "Paid to your
wallet on verification." Never exclamation marks, never "Congratulations",
never "You won!", never emoji, never casino language like jackpot, lucky,
bonanza, mega, fortune.

Never use em-dashes in any visible text. Use commas, periods or parentheses.

## ACCEPTANCE CHECK

Before you return the code, verify every one of these:
1. No colour appears anywhere outside the token list above.
2. Blue appears only on money. Red never appears on money.
3. Every small label is spaced uppercase mono.
4. No gloss, metallic reflection, bloom or coloured shadow on the 3D wheel.
5. The spin stops without bouncing.
6. No confetti, particles or white flash on a win.
7. Spin logic, odds, markup structure and public API are byte-for-byte
   unchanged in behaviour.

Return the full restyled file. Where you changed a visual decision that was
load-bearing for the existing layout, note it in one line above the code.
```
