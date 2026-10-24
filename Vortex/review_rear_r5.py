"""review_rear_r5.py - rear / chase-camera look-dev for the Vortex (build spec 4b rules 11-16). Opus rear pass r5
(copy of review_rear_opus.py: every frame <= 1600 px wide (GPU shared with the UE tests), a 3/4-rear view at axle
height ('rear_axle34', lead ruling on rules 11/14), the rear-pane glass mask applied to imported FBX windows that
predate it, and the build-script hash + export health stamp written next to every frame in <tag>_provenance.json).

Never exports, never saves a .blend, never writes into export/, the sidecar or the shipped tampo.

Two sources for the car:
  --src fast            build from build_Vortex.py with RAW surface nets (no decimation, analytic normals): the
                        look-dev path, minutes instead of the export pipeline's ~25 min. Same SDFs, same UVs/tampo.
  --src DIR             import the FBX parts of an export folder (e.g. ../Vortex/export or _healthcheck/export) and
                        dress them with the preview materials: what ships, exactly (custom normals from the FBX).
                        The tampo is generated from the build script into preview/opus_rear/_tampo_<tag>.png.

Shots (Navvy's deck stage, Navvy's material/light numbers):
  chase         behind, 17 deg above, ~3 car lengths, 40 mm, warm low sun        (the game camera; rule 15)
  chase_family  the same view, approved Navvy beside it (Navvy's EXISTING FBX imported read-only)
  rear_macro    3/4-rear macro matched to Docs/Reference/DieCast/rear_ref_02_white_wedge_supercar_1990s.jpg
  hero          the build script's own hero_34_front camera (front-end regression check)
  side / top    silhouette checks (side_profile / top_down cameras of the build script)

blender -b --factory-startup --python review_rear_opus.py -- --tag T [--src fast|DIR] [--shots a,b] [--samples N]
        [--pct N] [--quick] [--hide Windows,...] [--tampo existing.png]
Output: SourceArt/Blender/Vortex/preview/opus_rear/<tag>_<shot>.png
"""
import importlib.util
import math
import os
import sys
import time

import bpy
import numpy as np
from mathutils import Euler

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build_Vortex.py")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d


TAG = arg("--tag", "after")
SRC = arg("--src", "fast")
SHOTS = arg("--shots", "chase,rear_macro,chase_family,hero").split(",")
SAMPLES = int(arg("--samples", "128"))
PCT = int(arg("--pct", "100"))
QUICK = "--quick" in argv
HIDE = [h for h in arg("--hide", "").split(",") if h]
OUT = os.path.join(HERE, "preview", arg("--outdir", "opus_rear"))
os.makedirs(OUT, exist_ok=True)

# load the build script as a module (it parses sys.argv after "--" itself: give it a harmless set)
sys.argv = [sys.argv[0], "--", "--norender", "--noexport"] + (["--quick"] if QUICK else [])
spec = importlib.util.spec_from_file_location("build_Vortex_review", BUILD)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
W = mod.W
UU = mod.UU
# look-dev overrides of the r5 per-pane glass / tub numbers (never written back)
for _k, _a in (("GLASS_SPEC_REAR", "--gspec"), ("GLASS_ROUGH_REAR", "--grough"), ("GLASS_IOR_REAR", "--gior")):
    if arg(_a):
        setattr(mod, _k, float(arg(_a)))
for _i, _a in enumerate(argv):                    # r5b look-dev: --mset NAME=VALUE on the build module
    if _a == "--mset":
        _k, _v = argv[_i + 1].split("=", 1)
        setattr(mod, _k, eval(_v))
for _k, _a in (("GLASS_TINT_REAR", "--grear"), ("GLASS_TINT_FRONT", "--gfront"), ("INTERIOR_R5", "--tub")):
    if arg(_a):
        setattr(mod, _k, tuple(float(v) for v in arg(_a).split(",")) + (1.0,))


def log(*a):
    print("[review]", *a, flush=True)


FLAKE_CLAMP = None


def clamp_flake(pm):
    """placeholder, replaced below if the build script defines its own preview clamp"""
    return


def fast_sdf_part(name, fn, bmin, bmax, cell, target_tris, symmetric=True, normal_eps=0.02, *a, **kw):
    """raw surface nets + projection, analytic per-vertex normals: no decimation (look-dev only)"""
    t0 = time.time()
    V, Q = W.surface_nets(fn, bmin, bmax, cell)
    V = W.project(fn, V, iters=2, maxstep=cell)
    T = np.concatenate([Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]])
    N = W._unit(W.sdf_grad(fn, V, eps=normal_eps))
    log("  fast part %-16s %d tris (%.1fs)" % (name, len(T), time.time() - t0))
    return V, T, N


def materials(tampo):
    liv = dict(mod.LIVERIES["classof93"])
    if hasattr(mod, "preview_materials"):          # r4: the build script's own preview materials (smoke glass, matt tub)
        mod.preview_materials(liv, tampo)
        return
    W.make_slot_material("Paint", paint=liv["paint"], flake=liv["flake"], tampo=tampo)
    for slot in ("Chrome", "Lamp", "Zamac", "Base", "Glass", "Tire", "Hub"):
        W.make_slot_material(slot)
    W.make_slot_material("Interior", interior=liv["interior"])


def build_fast():
    W.sdf_part = fast_sdf_part
    mod.W.sdf_part = fast_sdf_part
    coll = W.get_coll("Vortex")
    objs = {"Body": mod.build_body(coll), "Base": mod.build_base(coll),
            "Windows": mod.build_windows(coll), "Interior": mod.build_interior(coll)}
    for o in objs.values():
        W.smart_uv(o, "UV0", angle=60.0, margin=0.002)
    mod.uv1_tampo(objs["Body"], mod.body_hidden, getattr(mod, "tail_pad_faces", None))
    mod.uv1_tampo(objs["Windows"])
    mod.base_uv1(objs["Base"])
    mod.copy_uv0_to_uv1(objs["Interior"])
    return objs


def import_export(d):
    objs = {}
    for part in ("Body", "Base", "Windows", "Interior"):
        p = os.path.join(d, "SM_Vortex_%s.fbx" % part)
        before = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=p, use_manual_orientation=True, axis_forward='X', axis_up='Z',
                                 use_custom_normals=True)
        new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
        ob = new[0]
        slots = mod.json_slots[part] if hasattr(mod, "json_slots") else \
            {"Body": ["Paint", "Chrome", "Lamp", "Zamac"], "Base": ["Base"], "Windows": ["Glass"],
             "Interior": ["Interior"]}[part]
        me = ob.data
        for i, s in enumerate(slots):
            m = bpy.data.materials.get(s)
            if i < len(me.materials):
                me.materials[i] = m
            else:
                me.materials.append(m)
        # vertex colour name / UV names as the build script authored them
        if me.color_attributes and "Col" not in me.color_attributes:
            me.color_attributes[0].name = "Col"
        if "Col" in me.color_attributes:
            me.color_attributes.active_color = me.color_attributes["Col"]
            me.color_attributes.render_color_index = me.color_attributes.find("Col")
        if part == "Windows" and hasattr(mod, "rear_pane_mask"):
            # (re)computed from the geometry exactly as build_windows writes it (exports before r5 carry Col = white)
            V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", V)
            V = (np.array(ob.matrix_world.to_3x3()) @ V.reshape(-1, 3).T).T / UU
            m = mod.rear_pane_mask(V)
            for a in list(me.color_attributes):
                me.color_attributes.remove(a)
            ca = me.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
            ca.data.foreach_set("color", np.stack([m, 0 * m, 0 * m, 1 + 0 * m], 1).ravel())
            me.color_attributes.active_color = ca
            me.color_attributes.render_color_index = 0
            log("windows: rear-pane mask from the geometry (%d of %d verts)" % (int(m.sum()), len(m)))
        objs[part] = ob
        log("imported %s: %d tris, uv %s, col %s" % (os.path.basename(p), sum(len(f.vertices) - 2 for f in me.polygons),
                                                   [u.name for u in me.uv_layers],
                                                   [c.name for c in me.color_attributes]))
    return objs


CAR_L = 1.19
CFG = {
    "chase": dict(az=180.0, el=17.0, dist=3.0 * CAR_L, lens=40, target=(-0.10, 0.0, 0.11),
                  focus=(-0.58, 0.0, 0.14), fstop=9.0, sun=(-150.0, 17.0)),
    # rear_ref_02: the tail seen ~34 deg off the axis from the car's LEFT, ~15 deg above, macro, car fills the frame
    "rear_macro": dict(az=146.0, el=15.0, dist=5.0, lens=100, target=(-0.15, 0.03, 0.12),
                       focus=(-0.57, 0.10, 0.14), fstop=3.2, sun=(-150.0, 24.0)),
    "hero": dict(mod.SHOTS["hero_34_front"]),
    "side": dict(mod.SHOTS["side_profile"]),
    "top": dict(mod.SHOTS["top_down"]),
    "under": dict(mod.SHOTS["underside"]),
    "bay_close": dict(az=162.0, el=24.0, dist=2.6, lens=100, target=(-0.27, 0.0, 0.22), focus=(-0.27, 0.0, 0.23),
                      fstop=5.6, sun=(-150.0, 24.0)),
    "rear_low": dict(az=180.0, el=4.0, dist=5.6, lens=100, target=(-0.30, 0.0, 0.12), focus=(-0.58, 0.0, 0.12),
                     fstop=4.0, sun=(-150.0, 24.0)),
}
# r3: top-rear views aimed at each C-pillar / side-window opening (the owner's "black bad faces" lived there)
CFG["cpillar_L"] = dict(az=148.0, el=34.0, dist=1.9, lens=100, target=(-0.10, 0.27, 0.235),
                        focus=(-0.10, 0.27, 0.235), fstop=8.0, sun=(-120.0, 18.0))
CFG["cpillar_R"] = dict(az=-148.0, el=34.0, dist=1.9, lens=100, target=(-0.10, -0.27, 0.235),
                        focus=(-0.10, -0.27, 0.235), fstop=8.0, sun=(120.0, 18.0))
CFG["side_glass"] = dict(az=90.0, el=10.0, dist=2.4, lens=100, target=(0.0, 0.30, 0.235), focus=(0.0, 0.30, 0.235),
                         fstop=8.0, sun=(60.0, 30.0))
CFG["tail_corner"] = dict(az=150.0, el=12.0, dist=1.7, lens=100, target=(-0.56, 0.33, 0.11),
                          focus=(-0.56, 0.33, 0.11), fstop=8.0, sun=(-150.0, 24.0))
CFG["corner_R"] = dict(az=-140.0, el=28.0, dist=0.9, lens=100, target=(-0.135, -0.29, 0.243),
                       focus=(-0.135, -0.29, 0.243), fstop=11.0, sun=(110.0, 18.0))
CFG["scoop_R"] = dict(az=-115.0, el=16.0, dist=1.1, lens=100, target=(-0.13, -0.37, 0.17),
                      focus=(-0.13, -0.37, 0.17), fstop=11.0, sun=(110.0, 18.0))
# r5 (lead ruling, rules 11 + 14): 3/4 rear at about axle height - the steel axle must show between tyre and body
CFG["rear_axle34"] = dict(az=-150.0, el=2.5, dist=2.6, lens=100, target=(-0.36, -0.12, 0.10),
                          focus=(-0.34, -0.37, 0.10), fstop=8.0, sun=(-150.0, 24.0))
# the same ruling, close on the right rear wheel's inner side (3/4 rear, camera at axle height)
CFG["rear_axle_close"] = dict(az=-164.0, el=1.0, dist=1.6, lens=100, target=(-0.36, -0.30, 0.098),
                              focus=(-0.34, -0.30, 0.095), fstop=11.0, sun=(-150.0, 24.0))
CFG["front_cab"] = dict(az=34.0, el=9.5, dist=2.4, lens=100, target=(0.06, 0.05, 0.20), focus=(0.10, 0.12, 0.20),
                        fstop=5.6, sun=(-12.0, 24.0))
CFG["chase_family"] = dict(CFG["chase"], target=(-0.10, -0.575, 0.13), focus=(-0.58, -0.575, 0.16),
                           dist=3.0 * CAR_L * 1.18)
NAVVY_AT = (0.0, -1.15, 0.0)              # Navvy on the Vortex's right, same heading


def main():
    t0 = time.time()
    load = arg("--load")                       # look-dev cache: a scene saved by an earlier --save run
    if load:
        bpy.ops.wm.open_mainfile(filepath=load)
        sc = bpy.context.scene
        objs = {k: bpy.data.objects["SM_Vortex_" + k] for k in ("Body", "Base", "Windows", "Interior")}
        if arg("--interior"):
            col = tuple(float(v) for v in arg("--interior").split(",")) + (1.0,)
            bpy.data.materials["Interior"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = col
    else:
        sc = W.reset_scene()
        tampo = arg("--tampo")
        if tampo is None:
            tampo = os.path.join(OUT, "_tampo_%s.png" % TAG)
            mod.make_tampo(tampo, res=2048 if QUICK else 4096)
        materials(tampo)
        # r5: the preview enamel's paint-pooling AO node sampled 12 rays per shading point; on the broad concave fillets
        # (C-pillar foot) that noise rendered as dark 'grime' speckles that are not in the geometry (clay is clean).
        # 64 rays: same pooling, no speckle. Look-dev renders only; the build script's material is unchanged.
        pm = bpy.data.materials.get("Paint")
        for n in (pm.node_tree.nodes if pm and pm.node_tree else []):
            if n.type == 'AMBIENT_OCCLUSION':
                n.samples = 64
                if "--diag-nopool" in argv:
                    n.inputs['Distance'].default_value = 0.0
            if n.type == 'NEW_GEOMETRY' and "--diag-noedge" in argv:
                for l in list(pm.node_tree.links):
                    if l.from_node == n and l.from_socket.name == 'Pointiness':
                        pm.node_tree.links.remove(l)
            # r5b (gate fix 1) diagnostics: flake normal perturbation off / flake colour off
            if n.type == 'VECT_MATH' and n.operation == 'SCALE' and "--diag-noflakeN" in argv:
                n.inputs['Scale'].default_value = 0.0
            if n.type == 'MIX' and "--diag-noflakeC" in argv:
                if abs(float(n.inputs[0].default_value) - 0.38) < 1e-6 and not n.inputs[0].is_linked:
                    n.inputs[0].default_value = 0.0
        if FLAKE_CLAMP is not None:
            clamp_flake(pm)
        objs = build_fast() if SRC == "fast" else import_export(os.path.abspath(SRC))
        wcoll = W.get_coll("PreviewWheels")
        wheel = W.build_wheel(name="W02_Fan_preview", coll=wcoll, quick=QUICK)
        wheel.hide_render = True
        wheel.hide_set(True)
        mod.stage_wheels(wheel, wcoll)
        if arg("--save"):
            bpy.ops.wm.save_as_mainfile(filepath=arg("--save"), compress=False)
    for k in HIDE:
        if k in objs:
            objs[k].hide_render = True
    if "--clay" in argv:                       # glossy grey clay on the casting parts (shading faults read as dark smears)
        clay = bpy.data.materials.new("LookClay")
        clay.use_nodes = True
        b = clay.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.42, 0.42, 0.42, 1.0)
        b.inputs["Roughness"].default_value = 0.12
        for ob in objs.values():
            if ob.name.endswith("Windows") and "--clayglass" not in argv:
                continue
            for s in ob.material_slots:
                s.link = 'OBJECT'
                s.material = clay
    log("scene ready %.1fs" % (time.time() - t0))
    W.STAGE_OPT['samples'] = SAMPLES
    W.STAGE_OPT['pct'] = PCT
    W.setup_render(sc)
    # owner notes 17 Oct (V1): light reaches the tub through the glass (build_Vortex.PREVIEW_REFRACTIVE_CAUSTICS)
    sc.cycles.caustics_refractive = bool(getattr(mod, "PREVIEW_REFRACTIVE_CAUSTICS", False))
    rig = W.setup_stage(sc)
    navvy = None
    for s in SHOTS:
        cfg = CFG[s]
        if s in ("chase", "chase_family"):
            sc.render.resolution_x, sc.render.resolution_y = 1600, 900
        else:
            sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
        if s == "chase_family" and navvy is None:
            navvy = W.import_navvy(location=NAVVY_AT, yaw_deg=0.0)
        if navvy is not None:
            for o in navvy.children_recursive:
                o.hide_render = (s != "chase_family") or o.name.startswith("SM_Wheel_W03_Lug")
        path = os.path.join(OUT, "%s_%s.png" % (TAG, s))
        W.render_shot(sc, rig, path, cfg)
    import hashlib, json
    prov = {"tag": TAG, "src": SRC, "shots": SHOTS, "samples": SAMPLES,
            "build_script_sha256": hashlib.sha256(open(BUILD, "rb").read()).hexdigest(),
            "build_script_mtime": time.ctime(os.path.getmtime(BUILD)), "rendered": time.strftime("%Y-%m-%d %H:%M:%S")}
    hp = os.path.join(os.path.abspath(SRC), "health.json") if SRC != "fast" else None
    if hp and os.path.exists(hp):
        h = json.load(open(hp))
        prov["export_health"] = {"pass": h.get("pass"), "written": h.get("written"),
                                 "build_script_sha256": h.get("build_script_sha256"),
                                 "tris": {k: v["summary"]["tris"] for k, v in h.get("parts", {}).items()}}
    json.dump(prov, open(os.path.join(OUT, "%s_provenance.json" % TAG), "w"), indent=1)
    log("done %.1fs" % (time.time() - t0))


main()
