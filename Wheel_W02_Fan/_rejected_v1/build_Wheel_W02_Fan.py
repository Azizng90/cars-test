"""
build_Wheel_W02_Fan.py  -  MODEL '93 / CozyCarGame, Slice 1A
=================================================================
Builds the shared toy wheel design W02_Fan (chrome fan/turbine disc, hard black plastic
tyre) from an empty scene, saves Wheel_W02_Fan.blend, exports SM_Wheel_W02_Fan.fbx and the
JSON sidecar, and renders look-dev previews.

Run headless:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup
      --python build_Wheel_W02_Fan.py [-- --quick] [-- --norender]

Conventions (Docs/Build/SLICE_1A_BUILD_SPEC.md):
  * game scale in Blender metres: 1 uu = 0.01 m (real cm x 16)
  * origin = wheel centre, axle along Y, the OUTER (show) face points +Y (Blender left)
  * slots: Tire, Hub
This file is also the shared TOOLKIT for build_Vortex.py (SDF ops, surface-nets mesher,
mesh/normal helpers, stand-in slot materials and the macro PREVIEW RIG), so keep the API
stable. Parts of the SDF toolkit follow the same recipe as build_HatchlingS.py so the
castings share one modelling language (rounded die-cast fillets everywhere).
"""
import bpy, bmesh, math, os, sys, json, time
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = "Wheel_W02_Fan"
MESH_NAME = "SM_Wheel_W02_Fan"
UU = 0.01                       # Blender metres per uu
WHEEL_RADIUS_UU = 9.6
WHEEL_WIDTH_UU = 8.0
TYRE_SEGMENTS = 48
N_VANES = 10
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
    """Spec section 2 export settings, one part per file."""
    set_active(ob)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True,
                             apply_scale_options='FBX_SCALE_UNITS', axis_forward='X', axis_up='Z',
                             bake_space_transform=True, mesh_smooth_type='FACE', use_tspace=True,
                             add_leaf_bones=False, use_mesh_modifiers=True, object_types={'MESH'},
                             use_custom_props=False, path_mode='STRIP')
    log("exported", os.path.basename(path))


def bbox_uu(ob):
    co = np.empty(len(ob.data.vertices) * 3)
    ob.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3) / UU
    return [round(float(v), 2) for v in (co[:, 0].min(), co[:, 0].max(), co[:, 1].min(), co[:, 1].max(),
                                          co[:, 2].min(), co[:, 2].max())]


# =============================================================================
#  SDF toolkit (uu).  Rounded union / intersection after hg_sdf (exact radius for
#  perpendicular surfaces) = the "cast zinc" fillet language of every part.
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


def feature_weights(V, Q, N):
    """0..1 per vertex: how much the analytic normal turns across the 1-ring (creases,
    grooves, fillets get 1, flat panels 0). Drives the decimator's vertex group."""
    mind = np.ones(len(V))
    for i in range(Q.shape[1]):
        a = Q[:, i]; b = Q[:, (i + 1) % Q.shape[1]]
        d = (N[a] * N[b]).sum(1)
        np.minimum.at(mind, a, d); np.minimum.at(mind, b, d)
    return np.clip((1.0 - mind) / 0.06, 0.0, 1.0)


def corner_normals(fn, V, T, N, eps=0.02, cos_bad=math.cos(math.radians(24.0)), shift=0.45):
    """Per-corner normals. Analytic vertex normals everywhere, except where a vertex normal
    disagrees with its (decimated) face: then sample the SDF gradient a little way inside
    the face, so a big flat triangle touching a groove lip stays flat instead of streaking."""
    P = V[T]                                       # (nT,3,3)
    fn_ = _unit(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]))
    NC = N[T].copy()
    dots = (NC * fn_[:, None, :]).sum(2)
    bad = dots < cos_bad
    nb = int(bad.sum())
    if nb:
        C = P.mean(1)                                 # (nT,3)
        ti, ci = np.nonzero(bad)
        pv = P[ti, ci]; dv = C[ti] - pv
        ln = np.linalg.norm(dv, axis=1)
        st = np.minimum(shift, 0.45 * ln)
        q = pv + dv / np.maximum(ln, 1e-9)[:, None] * st[:, None]
        g = _unit(sdf_grad(fn, q, eps=eps))
        # still far off the face (strongly curved big face): blend toward the face normal
        d2 = (g * fn_[ti]).sum(1)
        far = d2 < cos_bad
        g[far] = _unit(g[far] + fn_[ti][far])
        NC[ti, ci] = g
    return NC, nb


def sdf_part(name, fn, bmin, bmax, cell, target_tris, symmetric=True, normal_eps=0.02, protect=8.0):
    """SDF -> surface nets -> project -> feature-weighted decimate -> reproject -> analytic
    per-corner normals. Returns (V uu, T, NC per-corner normals (nT,3,3))."""
    t0 = time.time()
    V, Q = surface_nets(fn, bmin, bmax, cell)
    V = project(fn, V, iters=2, maxstep=cell)
    me = mesh_from_numpy(name + "_tmp", V * UU, Q)
    ob = bpy.data.objects.new(name + "_tmp", me)
    bpy.context.scene.collection.objects.link(ob)
    ntri = 2 * len(Q)
    if target_tris < ntri:
        md = ob.modifiers.new("Dec", 'DECIMATE')
        md.decimate_type = 'COLLAPSE'
        md.ratio = min(1.0, target_tris / max(ntri, 1))
        md.use_collapse_triangulate = True
        if symmetric:
            md.use_symmetry = True
            md.symmetry_axis = 'Y'
        if protect > 0:
            N0 = _unit(sdf_grad(fn, V, eps=normal_eps))
            wts = feature_weights(V, Q, N0)
            vg = ob.vertex_groups.new(name="feat")
            idx = np.nonzero(wts > 0.02)[0]
            # add() per distinct weight bucket (fast enough: 11 calls)
            buckets = np.round(wts[idx] * 10) / 10
            for bv in np.unique(buckets):
                sel = idx[buckets == bv]
                vg.add(sel.tolist(), float(max(bv, 0.05)), 'REPLACE')
            md.vertex_group = "feat"
            md.vertex_group_factor = protect
        apply_modifiers(ob)
    V2, T = mesh_arrays(ob.data)
    V2 = V2 / UU
    V2 = project(fn, V2, iters=1, maxstep=0.1)
    N = _unit(sdf_grad(fn, V2, eps=normal_eps))
    NC, nb = corner_normals(fn, V2, T, N, eps=normal_eps)
    me2 = ob.data
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me2)
    log("  part %-16s %8d -> %6d tris, %d corners re-aimed (%.1fs)" % (name, ntri, len(T), nb, time.time() - t0))
    return V2, T, NC


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
    # make winding agree with the normals
    e1 = V[T[:, 1]] - V[T[:, 0]]; e2 = V[T[:, 2]] - V[T[:, 0]]
    fn = np.cross(e1, e2); nn = N[T[:, 0]] + N[T[:, 1]] + N[T[:, 2]]
    bad = (fn * nn).sum(1) < 0
    T[bad] = T[bad][:, ::-1]
    return V, T, N


def fix_winding(V, T, N):
    e1 = V[T[:, 1]] - V[T[:, 0]]; e2 = V[T[:, 2]] - V[T[:, 0]]
    fn = np.cross(e1, e2); nn = N[T[:, 0]] + N[T[:, 1]] + N[T[:, 2]]
    bad = (fn * nn).sum(1) < 0
    T = T.copy(); T[bad] = T[bad][:, ::-1]
    return T


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
        # loops are laid out triangle by triangle, corner order == T order
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


def _flake_normal(nt, bs, scale=2600.0, strength=0.08):
    """fine metal-flake sparkle under the clear coat (game scale: 1 m = 100 uu)"""
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-900, -300)
    vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.location = (-700, -300)
    vor.inputs['Scale'].default_value = scale
    try:
        vor.feature = 'F1'
    except Exception:
        pass
    nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.location = (-450, -300)
    bump.inputs['Strength'].default_value = strength
    bump.inputs['Distance'].default_value = 0.0004
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bs.inputs['Normal'])


def make_slot_material(slot, **kw):
    """Simple Principled stand-ins named exactly like the UE slots."""
    m, nt, bs = _principled(slot)
    if slot == "Paint":            # candy over metallic flake, glossy clear coat
        col = kw.get("paint", (0.50, 0.010, 0.016, 1))
        _set(bs, 'Base Color', col); _set(bs, 'Metallic', 0.9); _set(bs, 'Roughness', 0.32)
        _set(bs, 'Coat Weight', 1.0); _set(bs, 'Coat Roughness', 0.03); _set(bs, 'Coat IOR', 1.55)
        _set(bs, 'Coat Tint', kw.get("coat_tint", (1.0, 0.42, 0.40, 1)))
        _flake_normal(nt, bs)
        m.diffuse_color = col
    elif slot in ("Chrome", "Hub"):
        _set(bs, 'Base Color', (0.93, 0.93, 0.95, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.05)
        m.diffuse_color = (0.9, 0.9, 0.9, 1)
    elif slot == "Zamac":          # bare zinc alloy #9C9A94 / steel axles
        _set(bs, 'Base Color', (0.36, 0.35, 0.33, 1)); _set(bs, 'Metallic', 1.0); _set(bs, 'Roughness', 0.24)
    elif slot == "Lamp":           # clear lens tinted by the 'Col' vertex colour (tail lamps red)
        attr = nt.nodes.new('ShaderNodeVertexColor'); attr.location = (-400, 0)
        try:
            attr.layer_name = "Col"
        except Exception:
            pass
        _set(bs, 'Metallic', 0.0); _set(bs, 'Roughness', 0.05); _set(bs, 'IOR', 1.5)
        _set(bs, 'Transmission Weight', 0.55)
        nt.links.new(attr.outputs['Color'], bs.inputs['Base Color'])
        # a little self-glow so the lenses read as lamps in shadow
        if 'Emission Color' in bs.inputs:
            nt.links.new(attr.outputs['Color'], bs.inputs['Emission Color'])
        _set(bs, 'Emission Strength', 0.15)
    elif slot == "Glass":
        _set(bs, 'Base Color', kw.get("glass", (0.30, 0.36, 0.40, 1))); _set(bs, 'Metallic', 0.0)
        _set(bs, 'Roughness', 0.02)
        _set(bs, 'IOR', 1.49); _set(bs, 'Transmission Weight', 1.0)
        m.diffuse_color = (0.3, 0.35, 0.4, 0.4)
    elif slot == "Interior":
        _set(bs, 'Base Color', kw.get("interior", (0.30, 0.29, 0.27, 1))); _set(bs, 'Roughness', 0.62)
        _set(bs, 'Specular IOR Level', 0.35)
    elif slot == "Base":           # black satin plastic chassis
        _set(bs, 'Base Color', kw.get("base", (0.022, 0.022, 0.024, 1))); _set(bs, 'Roughness', 0.42)
        _set(bs, 'Specular IOR Level', 0.5)
    elif slot == "Tire":           # hard black toy plastic, a little glossy
        _set(bs, 'Base Color', (0.014, 0.014, 0.015, 1)); _set(bs, 'Roughness', 0.36)
        _set(bs, 'Specular IOR Level', 0.5)
    return m


# =============================================================================
#  Shared PREVIEW RIG  (sunlit deck boards, HDRI + sun, macro camera)
# =============================================================================
def setup_render(scene, samples=96, res=(1600, 1200)):
    scene.render.engine = 'CYCLES'
    cprefs = bpy.context.preferences.addons['cycles'].preferences
    dev = 'CPU'
    for t in ('OPTIX', 'CUDA'):
        try:
            cprefs.compute_device_type = t
            cprefs.refresh_devices()
            gpus = [d for d in cprefs.devices if d.type == t]
            if gpus:
                for d in cprefs.devices:
                    d.use = (d.type == t)
                dev = t
                break
        except Exception as e:
            log("GPU init", t, "failed:", e)
    scene.cycles.device = 'GPU' if dev != 'CPU' else 'CPU'
    log("render device:", dev)
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = 'OPTIX' if dev == 'OPTIX' else 'OPENIMAGEDENOISE'
    except Exception:
        pass
    scene.cycles.max_bounces = 12
    scene.cycles.glossy_bounces = 8
    scene.cycles.transmission_bounces = 12
    scene.cycles.transparent_max_bounces = 12
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.blur_glossy = 0.5
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    try:
        scene.view_settings.view_transform = 'AgX'
    except Exception:
        scene.view_settings.view_transform = 'Filmic'
    for look in ('AgX - Medium High Contrast', 'Medium High Contrast', 'AgX - Base Contrast', 'None'):
        try:
            scene.view_settings.look = look
            break
        except Exception:
            continue
    scene.view_settings.exposure = 0.0
    return dev


def hdri_sun_azimuth(path):
    """Azimuth (deg, Blender world, 0 = +X, CCW) of the brightest pixel of an equirect HDRI."""
    img = bpy.data.images.load(path, check_existing=True)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    lum = px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722
    r, c = np.unravel_index(int(np.argmax(lum)), lum.shape)
    u = (c + 0.5) / w
    ang = (u - 0.5) * 2 * math.pi
    dx, dy = -math.cos(ang), math.sin(ang)
    return math.degrees(math.atan2(dy, dx)), img


def setup_world(scene, hdri="courtyard.exr", strength=0.6, sun_az=120.0, bg_strength=None):
    w = bpy.data.worlds.new("PreviewWorld")
    scene.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    nt = w.node_tree
    nt.nodes.clear()
    path = os.path.join(BLENDER_HDRI_DIR, hdri)
    az_img, img = hdri_sun_azimuth(path)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = img
    bg = nt.nodes.new('ShaderNodeBackground')
    out = nt.nodes.new('ShaderNodeOutputWorld')
    mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(az_img - sun_az))
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    nt.links.new(env.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    if bg_strength is not None:
        lp = nt.nodes.new('ShaderNodeLightPath')
        bg2 = nt.nodes.new('ShaderNodeBackground')
        nt.links.new(env.outputs['Color'], bg2.inputs['Color'])
        bg2.inputs['Strength'].default_value = bg_strength
        mix = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs['Fac'])
        nt.links.new(bg.outputs[0], mix.inputs[1])
        nt.links.new(bg2.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs['Surface'])
    else:
        nt.links.new(bg.outputs[0], out.inputs['Surface'])
    w["sun_az"] = sun_az
    return w


def set_world_rotation(scene, sun_az):
    """re-aim the HDRI's own sun at a new azimuth (keeps one world for every shot)"""
    w = scene.world
    nt = w.node_tree
    env = [n for n in nt.nodes if n.type == 'TEX_ENVIRONMENT'][0]
    mp = [n for n in nt.nodes if n.type == 'MAPPING'][0]
    if "az_img" not in w:
        w["az_img"], _ = hdri_sun_azimuth(env.image.filepath)
    mp.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(w["az_img"] - sun_az))


def add_sun(scene, az_deg=120.0, el_deg=30.0, strength=4.5, color=(1.0, 0.84, 0.66), angle_deg=1.0):
    ld = bpy.data.lights.new("PreviewSun", 'SUN')
    ld.energy = strength
    ld.color = color
    ld.angle = math.radians(angle_deg)
    ob = bpy.data.objects.new("PreviewSun", ld)
    link(ob, get_coll("Preview"))
    aim_sun(ob, az_deg, el_deg)
    return ob


def aim_sun(ob, az_deg, el_deg):
    az, el = math.radians(az_deg), math.radians(el_deg)
    s = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    ob.rotation_euler = s.to_track_quat('Z', 'Y').to_euler()


def make_wood_material(name="PV_Wood"):
    """Sun-warmed, lightly weathered deck board (procedural). Object coords in Blender m
    (1 m = 6.25 cm real): growth rings ~3-5 mm real apart, cathedral grain wandering along X
    (boards run along X), streaky fibres, raised latewood, per-board tone."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new; L = nt.links.new

    def mth(op, a=None, b=None, va=None, vb=None, c=None, vc=None):
        n = N('ShaderNodeMath'); n.operation = op
        for i, (s, v) in enumerate(((a, va), (b, vb), (c, vc))):
            if s is not None:
                L(s, n.inputs[i])
            elif v is not None:
                n.inputs[i].default_value = v
        return n.outputs[0]

    def noise(vec, scale, detail=3.0, rough=0.5, dist=0.0):
        n = N('ShaderNodeTexNoise')
        n.inputs['Scale'].default_value = scale
        n.inputs['Detail'].default_value = detail
        n.inputs['Roughness'].default_value = rough
        if 'Distortion' in n.inputs:
            n.inputs['Distortion'].default_value = dist
        L(vec, n.inputs['Vector'])
        return n.outputs['Fac']

    def mapping(vec, scale, loc=(0, 0, 0)):
        mp = N('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = scale
        mp.inputs['Location'].default_value = loc
        L(vec, mp.inputs['Vector'])
        return mp.outputs['Vector']

    out = N('ShaderNodeOutputMaterial')
    bs = N('ShaderNodeBsdfPrincipled')
    tc = N('ShaderNodeTexCoord')
    oi = N('ShaderNodeObjectInfo')
    rnd = oi.outputs['Random']
    rv = N('ShaderNodeCombineXYZ')
    L(mth('MULTIPLY', rnd, vb=173.0), rv.inputs[0]); L(mth('MULTIPLY', rnd, vb=29.0), rv.inputs[2])
    off = N('ShaderNodeVectorMath'); off.operation = 'ADD'
    L(tc.outputs['Object'], off.inputs[0]); L(rv.outputs[0], off.inputs[1])
    P = off.outputs[0]
    sep = N('ShaderNodeSeparateXYZ'); L(P, sep.inputs[0])
    py = sep.outputs['Y']
    # cathedral wander: slow along X, a little across Y
    w1 = noise(mapping(P, (0.10, 0.55, 1.0)), 1.0, detail=2.0, rough=0.5)
    w2 = noise(mapping(P, (0.45, 2.2, 1.0)), 1.0, detail=3.0, rough=0.55)
    wander = mth('ADD', mth('MULTIPLY', mth('SUBTRACT', w1, vb=0.5), vb=0.95),
                 mth('MULTIPLY', mth('SUBTRACT', w2, vb=0.5), vb=0.16))
    # ring phase: ~0.06 m (4 mm real) per ring
    sp = noise(mapping(P, (0.04, 0.9, 1.0)), 1.0, detail=2.0)          # uneven ring spacing
    phase = mth('ADD', mth('MULTIPLY', mth('ADD', py, wander), vb=15.0), mth('MULTIPLY', sp, vb=7.0))
    v = mth('FRACT', phase)
    late = mth('POWER', v, vb=4.0)                       # gradual dark-up then a sharp reset
    # fibre streaks (very stretched)
    fib = noise(mapping(P, (0.010, 1.0, 1.0)), 48.0, detail=5.0, rough=0.66)
    fib2 = noise(mapping(P, (0.03, 1.0, 1.0)), 260.0, detail=2.0, rough=0.5)
    # weathering / colour patches
    big = noise(P, 0.35, detail=3.0, rough=0.55)
    stain = noise(mapping(P, (0.05, 1.0, 1.0)), 6.0, detail=2.0)
    # ---- colour ----------------------------------------------------------
    ramp = N('ShaderNodeValToRGB')
    el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0.56, 0.34, 0.135, 1)       # earlywood (honey)
    el[1].position = 1.0; el[1].color = (0.19, 0.088, 0.026, 1)      # latewood
    e2 = ramp.color_ramp.elements.new(0.5); e2.color = (0.40, 0.215, 0.075, 1)
    gval = mth('ADD', mth('MULTIPLY', late, vb=0.80),
               mth('MULTIPLY', mth('SUBTRACT', fib, vb=0.5), vb=0.95))
    gval = mth('ADD', gval, mth('MULTIPLY', mth('SUBTRACT', stain, vb=0.5), vb=0.35))
    gcl = mth('MINIMUM', mth('MAXIMUM', gval, vb=0.0), vb=1.0)
    L(gcl, ramp.inputs['Fac'])
    col = ramp.outputs['Color']
    # fine fibre value jitter
    jit = N('ShaderNodeMix'); jit.data_type = 'RGBA'; jit.blend_type = 'MULTIPLY'
    jit.inputs['Factor'].default_value = 1.0
    L(col, jit.inputs['A'])
    fj = N('ShaderNodeMapRange'); fj.inputs['To Min'].default_value = 0.82; fj.inputs['To Max'].default_value = 1.12
    L(fib2, fj.inputs['Value'])
    fjc = N('ShaderNodeCombineColor'); L(fj.outputs['Result'], fjc.inputs[0]); L(fj.outputs['Result'], fjc.inputs[1]); L(fj.outputs['Result'], fjc.inputs[2])
    L(fjc.outputs[0], jit.inputs['B'])
    # sun-bleached grey-brown patches
    wmix = N('ShaderNodeMix'); wmix.data_type = 'RGBA'
    wmix.inputs['B'].default_value = (0.30, 0.235, 0.16, 1)
    wf = N('ShaderNodeMapRange')
    wf.inputs['From Min'].default_value = 0.42; wf.inputs['From Max'].default_value = 0.75
    wf.inputs['To Min'].default_value = 0.0; wf.inputs['To Max'].default_value = 0.45
    L(big, wf.inputs['Value']); L(wf.outputs['Result'], wmix.inputs['Factor'])
    L(jit.outputs['Result'], wmix.inputs['A'])
    # per-board tone
    hsv = N('ShaderNodeHueSaturation')
    rb = N('ShaderNodeMapRange'); rb.inputs['To Min'].default_value = 0.80; rb.inputs['To Max'].default_value = 1.10
    L(rnd, rb.inputs['Value']); L(rb.outputs['Result'], hsv.inputs['Value'])
    rh = N('ShaderNodeMapRange'); rh.inputs['To Min'].default_value = 0.485; rh.inputs['To Max'].default_value = 0.515
    L(rnd, rh.inputs['Value']); L(rh.outputs['Result'], hsv.inputs['Hue'])
    L(wmix.outputs['Result'], hsv.inputs['Color'])
    L(hsv.outputs['Color'], bs.inputs['Base Color'])
    # ---- roughness / bump ----------------------------------------------------
    rr = N('ShaderNodeMapRange')
    rr.inputs['To Min'].default_value = 0.86; rr.inputs['To Max'].default_value = 0.70
    L(late, rr.inputs['Value'])
    L(rr.outputs['Result'], bs.inputs['Roughness'])
    _set(bs, 'Specular IOR Level', 0.25)
    h = mth('ADD', mth('MULTIPLY', late, vb=1.0), mth('MULTIPLY', fib, vb=0.45))
    h = mth('ADD', h, mth('MULTIPLY', fib2, vb=0.25))
    bump = N('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.13
    bump.inputs['Distance'].default_value = 0.005
    L(h, bump.inputs['Height'])
    L(bump.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface'])
    return m


def make_box(name, center, half, coll=None, mat=None, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * half[0] + center[0], v.co.y * half[1] + center[1], v.co.z * half[2] + center[2]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    link(ob, coll)
    if mat:
        me.materials.append(mat)
    if bevel > 0:
        md = ob.modifiers.new("Bevel", 'BEVEL'); md.width = bevel; md.segments = 6
        md.limit_method = 'ANGLE'
    for p in me.polygons:
        p.use_smooth = True
    return ob


def make_deck(y_shift=0.0, n=5, length=60.0):
    """Deck boards at game scale (Blender m): 14 cm real wide = 2.24 m, gap 6 mm = 0.096 m,
    2.4 cm thick = 0.384 m, running along X. Top surface at z = 0."""
    coll = get_coll("Preview")
    mat = make_wood_material()
    bw, gap, th = 2.24, 0.096, 0.384
    pitch = bw + gap
    obs = []
    for i in range(n):
        yc = (i - n // 2) * pitch + y_shift
        ob = make_box("PV_Board_%d" % i, (0, yc, -th / 2), (length / 2, bw / 2, th / 2), coll, mat, bevel=0.05)
        obs.append(ob)
    dark = bpy.data.materials.new("PV_Under")
    dark.diffuse_color = (0.01, 0.008, 0.006, 1)
    m, nt, bs = _principled("PV_Under")
    _set(bs, 'Base Color', (0.012, 0.009, 0.007, 1)); _set(bs, 'Roughness', 0.9)
    make_box("PV_UnderDeck", (0, y_shift, -1.2), (length / 2, n * pitch / 2 + 2, 0.05), coll, m)
    return obs


def make_camera(name, target, az_deg, el_deg, dist, focal_mm=100.0, fstop=2.8, focus=None, shift=(0, 0), roll=0.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = focal_mm
    cd.sensor_width = 36.0
    cd.sensor_fit = 'HORIZONTAL'
    cd.clip_start = 0.05
    cd.clip_end = 1000.0
    cd.shift_x, cd.shift_y = shift
    ob = bpy.data.objects.new(name, cd)
    link(ob, get_coll("Preview"))
    t = Vector(target)
    az, el = math.radians(az_deg), math.radians(el_deg)
    d = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    ob.location = t + d * dist
    if abs(el_deg) > 89.0:
        # straight down; image up = -Y... rotate so the car's front (+X) points to image right
        ob.rotation_euler = Euler((0.0, 0.0, math.radians(roll)))
    else:
        q = (t - ob.location).to_track_quat('-Z', 'Y')
        if roll:
            q = q @ Euler((0, 0, math.radians(roll))).to_quaternion()
        ob.rotation_euler = q.to_euler()
    cd.dof.use_dof = fstop is not None
    if fstop is not None:
        cd.dof.aperture_fstop = fstop
        fp = Vector(focus) if focus is not None else t
        cd.dof.focus_distance = (fp - ob.location).length
    return ob


def render_view(scene, cam, path):
    scene.camera = cam
    scene.render.filepath = path
    t0 = time.time()
    try:
        bpy.ops.render.render(write_still=True)
    except Exception as e:
        log("GPU render failed (%s); retrying on CPU" % e)
        scene.cycles.device = 'CPU'
        bpy.ops.render.render(write_still=True)
    log("rendered %s in %.1fs" % (os.path.basename(path), time.time() - t0))


# =============================================================================
#  The wheel  (wheel-local uu: origin at the centre, axle along Y, show face +Y)
# =============================================================================
def tyre_profile():
    """Closed tyre cross-section in (r, y), rounded where it shows."""
    R, H = WHEEL_RADIUS_UU, WHEEL_WIDTH_UU / 2.0       # 9.6, 4.0
    g1, g2, gd, gw = -1.35, 1.35, 0.32, 0.26            # two thin tread rings
    pts = [
        (6.45, -3.55),          # bore, back (hidden)
        (7.9, -H),              # back sidewall
        (R, -H + 0.95),         # back shoulder
        (R, g1 - gw), (R - gd, g1), (R, g1 + gw),
        (R, g2 - gw), (R - gd, g2), (R, g2 + gw),
        (R, H - 0.95),          # front shoulder
        (8.15, H),              # front sidewall (slightly crowned via the radius)
        (6.95, H - 0.05),       # tyre lip around the chrome face
        (6.55, H - 0.55),       # lip turn-in
        (6.45, H - 1.2),        # bore, front (behind the hub lip)
    ]
    radii = [0.0, 0.7, 1.15, 0.0, 0.12, 0.0, 0.0, 0.12, 0.0, 1.15, 0.7, 0.4, 0.25, 0.0]
    nseg = [0, 2, 4, 0, 1, 0, 0, 1, 0, 4, 2, 2, 1, 0]
    return round_corners(pts, radii, nseg)


def profile_normals(P):
    """outward vertex normals of a closed 2D polyline (r, y)"""
    n = len(P)
    area = 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    E = np.roll(P, -1, axis=0) - P                # edge i: P[i] -> P[i+1]
    En = np.stack([E[:, 1], -E[:, 0]], 1)         # right-hand normal
    if area < 0:
        En = -En
    En /= np.maximum(np.linalg.norm(En, axis=1), 1e-12)[:, None]
    Nv = En + np.roll(En, 1, axis=0)
    Nv /= np.maximum(np.linalg.norm(Nv, axis=1), 1e-12)[:, None]
    return Nv


def revolve(P, Nr, seg):
    """revolve a closed (r, y) profile around the Y axis; returns V, T, N (uu)."""
    m = len(P)
    th = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    V = np.zeros((m * seg, 3)); N = np.zeros((m * seg, 3))
    for i in range(m):
        V[i * seg:(i + 1) * seg] = np.stack([P[i, 0] * c, np.full(seg, P[i, 1]), P[i, 0] * s], 1)
        N[i * seg:(i + 1) * seg] = np.stack([Nr[i, 0] * c, np.full(seg, Nr[i, 1]), Nr[i, 0] * s], 1)
    T = []
    for i in range(m):
        i2 = (i + 1) % m
        for j in range(seg):
            j2 = (j + 1) % seg
            a, b, cc, d = i * seg + j, i2 * seg + j, i2 * seg + j2, i * seg + j2
            T.append((a, b, cc)); T.append((a, cc, d))
    T = np.array(T)
    return V, fix_winding(V, T, N), N


HUB_PROFILE = None


def hub_profile():
    """chrome disc cross-section (r, y): outer lip, dished floor, centre boss.
    Mirrored across r = 0 so the axis is interior (no fake axis edge in the SDF)."""
    half = [(6.75, -3.0), (6.75, 3.15), (6.25, 3.72), (5.75, 3.60), (5.45, 2.70),
            (2.75, 2.55), (2.35, 3.05), (1.55, 3.70)]
    radii = [0.2, 0.25, 0.32, 0.25, 0.3, 0.35, 0.3, 0.5]
    nseg = [1, 3, 4, 3, 3, 3, 3, 4]
    pts = [(-0.0, -3.0)] + half + [(0.0, 3.86)] + [(-r, y) for (r, y) in half[::-1]]
    rr = [0] + radii + [0] + radii[::-1]
    ns = [0] + nseg + [0] + nseg[::-1]
    # drop the duplicated axis points (keep (0,3.86) as the apex; the base point closes the loop)
    return round_corners(pts, rr, ns)


def hub_sdf(x, y, z):
    global HUB_PROFILE
    if HUB_PROFILE is None:
        HUB_PROFILE = hub_profile()
    r = np.hypot(x, z)
    # revolved profile: mirror the profile across r = 0 so the axis is interior
    d = sd_poly(r, y, HUB_PROFILE)
    # ten curved turbine vanes on the dished floor
    phi = np.arctan2(z, x)
    k = 0.34                                          # spiral sweep (rad per uu)
    per = 2 * np.pi / N_VANES
    a = np.mod(phi - k * (r - 2.4) + 0.5 * per, per) - 0.5 * per
    cospsi = 1.0 / np.sqrt(1.0 + (k * r) ** 2)
    d_ang = np.abs(r * a) * cospsi - 0.27
    d_rad = np.maximum(2.25 - r, r - 5.75)
    ytop = 3.30 + 0.16 * np.clip((r - 2.3) / 3.4, 0, 1)
    d_y = y - ytop
    vane = i_round(np.maximum(d_ang, d_rad), np.maximum(d_y, 1.9 - y), 0.14)
    d = u_round(d, vane, 0.16)
    # peened axle head: a small dimpled dome on the boss
    head = sd_ellipsoid(x, y, z, (0.0, 3.86, 0.0), (0.95, 0.42, 0.95))
    d = u_round(d, head, 0.12)
    dimple = np.sqrt(x * x + (y - 4.62) ** 2 + z * z) - 0.5
    d = s_round(d, dimple, 0.06)
    # axle hole on the back (so a steel axle can enter)
    hole = np.maximum(np.hypot(x, z) - 0.85, y - 1.5)
    d = np.maximum(d, -hole)
    return d


def build_wheel(name=MESH_NAME, coll=None, quick=False, mat_kw=None):
    t0 = time.time()
    P = tyre_profile()
    Nr = profile_normals(P)
    Vt, Tt, Nt = revolve(P, Nr, TYRE_SEGMENTS)
    cell = 0.12 if quick else 0.075
    Vh, Th, Nh = sdf_part("W02_Hub", hub_sdf, (-7.0, -3.3, -7.0), (7.0, 4.7, 7.0), cell,
                          target_tris=2700, symmetric=False, normal_eps=0.01)
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
        "description": "Chrome fan/turbine disc: raised outer lip, dished floor with 10 swept vanes, "
                       "centre boss with a peened axle head; hard black plastic low-profile tyre with two tread rings.",
        "radius": WHEEL_RADIUS_UU,
        "width": WHEEL_WIDTH_UU,
        "units": "uu (1 uu = 1/16 real cm); FBX authored in Blender metres, 1 m = 100 uu",
        "origin": "wheel centre",
        "axle_axis": "Y",
        "outer_face": "Blender +Y = left side of the car. After the FBX import that is UE -Y (left). Use as-is on the "
                      "LEFT wheels (FL, RL); rotate 180 deg yaw for the RIGHT wheels (FR, RR). The vanes are swept, "
                      "a yaw (not a mirror) keeps them correct.",
        "spin_axis_ue": "Y",
        "slots": ["Tire", "Hub"],
        "tris": tri_count(ob),
        "normals": "authored (analytic). Import normals, do not recompute.",
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
    coll = get_coll("Wheel")
    ob = build_wheel(coll=coll, quick=quick)
    wheel_uvs(ob)
    export_fbx(ob, os.path.join(HERE, "export", MESH_NAME + ".fbx"))
    wheel_sidecar(ob, os.path.join(HERE, ASSET + ".json"))
    if norender:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"))
        return
    # ---- previews: the wheel standing on the deck, show face toward the camera
    setup_render(sc, samples=48 if quick else 96, res=(800, 600) if quick else (1600, 1200))
    sun_az = 150.0
    setup_world(sc, "courtyard.exr", strength=0.55, sun_az=sun_az)
    add_sun(sc, az_deg=sun_az, el_deg=26.0, strength=4.2)
    make_deck(y_shift=-0.4)
    ob.location = (0.0, 0.0, WHEEL_RADIUS_UU * UU)
    ob.rotation_euler = (0.0, 0.0, math.radians(-20.0))
    tgt = (0.0, 0.0, WHEEL_RADIUS_UU * UU)
    shots = {
        "W02_Fan_34": make_camera("Cam34", tgt, 62.0, 14.0, 1.15, 100.0, 3.2,
                                  focus=(0.0, 0.03, WHEEL_RADIUS_UU * UU)),
        "W02_Fan_face": make_camera("CamFace", tgt, 70.0, 4.0, 1.05, 100.0, 5.6,
                                    focus=(0.0, 0.04, WHEEL_RADIUS_UU * UU)),
    }
    for nm, cam in shots.items():
        render_view(sc, cam, os.path.join(HERE, "preview", nm + ".png"))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"))
    log("saved", ASSET + ".blend")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    main(quick="--quick" in argv, norender="--norender" in argv)
