# triangle-composite

Puts the pain.bet triangle into the reference stills in `scratch/refs/`.

The plates were pulled from the finished clips, so they carry the grade of the
shot footage exactly. Regenerating them to add the brand geometry would throw
that away, so the geometry is composited on instead and the originals are kept.

```
python3 do_ward_clean.py      ->  ../refs/ref_ward_clean_tri.jpg
python3 do_ward_decayed.py    ->  ../refs/ref_ward_decayed_tri.jpg
python3 do_examroom.py        ->  ../refs/ref_examroom_tri.jpg
python3 do_locker.py          ->  ../refs/ref_locker_tri.jpg
```

Each script also drops zoomed verification crops in `preview/`. Needs Pillow and
nothing else. Coordinates are hard-coded per plate, so a script only makes sense
against the plate it names.

| Plate | Edit |
|---|---|
| `ward_clean` | EXIT lettering off the sign, red triangle in its place; stencil triangle above the 07 |
| `ward_decayed` | Both signs delettered to red triangles; stencil triangle above the 07 |
| `examroom` | Stencil triangle above the 0; dense bright triangle in the chest x-ray |
| `locker` | Biohazard trefoil removed, glowing red triangle seal light in its place |

## What the plates forced

- **The sign panels and the locker face need different removal techniques.** On
  the sign panels the lettering separates from the red on the green channel, so
  a per-row median plus a horizontal smear erases it. The locker's drawer face
  is lit brightly enough that the trefoil and the metal overlap in every
  channel, so no threshold works there and the face is rebuilt by interpolating
  each row across the marking from the clean columns either side.
- **Paste through a shape, not a box.** Any rectangular paste shows as a band on
  textured metal. The interpolated fill avoids it by meeting the plate exactly
  at both edges.
- **The x-ray triangle has to be bright.** On this footage lungs render dark and
  dense tissue renders bright, so a dark triangle over a lung field disappears.
- **Drawn geometry needs wearing down** (`distress`) or it reads as vector art
  beside the plates' chipped stencil numerals.
