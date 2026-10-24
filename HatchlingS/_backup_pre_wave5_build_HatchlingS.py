"""
build_HatchlingS.py  -  MODEL '93 / CozyCarGame, Slice 1A                 (rev 2, spec 4b)
=========================================================================================
Die-cast casting "Hatchling S" (STREAKLINE, 1991 casting; the player's "Old Faithful").
Class Compact, hitbox 112 x 84 x 40 uu, wheels W01_Dish (era one-piece plastic wheels).

Rev 2 reworks the casting to the binding die-cast realism rules (SLICE_1A_BUILD_SPEC.md 4b):
CAST, NOT ASSEMBLED (thick >= 5 uu pillars, 2.2 uu shell visible at every glass edge, mirrors
reduced to cast nubs, lamps as cast bosses coloured by tampo, grille as soft grooves, the rally
lamp bar cast into the roof); SOFT EDGES (0.8-1.5 uu radii, rounded half-filled panel grooves);
ERA WHEELS (rebuilt W01_Dish, steel axles with peened heads in the hub bore); VISIBLE BASE (a
~4.5 uu black plastic band under the sill, black wheel-well liners, rivets, text panel);
ONE THICK LIGHT-SMOKE WINDOW PIECE (2.3 uu, ~46 % transmission) over a tan one-colour
interior tub; TAMPO livery on UV1 (procedural, registration offsets, print flaws); toy STANCE
(3 uu arch gaps, 0.5 deg nose-down rake, oversized wheels pushed to the corners).

Builds everything from an empty scene:
  * Body (Paint/Chrome/Lamp/Zamac), Base (Base: black plastic + steel axles/rivets via Col),
    Windows (Glass), Interior (Interior)
  * textures/T_HatchlingS_OldFaithful_Tampo.png (+ _TampoMetal.png) - the default livery
  * saves HatchlingS.blend, exports export/SM_HatchlingS_<Part>.fbx, writes HatchlingS.json
  * renders preview/*.png on the shared Navvy stage (identical camera/light/deck), incl. the
    family shot beside the imported Navvy FBX.

Run headless:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup
      --python build_HatchlingS.py -- [--quick] [--no-render] [--no-export]
      [--shots hero_34_front,family_navvy] [--pct 50] [--samples 32] [--suffix _i1]
--quick = coarse SDF meshing for look iterations (spec 4b rule 10: 50 % / 32 samples).

Modelling method: every cast part is a signed distance field written in uu (cast-style rounded
unions / cuts / grooves), meshed with surface nets, decimated to budget and given analytic
(gradient) normals, so every edge has a consistent rounded die-cast radius.
Conventions: Blender metres at game scale (1 uu = 0.01 m), front +X, left +Y, up +Z, origin at
ground level centred between the axles.
"""
import bpy, bmesh, math, os, sys, json, time, importlib.util
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = "HatchlingS"
UU = 0.01

# --- the wheel design module (also hosts the shared Navvy preview stage) -----------
_WPATH = os.path.join(os.path.dirname(HERE), "Wheel_W01_Dish", "build_Wheel_W01_Dish.py")
_spec = importlib.util.spec_from_file_location("build_Wheel_W01_Dish", _WPATH)
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)


def log(*a):
    print("[%s]" % ASSET, *a, flush=True)


def parse_args():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    o = dict(quick=False, render=True, export=True, shots=None, pct=100, samples=96, suffix='')
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--quick': o['quick'] = True
        elif a == '--no-render': o['render'] = False
        elif a == '--no-export': o['export'] = False
        elif a == '--shots': o['shots'] = argv[i + 1].split(','); i += 1
        elif a == '--pct': o['pct'] = int(argv[i + 1]); i += 1
        elif a == '--samples': o['samples'] = int(argv[i + 1]); i += 1
        elif a == '--suffix': o['suffix'] = argv[i + 1]; i += 1
        i += 1
    return o


OPT = parse_args()

# =============================================================================
#  Casting constants (uu)
# =============================================================================
WHEEL_R = W.WHEEL_RADIUS_UU          # 10.0
WHEEL_WD = W.WHEEL_WIDTH_UU          # 7.0 (narrow era wheel)
X_FA, X_RA = 37.0, -37.0             # axles: wheelbase 74, wheels pushed to the corners
WHEEL_Y = 36.6                       # wheel centre |y|: tyre face 40.1, hub lip 40.6, flare 41.0
AXLE_Z = WHEEL_R
AXLE_R = 0.9
ARCH_R, ARCH_Z = 12.9, 10.2          # oversized arch: ~3 uu tyre-to-arch gap (2.8 front / 3.4 rear after rake)
T_SHELL = 2.2                        # zamac wall (1.4 mm real): visible at every opening
Z_SILL = 9.2                         # body skin ends here; the base band shows below it
Z_BOT = 2.0                          # base underside (rev 3: lowered 1.6 uu so the black band is ~7.7 uu tall between the wheels)
BUMPER_TOP = 12.9
BAR_Z0 = 7.4                         # bumper bar bottom; below it a recessed chin
BUMP_FX, BUMP_RX = 50.8, -49.8       # base bumpers start in front of / behind these x
RAKE_DEG = 0.5                       # toy rake: nose down about the axle line
GLASS_T, GLASS_GAP = 2.3, 0.08       # window piece thickness, gap to the shell
HITBOX = {"center": [2.0, 0.0, 20.0], "extent": [56.0, 42.0, 20.0]}   # 112 x 84 x 40 (spec)

# Old Faithful default livery (spec: NOT red - the Vortex is red)
PAINT_LIN = (0.012, 0.088, 0.40)     # period metallic "Streak Blue"
PAINT_SRGB = "#1C53AA"
INTERIOR_LIN = (0.52, 0.38, 0.22)    # tan one-colour tub
GLASS_TINT = (0.70, 0.72, 0.72)      # per surface -> ~50 % through the 2-surface piece
WHEEL_WOBBLE = {"FL": (0.4, -0.3), "FR": (-0.3, 0.2), "RL": (-0.2, 0.4), "RR": (0.5, -0.2)}   # camber, toe deg


# =============================================================================
#  Small numeric toolkit
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
    """Smooth 1D profile (monotone cubic through keys), constant outside the key range."""
    def __init__(self, xk, yk, n=4096):
        self.x = np.linspace(xk[0], xk[-1], n)
        self.y = pchip_eval(xk, yk, self.x)
        self.dy = np.gradient(self.y, self.x)

    def __call__(self, q):
        return np.interp(q, self.x, self.y)

    def d(self, q):
        return np.interp(q, self.x, self.dy, left=0.0, right=0.0)


def mx0(a):
    return np.maximum(a, 0.0)


def u_round(a, b, r):
    """union with a concave fillet of radius r"""
    ua = mx0(r - a); ub = mx0(r - b)
    return np.maximum(r, np.minimum(a, b)) - np.sqrt(ua * ua + ub * ub)


def i_round(a, b, r):
    """intersection with a convex round of radius r"""
    ua = mx0(r + a); ub = mx0(r + b)
    return np.minimum(-r, np.maximum(a, b)) + np.sqrt(ua * ua + ub * ub)


def s_round(a, b, r):
    """subtract b from a, cut edge rounded by r"""
    return i_round(a, -b, r)


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


def rot_xz(x, z, cx, cz, ang):
    """rotate (x,z) about (cx,cz) by -ang (to express points in a frame pitched by ang)"""
    c, s = math.cos(ang), math.sin(ang)
    dx, dz = x - cx, z - cz
    return cx + c * dx + s * dz, cz - s * dx + c * dz


def offset_convex(poly, d):
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


# =============================================================================
#  BODY  -  shape definition (uu)
# =============================================================================
WPLAN = Prof([-55, -50, -42, 42, 50, 58], [34.6, 36.4, 37.4, 37.4, 36.3, 33.4])
WSEC = Prof([5, 8.5, 13, 18, 22, 28], [-1.4, -0.65, 0.0, 0.0, -0.4, -1.4])      # tuck-under draft + shoulder
TOPX = Prof([-57, -45, -20, 0, 20, 30, 45, 60], [25.6, 25.4, 24.9, 24.6, 24.2, 23.8, 23.0, 21.6])
CROWN = Prof([-57, 18, 26, 60], [0.35, 0.35, 0.9, 0.9])
ROOFX = Prof([-40, -15, 10], [38.6, 38.9, 38.5])
ROOF_CROWN, ROOF_CW = 1.0, 27.0


def _plane(p0, p1, outward_sign):
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dz)
    U = (dx / ln, dz / ln)
    N = (outward_sign * U[1], -outward_sign * U[0])
    return U, N, ln


WS_A, WS_B = (22.5, 24.0), (7.5, 38.8)
WS_U, WS_N, WS_LEN = _plane(WS_A, WS_B, 1.0)       # N points forward/up
HT_D, HT_C = (-48.5, 25.0), (-35.0, 38.8)
HT_U, HT_N, HT_LEN = _plane(HT_D, HT_C, -1.0)      # N points back/up
GW_B = 0.31
GW_NORM = math.sqrt(1 + GW_B ** 2)


def nose_x(z):
    return 56.6 - 0.10 * (z - 12.0)


def tail_x(z):
    return -52.6 + 0.06 * (z - 12.0)


def GW(z):
    return 32.2 - GW_B * (z - 24.0)


def x_ws(z):
    return WS_A[0] + (z - WS_A[1]) * (WS_U[0] / WS_U[1])


def x_ht(z):
    return HT_D[0] + (z - HT_D[1]) * (HT_U[0] / HT_U[1])


def roof_z(x, y):
    return ROOFX(x) + ROOF_CROWN * (1.0 - (y / ROOF_CW) ** 2)


def top_z(x, y):
    c = CROWN(x)
    return TOPX(x) + c * (1.0 - (y / 38.0) ** 2)


def lower_plan(x, y, z):
    W_ = WPLAN(x) + WSEC(z)
    side = (np.abs(y) - W_) / np.sqrt(1 + WPLAN.d(x) ** 2 + WSEC.d(z) ** 2)
    d = i_round(side, (x - nose_x(z)) / 1.005, 6.0)
    return i_round(d, (tail_x(z) - x) / 1.0018, 5.0)


def lower_body(x, y, z):
    c = CROWN(x)
    top = TOPX(x) + c * (1.0 - (y / 38.0) ** 2)
    d_top = (z - top) / np.sqrt(1 + TOPX.d(x) ** 2 + (2 * c * y / 1444.0) ** 2)
    A = i_round(lower_plan(x, y, z), d_top, 2.6)
    return np.maximum(A, 4.0 - z)


def greenhouse(x, y, z):
    gs = (np.abs(y) - GW(z)) / GW_NORM
    gws = (x - WS_A[0]) * WS_N[0] + (z - WS_A[1]) * WS_N[1]
    gh = (x - HT_D[0]) * HT_N[0] + (z - HT_D[1]) * HT_N[1]
    rz = roof_z(x, y)
    gt = (z - rz) / np.sqrt(1 + ROOFX.d(x) ** 2 + (2 * ROOF_CROWN * y / ROOF_CW ** 2) ** 2)
    G = i_round(gs, gws, 2.8)
    G = i_round(G, gh, 3.2)
    G = i_round(G, gt, 4.0)
    return np.maximum(G, 22.5 - z)


def outer_master(x, y, z):
    return u_round(lower_body(x, y, z), greenhouse(x, y, z), 1.1)


FLARE_TOP = {X_FA: 25.0, X_RA: 25.9}


def flares(x, y, z):
    ay = np.abs(y)
    d = None
    for xw in (X_FA, X_RA):
        hl = 17.4 - (z - 4.0) * (2.9 / 21.0)
        dx = (np.abs(x - xw) - hl) / 1.0095
        side2d = i_round(dx, z - FLARE_TOP[xw], 3.2)
        dy = ay - (41.0 - (z - 10.0) * 0.07)
        f = i_round(side2d, dy, 1.8)
        f = np.maximum(f, 28.0 - ay)
        f = np.maximum(f, 4.0 - z)
        d = f if d is None else np.minimum(d, f)
    d = i_round(d, x - (nose_x(z) - 1.2), 2.0)
    d = i_round(d, (tail_x(z) + 1.2) - x, 2.0)
    return d


def arches(x, y, z):
    d = np.minimum(np.hypot(x - X_FA, z - ARCH_Z), np.hypot(x - X_RA, z - ARCH_Z)) - ARCH_R
    return np.maximum(d, 24.0 - np.abs(y))


def bulge(x, y, z):
    top = top_z(x, y)
    d = i_round(z - top - 0.8, sd_rrect2(x - 40.0, y, 12.5, 10.0, 4.0), 2.2)
    return np.maximum(d, top - 3.0 - z)


def spoiler(x, y, z):
    xr, zr = rot_xz(x, z, -36.2, 39.1, math.radians(-6))
    return sd_rbox(xr, y, zr, (-36.2, 0.0, 39.1), (3.3, 25.5, 1.25), 1.15)


SCOOP_X0, SCOOP_X1, SCOOP_H = -11.0, -1.4, 2.6


def scoop(x, y, z):
    rz = roof_z(x, y)
    h = np.interp(x, [SCOOP_X0, SCOOP_X1], [0.0, SCOOP_H], left=0.0, right=0.0)
    d_top = (z - rz - h) / 1.027
    d_xy = sd_rrect2(x - 0.5 * (SCOOP_X0 + SCOOP_X1), y, 0.5 * (SCOOP_X1 - SCOOP_X0), 7.2, 1.8)
    sc = i_round(d_top, d_xy, 1.0)
    return np.maximum(sc, rz - 1.5 - z)


def scoop_mouth(x, y, z):
    zc = float(roof_z(np.array(-1.8), np.array(0.0))) + 1.2
    m = sd_rbox(x, y, z, (-1.4, 0.0, zc), (1.6, 5.8, 0.8), 0.55)
    return m, zc


def mirror_nubs(x, y, z):
    """mirrors reduced to tiny cast nubs on the shoulder ahead of the door glass"""
    return sd_ellipsoid(x, np.abs(y), z, (17.6, GW(26.3) + 0.4, 26.0), (2.2, 1.6, 1.3))


# --- window openings (thick pillars) -----------------------------------------
WIN_ZB, WIN_ZT = 26.4, 34.0
A_OFF = 7.0                              # door glass starts 7 uu behind the windscreen line (A-pillar >= 5)
B_FRONT, B_REAR = -12.0, -18.6           # B-pillar 6.6 wide
C_PILLAR = 13.2                          # thick hot-hatch C-pillar
DOOR_POLY = [(x_ws(WIN_ZB) - A_OFF, WIN_ZB), (B_FRONT, WIN_ZB), (B_FRONT, WIN_ZT), (x_ws(WIN_ZT) - A_OFF, WIN_ZT)]
QTR_POLY = [(x_ht(WIN_ZB) + C_PILLAR, WIN_ZB), (B_REAR, WIN_ZB), (B_REAR, WIN_ZT), (x_ht(WIN_ZT) + C_PILLAR, WIN_ZT)]
R_SIDEWIN = 2.2


def _ws_hw(u):
    return GW(WS_A[1] + u * WS_U[1]) - 5.6


def _ht_hw(u):
    return GW(HT_D[1] + u * HT_U[1]) - 6.4


WS_U0, WS_U1 = 2.6, WS_LEN - 4.8         # cowl lip, roof header 4.8
HT_U0, HT_U1 = 3.2, HT_LEN - 4.6
WS_POLY = [(WS_U0, -_ws_hw(WS_U0)), (WS_U1, -_ws_hw(WS_U1)), (WS_U1, _ws_hw(WS_U1)), (WS_U0, _ws_hw(WS_U0))]
HT_POLY = [(HT_U0, -_ht_hw(HT_U0)), (HT_U1, -_ht_hw(HT_U1)), (HT_U1, _ht_hw(HT_U1)), (HT_U0, _ht_hw(HT_U0))]
R_WS, R_HT = 2.8, 2.8
DOOR_SHR = offset_convex(DOOR_POLY, -R_SIDEWIN)
QTR_SHR = offset_convex(QTR_POLY, -R_SIDEWIN)
WS_SHR = offset_convex(WS_POLY, -R_WS)
HT_SHR = offset_convex(HT_POLY, -R_HT)


def windows_zone(x, y, z, grow=0.0, slab=3.0):
    """Openings (grow = 0) or the window-piece footprint (grow > 0) as one SDF."""
    ay = np.abs(y)
    side = np.minimum(sd_poly(x, z, DOOR_SHR), sd_poly(x, z, QTR_SHR)) - R_SIDEWIN - grow
    side = np.maximum(side, 19.0 - ay)
    u = (x - WS_A[0]) * WS_U[0] + (z - WS_A[1]) * WS_U[1]
    w = (x - WS_A[0]) * WS_N[0] + (z - WS_A[1]) * WS_N[1]
    ws = np.maximum(sd_poly(u, y, WS_SHR) - R_WS - grow, np.abs(w + slab - 3.0) - slab)
    uh = (x - HT_D[0]) * HT_U[0] + (z - HT_D[1]) * HT_U[1]
    wh = (x - HT_D[0]) * HT_N[0] + (z - HT_D[1]) * HT_N[1]
    ht = np.maximum(sd_poly(uh, y, HT_SHR) - R_HT - grow, np.abs(wh + slab - 3.0) - slab)
    return np.minimum(side, np.minimum(ws, ht))


# --- cast lamp bosses (coloured by tampo), grille grooves, plate --------------
HL_Y, HL_Z, HL_HY, HL_HZ, HL_R, HL_RAISE = 22.6, 17.2, 6.6, 2.7, 1.6, 0.6
HL_DOMES = [(HL_Y + 2.4, 2.25), (HL_Y - 3.4, 1.65)]       # (|y|, r): main lamp + driving lamp
TL_Y, TL_Z, TL_HY, TL_HZ, TL_R, TL_RAISE = 25.5, 20.5, 5.0, 2.8, 1.3, 0.5
GRILLE_Z = (15.6, 17.3, 19.0)
LID_Y, LID_Z = 19.6, 15.4


def lamp_bosses(x, y, z):
    ay = np.abs(y)
    xn = nose_x(z)
    hl = i_round(sd_rrect2(ay - HL_Y, z - HL_Z, HL_HY, HL_HZ, HL_R), x - (xn + HL_RAISE), 0.5)
    hl = np.maximum(hl, (xn - 3.0) - x)
    for (yc, r) in HL_DOMES:
        dm = i_round(np.hypot(ay - yc, z - HL_Z) - r, x - (xn + HL_RAISE + 0.35), 0.3)
        dm = np.maximum(dm, (xn - 1.0) - x)
        hl = u_round(hl, dm, 0.2)
    xt = tail_x(z)
    tl = i_round(sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY, TL_HZ, TL_R), (xt - TL_RAISE) - x, 0.45)
    tl = np.maximum(tl, x - (xt + 3.0))
    return np.minimum(hl, tl)


def recesses(x, y, z, Oo):
    gr = None
    for zc in GRILLE_Z:
        g = sd_rrect2(y, z - zc, 12.6, 0.5, 0.48)
        gr = g if gr is None else np.minimum(gr, g)
    gr = np.maximum(np.maximum(gr, -(Oo + 0.8)), 50.0 - x)
    plate = np.maximum(np.maximum(sd_rrect2(y, z - 18.6, 8.2, 2.3, 0.9), -(Oo + 0.45)), x + 46.0)
    return np.minimum(gr, plate)


GROOVE_HW, GROOVE_DEPTH = 0.36, 0.55
MOOD = {"cx": -21.5, "cy": 0.0, "hx": 9.0, "hy": 15.5, "r": 3.2}
DOOR_FX, DOOR_RX = 19.8, -15.3


def grooves(x, y, z, Oo):
    ay = np.abs(y); hw = GROOVE_HW
    g = np.maximum.reduce([np.abs(x - DOOR_FX) - hw, Z_SILL - z, z - 25.6, 30.0 - ay])            # door front
    g = np.minimum(g, np.maximum.reduce([np.abs(x - DOOR_RX) - hw, Z_SILL - z, z - 35.4, 25.0 - ay]))  # door rear
    g = np.minimum(g, np.maximum.reduce([np.abs(ay - 32.6) - hw, 24.4 - x, x - 55.0, 20.5 - z]))  # bonnet sides
    g = np.minimum(g, np.maximum.reduce([np.abs(x - 24.4) - hw, ay - 32.6, 21.5 - z]))           # cowl
    g = np.minimum(g, np.maximum.reduce([np.abs(z - 20.9) - hw, 50.5 - x, ay - 32.6]))           # bonnet lip
    g = np.minimum(g, np.maximum.reduce([np.abs(ay - LID_Y) - hw, x + 47.0, LID_Z - z, z - 27.5]))  # lid sides
    g = np.minimum(g, np.maximum.reduce([np.abs(z - LID_Z) - hw, x + 47.0, ay - LID_Y]))         # lid bottom
    mp = sd_rrect2(x - MOOD["cx"], y - MOOD["cy"], MOOD["hx"], MOOD["hy"], MOOD["r"])
    g = np.minimum(g, np.maximum(np.abs(mp) - hw, 37.0 - z))                                     # mood panel
    return np.maximum(g, -(Oo + GROOVE_DEPTH))


# --- roof rally lamps: bar cast into the roof (Paint), chrome pods, amber lenses ----
RL_Y, RL_R, RL_XB, RL_XF = 8.8, 3.4, 0.0, 4.6
BAR_X, BAR_HY, FOOT_Y = 2.0, 14.0, 12.4
RALLY_TINT = (1.0, 0.70, 0.16)
RALLY = {}


def rally_geo():
    if not RALLY:
        rc = float(roof_z(np.array(BAR_X), np.array(0.0)))
        rf = float(roof_z(np.array(BAR_X), np.array(FOOT_Y)))
        bar_z = rc + 0.95
        RALLY.update(roof=rc, roof_f=rf, bar_z=bar_z, zc=bar_z + 1.0 + RL_R - 0.9)
        RALLY['top'] = RALLY['zc'] + RL_R
        log("rally lamps: roof %.2f bar %.2f lamp centre %.2f top %.2f" % (rc, bar_z, RALLY['zc'], RALLY['top']))
    return RALLY


def rally_bar(x, y, z):
    g = rally_geo()
    ay = np.abs(y)
    bar = sd_rbox(x, y, z, (BAR_X, 0.0, g['bar_z']), (1.5, BAR_HY, 1.1), 0.9)
    zf0 = g['roof_f'] - 1.0
    feet = sd_rbox(x, ay, z, (BAR_X, FOOT_Y, 0.5 * (g['bar_z'] + zf0)), (1.8, 1.5, 0.5 * (g['bar_z'] - zf0)), 0.8)
    return u_round(bar, feet, 0.8)


def rally_pod(x, y, z):
    g = rally_geo()
    ay = np.abs(y)
    rho = np.hypot(ay - RL_Y, z - g['zc'])
    d = i_round(i_round(rho - RL_R, x - RL_XF, 0.55), RL_XB - x, 1.7)
    d = s_round(d, np.maximum(rho - (RL_R - 0.6), np.abs(x - RL_XF) - 0.4), 0.15)     # lens seat
    return d


def rally_stalk(x, y, z):
    g = rally_geo()
    return sd_rbox(x, np.abs(y), z, (BAR_X + 0.3, RL_Y, g['bar_z'] + 1.15), (0.85, 0.85, 0.75), 0.3)


def rally_lens(x, y, z):
    g = rally_geo()
    ay = np.abs(y)
    rho = np.hypot(ay - RL_Y, z - g['zc'])
    sph = np.sqrt((x - (RL_XF - 6.2)) ** 2 + rho ** 2) - 6.55
    d = np.maximum.reduce([sph, rho - (RL_R - 0.45), (RL_XF - 0.6) - x])
    bars = np.maximum(np.minimum(np.abs(ay - RL_Y), np.abs(z - g['zc'])) - 0.16, rho - (RL_R - 0.7))
    bars = np.maximum(bars, (RL_XF + 0.25) - x)
    return s_round(d, np.maximum(bars, -(sph + 0.1)), 0.05)


def body_fields(x, y, z):
    A = lower_body(x, y, z)
    G = greenhouse(x, y, z)
    Om = u_round(A, G, 1.1)
    Oo = u_round(Om, flares(x, y, z), 2.2)
    Oo = u_round(Oo, bulge(x, y, z), 2.0)
    Oo = u_round(Oo, spoiler(x, y, z), 1.1)
    Oo = u_round(Oo, scoop(x, y, z), 0.9)
    S = np.maximum(Oo, -(Om + T_SHELL))
    S = s_round(S, arches(x, y, z), 1.1)
    S = i_round(S, Z_SILL - z, 0.9)
    S = s_round(S, np.maximum(BUMP_FX + 1.4 - x, z - BUMPER_TOP), 0.8)
    S = s_round(S, np.maximum(x - (BUMP_RX - 1.4), z - BUMPER_TOP), 0.8)
    S = s_round(S, windows_zone(x, y, z), 1.0)
    S = u_round(S, lamp_bosses(x, y, z), 0.4)
    S = s_round(S, recesses(x, y, z, Oo), 0.35)
    S = s_round(S, grooves(x, y, z, Oo), 0.3)
    S = u_round(S, mirror_nubs(x, y, z), 0.8)
    S = u_round(S, rally_bar(x, y, z), 0.9)
    m, zc = scoop_mouth(x, y, z)
    S = s_round(S, m, 0.4)
    return S, Om, Oo


def body_sdf(x, y, z):
    return body_fields(x, y, z)[0]


# =============================================================================
#  WINDOW PIECE (one thick light-smoke moulding inside the shell)
# =============================================================================
def glass_sdf(x, y, z):
    Om = outer_master(x, y, z)
    shell = np.abs(Om + T_SHELL + GLASS_GAP + 0.5 * GLASS_T) - 0.5 * GLASS_T
    return i_round(shell, windows_zone(x, y, z, grow=2.6, slab=7.0), 0.8)


# =============================================================================
#  BASE (chassis) SDF  - black plastic: band under the sill, bumpers, wheel wells
# =============================================================================
RIVETS = [(45.0, 0.0), (-44.0, 0.0)]
TEXT_AREA = {"cx": -2.0, "cy": 0.0, "hx": 20.0, "hy": 12.0}
BAND_INSET = -0.30                   # rev 3: band stands 0.3 uu PROUD of the sill so it catches light as a black rocker


def base_sdf(x, y, z):
    ay = np.abs(y)
    plan8 = lower_plan(x, y, np.full_like(z, 8.2))
    zb1 = Z_SILL + 0.5
    band = i_round(plan8 + BAND_INSET, np.abs(z - 0.5 * (Z_BOT + zb1)) - 0.5 * (zb1 - Z_BOT), 1.1)
    plug = i_round(plan8 + T_SHELL + 0.35, np.abs(z - (Z_SILL + 1.2)) - 1.0, 0.5)
    B = u_round(band, plug, 0.4)
    # bumpers: the base wraps up into chunky front/rear bumpers
    plan10 = lower_plan(x, y, np.full_like(z, 10.0))
    # a bumper bar (z BAR_Z0..BUMPER_TOP) over a recessed chin/valance down to the base
    bump_z = np.abs(z - 0.5 * (BAR_Z0 + BUMPER_TOP)) - 0.5 * (BUMPER_TOP - BAR_Z0)
    val_z = np.abs(z - 0.5 * (Z_BOT + BAR_Z0 + 0.6)) - 0.5 * (BAR_Z0 + 0.6 - Z_BOT)
    fb = u_round(i_round(i_round(plan10 - 2.0, bump_z, 1.5), BUMP_FX - x, 1.2),
                 i_round(i_round(plan10 + 0.4, val_z, 1.1), BUMP_FX + 1.0 - x, 1.0), 0.5)
    rb = u_round(i_round(i_round(plan10 - 2.0, bump_z, 1.5), x - BUMP_RX, 1.2),
                 i_round(i_round(plan10 + 0.4, val_z, 1.1), x - (BUMP_RX - 1.0), 1.0), 0.5)
    bumpers = np.minimum(fb, rb)
    B = u_round(B, bumpers, 0.8)
    strip = np.maximum(np.abs(z - 10.15) - 0.45, -(bumpers + 0.5))
    slot = np.maximum(sd_rrect2(y, z - 5.6, 15.0, 0.75, 0.65), -(fb + 0.9))
    ind = np.maximum(sd_rrect2(ay - 26.0, z - 11.6, 3.0, 0.7, 0.6), -(fb + 0.5))
    exh = np.maximum(sd_rrect2(y + 21.0, z - 5.6, 3.0, 1.2, 1.15), -(rb + 1.2))
    B = s_round(B, np.minimum.reduce([strip, slot, ind, exh]), 0.3)
    # wheel notches
    for xw in (X_FA, X_RA):
        B = s_round(B, sd_rbox(x, ay, z, (xw, 50.0, 10.0), (ARCH_R - 0.2, 50.0 - (WHEEL_Y - WHEEL_WD / 2 - 1.4), 12.0), 2.0), 0.6)
    # wheel-well liners (black) so the arches never show the empty body cavity
    Om = outer_master(x, y, z)
    for xw in (X_FA, X_RA):
        rr = np.hypot(x - xw, z - ARCH_Z)
        liner = np.maximum.reduce([np.abs(rr - (ARCH_R + 0.9)) - 0.7, 25.6 - ay, Z_SILL - 1.0 - z])
        back = np.maximum.reduce([np.abs(ay - 26.2) - 0.6, rr - (ARCH_R + 1.6), Z_BOT + 1.0 - z])
        Lw = np.maximum(np.minimum(liner, back), Om + T_SHELL + 0.15)
        B = u_round(B, Lw, 0.5)
    # axle carriers (inside) and channels open from below so the steel axle reads
    for xw in (X_FA, X_RA):
        B = u_round(B, sd_rbox(x, y, z, (xw, 0.0, AXLE_Z - 0.2), (4.8, 26.0, 2.4), 1.2), 0.6)
        ztop = AXLE_Z + 0.5
        B = s_round(B, sd_rbox(x, y, z, (xw, 0.0, 0.5 * ztop), (3.4, 27.0, 0.5 * ztop), 1.6), 0.7)
    # rivets: dimple + domed head
    for (rx, ry) in RIVETS:
        B = s_round(B, np.maximum(np.hypot(x - rx, y - ry) - 3.4, z - (Z_BOT + 0.35)), 0.25)
        B = u_round(B, sd_ellipsoid(x, y, z, (rx, ry, Z_BOT + 0.35), (2.1, 2.1, 1.1)), 0.2)
    # plain recessed text / decal area
    ta = sd_rrect2(x - TEXT_AREA["cx"], y - TEXT_AREA["cy"], TEXT_AREA["hx"], TEXT_AREA["hy"], 2.0)
    B = s_round(B, np.maximum(ta, z - (Z_BOT + 0.32)), 0.15)
    # moulded chassis relief on the underside
    exhaust = sd_capsule(x, y, z, (24.0, -19.0, Z_BOT + 0.05), (-31.0, -19.0, Z_BOT + 0.05), 1.0)
    muffler = sd_rbox(x, y, z, (-44.5, -19.0, Z_BOT), (4.5, 3.4, 1.15), 1.0)
    sump = sd_rbox(x, y, z, (44.0, -14.0, Z_BOT), (4.0, 4.6, 0.8), 1.0)
    tank = sd_rbox(x, y, z, (-29.0, 13.0, Z_BOT), (5.0, 7.0, 0.75), 1.2)
    ribs = np.minimum(sd_capsule(x, ay, z, (-24.0, 26.0, Z_BOT), (24.0, 26.0, Z_BOT), 0.55),
                      sd_capsule(x, y, z, (29.0, -10.0, Z_BOT), (29.0, 10.0, Z_BOT), 0.45))
    relief = np.minimum.reduce([exhaust, muffler, sump, tank, ribs])
    B = u_round(B, relief, 0.5)
    return B


# =============================================================================
#  INTERIOR SDF (one colour moulding, seats + wheel + dash cast in)
# =============================================================================
def seat_back(x, y, z, cx, cy, cz, h, r, ang):
    xr, zr = rot_xz(x, z, cx, cz, ang)
    return sd_rbox(xr, y, zr, (cx, cy, cz), h, r)


def interior_sdf(x, y, z):
    ay = np.abs(y)
    tub = sd_rbox(x, y, z, (-8.5, 0.0, 12.0), (32.0, 30.0, 1.0), 0.8)
    cush = sd_rbox(x, ay, z, (-3.0, 13.2, 15.0), (5.8, 5.6, 2.6), 1.8)
    back = seat_back(x, ay, z, -9.6, 13.2, 22.8, (1.7, 5.6, 8.0), 1.5, math.radians(-12))
    bol = seat_back(x, np.abs(ay - 13.2), z, -8.9, 5.1, 21.5, (1.5, 0.9, 6.6), 0.8, math.radians(-12))
    head = seat_back(x, ay, z, -11.5, 13.2, 32.2, (1.3, 3.4, 2.2), 1.1, math.radians(-12))
    seats = u_round(u_round(cush, back, 1.0), u_round(bol, head, 0.6), 0.6)
    rc = sd_rbox(x, y, z, (-25.0, 0.0, 14.6), (5.2, 22.5, 3.2), 1.8)
    rbk = seat_back(x, y, z, -31.2, 0.0, 22.0, (1.6, 22.5, 7.6), 1.5, math.radians(-16))
    rear = u_round(rc, rbk, 1.0)
    # rev 3: the dash is a SOLID cowl block from the tub floor to z 24.4 (>= 12 uu of cast plastic, top face 14 uu deep),
    # not a plank, so no thin sheet can catch a specular sliver behind the windscreen
    dash = sd_rbox(x, y, z, (15.5, 0.0, 18.2), (5.5, 29.0, 6.2), 1.6)
    binn = sd_rbox(x, y, z, (12.5, 13.2, 24.3), (3.0, 5.2, 1.6), 1.0)
    c = np.array([8.6, 13.2, 23.4]); a = np.array([-0.906, 0.0, 0.423])
    px, py, pz = x - c[0], y - c[1], z - c[2]
    pa = px * a[0] + py * a[1] + pz * a[2]
    qx, qy, qz = px - pa * a[0], py - pa * a[1], pz - pa * a[2]
    rho = np.sqrt(qx * qx + qy * qy + qz * qz)
    wheel = np.hypot(rho - 3.4, pa) - 1.05
    spoke = np.maximum(np.maximum(np.abs(qy) - 0.95, np.abs(pa) - 0.9), rho - 3.4)
    hub = np.maximum(rho - 1.9, np.abs(pa) - 1.2)
    col = sd_capsule(x, y, z, tuple(c), (14.0, 13.2, 24.0), 1.3)
    steer = np.minimum.reduce([wheel, spoke, hub, col])
    cons = sd_rbox(x, y, z, (2.0, 0.0, 13.6), (9.0, 2.8, 2.2), 1.0)
    gear = np.minimum(sd_capsule(x, y, z, (4.0, 0.0, 14.5), (3.3, 0.0, 18.0), 0.45),
                      np.sqrt((x - 3.2) ** 2 + y ** 2 + (z - 18.5) ** 2) - 0.95)
    D = np.minimum.reduce([tub, seats, rear, dash, binn, steer, cons, gear])
    # keep clear of the wheel-well liners and of the shell / window piece
    for xw in (X_FA, X_RA):
        D = s_round(D, np.maximum(np.hypot(x - xw, z - ARCH_Z) - (ARCH_R + 2.0), 25.0 - ay), 0.5)
    Om = outer_master(x, y, z)
    off = 2.6 + 2.4 * np.clip((z - 22.5) / 2.0, 0.0, 1.0)
    return np.maximum(D, Om + off)


# =============================================================================
#  Surface nets mesher + SDF part pipeline
# =============================================================================
def surface_nets(fn, bmin, bmax, cell, chunk=1_500_000):
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
    if any(touch):
        del F, s
        pad = 3.0
        for k in range(3):
            if touch[2 * k]:
                bmin[k] -= pad
            if touch[2 * k + 1]:
                bmax[k] += pad
        log("  domain touched %s -> grown to %s %s" % (touch, bmin.round(2).tolist(), bmax.round(2).tolist()))
        return surface_nets(fn, bmin, bmax, cell, chunk)
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


def sdf_part(name, fn, bmin, bmax, cell, target_tris, symmetric=True, normal_eps=0.02):
    """SDF -> surface nets -> decimate -> reproject -> analytic normals. Returns (V uu, T, N)."""
    t0 = time.time()
    V, Q = surface_nets(fn, bmin, bmax, cell)
    V = project(fn, V, iters=2, maxstep=cell)
    me = mesh_from_numpy(name + "_tmp", V * UU, Q)
    ob = bpy.data.objects.new(name + "_tmp", me)
    bpy.context.scene.collection.objects.link(ob)
    ntri = 2 * len(Q)
    mp = ob.modifiers.new("Planar", 'DECIMATE')
    mp.decimate_type = 'DISSOLVE'
    mp.angle_limit = math.radians(0.5)
    W.apply_modifiers(ob)
    nmid = sum(len(p.vertices) - 2 for p in ob.data.polygons)
    md = ob.modifiers.new("Dec", 'DECIMATE')
    md.decimate_type = 'COLLAPSE'
    md.ratio = min(1.0, target_tris / max(nmid, 1))
    md.use_collapse_triangulate = True
    if symmetric:
        md.use_symmetry = True
        md.symmetry_axis = 'Y'
    W.apply_modifiers(ob)
    V2, T = mesh_arrays(ob.data)
    V2 = V2 / UU
    V2 = project(fn, V2, iters=1, maxstep=0.12)
    N = sdf_grad(fn, V2, eps=normal_eps)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
    me2 = ob.data
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me2)
    log("  part %-14s %7d -> planar %7d -> %6d tris  (%.1fs)" % (name, ntri, nmid, len(T), time.time() - t0))
    return V2, T, N


def cylinder_y(xc, zc, r, y0, y1, seg=16):
    """Analytic steel axle along Y (uu)."""
    ang = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ring = np.stack([xc + r * np.cos(ang), np.zeros(seg), zc + r * np.sin(ang)], 1)
    nrm_ring = np.stack([np.cos(ang), np.zeros(seg), np.sin(ang)], 1)
    V = np.concatenate([ring + [0, y0, 0], ring + [0, y1, 0]])
    N = np.concatenate([nrm_ring, nrm_ring])
    T = []
    for k in range(seg):
        k2 = (k + 1) % seg
        T += [(k, seg + k, seg + k2), (k, seg + k2, k2)]
    return V, np.array(T), N


def axle_heads(xc, zc, y_out):
    """Both peened axle heads of one axle (W01 head shape), as (V, T, N) in uu."""
    out = []
    for sgn in (1.0, -1.0):
        hv, hf = W.axle_head_geo(y_out)
        bm = bmesh.new()
        vs = [bm.verts.new((xc + a, sgn * b, zc + c)) for (a, b, c) in hv]
        for f in hf:
            try:
                bm.faces.new([vs[i] for i in (f if sgn > 0 else f[::-1])])
            except ValueError:
                pass
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.normal_update()
        bm.verts.index_update()
        V = np.array([v.co[:] for v in bm.verts])
        T = np.array([[v.index for v in f.verts] for f in bm.faces])
        N = np.array([v.normal[:] for v in bm.verts])
        bm.free()
        out.append((V, T, N))
    return out


RAKE = Matrix.Translation((0, 0, AXLE_Z)) @ Matrix.Rotation(math.radians(RAKE_DEG), 4, 'Y') @ \
    Matrix.Translation((0, 0, -AXLE_Z))
RAKE_NP = np.array(RAKE)
RAKE_INV_NP = np.array(RAKE.inverted())


def rake_points(P, inv=False):
    M = RAKE_INV_NP if inv else RAKE_NP
    return P @ M[:3, :3].T + M[:3, 3]


def build_object(name, parts, mat_names, coll=None, rake=True):
    """parts: list of dict(V uu, T, N, mat, col(optional (nV,4)), rake(optional bool))"""
    Vs, Ts, Ns, Ms, Cs = [], [], [], [], []
    off = 0
    R3 = RAKE_NP[:3, :3]
    for p in parts:
        V, T, N = p["V"], p["T"], p["N"]
        if rake and p.get("rake", True):
            V = rake_points(V); N = N @ R3.T
        Vs.append(V); Ts.append(T + off); Ns.append(N)
        Ms.append(np.full(len(T), p["mat"], np.int32))
        c = p.get("col")
        Cs.append(np.tile([1.0, 1.0, 1.0, 1.0], (len(V), 1)) if c is None else c)
        off += len(V)
    V = np.concatenate(Vs); T = np.concatenate(Ts); N = np.concatenate(Ns)
    M = np.concatenate(Ms); C = np.concatenate(Cs)
    me = mesh_from_numpy(name, V * UU, T)
    for mn in mat_names:
        me.materials.append(bpy.data.materials.get(mn) or W.make_slot_material(mn))
    me.polygons.foreach_set("material_index", M)
    me.polygons.foreach_set("use_smooth", np.ones(len(T), bool))
    me.update()
    try:
        me.normals_split_custom_set_from_vertices(N.tolist())
    except Exception as e:
        log("custom normals (vertex) failed:", e)
    attr = me.color_attributes.new("Col", 'BYTE_COLOR', 'POINT')
    attr.data.foreach_set("color", C.astype(np.float32).ravel())
    try:
        me.color_attributes.active_color = attr
        me.color_attributes.render_color_index = 0
    except Exception:
        pass
    ob = bpy.data.objects.new(name, me)
    W.link(ob, coll)
    return ob


# =============================================================================
#  UVs  (UV1 = tampo layout, computed in the un-raked casting frame)
# =============================================================================
X_FRONT_UV, X_REAR_UV, UV_SPAN = 61.5, -58.5, 120.0
UV_S = 0.5 / UV_SPAN


def uv1_tampo(ob, misc_mask_fn=None):
    """UV1 = tampo layout: left side U 0-0.5, right side U 0.5-1 (V 0-0.2), top strip V 0.65-1,
    front/rear small islands, anything inside/underneath parked in the 0.92-1 corner."""
    me = ob.data
    nP = len(me.polygons)
    nrm = np.empty(nP * 3); me.polygons.foreach_get("normal", nrm); nrm = nrm.reshape(-1, 3)
    cen = np.empty(nP * 3); me.polygons.foreach_get("center", cen); cen = rake_points(cen.reshape(-1, 3) / UU, inv=True)
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co)
    co = rake_points(co.reshape(-1, 3) / UU, inv=True)
    li = np.empty(len(me.loops), np.int64); me.loops.foreach_get("vertex_index", li)
    lt = np.empty(nP, np.int64); me.polygons.foreach_get("loop_total", lt)
    fol = np.repeat(np.arange(nP), lt)
    nx, ny, nz = nrm[:, 0], nrm[:, 1], nrm[:, 2]
    cls = np.full(nP, 5)
    side = (np.abs(ny) >= 0.5) & (np.abs(ny) >= np.abs(nz))
    cls[side & (ny > 0)] = 0
    cls[side & (ny < 0)] = 1
    top = ~side & (nz >= 0.45)
    cls[top] = 2
    fr = ~side & ~top & (np.abs(nx) >= 0.5)
    cls[fr & (nx > 0)] = 3
    cls[fr & (nx < 0)] = 4
    if misc_mask_fn is not None:
        cls[misc_mask_fn(cen)] = 5
    c = cls[fol]; p = co[li]
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    u = np.zeros(len(li)); v = np.zeros(len(li))
    S = UV_S
    m = c == 0; u[m] = S * (X_FRONT_UV - x[m]); v[m] = S * z[m]
    m = c == 1; u[m] = 0.5 + S * (x[m] - X_REAR_UV); v[m] = S * z[m]
    m = c == 2; u[m] = S * (x[m] - X_REAR_UV); v[m] = 1.0 - S * (42.0 - y[m])
    m = c == 3; u[m] = 0.55 + S * (y[m] + 42.0); v[m] = 0.25 + S * z[m]
    m = c == 4; u[m] = 0.55 + S * (42.0 - y[m]); v[m] = 0.45 + S * z[m]
    m = c == 5; u[m] = 0.92 + 0.08 * (x[m] - X_REAR_UV) / UV_SPAN; v[m] = 0.92 + 0.08 * (y[m] + 42.0) / 84.0
    uv = me.uv_layers.new(name="UV1")
    uv.data.foreach_set("uv", np.stack([u, v], 1).ravel())
    me.uv_layers.active = me.uv_layers["UV0"]
    return np.bincount(cls, minlength=6)


def mood_uv1_rect():
    x0, x1 = MOOD["cx"] - MOOD["hx"], MOOD["cx"] + MOOD["hx"]
    y0, y1 = MOOD["cy"] - MOOD["hy"], MOOD["cy"] + MOOD["hy"]
    return [round(UV_S * (x0 - X_REAR_UV), 5), round(1.0 - UV_S * (42.0 - y0), 5),
            round(UV_S * (x1 - X_REAR_UV), 5), round(1.0 - UV_S * (42.0 - y1), 5)]


def do_uvs(ob, misc_mask_fn=None):
    W.smart_uv(ob, "UV0", angle=60.0, margin=0.002)
    return uv1_tampo(ob, misc_mask_fn)


# =============================================================================
#  TAMPO (procedural UV1 livery "Old Faithful": 1991 rally-hatch graphics)
# =============================================================================
TAMPO_RES = 2048
INK = {   # sRGB 0-1 (tampo inks are opaque, matte-ish)
    'white': (0.94, 0.93, 0.89), 'yellow': (0.98, 0.76, 0.07), 'red': (0.86, 0.16, 0.08),
    'black': (0.045, 0.045, 0.05), 'silver': (0.74, 0.75, 0.76), 'lens': (0.96, 0.96, 0.93),
    'fog': (0.99, 0.85, 0.25), 'tail': (0.70, 0.035, 0.04), 'amber': (0.98, 0.52, 0.06),
}
METAL_INKS = {'silver'}
TAMPO_SLANT = 0.42                     # stripes' italic cut (x per z)


def vnoise(x, y, seed, cell):
    rng = np.random.default_rng(seed)
    G = rng.random((258, 258)).astype(np.float32)
    xi = x / cell; yi = y / cell
    x0 = np.floor(xi); y0 = np.floor(yi)
    fx = xi - x0; fy = yi - y0
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    x0 = x0.astype(np.int64) % 256; y0 = y0.astype(np.int64) % 256
    a = G[x0, y0]; b = G[x0 + 1, y0]; c = G[x0, y0 + 1]; d = G[x0 + 1, y0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def sd_arc(px, py, cx, cy, r, a0, a1):
    ang = np.degrees(np.arctan2(py - cy, px - cx))
    rel = (ang - a0) % 360.0
    inside = rel <= (a1 - a0)
    d_ring = np.abs(np.hypot(px - cx, py - cy) - r)
    e0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    e1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    d_end = np.minimum(np.hypot(px - e0[0], py - e0[1]), np.hypot(px - e1[0], py - e1[1]))
    return np.where(inside, d_ring, d_end)


def glyph_S(gx, gz, a, t):
    gx = gx - 0.16 * gz                  # italic
    up = sd_arc(gx, gz, 0.0, a, a, 25.0, 270.0)
    lo = sd_arc(gx, gz, 0.0, -a, a, -155.0, 90.0)
    return np.minimum(up, lo) - 0.5 * t


SEVEN = [(-1.95, 3.0), (2.0, 3.0), (2.0, 1.95), (-0.2, -3.0), (-1.75, -3.0), (0.4, 1.7), (-1.95, 1.7)]


def glyph_7(gx, gz, h):
    s = h / 6.0
    gx = gx - 0.16 * gz                  # italic
    return sd_poly(gx / s, gz / s, SEVEN) * s


def stripe(x, z, z0, z1, xr, xf):
    k = math.sqrt(1 + TAMPO_SLANT ** 2)
    dz = np.abs(z - 0.5 * (z0 + z1)) - 0.5 * (z1 - z0)
    dxf = (x - (xf + TAMPO_SLANT * (z - 12.0))) / k
    dxr = ((xr + TAMPO_SLANT * (z - 12.0)) - x) / k
    return np.maximum(dz, np.maximum(dxf, dxr))


ROUNDEL = dict(x=2.6, z=19.6, r=4.8, ring=0.75)
BADGE = dict(x=-36.0, z=30.0, h=2.3)


def tampo_layers(region, P, rd):
    """Returns [(ink, sdf)] for one region; P = dict of car-space coordinate arrays; rd = reading
    direction along +x (-1 on the left side, +1 on the right side)."""
    L = []
    if region == 'side':
        x, z = P['x'], P['z']
        rnd = np.hypot(x - ROUNDEL['x'], z - ROUNDEL['z'])
        knock = rnd - (ROUNDEL['r'] + 0.45)             # stripes knocked out around the roundel
        for ink, z0, z1, xr, xf in (('white', 13.9, 17.5, -19.4, 22.6), ('yellow', 12.3, 13.1, -20.8, 21.2),
                                    ('red', 10.7, 11.5, -22.2, 19.8)):
            L.append((ink, np.maximum(stripe(x, z, z0, z1, xr, xf), -knock)))
        ring = np.maximum(rnd - ROUNDEL['r'], -(rnd - (ROUNDEL['r'] - ROUNDEL['ring'])))
        L.append(('red', ring))
        gx = (x - ROUNDEL['x']) * rd; gz = z - ROUNDEL['z']
        disc = np.maximum(rnd - (ROUNDEL['r'] - ROUNDEL['ring'] + 0.05), -glyph_7(gx, gz, 5.6))   # "7" knocked out
        L.append(('white', disc))
        bx = (x - BADGE['x']) * rd; bz = z - BADGE['z']
        L.append(('red', sd_rrect2(bx, bz, BADGE['h'], BADGE['h'], 0.8)))
        L.append(('white', glyph_S(bx, bz, 0.68, 0.62)))
    elif region == 'top':
        x, y = P['x'], P['y']
        ay = np.abs(y)
        k = 25.8
        cut = np.maximum(k - x, x - 54.0)
        L.append(('white', np.maximum(np.abs(ay - 4.5) - 2.1, cut)))
        L.append(('red', np.maximum(np.abs(ay - 7.75) - 0.4, cut + 0.6)))
    elif region == 'front':
        y, z = P['y'], P['z']
        ay = np.abs(y)
        L.append(('black', sd_rrect2(y, z - 17.3, 13.6, 2.75, 0.9)))
        L.append(('red', sd_rrect2(y, z - 17.3, 2.2, 0.85, 0.4)))
        L.append(('silver', sd_rrect2(ay - HL_Y, z - HL_Z, HL_HY - 0.35, HL_HZ - 0.35, 1.25)))
        L.append(('lens', np.hypot(ay - HL_DOMES[0][0], z - HL_Z) - (HL_DOMES[0][1] - 0.15)))
        L.append(('fog', np.hypot(ay - HL_DOMES[1][0], z - HL_Z) - (HL_DOMES[1][1] - 0.15)))
        L.append(('silver', np.maximum(np.abs(np.hypot(ay - HL_DOMES[0][0], z - HL_Z) - 0.7) - 0.18, 0.0 - 1.0)))
    elif region == 'rear':
        y, z = P['y'], P['z']
        ay = np.abs(y)
        L.append(('tail', sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY - 0.3, TL_HZ - 0.3, 1.0)))
        L.append(('amber', np.maximum(sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY - 0.3, TL_HZ - 0.3, 1.0), np.abs(ay - 28.9) - 1.0)))
        L.append(('white', np.maximum(sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY - 0.3, TL_HZ - 0.3, 1.0), np.abs(ay - 21.9) - 0.8)))
        L.append(('white', sd_rrect2(y, z - 18.6, 7.7, 1.9, 0.6)))
        L.append(('black', np.maximum(np.abs(sd_rrect2(y, z - 18.6, 7.7, 1.9, 0.6) + 0.25) - 0.18, -1.0)))
    return L


def make_tampo(path_rgba, path_metal, res=TAMPO_RES):
    """Rasterises the livery into the UV1 layout. Per-ink, per-side registration offsets
    (0.3-0.5 uu), wobbly print edges, density variation and pinholes."""
    t0 = time.time()
    u = (np.arange(res) + 0.5) / res
    U, V = np.meshgrid(u, u)                 # rows = v from the bottom (Blender image order)
    rgb = np.zeros((res, res, 3), np.float32)
    alpha = np.zeros((res, res), np.float32)
    metal = np.zeros((res, res), np.float32)
    px = 1.0 / (UV_S * res)                  # uu per pixel
    S = UV_S
    regions = [
        ('side', 'L', (U < 0.5) & (V < 0.22), dict(x=X_FRONT_UV - U / S, z=V / S), -1.0),
        ('side', 'R', (U >= 0.5) & (V < 0.22), dict(x=(U - 0.5) / S + X_REAR_UV, z=V / S), 1.0),
        ('top', 'T', (U < 0.5) & (V >= 0.64), dict(x=U / S + X_REAR_UV, y=42.0 - (1.0 - V) / S), 1.0),
        ('front', 'F', (U >= 0.55) & (U <= 0.9) & (V >= 0.25) & (V < 0.445), dict(y=(U - 0.55) / S - 42.0, z=(V - 0.25) / S), 1.0),
        ('rear', 'B', (U >= 0.55) & (U <= 0.9) & (V >= 0.45) & (V < 0.645), dict(y=42.0 - (U - 0.55) / S, z=(V - 0.45) / S), 1.0),
    ]
    rng = np.random.default_rng(1991)
    reg = {}
    for ink in INK:
        for side in ('L', 'R', 'T', 'F', 'B'):
            a = rng.uniform(0, 2 * math.pi); mag = rng.uniform(0.3, 0.5)
            reg[(ink, side)] = (mag * math.cos(a), mag * math.sin(a))
    reg[('white', 'L')] = reg[('white', 'R')] = (0.0, 0.0)          # white is the key plate
    for region, side, mask, P, rd in regions:
        idx = np.nonzero(mask)
        if len(idx[0]) == 0:
            continue
        Pm = {k: v[idx] for k, v in P.items()}
        keys = list(Pm.keys())
        a0, a1 = keys[0], keys[1]
        wob = 0.06 * (vnoise(Pm[a0] * 1.0, Pm[a1] * 1.0, 7, 0.35) - 0.5) + \
              0.03 * (vnoise(Pm[a0], Pm[a1], 11, 0.09) - 0.5)
        dens = 0.93 + 0.06 * vnoise(Pm[a0], Pm[a1], 3, 4.0)
        pin = (vnoise(Pm[a0], Pm[a1], 5, 0.07) > 0.972).astype(np.float32) * 0.5
        if region == 'side':     # tampo struggles to print into the door grooves
            gaps = np.minimum(np.abs(Pm['x'] - DOOR_FX), np.abs(Pm['x'] - DOOR_RX)) < 0.38
        else:
            gaps = np.zeros(len(idx[0]), bool)
        R_ = rgb[idx]; A_ = alpha[idx]; M_ = metal[idx]
        # evaluate each ink layer with its own registration offset
        for li, (ink, _) in enumerate(tampo_layers(region, Pm, rd)):
            dx, dz = reg[(ink, side)]
            Q = dict(Pm)
            Q[a0] = Pm[a0] - dx; Q[a1] = Pm[a1] - dz
            d = tampo_layers(region, Q, rd)[li][1] + wob
            cov = np.clip(0.5 - d / px, 0.0, 1.0) * dens * (1.0 - pin)
            cov = np.where(gaps, cov * 0.35, cov) * 0.97
            col = np.array(INK[ink], np.float32)
            R_ = col[None, :] * cov[:, None] + R_ * (1 - cov[:, None])
            M_ = (1.0 if ink in METAL_INKS else 0.0) * cov + M_ * (1 - cov)
            A_ = cov + A_ * (1 - cov)
        rgb[idx] = R_; alpha[idx] = A_; metal[idx] = M_
    # un-premultiplied colour where alpha > 0 is already straight (over-composite of opaque inks)
    def save(path, pix, ch):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        name = os.path.basename(path)
        im = bpy.data.images.get(name) or bpy.data.images.new(name, res, res, alpha=(ch == 4))
        if ch == 4:
            flat = np.concatenate([pix[0], pix[1][..., None]], 2)
        else:
            flat = np.repeat(pix[..., None], 4, 2); flat[..., 3] = 1.0
        im.pixels.foreach_set(flat.astype(np.float32).ravel())
        im.filepath_raw = path
        im.file_format = 'PNG'
        im.save()
        return im
    im = save(path_rgba, (rgb, alpha), 4)
    im2 = save(path_metal, metal, 1)
    log("tampo %dx%d written in %.1fs" % (res, res, time.time() - t0))
    return im, im2


# =============================================================================
#  Preview materials for this casting (UE gets slots + sidecar values)
# =============================================================================
def make_paint_material(tampo_path, metal_path):
    m, nt, bs = W._principled("Paint")
    L = nt.links.new
    N = nt.nodes.new
    tc = N('ShaderNodeTexCoord'); geo = N('ShaderNodeNewGeometry')
    uvm = N('ShaderNodeUVMap'); uvm.uv_map = "UV1"
    ti = N('ShaderNodeTexImage'); ti.image = bpy.data.images.load(tampo_path, check_existing=True)
    ti.extension = 'CLIP'; ti.interpolation = 'Cubic'
    mi = N('ShaderNodeTexImage'); mi.image = bpy.data.images.load(metal_path, check_existing=True)
    mi.image.colorspace_settings.name = 'Non-Color'; mi.extension = 'CLIP'
    L(uvm.outputs['UV'], ti.inputs['Vector']); L(uvm.outputs['UV'], mi.inputs['Vector'])
    # metallic flake: random per-cell normal tilt in the base layer (under the clearcoat)
    vor = N('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = 850.0
    L(tc.outputs['Object'], vor.inputs['Vector'])
    fl = N('ShaderNodeVectorMath'); fl.operation = 'MULTIPLY_ADD'
    L(vor.outputs['Color'], fl.inputs[0]); fl.inputs[1].default_value = (2, 2, 2); fl.inputs[2].default_value = (-1, -1, -1)
    fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; fs.inputs['Scale'].default_value = 0.12
    L(fl.outputs[0], fs.inputs[0])
    fa = N('ShaderNodeVectorMath'); fa.operation = 'ADD'
    L(geo.outputs['Normal'], fa.inputs[0]); L(fs.outputs[0], fa.inputs[1])
    fnrm = N('ShaderNodeVectorMath'); fnrm.operation = 'NORMALIZE'; L(fa.outputs[0], fnrm.inputs[0])
    # under tampo ink the flake tilt goes away (ink is flat)
    nmix = N('ShaderNodeMix'); nmix.data_type = 'VECTOR'
    L(ti.outputs['Alpha'], nmix.inputs['Factor']); L(fnrm.outputs[0], nmix.inputs[4]); L(geo.outputs['Normal'], nmix.inputs[5])
    L(nmix.outputs[1], bs.inputs['Normal'])
    # enamel orange peel on the clearcoat + a faint casting seam along the roof sides
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 150.0; nz.inputs['Detail'].default_value = 3.0
    L(tc.outputs['Object'], nz.inputs['Vector'])
    sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sep.inputs[0])
    seam = W._mrange(nt, W._math(nt, 'ABSOLUTE', W._math(nt, 'SUBTRACT', sep.outputs['Z'], 0.362)), 0.0, 0.0018, 1.0, 0.0)
    side_only = W._mrange(nt, W._math(nt, 'ABSOLUTE', sep.outputs['Y']), 0.20, 0.24, 0.0, 1.0)
    seam = W._math(nt, 'MULTIPLY', seam, side_only)
    h = W._math(nt, 'MULTIPLY_ADD', seam, 0.6, nz.outputs['Fac'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.09; bp.inputs['Distance'].default_value = 0.0004
    L(h, bp.inputs['Height'])
    L(bp.outputs['Normal'], bs.inputs['Coat Normal'])
    # paint pooling in recesses (darker) and thinning on the sharpest edges (lighter, a hint of zamac)
    ao = N('ShaderNodeAmbientOcclusion'); ao.only_local = True; ao.samples = 8
    ao.inputs['Distance'].default_value = 0.02
    pool = W._mrange(nt, ao.outputs['AO'], 0.25, 1.0, 0.58, 1.0)
    edge = W._mrange(nt, geo.outputs['Pointiness'], 0.55, 0.66, 0.0, 0.18)
    base = W._mixc(nt, edge, tuple(PAINT_LIN) + (1.0,), (0.30, 0.34, 0.42, 1.0))
    pm = N('ShaderNodeMix'); pm.data_type = 'RGBA'; pm.blend_type = 'MULTIPLY'; pm.inputs[0].default_value = 1.0
    L(base, pm.inputs[6]); L(pool, pm.inputs[7])
    # tampo over the paint
    col = W._mixc(nt, ti.outputs['Alpha'], pm.outputs[2], ti.outputs['Color'])
    L(col, bs.inputs['Base Color'])
    inkmet = W._math(nt, 'MULTIPLY', mi.outputs['Color'], 0.85)
    met = N('ShaderNodeMix'); met.data_type = 'FLOAT'
    L(ti.outputs['Alpha'], met.inputs['Factor']); met.inputs[2].default_value = 0.66; L(inkmet, met.inputs[3])
    L(met.outputs[0], bs.inputs['Metallic'])
    rough = N('ShaderNodeMix'); rough.data_type = 'FLOAT'
    L(ti.outputs['Alpha'], rough.inputs['Factor']); rough.inputs[2].default_value = 0.30; rough.inputs[3].default_value = 0.40
    L(rough.outputs[0], bs.inputs['Roughness'])
    coat = N('ShaderNodeMix'); coat.data_type = 'FLOAT'
    L(ti.outputs['Alpha'], coat.inputs['Factor']); coat.inputs[2].default_value = 1.0; coat.inputs[3].default_value = 0.4
    L(coat.outputs[0], bs.inputs['Coat Weight'])
    W._set(bs, 'Coat Roughness', 0.025); W._set(bs, 'Coat IOR', 1.52)
    m.diffuse_color = tuple(PAINT_LIN) + (1.0,)
    return m


def make_glass_material():
    """Thin light-smoke toy plastic: Fresnel mix of a tinted Transparent BSDF (lets the sun light
    the interior, ~0.68 per surface -> ~46 % through the piece) and a sharp gloss."""
    m = bpy.data.materials.get("Glass") or bpy.data.materials.new("Glass")
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tr.inputs['Color'].default_value = tuple(GLASS_TINT) + (1.0,)
    gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.025
    fr = nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.49
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(fr.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    try:
        m.surface_render_method = 'BLENDED'
    except Exception:
        pass
    m.diffuse_color = tuple(GLASS_TINT) + (0.5,)
    return m


def make_materials(tampo, metal):
    make_paint_material(tampo, metal)
    for s in ("Chrome", "Lamp", "Zamac", "Base", "Tire", "Hub"):
        W.make_slot_material(s)
    W.make_slot_material("Interior", interior=tuple(INTERIOR_LIN) + (1.0,))
    m = bpy.data.materials["Interior"]
    W._set(m.node_tree.nodes.get('Principled BSDF') or [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0],
           'Roughness', 0.48)
    make_glass_material()


# =============================================================================
#  Build all parts
# =============================================================================
def build_body(coll, q):
    cell = 0.5 if q else 0.25
    parts = []
    V, T, N = sdf_part("BodyShell", body_sdf, (-56.5, -43.5, 7.0), (60.5, 43.5, 44.5), cell,
                       target_tris=30000 if q else 64000)
    parts.append(dict(V=V, T=T, N=N, mat=0))
    g = rally_geo()
    c2 = 0.14 if q else 0.07
    lo = (RL_XB - 0.6, -RL_Y - RL_R - 0.6, g['zc'] - RL_R - 0.6)
    hi = (RL_XF + 0.9, RL_Y + RL_R + 0.6, g['zc'] + RL_R + 0.6)
    V, T, N = sdf_part("RallyPods", rally_pod, lo, hi, c2, 2600)
    parts.append(dict(V=V, T=T, N=N, mat=1))
    V, T, N = sdf_part("RallyLens", rally_lens, lo, hi, c2, 1200)
    parts.append(dict(V=V, T=T, N=N, mat=2, col=np.tile(list(RALLY_TINT) + [1.0], (len(V), 1))))
    lo = (BAR_X - 1.6, -RL_Y - 1.4, g['bar_z']); hi = (BAR_X + 1.9, RL_Y + 1.4, g['bar_z'] + 2.4)
    V, T, N = sdf_part("RallyStalks", rally_stalk, lo, hi, c2, 400)
    parts.append(dict(V=V, T=T, N=N, mat=3))
    return build_object("SM_HatchlingS_Body", parts, ["Paint", "Chrome", "Lamp", "Zamac"], coll)


def build_base(coll, q):
    cell = 0.44 if q else 0.22
    V, T, N = sdf_part("Base", base_sdf, (-58.0, -40.0, 0.5), (61.5, 40.0, 26.0), cell,
                       target_tris=8000 if q else 13500)
    col = np.zeros((len(V), 4)); col[:, 3] = 1.0
    for (rx, ry) in RIVETS:
        m = (np.hypot(V[:, 0] - rx, V[:, 1] - ry) < 2.25) & (V[:, 2] < Z_BOT + 0.4)
        col[m, 1] = 1.0
    parts = [dict(V=V, T=T, N=N, mat=0, col=col)]
    for xw in (X_FA, X_RA):
        Va, Ta, Na = cylinder_y(xw, AXLE_Z, AXLE_R, -(WHEEL_Y + 2.6), WHEEL_Y + 2.6, seg=16)
        ca = np.zeros((len(Va), 4)); ca[:, 0] = 1.0; ca[:, 3] = 1.0
        parts.append(dict(V=Va, T=Ta, N=Na, mat=0, col=ca, rake=False))
        for (Vh, Th, Nh) in axle_heads(xw, AXLE_Z, WHEEL_Y + W.AXLE_HEAD_Y_UU):
            ch = np.zeros((len(Vh), 4)); ch[:, 0] = 1.0; ch[:, 3] = 1.0
            parts.append(dict(V=Vh, T=Th, N=Nh, mat=0, col=ch, rake=False))
    return build_object("SM_HatchlingS_Base", parts, ["Base"], coll)


def build_interior(coll, q):
    cell = 0.56 if q else 0.28
    V, T, N = sdf_part("Interior", interior_sdf, (-42.0, -33.0, 9.6), (24.0, 33.0, 36.0), cell,
                       target_tris=5000 if q else 9000)
    return build_object("SM_HatchlingS_Interior", [dict(V=V, T=T, N=N, mat=0)], ["Interior"], coll)


def build_windows(coll, q):
    cell = 0.4 if q else 0.22
    V, T, N = sdf_part("Windows", glass_sdf, (-52.0, -37.0, 21.0), (27.0, 37.0, 39.0), cell,
                       target_tris=2000 if q else 2900)
    return build_object("SM_HatchlingS_Windows", [dict(V=V, T=T, N=N, mat=0)], ["Glass"], coll)


def body_misc_mask(cen):
    _, Om, _ = body_fields(cen[:, 0], cen[:, 1], cen[:, 2])
    inner = np.abs(Om + T_SHELL) < 0.35
    rim = cen[:, 2] < Z_SILL + 0.3
    return inner | rim


# =============================================================================
#  Export + sidecar
# =============================================================================
def write_sidecar(objs, path, tris, tampo_rel, metal_rel):
    allv = []
    for ob in objs:
        co = np.empty(len(ob.data.vertices) * 3); ob.data.vertices.foreach_get("co", co)
        allv.append(co.reshape(-1, 3) / UU)
    allv = np.concatenate(allv)
    mn, mxv = allv.min(0), allv.max(0)
    mn[2] = 0.0
    wy = max(mxv[1], WHEEL_Y + WHEEL_WD / 2); mn[1] = min(mn[1], -wy); mxv[1] = max(mxv[1], wy)
    ue = lambda p: [round(float(p[0]), 3), round(float(-p[1]), 3), round(float(p[2]), 3)]
    g = rally_geo()
    data = {
        "casting": "HatchlingS",
        "display_name": "Hatchling S",
        "nickname_1A": "Old Faithful",
        "class": "Compact",
        "brand": "STREAKLINE",
        "casting_year": 1991,
        "units": "uu, UE axes (X forward, Y right, Z up); origin at ground level centred between the axles",
        "length": round(float(mxv[0] - mn[0]), 2),
        "width": round(float(mxv[1] - mn[1]), 2),
        "height": round(float(mxv[2] - mn[2]), 2),
        "bounds_min": ue([mn[0], mxv[1], mn[2]]),
        "bounds_max": ue([mxv[0], mn[1], mxv[2]]),
        "roof_height": round(g['roof'], 2),
        "hitbox": HITBOX,
        "wheel_design": "W01_Dish",
        "wheel_mesh": "SM_Wheel_W01_Dish",
        "wheel_radius": WHEEL_R,
        "wheel_width": WHEEL_WD,
        "wheelbase": X_FA - X_RA,
        "track": 2 * WHEEL_Y,
        "wheels": {
            "FL": ue([X_FA, WHEEL_Y, AXLE_Z]), "FR": ue([X_FA, -WHEEL_Y, AXLE_Z]),
            "RL": ue([X_RA, WHEEL_Y, AXLE_Z]), "RR": ue([X_RA, -WHEEL_Y, AXLE_Z]),
        },
        "wheel_outer_face": "W01 mesh is authored with its show face on Blender +Y (= UE -Y, left). Left wheels (FL, RL) as-is; right wheels (FR, RR) yaw 180 deg.",
        "wheel_cosmetic_wobble_deg": {k: {"camber": v[0], "toe": v[1]} for k, v in WHEEL_WOBBLE.items()},
        "wheel_wobble_note": "spec 4b rule 3: tiny per-wheel camber/toe imperfection, cosmetic only (apply to the wheel mesh component, not to physics)",
        "wheel_arch": {"radius": ARCH_R, "centre_z": ARCH_Z, "gap_front": 2.8, "gap_rear": 3.4,
                       "note": "toy ride height; the wheel may travel ~2.5 uu up before touching the arch"},
        "stance": {"rake_deg": RAKE_DEG, "pivot_z": AXLE_Z,
                   "note": "body, base, windows and interior meshes are already pitched nose-down by rake_deg about the axle line; do not add it again"},
        "axles": {"radius": AXLE_R, "z": AXLE_Z, "x": [X_FA, X_RA], "half_length": WHEEL_Y + 2.6, "part": "Base",
                  "vertex_color": "R", "heads": {"y": round(WHEEL_Y + W.AXLE_HEAD_Y_UU, 2), "radius": 1.32,
                  "note": "peened steel heads sit in the W01 hub bores; keep wheel centres at the sidecar positions (no visual suspension travel), or they float"}},
        "base_band": {"z": [Z_BOT, Z_SILL], "inset": BAND_INSET,
                      "note": "black plastic band visible under the body sill in side view (spec 4b rule 4)"},
        "parts": {"Body": "SM_HatchlingS_Body", "Base": "SM_HatchlingS_Base",
                  "Windows": "SM_HatchlingS_Windows", "Interior": "SM_HatchlingS_Interior"},
        "slots": {"Body": ["Paint", "Chrome", "Lamp", "Zamac"], "Base": ["Base"],
                  "Windows": ["Glass"], "Interior": ["Interior"]},
        "slot_use": {"Paint": "the whole casting incl. cast lamp bosses, grille grooves, mirror nubs and the roof lamp bar (lamps/grille are coloured by the tampo)",
                     "Chrome": "rally lamp pods", "Lamp": "rally lamp lenses (amber via Col)", "Zamac": "bare lamp stalks"},
        "feature": {"type": "MoodPaint", "panel": "roof",
                    "panel_center": ue([MOOD["cx"], MOOD["cy"], 40.0]),
                    "panel_extent": [MOOD["hx"], MOOD["hy"]],
                    "panel_corner_radius": MOOD["r"],
                    "panel_uv1_rect": mood_uv1_rect(),
                    "note": "engraved rounded-rectangle panel on the roof between the roof scoop and the spoiler; mask it in M_ToyPaint with panel_uv1_rect (u0,v0,u1,v1); the tampo leaves it clear"},
        "rally_lamps": {"count": 2, "radius": RL_R,
                        "lens_centres": [ue([RL_XF, RL_Y, g['zc']]), ue([RL_XF, -RL_Y, g['zc']])],
                        "top_z": round(g['top'], 2),
                        "note": "pods on a bar cast into the roof front; they stand above the 40 uu hitbox (visual only)"},
        "headlamps": {"type": "cast bosses printed by the tampo (silver bezel, white main lamp, yellow driving lamp)",
                      "centres": [ue([nose_x(HL_Z), HL_Y, HL_Z]), ue([nose_x(HL_Z), -HL_Y, HL_Z])],
                      "half_size_yz": [HL_HY, HL_HZ]},
        "tail_lamps": {"type": "cast bosses printed by the tampo (red, amber, white)",
                       "centres": [ue([tail_x(TL_Z), TL_Y, TL_Z]), ue([tail_x(TL_Z), -TL_Y, TL_Z])],
                       "half_size_yz": [TL_HY, TL_HZ]},
        "vertex_color": {"Body": "Col on the Lamp slot: amber (1,0.70,0.16) = rally lamps; white elsewhere. Multiply the Lamp colour by it",
                         "Base": "Col: R = steel axles + peened heads, G = rivet heads, black = moulded black plastic base"},
        "uv": {"UV0": "smart unwrap per part, non-overlapping (wear / grain masks)",
               "UV1": "tampo layout in the un-raked casting frame (uniform scale 0.5/120 per uu): left side U0-0.5 V0-0.2 (front at U0, as seen from the left), right side U0.5-1 V0-0.2 (front at U1), top strip U0-0.5 V0.65-1 (U rear->front from x=-58.5, V = 1-(42-y)/240), front island U0.55-0.9 V0.25-0.445 (U from the car's right to left, V by height), rear island U0.55-0.9 V0.45-0.645 (U from left to right as seen from behind), inside/underside parked in U0.92-1 V0.92-1"},
        "default_variant": "OldFaithful",
        "variants": {
            "OldFaithful": {
                "card": "Summer Starter - Old Faithful (owned, loose)",
                "paint": {"name": "Streak Blue metallic", "base_color_srgb": PAINT_SRGB, "base_color_linear": list(PAINT_LIN),
                          "finish": "metallic enamel, fine visible flake, mild orange-peel gloss clearcoat (coat roughness ~0.025)",
                          "metallic": 0.66, "roughness": 0.30},
                "tampo": {"texture": tampo_rel, "metal_mask": metal_rel, "uv": "UV1",
                          "inks": {k: [round(c, 3) for c in v] for k, v in INK.items()},
                          "design": "1991 rally-hatch: white side band with yellow + red pinstripes (italic cut), red-ringed white door roundel with a knocked-out '7', red 'S' casting badge on the C-pillar, white twin bonnet stripes with red pinstripes, printed silver/white/yellow headlamps, black grille, red/amber/white tail lamps, white rear plate",
                          "flaws": "0.3-0.5 uu per-ink registration offsets, wobbly edges, density variation, pinholes, thin print in the door grooves",
                          "blend": "alpha = ink coverage; ink is matte-ish (roughness ~0.4, clearcoat reduced), metal_mask R = metallic silver ink"},
                "interior": {"color_linear": list(INTERIOR_LIN), "name": "tan"},
                "windows": {"tint_per_surface_linear": list(GLASS_TINT), "transmission_through_piece": 0.50,
                            "thickness": GLASS_T, "note": "light-smoke clear plastic; the interior must stay clearly visible"},
                "base": "black plastic (Col R/G steel)",
                "wheels": "W01_Dish chrome hub / black ring",
            }
        },
        "base_decal_area": {"center": ue([TEXT_AREA["cx"], TEXT_AREA["cy"], Z_BOT]), "extent": [TEXT_AREA["hx"], TEXT_AREA["hy"]],
                            "text": "STREAKLINE \u00b7 HATCHLING S \u00b7 1991 \u00b7 MADE IN ...", "note": "recessed plain panel on the underside for a decal"},
        "rivets": [ue([rx, ry, Z_BOT]) for (rx, ry) in RIVETS],
        "tris": tris,
        "nanite": {"Body": True, "Base": True, "Windows": False, "Interior": True},
        "export": "FBX per part, Blender metres at game scale (1 m = 100 uu), axis_forward X, axis_up Z",
        "source": "SourceArt/Blender/HatchlingS/build_HatchlingS.py (rev 2, spec 4b)",
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log("sidecar", path)
    return data


# =============================================================================
#  Previews  (Navvy stage; identical camera / light / deck conventions)
# =============================================================================
SHOTS = {
    'hero_34_front': dict(az=34.0, el=9.5, dist=6.0, lens=100, target=(0.08, 0.0, 0.17), focus=(0.46, 0.34, 0.15),
                          fstop=0.7, sun=(-12.0, 24.0)),
    'family_navvy': dict(az=30.0, el=10.0, dist=8.8, lens=100, target=(-0.30, 0.56, 0.19), focus=(-0.05, 0.25, 0.17),
                         fstop=2.8, sun=(-12.0, 24.0), navvy=True),
    'detail_34_front': dict(az=34.0, el=13.0, dist=4.4, lens=100, target=(0.06, 0.0, 0.19), focus=(0.18, 0.3, 0.2),
                            fstop=4.0, sun=(-12.0, 24.0)),
    'side_profile': dict(az=90.0, el=3.0, dist=8.2, lens=135, target=(0.02, 0.0, 0.21), focus=(0.0, 0.41, 0.18),
                         fstop=2.0, sun=(48.0, 28.0)),
    'rear_34': dict(az=-138.0, el=11.0, dist=6.6, lens=100, target=(-0.04, 0.0, 0.2), focus=(-0.50, -0.37, 0.2),
                    fstop=0.9, sun=(-150.0, 26.0)),
    'top_down': dict(top=True, dist=6.4, lens=100, target=(0.02, 0.0, 0.0), focus=(0.0, 0.0, 0.40), fstop=5.6,
                     sun=(110.0, 42.0)),
    'underside': dict(under=True, az=-30.0, el=-62.0, dist=6.8, lens=100, target=(0.02, 0.0, 0.10),
                      focus=(0.0, 0.0, 0.05), fstop=4.0, sun=(90.0, -20.0)),
    'windscreen_34': dict(az=22.0, el=19.0, dist=3.0, lens=100, target=(-0.02, 0.0, 0.27), focus=(-0.02, 0.0, 0.26), fstop=5.6,
                          sun=(-12.0, 40.0)),
    'wheel_close': dict(az=62.0, el=10.0, dist=2.6, lens=100, target=(X_FA * UU, WHEEL_Y * UU, AXLE_Z * UU),
                        focus=(X_FA * UU, (WHEEL_Y + 4) * UU, AXLE_Z * UU), fstop=2.2, sun=(80.0, 28.0)),
}
DEFAULT_SHOTS = ['hero_34_front', 'family_navvy', 'detail_34_front', 'side_profile', 'rear_34', 'top_down',
                 'underside', 'wheel_close']


def place_preview_wheels(coll, wheel_ob):
    out = []
    for key, (x, y) in {"FL": (X_FA, WHEEL_Y), "FR": (X_FA, -WHEEL_Y),
                        "RL": (X_RA, WHEEL_Y), "RR": (X_RA, -WHEEL_Y)}.items():
        o = bpy.data.objects.new("PV_Wheel_" + key, wheel_ob.data)
        W.link(o, coll)
        o.location = (x * UU, y * UU, AXLE_Z * UU)
        cam, toe = WHEEL_WOBBLE[key]
        sgn = 1.0 if y > 0 else -1.0
        o.rotation_euler = (math.radians(cam) * sgn, 0.0, (0.0 if y > 0 else math.pi) + math.radians(toe))
        out.append(o)
    return out


def render_previews(sc, car_objs, wheel_ob, shots):
    W.stage_setup_render(sc, samples=OPT['samples'], pct=OPT['pct'])
    rig = W.stage_setup(sc)
    pcoll = W.get_coll("Preview")
    place_preview_wheels(pcoll, wheel_ob)
    nv = None
    pv = os.path.join(HERE, "preview")
    os.makedirs(pv, exist_ok=True)
    for name in shots:
        cfg = SHOTS[name]
        if cfg.get('navvy') and nv is None:
            nv = W.import_navvy(location=(-0.58, 1.18, 0.0), yaw_deg=0.0)
        if nv is not None:
            for o in nv.children:
                o.hide_render = not cfg.get('navvy', False)
        W.stage_render(sc, rig, cfg, os.path.join(pv, "HatchlingS_" + name + OPT['suffix'] + ".png"))


# =============================================================================
#  Main
# =============================================================================
def main():
    t0 = time.time()
    q = OPT['quick']
    sc = W.reset_scene()
    tex = os.path.join(HERE, "textures")
    tampo_p = os.path.join(tex, "T_HatchlingS_OldFaithful_Tampo.png")
    metal_p = os.path.join(tex, "T_HatchlingS_OldFaithful_TampoMetal.png")
    make_tampo(tampo_p, metal_p, res=1024 if q else TAMPO_RES)
    make_materials(tampo_p, metal_p)
    coll = W.get_coll("HatchlingS")
    log("building body ...")
    body = build_body(coll, q)
    log("building base ...")
    base = build_base(coll, q)
    log("building interior ...")
    interior = build_interior(coll, q)
    log("building windows ...")
    windows = build_windows(coll, q)
    log("uvs ...")
    do_uvs(body, body_misc_mask)
    do_uvs(base, lambda c: c[:, 2] > Z_SILL + 0.6)
    do_uvs(interior, lambda c: c[:, 2] < 10.0)
    do_uvs(windows)
    tris = {ob.name: W.tri_count(ob) for ob in (body, base, windows, interior)}
    log("tris:", tris)
    wcoll = W.get_coll("Wheel_W01_Dish (reference)")
    wheel = W.build_wheel(coll=wcoll)
    W.wheel_uvs(wheel)
    wheel.hide_render = True
    if OPT['export']:
        exp = os.path.join(HERE, "export")
        for ob in (body, base, windows, interior):
            W.export_fbx(ob, os.path.join(exp, ob.name + ".fbx"))
        write_sidecar((body, base, windows, interior), os.path.join(HERE, ASSET + ".json"), tris,
                      "SourceArt/Blender/HatchlingS/textures/T_HatchlingS_OldFaithful_Tampo.png",
                      "SourceArt/Blender/HatchlingS/textures/T_HatchlingS_OldFaithful_TampoMetal.png")
    if OPT['render']:
        render_previews(sc, (body, base, windows, interior), wheel, OPT['shots'] or DEFAULT_SHOTS)
    if OPT['export']:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"), compress=True)
    log("done in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
