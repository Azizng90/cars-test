"""make_gate_crops_r5b.py - 3-4x crops, attempt 1 (r5) vs attempt 2 (r5b), at the exact image coordinates the r5 gate
named in its fixes 1-7 (1024-spp grazing proofs in shading/proof_r5 vs shading/proof_r5b, zebra/curvature renders in
shading/zebra_r5 vs shading/zebra_r5b). Stamped with the r5b export's build-script sha256 / mtime.
  python make_gate_crops_r5b.py      -> preview/opus_rear_r5b/gate_fix_crops.png"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "opus_rear_r5b")
H = json.load(open(os.path.join(HERE, "export", "health.json")))
STAMP = "r5b export: build_HatchlingS.py sha256 %s  mtime %s  | health %s (%s)" % (
    H["build_script_sha256"][:16], H["build_script_mtime"], "PASS" if H["pass"] else "FAIL", H["written"])
SRC = {"r5": (os.path.join(HERE, "shading", "proof_r5"), os.path.join(HERE, "shading", "zebra_r5")),
       "r5b": (os.path.join(HERE, "shading", "proof_r5b"), os.path.join(HERE, "shading", "zebra_r5b"))}


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def path(tag, name):
    p, z = SRC[tag]
    if name.startswith(("zebra_", "curv_")):
        return os.path.join(z, name % ("HatchlingS_export",))
    return os.path.join(p, name)


Z = [  # (label, image name, box, scale)
    ("fix 1 zebra shoulder_R: bullseye pair / U-turn (390-554, 472)", "zebra_%s_shoulder_R.png", (300, 380, 700, 660), 2.0),
    ("fix 1 curv shoulder_R: blue band (400-445, 440-640)", "curv_%s_shoulder_R.png", (300, 380, 700, 660), 2.0),
    ("fix 1 zebra shoulder_L (same zone, mirrored view)", "zebra_%s_shoulder_L.png", (700, 380, 1100, 660), 2.0),
    ("fix 2 paint shoulder_R hip top (250-575, 480-560), 6 deg sun", "proof_paint_shoulder_R.png", (230, 440, 600, 600), 2.5),
    ("fix 3 clay rearwin shut-line top L (290, 560-640)", "proof_clay_rearwin.png", (240, 530, 340, 680), 3.0),
    ("fix 3 clay rearwin shut-line top R (1310, 560-640)", "proof_clay_rearwin.png", (1260, 530, 1360, 680), 3.0),
    ("fix 3 clay shoulder_L (1440-1600, 297-400)", "proof_clay_shoulder_L.png", (1400, 280, 1600, 420), 3.0),
    ("fix 4 clay tail_R dent walls (510-575, 160-340)", "proof_clay_tail_R.png", (490, 150, 600, 350), 3.0),
    ("fix 4 paint tail_L lamp/dent walls (790-1120, 120-460)", "proof_paint_tail_L.png", (790, 120, 1120, 460), 1.5),
    ("fix 5 clay tail_R notch / lip (780-830, 680-790)", "proof_clay_tail_R.png", (740, 640, 880, 800), 3.0),
    ("fix 7 zebra sideglass_L sills (350-700 / 900-1150, 515-545)", "zebra_%s_sideglass_L.png", (330, 470, 1170, 570), 1.4),
]


def tile(tag, name, box, sc, label):
    im = Image.open(path(tag, name)).convert("RGB").crop(box)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 9 * len(label) + 12, 22), fill=(0, 0, 0))
    d.text((5, 3), label, fill=(255, 255, 255), font=font(15))
    return im


rows = []
for label, name, box, sc in Z:
    a = tile("r5", name, box, sc, "r5  " + label)
    b = tile("r5b", name, box, sc, "r5b  (%.1fx)" % sc)
    r = Image.new("RGB", (a.width + b.width + 18, max(a.height, b.height) + 12), (24, 24, 26))
    r.paste(a, (6, 6)); r.paste(b, (a.width + 12, 6))
    rows.append(r)
W = max(r.width for r in rows)
out = Image.new("RGB", (W, 70 + sum(r.height for r in rows)), (24, 24, 26))
d = ImageDraw.Draw(out)
d.text((12, 8), "r5 gate fixes 1-7 at the gate's own image coordinates: attempt 1 (r5) | attempt 2 (r5b)", fill=(255, 255, 255), font=font(24))
d.text((12, 40), STAMP, fill=(200, 200, 160), font=font(16))
y = 70
for r in rows:
    out.paste(r, (0, y)); y += r.height
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "gate_fix_crops.png")
out.save(p)
print("wrote", p, out.size)
