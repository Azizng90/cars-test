"""make_review_compare_r2.py - judging sheets for the Hatchling S rear pass 2 (spec 4b rules 9, 11-16).

  python make_review_compare_r2.py

Reads preview/opus_rear_r2/HatchlingS_<shot>_<tag>.png (rendered by review_opus_rear.py) and writes, in the same folder:
  review_compare.png      final 3/4-rear macros next to the real loose die-cast photos they were matched to
  front_before_after.png  row 1: geometry-only proof - pre-rear baseline vs final build script, SAME dense mesher and
                          SAME preview shaders, plus the x4 difference; row 2: the owner-seen export (old pipeline) vs
                          the final production export (clean pipeline)
  chase_before_after.png  chase cam: rev 5 (round 1) vs final
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear_r2")
R1 = os.path.join(HERE, "preview", "opus_rear")
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


def P(name, tag, d=OUT):
    return os.path.join(d, "HatchlingS_%s_%s.png" % (name, tag))


def diff(a, b, gain=4.0):
    A = Image.open(a).convert("RGB"); B = Image.open(b).convert("RGB")
    D = np.asarray(ImageChops.difference(A, B)).astype(np.float32)
    print("%s vs %s: mean abs diff %.3f, 99.9th pct %.1f, pixels > 30: %d" % (
        os.path.basename(a), os.path.basename(b), D.mean(), np.percentile(D.max(2), 99.9), int((D.max(2) > 30).sum())))
    return Image.fromarray(np.clip(D * gain, 0, 255).astype(np.uint8))


stack([row([(P("macro_r5", "final"), "OURS  Hatchling S 'Old Faithful' - final export, matched camera"),
            (os.path.join(REF, "ref_hw_renault5turbo_1991_canada_b.jpg"), "REAL  loose 1991 1:64 hatch casting (closest reference)")]),
       row([(P("macro_golf", "final"), "OURS  matched to the hatchback-on-wood photo"),
            (os.path.join(REF, "rear_ref_03_hatchback_diecast_on_wood.jpg"), "REAL  1:64 hatchback die-cast (ignore its aftermarket wheels)")])],
      os.path.join(OUT, "review_compare.png"))

rows = [row([(P("hero_34_front", "geom_before"), "GEOMETRY  pre-rear baseline script (dense mesh)"),
             (P("hero_34_front", "geom_after"), "GEOMETRY  final script (same mesher + shaders)"),
             (diff(P("hero_34_front", "geom_before"), P("hero_34_front", "geom_after")), "difference x4 (black = identical)")], h=600)]
if os.path.exists(P("hero_34_front", "before", R1)) and os.path.exists(P("hero_34_front", "final")):
    rows.append(row([(P("hero_34_front", "before", R1), "EXPORT  owner-seen (pre-rear, old decimating pipeline)"),
                     (P("hero_34_front", "final"), "EXPORT  final (clean pipeline, health gate PASS)"),
                     (diff(P("hero_34_front", "before", R1), P("hero_34_front", "final")), "difference x4")], h=600))
stack(rows, os.path.join(OUT, "front_before_after.png"))

if os.path.exists(P("chase", "w1", R1)) and os.path.exists(P("chase", "final")):
    stack([row([(P("chase", "before", R1), "CHASE CAM  pre-rear baseline"), (P("chase", "w1", R1), "CHASE CAM  rev 5 (round 1)"),
                (P("chase", "final"), "CHASE CAM  final")], h=600)],
          os.path.join(OUT, "chase_before_after.png"))
