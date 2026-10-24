"""review_boards_owner_notes.py - before | after boards for the owner notes of 17 Oct (V1-V5), Vortex.
Before = the r5b export renders (preview/opus_rear_r5b, shading/proof_r5b, shading/zebra_r5b); after = the owner-notes
export renders (preview/owner_notes_20261017, shading/proof_on, shading/zebra_on). Same cameras, same crops.
System Python (Pillow + numpy):  python SourceArt/Blender/Vortex/review_boards_owner_notes.py
Every board is <= 1600 px wide and stamped with the build-script hash and the export health."""
import hashlib
import json
import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
B5 = os.path.join(HERE, "preview", "opus_rear_r5b")
ON = os.path.join(HERE, "preview", "owner_notes_20261017")
PB, PA = os.path.join(HERE, "shading", "proof_r5b"), os.path.join(HERE, "shading", "proof_on")
ZB, ZA = os.path.join(HERE, "shading", "zebra_r5b"), os.path.join(HERE, "shading", "zebra_on")
OUT = os.path.join(ON, "boards")
os.makedirs(OUT, exist_ok=True)


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            continue
    return ImageFont.load_default()


F1, F2, F3 = font(22), font(18), font(13)
BUILD = os.path.join(HERE, "build_Vortex.py")
SHA = hashlib.sha256(open(BUILD, "rb").read()).hexdigest()
H = json.load(open(os.path.join(HERE, "export", "health.json")))
STAMP = "build_Vortex.py sha256 %s.. | export health.json pass=%s, script sha %s.. | tris %s" % (
    SHA[:12], H.get("pass"), str(H.get("build_script_sha256"))[:12],
    ", ".join("%s %d" % (k.replace("SM_Vortex_", ""), v["summary"]["tris"]) for k, v in H.get("parts", {}).items()))


def crop(path, box, k):
    im = Image.open(path).convert("RGB").crop(box)
    return im.resize((im.width * k, im.height * k), Image.LANCZOS)


def fit(im, w):
    if im.width <= w:
        return im
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


def board(title, tiles, name, cols=2, maxw=1600):
    """tiles: [(PIL image, label)]; laid out in a grid, scaled so the board is <= maxw wide"""
    pad, top, lab, foot = 10, 40, 28, 26
    tw = min(max(t[0].width for t in tiles), (maxw - pad * (cols + 1)) // cols)
    ims = [fit(t[0], tw) for t in tiles]
    th = max(i.height for i in ims)
    rows = (len(ims) + cols - 1) // cols
    W = pad + cols * (tw + pad)
    Hh = top + rows * (th + lab + pad) + foot
    bd = Image.new("RGB", (W, Hh), (24, 24, 28))
    d = ImageDraw.Draw(bd)
    d.text((pad, 9), title, fill=(240, 240, 240), font=F1)
    for i, (im, (_, label)) in enumerate(zip(ims, tiles)):
        r, c = divmod(i, cols)
        x, y = pad + c * (tw + pad), top + r * (th + lab + pad)
        bd.paste(im, (x, y))
        d.text((x, y + im.height + 4), label, fill=(225, 225, 225), font=F2)
    d.text((pad, Hh - foot + 6), STAMP, fill=(150, 150, 150), font=F3)
    p = os.path.join(OUT, name)
    bd.save(p)
    print("board", os.path.relpath(p, HERE), bd.size)
    return p


def x4(a, b, out):
    A = np.asarray(Image.open(a).convert("RGB")).astype(float)
    Bb = np.asarray(Image.open(b).convert("RGB")).astype(float)
    d = np.clip(np.abs(A - Bb) * 4.0, 0, 255).astype(np.uint8)
    Image.fromarray(d).save(out)
    m = np.abs(A - Bb).mean(2)
    return out, float(m.mean())


def main():
    b, a = os.path.join(B5, "r5b_%s.png"), os.path.join(ON, "on_%s.png")
    # V1 front windscreen (hero 4x crop 620-940 x 470-560) + the 100 mm cab close-up
    board("V1 windscreen: hero 4x crop (620-940 x 470-560) - r5b | owner notes",
          [(crop(b % "hero", (620, 470, 940, 560), 4), "before (r5b)"),
           (crop(a % "hero", (620, 470, 940, 560), 4), "after")], "V1_windscreen_hero_4x.png", cols=1)
    board("V1 windscreen: front_cab close-up - r5b | owner notes",
          [(Image.open(b % "front_cab").convert("RGB").crop((250, 380, 1150, 700)), "before (r5b)"),
           (Image.open(a % "front_cab").convert("RGB").crop((250, 380, 1150, 700)), "after")],
          "V1_windscreen_front_cab.png", cols=1)
    # V2 rear pane (scoop_R top-left, 3x) + C-pillar R
    board("V2 rear pane: scoop_R 3x crop (100-500 x 0-200) - r5b | owner notes",
          [(crop(b % "scoop_R", (100, 0, 500, 200), 3), "before (r5b)"),
           (crop(a % "scoop_R", (100, 0, 500, 200), 3), "after")], "V2_rear_pane_scoop_R_3x.png", cols=1)
    board("V2 rear pane: cpillar_R (0-800 x 150-650) - r5b | owner notes",
          [(Image.open(b % "cpillar_R").convert("RGB").crop((0, 150, 800, 650)), "before (r5b)"),
           (Image.open(a % "cpillar_R").convert("RGB").crop((0, 150, 800, 650)), "after")], "V2_rear_pane_cpillar_R.png")
    # V3 front door line (grazing proof clay, 3x 120-380 x 620-900) + both lines
    pb, pa = os.path.join(PB, "proof_clay_sideglass_L.png"), os.path.join(PA, "proof_clay_sideglass_L.png")
    board("V3 front door line: proof_clay_sideglass_L 3x (120-380 x 620-900) - r5b | owner notes",
          [(crop(pb, (120, 620, 380, 900), 3), "before (r5b)"), (crop(pa, (120, 620, 380, 900), 3), "after")],
          "V3_front_door_line_3x.png")
    board("V3 both door lines (front left, rear right): proof_clay_sideglass_L (60-1000 x 560-920) - r5b | owner notes",
          [(crop(pb, (60, 560, 1000, 920), 1), "before (r5b)"), (crop(pa, (60, 560, 1000, 920), 1), "after")],
          "V3_door_lines_pair.png", cols=1)
    pb, pa = os.path.join(PB, "proof_paint_sideglass_L.png"), os.path.join(PA, "proof_paint_sideglass_L.png")
    board("V3 door lines in paint: proof_paint_sideglass_L (60-1000 x 560-920) - r5b | owner notes",
          [(crop(pb, (60, 560, 1000, 920), 1), "before (r5b)"), (crop(pa, (60, 560, 1000, 920), 1), "after")],
          "V3_door_lines_paint.png", cols=1)
    # V4 lower door zebra (417-700 x 757-813, 3x; with context 730-840)
    zb, za = os.path.join(ZB, "zebra_Vortex_export_sideglass_L.png"), os.path.join(ZA, "zebra_Vortex_export_sideglass_L.png")
    board("V4 lower door above the rocker step: zebra sideglass_L 3x (417-700 x 730-840) - r5b | owner notes",
          [(crop(zb, (417, 730, 700, 840), 3), "before (r5b)"), (crop(za, (417, 730, 700, 840), 3), "after")],
          "V4_zebra_lower_door_3x.png", cols=1)
    cb, ca = os.path.join(ZB, "curv_Vortex_export_sideglass_L.png"), os.path.join(ZA, "curv_Vortex_export_sideglass_L.png")
    board("V4 curvature sideglass_L 3x (417-700 x 730-840) - r5b | owner notes",
          [(crop(cb, (417, 730, 700, 840), 3), "before (r5b)"), (crop(ca, (417, 730, 700, 840), 3), "after")],
          "V4_curvature_lower_door_3x.png", cols=1)
    # V5 tampo across the shut lines
    board("V5 tampo: scoop_R 3x (940-1240 x 560-800) - r5b | owner notes",
          [(crop(b % "scoop_R", (940, 560, 1240, 800), 3), "before (r5b)"),
           (crop(a % "scoop_R", (940, 560, 1240, 800), 3), "after")], "V5_tampo_scoop_R_3x.png")
    board("V5 tampo: side_profile 4x door crop (600-900 x 550-650) - r5b | owner notes",
          [(crop(b % "side", (600, 550, 900, 650), 4), "before (r5b)"), (crop(a % "side", (600, 550, 900, 650), 4), "after")],
          "V5_tampo_side_4x.png", cols=1)
    board("V5 tampo: side_glass (left doors) - r5b | owner notes",
          [(Image.open(b % "side_glass").convert("RGB"), "before (r5b)"), (Image.open(a % "side_glass").convert("RGB"), "after")],
          "V5_tampo_side_glass.png")
    # chase, rear 3/4 macro, front hero + x4 difference
    board("Chase camera (rule 15) - r5b | owner notes",
          [(Image.open(b % "chase").convert("RGB"), "before (r5b)"), (Image.open(a % "chase").convert("RGB"), "after")],
          "chase.png")
    board("Rear 3/4 macro - r5b | owner notes",
          [(Image.open(b % "rear_macro").convert("RGB"), "before (r5b)"), (Image.open(a % "rear_macro").convert("RGB"), "after")],
          "rear_macro.png")
    dp, dm = x4(b % "hero", a % "hero", os.path.join(OUT, "_diff_hero_r5b_on_x4.png"))
    board("Front hero - r5b | owner notes | |r5b - after| x4 (mean |diff| %.2f levels)" % dm,
          [(Image.open(b % "hero").convert("RGB"), "before (r5b)"), (Image.open(a % "hero").convert("RGB"), "after"),
           (Image.open(dp).convert("RGB"), "|r5b - after| x4")], "front_hero_x4.png")
    zs = [v for v in ("rear34_L", "rear34_R", "cpillar_L", "cpillar_R", "shoulder_L", "shoulder_R", "sideglass_L",
                      "sideglass_R")]
    board("Zebra set (after, from the final export)",
          [(Image.open(os.path.join(ZA, "zebra_Vortex_export_%s.png" % v)).convert("RGB"), v) for v in zs],
          "zebra_set.png", cols=2)
    print("stamp:", STAMP, time.strftime("%H:%M"))


main()
