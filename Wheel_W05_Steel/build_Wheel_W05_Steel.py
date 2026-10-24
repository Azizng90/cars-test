"""
build_Wheel_W05_Steel.py  -  MODEL '93 shared wheel design W05_Steel (20 Oct 2026, CAIRN brief §3.4)
====================================================================================================
One-piece toy wheel: a chunky black all-terrain tyre ring (2 staggered rows of 18 blocks, centre groove, shoulder lugs
1.5 uu down the sidewall, one moulded 0.6 uu step ring on each sidewall, no lettering) on a satin-black dished STEEL
wheel (6 round vents dia 2.0 on r 5, a raised centre disc r 2.6; the bore is covered by the axle head, so the disc stays whole).  The centre disc's
rim ring (0.8 wide) and its 6 nut nubs (dia 1.2 on r 1.9) are bright (HubBright = the chrome hub MI) so the wheel never
reads as a black blob in the chase cam.  No emblem anywhere.  Radius 13, width 10 (CAIRN width A).

Authored as a LEFT wheel: axle along Y, outer (show) face +Y, origin at the wheel centre.  The tread is 180-deg
symmetric, so right wheels yaw 180 deg (like W03).  The casting's peened axle head (on SM_Cairn_Body, Zamac) sits on the
centre disc at local y 3.5, its dome centred on the spin axis.

Geometry toolkit (surface nets, projection, rounded SDF ops, tyre profile) is shared with ../Cairn/build_Cairn.py
(imported read-only, no bytecode written).  Export ONLY through the clean-topology pipeline:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup --python
      Tools/Assembly/blender_export_casting.py -- SourceArt/Blender/Wheel_W05_Steel/build_Wheel_W05_Steel.py
Writes export/SM_Wheel_W05_Steel.fbx, export/health.json, Wheel_W05_Steel.json, Wheel_W05_Steel.blend.
"""
import bpy, math, os, sys, json, time, importlib.util
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = "Wheel_W05_Steel"
MESH_NAME = "SM_Wheel_W05_Steel"
UU = 0.01

_CP = os.path.join(os.path.dirname(HERE), "Cairn", "build_Cairn.py")
_spec = importlib.util.spec_from_file_location("build_Cairn_toolkit", _CP)
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
W = C.W

# the toolkit, as module attributes (blender_export_casting.py patches sdf_part / build_object / export on THIS module)
surface_nets = C.surface_nets
project = C.project
sdf_grad = C.sdf_grad
eval_chunked = C.eval_chunked
sdf_part = C.sdf_part
build_object = C.build_object
u_round, i_round, s_round, sd_rrect2 = C.u_round, C.i_round, C.s_round, C.sd_rrect2


def log(*a):
    print("[%s]" % ASSET, *a, flush=True)


R, RI, WD = 13.0, 7.4, 10.0          # tyre outer radius, bead radius (0.5 into the rim barrel), width
RIM_R = 7.9
FACE_Y = 2.3                         # dished wheel face (1.5 below the rim lip at 3.8)
DISC_R, DISC_Y = 2.6, 3.5            # raised centre disc (its face = where the axle head sits)
BORE_R = 0.9
VENT_R, VENT_PCD = 1.0, 5.0
NUT_R, NUT_PCD = 0.6, 1.9
RING = (1.65, 2.45)                  # bright centre ring (0.8 wide)


def tire_sdf(x, y, z):
    t = C.tyre_sdf(y, x, z, R, RI, WD, 2.4, nblk=18, depth=1.1, rc=0.6, gap=2.0)
    rr = np.sqrt(x * x + z * z)
    side = C.sm((np.abs(y) - 3.6) / 0.6)                                       # only on the sidewall faces
    return t - C.bell(rr - 8.6, 1.0, 0.25) * side                              # low on the sidewall, clear of the lugs                              # moulded step ring: a soft 0.3 bead, ~0.6 wide


def hub_sdf(x, y, z):
    rr = np.sqrt(x * x + z * z)
    rim = sd_rrect2(rr, y + 0.3, RIM_R, 4.1, 0.8)                              # barrel y -4.4 .. 3.8
    rim = s_round(rim, sd_rrect2(rr, y - (FACE_Y + 2.0), 6.7, 2.0, 0.8), 0.8)  # dish down to y 2.3
    rim = u_round(rim, sd_rrect2(rr, y - (DISC_Y - 0.9), DISC_R, 0.9, 0.6), 0.6)   # centre disc to y 3.5
    holes = []
    for k in range(6):
        t = k * math.pi / 3.0 + math.pi / 6.0
        pc, qc = VENT_PCD * math.cos(t), VENT_PCD * math.sin(t)
        rh = np.sqrt((x - pc) ** 2 + (z - qc) ** 2)
        holes.append(sd_rrect2(rh, y - (FACE_Y + 0.4), VENT_R, 1.4, 0.75))    # 1.0 deep, full-round bottom
    # no through-bore: the casting's peened head (dia 2.2) covers the centre, so the disc face stays whole
    return s_round(rim, C.U(*holes), 0.65)


def bright_sdf(x, y, z):
    rr = np.sqrt(x * x + z * z)
    a, b = RING
    ring = sd_rrect2(rr - 0.5 * (a + b), y - (DISC_Y - 0.1), 0.5 * (b - a), 0.45, 0.38)   # y 2.95..3.85 (0.35 proud)
    nuts = []
    for k in range(6):
        t = k * math.pi / 3.0
        pc, qc = NUT_PCD * math.cos(t), NUT_PCD * math.sin(t)
        nuts.append(sd_rrect2(np.sqrt((x - pc) ** 2 + (z - qc) ** 2), y - 3.6, NUT_R, 0.5, 0.32))   # to y 4.1, domed
    return u_round(ring, C.U(*nuts), 0.3)


def part(name, fn, lo, hi, cell, tgt):
    V, T, N = sdf_part(name, fn, lo, hi, cell, tgt)
    return C.refined(fn, name, V, T, N, force=True)        # crease fix: split the collapse's > 55 deg outliers


def build_w05(coll):
    parts = []
    V, T, N = part("W05_Tire", tire_sdf, (-13.6, -5.6, -13.6), (13.6, 5.6, 13.6), 0.08, 9000)
    parts.append(dict(V=V, T=T, N=N, mat=0, rake=False))
    V, T, N = part("W05_Hub", hub_sdf, (-8.4, -4.9, -8.4), (8.4, 4.3, 8.4), 0.06, 4000)
    parts.append(dict(V=V, T=T, N=N, mat=1, rake=False))
    V, T, N = part("W05_HubBright", bright_sdf, (-3.0, 2.6, -3.0), (3.0, 4.4, 3.0), 0.03, 1500)
    parts.append(dict(V=V, T=T, N=N, mat=2, rake=False))
    C._separate_touching_parts(parts)
    return build_object(MESH_NAME, parts, ["Tire", "Hub", "HubBright"], coll, rake=False)


def make_materials():
    W.make_slot_material("Tire")
    m, nt, bs = W._principled("Tire"); W._set(bs, 'Base Color', (0.017, 0.017, 0.019, 1)); W._set(bs, 'Roughness', 0.62)
    m, nt, bs = W._principled("Hub")
    W._set(bs, 'Base Color', (0.026, 0.026, 0.028, 1)); W._set(bs, 'Metallic', 0.35); W._set(bs, 'Roughness', 0.34)
    W._set(bs, 'Coat Weight', 0.3); W._set(bs, 'Coat Roughness', 0.2)
    m, nt, bs = W._principled("HubBright")
    W._set(bs, 'Base Color', (0.93, 0.93, 0.95, 1)); W._set(bs, 'Metallic', 1.0); W._set(bs, 'Roughness', 0.06)


def wheel_uvs(ob):
    me = ob.data
    W.smart_uv(ob, "UV0", angle=60.0, margin=0.004)
    uv1 = me.uv_layers.new(name="UV1")
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    li = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", li)
    p = co[li]
    Rm = R * UU * 1.05
    uv1.data.foreach_set("uv", np.stack([(p[:, 0] / Rm) * 0.5 + 0.5, (p[:, 2] / Rm) * 0.5 + 0.5], 1).ravel())
    me.uv_layers.active = me.uv_layers["UV0"]


def write_sidecar(ob, path):
    data = {
        "wheel_design": "W05_Steel",
        "mesh": MESH_NAME,
        "description": "Chunky all-terrain toy tyre (2 staggered rows of 18 blocks, centre groove, shoulder lugs, one moulded step ring, no lettering) on a satin-black dished steel wheel: 6 round vents, raised centre disc with a bright rim ring and 6 bright nut nubs, axle bore in the exact centre. No emblem.",
        "units": "uu, UE axes (X fwd, Y right, Z up); FBX authored in Blender metres, 1 m = 100 uu",
        "radius": R, "width": WD, "hub_radius": RIM_R, "bore_radius": 0.0, "bore_note": "no through-bore: the axle head (dia 2.2) covers the disc centre",
        "centre_disc": {"radius": DISC_R, "face_y": DISC_Y, "bright_ring": list(RING), "nut_nubs": {"count": 6, "radius": NUT_R, "pcd_radius": NUT_PCD}},
        "vents": {"count": 6, "radius": VENT_R, "pcd_radius": VENT_PCD},
        "axle_head_offset": DISC_Y,
        "axle_head_note": "the peened steel axle head belongs to the casting (Cairn: SM_Cairn_Body, Zamac); its dome base sits on the centre disc at wheel centre + 3.5 along the axle, centred on the spin axis, standing 0.3 above the bright ring",
        "origin": "wheel centre", "axle_axis": "Y",
        "outer_face": "Blender +Y = UE -Y, i.e. authored as a LEFT wheel. Right wheels: yaw 180 deg (tread is 180-deg symmetric: 18 staggered blocks per row).",
        "slots": ["Tire", "Hub", "HubBright"],
        "slot_look": {"Tire": "existing TireLug MI (hard black toy plastic, roughness 0.62)",
                      "Hub": "NEW MI_Hub_SatinBlack (satin black painted steel; brief §3.4 rule-3 deviation, owner-visible choice: the reference wears black steel wheels)",
                      "HubBright": "the existing chrome Hub MI (centre ring + nut nubs)"},
        "tris": W.tri_count(ob),
        "uv": {"UV0": "smart unwrap (wear/grain)", "UV1": "planar side projection X/Z over the wheel diameter"},
        "used_by": ["Cairn"],
        "export_pipeline": "Tools/Assembly/blender_export_casting.py (clean topology + mesh-health gate)",
        "source": "SourceArt/Blender/Wheel_W05_Steel/build_Wheel_W05_Steel.py",
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log("sidecar", path)


def main():
    t0 = time.time()
    W.reset_scene()
    make_materials()
    coll = W.get_coll("Wheel_W05_Steel")
    ob = build_w05(coll)
    wheel_uvs(ob)
    log("tris", W.tri_count(ob))
    W.export_fbx(ob, os.path.join(HERE, "export", MESH_NAME + ".fbx"))
    write_sidecar(ob, os.path.join(HERE, ASSET + ".json"))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"), compress=True)
    log("done in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
