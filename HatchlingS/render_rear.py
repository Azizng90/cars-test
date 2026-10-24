"""render_rear.py - rear / chase-camera look-dev renders for the Hatchling S (spec 4b rules 11-15).

  blender.exe -b --factory-startup --python render_rear.py -- [--blend X.blend] [--shots a,b] [--suffix _i1]
                                                                [--pct 50] [--samples 32] [--out DIR]

Opens an already-built HatchlingS.blend (written by build_HatchlingS.py), throws away its saved preview
stage and sets up the shared Navvy stage again (same sun / deck / camera conventions as every other
casting preview), then renders the rear shots:

  chase         from behind, ~17 deg above, 3 car lengths back, 50 mm, warm low sun, deck boards (the game camera)
  chase_navvy   the same camera / light with Navvy beside the car (family check, rule 9)
  macro         3/4-rear macro, 100 mm
  macro_navvy   3/4-rear with Navvy beside it
  under_rear    low rear 3/4 (8 deg) that looks under the tail: axle, inner wheel faces, valance, exhaust tip
"""
import bpy, os, sys, math, importlib.util
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
UU = 0.01
_WPATH = os.path.join(os.path.dirname(HERE), "Wheel_W01_Dish", "build_Wheel_W01_Dish.py")
_spec = importlib.util.spec_from_file_location("build_Wheel_W01_Dish", _WPATH)
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
opt = dict(blend=os.path.join(HERE, "HatchlingS.blend"), shots=None, suffix='', pct=100, samples=96,
           out=os.path.join(HERE, "preview", "rear_pass"))
i = 0
while i < len(argv):
    a = argv[i]
    if a == '--cpu':
        opt['cpu'] = True
    elif a in ('--blend', '--shots', '--suffix', '--pct', '--samples', '--out'):
        v = argv[i + 1]
        opt[a[2:]] = v.split(',') if a == '--shots' else (int(v) if a in ('--pct', '--samples') else v)
        i += 1
    i += 1

SUN_LOW = (212.0, 21.0)          # behind-left, low and warm: rakes across the tail and the deck boards
SHOTS = {
    'chase': dict(az=180.0, el=17.0, dist=3.6, lens=50, target=(-0.08, 0.0, 0.14), focus=(-0.53, 0.0, 0.16),
                  fstop=11.0, sun=SUN_LOW),
    'chase_navvy': dict(az=180.0, el=17.0, dist=3.7, lens=40, target=(-0.08, 0.50, 0.14), focus=(-0.53, 0.0, 0.16),
                        fstop=11.0, sun=SUN_LOW, navvy=(0.0, 1.0)),
    'macro': dict(az=-146.0, el=15.0, dist=2.3, lens=100, target=(-0.30, 0.0, 0.17), focus=(-0.52, -0.16, 0.16),
                  fstop=4.5, sun=(205.0, 22.0)),
    'macro_navvy': dict(az=-146.0, el=15.0, dist=3.4, lens=70, target=(-0.35, 0.40, 0.16), focus=(-0.52, -0.16, 0.16),
                        fstop=5.6, sun=(205.0, 22.0), navvy=(-0.52, 0.98)),
    'rear_wheel': dict(az=-128.0, el=6.0, dist=1.15, lens=100, target=(-0.42, -0.30, 0.09), focus=(-0.42, -0.36, 0.09),
                       fstop=5.6, sun=(205.0, 22.0)),
    'under_rear': dict(az=-158.0, el=7.0, dist=2.0, lens=100, target=(-0.42, 0.0, 0.08), focus=(-0.45, -0.10, 0.07),
                       fstop=5.6, sun=(200.0, 18.0)),
}
opt["out"] = os.path.abspath(opt["out"]); opt["blend"] = os.path.abspath(opt["blend"])
shots = opt['shots'] or ['chase', 'macro', 'chase_navvy', 'macro_navvy']

bpy.ops.wm.open_mainfile(filepath=opt['blend'])
sc = bpy.context.scene
# drop the saved preview stage + Navvy so the stage is rebuilt identically
for cn in ("PreviewStage", "Navvy (benchmark)"):
    c = bpy.data.collections.get(cn)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o)
        bpy.data.collections.remove(c)
for w in list(bpy.data.worlds):
    bpy.data.worlds.remove(w)
for l in list(bpy.data.lights):
    bpy.data.lights.remove(l)

# wheels: the build script only places its preview wheels while rendering, so place them here (same numbers)
wheel_ob = bpy.data.objects["SM_Wheel_W01_Dish"]
pcoll = W.get_coll("Preview")
for o in [o for o in bpy.data.objects if o.name.startswith("PV_Wheel_")]:
    bpy.data.objects.remove(o)
WOBBLE = {"FL": (0.4, -0.3), "FR": (-0.3, 0.2), "RL": (-0.2, 0.4), "RR": (0.5, -0.2)}
for key, (x, y) in {"FL": (37.0, 36.6), "FR": (37.0, -36.6), "RL": (-37.0, 36.6), "RR": (-37.0, -36.6)}.items():
    o = bpy.data.objects.new("PV_Wheel_" + key, wheel_ob.data)
    W.link(o, pcoll)
    o.location = (x * UU, y * UU, 10.0 * UU)
    cam, toe = WOBBLE[key]
    sgn = 1.0 if y > 0 else -1.0
    o.rotation_euler = (math.radians(cam) * sgn, 0.0, (0.0 if y > 0 else math.pi) + math.radians(toe))

W.stage_setup_render(sc, samples=opt['samples'], pct=opt['pct'])
if opt.get('cpu'):
    sc.cycles.device = 'CPU'      # the shared GPU is often saturated by other agents' renders
rig = W.stage_setup(sc)
nv = None
os.makedirs(opt['out'], exist_ok=True)
for name in shots:
    cfg = SHOTS[name]
    if cfg.get('navvy'):
        if nv is not None:
            for o in list(nv.children):
                bpy.data.objects.remove(o)
            bpy.data.objects.remove(nv)
            c = bpy.data.collections.get("Navvy (benchmark)")
            if c:
                bpy.data.collections.remove(c)
        nv = W.import_navvy(location=(cfg['navvy'][0], cfg['navvy'][1], 0.0), yaw_deg=0.0)
    elif nv is not None:
        for o in nv.children:
            o.hide_render = True
    W.stage_render(sc, rig, cfg, os.path.join(opt['out'], "HatchlingS_rear_" + name + opt['suffix'] + ".png"))
