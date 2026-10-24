"""compose review boards for the Vortex rear pass r3 (PIL; writes into preview/opus_rear)"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

V = r"C:\Users\PC\Desktop\CozyCarGame\SourceArt\Blender\Vortex\preview\opus_rear"
REF = r"C:\Users\PC\Desktop\CozyCarGame\Docs\Reference\DieCast"
T = "r3final"
try:
    F = ImageFont.truetype("arialbd.ttf", 30)
    f = ImageFont.truetype("arial.ttf", 22)
except Exception:
    F = f = ImageFont.load_default()


def fit(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def board(title, panels, out, h=760):
    ims = [fit(Image.open(p).convert("RGB"), h) for p, _ in panels]
    W = sum(i.width for i in ims) + 12 * (len(ims) + 1)
    B = Image.new("RGB", (W, h + 110), (24, 24, 28))
    d = ImageDraw.Draw(B)
    d.text((14, 12), title, font=F, fill=(240, 240, 240))
    x = 12
    for im, (_, cap) in zip(ims, panels):
        B.paste(im, (x, 56))
        d.text((x + 4, 56 + h + 12), cap, font=f, fill=(225, 225, 225))
        x += im.width + 12
    B.save(os.path.join(V, out))
    print("wrote", out)


def P(n):
    return os.path.join(V, n)


board("Vortex rear pass r3 - rear 3/4 macro vs closest real reference",
      [(P(T + "_rear_macro.png"), "Vortex r3, rear 3/4 macro (exported FBX, Cycles)"),
       (os.path.join(REF, "rear_ref_02_white_wedge_supercar_1990s.jpg"), "rear_ref_02 (real loose early-90s casting)")],
      "review_compare.png")
board("Chase camera (17 deg, 3 car lengths, 40 mm) - beside the approved Navvy",
      [(P(T + "_chase_family.png"), "Vortex r3 + Navvy (Navvy's existing FBX, read-only)")], "review_chase_family_board.png")
board("Chase camera - round 2 (left) vs round 3 (right)",
      [(P("final_chase.png"), "r2 (failed review)"), (P(T + "_chase.png"), "r3")], "review_chase_before_after.png", h=600)
board("Rear 3/4 macro - round 2 vs round 3",
      [(P("final_rear_macro.png"), "r2"), (P(T + "_rear_macro.png"), "r3")], "review_rear_macro_before_after.png", h=640)
board("Bay / C-pillars from behind - round 2 vs round 3",
      [(P("final_bay_close.png"), "r2 (torn C-pillar cut-outs, tail-corner slits)"), (P(T + "_bay_close.png"), "r3")],
      "review_bay_close_before_after.png", h=640)
board("C-pillars from above and behind (left / right) - round 2 export vs round 3 export",
      [(P("r3exp_cpillar_L.png"), "r2 left"), (P(T + "_cpillar_L.png"), "r3 left"),
       (P("r3exp_cpillar_R.png"), "r2 right"), (P(T + "_cpillar_R.png"), "r3 right")],
      "review_cpillars_before_after.png", h=520)
board("Side glass - round 2 vs round 3",
      [(P("r3exp_side_glass.png"), "r2 (lumpy S-shaped shell)"), (P(T + "_side_glass.png"), "r3 (fair slab)")],
      "review_side_glass_before_after.png", h=600)
board("Tail corner - round 2 vs round 3",
      [(P("r3exp_tail_corner.png"), "r2 (rocker-step slit, ragged stripe end)"), (P(T + "_tail_corner.png"), "r3")],
      "review_tail_corner_before_after.png", h=600)
# front regression: the pre-rear-pass baseline, r2 and r3 + x4 difference r2 -> r3
a = Image.open(P("before_hero.png")).convert("RGB")
b = Image.open(P("final_hero.png")).convert("RGB")
c = Image.open(P(T + "_hero.png")).convert("RGB")
dif = ImageChops.difference(b, c).point(lambda v: min(255, v * 4))
dif.save(P("_diff_hero_r2_r3_x4.png"))
board("Front hero regression - 16 Oct baseline / r2 / r3 / |r2 - r3| x4",
      [(P("before_hero.png"), "16 Oct (before the rear passes)"), (P("final_hero.png"), "r2"),
       (P(T + "_hero.png"), "r3"), (P("_diff_hero_r2_r3_x4.png"), "|r2 - r3| x4")],
      "review_front_hero_before_after.png", h=480)
