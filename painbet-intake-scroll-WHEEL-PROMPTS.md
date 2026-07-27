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
