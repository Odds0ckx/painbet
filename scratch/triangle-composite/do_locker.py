import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageFilter
from composite import distress, draw_tri, interpolate_fill, screen_glow

SRC = '/home/user/painbet/scratch/refs/ref_locker.jpg'
OUT = '/home/user/painbet/scratch/refs/ref_locker_tri.jpg'

im = Image.open(SRC).convert('RGB')

# 1. take the biohazard trefoil off the drawer face --------------------------
# The trefoil is the one thing on these plates the brief negative-prompts, and
# it is what the seal light has to replace. Pale pink on dark red separates on
# the green channel the same way the sign lettering did.
TREFOIL = (489, 966, 538, 1033)
interpolate_fill(im, TREFOIL, seed=41)

# 2. a glowing red triangle seal light in its place ---------------------------
# It has to read as an emitting seal light, not painted geometry: a hot
# red-white core, then two glows so the light actually spills onto the metal
# around it the way the sign panels do.
seal = draw_tri(im.size, cx=512, cy=1000, w=42, h=36, fill=255)
im = screen_glow(im, seal, (255, 26, 16), radius=26, strength=0.95)
im = screen_glow(im, seal, (255, 40, 26), radius=9, strength=1.0)
im.paste(Image.new('RGB', im.size, (255, 158, 140)), (0, 0),
         seal.filter(ImageFilter.GaussianBlur(0.7)))
im = screen_glow(im, seal, (255, 90, 70), radius=2, strength=0.9)

im.save(OUT, quality=95)
Image.open(OUT).crop((430, 930, 700, 1080)).resize((1080, 600), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_locker.png')
print('ok')
