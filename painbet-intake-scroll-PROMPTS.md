# THE INTAKE — Higgsfield keyframe prompts (portrait, spatially locked)

Generate keyframe STILLS first (Higgsfield Soul), then feed each pair as
Start/End frame into DoP with the motion prompt. Where a boundary is shared,
reuse the same still — do not regenerate.

**Orientation:** portrait **9:16, 1080x1920**. Keep all key action (EXIT sign,
nurse, doors, drawer) in the **center third** so cover-crop survives desktop.

---

## LOCK — paste into EVERY image prompt
```
STYLE LOCK: photoreal cinematic film still, 35mm, PORTRAIT 9:16, center-safe
composition. Teal-green shadows with arterial-red glow (complementary grade),
low-key, volumetric haze, soft bloom, heavy 35mm film grain, shallow DoF.
CHARACTER LOCK: one nurse, woman in her 30s, pale blue vintage nurse uniform,
white collar and starched cap, small ID badge, dark hair pulled back, pale
tired face. Always standing on the corridor centerline.
NEGATIVE: text overlay, watermark, subtitles, extra limbs, warped face, cartoon,
daylight, modern hospital, doors or signs in different positions, floating signs.
```

---

## WARD CONTINUITY MAP — the fixed layout (never changes)
Camera travels forward along the corridor **centerline** at gurney height
(~1.1 m). The corridor is **12 m** long. These landmarks are bolted in place;
they only enter/leave frame as the camera passes them. State them the SAME way
in every frame so nothing drifts.

| Landmark | Side | Distance from start |
|---|---|---|
| Red **EXIT** sign (illuminated) | **straight ahead, dead center, mounted ABOVE the far doors** | 12 m (visible in every corridor frame until arrival) |
| Red **double doors** + stenciled **`07`** on the left leaf | straight ahead, center | 12 m |
| Ceiling fluorescent tubes | overhead, center, receding | every 2 m |
| `WARDS 01-08 →` hanging directional sign | overhead, center | 4 m |
| **Room 03** door + red number plate | **LEFT wall** | 3 m |
| **Room 04** door + red number plate | **RIGHT wall** | 5 m |
| Red glass **fire-hose cabinet** | **RIGHT wall** | 6 m |
| **Room 05** door + red number plate | **LEFT wall** | 7 m |
| **Room 06** door + red number plate | **RIGHT wall** | 9 m |
| Paired chrome **gurneys** | both walls, between doors | throughout |
| The **nurse** | centerline | starts at 8 m, leads camera forward |

**Decay gradient:** 0 m clean and intact; rust and streaks begin ~6 m; walls
torn and bleeding by 10 m.

---

## CLIP 1 — ADMISSIONS (corridor descent)
Give START + END (required pair). MID frames are optional, for generating the
clip in tighter segments. Every frame states camera distance + distance advanced.

### 1A START — camera at 0 m (advanced 0 m)
```
[LOCK] Camera at the mouth of the ward, 0 m traveled, 12 m of corridor ahead.
STRAIGHT AHEAD dead center: the red EXIT sign glowing above the closed red
double doors at the far end (12 m) - clearly visible. Ceiling fluorescents
recede straight ahead down the center; the WARDS 01-08 hanging sign spans the
corridor overhead at 4 m. LEFT wall: Room 03 door ahead at 3 m, Room 05 door
faint at 7 m. RIGHT wall: Room 04 door at 5 m, red fire-hose cabinet at 6 m,
Room 06 door at 9 m. Paired chrome gurneys line both walls. The nurse stands on
the centerline at 8 m, small, facing camera. Walls clean and intact, cold light.
```

### 1B MID (optional) — camera at 6 m (advanced 6 m)
```
[LOCK] Camera advanced to 6 m (6 m still to the doors). STRAIGHT AHEAD center:
the red EXIT sign and red double doors, larger, still dead center and visible.
The WARDS 01-08 hanging sign has just passed overhead (top edge of frame). LEFT
wall: Room 03 door now behind camera; Room 05 door beside the camera on the left
at 7 m, its red number plate level with the lens. RIGHT wall: fire-hose cabinet
passing on the right at 6 m; Room 06 door ahead on the right at 9 m. Nurse now
~4 m ahead, closer, turning to lead. Walls beginning to rust and streak.
```

### 1C END — camera at 10 m (advanced 4 m) — SHARED with Clip 2 start
```
[LOCK] Camera advanced to 10 m, now 2 m from the doors. STRAIGHT AHEAD filling
the center: the red double doors with a stenciled 07 on the left leaf and the
red EXIT sign directly above them. LEFT wall: Room 05 door now behind camera.
RIGHT wall: Room 06 door beside the camera on the right at 9 m. Nurse standing
just left of the doors, close, watching. Walls heavily decayed, torn and
bleeding, red light seeping around the door seams.
```

---

## CLIP 2 — INTAKE (through the doors) *(optional bridge)*
Start = reuse 1C. Camera pushes from 10 m through the doors into the exam bay.
### 2B END — camera at 13 m (advanced 3 m, now inside)
```
[LOCK] The red double doors have swung open and the camera has pushed 3 m
through them into a small examination bay (13 m). STRAIGHT AHEAD center: an
empty steel gurney under a single swinging overhead lamp, and behind it a
wall-mounted x-ray lightbox glowing faint red, dead center. A blank patient
chart on a clipboard rests on the gurney, centered, sharp focus. Blood-flecked
tiles, decayed. The EXIT sign is now behind the camera (gone from frame,
correctly). Static.
```

---

## CLIP 3 — LOCKER 07 (prize drawer, scrubs both ways)
Macro, no corridor. Camera pushes straight toward the drawer face. Distance =
push distance; the drawer also slides OUT toward camera. Signage positions are
fixed so they persist.
### 3A START — camera 1.2 m from drawer, drawer closed (0 cm out)
```
[LOCK] Macro, camera 1.2 m from a single stainless steel morgue specimen drawer,
square-on. CENTER of frame: the drawer face with a stenciled 07 dead center. Red
biohazard seal light at the TOP-RIGHT corner of the drawer face, glowing. Heavy
chrome latch at center-bottom, engaged. Drawer flush with the wall, 0 cm out.
Cold blue-red rim light, wet metal reflections, dark surround.
```
### 3B END — camera 0.4 m (advanced 0.8 m), drawer slid 0.4 m out
```
[LOCK] Same drawer, camera pushed to 0.4 m (advanced 0.8 m). The drawer has slid
0.4 m OUT toward camera. The 07 stencil still dead center on the drawer front;
the seal light still at TOP-RIGHT (now dimmed); the latch at center-bottom,
released. Arterial-red light floods from inside the open tray, cold vapor spills
over the near lip, a single glowing red object rests centered on the steel tray.
```

---

## CLIP 4 — DISCHARGE (reverse outro) *(optional)*
### 4A START — camera at 10 m looking back, decayed
```
[LOCK] Camera at 10 m looking back DOWN the corridor toward the red EXIT sign at
the far end (straight ahead, center, visible), gurneys receding, walls decayed
and bloodied, the nurse standing on the centerline at ~6 m facing camera.
```
### 4B END — camera at 0 m (retreated 10 m), corridor healed
```
[LOCK] Camera retreated to 0 m at the mouth of the ward. STRAIGHT AHEAD center:
the red EXIT sign small and distant at the far end (12 m), still visible. The
corridor is now clean and healed, walls pale and intact, calm light, the nurse
small on the centerline near the EXIT. Same landmark layout, undamaged.
```

---

## Form-scene backdrops (stills, not video)
The capture rooms (wallet, quiz, discharge, dispensary, dashboard, login) hold a
dimmed STATIC frame behind the card. Cheapest: reuse a nearby corridor/exam
still. For extra polish, one dedicated still per room at the matching depth
(e.g. wallet = exam bay at 13 m, dispensary = a pharmacy shelf room). Same LOCK,
same center-safe framing, no camera-move language needed.
```
[LOCK] Static interior of a decayed ward [room type], dim, one overhead lamp,
center-safe, no text. [key prop] centered. Cold teal-red grade, film grain.
```
