"""
build_Wheel_W02_Fan.py  -  MODEL '93 / CozyCarGame, Slice 1A          (rebuild v2, 14 Oct 2026)
==================================================================================================
Shared toy wheel W02_Fan, rebuilt to spec 4b rule 3 ("era wheels"):
  ONE plastic part: a narrow hard black plastic "tyre" ring (no rubber sidewall, no tread, a faint
  mould parting line) moulded round a vacuum-chromed fan disc (8 thick swept vanes on a dished
  floor, a fat outer lip, a centre boss with a through hole where the steel axle's peened head
  shows). Slightly oversized for the scale: radius 9.8 uu (12.3 mm real diameter), width 6.4 uu.

This file is ALSO the shared toolkit for ../Vortex/build_Vortex.py:
  * SDF ops + surface-nets mesher + planar/collapse decimation + analytic corner normals
  * toy stand-in materials named like the UE slots
  * the PREVIEW STAGE copied from ../Navvy/build_navvy.py (the benchmark that passed with the
    owner): sunset.exr world rotated 200 deg with a warm multiply, procedural deck boards on a
    ground plane at y = 1.05 m, warm 0.9 deg sun, 36 mm sensor, 100-135 mm lenses, f/0.7-2 DOF,
    Cycles + AgX, 1600x1200. Same numbers, so every car is judged under identical conditions.
  * import_navvy(): Navvy's exported FBX parts + SM_Wheel_W03_Lug with Navvy's own material
    recipe, for the "same toy box" family shots (spec 4b rule 9).

Run headless:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup
      --python build_Wheel_W02_Fan.py [-- --quick] [--norender]

Conventions (Docs/Build/SLICE_1A_BUILD_SPEC.md): game scale in Blender metres (1 uu = 0.01 m),
origin = wheel centre, axle along Y, the OUTER (show) face points +Y (Blender left). Slots: Tire, Hub.
"""
import bpy, bmesh, math, os, sys, json, time
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER_DIR = os.path.dirname(HERE)
ASSET = "Wheel_W02_Fan"
MESH_NAME = "SM_Wheel_W02_Fan"
UU = 0.01                       # Blender metres per uu
WHEEL_RADIUS_UU = 9.8
WHEEL_WIDTH_UU = 6.4
TYRE_SEGMENTS = 48
N_VANES = 8
HUB_FACE_Y = 2.55               # wheel-local y of the hub boss face (axle head sits on it)
BLENDER_HDRI_DIR = r"C:\Program Files\Blender Foundation\Blender 5.2\5.2\datafiles\studiolights\world"


# =============================================================================
#  Generic helpers
# =============================================================================
def log(*a):
    print("[W02]", *a, flush=True)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.scale_length = 1.0
    sc.unit_settings.length_unit = 'METERS'
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


def set_active(ob):
    bpy.context.view_layer.update()
    for o in list(bpy.context.view_layer.objects):
        if o is not None:
            o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)


def apply_modifiers(ob):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def tri_count(ob):
    return int(sum(len(p.vertices) - 2 for p in ob.data.polygons))


def smart_uv(ob, uv_name="UV0", angle=60.0, margin=0.003):
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
    """Spec section 2 export settings, one part per file (object at the origin)."""
    old = ob.location.copy(), ob.rotation_euler.copy(), ob.hide_get(), ob.hide_render
    ob.hide_set(False)
    ob.location = (0, 0, 0); ob.rotation_euler = (0, 0, 0)
    set_active(ob)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True,
                             apply_scale_options='FBX_SCALE_UNITS', axis_forward='X', axis_up='Z',
                             bake_space_transform=True, mesh_smooth_type='FACE', use_tspace=True,
                             add_leaf_bones=False, use_mesh_modifiers=True, object_types={'MESH'},
                             use_custom_props=False, path_mode='STRIP')
    ob.location, ob.rotation_euler = old[0], old[1]
    ob.hide_set(old[2])
    log("exported", os.path.basename(path), "%.1f MB" % (os.path.getsize(path) / 1e6))


def bbox_uu(ob):
    co = np.empty(len(ob.data.vertices) * 3)
    ob.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3) / UU
    return [round(float(v), 2) for v in (co[:, 0].min(), co[:, 0].max(), co[:, 1].min(), co[:, 1].max(),
                                          co[:, 2].min(), co[:, 2].max())]


# =============================================================================
#  SDF toolkit (uu).  Rounded union / intersection after hg_sdf (exact radius for
#  perpendicular surfaces) = the "cast zinc + thick enamel" fillet language of every part.
# =============================================================================
def pchip_eval(xk, yk, xq):
    xk = np.asarray(xk, float); yk = np.asarray(yk, float); xq = np.asarray(xq, float)
    n = len(xk)
    h = np.diff(xk); d = np.diff(yk) / h
    m = np.zeros(n)
    for k in range(1, n - 1):
        if d[k - 1] * d[k] > 0:
            w1 = 2 * h[k] + h[k - 1]; w2 = h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    m[0] = d[0] * 0.5; m[-1] = d[-1] * 0.5
    idx = np.clip(np.searchsorted(xk, xq, side='right') - 1, 0, n - 2)
    t = (xq - xk[idx]) / h[idx]
    t2, t3 = t * t, t * t * t
    return ((2 * t3 - 3 * t2 + 1) * yk[idx] + (t3 - 2 * t2 + t) * h[idx] * m[idx]
            + (-2 * t3 + 3 * t2) * yk[idx + 1] + (t3 - t2) * h[idx] * m[idx + 1])


class Prof:
    """Smooth 1D profile (monotone cubic through keys), clamped outside the key range."""
    def __init__(self, xk, yk, n=4096):
        order = np.argsort(xk)
        xk = np.asarray(xk, float)[order]; yk = np.asarray(yk, float)[order]
        self.x = np.linspace(xk[0], xk[-1], n)
        self.y = pchip_eval(xk, yk, self.x)
        self.dy = np.gradient(self.y, self.x)

    def __call__(self, q):
        return np.interp(q, self.x, self.y)

    def d(self, q):
        return np.interp(q, self.x, self.dy, left=0.0, right=0.0)


def mx0(a):
    return np.maximum(a, 0.0)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def softplus_r(t, r):
    """smooth max(t, 0) with a rounded knee of size r"""
    return 0.5 * (t + np.sqrt(t * t + r * r))


def u_round(a, b, r):
    """union with a concave fillet of radius r"""
    ua = mx0(r - a); ub = mx0(r - b)
    return np.maximum(r, np.minimum(a, b)) - np.sqrt(ua * ua + ub * ub)


def i_round(a, b, r):
    """intersection with a convex round of radius r"""
    ua = mx0(r + a); ub = mx0(r + b)
    return np.minimum(-r, np.maximum(a, b)) + np.sqrt(ua * ua + ub * ub)


def s_round(a, b, r):
    """subtract b from a, the cut edge rounded by r"""
    return i_round(a, -b, r)


def smin_poly(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def sd_rbox(x, y, z, c, h, r):
    qx = np.abs(x - c[0]) - (h[0] - r)
    qy = np.abs(y - c[1]) - (h[1] - r)
    qz = np.abs(z - c[2]) - (h[2] - r)
    return (np.sqrt(mx0(qx) ** 2 + mx0(qy) ** 2 + mx0(qz) ** 2)
            + np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0.0) - r)


def sd_rrect2(a, b, ha, hb, r):
    qa = np.abs(a) - (ha - r); qb = np.abs(b) - (hb - r)
    return np.hypot(mx0(qa), mx0(qb)) + np.minimum(np.maximum(qa, qb), 0.0) - r


def sd_poly(px, py, V):
    """exact signed distance to a closed 2D polygon (any winding, may be non-convex)"""
    V = np.asarray(V, float); n = len(V)
    d = (px - V[0, 0]) ** 2 + (py - V[0, 1]) ** 2
    s = np.ones_like(px)
    j = n - 1
    for i in range(n):
        ex = V[j, 0] - V[i, 0]; ey = V[j, 1] - V[i, 1]
        wx = px - V[i, 0]; wy = py - V[i, 1]
        t = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey), 0.0, 1.0)
        bx = wx - ex * t; by = wy - ey * t
        d = np.minimum(d, bx * bx + by * by)
        c1 = py >= V[i, 1]; c2 = py < V[j, 1]; c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
        j = i
    return s * np.sqrt(d)


def sd_capsule(x, y, z, a, b, r):
    ax, ay_, az = a; bx, by, bz = b
    pax, pay, paz = x - ax, y - ay_, z - az
    bax, bay, baz = bx - ax, by - ay_, bz - az
    h = np.clip((pax * bax + pay * bay + paz * baz) / (bax * bax + bay * bay + baz * baz), 0, 1)
    return np.sqrt((pax - bax * h) ** 2 + (pay - bay * h) ** 2 + (paz - baz * h) ** 2) - r


def sd_seg2(px, py, a, b):
    """unsigned distance to a 2D segment"""
    bax, bay = b[0] - a[0], b[1] - a[1]
    pax, pay = px - a[0], py - a[1]
    h = np.clip((pax * bax + pay * bay) / (bax * bax + bay * bay), 0.0, 1.0)
    return np.hypot(pax - bax * h, pay - bay * h)


def sd_ellipsoid(x, y, z, c, rad):
    px, py, pz = (x - c[0]) / rad[0], (y - c[1]) / rad[1], (z - c[2]) / rad[2]
    k0 = np.sqrt(px * px + py * py + pz * pz)
    qx, qy, qz = px / rad[0], py / rad[1], pz / rad[2]
    k1 = np.sqrt(qx * qx + qy * qy + qz * qz) + 1e-9
    return k0 * (k0 - 1.0) / k1


def offset_convex(poly, d):
    """offset a convex polygon outward by d (negative = inward)"""
    P = np.asarray(poly, float); n = len(P)
    area = 0.5 * sum(P[i, 0] * P[(i + 1) % n, 1] - P[(i + 1) % n, 0] * P[i, 1] for i in range(n))
    if area < 0:
        P = P[::-1].copy()
    lines = []
    for i in range(n):
        a = P[i]; b = P[(i + 1) % n]; e = (b - a) / np.linalg.norm(b - a)
        nrm = np.array([e[1], -e[0]])
        lines.append((a + nrm * d, e))
    out = []
    for i in range(n):
        p1, d1 = lines[i - 1]; p2, d2 = lines[i]
        A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
        t = np.linalg.solve(A, p2 - p1)[0]
        out.append(p1 + t * d1)
    return np.array(out)


def sd_rpoly(px, py, poly, r):
    """rounded convex polygon: the outline passes through `poly`'s edges, corners rounded by r"""
    return sd_poly(px, py, offset_convex(poly, -r)) - r


def round_corners(pts, radii, nseg):
    """Closed 2D polyline with per-vertex tangent fillets; returns sampled points."""
    P = np.asarray(pts, float); n = len(P); out = []
    for i in range(n):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
        r = radii[i]; k = nseg[i]
        if r <= 0 or k <= 0:
            out.append(p1.copy()); continue
        d0 = p0 - p1; d1 = p2 - p1
        l0 = np.linalg.norm(d0); l1 = np.linalg.norm(d1)
        d0 = d0 / l0; d1 = d1 / l1
        ang = math.acos(float(np.clip(np.dot(d0, d1), -1.0, 1.0)))
        if ang > math.pi - 1e-3:
            out.append(p1.copy()); continue
        t = r / math.tan(ang / 2)
        t = min(t, 0.48 * l0, 0.48 * l1)
        re = t * math.tan(ang / 2)
        a = p1 + d0 * t; b = p1 + d1 * t
        bis = d0 + d1; bis = bis / np.linalg.norm(bis)
        c = p1 + bis * (re / math.sin(ang / 2))
        a0 = math.atan2(a[1] - c[1], a[0] - c[0]); a1 = math.atan2(b[1] - c[1], b[0] - c[0])
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        for j in range(k + 1):
            th = a0 + da * j / k
            out.append(c + re * np.array([math.cos(th), math.sin(th)]))
    return np.array(out)


# =============================================================================
#  Surface nets mesher + SDF part pipeline
# =============================================================================
def surface_nets(fn, bmin, bmax, cell, chunk=1_500_000, _depth=0):
    t0 = time.time()
    bmin = np.asarray(bmin, float); bmax = np.asarray(bmax, float)
    n = (np.ceil((bmax - bmin) / cell)).astype(int) + 1
    xs = bmin[0] + np.arange(n[0]) * cell
    ys = bmin[1] + np.arange(n[1]) * cell
    zs = bmin[2] + np.arange(n[2]) * cell
    F = np.empty(tuple(n), np.float32)
    per = max(1, chunk // int(n[1] * n[2]))
    for i0 in range(0, n[0], per):
        i1 = min(n[0], i0 + per)
        X, Y, Z = np.meshgrid(xs[i0:i1], ys, zs, indexing='ij')
        F[i0:i1] = fn(X, Y, Z)
    F[F == 0] = 1e-6
    t1 = time.time()
    s = F < 0
    touch = [s[0].any(), s[-1].any(), s[:, 0].any(), s[:, -1].any(), s[:, :, 0].any(), s[:, :, -1].any()]
    if any(touch) and _depth < 4:
        del F, s
        pad = 2.0
        for k in range(3):
            if touch[2 * k]:
                bmin[k] -= pad
            if touch[2 * k + 1]:
                bmax[k] += pad
        log("  domain touched %s -> grown to %s %s" % (touch, bmin.round(2).tolist(), bmax.round(2).tolist()))
        return surface_nets(fn, bmin, bmax, cell, chunk, _depth + 1)
    cnt = np.zeros(tuple(n - 1), np.uint8)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                cnt += s[a:n[0] - 1 + a, b:n[1] - 1 + b, c:n[2] - 1 + c]
    active = (cnt > 0) & (cnt < 8)
    del cnt
    ci, cj, ck = np.nonzero(active)
    del active
    nv = len(ci)
    vmap = np.full(tuple(n - 1), -1, np.int32)
    vmap[ci, cj, ck] = np.arange(nv, dtype=np.int32)
    offs = [(a, b, c) for c in (0, 1) for b in (0, 1) for a in (0, 1)]
    vals = np.stack([F[ci + a, cj + b, ck + c] for (a, b, c) in offs], 1).astype(np.float64)
    offa = np.array(offs, float)
    acc = np.zeros((nv, 3)); num = np.zeros(nv)
    for i in range(8):
        for k in range(3):
            if (i >> k) & 1:
                continue
            j = i | (1 << k)
            f0 = vals[:, i]; f1 = vals[:, j]
            m = (f0 < 0) != (f1 < 0)
            t = np.where(m, f0 / np.where(m, f0 - f1, 1.0), 0.0)
            p = offa[i][None, :] + t[:, None] * (offa[j] - offa[i])[None, :]
            acc += p * m[:, None]; num += m
    local = acc / np.maximum(num, 1)[:, None]
    V = bmin[None, :] + (np.stack([ci, cj, ck], 1) + local) * cell
    quads = []
    sx = s[:-1, 1:-1, 1:-1] != s[1:, 1:-1, 1:-1]
    i_, j_, k_ = np.nonzero(sx); j_ = j_ + 1; k_ = k_ + 1; del sx
    q = np.stack([vmap[i_, j_ - 1, k_ - 1], vmap[i_, j_, k_ - 1], vmap[i_, j_, k_], vmap[i_, j_ - 1, k_]], 1)
    flip = ~s[i_, j_, k_]; q[flip] = q[flip][:, ::-1]; quads.append(q)
    sy = s[1:-1, :-1, 1:-1] != s[1:-1, 1:, 1:-1]
    i_, j_, k_ = np.nonzero(sy); i_ = i_ + 1; k_ = k_ + 1; del sy
    q = np.stack([vmap[i_ - 1, j_, k_ - 1], vmap[i_ - 1, j_, k_], vmap[i_, j_, k_], vmap[i_, j_, k_ - 1]], 1)
    flip = ~s[i_, j_, k_]; q[flip] = q[flip][:, ::-1]; quads.append(q)
    sz = s[1:-1, 1:-1, :-1] != s[1:-1, 1:-1, 1:]
    i_, j_, k_ = np.nonzero(sz); i_ = i_ + 1; j_ = j_ + 1; del sz
    q = np.stack([vmap[i_ - 1, j_ - 1, k_], vmap[i_, j_ - 1, k_], vmap[i_, j_, k_], vmap[i_ - 1, j_, k_]], 1)
    flip = ~s[i_, j_, k_]; q[flip] = q[flip][:, ::-1]; quads.append(q)
    Q = np.concatenate(quads, 0)
    log("  surface nets: grid %s (%.1fM pts) eval %.1fs, %d verts, %d quads, %.1fs" %
        (tuple(n), np.prod(n) / 1e6, t1 - t0, nv, len(Q), time.time() - t0))
    return V, Q


def eval_chunked(fn, P, chunk=1_000_000):
    out = np.empty(len(P))
    for i in range(0, len(P), chunk):
        p = P[i:i + chunk]
        out[i:i + chunk] = fn(p[:, 0], p[:, 1], p[:, 2])
    return out


def sdf_grad(fn, P, eps=0.02):
    g = np.zeros_like(P)
    for k in range(3):
        d = np.zeros(3); d[k] = eps
        g[:, k] = (eval_chunked(fn, P + d) - eval_chunked(fn, P - d)) / (2 * eps)
    return g


def project(fn, P, iters=2, maxstep=0.3):
    for _ in range(iters):
        f = eval_chunked(fn, P)
        g = sdf_grad(fn, P)
        g2 = (g * g).sum(1) + 1e-12
        step = (f / g2)[:, None] * g
        ln = np.linalg.norm(step, axis=1)
        sc = np.minimum(1.0, maxstep / np.maximum(ln, 1e-12))
        P = P - step * sc[:, None]
    return P


def mesh_from_numpy(name, V, F):
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(V))
    me.vertices.foreach_set("co", np.asarray(V, np.float32).ravel())
    k = F.shape[1]
    me.loops.add(F.size)
    me.loops.foreach_set("vertex_index", np.asarray(F, np.int32).ravel())
    me.polygons.add(len(F))
    me.polygons.foreach_set("loop_start", np.arange(0, F.size, k, dtype=np.int32))
    try:
        me.polygons.foreach_set("loop_total", np.full(len(F), k, np.int32))
    except Exception:
        pass
    me.update(calc_edges=True)
    return me


def mesh_arrays(me):
    V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", V)
    me.calc_loop_triangles()
    T = np.empty(len(me.loop_triangles) * 3, np.int64); me.loop_triangles.foreach_get("vertices", T)
    return V.reshape(-1, 3), T.reshape(-1, 3)


def _unit(v):
    return v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-12)


def corner_normals(fn, V, T, N, eps=0.02, cos_bad=math.cos(math.radians(24.0)), shift=0.45):
    """Per-corner normals. Analytic vertex normals everywhere, except where a vertex normal
    disagrees with its (decimated) face: then sample the SDF gradient a little way inside
    the face, so a big flat triangle touching a groove lip stays flat instead of streaking."""
    P = V[T]
    fn_ = _unit(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]))
    NC = N[T].copy()
    dots = (NC * fn_[:, None, :]).sum(2)
    bad = dots < cos_bad
    nb = int(bad.sum())
    if nb:
        C = P.mean(1)
        ti, ci = np.nonzero(bad)
        pv = P[ti, ci]; dv = C[ti] - pv
        ln = np.linalg.norm(dv, axis=1)
        st = np.minimum(shift, 0.45 * ln)
        q = pv + dv / np.maximum(ln, 1e-9)[:, None] * st[:, None]
        g = _unit(sdf_grad(fn, q, eps=eps))
        d2 = (g * fn_[ti]).sum(1)
        far = d2 < cos_bad
        g[far] = _unit(g[far] + fn_[ti][far])
        NC[ti, ci] = g
    return NC, nb


def sdf_part(name, fn, bmin, bmax, cell, target_tris, symmetric=True, normal_eps=0.02, planar_deg=0.6):
    """SDF -> surface nets -> project -> planar dissolve -> quadric collapse to budget ->
    reproject -> analytic per-corner normals. Returns (V uu, T, NC (nT,3,3))."""
    t0 = time.time()
    V, Q = surface_nets(fn, bmin, bmax, cell)
    V = project(fn, V, iters=2, maxstep=cell)
    me = mesh_from_numpy(name + "_tmp", V * UU, Q)
    ob = bpy.data.objects.new(name + "_tmp", me)
    bpy.context.scene.collection.objects.link(ob)
    ntri = 2 * len(Q)
    nmid = ntri
    if target_tris < ntri:
        # 1) flat panels are truly planar (verts sit on the SDF): dissolve them first so the
        #    budget goes to fillets, grooves and lamps
        if planar_deg > 0:
            mp = ob.modifiers.new("Planar", 'DECIMATE')
            mp.decimate_type = 'DISSOLVE'
            mp.angle_limit = math.radians(planar_deg)
            apply_modifiers(ob)
            nmid = sum(len(p.vertices) - 2 for p in ob.data.polygons)
        # 2) quadric collapse to the budget
        if target_tris < nmid:
            md = ob.modifiers.new("Dec", 'DECIMATE')
            md.decimate_type = 'COLLAPSE'
            md.ratio = min(1.0, target_tris / max(nmid, 1))
            md.use_collapse_triangulate = True
            if symmetric:
                md.use_symmetry = True
                md.symmetry_axis = 'Y'
            apply_modifiers(ob)
    V2, T = mesh_arrays(ob.data)
    V2 = V2 / UU
    V2 = project(fn, V2, iters=1, maxstep=0.1)
    N = _unit(sdf_grad(fn, V2, eps=normal_eps))
    NC, nb = corner_normals(fn, V2, T, N, eps=normal_eps)
    me2 = ob.data
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me2)
    log("  part %-18s %8d -> planar %7d -> %6d tris, %d corners re-aimed (%.1fs)" %
        (name, ntri, nmid, len(T), nb, time.time() - t0))
    return V2, T, NC


def fix_winding(V, T, N):
    e1 = V[T[:, 1]] - V[T[:, 0]]; e2 = V[T[:, 2]] - V[T[:, 0]]
    fn = np.cross(e1, e2); nn = N[T[:, 0]] + N[T[:, 1]] + N[T[:, 2]]
    bad = (fn * nn).sum(1) < 0
    T = T.copy(); T[bad] = T[bad][:, ::-1]
    return T


def profile_normals(P):
    """outward vertex normals of a closed 2D polyline (r, y)"""
    area = 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    E = np.roll(P, -1, axis=0) - P
    En = np.stack([E[:, 1], -E[:, 0]], 1)
    if area < 0:
        En = -En
    En /= np.maximum(np.linalg.norm(En, axis=1), 1e-12)[:, None]
    Nv = En + np.roll(En, 1, axis=0)
    Nv /= np.maximum(np.linalg.norm(Nv, axis=1), 1e-12)[:, None]
    return Nv


def revolve(P, Nr, seg, closed=True):
    """revolve an (r, y) profile around the Y axis; returns V, T, N (uu)."""
    m = len(P)
    th = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    V = np.zeros((m * seg, 3)); N = np.zeros((m * seg, 3))
    for i in range(m):
        V[i * seg:(i + 1) * seg] = np.stack([P[i, 0] * c, np.full(seg, P[i, 1]), P[i, 0] * s], 1)
        N[i * seg:(i + 1) * seg] = np.stack([Nr[i, 0] * c, np.full(seg, Nr[i, 1]), Nr[i, 0] * s], 1)
    T = []
    for i in range(m if closed else m - 1):
        i2 = (i + 1) % m
        for j in range(seg):
            j2 = (j + 1) % seg
            a, b, cc, d = i * seg + j, i2 * seg + j, i2 * seg + j2, i * seg + j2
            T.append((a, b, cc)); T.append((a, cc, d))
    T = np.array(T)
    return V, fix_winding(V, T, N), N


def cylinder_y(xc, zc, r, y0, y1, seg=12):
    """Analytic cylinder along Y (uu) with flat caps; returns V, T, N."""
    ang = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ring = np.stack([xc + r * np.cos(ang), np.zeros(seg), zc + r * np.sin(ang)], 1)
    nrm_ring = np.stack([np.cos(ang), np.zeros(seg), np.sin(ang)], 1)
    V = np.concatenate([ring + [0, y0, 0], ring + [0, y1, 0]])
    N = np.concatenate([nrm_ring, nrm_ring])
    T = []
    for k in range(seg):
        k2 = (k + 1) % seg
        T += [(k, k2, seg + k2), (k, seg + k2, seg + k)]
    c0 = len(V); c1 = c0 + 1
    V = np.concatenate([V, [[xc, y0, zc], [xc, y1, zc]]]); N = np.concatenate([N, [[0, -1, 0], [0, 1, 0]]])
    capv0 = len(V); V = np.concatenate([V, ring + [0, y0, 0]]); N = np.concatenate([N, np.tile([0, -1, 0], (seg, 1))])
    capv1 = len(V); V = np.concatenate([V, ring + [0, y1, 0]]); N = np.concatenate([N, np.tile([0, 1, 0], (seg, 1))])
    for k in range(seg):
        k2 = (k + 1) % seg
        T += [(c0, capv0 + k, capv0 + k2), (c1, capv1 + k2, capv1 + k)]
    T = np.array(T)
    return V, fix_winding(V, T, N), N


def build_object(name, parts, mat_names, coll=None, mat_kw=None):
    """parts: list of dict(V uu, T, N, mat index, col optional (nV,4) or (4,)).
    N may be per-vertex (nV,3) or per-corner (nT,3,3)."""
    Vs, Ts, NCs, Ms, Cs = [], [], [], [], []
    off = 0
    for p in parts:
        V, T, N = p["V"], p["T"], p["N"]
        Vs.append(V); Ts.append(T + off)
        NCs.append(N if N.ndim == 3 else N[T])
        Ms.append(np.full(len(T), p["mat"], np.int32))
        c = p.get("col")
        if c is None:
            c = np.tile([1.0, 1.0, 1.0, 1.0], (len(V), 1))
        elif np.ndim(c) == 1:
            c = np.tile(np.asarray(c, float), (len(V), 1))
        Cs.append(c)
        off += len(V)
    V = np.concatenate(Vs); T = np.concatenate(Ts); NC = np.concatenate(NCs)
    M = np.concatenate(Ms); C = np.concatenate(Cs)
    me = mesh_from_numpy(name, V * UU, T)
    for mn in mat_names:
        me.materials.append(bpy.data.materials.get(mn) or make_slot_material(mn, **(mat_kw or {})))
    me.polygons.foreach_set("material_index", M)
    me.polygons.foreach_set("use_smooth", np.ones(len(T), bool))
    me.update()
    try:
        me.normals_split_custom_set(NC.reshape(-1, 3).tolist())
    except Exception as e:
        log("custom normals (corner) failed:", e)
    attr = me.color_attributes.new("Col", 'BYTE_COLOR', 'POINT')
    attr.data.foreach_set("color", C.astype(np.float32).ravel())
    try:
        me.color_attributes.active_color = attr
        me.color_attributes.render_color_index = 0
    except Exception:
        pass
    ob = bpy.data.objects.new(name, me)
    link(ob, coll)
    return ob


# =============================================================================
#  Toy stand-in materials, named exactly like the UE slots (spec 4b rules 3, 5, 7)
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
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (600, 0)
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.location = (200, 0)
    nt.links.new(bs.outputs[0], out.inputs['Surface'])
    return m, nt, bs


def _set(bs, key, val):
    if key in bs.inputs:
        bs.inputs[key].default_value = val


def _node(nt, typ, loc=(0, 0), **inputs):
    n = nt.nodes.new(typ)
    n.location = loc
    for k, v in inputs.items():
        n.inputs[k].default_value = v
    return n


def _math(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    for i, x in enumerate((a, b)):
        if x is None:
            continue
        if isinstance(x, (int, float)):
            n.inputs[i].default_value = x
        else:
            nt.links.new(x, n.inputs[i])
    return n.outputs[0]


def _mix(nt, fac, a, b, blend='MIX'):
    n = nt.nodes.new('ShaderNodeMix'); n.data_type = 'RGBA'; n.blend_type = blend
    for sock, x in ((n.inputs[0], fac), (n.inputs[6], a), (n.inputs[7], b)):
        if isinstance(x, (int, float, tuple)):
            sock.default_value = x
        else:
            nt.links.new(x, sock)
    return n.outputs[2]


def _mixf(nt, fac, a, b):
    n = nt.nodes.new('ShaderNodeMix'); n.data_type = 'FLOAT'
    for sock, x in ((n.inputs[0], fac), (n.inputs[2], a), (n.inputs[3], b)):
        if isinstance(x, (int, float)):
            sock.default_value = x
        else:
            nt.links.new(x, sock)
    return n.outputs[0]


def _maprange(nt, val, f0, f1, t0=0.0, t1=1.0):
    n = nt.nodes.new('ShaderNodeMapRange')
    nt.links.new(val, n.inputs['Value'])
    n.inputs['From Min'].default_value = f0; n.inputs['From Max'].default_value = f1
    n.inputs['To Min'].default_value = t0; n.inputs['To Max'].default_value = t1
    return n.outputs[0]


def toy_paint_material(name="Paint", paint=(0.15, 0.03, 0.52, 1), flake=(0.55, 0.45, 0.95, 1),
                       tampo_path=None, uv1="UV1", seam=True):
    """Thick die-cast enamel, preview stand-in for the UE M_ToyPaint:
      * metallic base with visible flake sparkle (per-flake random normals, ~0.06 mm real flakes)
      * hard gloss coat with mild orange peel
      * paint pooling: recesses and panel grooves darker / richer (AO, 1.2 uu)
      * paint thinning on the sharpest convex edges (zamac shows through a little)
      * tampo (printed ink, UV1 RGBA texture) on top: opaque satin ink, no metal flake"""
    m, nt, bs = _principled(name)
    L = nt.links.new
    tc = _node(nt, 'ShaderNodeTexCoord', (-1600, 200))
    geo = _node(nt, 'ShaderNodeNewGeometry', (-1600, -200))
    # ---- flake: random normal per voronoi cell (object space, Blender metres) ----------------
    vor = _node(nt, 'ShaderNodeTexVoronoi', (-1300, -500), Scale=1300.0)
    L(tc.outputs['Object'], vor.inputs['Vector'])
    vsub = nt.nodes.new('ShaderNodeVectorMath'); vsub.operation = 'SUBTRACT'
    L(vor.outputs['Color'], vsub.inputs[0]); vsub.inputs[1].default_value = (0.5, 0.5, 0.5)
    vsc = nt.nodes.new('ShaderNodeVectorMath'); vsc.operation = 'SCALE'
    L(vsub.outputs[0], vsc.inputs[0]); vsc.inputs['Scale'].default_value = 0.30
    vadd = nt.nodes.new('ShaderNodeVectorMath'); vadd.operation = 'ADD'
    L(geo.outputs['Normal'], vadd.inputs[0]); L(vsc.outputs[0], vadd.inputs[1])
    vnorm = nt.nodes.new('ShaderNodeVectorMath'); vnorm.operation = 'NORMALIZE'
    L(vadd.outputs[0], vnorm.inputs[0])
    # ---- orange peel on the coat --------------------------------------------------------------
    peel = _node(nt, 'ShaderNodeTexNoise', (-1300, -900), Scale=140.0, Detail=3.0, Roughness=0.55)
    L(tc.outputs['Object'], peel.inputs['Vector'])
    pb = _node(nt, 'ShaderNodeBump', (-1000, -900), Strength=0.045, Distance=0.0006)
    L(peel.outputs['Fac'], pb.inputs['Height'])
    # ---- paint pooling / edge thinning ---------------------------------------------------------
    ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.location = (-1300, 500)
    ao.samples = 12; ao.only_local = True
    ao.inputs['Distance'].default_value = 0.009
    pool_ao = _maprange(nt, ao.outputs['AO'], 0.45, 1.0, 0.75, 0.0)      # deep recesses
    # authored pooling mask (vertex colour Col.G: panel lines, louvre slots)
    vc = nt.nodes.new('ShaderNodeAttribute'); vc.attribute_name = 'Col'; vc.location = (-1600, 700)
    sep = nt.nodes.new('ShaderNodeSeparateColor'); sep.location = (-1400, 700)
    L(vc.outputs['Color'], sep.inputs[0])
    pool_vc = _math(nt, 'MULTIPLY', _math(nt, 'POWER', sep.outputs[1], 0.45), 0.9)
    pool = _math(nt, 'MAXIMUM', pool_ao, pool_vc)
    edge = _maprange(nt, geo.outputs['Pointiness'], 0.535, 0.63, 0.0, 1.0)
    base_col = _mix(nt, pool, paint, tuple(c * 0.22 for c in paint[:3]) + (1,))
    base_col = _mix(nt, _math(nt, 'MULTIPLY', edge, 0.22), base_col, (0.42, 0.41, 0.40, 1))
    flake_col = _mix(nt, 0.5, base_col, flake, 'MULTIPLY')
    metal_col = _mix(nt, 0.38, base_col, flake_col)
    # ---- tampo ---------------------------------------------------------------------------------
    ink_a = None
    if tampo_path and os.path.exists(tampo_path):
        img = bpy.data.images.load(tampo_path, check_existing=True)
        try:
            img.alpha_mode = 'STRAIGHT'
        except Exception:
            pass
        uvn = nt.nodes.new('ShaderNodeUVMap'); uvn.uv_map = uv1; uvn.location = (-1600, 900)
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img; tex.location = (-1300, 900)
        tex.interpolation = 'Cubic'; tex.extension = 'CLIP'
        L(uvn.outputs['UV'], tex.inputs['Vector'])
        # ink rubs a little off the sharpest edges and pools darker in grooves
        ink_a = _math(nt, 'MULTIPLY', tex.outputs['Alpha'],
                      _math(nt, 'SUBTRACT', 1.0, _math(nt, 'MULTIPLY', edge, 0.35)))
        ink_col = _mix(nt, _math(nt, 'MULTIPLY', pool, 0.35), tex.outputs['Color'], (0.0, 0.0, 0.0, 1))
        col = _mix(nt, ink_a, metal_col, ink_col)
    else:
        col = metal_col
    L(col, bs.inputs['Base Color'])
    metal = _math(nt, 'SUBTRACT', 0.82, _math(nt, 'MULTIPLY', ink_a, 0.82)) if ink_a is not None else None
    if metal is not None:
        L(metal, bs.inputs['Metallic'])
        L(_mixf(nt, ink_a, 0.30, 0.42), bs.inputs['Roughness'])
        L(_mixf(nt, ink_a, 1.0, 0.55), bs.inputs['Coat Weight'])
    else:
        _set(bs, 'Metallic', 0.82); _set(bs, 'Roughness', 0.30); _set(bs, 'Coat Weight', 1.0)
    L(vnorm.outputs[0], bs.inputs['Normal'])
    L(pb.outputs['Normal'], bs.inputs['Coat Normal'])
    _set(bs, 'Coat Roughness', 0.045); _set(bs, 'Coat IOR', 1.5)
    m.diffuse_color = paint
    return m


def make_slot_material(slot, **kw):
    """Toy stand-ins named exactly like the UE slots."""
    if slot == "Paint":
        return toy_paint_material("Paint", kw.get("paint", (0.15, 0.03, 0.52, 1)),
                                  kw.get("flake", (0.6, 0.5, 1.0, 1)), kw.get("tampo"))
    m, nt, bs = _principled(slot)
    if slot == "Chrome":           # vacuum-metallised chrome
        _set(bs, 'Base Color', (0.92, 0.92, 0.93, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.06)
    elif slot == "Hub":            # chrome-plated plastic wheel face (a hair softer than bright chrome)
        _set(bs, 'Base Color', (0.90, 0.90, 0.92, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.075)
        m.diffuse_color = (0.9, 0.9, 0.9, 1)
    elif slot == "Zamac":          # bright steel axles, peened heads, rivets
        _set(bs, 'Base Color', (0.62, 0.61, 0.59, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.24)
    elif slot == "Lamp":           # cast lamp shapes coloured by printed ink (tint = vertex colour 'Col')
        attr = nt.nodes.new('ShaderNodeVertexColor'); attr.location = (-400, 0)
        try:
            attr.layer_name = "Col"
        except Exception:
            pass
        nt.links.new(attr.outputs['Color'], bs.inputs['Base Color'])
        _set(bs, 'Metallic', 0.0); _set(bs, 'Roughness', 0.30)
        _set(bs, 'Coat Weight', 0.6); _set(bs, 'Coat Roughness', 0.08)
    elif slot == "Glass":          # one-piece light-smoke moulding, 2 uu thick
        _set(bs, 'Base Color', kw.get("glass", (0.955, 0.965, 0.97, 1))); _set(bs, 'Metallic', 0.0)
        _set(bs, 'Roughness', 0.015); _set(bs, 'IOR', 1.49); _set(bs, 'Transmission Weight', 1.0)
        m.diffuse_color = (0.6, 0.65, 0.7, 0.4)
        # Cycles blocks shadow rays at refractive glass (no caustics), which leaves the cab black.
        # Shadow rays see a tinted transparent sheet instead, so sun and sky light the interior.
        out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
        lp = nt.nodes.new('ShaderNodeLightPath'); lp.location = (-200, 300)
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tr.location = (200, 250)
        tr.inputs['Color'].default_value = kw.get("glass_shadow", (0.86, 0.88, 0.89, 1))
        mx = nt.nodes.new('ShaderNodeMixShader'); mx.location = (420, 100)
        nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0])
        nt.links.new(bs.outputs[0], mx.inputs[1])
        nt.links.new(tr.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs['Surface'])
    elif slot == "Interior":       # one-colour moulded plastic tub
        _set(bs, 'Base Color', kw.get("interior", (0.42, 0.41, 0.39, 1))); _set(bs, 'Roughness', 0.5)
        _set(bs, 'Specular IOR Level', 0.45)
    elif slot == "Base":           # black plastic chassis, satin
        _set(bs, 'Base Color', kw.get("base", (0.020, 0.020, 0.022, 1))); _set(bs, 'Roughness', 0.42)
        _set(bs, 'Specular IOR Level', 0.5)
    elif slot == "Tire":           # hard black toy plastic ring, a little glossy
        _set(bs, 'Base Color', (0.016, 0.016, 0.017, 1)); _set(bs, 'Roughness', 0.34)
        _set(bs, 'Specular IOR Level', 0.5)
    return m


# =============================================================================
#  PREVIEW STAGE  --  copied from ../Navvy/build_navvy.py (setup_render, wood_material,
#  setup_stage, aim, sph, render_shots) so every casting is judged under identical conditions.
# =============================================================================
STAGE_OPT = dict(samples=96, pct=100, exposure=None, hdri=None, sun_energy=None, env='sunset.exr')


def studiolight(name):
    p = bpy.utils.system_resource('DATAFILES', path=os.path.join('studiolights', 'world', name))
    if not p or not os.path.exists(p):
        p = os.path.join(BLENDER_HDRI_DIR, name)
    return p


def setup_render(scene):
    OPT = STAGE_OPT
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
    log('RENDER DEVICE', dev)
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
    applied = None
    for look in ('AgX - Punchy', 'AgX - Medium High Contrast', 'None'):      # same order as Navvy
        try:
            vs.look = look
            applied = look
            break
        except Exception:
            continue
    log('view transform AgX, look', applied)
    vs.exposure = OPT['exposure'] if OPT['exposure'] is not None else 0.0


def _n(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items():
        if k.startswith('i_'):
            n.inputs[k[2:].replace('_', ' ')].default_value = v
        else:
            setattr(n, k, v)
    return n


def _nmath(nt, op, a=None, b=None, c=None):
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


def _nmrange(nt, val, f0, f1, t0=0.0, t1=1.0):
    m = nt.nodes.new('ShaderNodeMapRange')
    nt.links.new(val, m.inputs['Value'])
    m.inputs['From Min'].default_value = f0
    m.inputs['From Max'].default_value = f1
    m.inputs['To Min'].default_value = t0
    m.inputs['To Max'].default_value = t1
    return m.outputs[0]


def _nmixc(nt, fac, a, b, blend='MIX'):
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
    """Navvy's deck boards, verbatim: sun-bleached oiled boards (board 14 cm real = 2.24 m,
    gap 0.6 cm = 0.096 m, along X), flat-sawn ring figure, pores, per-board tone, weathering,
    rounded board edges and dark gaps."""
    m = bpy.data.materials.new('PreviewWood')
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    L = nt.links
    bsdf = nt.nodes.get('Principled BSDF')
    if bsdf is None:
        nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
        L.new(bsdf.outputs[0], out.inputs['Surface'])
    tc = _n(nt, 'ShaderNodeTexCoord')
    sep = _n(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    X, Y = sep.outputs['X'], sep.outputs['Y']
    pitch, gapw = 2.336, 0.096
    yb = _nmath(nt, 'MULTIPLY_ADD', Y, 1.0 / pitch, 0.5)
    board = _nmath(nt, 'FLOOR', yb)
    fy = _nmath(nt, 'FRACT', yb)
    ly = _nmath(nt, 'MULTIPLY', _nmath(nt, 'SUBTRACT', fy, 0.5), pitch)
    r1 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D'); L.new(board, r1.inputs['W'])
    r2 = _n(nt, 'ShaderNodeTexWhiteNoise', noise_dimensions='1D')
    L.new(_nmath(nt, 'ADD', board, 17.3), r2.inputs['W'])
    R1, R2 = r1.outputs['Value'], r2.outputs['Value']
    gx = _nmath(nt, 'MULTIPLY_ADD', R1, 60.0, X)
    gy = _nmath(nt, 'MULTIPLY_ADD', _nmath(nt, 'SUBTRACT', R2, 0.5), 2.2, ly)
    gz = _nmath(nt, 'MULTIPLY_ADD', R1, 1.6, 0.35)
    gv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_nmath(nt, 'MULTIPLY', gx, 0.22), gv.inputs['X']); L.new(gy, gv.inputs['Y']); L.new(gz, gv.inputs['Z'])
    rings = _n(nt, 'ShaderNodeTexWave', wave_type='RINGS', rings_direction='X', wave_profile='SAW',
               i_Scale=3.4, i_Distortion=3.2, i_Detail=2.5, i_Detail_Scale=1.4, i_Detail_Roughness=0.55)
    L.new(gv.outputs[0], rings.inputs['Vector'])
    latewood = _nmrange(nt, rings.outputs['Fac'], 0.62, 0.98, 0.0, 1.0)
    sv = _n(nt, 'ShaderNodeCombineXYZ')
    L.new(_nmath(nt, 'MULTIPLY', gx, 0.5), sv.inputs['X'])
    L.new(_nmath(nt, 'MULTIPLY', ly, 26.0), sv.inputs['Y'])
    L.new(_nmath(nt, 'MULTIPLY', R2, 30.0), sv.inputs['Z'])
    streak = _n(nt, 'ShaderNodeTexNoise', i_Scale=2.2, i_Detail=8.0, i_Roughness=0.62)
    L.new(sv.outputs[0], streak.inputs['Vector'])
    pores = _nmrange(nt, streak.outputs['Fac'], 0.3, 0.75, 0.0, 1.0)
    blot = _n(nt, 'ShaderNodeTexNoise', i_Scale=0.18, i_Detail=4.0, i_Roughness=0.6)
    L.new(tc.outputs['Object'], blot.inputs['Vector'])
    weather = _nmrange(nt, blot.outputs['Fac'], 0.38, 0.72, 0.0, 0.6)
    ad = _nmath(nt, 'ABSOLUTE', ly)
    half = pitch * 0.5
    gap = _nmrange(nt, ad, half - gapw * 0.5 - 0.004, half - gapw * 0.5, 0.0, 1.0)
    edge = _nmrange(nt, ad, half - gapw * 0.5 - 0.07, half - gapw * 0.5, 0.0, 1.0)
    early = _nmixc(nt, R1, (0.50, 0.33, 0.19, 1), (0.40, 0.25, 0.14, 1))
    late = _nmixc(nt, R2, (0.22, 0.12, 0.06, 1), (0.17, 0.095, 0.05, 1))
    col = _nmixc(nt, latewood, early, late)
    col = _nmixc(nt, _nmath(nt, 'MULTIPLY', pores, 0.35), col, (0.20, 0.12, 0.07, 1))
    col = _nmixc(nt, weather, col, (0.43, 0.38, 0.32, 1))
    col = _nmixc(nt, _nmath(nt, 'MULTIPLY', edge, 0.45), col, (0.12, 0.075, 0.045, 1))
    col = _nmixc(nt, gap, col, (0.008, 0.006, 0.004, 1))
    L.new(col, bsdf.inputs['Base Color'])
    rough = _nmath(nt, 'MULTIPLY_ADD', pores, 0.18, _nmath(nt, 'MULTIPLY_ADD', weather, 0.25, 0.5))
    L.new(rough, bsdf.inputs['Roughness'])
    h = _nmath(nt, 'MULTIPLY_ADD', latewood, 0.25, _nmath(nt, 'MULTIPLY', pores, 0.35))
    h = _nmath(nt, 'SUBTRACT', h, _nmath(nt, 'MULTIPLY', _nmath(nt, 'POWER', edge, 3.0), 2.5))
    bump = _n(nt, 'ShaderNodeBump', i_Strength=0.25, i_Distance=0.01)
    L.new(h, bump.inputs['Height'])
    L.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    bsdf.inputs['Specular IOR Level'].default_value = 0.45
    return m


def setup_stage(scene):
    """Navvy's stage, verbatim numbers."""
    OPT = STAGE_OPT
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
    if bg is None or out is None:
        nt.nodes.clear()
        bg = nt.nodes.new('ShaderNodeBackground')
        out = nt.nodes.new('ShaderNodeOutputWorld')
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
    gme = bpy.data.meshes.new('PreviewGround')
    s = 160.0
    gme.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    ground = bpy.data.objects.new('PreviewGround', gme)
    stage.objects.link(ground)
    gme.materials.append(wood_material())
    ground.location = (0.0, 1.05, 0.0)
    sl = bpy.data.lights.new('Sun', 'SUN')
    sl.energy = OPT['sun_energy'] if OPT['sun_energy'] is not None else 7.0
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


def aim(ob, target):
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def sph(az, el, dist, target):
    a, e = math.radians(az), math.radians(el)
    t = Vector(target)
    return t + dist * Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))


def render_shot(scene, rig, path, cfg):
    """Navvy's render_shots body for one shot config: az, el, dist, lens, target, focus, fstop,
    sun (az, el the light comes FROM), optional top=True / under=True."""
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
        uo = rig['under']
        uo.location = sph(cfg['az'] + 40.0, -55.0, 3.2, cfg['target'])
        aim(uo, cfg['target'])
    foc.location = cfg['focus']
    scene.render.filepath = path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    t0 = time.time()
    try:
        bpy.ops.render.render(write_still=True)
    except Exception as e:
        log("GPU render failed (%s); retrying on CPU" % e)
        scene.cycles.device = 'CPU'
        bpy.ops.render.render(write_still=True)
    log('RENDERED', os.path.basename(path), '%.1fs' % (time.time() - t0))


# =============================================================================
#  Navvy, imported from its exported FBX parts, wearing Navvy's own material recipe
#  (copied from build_navvy.py build_materials) -- spec 4b rule 9 family shots.
# =============================================================================
NAVVY_DIR = os.path.join(BLENDER_DIR, "Navvy")
NAVVY_SLOTS = {'SM_Navvy_Body': ['Paint', 'Chrome', 'Lamp', 'Zamac'], 'SM_Navvy_Base': ['Base'],
               'SM_Navvy_Windows': ['Glass'], 'SM_Navvy_Interior': ['Interior'],
               'SM_Navvy_Blade': ['Paint', 'Zamac'], 'SM_Wheel_W03_Lug': ['Tire', 'Hub']}


def _nv_principled(name, base, metallic=0.0, rough=0.5, coat=0.0, coat_rough=0.03, trans=0.0, ior=1.5,
                   vcol=False, spec=0.5, peel=0.0):
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    b = nt.nodes.get('Principled BSDF')
    if b is None:
        nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        b = nt.nodes.new('ShaderNodeBsdfPrincipled')
        nt.links.new(b.outputs[0], out.inputs['Surface'])
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
    bpy.ops.import_scene.fbx(filepath=path, use_custom_normals=True)
    new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
    return new


def import_navvy(location=(0.0, 0.0, 0.0), yaw_deg=0.0):
    """Navvy (all parts + 4 x W03_Lug) as exported for the game, parented to one empty."""
    coll = get_coll("Navvy")
    M = navvy_materials()
    root = bpy.data.objects.new("NavvyRoot", None)
    link(root, coll)
    parts = {}
    for nm in ('SM_Navvy_Body', 'SM_Navvy_Base', 'SM_Navvy_Windows', 'SM_Navvy_Interior', 'SM_Navvy_Blade'):
        obs = _import_fbx(os.path.join(NAVVY_DIR, "export", nm + ".fbx"))
        for o in obs:
            parts[nm] = o
    wobs = _import_fbx(os.path.join(BLENDER_DIR, "Wheel_W03_Lug", "export", "SM_Wheel_W03_Lug.fbx"))
    wheel = wobs[0]
    parts['SM_Wheel_W03_Lug'] = wheel
    bpy.context.view_layer.update()
    M0 = {}
    for nm, o in parts.items():
        for c in list(o.users_collection):
            c.objects.unlink(o)
        link(o, coll)
        for i, sl in enumerate(NAVVY_SLOTS[nm]):
            if i < len(o.data.materials):
                o.data.materials[i] = M[sl]
            else:
                o.data.materials.append(M[sl])
        # keep the importer's axis/unit conversion (rotation + scale), drop its translation
        m = o.matrix_world.copy()
        m.translation = (0.0, 0.0, 0.0)
        M0[nm] = m
        o.parent = root
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.matrix_basis = m
    parts['SM_Navvy_Blade'].matrix_basis = Matrix.Translation((-4.0 * UU, 0.0, 32.0 * UU)) @ M0['SM_Navvy_Blade']
    wheel.hide_render = True; wheel.hide_set(True)
    for key, (wx, wy) in {'FL': (33.0, 36.0), 'FR': (33.0, -36.0), 'RL': (-33.0, 36.0), 'RR': (-33.0, -36.0)}.items():
        inst = bpy.data.objects.new('NavvyWheel_' + key, wheel.data)
        link(inst, coll)
        inst.parent = root
        inst.matrix_parent_inverse = Matrix.Identity(4)
        inst.matrix_basis = (Matrix.Translation((wx * UU, wy * UU, 14.0 * UU)) @
                             Matrix.Rotation(math.pi if wy < 0 else 0.0, 4, 'Z') @ M0['SM_Wheel_W03_Lug'])
    root.location = location
    root.rotation_euler = (0.0, 0.0, math.radians(yaw_deg))
    bpy.context.view_layer.update()
    b = parts['SM_Navvy_Body']
    pts = [root.matrix_world.inverted() @ (b.matrix_world @ v.co) for v in b.data.vertices]
    bb = [round(min(p[k] for p in pts) / UU, 1) for k in range(3)] + [round(max(p[k] for p in pts) / UU, 1) for k in range(3)]
    log("Navvy imported, body bbox uu (root space, min xyz / max xyz):", bb, "(expect -62.8 -43.5 7.35 / 57.5 43.5 50.25)")
    return root


# =============================================================================
#  The wheel  (wheel-local uu: origin at the centre, axle along Y, show face +Y)
# =============================================================================
def tyre_profile():
    """Closed cross-section (r, y) of the black plastic ring: flat smooth tread with soft
    shoulders and a faint mould parting line, a narrow flat outer face, a rounded lip that
    holds the chrome disc, a plain back face round the axle boss."""
    R, H = WHEEL_RADIUS_UU, WHEEL_WIDTH_UU / 2.0       # 9.8, 3.2
    pts = [
        (4.0, -2.55),           # back boss (hidden), round the axle bore
        (7.6, -H + 0.05),       # back face
        (R, -H + 0.85),         # back shoulder
        (R, -0.08), (R + 0.045, 0.0), (R, 0.08),   # mould parting line
        (R - 0.06, H - 1.05),   # front shoulder (a whisper of taper: moulding draft)
        (8.75, H),              # outer face
        (7.55, H - 0.02),       # lip crown
        (7.05, H - 0.42),       # lip turn-in (the chrome face sits inside, ~0.6 lower)
        (6.85, 0.6),            # bore wall (hidden by the disc)
        (4.0, 0.2),
    ]
    radii = [0.0, 0.5, 0.75, 0.0, 0.04, 0.0, 0.75, 0.45, 0.42, 0.25, 0.0, 0.0]
    nseg = [0, 2, 4, 0, 1, 0, 4, 2, 3, 2, 0, 0]
    return round_corners(pts, radii, nseg)


HUB_PROFILE = None


def hub_profile():
    """chrome disc cross-section (r, y): fat outer lip, dished floor, centre boss.
    Mirrored across r = 0 so the axis is interior."""
    half = [(6.95, -1.0), (6.95, 2.42), (6.55, 2.72), (5.95, 2.62), (5.55, 1.62),
            (3.05, 1.42), (2.55, 1.85), (1.75, 2.55)]
    radii = [0.2, 0.25, 0.3, 0.3, 0.45, 0.45, 0.35, 0.45]
    nseg = [1, 3, 4, 3, 3, 3, 3, 4]
    pts = [(0.0, -1.0)] + half + [(0.0, 2.55)] + [(-r, y) for (r, y) in half[::-1]]
    rr = [0] + radii + [0] + radii[::-1]
    ns = [0] + nseg + [0] + nseg[::-1]
    return round_corners(pts, rr, ns)


def hub_sdf(x, y, z):
    global HUB_PROFILE
    if HUB_PROFILE is None:
        HUB_PROFILE = hub_profile()
    r = np.hypot(x, z)
    d = sd_poly(r, y, HUB_PROFILE)
    # eight thick swept fan vanes standing on the dished floor, tops flush with the lip
    phi = np.arctan2(z, x)
    k = 0.30                                          # spiral sweep (rad per uu)
    per = 2 * np.pi / N_VANES
    a = np.mod(phi - k * (r - 2.6) + 0.5 * per, per) - 0.5 * per
    cospsi = 1.0 / np.sqrt(1.0 + (k * r) ** 2)
    half_w = 0.30 + 0.10 * np.clip((r - 2.6) / 3.4, 0, 1)        # thicker toward the rim
    d_ang = np.abs(r * a) * cospsi - half_w
    d_rad = np.maximum(2.35 - r, r - 6.2)
    ytop = 2.38 + 0.12 * np.clip((r - 2.6) / 3.4, 0, 1)
    vane = i_round(np.maximum(d_ang, d_rad), np.maximum(y - ytop, 1.0 - y), 0.2)
    d = u_round(d, vane, 0.22)
    # centre hole: the steel axle's peened head (part of the car body) sits in it
    hole = np.hypot(x, z) - 0.95
    d = s_round(d, hole, 0.15)
    return d


def build_wheel(name=MESH_NAME, coll=None, quick=False, mat_kw=None):
    t0 = time.time()
    P = tyre_profile()
    Nr = profile_normals(P)
    Vt, Tt, Nt = revolve(P, Nr, TYRE_SEGMENTS)
    cell = 0.11 if quick else 0.07
    Vh, Th, Nh = sdf_part("W02_Hub", hub_sdf, (-7.3, -1.3, -7.3), (7.3, 3.1, 7.3), cell,
                          target_tris=2500, symmetric=False, normal_eps=0.01, planar_deg=0.4)
    parts = [dict(V=Vt, T=Tt, N=Nt, mat=0), dict(V=Vh, T=Th, N=Nh, mat=1)]
    ob = build_object(name, parts, ["Tire", "Hub"], coll, mat_kw)
    log("wheel built: %d tris (tyre %d, hub %d) in %.1fs" % (tri_count(ob), len(Tt), len(Th), time.time() - t0))
    return ob


def wheel_uvs(ob):
    smart_uv(ob, "UV0", angle=60.0, margin=0.004)
    me = ob.data
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3) / UU
    li = np.empty(len(me.loops), np.int64); me.loops.foreach_get("vertex_index", li)
    p = co[li]
    s = 0.5 / (WHEEL_RADIUS_UU * 1.02)
    u = 0.5 + p[:, 0] * s; v = 0.5 + p[:, 2] * s
    uv = me.uv_layers.new(name="UV1")
    uv.data.foreach_set("uv", np.stack([u, v], 1).ravel())
    me.uv_layers.active = me.uv_layers["UV0"]


def wheel_sidecar(ob, path):
    data = {
        "wheel_design": "W02_Fan",
        "mesh": MESH_NAME,
        "description": "Era one-piece toy wheel (spec 4b rule 3): narrow hard black plastic ring (smooth tread, "
                       "faint mould line, no rubber sidewall) moulded round a vacuum-chromed fan disc "
                       "(8 thick swept vanes, fat outer lip, centre boss with a through hole for the axle head).",
        "radius": WHEEL_RADIUS_UU,
        "width": WHEEL_WIDTH_UU,
        "units": "uu (1 uu = 1/16 real cm); FBX authored in Blender metres, 1 m = 100 uu",
        "origin": "wheel centre",
        "axle_axis": "Y",
        "hub_face_y": HUB_FACE_Y,
        "outer_face": "Blender +Y = left side of the car. After the FBX import that is UE -Y (left). Use as-is on the "
                      "LEFT wheels (FL, RL); rotate 180 deg yaw for the RIGHT wheels (FR, RR). The vanes are swept, "
                      "a yaw (not a mirror) keeps them correct.",
        "spin_axis_ue": "Y",
        "slots": ["Tire", "Hub"],
        "tris": tri_count(ob),
        "normals": "authored (analytic). Import normals, do not recompute.",
        "toy_imperfection": "give each wheel a fixed random camber/toe of up to +/-0.5 deg (the cars' sidecars list the preview values)",
        "uv": {"UV0": "smart unwrap, non-overlapping",
               "UV1": "planar side projection (hub face centred at 0.5,0.5)"},
        "native_for": ["Vortex"],
        "bbox_uu_blender_axes": bbox_uu(ob),
        "scale_note": "If another casting needs a different radius, scale uniformly by radius/%.1f." % WHEEL_RADIUS_UU,
        "source": "SourceArt/Blender/Wheel_W02_Fan/build_Wheel_W02_Fan.py",
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log("sidecar", os.path.basename(path))


def main(quick=False, norender=False):
    sc = reset_scene()
    for s in ("Tire", "Hub"):
        make_slot_material(s)
    coll = get_coll("Wheel")
    ob = build_wheel(coll=coll, quick=quick)
    wheel_uvs(ob)
    export_fbx(ob, os.path.join(HERE, "export", MESH_NAME + ".fbx"))
    wheel_sidecar(ob, os.path.join(HERE, ASSET + ".json"))
    if norender:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"), compress=True)
        return
    STAGE_OPT['samples'] = 32 if quick else 96
    STAGE_OPT['pct'] = 50 if quick else 100
    setup_render(sc)
    rig = setup_stage(sc)
    # the wheel standing on the deck, show face toward the camera (Navvy's wheel-close numbers)
    ob.location = (0.0, 0.0, WHEEL_RADIUS_UU * UU)
    ob.rotation_euler = (0.0, 0.0, math.radians(-12.0))
    wc = (0.0, 0.0, WHEEL_RADIUS_UU * UU)
    shots = {
        "W02_Fan_34": dict(az=62.0, el=12.0, dist=1.7, lens=100, target=wc, focus=(0.0, 0.03, wc[2]),
                           fstop=2.2, sun=(80.0, 28.0)),
        "W02_Fan_face": dict(az=82.0, el=4.0, dist=1.6, lens=100, target=wc, focus=(0.0, 0.03, wc[2]),
                             fstop=4.0, sun=(60.0, 30.0)),
    }
    for nm, cfg in shots.items():
        render_shot(sc, rig, os.path.join(HERE, "preview", nm + ".png"), cfg)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"), compress=True)
    log("saved", ASSET + ".blend")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(quick="--quick" in argv, norender="--norender" in argv)
