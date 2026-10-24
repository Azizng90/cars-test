"""
build_navvy.py -- MODEL '93, Slice 1A casting "Navvy" (KESTREL MOTOR WORKS, Lifted class)
plus the shared wheel design W03_Lug.

Reproducible: builds everything from an empty scene, saves navvy.blend, exports one FBX per part
(spec section 2 settings), writes the JSON sidecars and renders the look-dev previews.

Run (headless):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup --python build_navvy.py -- [options]
Options:
  --no-render        skip previews            --no-export   skip FBX/JSON/.blend
  --shots a,b,c      only these previews      --samples N   Cycles samples (default 96)
  --pct N            resolution percentage    --wheel-only  build/export/render only W03_Lug
                                              (that is what ../Wheel_W03_Lug/build_Wheel_W03_Lug.py runs)
  look-dev only: --override '{"hero_34_front": {"sun": [az, el], "fstop": 0.7}}'  --suffix _A
                 --sun-energy W  --hdri strength  --exposure EV  --env courtyard.exr|sunset.exr
Previews (preview/): hero_34_front, side_profile, rear_34, top_down, underside (base), blade_raised
(+ ../Wheel_W03_Lug/preview/wheel_close.png). Stage: wooden deck boards, sunset.exr HDRI + warm sun,
100-135 mm lens with shallow DOF, Cycles GPU (OptiX/CUDA, CPU fallback), AgX Punchy.
Budgets (spec 4): body 30-80k tris, base 5-15k, windows 1-3k, wheel 2-6k -- printed as PART lines.

Conventions (Docs/Build/SLICE_1A_BUILD_SPEC.md):
  * Geometry is authored in uu (1 uu = 1/16 real cm) and scaled by U = 0.01 into Blender metres.
  * Blender axes: front = +X, left = +Y, up = +Z. Origin: ground level, centred between the axles.
  * Sidecar values are in uu, UE axes (X fwd, Y RIGHT, Z up) -> Blender Y is negated.
"""
import bpy, bmesh, math, json, os, sys, time
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
WHEEL_DIR = os.path.join(os.path.dirname(HERE), 'Wheel_W03_Lug')
U = 0.01  # uu -> Blender metres
# extra bevel segments per part (Nanite body budget 30-80k tris, base 5-15k) and round-part density
BEVEL_ADD = {'Body': 3, 'Base': 3, 'Blade': 2, 'Interior': 1, 'Windows': 0, 'Wheel': 0}
CYL = {'mul': 1.0}

# ------------------------------------------------------------------------------------------------
# options
# ------------------------------------------------------------------------------------------------
def parse_args():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    o = dict(render=True, export=True, shots=None, samples=96, pct=100, wheel_only=False, override=None,
             suffix='', sun_energy=None, hdri=None, exposure=None, env='sunset.exr')
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--no-render': o['render'] = False
        elif a == '--no-export': o['export'] = False
        elif a == '--wheel-only': o['wheel_only'] = True
        elif a == '--shots': o['shots'] = argv[i + 1].split(','); i += 1
        elif a == '--samples': o['samples'] = int(argv[i + 1]); i += 1
        elif a == '--pct': o['pct'] = int(argv[i + 1]); i += 1
        elif a == '--override': o['override'] = json.loads(argv[i + 1]); i += 1   # look-dev: per-shot overrides
        elif a == '--suffix': o['suffix'] = argv[i + 1]; i += 1
        elif a == '--sun-energy': o['sun_energy'] = float(argv[i + 1]); i += 1
        elif a == '--hdri': o['hdri'] = float(argv[i + 1]); i += 1
        elif a == '--exposure': o['exposure'] = float(argv[i + 1]); i += 1
        elif a == '--env': o['env'] = argv[i + 1]; i += 1
        i += 1
    return o

OPT = parse_args()

# ------------------------------------------------------------------------------------------------
# casting dimensions (uu, Blender axes)
# ------------------------------------------------------------------------------------------------
AXLE_X = 33.0          # front axle +33, rear axle -33  (origin centred between axles)
AXLE_Z = 14.0          # axle height == wheel radius (wheels sit on the ground)
WHEEL_R = 14.0         # lug tops
WHEEL_W = 14.0
TRACK_Y = 36.0         # wheel centre |y|
HINGE = (-4.0, 0.0, 32.0)   # blade arm hinge axis (along Y)
BLADE_RANGE = (-1.4, 18.0)  # UE pitch degrees, + raises the blade; -1.4 = cutting edge on the ground

SLOTS = {
    'Body': ['Paint', 'Chrome', 'Lamp', 'Zamac'],
    'Base': ['Base'],
    'Windows': ['Glass'],
    'Interior': ['Interior'],
    'Blade': ['Paint', 'Zamac'],
    'Wheel': ['Tire', 'Hub'],
}
PART_NAMES = {
    'Body': 'SM_Navvy_Body', 'Base': 'SM_Navvy_Base', 'Windows': 'SM_Navvy_Windows',
    'Interior': 'SM_Navvy_Interior', 'Blade': 'SM_Navvy_Blade', 'Wheel': 'SM_Wheel_W03_Lug',
}
TINT_CLEAR = (1.0, 1.0, 1.0, 1.0)
TINT_RED = (1.0, 0.06, 0.03, 1.0)
TINT_AMBER = (1.0, 0.42, 0.02, 1.0)

# ------------------------------------------------------------------------------------------------
# scene
# ------------------------------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.scale_length = 1.0
    s.unit_settings.length_unit = 'METERS'
    return s

def new_coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c

# ------------------------------------------------------------------------------------------------
# 2D / 3D primitive helpers -- all coordinates in uu; geo = (verts, faces)
# ------------------------------------------------------------------------------------------------
def lin(a, b, n):
    return [a + (b - a) * i / n for i in range(n + 1)]

def arc(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def rrect(a0, a1, b0, b1, rt=0.0, rb=0.0, n=6):
    """CCW rounded rectangle in a 2D plane; rt = top corner radius, rb = bottom."""
    p = []
    p += arc(a1 - rb, b0 + rb, rb, -90, 0, n) if rb > 0 else [(a1, b0)]
    p += arc(a1 - rt, b1 - rt, rt, 0, 90, n) if rt > 0 else [(a1, b1)]
    p += arc(a0 + rt, b1 - rt, rt, 90, 180, n) if rt > 0 else [(a0, b1)]
    p += arc(a0 + rb, b0 + rb, rb, 180, 270, n) if rb > 0 else [(a0, b0)]
    return p

def circle3(p1, p2, p3):
    (ax, ay), (bx, by), (cx, cy) = p1, p2, p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy, math.hypot(ax - ux, ay - uy)

def map_plane(a, b, d, plane):
    if plane == 'XZ':
        return (a, d, b)
    if plane == 'YZ':
        return (d, a, b)
    return (a, b, d)

def extrude(prof, plane, d0, d1, caps=True, stations=None):
    n = len(prof)
    ds = stations or [d0, d1]
    verts = [map_plane(a, b, d, plane) for d in ds for (a, b) in prof]
    faces = []
    for s in range(len(ds) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((s * n + i, s * n + j, (s + 1) * n + j, (s + 1) * n + i))
    if caps:
        faces.append(tuple(range(n))[::-1])
        last = (len(ds) - 1) * n
        faces.append(tuple(range(last, last + n)))
    return (verts, faces)

def loft_x(prof, stations):
    """prof: (y,z) section; stations: (x, sy, zc, sz) -> y*sy, zc+(z-zc)*sz."""
    n = len(prof)
    verts = []
    for (x, sy, zc, sz) in stations:
        for (y, z) in prof:
            verts.append((x, y * sy, zc + (z - zc) * sz))
    faces = []
    for s in range(len(stations) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((s * n + i, s * n + j, (s + 1) * n + j, (s + 1) * n + i))
    faces.append(tuple(range(n))[::-1])
    last = (len(stations) - 1) * n
    faces.append(tuple(range(last, last + n)))
    return (verts, faces)

def box(x0, x1, y0, y1, z0, z1):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return (v, f)

def cyl(c, axis, r, h0, h1, segs=24, phase=0.0):
    if segs > 8:
        segs = int(round(segs * CYL['mul']))
    pr = [(r * math.cos(2 * math.pi * i / segs + phase), r * math.sin(2 * math.pi * i / segs + phase))
          for i in range(segs)]
    if axis == 'Z':
        return extrude([(c[0] + a, c[1] + b) for a, b in pr], 'XY', c[2] + h0, c[2] + h1)
    if axis == 'Y':
        return extrude([(c[0] + a, c[2] + b) for a, b in pr], 'XZ', c[1] + h0, c[1] + h1)
    return extrude([(c[1] + a, c[2] + b) for a, b in pr], 'YZ', c[0] + h0, c[0] + h1)

def revolve(prof, axis='Z', c=(0, 0, 0), segs=32, closed=False, phase=0.0):
    """prof: list of (r, h). r == 0 -> pole vertex."""
    def P(r, h, t):
        ct, st = math.cos(t), math.sin(t)
        if axis == 'Z':
            return (c[0] + r * ct, c[1] + r * st, c[2] + h)
        if axis == 'Y':
            return (c[0] + r * ct, c[1] + h, c[2] + r * st)
        return (c[0] + h, c[1] + r * ct, c[2] + r * st)
    verts, faces, rings = [], [], []
    for (r, h) in prof:
        if r < 1e-6:
            rings.append([len(verts)] * segs)
            verts.append(P(0.0, h, 0.0))
        else:
            idx = []
            for k in range(segs):
                idx.append(len(verts))
                verts.append(P(r, h, 2 * math.pi * k / segs + phase))
            rings.append(idx)
    m = len(prof)
    for i in range(m if closed else m - 1):
        A, B = rings[i], rings[(i + 1) % m]
        for k in range(segs):
            k2 = (k + 1) % segs
            q = []
            for v in (A[k], A[k2], B[k2], B[k]):
                if v not in q:
                    q.append(v)
            if len(q) >= 3:
                faces.append(tuple(q))
    return (verts, faces)

def dome(c, axis, r, h, segs=16, rings=4, sign=1.0, base=0.3):
    """Rivet / bolt head: flat base at c, dome bulging along +axis*sign by h."""
    prof = [(0.0, -base * sign)]
    prof.append((r, -base * sign))
    for i in range(rings + 1):
        t = math.radians(90.0 * i / rings)
        prof.append((r * math.cos(t), sign * h * math.sin(t)))
    prof[-1] = (0.0, sign * h)
    return revolve(prof, axis, c, segs)

def xform(geo, M):
    v, f = geo
    return ([tuple(M @ Vector(p)) for p in v], f)

def rot_about(geo, pivot, axis, deg):
    M = Matrix.Translation(Vector(pivot)) @ Matrix.Rotation(math.radians(deg), 4, axis) @ \
        Matrix.Translation(-Vector(pivot))
    return xform(geo, M)

def mirror_y(geo):
    v, f = geo
    return ([(x, -y, z) for (x, y, z) in v], [tuple(reversed(face)) for face in f])

def merge(*geos):
    V, F = [], []
    for v, f in geos:
        b = len(V)
        V.extend(v)
        F.extend([tuple(i + b for i in face) for face in f])
    return (V, F)

def polyline_offset(cl, half):
    """Closed outline around a 2D centre-line (list of (x,z)) with half thickness."""
    up, dn = [], []
    n = len(cl)
    for i in range(n):
        a = cl[max(i - 1, 0)]
        b = cl[min(i + 1, n - 1)]
        tx, tz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, tz)
        tx, tz = tx / L, tz / L
        nx, nz = -tz, tx
        up.append((cl[i][0] + nx * half, cl[i][1] + nz * half))
        dn.append((cl[i][0] - nx * half, cl[i][1] - nz * half))
    return up + dn[::-1]

# ------------------------------------------------------------------------------------------------
# objects / modifiers
# ------------------------------------------------------------------------------------------------
SRC = None
EXP = None
PREV = None
PIECES = {}
MATS = {}

def make_obj(name, geo, coll, recalc=True):
    v, f = geo
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x * U, y * U, z * U) for (x, y, z) in v], [], f)
    me.validate(clean_customdata=False)
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob

def add_bevel(ob, w, segs=3, angle=30.0):
    m = ob.modifiers.new('Bevel', 'BEVEL')
    m.width = w * U
    m.segments = segs
    m.limit_method = 'ANGLE'
    m.angle_limit = math.radians(angle)
    m.profile = 0.5
    m.use_clamp_overlap = True
    try:
        m.miter_outer = 'MITER_ARC'
    except Exception:
        pass
    return m

def add_bool(ob, cutter):
    m = ob.modifiers.new('Cut', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    try:
        m.solver = 'EXACT'
        m.use_self = True          # cutter boxes overlap at panel-line corners
    except Exception:
        pass
    m.object = cutter
    return m

def cutter_obj(name, geo):
    ob = make_obj('CUT_' + name, geo, SRC)
    ob.display_type = 'WIRE'
    ob.hide_render = True
    return ob

def piece(part, name, geo, mat, bevel=0.0, segs=3, angle=30.0, tint=None, cutter=None, solidify=None, recalc=True):
    ob = make_obj('%s_%s' % (part, name), geo, SRC, recalc=recalc)
    if solidify:
        m = ob.modifiers.new('Solidify', 'SOLIDIFY')
        m.thickness = solidify * U
        m.offset = -1.0
        m.use_even_offset = True
    if bevel > 0:
        add_bevel(ob, bevel, segs + BEVEL_ADD.get(part, 0), angle)
    if cutter is not None:
        add_bool(ob, cutter)
    PIECES.setdefault(part, []).append(dict(obj=ob, mat=mat, tint=tint or TINT_CLEAR))
    return ob

def both(part, name, geo, mat, **kw):
    """Left piece as authored (+Y) and its mirror (-Y)."""
    piece(part, name + '_L', geo, mat, **kw)
    piece(part, name + '_R', mirror_y(geo), mat, **kw)

# ------------------------------------------------------------------------------------------------
# preview materials (stand-ins named by the spec slot names)
# ------------------------------------------------------------------------------------------------
def principled(name, base, metallic=0.0, rough=0.5, coat=0.0, coat_rough=0.03, trans=0.0, ior=1.5,
               vcol=False, spec=0.5, peel=0.0):
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
        # enamel orange-peel on the clearcoat only (preview stand-in; UE master does the real thing)
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

def build_materials():
    # industrial-yellow enamel over zinc: light metallic flake under a hard gloss clearcoat
    MATS['Paint'] = principled('Paint', (1.0, 0.60, 0.008), metallic=0.12, rough=0.22, coat=1.0, coat_rough=0.012,
                               peel=0.08)
    MATS['Chrome'] = principled('Chrome', (0.95, 0.95, 0.96), metallic=1.0, rough=0.035)
    MATS['Lamp'] = principled('Lamp', (1.0, 1.0, 1.0), rough=0.03, trans=0.9, ior=1.5, vcol=True)
    MATS['Zamac'] = principled('Zamac', (0.66, 0.65, 0.63), metallic=1.0, rough=0.2)      # steel axles, rivets
    MATS['Base'] = principled('Base', (0.50, 0.49, 0.47), metallic=1.0, rough=0.42)       # bare satin zamac base
    MATS['Glass'] = principled('Glass', (0.62, 0.70, 0.66), rough=0.02, trans=1.0, ior=1.45)
    MATS['Interior'] = principled('Interior', (0.045, 0.045, 0.05), rough=0.55)
    MATS['Tire'] = principled('Tire', (0.02, 0.02, 0.022), rough=0.62, spec=0.4)
    MATS['Hub'] = principled('Hub', (1.0, 0.52, 0.0), rough=0.24, coat=0.6, coat_rough=0.05)   # yellow plastic

# ------------------------------------------------------------------------------------------------
# WHEEL W03_Lug  (wheel-local: origin at centre, axle along Y, hub face toward +Y = left side)
# ------------------------------------------------------------------------------------------------
LUG_N = 15            # per row, odd -> pattern is identical after a 180 deg yaw (right-side wheels)

def build_wheel():
    P = 'Wheel'
    # tyre carcass (closed revolve, r,y)
    carcass = [(8.6, 5.7), (9.6, 6.55), (10.8, 6.95), (11.8, 6.8), (12.35, 6.2), (12.6, 5.0),
               (12.65, 2.4), (12.65, 0.0), (12.65, -2.4), (12.6, -5.0), (12.35, -6.2), (11.8, -6.8),
               (10.8, -6.95), (9.6, -6.55), (8.6, -5.7), (8.4, 0.0)]
    piece(P, 'Carcass', revolve(carcass, 'Y', (0, 0, 0), 48, closed=True), 'Tire')
    # lugs: (y, r) side profile of one block, wrapped over the shoulder
    lugp = [(-1.7, 12.2), (5.6, 12.2), (6.9, 11.2), (7.2, 12.9), (6.7, 14.0), (-1.3, 14.0)]
    w_top, w_bot = math.radians(5.4), math.radians(6.6)
    lugs = []
    for row in (1, -1):
        for k in range(LUG_N):
            th = math.radians(360.0 / LUG_N * k + (0.0 if row > 0 else 180.0 / LUG_N))
            verts = []
            for side in (-1, 1):
                for (y, r) in lugp:
                    w = w_top + (w_bot - w_top) * (14.0 - r) / 3.0
                    t = th + side * w
                    verts.append((r * math.cos(t), y * row, r * math.sin(t)))
            n = len(lugp)
            faces = [tuple(range(n)), tuple(range(n, 2 * n))[::-1]]
            for i in range(n):
                j = (i + 1) % n
                faces.append((i, n + i, n + j, j))
            lugs.append((verts, faces))
    piece(P, 'Lugs', merge(*lugs), 'Tire', bevel=0.28, segs=1, angle=30)
    # hub (closed revolve, through-hole for the axle)
    hub = [(1.25, -4.9), (1.25, 5.5), (1.55, 5.95), (2.45, 5.95), (3.0, 5.55), (3.35, 4.75), (4.1, 4.45),
           (6.2, 4.3), (6.85, 4.55), (7.2, 5.35), (7.5, 6.3), (7.95, 6.62), (8.5, 6.55), (8.95, 6.05),
           (8.95, -6.05), (8.45, -6.5), (7.6, -6.5), (7.2, -5.6), (6.8, -4.6), (2.6, -4.6), (2.0, -5.15),
           (1.55, -5.2)]
    piece(P, 'Hub', revolve(hub, 'Y', (0, 0, 0), 40, closed=True), 'Hub')
    nuts = []
    for k in range(6):
        a = math.radians(60 * k + 30)
        cx, cz = 5.25 * math.cos(a), 5.25 * math.sin(a)
        nuts.append(cyl((cx, 0, cz), 'Y', 0.78, 4.2, 5.15, segs=6, phase=a))
    piece(P, 'Nuts', merge(*nuts), 'Hub', bevel=0.14, segs=1, angle=30)

# ------------------------------------------------------------------------------------------------
# BODY  (slots Paint, Chrome, Lamp, Zamac)
# ------------------------------------------------------------------------------------------------
def build_body():
    P = 'Body'
    CYL['mul'] = 1.75
    # ---- engine hood (rear frame) -------------------------------------------------------------
    hood_prof = rrect(-21.0, 21.0, 12.5, 33.5, rt=4.0, rb=0.0, n=6)
    cuts = []
    for zc in (19.3, 21.5, 23.7, 25.9, 28.1):                          # side louvres
        cuts.append(box(-47.0, -35.0, 20.4, 22.5, zc - 0.45, zc + 0.45))
        cuts.append(box(-47.0, -35.0, -22.5, -20.4, zc - 0.45, zc + 0.45))
    for sy in (1, -1):                                                 # side access doors
        y0, y1 = (20.6, 22.5) if sy > 0 else (-22.5, -20.6)
        cuts += [box(-32.0, -18.0, y0, y1, 28.0, 28.5), box(-32.0, -18.0, y0, y1, 15.5, 16.0),
                 box(-32.0, -31.5, y0, y1, 15.5, 28.5), box(-18.5, -18.0, y0, y1, 15.5, 28.5)]
    cuts += [box(-49.0, -31.0, 12.5, 13.0, 33.1, 35.0), box(-49.0, -31.0, -13.0, -12.5, 33.1, 35.0),
             box(-49.0, -48.5, -13.0, 13.0, 33.1, 35.0), box(-31.5, -31.0, -13.0, 13.0, 33.1, 35.0)]
    for zc in (27.9, 29.6, 31.3):                                      # rear radiator grille
        cuts.append(box(-56.5, -54.4, -14.0, 14.0, zc - 0.4, zc + 0.4))
    hood_cut = cutter_obj('Hood', merge(*cuts))
    piece(P, 'Hood', loft_x(hood_prof, [(-55.0, 1, 12.5, 1), (-15.0, 1, 12.5, 1)]), 'Paint',
          bevel=1.2, segs=3, cutter=hood_cut)

    # ---- counterweight, rear plate, tail lamps, hitch --------------------------------------
    piece(P, 'Counterweight', box(-59.5, -49.0, -25.0, 25.0, 10.0, 26.5), 'Paint', bevel=2.4, segs=4)
    piece(P, 'RearPlate', box(-60.0, -59.0, -9.0, 9.0, 14.0, 19.0), 'Paint', bevel=0.4, segs=2)
    both(P, 'TailLamp', box(-60.15, -59.0, 17.5, 22.0, 20.0, 23.2), 'Lamp', bevel=0.4, segs=2, tint=TINT_RED)
    piece(P, 'Hitch', box(-62.8, -58.5, -3.0, 3.0, 12.0, 15.2), 'Zamac', bevel=0.8, segs=3)
    piece(P, 'HitchPin', cyl((-61.2, 0, 0), 'Z', 1.0, 11.2, 16.4, segs=16), 'Zamac', bevel=0.25, segs=2)

    # ---- rear fenders ---------------------------------------------------------------------
    fender = [(-15.8, 18.5), (-22.5, 32.5), (-43.5, 32.5), (-50.2, 18.5)]
    fender += arc(-AXLE_X, AXLE_Z, 16.3, 158.0, 22.0, 16)
    both(P, 'Fender', extrude(fender, 'XZ', 19.5, 43.5), 'Paint', bevel=1.6, segs=3)

    # ---- cab deck, steps, hinge towers ----------------------------------------------------
    piece(P, 'Deck', box(-16.0, 12.0, -27.5, 27.5, 21.0, 25.5), 'Paint', bevel=1.0, segs=3)
    step = merge(box(-13.6, -12.4, 27.0, 28.6, 13.0, 21.5), box(-8.6, -7.4, 27.0, 28.6, 13.0, 21.5),
                 box(-13.0, -8.0, 27.3, 28.6, 15.0, 15.9), box(-13.0, -8.0, 27.3, 28.6, 18.2, 19.1))
    both(P, 'Step', step, 'Paint', bevel=0.35, segs=2)
    tower = [(-9.5, 21.0), (1.5, 21.0)] + arc(HINGE[0], HINGE[2], 5.5, 0.0, 180.0, 14)
    both(P, 'HingeTower', extrude(tower, 'XZ', 24.0, 33.0), 'Paint', bevel=1.0, segs=3)

    # ---- cab roll cage + roof -------------------------------------------------------------
    for (cx, cy) in ((-13.0, 18.0), (-13.0, -18.0), (8.5, 18.0), (8.5, -18.0)):
        piece(P, 'Post', box(cx - 2.0, cx + 2.0, cy - 2.0, cy + 2.0, 25.0, 41.5), 'Paint', bevel=1.0, segs=3)
    piece(P, 'Roof', box(-15.6, 11.1, -20.6, 20.6, 41.0, 44.0), 'Paint', bevel=1.3, segs=4)
    piece(P, 'RoofPanel', box(-12.5, 8.0, -16.5, 16.5, 43.5, 44.6), 'Paint', bevel=0.5, segs=2)
    # work lamps (front pair forward, rear pair backward)
    for sx, x0, x1, lx, dirn in ((1, 7.6, 10.6, 10.6, 1), (-1, -15.2, -12.2, -15.2, -1)):
        hous = box(x0, x1, 13.0, 17.6, 44.0, 47.2)
        both(P, 'WorkLampHousing%+d' % sx, hous, 'Chrome', bevel=0.7, segs=2)
        lens = cyl((lx, 15.3, 45.6), 'X', 1.35, -0.25 if dirn > 0 else -0.55, 0.55 if dirn > 0 else 0.25, segs=20)
        both(P, 'WorkLampLens%+d' % sx, lens, 'Lamp', bevel=0.2, segs=2)
    # beacon
    piece(P, 'BeaconBase', cyl((-9.0, 0, 0), 'Z', 2.7, 44.0, 45.5, segs=24), 'Chrome', bevel=0.45, segs=2)
    beacon = [(0.0, 45.2), (2.2, 45.2), (2.2, 46.9)] + \
             [(2.2 * math.cos(math.radians(a)), 46.9 + 1.9 * math.sin(math.radians(a))) for a in (20, 40, 58, 74)] + \
             [(0.0, 48.8)]
    piece(P, 'Beacon', revolve(beacon, 'Z', (-9.0, 0, 0), 32), 'Lamp', tint=TINT_AMBER)

    # ---- nose (front frame) ---------------------------------------------------------------
    nose_prof = rrect(-19.5, 19.5, 12.5, 28.5, rt=3.5, rb=0.0, n=6)
    ncuts = []
    for sy in (1, -1):
        y0, y1 = (19.1, 21.0) if sy > 0 else (-21.0, -19.1)
        ncuts += [box(22.0, 44.0, y0, y1, 24.0, 24.5), box(22.0, 44.0, y0, y1, 15.5, 16.0),
                  box(22.0, 22.5, y0, y1, 15.5, 24.5), box(43.5, 44.0, y0, y1, 15.5, 24.5)]
    for yc in (-9, -6, -3, 0, 3, 6, 9):
        ncuts.append(box(56.6, 59.0, yc - 0.4, yc + 0.4, 15.0, 21.0))
    # top access hatch (engraved ~0.45 deep) + a short bank of vent louvres ahead of it
    ncuts += [box(16.0, 33.0, 11.75, 12.25, 28.05, 29.5), box(16.0, 33.0, -12.25, -11.75, 28.05, 29.5),
              box(16.0, 16.5, -12.25, 12.25, 28.05, 29.5), box(32.5, 33.0, -12.25, 12.25, 28.05, 29.5)]
    for xc in (35.6, 37.2, 38.8, 40.4):
        ncuts.append(box(xc - 0.35, xc + 0.35, -8.0, 8.0, 28.05, 29.5))
    ring_o = rrect(-20.8, 20.8, 11.0, 29.8, rt=4.8, rb=0.0, n=6)
    ring_i = rrect(-19.1, 19.1, 11.0, 28.1, rt=3.1, rb=0.0, n=6)
    # U-shaped ring (articulation joint seam), open at the bottom
    u_ring = ring_o + ring_i[::-1]
    ncuts.append(extrude(u_ring, 'YZ', 12.9, 13.5))
    nose_cut = cutter_obj('Nose', merge(*ncuts))
    piece(P, 'Nose', loft_x(nose_prof, [(10.0, 1, 12.5, 1), (47.0, 1, 12.5, 1), (57.5, 0.98, 12.5, 0.6875)]),
          'Paint', bevel=1.2, segs=3, cutter=nose_cut)
    both(P, 'HeadLampHousing', box(42.5, 47.5, 12.0, 17.0, 28.2, 31.6), 'Chrome', bevel=0.7, segs=2)
    both(P, 'HeadLampLens', cyl((47.5, 14.5, 29.9), 'X', 1.4, -0.3, 0.6, segs=20), 'Lamp', bevel=0.2, segs=2)

    # ---- exhaust stack + air pre-cleaner -------------------------------------------------
    ex = (-26.0, -11.0)
    piece(P, 'ExFlange', cyl((ex[0], ex[1], 0), 'Z', 3.4, 32.8, 34.6, segs=28), 'Chrome', bevel=0.6, segs=2)
    piece(P, 'ExMuffler', cyl((ex[0], ex[1], 0), 'Z', 2.9, 34.2, 41.0, segs=28), 'Chrome', bevel=0.9, segs=3)
    piece(P, 'ExPipe', cyl((ex[0], ex[1], 0), 'Z', 1.95, 40.6, 48.2, segs=24), 'Chrome', bevel=0.45, segs=2)
    flap = cyl((ex[0], ex[1], 48.5), 'Z', 2.25, -0.35, 0.35, segs=24)
    piece(P, 'ExFlap', rot_about(flap, (ex[0] - 2.1, ex[1], 48.5), 'Y', -20.0), 'Chrome', bevel=0.25, segs=2)
    pc = (-26.0, 11.0)
    piece(P, 'PreCleanerBowl', cyl((pc[0], pc[1], 0), 'Z', 3.0, 33.0, 37.6, segs=28), 'Paint', bevel=0.6, segs=2)
    piece(P, 'PreCleanerCap', cyl((pc[0], pc[1], 0), 'Z', 3.5, 37.3, 39.0, segs=28), 'Chrome', bevel=0.7, segs=3)
    piece(P, 'PreCleanerKnob', cyl((pc[0], pc[1], 0), 'Z', 1.0, 38.8, 39.9, segs=12), 'Chrome', bevel=0.3, segs=2)

    # ---- steel axles + rivet heads (bare metal) ----------------------------------------
    for ax in (AXLE_X, -AXLE_X):
        piece(P, 'Axle', cyl((ax, 0, AXLE_Z), 'Y', 1.0, -41.8, 41.8, segs=16), 'Zamac', bevel=0.2, segs=2)
    for rx in (44.0, -44.0):
        piece(P, 'Rivet', dome((rx, 0.0, 8.6), 'Z', 2.3, 1.25, segs=20, rings=4, sign=-1.0, base=0.6), 'Zamac')

# ------------------------------------------------------------------------------------------------
# BASE (slot Base)
# ------------------------------------------------------------------------------------------------
def build_base():
    P = 'Base'
    outline = [(-56.0, -21.0), (-18.0, -21.0), (-15.0, -25.5), (12.0, -25.5), (15.0, -18.5), (55.0, -18.5),
               (55.0, 18.5), (15.0, 18.5), (12.0, 25.5), (-15.0, 25.5), (-18.0, 21.0), (-56.0, 21.0)]
    piece(P, 'Plate', extrude(outline, 'XY', 9.0, 12.5), 'Base', bevel=0.9, segs=3)
    for ax in (AXLE_X, -AXLE_X):
        piece(P, 'AxleBeam', box(ax - 4.0, ax + 4.0, -27.0, 27.0, 9.8, 17.8), 'Base', bevel=1.2, segs=3)
        sph = bmesh.new()
        bmesh.ops.create_uvsphere(sph, u_segments=24, v_segments=12, radius=1.0)
        v = [(ax + p.co.x * 5.0, p.co.y * 6.5, 11.0 + p.co.z * 4.6) for p in sph.verts]
        f = [tuple(vv.index for vv in fc.verts) for fc in sph.faces]
        sph.free()
        piece(P, 'Diff', (v, f), 'Base')
    # moulded text area border (area inside left plain for a decal)
    tb = [box(-25.0, 23.0, 13.7, 14.5, 8.4, 9.1), box(-25.0, 23.0, -14.5, -13.7, 8.4, 9.1),
          box(-25.0, -24.2, -14.5, 14.5, 8.4, 9.1), box(22.2, 23.0, -14.5, 14.5, 8.4, 9.1)]
    piece(P, 'TextBorder', merge(*tb), 'Base', bevel=0.25, segs=1)
    ribs = [box(39.0, 54.0, 10.5, 11.5, 8.3, 9.1), box(39.0, 54.0, -11.5, -10.5, 8.3, 9.1),
            box(-55.0, -39.0, 13.5, 14.5, 8.3, 9.1), box(-55.0, -39.0, -14.5, -13.5, 8.3, 9.1)]
    piece(P, 'Ribs', merge(*ribs), 'Base', bevel=0.3, segs=2)
    for rx in (44.0, -44.0):
        piece(P, 'RivetBoss', cyl((rx, 0, 0), 'Z', 3.3, 8.6, 9.3, segs=24), 'Base', bevel=0.25, segs=2)
    piece(P, 'PivotBoss', cyl((13.0, 0, 0), 'Z', 3.4, 8.2, 9.3, segs=24), 'Base', bevel=0.3, segs=2)
    piece(P, 'FuelTank', box(-12.0, 9.0, 21.0, 26.0, 12.0, 20.5), 'Base', bevel=1.2, segs=3)
    piece(P, 'BatteryBox', box(-12.0, 4.0, -26.0, -21.0, 12.0, 20.0), 'Base', bevel=1.0, segs=3)

# ------------------------------------------------------------------------------------------------
# WINDOWS (slot Glass) -- one-piece tinted glasshouse
# ------------------------------------------------------------------------------------------------
def build_windows():
    P = 'Windows'
    outline = rrect(-13.5, 9.4, -18.6, 18.6, rt=1.6, rb=1.6, n=8)  # (x, y) plane
    st = lin(25.6, 41.2, 7)
    v, f = extrude(outline, 'XY', 0, 0, caps=False, stations=st)
    piece(P, 'Glass', (v, f), 'Glass', solidify=0.6, recalc=False)

# ------------------------------------------------------------------------------------------------
# INTERIOR (slot Interior) -- one colour
# ------------------------------------------------------------------------------------------------
def build_interior():
    P = 'Interior'
    piece(P, 'Floor', box(-12.8, 8.7, -17.9, 17.9, 25.3, 26.2), 'Interior', bevel=0.3, segs=2)
    piece(P, 'Cushion', box(-9.5, -3.5, -5.2, 5.2, 26.2, 29.0), 'Interior', bevel=0.9, segs=3)
    back = rot_about(box(-11.6, -9.4, -5.2, 5.2, 28.0, 36.0), (-10.5, 0, 28.0), 'Y', -12.0)
    piece(P, 'SeatBack', back, 'Interior', bevel=0.9, segs=3)
    both(P, 'Armrest', box(-9.5, -4.0, 5.2, 6.4, 29.0, 30.4), 'Interior', bevel=0.4, segs=2)
    piece(P, 'Console', box(4.0, 8.0, -12.5, 12.5, 26.2, 31.0), 'Interior', bevel=0.6, segs=2)
    col = rot_about(cyl((0, 0, 0), 'Z', 0.45, 0.0, 5.0, segs=12), (0, 0, 0), 'Y', -36.87)
    col = xform(col, Matrix.Translation((5.0, 0.0, 30.0)))
    piece(P, 'Column', col, 'Interior')
    # steering wheel ring (torus) tilted with the column
    ring = [(2.8 + 0.45 * math.cos(2 * math.pi * i / 10), 0.45 * math.sin(2 * math.pi * i / 10)) for i in range(10)]
    tor = revolve(ring, 'Z', (0, 0, 0), 28, closed=True)
    spokes = merge(box(-2.8, 2.8, -0.3, 0.3, -0.25, 0.25), box(-0.3, 0.3, -2.8, 2.8, -0.25, 0.25))
    wheel = merge(tor, spokes)
    wheel = rot_about(wheel, (0, 0, 0), 'Y', -36.87)
    wheel = xform(wheel, Matrix.Translation((2.0, 0.0, 34.0)))
    piece(P, 'Steering', wheel, 'Interior')
    for sy in (1, -1):
        piece(P, 'Lever', cyl((-1.5, 8.5 * sy, 0), 'Z', 0.35, 26.2, 31.5, segs=10), 'Interior')
        sp = bmesh.new()
        bmesh.ops.create_uvsphere(sp, u_segments=12, v_segments=6, radius=0.8)
        v = [(-1.5 + p.co.x, 8.5 * sy + p.co.y, 31.6 + p.co.z) for p in sp.verts]
        f = [tuple(vv.index for vv in fc.verts) for fc in sp.faces]
        sp.free()
        piece(P, 'Knob', (v, f), 'Interior')

# ------------------------------------------------------------------------------------------------
# BLADE (slots Paint, Zamac) -- pivots at HINGE about Y
# ------------------------------------------------------------------------------------------------
def build_blade():
    P = 'Blade'
    # moldboard: concave front through 3 points
    A, B, C = (77.0, 2.0), (71.0, 13.0), (76.0, 24.0)
    cx, cz, r = circle3(A, B, C)
    a0 = math.degrees(math.atan2(A[1] - cz, A[0] - cx)) % 360
    a1 = math.degrees(math.atan2(C[1] - cz, C[0] - cx)) % 360
    front = arc(cx, cz, r, a0, a1, 18)      # A -> C, decreasing angle through 180
    prof = [(68.0, 2.0)] + front + [(74.6, 25.3), (66.2, 23.6), (64.5, 21.5), (64.5, 5.0), (66.0, 2.6)]
    piece(P, 'Moldboard', extrude(prof, 'XZ', -41.8, 41.8), 'Paint', bevel=1.0, segs=3)
    endp = [(64.5, 2.2), (78.4, 1.8), (77.9, 13.0), (77.6, 25.2), (66.0, 24.6), (64.5, 22.0)]
    both(P, 'EndPlate', extrude(endp, 'XZ', 41.8, 43.0), 'Paint', bevel=0.6, segs=2)
    # cutting edge strip (bare metal) along the lower front
    pts = [p for p in arc(cx, cz, r, a0, a0 - 26.0, 6)]
    inner, outer = [], []
    for (px, pz) in pts:
        nx, nz = (cx - px) / r, (cz - pz) / r
        inner.append((px - nx * 0.3, pz - nz * 0.3))
        outer.append((px + nx * 0.75, pz + nz * 0.75))
    strip = [(inner[0][0], 1.55), (outer[0][0] + 0.2, 1.55)] + outer + inner[::-1]
    piece(P, 'CuttingEdge', extrude(strip, 'XZ', -41.7, 41.7), 'Zamac', bevel=0.3, segs=2)
    # bolt heads on the cutting edge
    pb = arc(cx, cz, r, a0 - 13.0, a0 - 13.0, 1)[0]
    nx, nz = (cx - pb[0]) / r, (cz - pb[1]) / r
    tilt = math.degrees(math.atan2(nz, nx))
    bolts = []
    for yb in (-36, -27, -18, -9, 0, 9, 18, 27, 36):
        d = dome((0, 0, 0), 'X', 0.8, 0.55, segs=10, rings=3, sign=1.0, base=0.3)
        d = rot_about(d, (0, 0, 0), 'Y', -tilt)
        d = xform(d, Matrix.Translation((pb[0] + nx * 0.75, yb, pb[1] + nz * 0.75)))
        bolts.append(d)
    piece(P, 'Bolts', merge(*bolts), 'Zamac')
    # back beams + arm brackets
    piece(P, 'BeamLow', box(61.8, 65.2, -41.5, 41.5, 6.5, 10.0), 'Paint', bevel=0.8, segs=2)
    piece(P, 'BeamHigh', box(62.2, 65.2, -41.5, 41.5, 15.5, 19.0), 'Paint', bevel=0.8, segs=2)
    both(P, 'Bracket', box(59.5, 65.0, 32.8, 41.0, 6.0, 20.0), 'Paint', bevel=1.0, segs=3)
    # arms (gooseneck): straight over the front tyre, bend down to the blade
    cl = [(x, HINGE[2]) for x in lin(HINGE[0], 40.0, 8)]
    for a in lin(90.0, 40.0, 10)[1:]:
        cl.append((40.0 + 12.0 * math.cos(math.radians(a)), 20.0 + 12.0 * math.sin(math.radians(a))))
    ex, ez = cl[-1]
    dx, dz = math.sin(math.radians(40.0)), -math.cos(math.radians(40.0))
    L = (ez - 13.0) / -dz
    for s in lin(0.0, L, 4)[1:]:
        cl.append((ex + dx * s, ez + dz * s))
    arm = polyline_offset(cl, 2.5)
    both(P, 'Arm', extrude(arm, 'XZ', 33.3, 40.5), 'Paint', bevel=1.0, segs=3)
    both(P, 'HingeBoss', cyl((HINGE[0], 0, HINGE[2]), 'Y', 4.5, 33.3, 40.5, segs=32), 'Paint', bevel=1.0, segs=3)
    both(P, 'HingePin', cyl((HINGE[0], 0, HINGE[2]), 'Y', 2.0, 40.0, 41.3, segs=20), 'Zamac', bevel=0.45, segs=2)

# ------------------------------------------------------------------------------------------------
# merge pieces into a part object
# ------------------------------------------------------------------------------------------------
def merge_part(part, origin=(0.0, 0.0, 0.0)):
    name = PART_NAMES[part]
    slots = SLOTS[part]
    dg = bpy.context.evaluated_depsgraph_get()
    o = Vector(origin) * U
    V, F, FM, FT = [], [], [], []
    for p in PIECES[part]:
        ob = p['obj']
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ob.matrix_world.copy()
        b = len(V)
        V.extend([tuple((mw @ v.co) - o) for v in me.vertices])
        mi = slots.index(p['mat'])
        if len(me.polygons) < 4 or OPT.get('verbose'):
            print('  piece %-28s polys=%d (base %d)' % (ob.name, len(me.polygons), len(ob.data.polygons)))
        for poly in me.polygons:
            F.append(tuple(b + i for i in poly.vertices))
            FM.append(mi)
            FT.append(p['tint'])
        ev.to_mesh_clear()
    me = bpy.data.meshes.new(name)
    me.from_pydata(V, [], F)
    for s in slots:
        me.materials.append(MATS[s])
    me.polygons.foreach_set('material_index', FM)
    ca = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
    cols = []
    for poly in me.polygons:
        t = FT[poly.index]
        for _ in range(poly.loop_total):
            cols.extend(t)
    ca.data.foreach_set('color', cols)
    me.validate(clean_customdata=False)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-6, edges=bm.edges[:])
    bad = [f for f in bm.faces if f.calc_area() < 1e-10]
    if bad:
        bmesh.ops.delete(bm, geom=bad, context='FACES_ONLY')
    loose = [v for v in bm.verts if not v.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bm.to_mesh(me)
    bm.free()
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(40.0))
    ob = bpy.data.objects.new(name, me)
    EXP.objects.link(ob)
    ob.location = o
    tri = ob.modifiers.new('Triangulate', 'TRIANGULATE')
    tri.min_vertices = 5
    tri.quad_method = 'BEAUTY'
    tri.ngon_method = 'BEAUTY'
    try:
        tri.keep_custom_normals = True
    except Exception:
        pass
    wn = ob.modifiers.new('WeightedNormal', 'WEIGHTED_NORMAL')
    wn.mode = 'FACE_AREA'
    wn.weight = 50
    wn.keep_sharp = True
    return ob

# ------------------------------------------------------------------------------------------------
# UVs
# ------------------------------------------------------------------------------------------------
TAMPO_BOX = (-64.0, 64.0, -44.0, 44.0, 0.0, 50.0)   # uu, Blender axes (xmin,xmax,ymin,ymax,zmin,zmax)

def select_only(ob):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob

def uv_unwrap(ob):
    me = ob.data
    uv0 = me.uv_layers.new(name='UV0')
    me.uv_layers.new(name='UV1_Tampo')
    me.uv_layers.active_index = 0
    select_only(ob)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.002, area_weight=0.0,
                             correct_aspect=True, scale_to_bounds=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    me.uv_layers.active_index = 0
    try:
        me.uv_layers['UV0'].active_render = True
    except Exception:
        pass

def uv1_side_projection(ob, box_uu, offset=(0, 0, 0)):
    """UV1 tampo: left side U 0-0.5 (front at U=0, as seen from the left), right side U 0.5-1
    (rear at 0.5, front at 1, as seen from the right), both V 0-0.64 by height; top strip
    V 0.68-1 (U by length rear->front, V by width right->left as seen from above);
    front/rear/bottom faces go into the blank band V 0.64-0.68."""
    me = ob.data
    uv = me.uv_layers['UV1_Tampo'].data
    xr, xf, yr, yl, zb, zt = [c * U for c in box_uu]
    ox, oy, oz = [c * U for c in offset]
    L, W, H = xf - xr, yl - yr, zt - zb
    co = [v.co for v in me.vertices]
    for poly in me.polygons:
        n = poly.normal
        ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
        for li in poly.loop_indices:
            c = co[me.loops[li].vertex_index]
            x, y, z = c.x + ox, c.y + oy, c.z + oz
            if n.z > 0 and az >= ay and az >= ax:
                u, v = (x - xr) / L, 0.68 + 0.32 * (y - yr) / W
            elif ay >= ax and ay >= az:
                v = 0.64 * (z - zb) / H
                u = 0.5 * (xf - x) / L if n.y > 0 else 0.5 + 0.5 * (x - xr) / L
            else:
                v = 0.64 + 0.04 * min(max((z - zb) / H, 0.0), 1.0)
                u = 0.5 * (y - yr) / W if n.x >= 0 else 0.5 + 0.5 * (yl - y) / W
            uv[li].uv = (u, v)

def uv1_blade(ob):
    """Blade UV1 (wave 4 rewrite: every polygon gets ONE projection, chosen from its own normal, and the three projections
    own separate bands, so nothing overlaps and no polygon mixes projections - the old per-vertex test smeared the curved
    moldboard and printed arm text onto the arms' upper surfaces, mirrored):
      front-facing polygons  (n.x > 0.3, |n.y| < 0.6): U across the width seen from the front, V 0-0.6 by height
      side polygons          (|n.y| >= 0.6): left U 0-0.5 (front at U 0, seen from the left), right U 0.5-1 (front at U 1),
                             V 0.62-0.82 by height
      everything else (tops, undersides, rear): top projection, V 0.84-1.0
    Tools/Assembly/make_tampos.py paints the Navvy prints in 3D through this layout (Tools/Assembly/uv1_posmap.py)."""
    me = ob.data
    uv = me.uv_layers['UV1_Tampo'].data
    co = [v.co for v in me.vertices]
    xs = [c.x for c in co]; ys = [c.y for c in co]; zs = [c.z for c in co]
    x0, x1, y0, y1, z0, z1 = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
    for poly in me.polygons:
        n = poly.normal
        if n.x > 0.3 and abs(n.y) < 0.6:
            kind = 'front'
        elif abs(n.y) >= 0.6:
            kind = 'side'
        else:
            kind = 'top'
        for li in poly.loop_indices:
            c = co[me.loops[li].vertex_index]
            if kind == 'front':
                u, v = (c.y - y0) / (y1 - y0), 0.6 * (c.z - z0) / (z1 - z0)
            elif kind == 'side':
                u = 0.5 * (x1 - c.x) / (x1 - x0) if n.y > 0 else 0.5 + 0.5 * (c.x - x0) / (x1 - x0)
                v = 0.62 + 0.20 * (c.z - z0) / (z1 - z0)
            else:
                u, v = (c.x - x0) / (x1 - x0), 0.84 + 0.16 * (c.y - y0) / (y1 - y0)
            uv[li].uv = (u, v)

def uv1_bottom(ob):
    """Base UV1: projection from below, readable from below with the front to the right
    (U = rear->front, V = left->right)."""
    me = ob.data
    uv = me.uv_layers['UV1_Tampo'].data
    co = [v.co for v in me.vertices]
    xs = [c.x for c in co]; ys = [c.y for c in co]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for poly in me.polygons:
        for li in poly.loop_indices:
            c = co[me.loops[li].vertex_index]
            uv[li].uv = ((c.x - x0) / (x1 - x0), (y1 - c.y) / (y1 - y0))

def uv1_wheel(ob):
    me = ob.data
    uv = me.uv_layers['UV1_Tampo'].data
    co = [v.co for v in me.vertices]
    R = WHEEL_R * U
    for poly in me.polygons:
        for li in poly.loop_indices:
            c = co[me.loops[li].vertex_index]
            uv[li].uv = (0.5 + c.x / (2 * R), 0.5 + c.z / (2 * R))

def uv1_copy(ob):
    me = ob.data
    a = me.uv_layers['UV0'].data
    b = me.uv_layers['UV1_Tampo'].data
    for i in range(len(a)):
        b[i].uv = a[i].uv

# ------------------------------------------------------------------------------------------------
# stats / export / sidecars
# ------------------------------------------------------------------------------------------------
def eval_stats(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    mw = Matrix.Translation(ob.location)
    pts = [mw @ v.co for v in me.vertices]
    bb = [min(p.x for p in pts), max(p.x for p in pts), min(p.y for p in pts), max(p.y for p in pts),
          min(p.z for p in pts), max(p.z for p in pts)]
    ev.to_mesh_clear()
    return tris, [round(c / U, 2) for c in bb]

def export_fbx(ob, path, at_origin=True):
    bpy.context.view_layer.update()
    select_only(ob)
    bpy.context.view_layer.update()
    sel = [o.name for o in bpy.context.view_layer.objects if o.select_get()]
    if sel != [ob.name]:
        raise RuntimeError('export selection is %s, expected only %s' % (sel, ob.name))
    old = ob.location.copy()
    if at_origin:
        ob.location = (0.0, 0.0, 0.0)
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True,
                             apply_scale_options='FBX_SCALE_UNITS', axis_forward='X', axis_up='Z',
                             bake_space_transform=True, mesh_smooth_type='FACE', use_tspace=True,
                             add_leaf_bones=False, object_types={'MESH'}, use_mesh_modifiers=True)
    ob.location = old

def ue(v):  # Blender-axis uu -> UE-axis uu
    return [round(v[0], 2), round(-v[1], 2), round(v[2], 2)]

# ------------------------------------------------------------------------------------------------
# preview rendering
# ------------------------------------------------------------------------------------------------
def studiolight(name):
    p = bpy.utils.system_resource('DATAFILES', path=os.path.join('studiolights', 'world', name))
    if not p or not os.path.exists(p):
        p = os.path.join(os.path.dirname(bpy.app.binary_path), '5.2', 'datafiles', 'studiolights', 'world', name)
    return p

def setup_render(scene):
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
        print('GPU init failed:', e)
    scene.cycles.device = 'GPU' if dev != 'CPU' else 'CPU'
    print('RENDER DEVICE', dev)
    scene.cycles.samples = OPT['samples']
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        scene.cycles.denoising_use_gpu = True
    except Exception:
        pass
    scene.cycles.max_bounces = 12
    scene.cycles.transmission_bounces = 12
    scene.cycles.glossy_bounces = 6
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.blur_glossy = 0.5
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.resolution_percentage = OPT['pct']
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
    vs.exposure = OPT['exposure'] if OPT['exposure'] is not None else 0.0

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

def wood_material():
    """Sun-bleached oiled deck boards (game scale: board 14 cm real = 2.24 m, gap 0.6 cm = 0.096 m,
    boards along X). Flat-sawn ring figure around a per-board pith axis, fine pore streaks,
    per-board tone, grey weathering, soft rounded board edges and dark gaps."""
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
    fy = _math(nt, 'FRACT', yb)                                  # 0..1 across a board
    ly = _math(nt, 'MULTIPLY', _math(nt, 'SUBTRACT', fy, 0.5), pitch)   # metres from board centre
    r1 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D'); L.new(board, r1.inputs['W'])
    r2 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D')
    L.new(_math(nt, 'ADD', board, 17.3), r2.inputs['W'])
    R1, R2 = r1.outputs['Value'], r2.outputs['Value']
    # ring figure: rings around an axis along X, offset per board (flat-sawn cathedrals)
    gx = _math(nt, 'MULTIPLY_ADD', R1, 60.0, X)
    gy = _math(nt, 'MULTIPLY_ADD', _math(nt, 'SUBTRACT', R2, 0.5), 2.2, ly)
    gz = _math(nt, 'MULTIPLY_ADD', R1, 1.6, 0.35)
    gv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_math(nt, 'MULTIPLY', gx, 0.22), gv.inputs['X']); L.new(gy, gv.inputs['Y']); L.new(gz, gv.inputs['Z'])
    rings = _n(nt, 'ShaderNodeTexWave', wave_type='RINGS', rings_direction='X', wave_profile='SAW',
               i_Scale=3.4, i_Distortion=3.2, i_Detail=2.5, i_Detail_Scale=1.4, i_Detail_Roughness=0.55)
    L.new(gv.outputs[0], rings.inputs['Vector'])
    latewood = _mrange(nt, rings.outputs['Fac'], 0.62, 0.98, 0.0, 1.0)
    # fine longitudinal pores / streaks
    sv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_math(nt, 'MULTIPLY', gx, 0.5), sv.inputs['X'])
    L.new(_math(nt, 'MULTIPLY', ly, 26.0), sv.inputs['Y'])
    L.new(_math(nt, 'MULTIPLY', R2, 30.0), sv.inputs['Z'])
    streak = _n(nt, 'ShaderNodeTexNoise', i_Scale=2.2, i_Detail=8.0, i_Roughness=0.62)
    L.new(sv.outputs[0], streak.inputs['Vector'])
    pores = _mrange(nt, streak.outputs['Fac'], 0.3, 0.75, 0.0, 1.0)
    # large weathering blotches
    blot = _n(nt, 'ShaderNodeTexNoise', i_Scale=0.18, i_Detail=4.0, i_Roughness=0.6)
    L.new(tc.outputs['Object'], blot.inputs['Vector'])
    weather = _mrange(nt, blot.outputs['Fac'], 0.38, 0.72, 0.0, 0.6)
    # board edges: dark gap + slight rounding shade
    ad = _math(nt, 'ABSOLUTE', ly)
    half = pitch * 0.5
    gap = _mrange(nt, ad, half - gapw * 0.5 - 0.004, half - gapw * 0.5, 0.0, 1.0)
    edge = _mrange(nt, ad, half - gapw * 0.5 - 0.07, half - gapw * 0.5, 0.0, 1.0)
    # colour
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
    # bump: latewood ridges very slightly raised, pores, rounded edges into the gap
    h = _math(nt, 'MULTIPLY_ADD', latewood, 0.25, _math(nt, 'MULTIPLY', pores, 0.35))
    h = _math(nt, 'SUBTRACT', h, _math(nt, 'MULTIPLY', _math(nt, 'POWER', edge, 3.0), 2.5))
    bump = _n(nt, 'ShaderNodeBump', i_Strength=0.25, i_Distance=0.01)
    L.new(h, bump.inputs['Height'])
    L.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Specular IOR Level'].default_value = 0.45
    return m

def setup_stage(scene):
    stage = new_coll('PreviewStage')
    # world: HDRI for light + reflections; camera rays can be swapped to a soft backdrop (underside shot)
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
    env.image = bpy.data.images.load(studiolight(OPT['env']))
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
    bg.inputs['Strength'].default_value = OPT['hdri'] if OPT['hdri'] is not None else 0.6
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
    # ground
    gme = bpy.data.meshes.new('PreviewGround')
    s = 160.0
    gme.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    ground = bpy.data.objects.new('PreviewGround', gme)
    stage.objects.link(ground)
    gme.materials.append(wood_material())
    ground.location = (0.0, 1.05, 0.0)   # car sits on one board, not on a gap
    # sun: warm late-afternoon key
    sl = bpy.data.lights.new('Sun', 'SUN')
    sl.energy = OPT['sun_energy'] if OPT['sun_energy'] is not None else 7.0
    sl.angle = math.radians(0.9)
    sl.color = (1.0, 0.80, 0.58)
    sun = bpy.data.objects.new('Sun', sl)
    stage.objects.link(sun)
    # camera
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


def aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def sph(az, el, dist, target):
    a, e = math.radians(az), math.radians(el)
    t = Vector(target)
    return t + dist * Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))

SHOTS = {
    # name: camera azimuth (deg from +X toward +Y/left), elevation, distance (m), lens, target, focus, f-stop,
    # sun (azimuth, elevation) = direction the sunlight comes FROM
    'hero_34_front': dict(az=34.0, el=9.5, dist=6.0, lens=100, target=(0.12, 0.0, 0.19), focus=(0.40, 0.40, 0.16), fstop=0.7,
                          sun=(-12.0, 24.0)),
    'side_profile': dict(az=90.0, el=3.0, dist=8.2, lens=135, target=(0.08, 0.0, 0.24), focus=(0.05, 0.42, 0.2), fstop=2.0,
                         sun=(48.0, 28.0)),
    'rear_34': dict(az=-138.0, el=11.0, dist=6.6, lens=100, target=(-0.04, 0.0, 0.22), focus=(-0.58, -0.40, 0.22), fstop=0.9,
                    sun=(-150.0, 26.0)),
    'top_down': dict(top=True, dist=6.4, lens=100, target=(0.09, 0.0, 0.0), focus=(0.0, 0.0, 0.40), fstop=5.6,
                     sun=(110.0, 42.0)),
    'underside': dict(under=True, az=-30.0, el=-62.0, dist=6.8, lens=100, target=(0.08, 0.0, 0.13),
                      focus=(0.0, 0.0, 0.09), fstop=4.0, sun=(90.0, -20.0)),
    'blade_raised': dict(az=26.0, el=9.0, dist=6.8, lens=100, target=(0.16, 0.0, 0.24), focus=(0.70, 0.42, 0.3), fstop=0.8,
                         sun=(-12.0, 24.0), blade=BLADE_RANGE[1]),
}

def render_shots(scene, rig, outdir, shots, blade_ob=None):
    os.makedirs(outdir, exist_ok=True)
    for name in shots:
        cfg = dict(SHOTS[name])
        cfg.update((OPT['override'] or {}).get(name, {}))
        cam, foc, sun = rig['cam'], rig['focus'], rig['sun']
        cam.data.lens = cfg['lens']
        cam.data.dof.aperture_fstop = cfg['fstop']
        under = bool(cfg.get('under'))
        rig['ground'].hide_render = under
        rig['backdrop'].inputs[1].default_value = 1.0 if under else 0.0
        rig['under'].data.energy = 900.0 if under else 0.0
        saz, sel = cfg['sun']
        sun.rotation_euler = (-sph(saz, sel, 1.0, (0, 0, 0))).to_track_quat('-Z', 'Y').to_euler()
        if cfg.get('top'):
            t = Vector(cfg['target'])
            cam.location = (t.x, t.y, cfg['dist'])
            cam.rotation_euler = (0.0, 0.0, 0.0)
        else:
            cam.location = sph(cfg['az'], cfg['el'], cfg['dist'], cfg['target'])
            aim(cam, cfg['target'])
        if under:
            # soft box between the camera and the base, aimed at the base
            uo = rig['under']
            uo.location = sph(cfg['az'] + 40.0, -55.0, 3.2, cfg['target'])
            aim(uo, cfg['target'])
        foc.location = cfg['focus']
        if blade_ob is not None:
            blade_ob.rotation_euler = (0.0, -math.radians(cfg.get('blade', 0.0)), 0.0)
        scene.render.filepath = os.path.join(outdir, name + OPT['suffix'] + '.png')
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print('RENDERED', name, '%.1fs' % (time.time() - t0))
    if blade_ob is not None:
        blade_ob.rotation_euler = (0.0, 0.0, 0.0)

# ------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------
def main():
    global SRC, EXP, PREV
    t0 = time.time()
    scene = reset_scene()
    SRC = new_coll('_src_pieces')
    EXP = new_coll('Export')
    PREV = new_coll('PreviewWheels')
    build_materials()

    # ---- wheel ----
    build_wheel()
    wheel = merge_part('Wheel')
    uv_unwrap(wheel)
    uv1_wheel(wheel)
    wheel.hide_render = True   # master stays at the origin for export; instances below are rendered

    parts = {}
    if not OPT['wheel_only']:
        build_body(); build_base(); build_windows(); build_interior(); build_blade()
        for part in ('Body', 'Base', 'Windows', 'Interior'):
            parts[part] = merge_part(part)
        parts['Blade'] = merge_part('Blade', origin=HINGE)
        for part, ob in parts.items():
            uv_unwrap(ob)
        uv1_side_projection(parts['Body'], TAMPO_BOX)
        uv1_side_projection(parts['Windows'], TAMPO_BOX)
        uv1_blade(parts['Blade'])
        uv1_bottom(parts['Base'])
        uv1_copy(parts['Interior'])

    # wheel instances (left wheels as authored, right wheels yawed 180 deg)
    for key, (wx, wy) in {'FL': (AXLE_X, TRACK_Y), 'FR': (AXLE_X, -TRACK_Y),
                          'RL': (-AXLE_X, TRACK_Y), 'RR': (-AXLE_X, -TRACK_Y)}.items():
        inst = bpy.data.objects.new('Wheel_' + key, wheel.data)
        PREV.objects.link(inst)
        inst.location = (wx * U, wy * U, AXLE_Z * U)
        if wy < 0:
            inst.rotation_euler = (0.0, 0.0, math.pi)
        for mod in wheel.modifiers:
            nm = inst.modifiers.new(mod.name, mod.type)
            for attr in ('min_vertices', 'quad_method', 'ngon_method', 'mode', 'weight', 'keep_sharp'):
                if hasattr(mod, attr):
                    setattr(nm, attr, getattr(mod, attr))
        if OPT['wheel_only'] and key != 'FL':
            inst.hide_render = True
    bpy.context.view_layer.update()

    # ---- stats ----
    stats = {}
    for part, ob in list(parts.items()) + [('Wheel', wheel)]:
        tris, bb = eval_stats(ob)
        stats[part] = dict(tris=tris, bbox_uu=bb)
        print('PART %-9s %-20s tris=%6d  bbox(uu, blender)=%s' % (part, ob.name, tris, bb))

    # exclude the source pieces from the view layer (kept in the .blend for editing)
    bpy.context.view_layer.layer_collection.children['_src_pieces'].exclude = True

    # ---- export ----
    if OPT['export']:
        os.makedirs(os.path.join(WHEEL_DIR, 'export'), exist_ok=True)
        export_fbx(wheel, os.path.join(WHEEL_DIR, 'export', 'SM_Wheel_W03_Lug.fbx'))
        wheel_json = {
            "wheel_design": "W03_Lug", "mesh": "SM_Wheel_W03_Lug",
            "description": "Chunky off-road lug tyre, black, with a deep yellow dish hub (6 nuts, centre boss, axle hole).",
            "units": "uu, UE axes (X fwd, Y right, Z up)",
            "radius": WHEEL_R, "width": WHEEL_W, "hub_radius": 8.95,
            "origin": "wheel centre", "axle_axis": "Y",
            "outer_face": "Blender +Y = UE -Y, i.e. authored as a LEFT wheel. Right wheels: yaw 180 deg (tread is 180-deg symmetric: 15 staggered lugs per row).",
            "slots": ["Tire", "Hub"], "tris": stats['Wheel']['tris'],
            "uv": {"UV0": "smart unwrap (wear/grain)", "UV1": "planar side projection X/Z over the wheel diameter (sidewall decals)"},
            "used_by": ["Navvy"],
        }
        with open(os.path.join(WHEEL_DIR, 'Wheel_W03_Lug.json'), 'w') as f:
            json.dump(wheel_json, f, indent=2)
        if not OPT['wheel_only']:
            os.makedirs(os.path.join(HERE, 'export'), exist_ok=True)
            for part, ob in parts.items():
                export_fbx(ob, os.path.join(HERE, 'export', ob.name + '.fbx'))
            bb = stats['Body']['bbox_uu']
            bl = stats['Blade']['bbox_uu']
            sidecar = {
                "casting": "Navvy", "class": "Lifted", "brand": "KESTREL MOTOR WORKS",
                "units": "uu, UE axes (X fwd, Y right, Z up); origin at ground level centred between the axles",
                "length": 118, "width": 86, "height": 44,
                "hitbox": {"center": [0, 0, 22], "extent": [59, 43, 22]},
                "wheel_design": "W03_Lug", "wheel_radius": WHEEL_R, "wheel_width": WHEEL_W,
                "wheelbase": 2 * AXLE_X, "track": 2 * TRACK_Y,
                "wheels": {"FL": ue((AXLE_X, TRACK_Y, AXLE_Z)), "FR": ue((AXLE_X, -TRACK_Y, AXLE_Z)),
                           "RL": ue((-AXLE_X, TRACK_Y, AXLE_Z)), "RR": ue((-AXLE_X, -TRACK_Y, AXLE_Z))},
                "wheel_mesh_note": "SM_Wheel_W03_Lug is authored as a left wheel (hub face to UE -Y); yaw right wheels 180 deg.",
                "parts": {"Body": "SM_Navvy_Body", "Base": "SM_Navvy_Base", "Windows": "SM_Navvy_Windows",
                          "Interior": "SM_Navvy_Interior", "Blade": "SM_Navvy_Blade"},
                "feature": {
                    "type": "Blade", "part": "SM_Navvy_Blade",
                    "hinge": ue(HINGE), "hinge_axis": "Y (UE pitch)",
                    "mesh_origin": "SM_Navvy_Blade vertices are relative to the hinge: attach the blade component at 'hinge' with zero rotation; at pitch 0 it sits in its rest pose.",
                    "raise_range_deg": list(BLADE_RANGE), "rest_deg": 0.0,
                    "sign": "UE FRotator pitch, positive raises the blade (cutting edge moves up and forward)",
                    "at_min": "cutting edge touches the ground (z ~0)",
                    "rest_cutting_edge_z": 1.55,
                    "blade_width": 86.0, "blade_front_x": round(bl[1], 2),
                    "blade_adds_at_front": round(bl[1] - 59.5, 2),
                    "push_face": "concave moldboard, front x 70.9-78.4, z 1.5-25.3 at rest",
                },
                "slots": {"Body": SLOTS['Body'], "Base": SLOTS['Base'], "Windows": SLOTS['Windows'],
                          "Interior": SLOTS['Interior'], "Blade": SLOTS['Blade']},
                "lamp_tint": "Body vertex colour 'Col' on Lamp faces: white = clear (head/work lamps), red = tail lamps, amber = roof beacon. Multiply in the Lamp material.",
                "axles": "steel axles are part of SM_Navvy_Body (slot Zamac) at x = +/-33, z = 14, |y| <= 41.8, radius 1.0; the two rivet heads under the base are also Body/Zamac (bare metal).",
                "uv": {
                    "UV0": "smart unwrap per part, non-overlapping (wear, grain, chips)",
                    "UV1_body_windows": "tampo layout from a fixed box x[-64,64] y[-44,44] z[0,50] uu (Blender axes): left side U 0-0.5 (front at U 0, as seen from the left), right side U 0.5-1 (front at U 1), sides V 0-0.64 by height; top strip V 0.68-1 (U rear->front, V right->left seen from above); front/rear/underside faces in the blank band V 0.64-0.68",
                    "UV1_blade": "front projection of the push face U 0-1 across the width as seen from the front, V 0-0.6 by height; arm sides V 0.62-1 (left U 0-0.5, right U 0.5-1)",
                    "UV1_base": "projection from below, readable from below with the front to the right: U rear->front, V left->right; moulded text area is the plain panel x[-24.2,22.2] y[-13.7,13.7] uu inside the raised border (base text decal goes there)",
                    "UV1_interior": "copy of UV0",
                },
                "measured_bbox_uu_blender_axes": {k: v['bbox_uu'] for k, v in stats.items()},
                "tris": {k: v['tris'] for k, v in stats.items()},
                "source": "SourceArt/Blender/Navvy/build_navvy.py",
            }
            with open(os.path.join(HERE, 'Navvy.json'), 'w') as f:
                json.dump(sidecar, f, indent=2)

    # ---- previews ----
    if OPT['render']:
        setup_render(scene)
        rig = setup_stage(scene)
        if OPT['wheel_only']:
            wc = (AXLE_X * U, TRACK_Y * U, AXLE_Z * U)
            SHOTS['wheel_solo_34'] = dict(az=125.0, el=14.0, dist=2.0, lens=100, target=wc,
                                          focus=(wc[0], wc[1] + 0.07, wc[2]), fstop=1.4, sun=(60.0, 26.0))
            SHOTS['wheel_solo_face'] = dict(az=90.0, el=4.0, dist=2.1, lens=100, target=wc,
                                            focus=(wc[0], wc[1] + 0.07, wc[2]), fstop=2.8, sun=(60.0, 30.0))
            render_shots(scene, rig, os.path.join(WHEEL_DIR, 'preview'), OPT['shots'] or ['wheel_solo_34', 'wheel_solo_face'])
        else:
            shots = OPT['shots'] or ['hero_34_front', 'side_profile', 'rear_34', 'top_down', 'underside', 'blade_raised']
            render_shots(scene, rig, os.path.join(HERE, 'preview'), shots, blade_ob=parts.get('Blade'))
            if OPT['shots'] is None or 'wheel_close' in (OPT['shots'] or []):
                SHOTS['wheel_close'] = dict(az=62.0, el=10.0, dist=2.6, lens=100,
                                            target=(AXLE_X * U, TRACK_Y * U, AXLE_Z * U),
                                            focus=(AXLE_X * U, (TRACK_Y + 7) * U, AXLE_Z * U), fstop=2.2, sun=(80.0, 28.0))
                render_shots(scene, rig, os.path.join(WHEEL_DIR, 'preview'), ['wheel_close'], blade_ob=parts.get('Blade'))

    if OPT['export']:
        blend = os.path.join(WHEEL_DIR, 'Wheel_W03_Lug.blend') if OPT['wheel_only'] else os.path.join(HERE, 'navvy.blend')
        bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    print('DONE in %.1fs' % (time.time() - t0))

main()
