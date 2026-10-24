"""shading_proof_hatchling.py - spec 4b rule 16 grazing-light proof renders for the Hatchling S export (round 5).
(Copied from SourceArt/Blender/Vortex/shading_proof_vortex.py; Hatchling S views + paint colour; also burns the export's
build-script sha256 / mtime from export/health.json into every image.)

The pipeline's Tools/Assembly/shading_check.py renders 64 spp with no denoiser and only two full-car views: too
grainy to prove there are no black smears, and it never looked at the C-pillars from above, where the round-2 faults
were. This script REUSES its materials / import / lighting (glossy clay + metallic paint, chrome, clear glass, sun
6 deg above the horizon at right angles to the view) and renders the exported FBX files read-only:
  * on the GPU at high sample counts (default 1024 spp, adaptive, NO denoiser: nothing is smoothed away)
  * the four pipeline views (front34, rear34, side, top) + close views: top-rear, both C-pillars from above and
    behind, the left side glass, both tail corners, the rear window
  * clay AND paint passes, glass included in both (clay glass shows the moulding's fairness, paint glass is clear)

  blender -b --factory-startup --python shading_proof_vortex.py -- [export dir] [--out DIR] [--samples N]
          [--views a,b,...] [--res WxH]
Writes <out>/proof_<pass>_<view>.png and proof_sheet.png. Never writes next to the FBX files.
"""
import importlib.util
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "Tools", "Assembly"))
_spec = importlib.util.spec_from_file_location("shading_check", os.path.join(TOOLS, "shading_check.py"))
SC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SC)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


_pos = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or not argv[i - 1].startswith("--"))]
EXP = os.path.abspath(_pos[0]) if _pos else os.path.join(HERE, "export")
OUT = os.path.abspath(arg("--out", os.path.join(HERE, "shading", "proof")))
SAMPLES = int(arg("--samples", "1024"))
RES = tuple(int(v) for v in arg("--res", "1600x1000").lower().split("x"))

# camera az (deg, from +X toward +Y), el, distance (m), sun azimuth offset from the camera az, lens, target (m)
CAR_T = (0.0, 0.0, 0.14)
VIEWS = {
    "front34": dict(az=38.0, el=11.0, dist=3.5, sun=-95.0, lens=85, target=CAR_T),
    "rear34": dict(az=-142.0, el=14.0, dist=3.5, sun=95.0, lens=85, target=CAR_T),
    "side": dict(az=90.0, el=4.0, dist=3.8, sun=-80.0, lens=85, target=CAR_T),
    "top": dict(az=150.0, el=55.0, dist=3.8, sun=-100.0, lens=85, target=CAR_T),
    "toprear": dict(az=180.0, el=38.0, dist=2.4, sun=95.0, lens=85, target=(-0.30, 0.0, 0.24)),
    "cpillar_L": dict(az=148.0, el=34.0, dist=0.95, sun=95.0, lens=85, target=(-0.38, 0.29, 0.29)),
    "cpillar_R": dict(az=-148.0, el=34.0, dist=0.95, sun=-95.0, lens=85, target=(-0.38, -0.29, 0.29)),
    "shoulder_L": dict(az=125.0, el=22.0, dist=0.95, sun=95.0, lens=85, target=(-0.37, 0.35, 0.25)),
    "shoulder_R": dict(az=-125.0, el=22.0, dist=0.95, sun=-95.0, lens=85, target=(-0.37, -0.35, 0.25)),
    "sideglass_L": dict(az=95.0, el=12.0, dist=1.5, sun=-70.0, lens=85, target=(-0.08, 0.30, 0.30)),
    "tail_L": dict(az=150.0, el=12.0, dist=1.3, sun=-95.0, lens=85, target=(-0.52, 0.30, 0.13)),
    "tail_R": dict(az=-150.0, el=12.0, dist=1.3, sun=95.0, lens=85, target=(-0.52, -0.30, 0.13)),
    "rearwin": dict(az=180.0, el=20.0, dist=1.4, sun=60.0, lens=85, target=(-0.40, 0.0, 0.27)),
    "axle_R": dict(az=-160.0, el=2.0, dist=1.4, sun=95.0, lens=85, target=(-0.42, -0.31, 0.10)),
}
ORDER = arg("--views", ",".join(VIEWS)).split(",")


def gpu(scene):
    scene.cycles.device = 'CPU'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for t in ('OPTIX', 'CUDA'):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                if [d for d in prefs.devices if d.type == t]:
                    for d in prefs.devices:
                        d.use = (d.type == t)
                    scene.cycles.device = 'GPU'
                    return t
            except Exception:
                continue
    except Exception:
        pass
    return 'CPU'


def place(cam, sun, v):
    az, el = math.radians(v["az"]), math.radians(v["el"])
    t = Vector(v["target"])
    cam.location = t + Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))) * v["dist"]
    cam.rotation_euler = (t - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = v["lens"]
    saz, sel = az + math.radians(v["sun"]), math.radians(6.0)
    d = Vector((math.cos(saz) * math.cos(sel), math.sin(saz) * math.cos(sel), math.sin(sel)))
    sun.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()


def _stamp():
    import json, time
    try:
        h = json.load(open(os.path.join(EXP, "health.json")))
        return "%s %s" % (h["build_script_sha256"][:12], time.strftime("%d%b_%H.%M", time.strptime(h["build_script_mtime"])))
    except Exception as e:
        return "unknown"


STAMP = _stamp()


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    o = dict(samples=SAMPLES, res=RES)
    sun, cam = SC.setup(scene, o)
    dev = gpu(scene)
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.004
    scene.cycles.use_denoising = False
    print("[proof] device", dev, "samples", SAMPLES, flush=True)
    objs = SC.load_target(EXP, 0.0)
    # shading_check.load_target re-uses the wheel FBX's mesh data without the +90 deg Z rotation the FBX importer puts
    # on the imported object (the casting parts keep theirs), so its wheels stand turned 90 deg. Restore it here.
    src_rot = [o.rotation_euler.z for o in objs if o.name.startswith("SM_HatchlingS_Body")]
    for o in objs:
        if o.name.startswith("Wheel_"):
            o.rotation_euler.z += src_rot[0] if src_rot else math.pi / 2
    os.makedirs(OUT, exist_ok=True)
    paths = []
    for kind in ("clay", "paint"):
        pick = SC.pass_materials(kind, (0.012, 0.088, 0.40))      # Old Faithful 'Streak Blue' enamel
        for ob in objs:
            for s in ob.material_slots:
                nm = s.material.name if s.material else "Paint"
                s.link = 'OBJECT'
                s.material = pick(nm)
        for vn in ORDER:
            place(cam, sun, VIEWS[vn])
            p = os.path.join(OUT, "proof_%s_%s.png" % (kind, vn))
            scene.render.filepath = p
            bpy.ops.render.render(write_still=True)
            SC.label_png(p, "%s %s  build %s" % (kind, vn, STAMP))
            paths.append(p)
            print("[proof] wrote", p, flush=True)
    SC.sheet(paths, 2, len(ORDER), os.path.join(OUT, "proof_sheet.png"))
    print("[proof] sheet", os.path.join(OUT, "proof_sheet.png"), "(rows: clay, paint; columns: %s)" % ", ".join(ORDER),
          flush=True)


main()
