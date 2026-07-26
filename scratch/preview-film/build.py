#!/usr/bin/env python3
"""Build a standalone, scrubbable review page for the 60s intake film.

    python3 scratch/preview-film/build.py

Reads the committed frame sequence in assets/seq/film/ and writes
scratch/preview-film.html - one self-contained file with the frames embedded,
so it opens over file:// with no server and no network.

Why a proxy rather than the real frames: the full sequence is 1444 frames at
800x1450 and 81 MB, which no single HTML file wants to carry. Every fourth
frame at 240px comes to about 3 MB, which is enough to judge composition,
pacing and where the camera stops. It is not enough to judge grain or grade,
and the page says so.

The motion trace is measured from the full-resolution frames, not from the
proxy, so the holds it marks are real.

Needs ffmpeg and Pillow.
"""

import base64
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRAMES = os.path.join(ROOT, 'assets', 'seq', 'film')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'scratch', 'preview-film.html')

TOTAL = 1444
FPS = 24
EVERY = 4       # embed every Nth frame
WIDTH = 240     # proxy width in px
QUALITY = 50

# Measured from the full-resolution sequence; see the handoff. Regenerate with
# --holds if the footage is ever recut.
HOLDS = [
    (699, 722, 'End of the corridor'),
    (1063, 1177, 'The room, wide'),
    (1289, 1315, 'The x-ray wall'),
    (1324, 1350, 'The locker, in passing'),
    (1352, 1388, 'The desk and chart'),
    (1414, 1444, 'The locker, held to the end'),
]


def frame_path(i):
    return os.path.join(FRAMES, 'frame_%04d.webp' % i)


def measure_motion():
    """Mean absolute difference between consecutive frames, downsampled.

    Downsampling to 96x174 first is what makes this cheap enough to run over
    every frame, and it also stops film grain from swamping the real camera
    movement.
    """
    from PIL import Image, ImageChops, ImageStat
    diffs, prev = [], None
    for i in range(1, TOTAL + 1):
        im = Image.open(frame_path(i)).convert('L').resize((96, 174), Image.BILINEAR)
        if prev is not None:
            diffs.append(ImageStat.Stat(ImageChops.difference(im, prev)).mean[0])
        prev = im
        if i % 200 == 0:
            print('  measured %d/%d' % (i, TOTAL), file=sys.stderr)
    return diffs


def find_holds(diffs, thresh=0.6, minlen=8):
    """Runs of frames quiet enough to count as the camera holding still."""
    runs, start = [], None
    for i, v in enumerate(diffs):
        if v < thresh:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= minlen:
                runs.append((start + 1, i + 1))
            start = None
    if start is not None and len(diffs) - start >= minlen:
        runs.append((start + 1, len(diffs) + 1))
    return runs


def encode_proxies(tmp):
    idx = list(range(1, TOTAL + 1, EVERY))
    if idx[-1] != TOTAL:
        idx.append(TOTAL)
    out = []
    for n, i in enumerate(idx):
        dst = os.path.join(tmp, '%d.webp' % i)
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', frame_path(i),
             '-vf', 'scale=%d:-2' % WIDTH,
             '-c:v', 'libwebp', '-quality', str(QUALITY), dst, '-y'],
            check=True)
        with open(dst, 'rb') as fh:
            out.append(base64.b64encode(fh.read()).decode())
        if n and n % 100 == 0:
            print('  encoded %d/%d' % (n, len(idx)), file=sys.stderr)
    return idx, out


def main():
    if not os.path.isdir(FRAMES):
        sys.exit('missing %s - the film sequence is not in this checkout' % FRAMES)

    print('measuring motion across %d frames' % TOTAL, file=sys.stderr)
    diffs = measure_motion()

    if '--holds' in sys.argv:
        print('\nstill runs (frame ranges), for updating HOLDS:')
        for a, b in find_holds(diffs):
            print('  (%d, %d)  %.1fs to %.1fs  %d frames' % (a, b, a / FPS, b / FPS, b - a + 1))
        return

    print('encoding proxy frames', file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        idx, frames = encode_proxies(tmp)

    payload = {
        'idx': idx,
        'frames': frames,
        # clamped and quantised to a byte; the page square-roots it for display
        'motion': [round(min(v, 20) / 20 * 255) for v in diffs],
        'total': TOTAL,
        'fps': FPS,
        'holds': [{'from': a, 'to': b, 'name': n} for a, b, n in HOLDS],
    }

    html = open(os.path.join(HERE, 'template.html')).read()
    html = html.replace('__PAYLOAD__', json.dumps(payload))
    open(OUT, 'w').write(html)
    print('wrote %s (%.1f MB)' % (OUT, os.path.getsize(OUT) / 1e6), file=sys.stderr)


if __name__ == '__main__':
    main()
