#!/usr/bin/env python3
"""Build a standalone, self-contained copy of the real intake page.

    python3 scratch/preview-page/build.py

Reads painbet-intake-scroll.html and the committed frame sequence in
assets/seq/film/, and writes scratch/preview-page.html - the real page,
unmodified apart from its frame source, with a proxy set of frames embedded so
it opens over file:// with no server and no network.

This exists because the normal way to look at the page needs a web server for
the frame sequences, and the point of this file is to let the film and the
station backdrops be inspected (including at the pixel level) without one.
It is a debugging aid, not the deliverable: judge composition, layout and
whether a frame is drawing at all from this; judge grain, grade and real
scrubbing performance from the page served normally over assets/seq/film/.

Why a proxy rather than the real frames: the full sequence is 1444 frames at
800x1450 and 81 MB, which no single HTML file wants to carry. Every fourth
frame at 240px comes to a few MB, plenty to confirm each scene is painting the
right footage.

Two edits to the real page, both undone by working from the source file fresh
each run rather than mutating it in place:
  1. the Google Fonts <link> is dropped, since it fails closed-network anyway
     and a dead request only slows the page down here
  2. FilmSource's fetch is patched to read from an embedded frame map instead
     of hitting assets/seq/film/ over the network

Needs ffmpeg and Pillow.
"""

import base64
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRAMES = os.path.join(ROOT, 'assets', 'seq', 'film')
PAGE = os.path.join(ROOT, 'painbet-intake-scroll.html')
OUT = os.path.join(ROOT, 'scratch', 'preview-page.html')

TOTAL = 1444
EVERY = 4       # embed every Nth frame
WIDTH = 240     # proxy width in px
QUALITY = 50

FETCH_OLD = """      const im=new Image(); im.decoding='async';
      im.src=`${this.cfg.dir}/frame_${String(i).padStart(4,'0')}.${this.cfg.ext}`;
      this.imgs[i-1]=im;"""

FETCH_NEW = """      const d=window.EMBED&&window.EMBED[i];
      if(!d) continue;              // embedded preview carries every Nth frame
      const im=new Image(); im.decoding='async'; im.src=d;
      this.imgs[i-1]=im;"""


def frame_path(i):
    return os.path.join(FRAMES, 'frame_%04d.webp' % i)


def encode_proxies(tmp):
    idx = list(range(1, TOTAL + 1, EVERY))
    if idx[-1] != TOTAL:
        idx.append(TOTAL)
    out = {}
    for n, i in enumerate(idx):
        dst = os.path.join(tmp, '%d.webp' % i)
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', frame_path(i),
             '-vf', 'scale=%d:-2' % WIDTH,
             '-c:v', 'libwebp', '-quality', str(QUALITY), dst, '-y'],
            check=True)
        with open(dst, 'rb') as fh:
            out[str(i)] = 'data:image/webp;base64,' + base64.b64encode(fh.read()).decode()
        if n and n % 100 == 0:
            print('  encoded %d/%d' % (n, len(idx)), file=sys.stderr)
    return out


def main():
    if not os.path.isdir(FRAMES):
        sys.exit('missing %s - the film sequence is not in this checkout' % FRAMES)

    print('encoding proxy frames', file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        embed = encode_proxies(tmp)

    html = open(PAGE).read()
    html = re.sub(r'\s*<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>', '', html)

    if FETCH_OLD not in html:
        sys.exit('FilmSource fetch block has changed shape - update FETCH_OLD in this script')
    html = html.replace(FETCH_OLD, FETCH_NEW, 1)
    html = html.replace('<script>', '<script>window.EMBED=%s;</script>\n<script>' % json.dumps(embed), 1)

    open(OUT, 'w').write(html)
    print('wrote %s (%.1f MB)' % (OUT, os.path.getsize(OUT) / 1e6), file=sys.stderr)


if __name__ == '__main__':
    main()
