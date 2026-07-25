# THE INTAKE — video production reference (current plan)

Everything needed to shoot the footage for `painbet-intake-scroll.html`.
Higgsfield: **max 15s per generation, max 3 `@` references per prompt.**
All output **portrait 9:16, 1080x1920, 24fps**, same seed throughout.

> Style and negatives are written **inline in every prompt** below - copy the
> whole block. If Higgsfield offers a separate negative field, move the
> `Avoid: ...` sentence into it.

---

## 0. DECISIONS SETTLED

Both open questions from the last session are closed. What changed, and why.

### The sign is triangle-only, no word

The illuminated sign above the 07 doors shows **a red triangle and nothing
else**. Not "triangle + EXIT".

This is not a technical call. The shot footage renders the word EXIT cleanly at
three different sizes, so legibility was never the risk it was assumed to be. It
is a story call: a sign that should promise a way out, showing the house mark
instead, is the whole film in one frame. A sign that says EXIT is set dressing
from any hospital horror; a wordless red triangle is pain.bet. It also keeps the
negative prompt honest: asking for the word EXIT while negative-prompting text
is a contradiction that costs lettering quality everywhere else in frame.

### Negatives must not kill the numerals

Every prompt in the last version read `Avoid: text, lettering, words, ...` while
also asking for **a large stencilled number 07**. Same contradiction. The 07
survived it in the shot footage, but that is luck, not design.

All negatives below now read `words, letterforms, signage text` instead of
`text, lettering, words`. **Numerals are wanted, and are never
negative-prompted.** The rule is unchanged in spirit: the triangle goes in the
world, the wordmark stays on the page, and the only glyphs allowed in frame are
the 07.

### The reference stills are composited, not regenerated

The plates in `scratch/refs/` came out of the finished clips, so they carry the
grade of the shot footage exactly. Regenerating them to add the triangle would
throw that away and start the look from scratch. The triangle was composited
onto them instead.

| Plate | What was added |
|---|---|
| `ref_ward_clean_tri.jpg` | EXIT lettering off the sign, red triangle in its place; stencil triangle above the 07 |
| `ref_ward_decayed_tri.jpg` | Both signs delettered to red triangles; stencil triangle above the 07 |
| `ref_examroom_tri.jpg` | Stencil triangle above the 07; triangle mass in the chest x-ray |
| `ref_locker_tri.jpg` | Biohazard trefoil removed, glowing red triangle seal light in its place |

Originals are untouched alongside them. The tool that produces them is
`scratch/triangle-composite/` - one script per plate, rerun with
`python3 do_<plate>.py`, verification crops land in `preview/`.

**Upload the `_tri` plates as the `@` references, not the originals.** The
originals have no triangle anywhere and the locker original carries a biohazard
trefoil, which is the one marking the brief explicitly negative-prompts.

### What the plates taught us

- The x-ray triangle has to be **bright, not dark**. On this footage the lungs
  render dark and dense tissue renders bright, so the "dark triangle shadow"
  the old prompt asked for lands on a dark lung field and disappears. Described
  as a dense bright mass it reads instantly, and it is the radiographically
  correct way round. The `@examroom` prompt is updated accordingly.
- On the **interior** view of the doors the space directly above the numerals is
  crossed by the seam, the panel moulding and the lit door edge. The triangle
  sits in the clear field above the 0 there. On the corridor views, centred
  above the number is fine.

---

## 1. THE PLAN

One continuous ~60s film, generated as **4 x 15s segments** chained
start-frame-to-end-frame, then concatenated into a single master mp4. The page
treats it as one frame sequence with **station markers** at the four holds in
Segment 4: the playhead accelerates between markers and eases to a stop at each,
where a form popup opens (the "Matrix" beat).

| Segment | Beat | Keyframes |
|---|---|---|
| S1 | Burst in, nurse stares, she turns and leads, corridor starts to rot | F1 -> F2 |
| S2 | Two door-window glimpses of gamblers, lights flicker, silhouettes | F2 -> F3 |
| S3 | She opens the 07 doors, you pass through, turn back, she is aged and shuts you in | F3 -> F4 |
| S4 | The room: four holds (chair, x-ray wall, desk/chart, locker) | F4 -> F5 |

---

## 2. ASSET LIBRARY (generate these first)

**Canonical door block** - paste this wording *verbatim* wherever the doors
appear, so they do not drift between assets:

> a pair of battered red steel double doors with a large stencilled number 07
> across them and a single white stencilled equilateral triangle centred directly
> above the number, an illuminated red sign above the doorframe showing a red
> equilateral triangle and no writing of any kind

Brand rule: **the triangle goes in the world, the wordmark stays on the page.**
Describe it as *geometry*, never as a logo, and always negative-prompt words -
that is the only reliable way to get it rendered cleanly. The stencilled 07 is
the one exception and is never negative-prompted.

The reference stills to upload live in `scratch/refs/`: use the **`_tri`
versions** (`ref_ward_clean_tri.jpg`, `ref_ward_decayed_tri.jpg`,
`ref_examroom_tri.jpg`, `ref_locker_tri.jpg`), which are the plates from the
finished footage with the triangle composited in. They preserve the grade of the
shot footage exactly and already carry the brand geometry. The prompts below are
the alternative if generating fresh.

### `@ward_clean`
```
Empty 1970s hospital ward corridor, no people, pale teal-green tiled walls in
good condition, pale grey vinyl floor, suspended ceiling with recessed
fluorescent tubes running away from camera, rows of chrome gurneys with dark
vinyl pads along both walls. At the far end of the corridor stands a pair of
battered red steel double doors with a large stencilled number 07 across them
and a single white stencilled equilateral triangle centred directly above the
number, an illuminated red sign above the doorframe showing a red equilateral
triangle and no writing of any kind. Small red equilateral triangle hazard
placards are mounted at intervals along both walls. Establishing plate,
first-person eye level, centred on the corridor axis, portrait 9:16. Shot on
35mm anamorphic, shallow depth of field, teal-green shadows with arterial-red
glow, volumetric haze, heavy film grain, practical lighting only, photorealistic
cinematic horror. Avoid: words, letterforms, signage text, watermark, subtitles,
people, cartoon, daylight, rust, blood, decay.
```

### `@ward_decayed`
```
The same 1970s hospital ward corridor, no people, now heavily decayed:
teal-green tiles cracked and peeling, walls rusted, torn and streaked with dried
blood, grimy grey floor, most ceiling fluorescents dead or flickering, rows of
battered chrome gurneys along both walls. At the far end of the corridor stands
a pair of battered red steel double doors with a large stencilled number 07
across them and a single white stencilled equilateral triangle centred directly
above the number, an illuminated red sign above the doorframe showing a red
equilateral triangle and no writing of any kind, still glowing. Small red
equilateral triangle hazard placards, scuffed and stained, are mounted at
intervals along both walls. Establishing plate, first-person eye level, centred
on the corridor axis, portrait 9:16. Shot on 35mm anamorphic, shallow depth of
field, teal-green shadows with arterial-red glow, volumetric haze, heavy film
grain, practical lighting only, photorealistic cinematic horror. Avoid: words,
letterforms, signage text, watermark, subtitles, people, cartoon, daylight,
clean walls, bright light.
```

### `@reddoors`
```
A pair of battered red steel double doors with a large stencilled number 07
across them and a single white stencilled equilateral triangle centred directly
above the number, an illuminated red sign above the doorframe showing a red
equilateral triangle and no writing of any kind. Set in a dark green tiled wall,
closed, paint chipped and scratched, red light bleeding through the gaps around
them, a worn red triangle painted on the floor at the threshold. Straight-on
view, portrait 9:16. Shot on 35mm anamorphic, shallow depth of field, teal-green
shadows with arterial-red glow, volumetric haze, heavy film grain, practical
lighting only, photorealistic cinematic horror. Avoid: words, letterforms,
signage text, watermark, subtitles, people, cartoon, daylight, open doors.
```

### `@examroom`
```
Interior of a decayed 1970s hospital examination room, no people, dark green
tiled walls streaked with rust and dried blood, wet concrete floor, a single
caged bulb hanging on a chain casting a cold pool of light. A chrome gurney with
a black vinyl pad sits centre with a steel clipboard chart resting on it. On the
wall a mounted x-ray lightbox glows red, the chest x-ray showing a distinct
dense bright equilateral triangle where the heart shadow should be, brighter
than the surrounding lung field. In the corner stands a pair of battered red
steel double doors with a large stencilled number 07 across them and a single
white stencilled equilateral triangle centred directly above the number, seen
from the inside. A small red equilateral triangle hazard placard is fixed beside
them. Portrait 9:16. Shot on 35mm anamorphic, shallow depth of field, teal-green
shadows with arterial-red glow, volumetric haze, heavy film grain, practical
lighting only, photorealistic cinematic horror. Avoid: words, letterforms,
signage text, watermark, subtitles, people, cartoon, daylight.
```

### `@locker`
```
A single stainless steel specimen locker set into a dark green tiled wall,
closed, with a stencilled number 07 on its face and a glowing red equilateral
triangle seal light set into the door where a biohazard symbol would normally
be. Heavy chrome latch engaged, wet metal catching a cold blue and red rim
light, the surrounding wall falling into shadow. Straight-on macro view,
portrait 9:16. Shot on 35mm anamorphic, shallow depth of field, teal-green
shadows with arterial-red glow, volumetric haze, heavy film grain, practical
lighting only, photorealistic cinematic horror. Avoid: words, letterforms,
signage text, watermark, subtitles, people, cartoon, daylight, open drawer,
biohazard trefoil.
```

### `@nurse` (already exists - only regenerate if the pin is wanted)
```
Full-body portrait of a hospital nurse, woman in her 30s, slim, pale tired skin,
calm blank expression, dark hair pulled back under a white starched vintage cap,
wearing a pale-blue 1970s nurse uniform with a white collar, and a small red
equilateral triangle enamel pin on her chest where an ID badge would sit.
Standing straight, facing camera, plain dark background, portrait 9:16.
Photorealistic, soft even light, 35mm film grain. Avoid: words, letterforms,
signage text, watermark, subtitles, cartoon, warped face, extra limbs, daylight.
```

---

## 3. KEYFRAMES (5 images cover all 4 segments)

Each segment's end frame **is** the next one's start frame - generate once, use
twice. Generate F1 first, then use F1 as the reference image for F2, F2 for F3,
and so on.

| Frame | Serves as |
|---|---|
| F1 | S1 start |
| F2 | S1 end **=** S2 start |
| F3 | S2 end **=** S3 start |
| F4 | S3 end **=** S4 start |
| F5 | S4 end |

The **aged nurse is deliberately not in any keyframe** - she appears mid-shot in
S3 only, so no keyframe has to nail the ageing.

### F1 - Arrival · refs `@nurse` `@ward_clean`
```
Cinematic film still, first-person POV at chest height, 28mm, portrait 9:16,
centred on the corridor axis of @ward_clean. @nurse stands dead centre about
eight metres ahead, facing camera, motionless, arms at her sides, staring
straight down the lens. Swing doors just behind camera edge into the top corners
of frame, still settling. The ward is intact and coldly lit by overhead
fluorescents, a red triangle sign glowing small at the far end behind her. Shot
on 35mm anamorphic, shallow depth of field, teal-green shadows with arterial-red
glow, volumetric haze, heavy film grain, practical lighting only, photorealistic
cinematic horror. Avoid: words, letterforms, signage text, watermark, subtitles,
cartoon, warped face, extra limbs, daylight, decay, rust, blood.
```

### F2 - She leads, the rot begins · refs `@nurse` `@ward_decayed`
```
Cinematic film still, first-person POV at chest height, 28mm, portrait 9:16,
midway down @ward_decayed. @nurse is about four metres ahead on the centreline,
seen from behind, walking away from camera, mid-stride. The corridor has begun
to rot: paint peeling, rust blooming across the tiles, dark streaks running down
the walls, one overhead tube dimmer than the rest. The red triangle sign glows
ahead at the far end. Shot on 35mm anamorphic, shallow depth of field,
teal-green shadows with arterial-red glow, volumetric haze, heavy film grain,
practical lighting only, photorealistic cinematic horror. Avoid: words,
letterforms, signage text, watermark, subtitles, cartoon, warped face, extra
limbs, daylight, nurse facing camera.
```

### F3 - At the threshold · refs `@nurse` `@ward_decayed` `@reddoors`
```
Cinematic film still, first-person POV at chest height, 28mm, portrait 9:16, at
the far end of @ward_decayed. @reddoors fills the centre of frame a few metres
ahead, closed, the stencilled 07 and the triangle above it clearly visible, the
illuminated red triangle sign glowing directly above the doorframe. @nurse
stands close ahead just left of centre, seen from behind, reaching toward the
handle. The corridor here is heavily decayed, walls torn and bloodstained, most
overhead lights dead, deep shadow along both walls. Shot on 35mm anamorphic,
shallow depth of field, teal-green shadows with arterial-red glow, volumetric
haze, heavy film grain, practical lighting only, photorealistic cinematic
horror. Avoid: words, letterforms, signage text, watermark, subtitles, cartoon,
warped face, extra limbs, daylight, nurse facing camera.
```

### F4 - Shut in · refs `@examroom` `@reddoors`
```
Cinematic film still, first-person POV at chest height, 28mm, portrait 9:16,
standing inside @examroom looking back at @reddoors, now closed, filling the
centre of frame with the stencilled 07 and the triangle above it facing us. No
people, the room empty and silent. Thin red light bleeds around the door seams.
Behind and around us the tiled walls, the chrome gurney and the red glow of the
x-ray lightbox catch the edges of frame, lit by a single caged bulb overhead.
Shot on 35mm anamorphic, shallow depth of field, teal-green shadows with
arterial-red glow, volumetric haze, heavy film grain, practical lighting only,
photorealistic cinematic horror. Avoid: words, letterforms, signage text,
watermark, subtitles, people, nurse, cartoon, warped face, extra limbs,
daylight, open door.
```

### F5 - The locker · refs `@examroom` `@locker`
```
Cinematic film still, first-person POV at chest height, 28mm, portrait 9:16,
inside @examroom, stopped square-on in front of @locker set into the dark green
tiled wall, filling the centre of frame. The locker is closed, its stencilled 07
and glowing red triangle seal light clearly visible, heavy chrome latch engaged,
wet metal catching a cold rim light. The rest of the room falls into shadow
around it. Shot on 35mm anamorphic, shallow depth of field, teal-green shadows
with arterial-red glow, volumetric haze, heavy film grain, practical lighting
only, photorealistic cinematic horror. Avoid: words, letterforms, signage text,
watermark, subtitles, people, cartoon, extra limbs, daylight, open drawer.
```

---

## 4. MOTION PROMPTS (4 x 15s)

Feed each keyframe pair into DoP as Start / End frame with the matching prompt.

### SEGMENT 1 - ARRIVAL & THE LEAD (F1 -> F2) · refs `@nurse` `@ward_clean` `@ward_decayed`
```
First-person POV, 28mm, portrait 9:16, one continuous take. Beat one, zero to
three seconds: the camera bursts forward through a pair of swing doors which fly
open and rebound behind us, then settles to a slow breathing hover at chest
height, centred on the corridor axis of @ward_clean. @nurse stands dead centre
about eight metres ahead, motionless, staring straight down the lens, with a red
triangle sign glowing small at the far end behind her. Beat two, three to five
seconds: the camera holds completely still on her. Beat three, five to fifteen
seconds: @nurse turns away from camera and walks off down the corridor, and the
camera pushes after her in a slow constant dolly-in, holding her centred at a
fixed following distance, bobbing gently with the walk, while @ward_clean rots
into @ward_decayed ahead of us, paint peeling, rust blooming across the tiles,
dark streaks running down the walls. Shot on 35mm anamorphic, shallow depth of
field, teal-green shadows with arterial-red glow, volumetric haze, heavy film
grain, practical lighting only, photorealistic cinematic horror. Avoid: words,
letterforms, signage text, watermark, subtitles, cuts, jump cuts, fast motion,
camera shake, whip pans, cartoon, warped faces, extra limbs, daylight, nurse
turning back toward camera.
```

### SEGMENT 2 - THE WINDOWS & THE FLICKER (F2 -> F3) · refs `@nurse` `@ward_decayed`
```
First-person POV, 28mm, portrait 9:16, one continuous take moving down
@ward_decayed, forward dolly at a constant speed throughout, following @nurse
who stays centred ahead. Beat one, zero to four seconds: the camera yaws gently
left about fifteen degrees to look through a small square window set in a ward
door as we pass it, where a gambler hunches forward lit only by red screen glow,
face caught between agony and delight, mouth open, then yaws smoothly back to
centre. Beat two, four to eight seconds: the camera yaws right to a second door
window where another figure rocks back and forth, grinning, eyes wet, then
returns to centre. Beat three, eight to fifteen seconds: the overhead
fluorescents stutter and drop out in irregular bursts, and in each blackout the
corridor is lit only by the red triangle sign with tall thin silhouetted figures
standing motionless along the walls, nearer to camera on each successive
blackout, gone when the light snaps back. The camera never stops, never slows
and never flinches. Shot on 35mm anamorphic, shallow depth of field, teal-green
shadows with arterial-red glow, volumetric haze, heavy film grain, practical
lighting only, photorealistic cinematic horror. Avoid: words, letterforms,
signage text, watermark, subtitles, cuts, jump cuts, fast motion, camera shake,
whip pans, stopping, jump scares, silhouettes moving, cartoon, warped faces,
extra limbs, daylight.
```

### SEGMENT 3 - THE DOOR & SHUT IN (F3 -> F4) · refs `@nurse` `@reddoors` `@examroom`
```
First-person POV, 28mm, portrait 9:16, one continuous take. Beat one, zero to
five seconds: @nurse reaches @reddoors at the end of the corridor and stops, and
the camera's forward dolly decelerates smoothly to a near halt two metres away.
Beat two, five to nine seconds: she takes the handle, pulls @reddoors open
toward herself and steps aside holding it as red light spills across the floor,
and the camera eases forward again slowly, passing her shoulder, through the
doorway and two metres into @examroom. Beat three, nine to fifteen seconds: the
camera turns slowly one hundred and eighty degrees on its own axis to look back
at the doorway, where @nurse stands framed in the open door, now visibly aged,
skin drawn and grey, cheeks hollow, eyes sunken and dark, uniform stained and
worn, expression blank. She pulls the door slowly closed until it latches,
taking her out of frame, and the camera holds still on the closed door. Shot on
35mm anamorphic, shallow depth of field, teal-green shadows with arterial-red
glow, volumetric haze, heavy film grain, practical lighting only, photorealistic
cinematic horror. Avoid: words, letterforms, signage text, watermark, subtitles,
cuts, jump cuts, fast motion, camera shake, whip pans, jump scares, nurse
smiling, monster face, cartoon, warped faces, extra limbs, daylight.
```

### SEGMENT 4 - THE ROOM (F4 -> F5) · refs `@examroom` `@locker`
```
First-person POV, 28mm, portrait 9:16, one continuous take inside @examroom,
alone. The camera performs a single drifting move that visits four positions in
turn, easing to a complete stop at each and holding still for a full beat before
accelerating smoothly on to the next. Beat one, zero to four seconds: an
examination chair beneath a swinging overhead lamp. Beat two, four to eight
seconds: a wall of x-ray lightboxes glowing red. Beat three, eight to eleven
seconds: a steel desk with a patient chart and pen laid on it. Beat four, eleven
to fifteen seconds: @locker set into the tiled wall. Smooth acceleration and
deceleration between each stop, never a cut, never a whip, and the camera is
completely still at each of the four holds. Shot on 35mm anamorphic, shallow
depth of field, teal-green shadows with arterial-red glow, volumetric haze,
heavy film grain, practical lighting only, photorealistic cinematic horror.
Avoid: words, letterforms, signage text, watermark, subtitles, cuts, jump cuts,
fast motion, camera shake, whip pans, people, cartoon, warped faces, extra
limbs, daylight.
```

---

## 5. DELIVERY

Send the four mp4s (or one concatenated master), highest quality, 9:16. Do not
transcode to webm - the page runs on WebP frame sequences extracted from the
master, and a second lossy pass only costs quality.

Two things that make the joins invisible: keep the **forward dolly speed
identical** across S1-S3, and make sure each segment **ends on the stillness**
described - those held frames are where popups land and where the cuts are made.

---

## 6. FOOTAGE ALREADY SHOT (currently live in the page)

| Scene | Source | Frames |
|---|---|---|
| `admissions` | corridor descent, nurse leads to the 07 doors | 169 |
| `intake` | through the doors into the exam room | 169 |
| `locker07` | exam room to the locker, drawer opens on a red triangle | 145 |

These are wired into `assets/seq/<scene>/` and work today. The 4-segment film
above is the planned replacement, not a dependency.
