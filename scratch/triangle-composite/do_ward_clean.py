import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from composite import add_grain, distress, draw_tri, erase_lettering, screen_glow

SRC = '/home/user/painbet/scratch/refs/ref_ward_clean.jpg'
OUT = '/home/user/painbet/scratch/refs/ref_ward_clean_tri.jpg'


im = Image.open(SRC).convert('RGB')

# 1. the word EXIT comes off the sign --------------------------------------
PANEL = (499, 599, 578, 659)
erase_lettering(im, PANEL)
add_grain(im, PANEL, amount=4, seed=11)

# 2. a red triangle takes its place -----------------------------------------
tri = draw_tri(im.size, cx=538, cy=629, w=46, h=39, fill=255)
im.paste(Image.new('RGB', im.size, (255, 238, 232)), (0, 0), tri)
im = screen_glow(im, tri, (255, 44, 32), radius=8, strength=1.0)
im = screen_glow(im, tri, (255, 22, 15), radius=26, strength=0.5)

# 3. stencil triangle on the doors, directly above the 07 -------------------
# The lit seam between the two leaves runs through it, which is correct: the
# stencil is sprayed across both doors. Drawn a touch larger so it still
# reads as a triangle and not an arrow.
door = distress(draw_tri(im.size, cx=543, cy=726, w=32, h=25, fill=255), seed=31, edge=0.7)
im.paste(Image.new('RGB', im.size, (178, 180, 174)), (0, 0),
         door.point(lambda v: int(v * 0.90)))

im.save(OUT, quality=95)
Image.open(OUT).crop((400, 550, 700, 830)).resize((900, 840), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_clean.png')
print('ok')
