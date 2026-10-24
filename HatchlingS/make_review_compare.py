"""make_review_compare.py - side-by-side judging sheets for the Hatchling S rear pass (spec 4b rule 15).

  python make_review_compare.py [tag]       (tag default: after)

review_compare.png : each matched 3/4-rear macro next to the real loose die-cast photo it was matched to.
front_before_after.png : hero_34_front before | after, plus a x3 amplified difference image.
chase_before_after.png : chase before | after.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear")
REF = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Docs", "Reference", "DieCast"))
TAG = sys.argv[1] if len(sys.argv) > 1 else "after"
H = 900


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def fit(im, h):
    return im.convert("RGB").resize((round(im.width * h / im.height), h), Image.LANCZOS)


def row(pairs, h=H, pad=16, cap=44):
    ims = [fit(Image.open(p), h) for p, _ in pairs]
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


def P(name, tag=TAG):
    return os.path.join(OUT, "HatchlingS_%s_%s.png" % (name, tag))


stack([row([(P("macro_r5"), "OURS  Hatchling S 'Old Faithful' (Blender, matched camera)"),
            (os.path.join(REF, "ref_hw_renault5turbo_1991_canada_b.jpg"), "REAL  loose 1991 1:64 hatch casting (reference)")]),
       row([(P("macro_golf"), "OURS  matched to the hatchback-on-wood photo"),
            (os.path.join(REF, "rear_ref_03_hatchback_diecast_on_wood.jpg"), "REAL  1:64 hatchback die-cast (ignore its aftermarket wheels)")])],
      os.path.join(OUT, "review_compare.png"))

if os.path.exists(P("hero_34_front", "before")) and os.path.exists(P("hero_34_front")):
    a = Image.open(P("hero_34_front", "before")).convert("RGB")
    b = Image.open(P("hero_34_front")).convert("RGB")
    diff = np.asarray(ImageChops.difference(a, b)).astype(np.float32)
    print("front hero mean abs diff (0-255): %.3f   99.9th pct: %.1f" % (diff.mean(), np.percentile(diff.max(2), 99.9)))
    dimg = Image.fromarray(np.clip(diff * 3.0, 0, 255).astype(np.uint8))
    tmp = os.path.join(OUT, "_front_diff_x3.png"); dimg.save(tmp)
    stack([row([(P("hero_34_front", "before"), "FRONT HERO  before (baseline)"), (P("hero_34_front"), "FRONT HERO  after (rear pass)"),
                (tmp, "difference x3 (black = identical)")], h=600)],
          os.path.join(OUT, "front_before_after.png"))
if os.path.exists(P("chase", "before")) and os.path.exists(P("chase")):
    stack([row([(P("chase", "before"), "CHASE CAM  before"), (P("chase"), "CHASE CAM  after")], h=700)],
          os.path.join(OUT, "chase_before_after.png"))
