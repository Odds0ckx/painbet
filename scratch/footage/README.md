# footage

Source mp4s for the intake film. **Nothing in here is committed** except this
file and the `.gitignore` beside it.

The page never loads an mp4. It reads WebP frame sequences from
`assets/seq/<scene>/`, extracted from these files, and those are what the repo
tracks. Keeping the sources out avoids carrying tens of megabytes the page has
no use for.

Save them here, numbered in play order so the concat order is unambiguous:

| File | Segment |
|---|---|
| `01-arrival.mp4` | S1 burst in, nurse stares, she leads, the rot begins |
| `02-flicker.mp4` | S2 corridor, the lights stutter, silhouettes |
| `03-door.mp4` | S3 she opens 07, you pass through, shut in |
| `04-room.mp4` | S4 the room, four holds |
| `intake-master.mp4` | the four concatenated |

Deliver at highest quality, 9:16, no webm transcode - the frames come out of the
master and a second lossy pass before that only costs quality.

Two things make the joins invisible: keep the forward dolly speed identical
across S1 to S3, and let each segment end on the stillness its prompt describes.
Those held frames are where the popups land and where the cuts are made.

Prompts are in `painbet-intake-scroll-PROMPTS.md`.
