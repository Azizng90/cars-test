"""review_opus_rear.py - rear / chase-camera judging renders for the Hatchling S (spec 4b rules 9, 11-15).

  blender.exe -b --factory-startup --python review_opus_rear.py -- --blend <HatchlingS.blend> --tag before|after
              [--shots chase,chase_navvy,macro_r5,macro_golf,rear_low,hero_34_front] [--samples 128] [--pct 100]

Opens a built HatchlingS.blend READ-ONLY (never saved), rebuilds the shared Navvy preview stage (same deck boards,
HDRI, sun colour and camera conventions as every casting preview), places the four W01 wheels at the sidecar
positions and renders:

  chase          behind, 17 deg above, ~3 car lengths (3.6 m = 360 uu), 40 mm, low warm sun   (the game camera)
  chase_navvy    the same camera / sun with the approved Navvy beside it (its EXISTING export FBX, read-only)
  macro_r5       3/4-rear macro matched to Docs/Reference/DieCast/ref_hw_renault5turbo_1991_canada_b.jpg
  macro_golf     3/4-rear matched to Docs/Reference/DieCast/rear_ref_03_hatchback_diecast_on_wood.jpg
  rear_low       low rear 3/4 that looks under the tail (rear axle, inner wheel faces, base lip, exhaust tip)
  hero_34_front  the build script's own hero_34_front camera (front before/after proof)

Output: SourceArt/Blender/HatchlingS/preview/opus_rear/HatchlingS_<shot>_<tag>.png (1600 x 1200).
"""
import bpy, os, sys, math, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
UU = 0.01
_WPATH = os.path.join(os.path.dirname(HERE), "Wheel_W01_Dish", "build_Wheel_W01_Dish.py")
_spec = importlib.util.spec_from_file_location("build_Wheel_W01_Dish", _WPATH)
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(blend=os.path.join(HERE, "HatchlingS.blend"), shots=None, tag='after', pct=100, samples=128,
           out=os.path.join(HERE, "preview", "opus_rear"))
i = 0
while i < len(argv):
    a = argv[i]
    if a in ('--blend', '--shots', '--tag', '--pct', '--samples', '--out'):
        v = argv[i + 1]
        opt[a[2:]] = v.split(',') if a == '--shots' else (int(v) if a in ('--pct', '--samples') else v)
        i += 1
    i += 1
opt["out"] = os.path.abspath(opt["out"]); opt["blend"] = os.path.abspath(opt["blend"])

SUN_CHASE = (210.0, 20.0)        # low, warm, behind-right of the car: rakes across the tail and the boards
SHOTS = {
    'chase': dict(az=180.0, el=19.5, dist=3.6, lens=40, target=(0.0, 0.0, 0.14), focus=(-0.53, 0.0, 0.14),
                  fstop=11.0, sun=SUN_CHASE),
    'chase_navvy': dict(az=180.0, el=19.5, dist=3.6, lens=40, target=(0.0, 0.55, 0.14), focus=(-0.53, 0.3, 0.14),
                        fstop=11.0, sun=SUN_CHASE, navvy=(0.0, 1.10)),
    # R5 photo: camera behind-RIGHT of the car, ~22 deg up, close (phone macro, strong perspective)
    'macro_r5': dict(az=-128.0, el=21.0, dist=1.85, lens=50, target=(-0.04, -0.06, 0.17), focus=(-0.50, -0.34, 0.17),
                     fstop=5.6, sun=(-120.0, 34.0)),
    # Golf photo: camera behind-LEFT, ~11 deg up, medium distance
    'macro_golf': dict(az=133.0, el=11.0, dist=3.0, lens=70, target=(-0.02, 0.0, 0.17), focus=(-0.45, 0.36, 0.14),
                       fstop=8.0, sun=(120.0, 40.0)),
    'rear_low': dict(az=-160.0, el=4.0, dist=2.7, lens=85, target=(-0.30, -0.04, 0.10), focus=(-0.52, -0.20, 0.08),
                     fstop=8.0, sun=(205.0, 18.0)),
    # identical to build_HatchlingS.SHOTS['side_profile']
    'side_profile': dict(az=90.0, el=3.0, dist=8.2, lens=135, target=(0.02, 0.0, 0.21), focus=(0.0, 0.41, 0.18),
                         fstop=2.0, sun=(48.0, 28.0)),
    # identical to build_HatchlingS.SHOTS['hero_34_front']
    'hero_34_front': dict(az=34.0, el=9.5, dist=6.0, lens=100, target=(0.08, 0.0, 0.17), focus=(0.46, 0.34, 0.15),
                          fstop=0.7, sun=(-12.0, 24.0)),
}
shots = opt['shots'] or ['chase', 'chase_navvy', 'macro_r5', 'macro_golf', 'rear_low', 'hero_34_front']

bpy.ops.wm.open_mainfile(filepath=opt['blend'])
sc = bpy.context.scene
for cn in ("PreviewStage", "Navvy (benchmark)", "Preview"):
    c = bpy.data.collections.get(cn)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o)
        bpy.data.collections.remove(c)
for w in list(bpy.data.worlds):
    bpy.data.worlds.remove(w)
for l in list(bpy.data.lights):
    bpy.data.lights.remove(l)

wheel_ob = bpy.data.objects["SM_Wheel_W01_Dish"]
wheel_ob.hide_render = True
pcoll = W.get_coll("Preview")
WOBBLE = {"FL": (0.4, -0.3), "FR": (-0.3, 0.2), "RL": (-0.2, 0.4), "RR": (0.5, -0.2)}
for key, (x, y) in {"FL": (37.0, 36.6), "FR": (37.0, -36.6), "RL": (-37.0, 36.6), "RR": (-37.0, -36.6)}.items():
    o = bpy.data.objects.new("PV_Wheel_" + key, wheel_ob.data)
    W.link(o, pcoll)
    o.location = (x * UU, y * UU, 10.0 * UU)
    cam, toe = WOBBLE[key]
    sgn = 1.0 if y > 0 else -1.0
    o.rotation_euler = (math.radians(cam) * sgn, 0.0, (0.0 if y > 0 else math.pi) + math.radians(toe))

W.stage_setup_render(sc, samples=opt['samples'], pct=opt['pct'])
rig = W.stage_setup(sc)
nv = None
os.makedirs(opt['out'], exist_ok=True)
for name in shots:
    cfg = SHOTS[name]
    if cfg.get('navvy'):
        if nv is None:
            nv = W.import_navvy(location=(cfg['navvy'][0], cfg['navvy'][1], 0.0), yaw_deg=0.0)
            # report the lamp tint layer so a missing red never goes unnoticed
            for o in nv.children:
                if o.type == 'MESH':
                    print("[navvy] %s colour attrs %s mats %s" % (o.name, [a.name for a in o.data.color_attributes],
                                                                  [s.material.name if s.material else None for s in o.material_slots]))
        for o in nv.children:
            o.hide_render = False
    elif nv is not None:
        for o in nv.children:
            o.hide_render = True
    W.stage_render(sc, rig, cfg, os.path.join(opt['out'], "HatchlingS_%s_%s.png" % (name, opt['tag'])))
