import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from composite import add_grain, distress, draw_tri, erase_lettering, screen_glow

SRC = '/home/user/painbet/scratch/refs/ref_ward_decayed.jpg'
OUT = '/home/user/painbet/scratch/refs/ref_ward_decayed_tri.jpg'

im = Image.open(SRC).convert('RGB')

# 1. the big sign at the top of frame, cropped by the frame edge ------------
TOP = (378, 0, 684, 101)
erase_lettering(im, TOP, g_thresh=60)
add_grain(im, TOP, amount=5, seed=3)

top_tri = draw_tri(im.size, cx=531, cy=50, w=97, h=84, fill=255)
im.paste(Image.new('RGB', im.size, (255, 226, 220)), (0, 0), top_tri)
im = screen_glow(im, top_tri, (255, 40, 28), radius=14, strength=1.0)
im = screen_glow(im, top_tri, (255, 20, 12), radius=44, strength=0.6)

# 2. the sign above the doorframe -------------------------------------------
DOOR_SIGN = (484, 631, 592, 697)
erase_lettering(im, DOOR_SIGN, g_thresh=70)
add_grain(im, DOOR_SIGN, amount=4, seed=5)

sign_tri = draw_tri(im.size, cx=538, cy=664, w=48, h=41, fill=255)
im.paste(Image.new('RGB', im.size, (255, 234, 228)), (0, 0), sign_tri)
im = screen_glow(im, sign_tri, (255, 44, 32), radius=9, strength=1.0)
im = screen_glow(im, sign_tri, (255, 22, 15), radius=30, strength=0.55)

# 3. stencil triangle above the 07 ------------------------------------------
# On this plate the numerals sit left of the seam rather than straddling it,
# so the triangle is centred on the numerals, not on the doors.
stencil = distress(draw_tri(im.size, cx=477, cy=752, w=54, h=45, fill=255),
                   seed=21, scale=5, depth=0.3, edge=0.6)
im.paste(Image.new('RGB', im.size, (196, 199, 191)), (0, 0),
         stencil.point(lambda v: int(v * 0.92)))

im.save(OUT, quality=95)
Image.open(OUT).crop((400, 580, 700, 880)).resize((900, 900), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_dec_door.png')
Image.open(OUT).crop((250, 0, 830, 130)).resize((1160, 260), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_dec_top.png')
print('ok')
