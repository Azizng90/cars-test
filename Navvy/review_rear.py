"""review_rear.py - rear / chase-camera look-dev for Navvy (spec 4b rules 11-15).

Imports the EXPORTED FBXs (so it judges exactly what ships), puts the tampo texture on Paint through UV1_Tampo, and renders
  chase       : from behind, 17 deg above, ~3 car lengths, 40 mm, low warm sun, deck boards
  rear34      : 3/4-rear macro
  chase_fam / rear34_fam : the same with a Vortex beside it (family check)
Usage: blender -b --factory-startup --python review_rear.py -- --exp <export dir> --wheel <fbx> --tex <textures dir> --tag before
                 [--samples 48 --pct 50 --shots chase,rear34 --variant GransPick]
"""
import bpy, sys, os, re, math
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
argv = sys.argv[sys.argv.index('--') + 1:]
def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d
EXP = os.path.abspath(arg('--exp', os.path.join(HERE, 'export')))
WHEEL = os.path.abspath(arg('--wheel', os.path.join(ART, 'Wheel_W03_Lug', 'export', 'SM_Wheel_W03_Lug.fbx')))
TEX = os.path.abspath(arg('--tex', os.path.join(HERE, 'textures')))
TAG = arg('--tag', 'after')
VARIANT = arg('--variant', 'GransPick')
OUT = os.path.join(HERE, 'review')
src = open(os.path.join(HERE, 'build_navvy.py'), encoding='utf-8').read()
src = re.sub(r'\nmain\(\)\s*$', '\n', src)
sys.argv = [sys.argv[0], '--', '--samples', arg('--samples', '48'), '--pct', arg('--pct', '50'), '--suffix', '_' + TAG]
g = {'__file__': os.path.join(HERE, 'build_navvy.py'), '__name__': 'bn'}
exec(compile(src, 'build_navvy.py', 'exec'), g)
U = g['U']

scene = g['reset_scene']()
g['EXP'] = g['new_coll']('Export')
g['build_materials']()
MATS = g['MATS']

def imp(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path, axis_forward='X', axis_up='Z', global_scale=1.0)
    return [o for o in bpy.data.objects if o not in before and o.type == 'MESH']

def tampo_paint(name, png, base):
    m = MATS['Paint'].copy(); m.name = name
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = bpy.data.images.load(png)
    tx.image.colorspace_settings.name = 'sRGB'
    tx.interpolation = 'Cubic'
    uvn = nt.nodes.new('ShaderNodeUVMap'); uvn.uv_map = 'UV1_Tampo'
    nt.links.new(uvn.outputs[0], tx.inputs[0])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (*base, 1.0)
    nt.links.new(tx.outputs['Alpha'], mix.inputs[0])
    nt.links.new(tx.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    return m

def fix_mats(ob, paint=None):
    for i, s in enumerate(ob.material_slots):
        nm = s.material.name.split('.')[0] if s.material else ''
        if nm == 'Paint' and paint:
            s.material = paint
        elif nm in MATS:
            s.material = MATS[nm]

parts = {}
for p in ('Body', 'Base', 'Windows', 'Interior', 'Blade'):
    ob = imp(os.path.join(EXP, 'SM_Navvy_%s.fbx' % p))[0]
    parts[p] = ob
body_paint = tampo_paint('PaintBody', os.path.join(TEX, 'T_Navvy_%s_Tampo.png' % VARIANT), (1.0, 0.60, 0.008))
blade_paint = tampo_paint('PaintBlade', os.path.join(TEX, 'T_Navvy_%s_BladeTampo.png' % VARIANT), (1.0, 0.60, 0.008))
for p, ob in parts.items():
    fix_mats(ob, body_paint if p == 'Body' else blade_paint if p == 'Blade' else None)
parts['Blade'].location = Vector(g['HINGE']) * U
wheel = imp(WHEEL)[0]
fix_mats(wheel)
wheel.hide_render = True
AX, TR, AZ = g['AXLE_X'], g['TRACK_Y'], g['AXLE_Z']
for key, (wx, wy) in {'FL': (AX, TR), 'FR': (AX, -TR), 'RL': (-AX, TR), 'RR': (-AX, -TR)}.items():
    inst = bpy.data.objects.new('Wheel_' + key, wheel.data)
    scene.collection.objects.link(inst)
    inst.location = (wx * U, wy * U, AZ * U)
    if wy < 0:
        inst.rotation_euler = (0, 0, math.pi)
    for mod in wheel.modifiers:
        inst.modifiers.new(mod.name, mod.type)

# ---- family: Vortex beside Navvy (read-only import of its export) ----
def add_vortex(yoff):
    import json
    vd = os.path.join(ART, 'Vortex')
    vj = json.load(open(os.path.join(vd, 'Vortex.json')))
    paint = MATS['Paint'].copy(); paint.name = 'PaintVortex'
    paint.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.20, 0.05, 0.42, 1)
    objs = []
    for p in ('Body', 'Base', 'Windows', 'Interior'):
        o = imp(os.path.join(vd, 'export', 'SM_Vortex_%s.fbx' % p))[0]
        fix_mats(o, paint); o.location = (0, yoff * U, 0); objs.append(o)
    wf = os.path.join(ART, 'Wheel_W02_Fan', 'export', 'SM_Wheel_W02_Fan.fbx')
    w = imp(wf)[0]; fix_mats(w); w.hide_render = True; objs.append(w)
    r = vj['wheel_radius']
    for key, (x, y, z) in vj['wheels'].items():
        by = -y
        inst = bpy.data.objects.new('VW_' + key, w.data)
        scene.collection.objects.link(inst)
        inst.location = (x * U, (by + yoff) * U, z * U)
        if by < 0:
            inst.rotation_euler = (0, 0, math.pi)
        objs.append(inst)
    return objs
FAM = add_vortex(115.0)
for o in FAM:
    o.hide_render = True
    if o.name.startswith('Wheel_W02') or o.name.endswith('.001') and False:
        pass
for o in bpy.data.objects:
    if o.name.startswith('SM_Wheel_W02'):
        o.hide_render = True

g['setup_render'](scene)
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
rig = g['setup_stage'](scene)

SH = g['SHOTS']
SH.clear()
SH['chase'] = dict(az=180.0, el=17.0, dist=3.55, lens=40, target=(-0.05, 0.0, 0.17), focus=(-0.6, 0.0, 0.2), fstop=9.0, sun=(-150.0, 17.0))
SH['rear34'] = dict(az=-145.0, el=13.0, dist=5.2, lens=100, target=(-0.30, 0.0, 0.2), focus=(-0.6, -0.2, 0.2), fstop=1.6, sun=(-120.0, 20.0))
SH['chase_fam'] = dict(SH['chase'], target=(-0.05, 0.57, 0.17), focus=(-0.6, 0.57, 0.2), dist=4.3)
SH['rear34_fam'] = dict(SH['rear34'], target=(-0.30, 0.55, 0.2), dist=7.2, lens=100, fstop=2.8)
SH['rear_low'] = dict(az=-150.0, el=5.0, dist=3.0, lens=100, target=(-0.38, -0.25, 0.14), focus=(-0.4, -0.3, 0.14), fstop=3.5, sun=(-120.0, 20.0))
shots = arg('--shots', 'chase,rear34,chase_fam,rear34_fam').split(',')
os.makedirs(OUT, exist_ok=True)
for s in shots:
    fam = s.endswith('_fam')
    for o in FAM:
        if not o.name.startswith('SM_Wheel_W02'):
            o.hide_render = not fam
    g['render_shots'](scene, rig, OUT, [s], blade_ob=None)
print('REVIEW DONE')
