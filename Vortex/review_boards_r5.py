"""review_boards_r5.py - compose the Vortex rear pass r5 review boards (PIL; system Python; writes preview/opus_rear_r5).
Every board carries the provenance stamp: build-script sha256 + mtime and the export health.json (written, pass, tris)
of the export the renders were made from. Round-4 images come from _backup_opus_rear_r5_20261017 (the r4 state),
round-5 from preview/opus_rear_r5 and shading/proof_r5 (all rendered from the r5 production export).
  python review_boards_r5.py"""
import hashlib
import json
import os
import time

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "preview", "opus_rear_r5")
R4 = os.path.join(HERE, "_backup_opus_rear_r5_20261017")
R4P = os.path.join(R4, "preview", "opus_rear")
R4S = os.path.join(R4, "shading", "proof")
PR = os.path.join(HERE, "shading", "proof_r5")
ZB = os.path.join(HERE, "shading", "zebra_r5")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))
T = "r5"
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
    """box in pixels (x0, y0, x1, y1) of the source frame; s x LANCZOS upscale"""
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


if __name__ == "__main__":
    os.makedirs(V, exist_ok=True)
    # fix 8 / rule 15: chase, macro, axle-height 3/4, beside the refs and Navvy
    board("Vortex r5 - chase camera (17 deg, 3 car lengths, 40 mm) and beside Navvy",
          [(P(T + "_chase.png"), "r5 chase (from the r5 export)"), (P(T + "_chase_family.png"), "r5 + Navvy (Navvy FBX read-only)")],
          "board_chase_family.png", h=520)
    board("Vortex r5 - rear 3/4 macro beside real early-90s castings",
          [(P(T + "_rear_macro.png"), "r5 rear 3/4 macro"),
           (os.path.join(REF, "rear_ref_01_red_wedge_supercar_1990s.jpg"), "rear_ref_01"),
           (os.path.join(REF, "rear_ref_02_white_wedge_supercar_1990s.jpg"), "rear_ref_02")],
          "board_rear_refs.png", h=560)
    board("Vortex r5 - rear low 3/4 at axle height (lead ruling: steel axle between tyre and body) / straight rear low",
          [(P(T + "_rear_axle34.png"), "r5 3/4 rear at axle height"), (P(T + "_rear_low.png"), "r5 straight behind, low")],
          "board_rear_axle.png", h=560)
    board("C-pillars from above and behind - r4 vs r5 (fix 1, fix 3)",
          [(os.path.join(R4P, "r4final_cpillar_L.png"), "r4 left"), (P(T + "_cpillar_L.png"), "r5 left"),
           (os.path.join(R4P, "r4final_cpillar_R.png"), "r4 right"), (P(T + "_cpillar_R.png"), "r5 right")],
          "board_cpillars_r4_r5.png", h=480)
    board("Side scoop (right) - r4 vs r5 (fix 6)",
          [(os.path.join(R4P, "r4final_scoop_R.png"), "r4"), (P(T + "_scoop_R.png"), "r5")], "board_scoop_r4_r5.png", h=560)
    board("Side glass / door lines (left) - r4 vs r5 (fixes 1, 4, 6)",
          [(os.path.join(R4P, "r4final_side_glass.png"), "r4"), (P(T + "_side_glass.png"), "r5")],
          "board_side_glass_r4_r5.png", h=560)
    board("Rear 3/4 macro - r4 vs r5 (fix 7: no print on the ducktail behind the bay)",
          [(os.path.join(R4P, "r4final_rear_macro.png"), "r4"), (P(T + "_rear_macro.png"), "r5")],
          "board_rear_macro_r4_r5.png", h=560)
    # front regression (fix 5): 16 Oct / r4 / r5 + x4 differences
    h16 = os.path.join(R4P, "before_hero.png")
    h4 = os.path.join(R4P, "r4final_hero.png")
    h5 = P(T + "_hero.png")
    d16 = x4(h16, h5, P("_diff_hero_16oct_r5_x4.png"))
    d4 = x4(h4, h5, P("_diff_hero_r4_r5_x4.png"))
    board("Front hero regression - 16 Oct baseline / r4 / r5 / |16 Oct - r5| x4 / |r4 - r5| x4",
          [(h16, "16 Oct"), (h4, "r4"), (h5, "r5"), (d16, "|16 Oct - r5| x4"), (d4, "|r4 - r5| x4")],
          "board_front_hero.png", h=380)
    cab = (560, 360, 1120, 680)
    board("Front hero, 3x crop of the windscreen (fix 5: dark-grey tub through ~55 % glass)",
          [(crop3(h16, cab, P("_crop3_hero_cab_16oct.png")), "16 Oct"),
           (crop3(h4, cab, P("_crop3_hero_cab_r4.png")), "r4 (near-opaque)"),
           (crop3(h5, cab, P("_crop3_hero_cab_r5.png")), "r5")], "board_front_cab_crop3x.png", h=480)
    # grazing-light proofs r4 vs r5
    for v, cap in (("clay_cpillar_R", "C-pillar right, clay"), ("paint_cpillar_R", "C-pillar right, paint"),
                   ("clay_cpillar_L", "C-pillar left, clay"), ("clay_toprear", "top rear, clay"),
                   ("clay_sideglass_L", "side glass / scoop / door lines, clay"),
                   ("paint_sideglass_L", "side glass / scoop / door lines, paint"), ("clay_tail_R", "tail right, clay")):
        pa, pb = os.path.join(R4S, "proof_%s.png" % v), os.path.join(PR, "proof_%s.png" % v)
        if os.path.exists(pa) and os.path.exists(pb):
            board("Grazing-light proof (1024 spp, no denoiser): %s - r4 vs r5" % cap, [(pa, "r4"), (pb, "r5")],
                  "board_proof_%s_r4_r5.png" % v, h=560)
    Z4 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Build", "progress", "zebra_r5_gate_20261017", "Vortex"))
    for v in ("cpillar_R", "cpillar_L", "shoulder_R", "sideglass_L", "rear34_R"):
        pa = os.path.join(Z4, "zebra_Vortex_export_%s.png" % v)
        pb = os.path.join(ZB, "zebra_Vortex_export_%s.png" % v)
        if os.path.exists(pa) and os.path.exists(pb):
            board("Zebra %s - r4 export (gate agent) vs r5 export" % v, [(pa, "r4"), (pb, "r5")], "board_zebra_%s_r4_r5.png" % v, h=560)
    print(STAMP)
