"""compose review boards for the Vortex rear pass r4 (reviewer round-3 fixes; PIL; writes into preview/opus_rear).
Round-3 images come from the r3 backup (_backup_opus_rear_r3_20261017), round-4 from preview/opus_rear and
shading/proof (both rendered from the r4 export FBX files)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "preview", "opus_rear")
R3 = os.path.join(HERE, "_backup_opus_rear_r3_20261017")
R3P = os.path.join(R3, "preview_opus_rear_r3final")
R3S = os.path.join(R3, "shading_proof")
PR = os.path.join(HERE, "shading", "proof")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))
T = "r4final"
try:
    F = ImageFont.truetype("arialbd.ttf", 30)
    f = ImageFont.truetype("arial.ttf", 22)
except Exception:
    F = f = ImageFont.load_default()


def fit(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def board(title, panels, out, h=760):
    ims = [fit(p if isinstance(p, Image.Image) else Image.open(p).convert("RGB"), h) for p, _ in panels]
    Wd = sum(i.width for i in ims) + 12 * (len(ims) + 1)
    B = Image.new("RGB", (Wd, h + 110), (24, 24, 28))
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


def crop3(path, box, out):
    """box in fractions of the frame (x0, y0, x1, y1); 3x LANCZOS upscale"""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    c = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    c = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    c.save(out)
    return out


board("Vortex rear pass r4 - rear 3/4 macro vs closest real reference",
      [(P(T + "_rear_macro.png"), "Vortex r4, rear 3/4 macro (exported FBX, Cycles)"),
       (os.path.join(REF, "rear_ref_02_white_wedge_supercar_1990s.jpg"), "rear_ref_02 (real loose early-90s casting)")],
      "review_compare.png")
board("Chase camera (17 deg, 3 car lengths, 40 mm) - beside the approved Navvy",
      [(P(T + "_chase_family.png"), "Vortex r4 + Navvy (Navvy's existing FBX, read-only)")], "review_chase_family_board.png")
board("Chase camera - round 3 (left) vs round 4 (right)",
      [(os.path.join(R3P, "r3final_chase.png"), "r3 (failed review)"), (P(T + "_chase.png"), "r4")],
      "review_chase_before_after.png", h=600)
# fix 8: 3x crops of the chase frame over the sails / haunches and the rear window (game distance)
box = (0.36, 0.33, 0.64, 0.52)
a = crop3(os.path.join(R3P, "r3final_chase.png"), box, P("_crop3_chase_sails_r3.png"))
b = crop3(P(T + "_chase.png"), box, P("_crop3_chase_sails_r4.png"))
board("Chase camera, 3x crop of the sails, haunches and rear window - r3 vs r4",
      [(a, "r3: dark wavy door lines on the sails, grey window box"), (b, "r4")], "review_chase_sails_crop3x.png", h=560)
board("Rear 3/4 macro - round 3 vs round 4",
      [(os.path.join(R3P, "r3final_rear_macro.png"), "r3"), (P(T + "_rear_macro.png"), "r4")],
      "review_rear_macro_before_after.png", h=640)
board("C-pillars from above and behind (left / right) - r3 export vs r4 export",
      [(os.path.join(R3P, "r3final_cpillar_L.png"), "r3 left"), (P(T + "_cpillar_L.png"), "r4 left"),
       (os.path.join(R3P, "r3final_cpillar_R.png"), "r3 right"), (P(T + "_cpillar_R.png"), "r4 right")],
      "review_cpillars_before_after.png", h=520)
board("Side scoop (right) - r3 vs r4",
      [(os.path.join(R3P, "r3final_scoop_R.png"), "r3 (zig-zag fins, mottled smears)"), (P(T + "_scoop_R.png"), "r4")],
      "review_scoop_before_after.png", h=600)
board("Bay / rear window close - r3 vs r4",
      [(os.path.join(R3P, "r3final_bay_close.png"), "r3"), (P(T + "_bay_close.png"), "r4")],
      "review_bay_close_before_after.png", h=600)
board("Tail corner - r3 vs r4",
      [(os.path.join(R3P, "r3final_tail_corner.png"), "r3 (print high, dark pod end wall)"), (P(T + "_tail_corner.png"), "r4")],
      "review_tail_corner_before_after.png", h=600)
for v, cap in (("clay_sideglass_L", "side glass / scoop / door lines, clay"),
               ("paint_sideglass_L", "side glass / scoop / door lines, paint"),
               ("clay_cpillar_L", "C-pillar left, clay"), ("clay_cpillar_R", "C-pillar right, clay"),
               ("clay_tail_R", "tail right, clay"), ("clay_toprear", "top rear, clay")):
    pa, pb = os.path.join(R3S, "proof_%s.png" % v), os.path.join(PR, "proof_%s.png" % v)
    if os.path.exists(pa) and os.path.exists(pb):
        board("Grazing-light proof (1024 spp, no denoiser): %s - r3 vs r4" % cap,
              [(pa, "r3"), (pb, "r4")], "review_proof_%s_r3_r4.png" % v, h=600)
# front regression: the pre-rear-pass baseline, r3 and r4 + x4 difference r3 -> r4
b3 = Image.open(os.path.join(R3P, "r3final_hero.png")).convert("RGB")
c4 = Image.open(P(T + "_hero.png")).convert("RGB")
dif = ImageChops.difference(b3, c4).point(lambda v: min(255, v * 4))
dif.save(P("_diff_hero_r3_r4_x4.png"))
board("Front hero regression - 16 Oct baseline / r3 / r4 / |r3 - r4| x4",
      [(P("before_hero.png"), "16 Oct (before the rear passes)"), (os.path.join(R3P, "r3final_hero.png"), "r3"),
       (P(T + "_hero.png"), "r4"), (P("_diff_hero_r3_r4_x4.png"), "|r3 - r4| x4")],
      "review_front_hero_before_after.png", h=480)
