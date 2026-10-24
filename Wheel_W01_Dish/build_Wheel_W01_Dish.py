"""
build_Wheel_W01_Dish.py  -  MODEL '93 / CozyCarGame, Slice 1A          (rev 2, spec 4b)
=====================================================================================
Shared toy wheel design W01_Dish: an ERA ONE-PIECE PLASTIC WHEEL (late-80s "basic wheel"):
a narrow black plastic ring ("tyre", same moulding, no rubber sidewall, no tread, just a
faint mould parting line) around a chrome-plated dish hub with a raised lip and a centre cap,
a through-bore where the peened steel axle end shows (the axle head is part of the casting's
Base mesh, not of the wheel). Hollow back like the real moulding.

Builds from an empty scene, saves Wheel_W01_Dish.blend, exports SM_Wheel_W01_Dish.fbx +
Wheel_W01_Dish.json, renders previews on the shared stage.

Run headless:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup
      --python build_Wheel_W01_Dish.py [-- --quick]

Conventions (SLICE_1A_BUILD_SPEC.md):
  * game scale in Blender metres: 1 uu = 0.01 m (real cm x 16)
  * origin = wheel centre, axle along Y, the OUTER (show) face points +Y (Blender left)
  * slots: Tire, Hub
This file also hosts the shared PREVIEW STAGE, a faithful copy of the Navvy benchmark stage
(SourceArt/Blender/Navvy/build_navvy.py: deck-board ground, sunset.exr HDRI rotated 200 deg x
warm filter, warm 7 W sun, 36 mm sensor, 100-135 mm lens, focus-object DOF, AgX Punchy) and a
Navvy FBX importer, so every Hatchling S render is judged under identical conditions and can
be put beside Navvy.  build_HatchlingS.py imports this module.
"""
import bpy, bmesh, math, os, sys, json, time
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = "Wheel_W01_Dish"
MESH_NAME = "SM_Wheel_W01_Dish"
UU = 0.01                       # Blender metres per uu
WHEEL_RADIUS_UU = 10.0          # ~15 % oversized for a 72 mm casting (real BW ~ 11 mm)
WHEEL_WIDTH_UU = 7.0            # narrow: 4.4 mm real
HUB_RADIUS_UU = 7.6             # chrome face radius (tyre ring is 2.4 uu = 1.5 mm)
BORE_R_UU = 0.95                # through-bore; the steel axle head sits in it
AXLE_HEAD_Y_UU = 3.62           # where a casting puts its peened axle head (from the wheel centre, outward)
SEGMENTS = 48
NAVVY_DIR = os.path.join(os.path.dirname(HERE), "Navvy")
W03_DIR = os.path.join(os.path.dirname(HERE), "Wheel_W03_Lug")


# =============================================================================
#  Generic helpers
# =============================================================================
def log(*a):
    print("[%s]" % ASSET, *a, flush=True)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.scale_length = 1.0
    return sc


def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def get_coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def apply_modifiers(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def tri_count(ob):
    me = ob.data
    return int(sum(len(p.vertices) - 2 for p in me.polygons))


def triangulate_ngons(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data)
    ng = [f for f in bm.faces if len(f.verts) > 4]
    if ng:
        bmesh.ops.triangulate(bm, faces=ng, quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.to_mesh(ob.data); bm.free()


def set_active(ob):
    bpy.context.view_layer.update()
    for o in list(bpy.context.view_layer.objects):
        if o is not None:
            o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)


def smart_uv(ob, uv_name="UV0", angle=66.0, margin=0.004):
    me = ob.data
    if uv_name not in me.uv_layers:
        me.uv_layers.new(name=uv_name)
    me.uv_layers.active = me.uv_layers[uv_name]
    set_active(ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=margin,
                             area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')


def export_fbx(ob, path):
    set_active(ob)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True,
                             apply_scale_options='FBX_SCALE_UNITS', axis_forward='X', axis_up='Z',
                             bake_space_transform=True, mesh_smooth_type='FACE', use_tspace=True,
                             add_leaf_bones=False, use_mesh_modifiers=True, object_types={'MESH'},
                             use_custom_props=False, path_mode='STRIP')
    log("exported", path)


# =============================================================================
#  Stand-in slot materials (named exactly like the UE slots)
# =============================================================================
def _principled(name):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (400, 0)
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.location = (0, 0)
    nt.links.new(bs.outputs[0], out.inputs['Surface'])
    return m, nt, bs


def _set(bs, key, val):
    if key in bs.inputs:
        bs.inputs[key].default_value = val


def make_slot_material(slot, **kw):
    """Preview stand-ins.  Casting scripts override Paint / Glass / Interior with their own."""
    m, nt, bs = _principled(slot)
    if slot == "Paint":
        col = kw.get("paint", (0.02, 0.08, 0.36, 1))
        _set(bs, 'Base Color', col); _set(bs, 'Metallic', 0.7); _set(bs, 'Roughness', 0.3)
        _set(bs, 'Coat Weight', 1.0); _set(bs, 'Coat Roughness', 0.02)
        m.diffuse_color = col
    elif slot == "Chrome":
        _set(bs, 'Base Color', (0.95, 0.95, 0.96, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.035)
        m.diffuse_color = (0.9, 0.9, 0.9, 1)
    elif slot == "Hub":            # vacuum-metallised plastic: bright, a touch softer than real chrome
        _set(bs, 'Base Color', (0.93, 0.93, 0.95, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.06)
        m.diffuse_color = (0.9, 0.9, 0.9, 1)
    elif slot == "Zamac":          # bare die-cast zinc (dull satin)
        _set(bs, 'Base Color', (0.62, 0.61, 0.58, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.3)
    elif slot == "Lamp":           # clear lens, tinted by the 'Col' vertex colour
        attr = nt.nodes.new('ShaderNodeVertexColor'); attr.location = (-400, 0)
        try:
            attr.layer_name = "Col"
        except Exception:
            pass
        _set(bs, 'Metallic', 0.0); _set(bs, 'Roughness', 0.04); _set(bs, 'IOR', 1.5)
        _set(bs, 'Transmission Weight', 0.85)
        nt.links.new(attr.outputs['Color'], bs.inputs['Base Color'])
    elif slot == "Glass":
        _set(bs, 'Base Color', (0.80, 0.82, 0.82, 1)); _set(bs, 'Roughness', 0.02)
        _set(bs, 'IOR', 1.49); _set(bs, 'Transmission Weight', 1.0)
    elif slot == "Interior":
        _set(bs, 'Base Color', kw.get("interior", (0.055, 0.050, 0.046, 1))); _set(bs, 'Roughness', 0.55)
        _set(bs, 'Specular IOR Level', 0.4)
    elif slot == "Base":           # black satin plastic; axles (Col.R) and rivets (Col.G) read as steel
        attr = nt.nodes.new('ShaderNodeVertexColor'); attr.location = (-700, 0)
        try:
            attr.layer_name = "Col"
        except Exception:
            pass
        sep = nt.nodes.new('ShaderNodeSeparateColor'); sep.location = (-500, 0)
        nt.links.new(attr.outputs['Color'], sep.inputs[0])
        mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; mx.location = (-300, 0)
        nt.links.new(sep.outputs[0], mx.inputs[0]); nt.links.new(sep.outputs[1], mx.inputs[1])
        mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.location = (-150, 150)
        mixc.inputs['A'].default_value = kw.get("base", (0.022, 0.022, 0.024, 1))
        mixc.inputs['B'].default_value = (0.66, 0.66, 0.67, 1)
        nt.links.new(mx.outputs[0], mixc.inputs['Factor'])
        nt.links.new(mixc.outputs['Result'], bs.inputs['Base Color'])
        nt.links.new(mx.outputs[0], bs.inputs['Metallic'])
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.location = (-150, -150)
        mr.inputs['To Min'].default_value = 0.46; mr.inputs['To Max'].default_value = 0.18
        nt.links.new(mx.outputs[0], mr.inputs['Value'])
        nt.links.new(mr.outputs['Result'], bs.inputs['Roughness'])
    elif slot == "Tire":           # hard black toy plastic with a moulded sheen (not rubber)
        _set(bs, 'Base Color', (0.014, 0.014, 0.015, 1)); _set(bs, 'Roughness', 0.30)
        _set(bs, 'Specular IOR Level', 0.5)
    return m


# =============================================================================
#  Shared PREVIEW STAGE  (faithful copy of build_navvy.py's stage)
# =============================================================================
STAGE = dict(env='sunset.exr', hdri=0.6, sun_energy=7.0, exposure=0.0)


def stage_studiolight(name):
    p = bpy.utils.system_resource('DATAFILES', path=os.path.join('studiolights', 'world', name))
    if not p or not os.path.exists(p):
        p = os.path.join(os.path.dirname(bpy.app.binary_path), '5.2', 'datafiles', 'studiolights', 'world', name)
    return p


def stage_setup_render(scene, samples=96, pct=100):
    scene.render.engine = 'CYCLES'
    dev = 'CPU'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for t in ('OPTIX', 'CUDA'):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                gpus = [d for d in prefs.devices if d.type == t]
                if gpus:
                    for d in prefs.devices:
                        d.use = (d.type == t)
                    dev = t
                    break
            except Exception:
                continue
    except Exception as e:
        log('GPU init failed:', e)
    scene.cycles.device = 'GPU' if dev != 'CPU' else 'CPU'
    log('RENDER DEVICE', dev)
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        scene.cycles.denoising_use_gpu = True
    except Exception:
        pass
    scene.cycles.max_bounces = 12
    scene.cycles.transmission_bounces = 12
    scene.cycles.transparent_max_bounces = 16
    scene.cycles.glossy_bounces = 6
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.blur_glossy = 0.5
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.resolution_percentage = pct
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.film_transparent = False
    vs = scene.view_settings
    vs.view_transform = 'AgX'
    for look in ('AgX - Punchy', 'AgX - Medium High Contrast', 'None'):
        try:
            vs.look = look
            break
        except Exception:
            continue
    vs.exposure = STAGE['exposure']
    return dev


def _n(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items():
        if k.startswith('i_'):
            n.inputs[k[2:].replace('_', ' ')].default_value = v
        else:
            setattr(n, k, v)
    return n


def _math(nt, op, a=None, b=None, c=None):
    m = nt.nodes.new('ShaderNodeMath')
    m.operation = op
    for i, x in enumerate((a, b, c)):
        if x is None:
            continue
        if isinstance(x, (int, float)):
            m.inputs[i].default_value = x
        else:
            nt.links.new(x, m.inputs[i])
    return m.outputs[0]


def _mrange(nt, val, f0, f1, t0=0.0, t1=1.0):
    m = nt.nodes.new('ShaderNodeMapRange')
    nt.links.new(val, m.inputs['Value'])
    m.inputs['From Min'].default_value = f0
    m.inputs['From Max'].default_value = f1
    m.inputs['To Min'].default_value = t0
    m.inputs['To Max'].default_value = t1
    return m.outputs[0]


def _mixc(nt, fac, a, b, blend='MIX'):
    m = nt.nodes.new('ShaderNodeMix')
    m.data_type = 'RGBA'
    m.blend_type = blend
    for sock, x in ((m.inputs[0], fac), (m.inputs[6], a), (m.inputs[7], b)):
        if isinstance(x, (int, float)):
            sock.default_value = x
        elif isinstance(x, tuple):
            sock.default_value = x
        else:
            nt.links.new(x, sock)
    return m.outputs[2]


def stage_wood_material():
    """Navvy's PreviewWood, verbatim: sun-bleached oiled deck boards at game scale (board 14 cm
    real = 2.24 m, gap 0.6 cm = 0.096 m, boards along X)."""
    m = bpy.data.materials.get('PreviewWood')
    if m:
        return m
    m = bpy.data.materials.new('PreviewWood')
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    L = nt.links
    bsdf = nt.nodes.get('Principled BSDF')
    tc = _n(nt, 'ShaderNodeTexCoord')
    sep = _n(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    X, Y = sep.outputs['X'], sep.outputs['Y']
    pitch, gapw = 2.336, 0.096
    yb = _math(nt, 'MULTIPLY_ADD', Y, 1.0 / pitch, 0.5)
    board = _math(nt, 'FLOOR', yb)
    fy = _math(nt, 'FRACT', yb)
    ly = _math(nt, 'MULTIPLY', _math(nt, 'SUBTRACT', fy, 0.5), pitch)
    r1 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D'); L.new(board, r1.inputs['W'])
    r2 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D')
    L.new(_math(nt, 'ADD', board, 17.3), r2.inputs['W'])
    R1, R2 = r1.outputs['Value'], r2.outputs['Value']
    gx = _math(nt, 'MULTIPLY_ADD', R1, 60.0, X)
    gy = _math(nt, 'MULTIPLY_ADD', _math(nt, 'SUBTRACT', R2, 0.5), 2.2, ly)
    gz = _math(nt, 'MULTIPLY_ADD', R1, 1.6, 0.35)
    gv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_math(nt, 'MULTIPLY', gx, 0.22), gv.inputs['X']); L.new(gy, gv.inputs['Y']); L.new(gz, gv.inputs['Z'])
    rings = _n(nt, 'ShaderNodeTexWave', wave_type='RINGS', rings_direction='X', wave_profile='SAW',
               i_Scale=3.4, i_Distortion=3.2, i_Detail=2.5, i_Detail_Scale=1.4, i_Detail_Roughness=0.55)
    L.new(gv.outputs[0], rings.inputs['Vector'])
    latewood = _mrange(nt, rings.outputs['Fac'], 0.62, 0.98, 0.0, 1.0)
    sv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_math(nt, 'MULTIPLY', gx, 0.5), sv.inputs['X'])
    L.new(_math(nt, 'MULTIPLY', ly, 26.0), sv.inputs['Y'])
    L.new(_math(nt, 'MULTIPLY', R2, 30.0), sv.inputs['Z'])
    streak = _n(nt, 'ShaderNodeTexNoise', i_Scale=2.2, i_Detail=8.0, i_Roughness=0.62)
    L.new(sv.outputs[0], streak.inputs['Vector'])
    pores = _mrange(nt, streak.outputs['Fac'], 0.3, 0.75, 0.0, 1.0)
    blot = _n(nt, 'ShaderNodeTexNoise', i_Scale=0.18, i_Detail=4.0, i_Roughness=0.6)
    L.new(tc.outputs['Object'], blot.inputs['Vector'])
    weather = _mrange(nt, blot.outputs['Fac'], 0.38, 0.72, 0.0, 0.6)
    ad = _math(nt, 'ABSOLUTE', ly)
    half = pitch * 0.5
    gap = _mrange(nt, ad, half - gapw * 0.5 - 0.004, half - gapw * 0.5, 0.0, 1.0)
    edge = _mrange(nt, ad, half - gapw * 0.5 - 0.07, half - gapw * 0.5, 0.0, 1.0)
    early = _mixc(nt, R1, (0.50, 0.33, 0.19, 1), (0.40, 0.25, 0.14, 1))
    late = _mixc(nt, R2, (0.22, 0.12, 0.06, 1), (0.17, 0.095, 0.05, 1))
    col = _mixc(nt, latewood, early, late)
    col = _mixc(nt, _math(nt, 'MULTIPLY', pores, 0.35), col, (0.20, 0.12, 0.07, 1))
    col = _mixc(nt, weather, col, (0.43, 0.38, 0.32, 1))
    col = _mixc(nt, _math(nt, 'MULTIPLY', edge, 0.45), col, (0.12, 0.075, 0.045, 1))
    col = _mixc(nt, gap, col, (0.008, 0.006, 0.004, 1))
    L.new(col, bsdf.inputs['Base Color'])
    rough = _math(nt, 'MULTIPLY_ADD', pores, 0.18, _math(nt, 'MULTIPLY_ADD', weather, 0.25, 0.5))
    L.new(rough, bsdf.inputs['Roughness'])
    h = _math(nt, 'MULTIPLY_ADD', latewood, 0.25, _math(nt, 'MULTIPLY', pores, 0.35))
    h = _math(nt, 'SUBTRACT', h, _math(nt, 'MULTIPLY', _math(nt, 'POWER', edge, 3.0), 2.5))
    bump = _n(nt, 'ShaderNodeBump', i_Strength=0.25, i_Distance=0.01)
    L.new(h, bump.inputs['Height'])
    L.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Specular IOR Level'].default_value = 0.45
    return m


def stage_setup(scene):
    """Navvy's setup_stage: world, deck ground, sun, camera with a DOF focus object, under-fill."""
    stage = get_coll('PreviewStage')
    w = bpy.data.worlds.new('World')
    scene.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    nt = w.node_tree
    bg = nt.nodes.get('Background')
    out = nt.nodes.get('World Output')
    env = nt.nodes.new('ShaderNodeTexEnvironment')
    env.image = bpy.data.images.load(stage_studiolight(STAGE['env']), check_existing=True)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(200.0))
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    warm = nt.nodes.new('ShaderNodeMix'); warm.data_type = 'RGBA'; warm.blend_type = 'MULTIPLY'
    warm.inputs[0].default_value = 1.0
    nt.links.new(env.outputs['Color'], warm.inputs[6])
    warm.inputs[7].default_value = (1.0, 0.9, 0.78, 1.0)
    nt.links.new(warm.outputs[2], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = STAGE['hdri']
    back = nt.nodes.new('ShaderNodeBackground')
    back.inputs['Color'].default_value = (0.62, 0.58, 0.52, 1.0)
    back.inputs['Strength'].default_value = 1.0
    lp = nt.nodes.new('ShaderNodeLightPath')
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MULTIPLY'
    nt.links.new(lp.outputs['Is Camera Ray'], fac.inputs[0])
    fac.inputs[1].default_value = 0.0
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(bg.outputs[0], mix.inputs[1])
    nt.links.new(back.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    gme = bpy.data.meshes.new('PreviewGround')
    s = 160.0
    gme.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    ground = bpy.data.objects.new('PreviewGround', gme)
    stage.objects.link(ground)
    gme.materials.append(stage_wood_material())
    ground.location = (0.0, 1.05, 0.0)
    sl = bpy.data.lights.new('Sun', 'SUN')
    sl.energy = STAGE['sun_energy']
    sl.angle = math.radians(0.9)
    sl.color = (1.0, 0.80, 0.58)
    sun = bpy.data.objects.new('Sun', sl)
    stage.objects.link(sun)
    cd = bpy.data.cameras.new('PreviewCam')
    cam = bpy.data.objects.new('PreviewCam', cd)
    stage.objects.link(cam)
    scene.camera = cam
    cd.sensor_fit = 'HORIZONTAL'
    cd.sensor_width = 36.0
    cd.clip_start = 0.05
    cd.clip_end = 600.0
    cd.dof.use_dof = True
    cd.dof.aperture_blades = 7
    cd.dof.aperture_rotation = math.radians(10.0)
    foc = bpy.data.objects.new('PreviewFocus', None)
    stage.objects.link(foc)
    cd.dof.focus_object = foc
    under = bpy.data.lights.new('UnderFill', 'AREA')
    under.energy = 0.0
    under.size = 8.0
    under.color = (1.0, 0.95, 0.88)
    uo = bpy.data.objects.new('UnderFill', under)
    stage.objects.link(uo)
    return dict(ground=ground, sun=sun, cam=cam, focus=foc, under=uo, env_map=mp, backdrop=fac)


def _aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def _sph(az, el, dist, target):
    a, e = math.radians(az), math.radians(el)
    t = Vector(target)
    return t + dist * Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))


def stage_render(scene, rig, cfg, path):
    """cfg like Navvy's SHOTS entries: az, el, dist, lens, target, focus, fstop, sun=(az, el),
    optional top=True / under=True."""
    cam, foc, sun = rig['cam'], rig['focus'], rig['sun']
    cam.data.lens = cfg['lens']
    cam.data.dof.aperture_fstop = cfg['fstop']
    cam.data.shift_x, cam.data.shift_y = cfg.get('shift', (0.0, 0.0))
    under = bool(cfg.get('under'))
    rig['ground'].hide_render = under
    rig['backdrop'].inputs[1].default_value = 1.0 if under else 0.0
    rig['under'].data.energy = 900.0 if under else 0.0
    saz, sel = cfg['sun']
    sun.rotation_euler = (-_sph(saz, sel, 1.0, (0, 0, 0))).to_track_quat('-Z', 'Y').to_euler()
    if cfg.get('top'):
        t = Vector(cfg['target'])
        cam.location = (t.x, t.y, cfg['dist'])
        cam.rotation_euler = (0.0, 0.0, 0.0)
    else:
        cam.location = _sph(cfg['az'], cfg['el'], cfg['dist'], cfg['target'])
        _aim(cam, cfg['target'])
    if under:
        uo = rig['under']
        uo.location = _sph(cfg['az'] + 40.0, -55.0, 3.2, cfg['target'])
        _aim(uo, cfg['target'])
    foc.location = cfg['focus']
    scene.camera = cam
    scene.render.filepath = path
    t0 = time.time()
    try:
        bpy.ops.render.render(write_still=True)
    except Exception as e:
        log("GPU render failed (%s); retrying on CPU" % e)
        scene.cycles.device = 'CPU'
        bpy.ops.render.render(write_still=True)
    log("RENDERED %s  %.1fs" % (os.path.basename(path), time.time() - t0))


# ---- Navvy (benchmark) import, with its own preview materials --------------------------------
def _nv_principled(name, base, metallic=0.0, rough=0.5, coat=0.0, coat_rough=0.03, trans=0.0, ior=1.5,
                   vcol=False, spec=0.5, peel=0.0):
    """Copy of build_navvy.principled() (same parameters -> same look)."""
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    b = nt.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*base, 1.0)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = rough
    b.inputs['IOR'].default_value = ior
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Coat Roughness'].default_value = coat_rough
    b.inputs['Transmission Weight'].default_value = trans
    b.inputs['Specular IOR Level'].default_value = spec
    if vcol:
        a = nt.nodes.new('ShaderNodeAttribute')
        a.attribute_name = 'Col'
        mix = nt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = 1.0
        mix.inputs[6].default_value = (*base, 1.0)
        nt.links.new(a.outputs['Color'], mix.inputs[7])
        nt.links.new(mix.outputs[2], b.inputs['Base Color'])
    if peel > 0:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        nz = nt.nodes.new('ShaderNodeTexNoise')
        nz.inputs['Scale'].default_value = 220.0
        nz.inputs['Detail'].default_value = 2.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bp = nt.nodes.new('ShaderNodeBump')
        bp.inputs['Strength'].default_value = peel
        bp.inputs['Distance'].default_value = 0.0005
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
        nt.links.new(bp.outputs['Normal'], b.inputs['Coat Normal'])
    m.diffuse_color = (*base, 1.0)
    return m


def navvy_materials():
    if bpy.data.materials.get('NV_Paint'):
        return {k: bpy.data.materials['NV_' + k] for k in
                ('Paint', 'Chrome', 'Lamp', 'Zamac', 'Base', 'Glass', 'Interior', 'Tire', 'Hub')}
    M = {}
    M['Paint'] = _nv_principled('NV_Paint', (1.0, 0.60, 0.008), metallic=0.12, rough=0.22, coat=1.0,
                                coat_rough=0.012, peel=0.08)
    M['Chrome'] = _nv_principled('NV_Chrome', (0.95, 0.95, 0.96), metallic=1.0, rough=0.035)
    M['Lamp'] = _nv_principled('NV_Lamp', (1.0, 1.0, 1.0), rough=0.03, trans=0.9, ior=1.5, vcol=True)
    M['Zamac'] = _nv_principled('NV_Zamac', (0.66, 0.65, 0.63), metallic=1.0, rough=0.2)
    M['Base'] = _nv_principled('NV_Base', (0.50, 0.49, 0.47), metallic=1.0, rough=0.42)
    M['Glass'] = _nv_principled('NV_Glass', (0.62, 0.70, 0.66), rough=0.02, trans=1.0, ior=1.45)
    M['Interior'] = _nv_principled('NV_Interior', (0.045, 0.045, 0.05), rough=0.55)
    M['Tire'] = _nv_principled('NV_Tire', (0.02, 0.02, 0.022), rough=0.62, spec=0.4)
    M['Hub'] = _nv_principled('NV_Hub', (1.0, 0.52, 0.0), rough=0.24, coat=0.6, coat_rough=0.05)
    return M


def _import_fbx(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def import_navvy(location=(0.0, 0.0, 0.0), yaw_deg=0.0, coll_name="Navvy (benchmark)"):
    """Imports the Navvy FBX parts + 4 W03_Lug wheels from their export folders, places them per
    Navvy.json (UE axes -> Blender: negate Y), assigns Navvy's own preview materials and parents
    everything to one empty at `location`.  Returns the root empty."""
    M = navvy_materials()
    coll = get_coll(coll_name)
    root = bpy.data.objects.new("NV_Root", None)
    link(root, coll)
    side = json.load(open(os.path.join(NAVVY_DIR, "Navvy.json")))
    parts = []
    for key, mesh in side["parts"].items():
        p = os.path.join(NAVVY_DIR, "export", mesh + ".fbx")
        if not os.path.exists(p):
            continue
        for o in _import_fbx(p):
            parts.append(o)
            if key == "Blade":
                h = side["feature"]["hinge"]
                o.location = (h[0] * UU, -h[1] * UU, h[2] * UU)
    wobj = _import_fbx(os.path.join(W03_DIR, "export", "SM_Wheel_W03_Lug.fbx"))
    wheel = [o for o in wobj if o.type == 'MESH'][0]
    wheel.hide_render = True; wheel.hide_viewport = True
    for k, p in side["wheels"].items():
        inst = bpy.data.objects.new("NV_Wheel_" + k, wheel.data)
        link(inst, coll)
        # the FBX importer may leave a rotation on the master: keep it, add the right-side yaw
        R = Matrix.Rotation(math.pi if k.endswith("R") else 0.0, 4, 'Z') @ wheel.matrix_world.to_3x3().to_4x4()
        inst.matrix_world = Matrix.Translation((p[0] * UU, -p[1] * UU, p[2] * UU)) @ R
        parts.append(inst)
    for o in parts:
        if o.type != 'MESH':
            continue
        for coll_old in list(o.users_collection):
            if coll_old is not coll:
                coll_old.objects.unlink(o)
        if coll not in o.users_collection:
            coll.objects.link(o)
        for s in o.material_slots:
            if s.material is None:
                continue
            base = s.material.name.split('.')[0]
            if base in M:
                s.link = 'OBJECT'
                s.material = M[base]
        mw = o.matrix_world.copy()
        o.parent = root
        o.matrix_world = mw
    root.location = location
    root.rotation_euler = (0.0, 0.0, math.radians(yaw_deg))
    bpy.context.view_layer.update()
    log("Navvy imported: %d objects" % len(parts))
    return root


# =============================================================================
#  The wheel
# =============================================================================
def round_polyline(pts, radii, tags):
    """pts: list of (r, y); radii per point (fillet radius, uu); tags per point (material of the
    segment that starts at that point). Returns new points + tags with quadratic-Bezier fillets."""
    out, otags = [], []
    n = len(pts)
    for i in range(n):
        p = np.array(pts[i], float)
        rad = radii[i]
        if i == 0 or i == n - 1 or rad <= 0:
            out.append(tuple(p)); otags.append(tags[i]); continue
        a = np.array(pts[i - 1], float); b = np.array(pts[i + 1], float)
        da, db = a - p, b - p
        la, lb = np.linalg.norm(da), np.linalg.norm(db)
        ua, ub = da / la, db / lb
        cosang = float(np.clip(np.dot(ua, ub), -1, 1))
        ang = math.acos(cosang)
        if ang > math.radians(175):
            out.append(tuple(p)); otags.append(tags[i]); continue
        t = rad / math.tan(ang / 2.0)
        t = min(t, 0.45 * la, 0.45 * lb)
        p0 = p + ua * t; p1 = p + ub * t
        nseg = max(1, min(4, int(round(rad / 0.35))))
        for k in range(nseg + 1):
            s = k / nseg
            q = (1 - s) ** 2 * p0 + 2 * (1 - s) * s * p + s ** 2 * p1
            out.append(tuple(q))
            otags.append(tags[i - 1] if s < 0.5 else tags[i])
    return out, otags


def wheel_profile():
    """(r, y, fillet, tag) closed loop: inner bore mouth -> hollow back -> inner face -> tread ->
    outer black face -> chrome lip -> dish -> centre cap -> outer bore mouth -> (bore wall back to
    the start).  Units: uu, final size (R 10, width 7)."""
    T, H = 0, 1
    hw = WHEEL_WIDTH_UU / 2.0          # 3.5
    R = WHEEL_RADIUS_UU
    P = [
        (BORE_R_UU, -2.30, 0.0, T),    # inner bore mouth
        (2.05, -2.30, 0.30, T),        # inner bore boss face
        (2.35, -1.55, 0.30, T),
        (5.50, -1.55, 0.70, T),        # hollow back (recess floor)
        (6.35, -hw + 0.15, 0.45, T),   # recess wall
        (8.80, -hw, 0.75, T),          # inner face of the ring
        (R, -2.75, 1.00, T),           # inner shoulder (soft, moulded)
        (R + 0.03, -0.14, 0.0, T),     # flat tread; faint parting line
        (R + 0.09, 0.00, 0.0, T),
        (R + 0.03, 0.14, 0.0, T),
        (R, 2.75, 1.00, T),            # outer shoulder
        (8.80, hw, 0.60, T),           # flat outer face of the black ring
        (7.95, hw - 0.04, 0.20, T),
        (7.72, hw - 0.42, 0.15, T),    # small step where the plating mask ends
        (7.50, hw - 0.42, 0.15, H),    # -> chrome from here
        (7.28, hw + 0.30, 0.30, H),    # raised hub lip
        (6.62, hw + 0.48, 0.35, H),
        (6.10, hw + 0.08, 0.45, H),    # lip falls into the dish
        (4.30, hw - 0.78, 1.70, H),    # concave dish floor
        (2.70, hw - 0.62, 0.55, H),
        (2.22, hw + 0.05, 0.30, H),    # centre cap
        (1.55, hw + 0.24, 0.30, H),
        (BORE_R_UU, hw + 0.10, 0.12, T),   # outer bore mouth; bore wall is black
        (BORE_R_UU, -2.30, 0.0, T),    # back to the start (merged)
    ]
    pts = [(p[0], p[1]) for p in P]
    rad = [p[2] for p in P]
    tags = [p[3] for p in P]
    return round_polyline(pts, rad, tags)


def profile_normals(pts):
    P = np.array(pts, float)
    seg = P[1:] - P[:-1]
    ln = np.linalg.norm(seg, axis=1); ln[ln == 0] = 1e-9
    tdir = seg / ln[:, None]
    nseg = np.stack([tdir[:, 1], -tdir[:, 0]], 1)
    nend0 = nseg.copy(); nend1 = nseg.copy()
    for i in range(1, len(P) - 1):
        a, b = nseg[i - 1], nseg[i]
        if np.dot(a, b) > math.cos(math.radians(38)):
            m = a + b; m /= np.linalg.norm(m)
            nend1[i - 1] = m; nend0[i] = m
    return P, nseg, nend0, nend1


def set_wheel_normals(ob, pts):
    """Analytic custom normals from the revolved profile."""
    me = ob.data
    P, nseg, n0, n1 = profile_normals(pts)
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3) / UU
    li = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", li)
    lt = np.empty(len(me.polygons), dtype=np.int64); me.polygons.foreach_get("loop_total", lt)
    face_of_loop = np.repeat(np.arange(len(me.polygons)), lt)
    fc = np.zeros((len(me.polygons), 3))
    np.add.at(fc, face_of_loop, co[li]); fc /= lt[:, None]

    def rz(p):
        return np.stack([np.hypot(p[:, 0], p[:, 2]), p[:, 1]], 1)
    fry = rz(fc)
    A = P[:-1]; B = P[1:]
    AB = B - A; L2 = (AB ** 2).sum(1); L2[L2 == 0] = 1e-12
    t = ((fry[:, None, :] - A[None]) * AB[None]).sum(2) / L2[None]
    t = np.clip(t, 0, 1)
    proj = A[None] + t[..., None] * AB[None]
    fseg = np.argmin(((fry[:, None, :] - proj) ** 2).sum(2), 1)
    lp = co[li]
    lry = rz(lp)
    s = fseg[face_of_loop]
    t = np.clip(((lry - A[s]) * AB[s]).sum(1) / L2[s], 0, 1)[:, None]
    n2 = (1 - t) * n0[s] + t * n1[s]
    n2 /= np.linalg.norm(n2, axis=1)[:, None]
    r = np.hypot(lp[:, 0], lp[:, 2]); r[r < 1e-9] = 1e-9
    nrm = np.stack([n2[:, 0] * lp[:, 0] / r, n2[:, 1], n2[:, 0] * lp[:, 2] / r], 1)
    me.normals_split_custom_set([tuple(x) for x in nrm])


def build_wheel(mat_tire=None, mat_hub=None, name=MESH_NAME, segments=SEGMENTS, coll=None):
    """Builds the wheel at game scale (metres), origin at the wheel centre, axle = Y, outer face +Y."""
    mat_tire = mat_tire or bpy.data.materials.get("Tire") or make_slot_material("Tire")
    mat_hub = mat_hub or bpy.data.materials.get("Hub") or make_slot_material("Hub")
    pts, tags = wheel_profile()
    bm = bmesh.new()
    rings = []
    for (r, y) in pts:
        ring = []
        for k in range(segments):
            a = 2 * math.pi * k / segments
            ring.append(bm.verts.new((r * math.cos(a) * UU, y * UU, r * math.sin(a) * UU)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        mi = tags[i]
        for k in range(segments):
            k2 = (k + 1) % segments
            f = bm.faces.new((A[k], A[k2], B[k2], B[k]))
            f.material_index = mi
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    me.materials.append(mat_tire)
    me.materials.append(mat_hub)
    ob = bpy.data.objects.new(name, me)
    link(ob, coll)
    for p in me.polygons:
        p.use_smooth = True
    triangulate_ngons(ob)
    set_wheel_normals(ob, pts)
    log("profile points:", len(pts), "segments:", segments, "tris:", tri_count(ob))
    return ob


def wheel_uvs(ob):
    me = ob.data
    smart_uv(ob, "UV0", angle=60.0, margin=0.006)
    # UV1: planar side projection (X,Z) -> 0..1, for printed hub tampo
    uv1 = me.uv_layers.new(name="UV1")
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    li = np.empty(len(me.loops), dtype=np.int64); me.loops.foreach_get("vertex_index", li)
    p = co[li]
    R = WHEEL_RADIUS_UU * UU * 1.05
    uv = np.stack([(p[:, 0] / R) * 0.5 + 0.5, (p[:, 2] / R) * 0.5 + 0.5], 1)
    uv1.data.foreach_set("uv", uv.ravel())
    me.uv_layers.active = me.uv_layers["UV0"]


def wheel_sidecar(ob, path):
    data = {
        "wheel_design": "W01_Dish",
        "mesh": MESH_NAME,
        "description": "Era one-piece plastic toy wheel: narrow black plastic ring (no rubber sidewall, no tread, faint mould parting line) "
                       "around a chrome-plated dish hub with a raised lip and a centre cap; through-bore where the casting's steel axle head shows; hollow back.",
        "radius": WHEEL_RADIUS_UU,
        "width": WHEEL_WIDTH_UU,
        "hub_radius": HUB_RADIUS_UU,
        "bore_radius": BORE_R_UU,
        "axle_head_offset": AXLE_HEAD_Y_UU,
        "axle_head_note": "the peened steel axle head belongs to the casting (Base mesh); it sits at wheel centre +/- axle_head_offset along the axle, filling the bore",
        "units": "uu (1 uu = 1/16 real cm); FBX authored in Blender metres, 1 m = 100 uu",
        "origin": "wheel centre",
        "axle_axis": "Y",
        "outer_face": "Blender +Y = left side of the car. After the FBX import that is UE -Y (left). Use as-is on the LEFT wheels (FL, RL); rotate 180 deg yaw for the RIGHT wheels (FR, RR).",
        "spin_axis_ue": "Y",
        "slots": ["Tire", "Hub"],
        "slot_look": {"Tire": "hard black toy plastic with a moulded sheen (roughness ~0.3), NOT rubber",
                      "Hub": "vacuum-metallised chrome (roughness 0.04-0.08)"},
        "tris": tri_count(ob),
        "uv": {"UV0": "smart unwrap, non-overlapping", "UV1": "planar side projection (hub face centred at 0.5,0.5)"},
        "native_for": ["HatchlingS"],
        "scale_note": "If another casting needs a different radius, scale uniformly by radius/%.1f." % WHEEL_RADIUS_UU,
        "source": "SourceArt/Blender/Wheel_W01_Dish/build_Wheel_W01_Dish.py",
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log("sidecar", path)


def axle_head_geo(y_outer, r_shank=0.9, r_head=1.32, h=0.5, seg=20):
    """Peened axle head (verts in uu, faces), outward along +Y from y_outer (use negative scale
    for the right side).  Exposed for castings that put the head in their Base mesh."""
    prof = [(r_shank, y_outer - 1.2), (r_shank, y_outer - 0.05), (r_head, y_outer - 0.02)]
    for i in range(1, 5):
        a = math.radians(90.0 * i / 4)
        prof.append((r_head * math.cos(a), y_outer + h * math.sin(a)))
    prof[-1] = (0.0, y_outer + h)
    V, F = [], []
    rings = []
    for (r, y) in prof:
        if r < 1e-6:
            rings.append([len(V)]); V.append((0.0, y, 0.0))
        else:
            idx = []
            for k in range(seg):
                a = 2 * math.pi * k / seg
                idx.append(len(V)); V.append((r * math.cos(a), y, r * math.sin(a)))
            rings.append(idx)
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        for k in range(seg):
            k2 = (k + 1) % seg
            if len(B) == 1:
                F.append((A[k], A[k2], B[0]))
            else:
                F.append((A[k], A[k2], B[k2], B[k]))
    return V, F


def main(quick=False):
    t0 = time.time()
    sc = reset_scene()
    make_slot_material("Tire"); make_slot_material("Hub")
    ob = build_wheel()
    wheel_uvs(ob)
    exp = os.path.join(HERE, "export", MESH_NAME + ".fbx")
    blend = os.path.join(HERE, ASSET + ".blend")
    export_fbx(ob, exp)
    wheel_sidecar(ob, os.path.join(HERE, ASSET + ".json"))
    # previews on the shared (Navvy) stage --------------------------------------
    stage_setup_render(sc, samples=32 if quick else 96, pct=50 if quick else 100)
    rig = stage_setup(sc)
    R = WHEEL_RADIUS_UU * UU
    ob.hide_render = True                      # the export master stays at the origin
    pv_coll = get_coll("Preview")
    w1 = bpy.data.objects.new("PV_Wheel_stand", ob.data); link(w1, pv_coll)
    w1.location = (0.0, 0.0, R)
    w1.rotation_euler = (0.0, 0.0, math.radians(-8.0))
    w2 = bpy.data.objects.new("PV_Wheel_flat", ob.data); link(w2, pv_coll)
    w2.rotation_euler = (math.radians(90), 0.0, math.radians(20))      # show face to the sky
    w2.location = (-0.26, 0.20, (WHEEL_WIDTH_UU / 2) * UU)
    w3 = bpy.data.objects.new("PV_Wheel_back", ob.data); link(w3, pv_coll)
    w3.rotation_euler = (math.radians(-90), 0.0, math.radians(-30))    # hollow back up
    w3.location = (-0.30, -0.18, (WHEEL_WIDTH_UU / 2 + 0.48) * UU)
    # the axle head the casting adds, shown in the standing wheel for the look
    V, F = axle_head_geo(AXLE_HEAD_Y_UU)
    hm = bpy.data.meshes.new("PV_AxleHead"); hm.from_pydata([(a * UU, b * UU, c * UU) for a, b, c in V], [], F)
    hm.materials.append(make_slot_material("Zamac"))
    for p in hm.polygons:
        p.use_smooth = True
    ho = bpy.data.objects.new("PV_AxleHead", hm); link(ho, pv_coll)
    ho.parent = w1
    pv = os.path.join(HERE, "preview")
    os.makedirs(pv, exist_ok=True)
    wc = (0.0, 0.0, R)
    stage_render(sc, rig, dict(az=62.0, el=14.0, dist=1.9, lens=100, target=(-0.08, 0.0, R * 0.8),
                               focus=(0.0, 0.05, R), fstop=2.0, sun=(60.0, 26.0)),
                 os.path.join(pv, "W01_Dish_34.png"))
    w2.hide_render = True; w3.hide_render = True
    stage_render(sc, rig, dict(az=90.0, el=4.0, dist=1.6, lens=100, target=wc,
                               focus=(0.0, 0.05, R), fstop=4.0, sun=(60.0, 30.0)),
                 os.path.join(pv, "W01_Dish_face.png"))
    ob.location = (0, 0, 0)
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    log("saved", blend, "total %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(quick="--quick" in argv)
