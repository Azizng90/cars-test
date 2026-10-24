"""make_review_compare_r4.py - judging sheets for the Hatchling S rear pass, round 4 (spec 4b rules 9, 11-16).

  python make_review_compare_r4.py

Reads preview/opus_rear_r4/HatchlingS_<shot>_<tag>.png (review_opus_rear_r4.py --out preview/opus_rear_r4) where
  r3m = the round-3 export (backup _backup_opus_rear_r4_20261017) rendered with the round-4 preview materials
        (glass IOR 1.56, interior roughness 0.65), so every difference shown is GEOMETRY
  r4  = the round-4 export
and writes, in the same folder:
  review_compare.png      round-4 3/4-rear macros next to the real loose die-cast photos they were matched to
  front_before_after.png  front hero r3m vs r4 + x4 difference (front-end proof)
  chase_before_after.png  chase cam r3m vs r4, plus 2x tail zooms
  detail_crops.png        r3m vs r4 crops: tail shoulders, shut lines, quarter window, flare top, rear corner / tyre
  rear_axle_compare.png   straight behind at axle height r3m vs r4 (rule 14)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear_r4")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def fit(im, h):
    return im.convert("RGB").resize((round(im.width * h / im.height), h), Image.LANCZOS)


def row(pairs, h=900, pad=16, cap=44):
    ims = [fit(p if isinstance(p, Image.Image) else Image.open(p), h) for p, _ in pairs]
    w = sum(i.width for i in ims) + pad * (len(ims) + 1)
    out = Image.new("RGB", (w, h + cap + pad * 2), (24, 24, 26))
    d = ImageDraw.Draw(out)
    x = pad
    for im, (_, label) in zip(ims, pairs):
        out.paste(im, (x, pad + cap))
        d.text((x + 4, pad + 6), label, fill=(235, 232, 225), font=font(28))
        x += im.width + pad
    return out


def stack(rows, path):
    w = max(r.width for r in rows)
    out = Image.new("RGB", (w, sum(r.height for r in rows)), (24, 24, 26))
    y = 0
    for r in rows:
        out.paste(r, (0, y)); y += r.height
    out.save(path)
    print("wrote", path, out.size)


def P(name, tag):
    return os.path.join(OUT, "HatchlingS_%s_%s.png" % (name, tag))


def crop(path, box, scale):
    im = Image.open(path).convert("RGB").crop(box)
    return im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)


def diff(a, b, gain=4.0):
    A = Image.open(a).convert("RGB"); B = Image.open(b).convert("RGB")
    D = np.asarray(ImageChops.difference(A, B)).astype(np.float32)
    print("%s vs %s: mean abs diff %.3f, 99.9th pct %.1f, pixels > 30: %d" % (
        os.path.basename(a), os.path.basename(b), D.mean(), np.percentile(D.max(2), 99.9), int((D.max(2) > 30).sum())))
    return Image.fromarray(np.clip(D * gain, 0, 255).astype(np.uint8))


stack([row([(P("macro_r5", "r4"), "OURS  Hatchling S 'Old Faithful' - round 4 export, matched camera"),
            (os.path.join(REF, "ref_hw_renault5turbo_1991_canada_b.jpg"), "REAL  loose 1991 1:64 hatch casting (closest reference)")]),
       row([(P("macro_golf", "r4"), "OURS  matched to the hatchback-on-wood photo"),
            (os.path.join(REF, "rear_ref_03_hatchback_diecast_on_wood.jpg"), "REAL  1:64 hatchback die-cast (ignore its aftermarket wheels)")])],
      os.path.join(OUT, "review_compare.png"))

stack([row([(P("hero_34_front", "r3m"), "FRONT HERO  round 3 export (same materials)"),
            (P("hero_34_front", "r4"), "FRONT HERO  round 4 export"),
            (diff(P("hero_34_front", "r3m"), P("hero_34_front", "r4")), "difference x4 (black = identical)")], h=600)],
      os.path.join(OUT, "front_before_after.png"))

Z = (540, 420, 1060, 780)
stack([row([(P("chase", "r3m"), "CHASE CAM  round 3"), (P("chase", "r4"), "CHASE CAM  round 4")], h=700),
       row([(crop(P("chase", "r3m"), Z, 2.0), "round 3, tail x2"), (crop(P("chase", "r4"), Z, 2.0), "round 4, tail x2")], h=700)],
      os.path.join(OUT, "chase_before_after.png"))

stack([row([(P("rear_axle", "r3m"), "STRAIGHT BEHIND, axle height  round 3"), (P("rear_axle", "r4"), "round 4")], h=700)],
      os.path.join(OUT, "rear_axle_compare.png"))

C = {   # (shot, box in the 1600x1200 frame, scale)
    "golf: tail shoulder + shut line x3": ("macro_golf", (880, 470, 1150, 680), 3.0),
    "golf: tail x2": ("macro_golf", (900, 440, 1460, 800), 2.0),
    "r5: tail x2.5": ("macro_r5", (40, 520, 470, 880), 2.5),
    "r5: quarter window x3": ("macro_r5", (690, 490, 870, 640), 3.0),
    "r5: flare top x3": ("macro_r5", (560, 560, 760, 760), 3.0),
    "rear_low: right rear corner x2.5": ("rear_low", (1060, 360, 1420, 800), 2.5),
}
rows = []
for label, (shot, box, s) in C.items():
    rows.append(row([(crop(P(shot, "r3m"), box, s), "R3 " + label), (crop(P(shot, "r4"), box, s), "R4 " + label)], h=520))
stack(rows, os.path.join(OUT, "detail_crops.png"))

SH = os.path.join(HERE, "shading_r4")
if os.path.isdir(SH):
    def S(kind, view):
        return os.path.join(SH, "shading_HatchlingS_export_%s_%s.png" % (kind, view))
    rows = []
    for view, box in (("rear34_rake", (90, 300, 700, 700)), ("rear_low", (80, 180, 1200, 700)), ("rear34_side", (450, 250, 1000, 600))):
        rows.append(row([(crop(S(k, view), box, 2.0), "%s %s x2" % (k, view)) for k in ("clay", "paint")], h=560))
    stack(rows, os.path.join(SH, "shading_crops.png"))
