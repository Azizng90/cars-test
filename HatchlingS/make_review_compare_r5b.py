"""make_review_compare_r5b.py - judging sheets for the Hatchling S rear pass, round 5 attempt 2 (r5b; spec 4b rules 5, 9, 11-16).
(Copy of make_review_compare_r5.py: new renders in preview/opus_rear_r5b tagged r5b; the oct16 / r4 / r5 (attempt 1)
renders are read from preview/opus_rear_r5, made with the same review script, stage and samples.)

  python make_review_compare_r5.py

Reads preview/opus_rear_r5/HatchlingS_<shot>_<tag>.png written by review_opus_rear_r5.py --out preview/opus_rear_r5 with
  oct16 = _backup_pre_rear_20261016/HatchlingS.blend   (the 16 Oct front baseline)
  r4    = _backup_opus_rear_r5_20261017/HatchlingS.blend (round 4, as shipped)
  r5    = HatchlingS.blend written by the round-5 production export (the meshes in export/*.fbx)
each with its own preview materials, same script / samples / stage. Every sheet carries the build-script sha256 and mtime
from export/health.json (the export the r5 renders were made from). Writes, in the same folder:
  front_before_after.png   hero / windscreen / side: 16 Oct | r4 | r5b | x4 |r5b-16Oct| | x4 |r5b-r4|
  fix_crops_3x.png         r5 (attempt 1) vs r5b crops (3-4x) of the review-render zones named in the r5 gate's fixes
  rear_axle_compare.png    3/4-rear at axle height, both sides, r5 vs r5b (+3x) and straight behind (rule 14)
  review_compare.png       r5 macros beside the real loose castings they were matched to
  family_chase.png         chase cam r5b beside Navvy (same camera, light, deck) + the chase cam r5 vs r5b
  cpillars_glass.png       both C-pillars from above, side glass, windscreen: r5 vs r5b (rules 5, 13, 16)
"""
import json
import os
import time

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear_r5b")
OLD = os.path.join(HERE, "preview", "opus_rear_r5")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))
H = json.load(open(os.path.join(HERE, "export", "health.json")))
STAMP = "build_HatchlingS.py sha256 %s  mtime %s  | export health %s (%s)  | renders %s" % (
    H["build_script_sha256"][:16], H["build_script_mtime"], "PASS" if H["pass"] else "FAIL", H["written"],
    time.ctime(os.path.getmtime(os.path.join(OUT, "HatchlingS_chase_r5b.png"))))


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def fit(im, h):
    return im.convert("RGB").resize((round(im.width * h / im.height), h), Image.LANCZOS)


def row(pairs, h=600, pad=12, cap=34):
    ims = [fit(p if isinstance(p, Image.Image) else Image.open(p), h) for p, _ in pairs]
    w = sum(i.width for i in ims) + pad * (len(ims) + 1)
    out = Image.new("RGB", (w, h + cap + pad * 2), (24, 24, 26))
    d = ImageDraw.Draw(out)
    x = pad
    for im, (_, label) in zip(ims, pairs):
        out.paste(im, (x, pad + cap))
        d.text((x + 4, pad + 4), label, fill=(235, 232, 225), font=font(22))
        x += im.width + pad
    return out


def stack(rows, path, title):
    w = max(r.width for r in rows)
    head = Image.new("RGB", (w, 70), (12, 12, 14))
    d = ImageDraw.Draw(head)
    d.text((12, 8), title, fill=(255, 255, 255), font=font(26))
    d.text((12, 42), STAMP, fill=(200, 200, 160), font=font(18))
    out = Image.new("RGB", (w, 70 + sum(r.height for r in rows)), (24, 24, 26))
    out.paste(head, (0, 0))
    y = 70
    for r in rows:
        out.paste(r, (0, y)); y += r.height
    out.save(path)
    print("wrote", path, out.size)


def P(name, tag):
    return os.path.join(OUT if tag == "r5b" else OLD, "HatchlingS_%s_%s.png" % (name, tag))


def crop(path, box, scale=3.0):
    im = Image.open(path).convert("RGB").crop(box)
    return im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)


def diff(a, b, gain=4.0):
    A = Image.open(a).convert("RGB"); B = Image.open(b).convert("RGB")
    D = np.asarray(ImageChops.difference(A, B)).astype(np.float32)
    print("%s vs %s: mean abs diff %.3f, 99.9th pct %.1f, pixels > 30: %d" % (
        os.path.basename(a), os.path.basename(b), D.mean(), np.percentile(D.max(2), 99.9), int((D.max(2) > 30).sum())))
    return Image.fromarray(np.clip(D * gain, 0, 255).astype(np.uint8)), D.mean()


# ---- front: 16 Oct | r4 | r5 | x4 diffs
rows = []
for shot in ("hero_34_front", "windscreen_34", "side_profile"):
    d16, m16 = diff(P(shot, "oct16"), P(shot, "r5b"))
    d4, m4 = diff(P(shot, "r4"), P(shot, "r5b"))
    rows.append(row([(P(shot, "oct16"), "%s  16 Oct" % shot), (P(shot, "r4"), "round 4"), (P(shot, "r5b"), "r5b (round 5, attempt 2)"),
                     (d16, "x4 |r5b - 16 Oct|  mean %.2f" % m16), (d4, "x4 |r5b - r4|  mean %.2f" % m4)], h=420))
stack(rows, os.path.join(OUT, "front_before_after.png"),
      "FRONT regression check (same camera / stage / samples; each build with its own preview materials)")

# ---- crops of every review-render zone named in the r5 gate's fixes (r5 = attempt 1, r5b = this export)
Z = [
    ("fix 1 tail quarter behind the rear arch (macro_r5 440-680, 690-860)", "macro_r5", (440, 690, 680, 860), 4.0),
    ("fix 1/2 hip + shoulder above the rear arch", "macro_r5", (440, 560, 800, 800), 3.0),
    ("fix 1 tail quarter, left side (macro_golf ~880-990, 640-760)", "macro_golf", (840, 600, 1040, 780), 3.0),
    ("fix 6 plate (rear_low 560-740, 455-500): raised boss, 'OF 91'", "rear_low", (520, 420, 780, 530), 4.0),
    ("fix 5 tail notch / base lip, right (rear_low)", "rear_low", (1050, 380, 1450, 760), 2.0),
    ("fix 3/4 shut lines + lamps (rear_low)", "rear_low", (150, 330, 1450, 760), 1.0),
]
rows = []
for label, shot, box, sc in Z:
    rows.append(row([(crop(P(shot, "r5"), box, sc), "r5  " + label), (crop(P(shot, "r5b"), box, sc), "r5b  (%.1fx, %s)" % (sc, shot))],
                    h=520))
stack(rows, os.path.join(OUT, "fix_crops_3x.png"), "r5 gate fixes: attempt 1 (r5) vs attempt 2 (r5b), crops of the named zones")

# ---- rule 14: axle visible from 3/4 rear at axle height
rows = [row([(P("rear34_axle_R", "r5"), "r5  3/4 rear right, axle height"), (P("rear34_axle_R", "r5b"), "r5b")], h=520),
        row([(P("rear34_axle_L", "r5"), "r5  3/4 rear left, axle height"), (P("rear34_axle_L", "r5b"), "r5b")], h=520),
        row([(crop(P("rear34_axle_R", "r5b"), (960, 480, 1360, 800)), "r5b right 3x: steel stub between tyre and body"),
             (crop(P("rear34_axle_L", "r5b"), (240, 480, 640, 800)), "r5b left 3x")], h=560),
        row([(P("rear_axle", "r5"), "r5  straight behind, axle height"), (P("rear_axle", "r5b"), "r5b (lead ruling: may hide the axle)")],
            h=520)]
stack(rows, os.path.join(OUT, "rear_axle_compare.png"), "Rule 14 (lead ruling): axle at a 3/4-rear view at axle height")

# ---- references
stack([row([(P("macro_r5", "r5b"), "OURS r5b  matched camera"),
            (os.path.join(REF, "ref_hw_renault5turbo_1991_canada_b.jpg"), "REAL  loose 1991 1:64 hatch casting")], h=700),
       row([(P("macro_golf", "r5b"), "OURS r5b  matched to the hatchback-on-wood photo"),
            (os.path.join(REF, "rear_ref_03_hatchback_diecast_on_wood.jpg"), "REAL  1:64 hatchback on wood")], h=700),
       row([(P("rear_low", "r5b"), "OURS r5b  rear low"),
            (os.path.join(REF, "ref_hw_peugeot205_rear.jpg"), "REAL  loose 205 castings from behind (axle, wheels)")], h=520)],
      os.path.join(OUT, "review_compare.png"), "Rear 3/4 macros beside the real loose die-cast references")

# ---- family / chase
stack([row([(P("chase_navvy", "r5b"), "chase cam  r5b beside the approved Navvy (same camera / light / deck)")], h=900),
       row([(P("chase", "r5"), "chase cam  r5"), (P("chase", "r5b"), "chase cam  r5b")], h=600),
       row([(crop(P("chase", "r5"), (560, 420, 1040, 720), 2.0), "r5 chase 2x"),
            (crop(P("chase", "r5b"), (560, 420, 1040, 720), 2.0), "r5b chase 2x")], h=600)],
      os.path.join(OUT, "family_chase.png"), "Chase camera (rule 15) and the Navvy family check (rule 9)")

# ---- C-pillars, glass
stack([row([(P("cpillar_R", "r5"), "r5  right C-pillar from above"), (P("cpillar_R", "r5b"), "r5b")], h=520),
       row([(P("cpillar_L", "r5"), "r5  left C-pillar from above"), (P("cpillar_L", "r5b"), "r5b")], h=520),
       row([(P("sideglass_L", "r5"), "r5  side glass"), (P("sideglass_L", "r5b"), "r5b")], h=440),
       row([(P("windscreen_34", "r5"), "r5  windscreen (rule 5)"), (P("windscreen_34", "r5b"), "r5b")], h=520)],
      os.path.join(OUT, "cpillars_glass.png"), "C-pillars from above, rear glass from oblique angles, side glass, windscreen")
