"""make_review_compare_r3.py - judging sheets for the Hatchling S rear pass, round 3 (spec 4b rules 9, 11-16).

  python make_review_compare_r3.py

Reads preview/opus_rear_r3/HatchlingS_<shot>_<tag>.png (rendered by review_opus_rear.py --out preview/opus_rear_r3)
and writes, in the same folder:
  review_compare.png      final 3/4-rear macros next to the real loose die-cast photos they were matched to
  front_before_after.png  front hero: round 2 export (reviewed) vs round 3 export, same script / camera / shaders, + x4 diff
  chase_before_after.png  chase cam: round 2 vs round 3, plus 3x zooms of the tail
  detail_crops.png        200-300 % crops (round 2 vs round 3): tail shut lines, quarter window, flare top, front-arch stripe
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear_r3")
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


stack([row([(P("macro_r5", "r3"), "OURS  Hatchling S 'Old Faithful' - round 3 export, matched camera"),
            (os.path.join(REF, "ref_hw_renault5turbo_1991_canada_b.jpg"), "REAL  loose 1991 1:64 hatch casting (closest reference)")]),
       row([(P("macro_golf", "r3"), "OURS  matched to the hatchback-on-wood photo"),
            (os.path.join(REF, "rear_ref_03_hatchback_diecast_on_wood.jpg"), "REAL  1:64 hatchback die-cast (ignore its aftermarket wheels)")])],
      os.path.join(OUT, "review_compare.png"))

stack([row([(P("hero_34_front", "r2"), "FRONT HERO  round 2 export (reviewed: no front regression)"),
            (P("hero_34_front", "r3"), "FRONT HERO  round 3 export"),
            (diff(P("hero_34_front", "r2"), P("hero_34_front", "r3")), "difference x4 (black = identical)")], h=600)],
      os.path.join(OUT, "front_before_after.png"))

Z = (540, 420, 1060, 780)
stack([row([(P("chase", "r2"), "CHASE CAM  round 2"), (P("chase", "r3"), "CHASE CAM  round 3")], h=700),
       row([(crop(P("chase", "r2"), Z, 2.0), "round 2, tail x2"), (crop(P("chase", "r3"), Z, 2.0), "round 3, tail x2")], h=700)],
      os.path.join(OUT, "chase_before_after.png"))

C = {   # macro_r5 crops (1600x1200 frame)
    "tail x2.5": ("macro_r5", (40, 520, 470, 880), 2.5),
    "quarter window x3": ("macro_r5", (690, 490, 870, 640), 3.0),
    "flare top x3": ("macro_r5", (560, 560, 760, 760), 3.0),
    "arch stripe x3": ("macro_r5", (1180, 600, 1400, 820), 3.0),
}
rows = []
for label, (shot, box, s) in C.items():
    rows.append(row([(crop(P(shot, "r2"), box, s), "R2 " + label), (crop(P(shot, "r3"), box, s), "R3 " + label)], h=520))
# A/B: the 'ghost S' on the flare top is a MIRROR REFLECTION of the C-pillar badge in the glossy clear coat, not ink:
# with the badge's ink removed from the tampo (render only) the ghost disappears too
if os.path.exists(P("macro_r5", "r3_nobadge")):
    b = C["flare top x3"][1]
    rows.append(row([(crop(P("macro_r5", "r3"), b, 3.0), "R3 flare top x3"),
                     (crop(P("macro_r5", "r3_nobadge"), b, 3.0), "same, badge ink off: ghost gone")], h=520))
stack(rows, os.path.join(OUT, "detail_crops.png"))

# (f) grazing-light proof crops from shading_r3 (shading_check_rear.py: low key light raking ACROSS the tail / along the flank)
SH = os.path.join(HERE, "shading_r3")
if os.path.isdir(SH):
    def S(kind, view):
        return os.path.join(SH, "shading_HatchlingS_export_%s_%s.png" % (kind, view))
    rows = []
    for view, lab in (("rear34_rake", "key light raking across the tail"), ("rear34_side", "key light along the flank")):
        rows.append(row([(crop(S(k, view), (90, 380, 560, 640), 3.0), "%s tail x3, %s" % (k, lab)) for k in ("clay", "paint")], h=520))
        rows.append(row([(crop(S(k, view), (590, 320, 820, 500), 3.0), "%s quarter window + flare top x3" % k) for k in ("clay", "paint")], h=520))
    stack(rows, os.path.join(SH, "shading_crops.png"))
