"""Shared helpers for compositing the pain.bet triangle into the reference stills.

The stills in `scratch/refs/` were pulled from the finished footage, so they
carry the exact grade of the shot clips. Regenerating them from scratch would
lose that, so the brand geometry the footage never had is composited on
instead. One script per plate sits alongside this module.

Triangles are drawn at 4x and downsampled so their edges carry the same
softness as the plate, then worn and grain-matched to what surrounds them.
"""

import random
from PIL import Image, ImageDraw, ImageFilter

SS = 4  # supersample factor


# --- geometry -----------------------------------------------------------


def tri_points(cx, cy, w, h):
    """Triangle, point up, centred on (cx, cy)."""
    return [(cx, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def draw_tri(size, cx, cy, w, h, fill=255):
    """An image-sized L mask with a supersampled triangle drawn on it."""
    m = Image.new("L", (size[0] * SS, size[1] * SS), 0)
    ImageDraw.Draw(m).polygon(tri_points(cx * SS, cy * SS, w * SS, h * SS), fill=fill)
    return m.resize(size, Image.LANCZOS)


def grain(size, amount, seed=7):
    """Monochrome noise, loosely matched to the plates' 35mm grain."""
    rnd = random.Random(seed)
    n = Image.new("L", size)
    n.putdata([max(0, min(255, int(rnd.gauss(128, amount)))) for _ in range(size[0] * size[1])])
    return n


def distress(mask, seed=13, scale=9, depth=0.55, edge=1.1):
    """Wear a stencil mask down so it sits like weathered paint.

    A low-frequency noise field thins the fill unevenly and a slight blur eats
    the edges, which is what stops a drawn triangle reading as vector art next
    to the plate's chipped numerals.
    """
    w, h = mask.size
    n = grain((max(1, w // scale), max(1, h // scale)), 70, seed).resize(mask.size, Image.BICUBIC)
    n = n.point(lambda v: int(255 - (255 - v) * depth))
    worn = Image.new("L", mask.size)
    worn.putdata([m * v // 255 for m, v in zip(mask.getdata(), n.getdata())])
    return worn.filter(ImageFilter.GaussianBlur(edge))


# --- removing what is already there --------------------------------------


def add_grain(im, box, amount=5, seed=7):
    region = im.crop(box)
    n = grain((box[2] - box[0], box[3] - box[1]), amount, seed).convert("RGB")
    im.paste(Image.blend(region, Image.blend(region, n, 0.5), 0.35), box[:2])


def erase_lettering(im, box, g_thresh=70, smear=0.9, feather=5):
    """Take the lettering off an illuminated red sign.

    The panel red sits near (170,28,26) and the lettering near (255,235,225),
    so the two separate cleanly on the green channel. Each lit pixel becomes
    the median of the unlit pixels on its own row, which keeps the panel's
    vertical falloff and its bloom instead of flattening them.
    """
    x0, y0, x1, y1 = box
    px = im.load()
    for y in range(y0, y1):
        keep = [px[x, y] for x in range(x0, x1) if px[x, y][1] <= g_thresh]
        if len(keep) < 4:
            continue
        keep.sort(key=lambda c: c[0])
        med = keep[len(keep) // 2]
        for x in range(x0, x1):
            if px[x, y][1] > g_thresh:
                px[x, y] = med

    # The median pass alone leaves faint letterforms wherever a stroke's
    # anti-aliased edge fell under the threshold. Letters are vertical strokes,
    # so a horizontal-only smear (drop the x resolution, put it back) erases
    # what is left while the panel's vertical falloff survives intact.
    w, h = x1 - x0, y1 - y0
    region = im.crop(box)
    smeared = region.resize((max(1, w // 12), h), Image.LANCZOS) \
                    .resize((w, h), Image.LANCZOS)
    soft = Image.blend(region, smeared, smear).filter(ImageFilter.GaussianBlur(1.2))

    # Feathered, or the patch runs onto the sign housing and shows as a
    # rectangle around the panel.
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((feather, feather, w - feather, h - feather), fill=255)
    im.paste(soft, (x0, y0), mask.filter(ImageFilter.GaussianBlur(feather * 0.9)))


def interpolate_fill(im, box, seed=1, noise=4):
    """Rebuild a strip by interpolating across it from the columns either side.

    The locker's drawer face is lit brightly enough on the left that the
    biohazard trefoil and the metal overlap in every channel, so no threshold
    separates them the way it does on the sign panels. Interpolating each row
    between the clean column just left of the marking and the clean column
    just right of it sidesteps segmentation entirely, and because the fill
    meets the plate exactly at both edges there is no patch boundary to see.
    """
    x0, y0, x1, y1 = box
    px = im.load()
    rnd = random.Random(seed)
    span = x1 - x0
    for y in range(y0, y1):
        left, right = px[x0 - 1, y], px[x1, y]
        for i in range(span):
            t = (i + 1) / (span + 1)
            n = rnd.gauss(0, noise)
            px[x0 + i, y] = tuple(
                max(0, min(255, int(a + (b - a) * t + n))) for a, b in zip(left, right)
            )
    im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(0.8)), (x0, y0))


# --- lighting -----------------------------------------------------------


def screen_glow(im, mask, colour, radius, strength):
    """Screen a blurred copy of `mask` over the plate as emitted light.

    Screen rather than paste, so the glow lifts what is already there instead
    of replacing it and never clips to a flat patch of colour.
    """
    g = mask.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * strength))
    px_g = list(g.getdata())
    out = []
    for ch, c in zip(im.split(), colour):
        data = [
            255 - (255 - s) * (255 - gv * c // 255) // 255
            for s, gv in zip(ch.getdata(), px_g)
        ]
        band = Image.new("L", im.size)
        band.putdata(data)
        out.append(band)
    return Image.merge("RGB", out)
