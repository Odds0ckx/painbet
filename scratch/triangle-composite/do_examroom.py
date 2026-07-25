import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from composite import distress, draw_tri, screen_glow

SRC = '/home/user/painbet/scratch/refs/ref_examroom.jpg'
OUT = '/home/user/painbet/scratch/refs/ref_examroom_tri.jpg'

im = Image.open(SRC).convert('RGB')

# 1. stencil triangle above the 07 -------------------------------------------
# This is the oblique interior view: the seam, the panel moulding and the lit
# door edge all cross the space directly above the numerals, and a triangle
# placed there straddles the moulding and reads as a decal. It goes in the
# clear field above the 0 on the near leaf instead, which from this angle
# still reads as sitting above the number.
stencil = distress(draw_tri(im.size, cx=252, cy=778, w=46, h=38, fill=255),
                   seed=17, scale=6, depth=0.32, edge=0.7)
im.paste(Image.new('RGB', im.size, (214, 216, 210)), (0, 0),
         stencil.point(lambda v: int(v * 0.93)))

# 2. the triangle in the chest x-ray -----------------------------------------
# On a PA film the heart projects to the viewer's right of the spine, so the
# triangle sits there rather than over the vertebrae. It is rendered as a
# dense bright mass, not a dark one: on this plate the lungs read dark and
# dense tissue reads bright, so a dark triangle over a lung field vanishes.
heart = distress(draw_tri(im.size, cx=897, cy=906, w=58, h=50, fill=255),
                 seed=23, scale=7, depth=0.20, edge=1.6)
im = screen_glow(im, heart, (255, 150, 138), radius=1.8, strength=0.82)
im = screen_glow(im, heart, (255, 70, 60), radius=9, strength=0.45)

im.save(OUT, quality=95)
Image.open(OUT).crop((60, 690, 420, 1030)).resize((1080, 1020), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_e_door.png')
Image.open(OUT).crop((740, 690, 1020, 1040)).resize((840, 1050), Image.LANCZOS) \
    .save('/home/user/painbet/scratch/triangle-composite/preview/check_e_xray.png')
print('ok')
