"""review_boards_r5b.py - Vortex rear pass r5, second attempt ('r5b'): review boards (PIL, system Python).
Writes preview/opus_rear_r5b/. Every board carries the provenance stamp: build-script sha256 + mtime and the export
health.json (written, pass, tris) of the export the r5b renders were made from.
Compared states: 16 Oct baseline + r4 (from _backup_opus_rear_r5_20261017), r5 = the gate-failed first attempt
(preview/opus_rear_r5, shading/proof_r5, shading/zebra_r5), r5b = this pass (preview/opus_rear_r5b, shading/proof_r5b,
shading/zebra_r5b).
  python review_boards_r5b.py"""
import hashlib
import json
import os
import time

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "preview", "opus_rear_r5b")
R5 = os.path.join(HERE, "preview", "opus_rear_r5")
R4 = os.path.join(HERE, "_backup_opus_rear_r5_20261017")
R4P = os.path.join(R4, "preview", "opus_rear")
PR5 = os.path.join(HERE, "shading", "proof_r5")
PR = os.path.join(HERE, "shading", "proof_r5b")
ZB5 = os.path.join(HERE, "shading", "zebra_r5")
ZB = os.path.join(HERE, "shading", "zebra_r5b")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))
T = "r5b"
try:
    F = ImageFont.truetype("arialbd.ttf", 28)
    f = ImageFont.truetype("arial.ttf", 20)
    fs = ImageFont.truetype("arial.ttf", 16)
except Exception:
    F = f = fs = ImageFont.load_default()

BUILD = os.path.join(HERE, "build_Vortex.py")
SHA = hashlib.sha256(open(BUILD, "rb").read()).hexdigest()
HJ = json.load(open(os.path.join(HERE, "export", "health.json")))
STAMP = ("build_Vortex.py sha256 %s.. mtime %s | export health.json written %s, pass=%s, script sha %s.. | tris %s"
         % (SHA[:12], time.ctime(os.path.getmtime(BUILD)), HJ.get("written"), HJ.get("pass"),
            HJ.get("build_script_sha256", "")[:12],
            ", ".join("%s %d" % (k.replace("SM_Vortex_", ""), v["summary"]["tris"]) for k, v in HJ["parts"].items())))


def fit(im, h):
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def board(title, panels, out, h=640):
    ims = [fit(p if isinstance(p, Image.Image) else Image.open(p).convert("RGB"), h) for p, _ in panels]
    Wd = max(sum(i.width for i in ims) + 12 * (len(ims) + 1), 1400)
    B = Image.new("RGB", (Wd, h + 130), (24, 24, 28))
    d = ImageDraw.Draw(B)
    d.text((14, 10), title, font=F, fill=(240, 240, 240))
    x = 12
    for im, (_, cap) in zip(ims, panels):
        B.paste(im, (x, 52))
        d.text((x + 4, 52 + h + 10), cap, font=f, fill=(225, 225, 225))
        x += im.width + 12
    d.text((14, h + 104), STAMP, font=fs, fill=(150, 150, 160))
    B.save(os.path.join(V, out))
    print("wrote", out)


def P(n):
    return os.path.join(V, n)


def crop3(path, box, out, s=3):
    im = Image.open(path).convert("RGB")
    c = im.crop(box)
    c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
    c.save(out)
    return out


def x4(a, b, out):
    A = Image.open(a).convert("RGB"); Bm = Image.open(b).convert("RGB")
    if A.size != Bm.size:
        Bm = Bm.resize(A.size, Image.LANCZOS)
    ImageChops.difference(A, Bm).point(lambda v: min(255, v * 4)).save(out)
    return out


def both(name5, name5b, box, tag):
    """3x crops of the same box in the r5 and r5b frame"""
    a = crop3(os.path.join(R5, name5), box, P("_c3_%s_r5.png" % tag))
    b = crop3(P(name5b), box, P("_c3_%s_r5b.png" % tag))
    return a, b


if __name__ == "__main__":
    os.makedirs(V, exist_ok=True)
    board("Vortex r5b - chase camera (17 deg, 3 car lengths, 40 mm) and beside Navvy",
          [(P(T + "_chase.png"), "r5b chase"), (P(T + "_chase_family.png"), "r5b + Navvy (Navvy FBX read-only)")],
          "board_chase_family.png", h=520)
    board("Vortex r5b - rear 3/4 macro beside real early-90s castings",
          [(P(T + "_rear_macro.png"), "r5b rear 3/4 macro"),
           (os.path.join(REF, "rear_ref_01_red_wedge_supercar_1990s.jpg"), "rear_ref_01"),
           (os.path.join(REF, "rear_ref_02_white_wedge_supercar_1990s.jpg"), "rear_ref_02")],
          "board_rear_refs.png", h=560)
    # fix 6 (rule 14): standard 3/4-rear frame at axle height, r5 vs r5b + 3x crops of the gate's box
    a, b = both("r5_rear_axle34.png", T + "_rear_axle34.png", (850, 500, 1250, 800), "axle34")
    board("Fix 6 - 3/4 rear at axle height (lead ruling: steel stub between tyre and body), r5 vs r5b",
          [(os.path.join(R5, "r5_rear_axle34.png"), "r5"), (P(T + "_rear_axle34.png"), "r5b"),
           (a, "r5 3x (850,500)-(1250,800)"), (b, "r5b 3x same box")], "board_rear_axle.png", h=440)
    board("Rear low, straight behind (axle may hide behind the tail paint) - r5 vs r5b",
          [(os.path.join(R5, "r5_rear_low.png"), "r5"), (P(T + "_rear_low.png"), "r5b")], "board_rear_low.png", h=520)
    # fixes 1 + 2: corner_R / cpillar_R paint and clay, 3x crops of the gate's boxes
    a1, b1 = both("r5_corner_R.png", T + "_corner_R.png", (760, 450, 1200, 780), "corner_paint")
    a2, b2 = both("r5clay_corner_R.png", T + "clay_corner_R.png", (760, 450, 1200, 780), "corner_clay")
    board("Fixes 1 + 2 - corner_R 3x (760,450)-(1200,780): blotch under the window corner, haunch dashes",
          [(a1, "r5 paint"), (b1, "r5b paint"), (a2, "r5 clay"), (b2, "r5b clay")], "board_corner_R_r5_r5b.png", h=440)
    a3, b3 = both("r5_cpillar_R.png", T + "_cpillar_R.png", (760, 380, 1000, 620), "cpR_paint")
    board("Fix 1 - cpillar_R paint 3x (760,380)-(1000,620): the dark patch below the window's rear-lower corner",
          [(a3, "r5"), (b3, "r5b")], "board_cpillar_R_crop_r5_r5b.png", h=600)
    board("C-pillars from above and behind - r5 vs r5b",
          [(os.path.join(R5, "r5_cpillar_L.png"), "r5 left"), (P(T + "_cpillar_L.png"), "r5b left"),
           (os.path.join(R5, "r5_cpillar_R.png"), "r5 right"), (P(T + "_cpillar_R.png"), "r5b right")],
          "board_cpillars_r5_r5b.png", h=480)
    board("Side glass / door lines (left) - r5 vs r5b",
          [(os.path.join(R5, "r5_side_glass.png"), "r5"), (P(T + "_side_glass.png"), "r5b")],
          "board_side_glass_r5_r5b.png", h=560)
    board("Rear 3/4 macro - r5 vs r5b",
          [(os.path.join(R5, "r5_rear_macro.png"), "r5"), (P(T + "_rear_macro.png"), "r5b")],
          "board_rear_macro_r5_r5b.png", h=560)
    board("Tail corner (left, low) - r5 vs r5b (fix 7)",
          [(os.path.join(R5, "r5_tail_corner.png"), "r5"), (P(T + "_tail_corner.png"), "r5b")],
          "board_tail_corner_r5_r5b.png", h=560)
    # front regression: 16 Oct / r4 / r5 / r5b + x4 differences against 16 Oct and r4
    h16 = os.path.join(R4P, "before_hero.png")
    h4 = os.path.join(R4P, "r4final_hero.png")
    h5 = os.path.join(R5, "r5_hero.png")
    h5b = P(T + "_hero.png")
    d16 = x4(h16, h5b, P("_diff_hero_16oct_r5b_x4.png"))
    d4 = x4(h4, h5b, P("_diff_hero_r4_r5b_x4.png"))
    d5 = x4(h5, h5b, P("_diff_hero_r5_r5b_x4.png"))
    board("Front hero regression - 16 Oct / r4 / r5 / r5b / |16 Oct - r5b| x4 / |r4 - r5b| x4 / |r5 - r5b| x4",
          [(h16, "16 Oct"), (h4, "r4"), (h5, "r5"), (h5b, "r5b"), (d16, "|16 Oct - r5b| x4"), (d4, "|r4 - r5b| x4"),
           (d5, "|r5 - r5b| x4")], "board_front_hero.png", h=300)
    nose = (380, 520, 840, 740)
    board("Front hero, 3x nose crop (380,520)-(840,740): 16 Oct / r4 / r5b",
          [(crop3(h16, nose, P("_crop3_nose_16oct.png")), "16 Oct"), (crop3(h4, nose, P("_crop3_nose_r4.png")), "r4"),
           (crop3(h5b, nose, P("_crop3_nose_r5b.png")), "r5b")], "board_front_nose_crop3x.png", h=440)
    cab = (560, 360, 1120, 680)
    board("Front hero, 3x windscreen crop: tub through ~55 % glass (16 Oct / r5 / r5b)",
          [(crop3(h16, cab, P("_crop3_hero_cab_16oct.png")), "16 Oct"),
           (crop3(h5, cab, P("_crop3_hero_cab_r5.png")), "r5"),
           (crop3(h5b, cab, P("_crop3_hero_cab_r5b.png")), "r5b")], "board_front_cab_crop3x.png", h=480)
    # grazing-light proofs r5 vs r5b
    for v, cap in (("clay_cpillar_R", "C-pillar right, clay"), ("paint_cpillar_R", "C-pillar right, paint"),
                   ("clay_cpillar_L", "C-pillar left, clay"), ("clay_toprear", "top rear, clay"),
                   ("clay_sideglass_L", "side glass / door lines, clay"),
                   ("paint_sideglass_L", "side glass / door lines, paint"), ("clay_tail_R", "tail right, clay"),
                   ("paint_tail_R", "tail right, paint")):
        pa, pb = os.path.join(PR5, "proof_%s.png" % v), os.path.join(PR, "proof_%s.png" % v)
        if os.path.exists(pa) and os.path.exists(pb):
            board("Grazing-light proof (1024 spp, no denoiser): %s - r5 vs r5b" % cap, [(pa, "r5"), (pb, "r5b")],
                  "board_proof_%s_r5_r5b.png" % v, h=560)
    for v in ("cpillar_R", "cpillar_L", "sideglass_L", "sideglass_R", "shoulder_R", "rear34_R"):
        pa = os.path.join(ZB5, "zebra_Vortex_export_%s.png" % v)
        pb = os.path.join(ZB, "zebra_Vortex_export_%s.png" % v)
        if os.path.exists(pa) and os.path.exists(pb):
            board("Zebra %s - r5 export vs r5b export" % v, [(pa, "r5"), (pb, "r5b")], "board_zebra_%s_r5_r5b.png" % v, h=560)
    print(STAMP)
