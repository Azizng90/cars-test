"""make_owner_notes_sheets.py - before | after judging sheets for the owner-notes pass (17 Oct; H1 plate, H2 roundel,
H3 headlamps, H4 door lines / flake, gate leftovers, front x4 difference, chase / macro). Every sheet <= 1600 px wide.

  python make_owner_notes_sheets.py

BEFORE = the r5b export (build sha d4a318ce836ad935): preview/opus_rear_r5b/*_r5b.png (review_opus_rear_r5.py, 128 spp),
         preview/owner_notes/before/*_r5b.png (the same script + close-up cameras, rendered from the r5b blend backup
         _backup_owner_notes_20261017/HatchlingS.blend), shading/proof_r5b, shading/zebra_r5b.
AFTER  = renders FROM THE FINAL EXPORT (HatchlingS.blend written by blender_export_casting.py): preview/owner_notes/
         *_after.png, shading/proof_owner_notes, shading/zebra_owner_notes.
Writes preview/owner_notes/sheet_*.png, stamped with the export's build sha / mtime.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview", "owner_notes")
BEF = os.path.join(OUT, "before")
R5B = os.path.join(HERE, "preview", "opus_rear_r5b")
H = json.load(open(os.path.join(HERE, "export", "health.json")))
STAMP = "AFTER = final export: build_HatchlingS.py sha256 %s  mtime %s  | health %s (%s)  | BEFORE = r5b (sha d4a318ce836ad935)" % (
    H["build_script_sha256"][:16], H["build_script_mtime"], "PASS" if H["pass"] else "FAIL", H["written"])
MAXW = 1600


def font(sz):
    for f in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def load(p, crop=None, scale=None, h=None):
    im = Image.open(p).convert("RGB")
    if crop:
        im = im.crop(crop)
    if scale:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    if h:
        im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    return im


def row(items, pad=10, cap=30):
    """items: [(image, label)] side by side; scaled down together if wider than MAXW"""
    w = sum(i.width for i, _ in items) + pad * (len(items) + 1)
    if w > MAXW:
        k = (MAXW - pad * (len(items) + 1)) / sum(i.width for i, _ in items)
        items = [(i.resize((max(1, round(i.width * k)), max(1, round(i.height * k))), Image.LANCZOS), l) for i, l in items]
        w = sum(i.width for i, _ in items) + pad * (len(items) + 1)
    h = max(i.height for i, _ in items)
    o = Image.new("RGB", (w, h + cap + pad), (24, 24, 26))
    d = ImageDraw.Draw(o)
    x = pad
    for im, lb in items:
        o.paste(im, (x, cap)); d.text((x + 4, 5), lb, fill=(236, 232, 220), font=font(19)); x += im.width + pad
    return o


def sheet(name, title, rows, note=None):
    w = max(r.width for r in rows)
    head_h = 66 + (24 if note else 0)
    o = Image.new("RGB", (w, head_h + sum(r.height for r in rows)), (24, 24, 26))
    d = ImageDraw.Draw(o)
    d.rectangle((0, 0, w, head_h), fill=(12, 12, 14))
    d.text((10, 6), title, fill=(255, 255, 255), font=font(24))
    d.text((10, 38), STAMP, fill=(200, 200, 160), font=font(14))
    if note:
        d.text((10, 60), note, fill=(190, 220, 190), font=font(15))
    y = head_h
    for r in rows:
        o.paste(r, (0, y)); y += r.height
    p = os.path.join(OUT, "sheet_%s.png" % name)
    o.save(p)
    print("wrote", p, o.size)


def B(shot):
    p = os.path.join(BEF, "HatchlingS_%s_r5b.png" % shot)
    return p if os.path.exists(p) else os.path.join(R5B, "HatchlingS_%s_r5b.png" % shot)


def A(shot, tag="after"):
    return os.path.join(OUT, "HatchlingS_%s_%s.png" % (shot, tag))


def pair(shot, crop=None, scale=None, h=None, lab=""):
    return row([(load(B(shot), crop, scale, h), "BEFORE r5b  " + lab), (load(A(shot), crop, scale, h), "AFTER  " + lab)])


def stacked(shot, crop, scale, lab):
    return [row([(load(B(shot), crop, scale), "BEFORE r5b  " + lab)]), row([(load(A(shot), crop, scale), "AFTER  " + lab)])]


def diff_row(a, b, lab):
    ia = Image.open(a).convert("RGB"); ib = Image.open(b).convert("RGB")
    d = np.abs(np.asarray(ia, np.float32) - np.asarray(ib, np.float32))
    dx = Image.fromarray(np.clip(d * 4, 0, 255).astype(np.uint8))
    m = d.mean()
    return row([(ia, "BEFORE r5b " + lab), (ib, "AFTER " + lab), (dx, "x4 |after - before|  mean %.3f" % m)]), m


if __name__ == "__main__":
    # H1 plate
    sheet("H1_plate", "H1  rear plate 'OF 91': cap 1.5 on the 2.84 field, even pitch + word space, centred by its ink box, clean 9",
          [pair("plate", h=560, lab="plate close-up"),
           pair("rear34_axle_R", crop=(380, 400, 660, 490), scale=2.6, lab="3/4-rear axle view, plate 2.6x")])
    # H2 roundel
    sheet("H2_roundel", "H2  door roundel 7: ink centroid on the disc (+0.15), strokes ~1.4x the ring, full disc (top no longer cut off)",
          [pair("roundel_R", h=520, lab="right door"), pair("roundel_L", h=520, lab="left door"),
           pair("rear34_axle_R", crop=(1330, 340, 1460, 520), scale=2.2, lab="3/4-rear axle view, roundel 2.2x")])
    # H3 headlamps
    sheet("H3_lamps", "H3  headlamps: lens / bezel / boss registered, lens = smooth cast cap, no blue crescents, no faceting",
          stacked("hero_34_front", (380, 590, 800, 720), 3.0, "front hero crop 380-800 x 590-720 at 3x") +
          [row([(load(B("lamp_L"), (250, 380, 1300, 900), h=330), "BEFORE r5b  left lamp"), (load(A("lamp_L"), (250, 380, 1300, 900), h=330), "AFTER  left lamp"),
                (load(B("lamp_R"), (250, 350, 1350, 900), h=330), "BEFORE r5b  right lamp"), (load(A("lamp_R"), (250, 350, 1350, 900), h=330), "AFTER  right lamp")])])
    # H4 doors + flake
    sheet("H4_doors", "H4  door shut lines: thin even pad-print break, no dark band; flake = fine additive sparkle (no grit)",
          [pair("rear34_axle_R", crop=(1050, 150, 1600, 600), scale=1.3, lab="owner crop 1050-1600 x 150-600"),
           pair("rear34_axle_R", crop=(1380, 330, 1600, 580), scale=3.0, lab="stripe crossing the door line, 3x")])
    sheet("H4_doors_close", "H4  door lines close-up (front line at the flare step / rear line), sun raking from behind",
          [pair("doorF_R", h=560, lab="front door line"), pair("doorR_R", h=560, lab="rear door line")])
    # gate leftovers
    PB = os.path.join(HERE, "shading", "proof_r5b"); PA = os.path.join(HERE, "shading", "proof_owner_notes")
    ZB = os.path.join(HERE, "shading", "zebra_r5b"); ZA = os.path.join(HERE, "shading", "zebra_owner_notes")

    def pp(fn, crop, scale, lab, bdir, adir):
        return row([(load(os.path.join(bdir, fn), crop, scale), "BEFORE r5b  " + lab), (load(os.path.join(adir, fn), crop, scale), "AFTER  " + lab)])
    sheet("leftovers", "Gate leftovers: tail shut-line caps / walls (2.0 uu dent like the door lines), shoulder-shelf knot (no union bulge)",
          [pp("proof_clay_tail_R.png", (450, 80, 850, 420), 1.5, "1024 spp clay tail_R, shut line + cap", PB, PA),
           pp("proof_paint_cpillar_R.png", (0, 600, 400, 900), 1.6, "1024 spp paint cpillar_R, line cap", PB, PA),
           pp("proof_paint_cpillar_R.png", (950, 280, 1500, 560), 1.3, "1024 spp paint cpillar_R, shoulder shelf", PB, PA)])
    sheet("zebra_shoulder", "Zebra / curvature: shoulder shelf in front of the C-pillar (the knot's bullseye), both sides",
          [pp("zebra_HatchlingS_export_shoulder_R.png", (250, 250, 1100, 650), 0.9, "zebra shoulder_R", ZB, ZA),
           pp("zebra_HatchlingS_export_shoulder_L.png", None, 0.55, "zebra shoulder_L", ZB, ZA),
           pp("curv_HatchlingS_export_shoulder_R.png", (250, 150, 1150, 600), 0.85, "curvature shoulder_R", ZB, ZA)])
    # front x4
    r1, m1 = diff_row(B("hero_34_front"), A("hero_34_front"), "paint")
    r2, m2 = diff_row(os.path.join(BEF, "HatchlingS_hero_34_front_r5bclay.png"), A("hero_34_front", "after_clay"), "clay")
    sheet("front_x4", "Front hero vs r5b: clay (shape) changes only at the headlamps; paint also shows the finer flake + lamp/roundel prints",
          [r1, r2], note="mean abs diff  paint %.3f   clay %.3f  (0-255 per channel)" % (m1, m2))
    # chase / macro
    sheet("chase", "Chase camera (game view, ~3 car lengths behind, 17-20 deg up) and the Navvy family check",
          [pair("chase", h=520, lab="chase cam"), row([(load(A("chase_navvy"), h=520), "AFTER  chase cam beside Navvy")])])
    sheet("macro", "3/4-rear macro (matched to the R5 Turbo casting photo) and both 3/4-rear axle-height views",
          [pair("macro_r5", h=500, lab="3/4-rear macro"), pair("rear34_axle_L", h=420, lab="3/4-rear axle L"),
           pair("rear34_axle_R", h=420, lab="3/4-rear axle R")])
