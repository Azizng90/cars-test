"""
build_HatchlingS.py  -  MODEL '93 / CozyCarGame, Slice 1A                 (rev 9, spec 4b)
=========================================================================================
Die-cast casting "Hatchling S" (STREAKLINE, 1991 casting; the player's "Old Faithful").
Class Compact, hitbox 112 x 84 x 40 uu, wheels W01_Dish (era one-piece plastic wheels).

Rev 10 (17 Oct, Opus rear pass 5b - the r5 gate's fixes 1-7, Docs/Build/progress/opus-rear-r5-HatchlingS.md):
  * Fixes 1/2: ONE-PIECE REAR QUARTER - behind x -33.5 the quarter is the lower body widened to the flare width and
    narrowed back by a long C2 taper (x -41.5..-52), not the flare exact-unioned onto the body (that left a vertical
    concave crease between two humps behind each rear arch and a braided double highlight on the hip). One top surface,
    one constant 2.6 uu roll from the C-pillar foot to the tail corner; deck morph C2 over 5.5 uu.
  * Fix 3: the tailgate side lines end on round caps half-way over the tail-top roll (no knot at the hatch-foot cove).
  * Fixes 4/5/7: local refinement after the export collapse (REFINE_ZONES: tail face, tail top, tail notch, side-pane
    bottoms); tail-notch rounds 1.4/1.5 (base 1.2); side panes 0.38 uu inside the shell and 1.0 deeper under the sill.
  * Fix 6 (tampo ruling): the plate is a RAISED 0.3 uu cast boss (printed on its top face), the '9' is one stroke.

Rev 9 (17 Oct, Opus rear pass 5 - round 4 review fixes + the r5 spike/notch gate, Docs/Build/progress/opus-rear-r5-HatchlingS.md):
  * Fix 1, shoulder: the rear flare top stood 0.55 uu over the lower-body top and the 2.2 union of those two near-parallel
    surfaces BULGED into a plateau beside the C-pillar with a kink outboard (two facets = the doubled S-badge image, the
    kink = the hard-edged dark band). Over the rear flare the lower-body top is raised to the SAME shoulder surface as the
    flare top (rq_top, outer skin only) and the two are joined by an exact union; the flare crown runs in under the pillar,
    the pillar-foot cove is the lower body / greenhouse cove (om_r 1.1-1.7; a 3.0 cove mirrored the badge as a second
    streak), and behind the pillar the crown MORPHS into the
    tail-deck surface with an exact union (flare_union_r): one cove + one convex crown, nothing coincident filleted.
  * Fixes 2/3/5, tail corner: the rev 8 corner tuck (blended fields = the pinched lump) and the rev 7 lower-only flare tuck
    (the 'fins') are gone. The rear flare ends behind the wheel in a full-height tangential taper into the body side, so
    the corner drops straight like the R5 casting; a clean subtractive TAIL NOTCH (|y| 30 + 45 deg chamfer, below the
    lamps) and an opened rear well (base out to the liner back wall, liner ring open behind the tyre below z 14) show the
    axle stub between tyre and body from a 3/4-rear view at axle height (lead ruling on rule 14). Liners = one smooth cup.
  * Fix 4: the tailgate outline's bottom sits on the bumper cove (side lines run into the ledge, no pit); plate recess
    walls soft (1.5). Fix 5: the hidden greenhouse cut moved under the hatch-foot cove (the second hatch line).
  * r5 gate (spike/notch 0 on every part): cabin_field() for every internal offset (no hidden greenhouse floor: it left a
    knife-thin film across the cabin and cut the front seat backs / wheel rim away); flat-slab window panes; door, bonnet
    and mood-panel lines as soft dents (bonnet one closed outline); filleted one-piece interior (wheel = rim over a disc);
    rounded scoop mouth, rally pods/lenses, bumper dents, liner caps, exhaust tip; interior budget 60k.

Rev 8 (17 Oct, Opus rear pass 4 - round 3 review fixes): the 'weird black' pinch at each tail shoulder came from HIDDEN
greenhouse geometry (the hatch plane and floor carried on under the deck to ~1 uu inside the tail-top round) and the
rear flare's flat pad (a hard inner wall at |y| 28 standing 0.3-0.4 proud of the deck); the round unions 'saw' both and
pushed lumps / a diagonal slit / a step into the skin. Now the greenhouse is cut 2.4 uu inside the tail (GH_CUT_X), the
deck cove is 1.7 (radii ramp over 9 uu, no hard x switch), and the rear flare top is ONE convex crown that settles onto the
tail deck behind the C-pillar (no pad, no wall, no second facet for the badge to mirror in). Shut lines are 1.4 uu soft
dents with 1.5+ uu of land to the lamp lenses, running straight over the tail top into the glass opening (no fade ramp).
Lamp bosses end inside the zamac wall. The rear corners tuck in behind the rear wheels (|y| 32.3 below z 12, chamfered out
under the lamps; thick cast corner; base lip and liners follow) so the rear tyres show at the chase camera. Interior: the
C-pillar quarter trim fills that window as a set-back charcoal moulding with an arm-rest crease. Front of x -36 the body
and interior fields are unchanged.

Rev 7 (17 Oct, Opus rear pass 3 - round 2 review fixes): hatch shut lines + plate panel are soft bell-profile DENTS on
the outer field (no zig-zag boolean lips, no blob ends); rear bumper crease 0.5 -> 1.1 and the deck/hatch cove 1.1 -> 3.0
behind x -40; the greenhouse floor is a rounded intersection behind x -38 (it printed a C0 crease across the tail top);
rear flares tuck inboard behind the rear wheels and the bumper sits flush with the body sides, so the rear tyres show
from the chase camera; the interior clip uses the true cabin field behind x -13 (the old union field shaved the rear
bench into a plank) plus rear side trim / arch humps / a quarter trim rail behind the C-pillar window; mid-dark
charcoal tub; UV1 side band carries the stripes over the front-arch step. Front of x -13 the body/interior fields are
bit-identical to rev 6.

Rev 6 (16-17 Oct, Opus rear pass 2, spec 4b rules 11-16): paint wraps the tail to z 4.4 over a cast body-colour
bumper (2.4 uu black lip, one zamac exhaust tip); geometry faults fixed at the source (door-front groove run-out, sealed
void in the base, knife-thin wheel-well liner clips, ringed axle tubes welded to the peened heads); preview glass
without back-face Fresnel so the dark tub reads through the rear window. Export ONLY through
Tools/Assembly/blender_export_casting.py (clean topology + spec rule 16 health gate).

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
    o = dict(quick=False, render=True, export=True, shots=None, pct=100, samples=96, suffix='', wip=None)
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
        elif a == '--wip': o['wip'] = os.path.abspath(argv[i + 1]); o['export'] = False; i += 1   # look-dev: no export
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
# rev 5 (Opus rear pass, spec 4b rules 11-15): the TAIL is body colour down to Z_RR over a cast body-colour bumper;
# the base shows at the back only as a thin black lip tucked under it, with one small bare-zamac exhaust tip.
# rev 6 (Opus rear pass 2): the paint comes 1 uu lower (Z_RR 5.4 -> 4.4, R5 reference: paint wraps almost to the
# ground) so the black lip shows only 2.4 uu; the bumper top follows down (12.4 -> 11.4) so the cast bumper keeps its
# 7 uu band; the exhaust tip sits lower, under the new bumper edge (its end stays at x -54.6: sidecar length unchanged).
Z_RR = 4.4                           # body skin bottom edge at the tail (sides keep Z_SILL)
RR_X0, RR_X1 = -48.6, -50.6          # x range over which the skin edge drops from Z_SILL to Z_RR (hidden by the arch)
RB_P, RB_Z1, RB_SIDE = 1.5, 11.4, -0.4  # rear bumper: proud of the tail panel, top z, vs the body sides (rev 7: 0.5 -> -0.4,
#   flush with the tucked-under body side so the rear tyres show beside it from the chase camera, spec 4b rule 14)
LIP_TOP, LIP_OUT = Z_RR + 1.5, 0.3   # base lip top (inside the shell) and how far it stands out of the tail-panel line
EXH_Y, EXH_Z, EXH_R, EXH_BORE = -19.0, 3.2, 1.25, 0.6    # exhaust tip (Blender -Y = car's right); rev 9: wall 0.36 -> 0.65
EXH_X0, EXH_X1 = -49.0, -54.6        # exhaust tip runs out from under the base to just past the bumper face
RAKE_DEG = 0.5                       # toy rake: nose down about the axle line
GLASS_T, GLASS_GAP = 2.3, 0.08       # window piece thickness, gap to the shell
HITBOX = {"center": [2.0, 0.0, 20.0], "extent": [56.0, 42.0, 20.0]}   # 112 x 84 x 40 (spec)

# Old Faithful default livery (spec: NOT red - the Vortex is red)
PAINT_LIN = (0.012, 0.088, 0.40)     # period metallic "Streak Blue"
PAINT_SRGB = "#1C53AA"
INTERIOR_LIN = (0.11, 0.11, 0.115)   # rev 8: 0.16 -> 0.11 (round 3 review: the lit quarter trim read greige). rev 7: mid-dark charcoal one-colour tub (spec 4b rule 13; round 2 review fix 1: the
#   rev 5 near-black 0.04 tub vanished behind the 50 % window piece - no seat shapes at chase distance)
#   = UE MI_ToyPlastic_InteriorCharcoal (Tools/Assembly/import_castings.py INTERIORS['Charcoal'])
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
TOPX = Prof([-57, -45, -20, 0, 20, 30, 45, 60], [25.45, 25.4, 24.9, 24.6, 24.2, 23.8, 23.0, 21.6])   # rev 9: tail key 25.6 -> 25.45
#   (the deck rose 0.15 toward the tail, so behind the C-pillar the shoulder, morphing down to it, left a shallow trough:
#   a jagged reflection line across the hip in the paint proof; the tail top is now <= 0.12 uu lower, flat)
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


def _s5(t):
    """C2 smootherstep 0 -> 1 (zero slope AND zero curvature at both ends: no curvature jump for the zebra to show)"""
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (6.0 * t - 15.0) + 10.0)


def _ds5(t):
    t = np.clip(t, 0.0, 1.0)
    return 30.0 * t * t * (1.0 - t) * (1.0 - t)


# rev 10 (r5 gate fixes 1 + 2): ONE-PIECE REAR QUARTER. Behind the rear flare's front end the quarter used to be the rear
# flare (|y| 41) exact-unioned onto the narrower lower body: its side tapered into the body side over 2.8 uu (a 4 uu step
# = a vertical concave crease between two humps: the zebra bullseye pair / blue curvature band behind each rear arch) and
# its top round ran almost coincident with the body's (two near-parallel rounded edges swapping = the braided highlight on
# the hip). Now behind x -33.5 the quarter is the lower body itself with its plan widened to the flare width (FLARE_W)
# and narrowed back to the body side by a long C2 taper (XQ0 -> XQ1): one side, one top (the rq_top shoulder surface),
# one constant 2.6 uu top roll from the C-pillar foot to the tail corner, no union of near-coincident surfaces.
XQ0, XQ1 = -41.5, -52.0               # the quarter's flare width tapers (C2) into the body side between these x


def flare_w(z):
    return 41.0 - (z - 10.0) * 0.07       # the rear flare's side (unchanged)


def lower_plan(x, y, z, wide=False):
    W_ = WPLAN(x) + WSEC(z)
    if wide:
        Lq = XQ0 - XQ1
        t = (XQ0 - x) / Lq
        s, ds = _s5(t), _ds5(t)
        D = flare_w(z) - W_
        dWx = WPLAN.d(x) * s + D * ds / Lq
        dWz = WSEC.d(z) * s - 0.07 * (1.0 - s)
        W_ = W_ + D * (1.0 - s)
        side = (np.abs(y) - W_) / np.sqrt(1 + dWx ** 2 + dWz ** 2)
    else:
        side = (np.abs(y) - W_) / np.sqrt(1 + WPLAN.d(x) ** 2 + WSEC.d(z) ** 2)
    d = i_round(side, (x - nose_x(z)) / 1.005, 6.0)
    return i_round(d, (tail_x(z) - x) / 1.0018, 4.0)   # rev 9: tail corner 5.0 -> 4.0 (the flare no longer widens it: keep the
    #   tail-lamp ends on the flat of the tail, 1 uu clear of the corner round)


# rev 9 (round 4 review fix 1 - the doubled badge reflection / dark band / C-pillar-foot dash): over the rear quarter the
# rear flare's top stood only ~0.55 uu above the lower-body top, and the 2.2 uu union of two near-parallel surfaces that
# close BULGES (it raised a flat 27.1 uu plateau between the C-pillar foot and |y| 35.5, then a kink down to the flare
# crown): two facets = two mirror images of the S badge, the kink = the hard-edged dark band. Over the rear flare the
# lower-body top is now RAISED to the very same shoulder surface (rq_top) and the two are joined by an exact union
# (flare_union_r), so the shoulder is one convex crown from the C-pillar-foot cove (the body/greenhouse cove, om_r) to the
# arch lip, morphing into the tail deck behind the pillar. Outer skin only (not the cavity / clips).
RQ_XF0, RQ_DXF = -30.0, 4.0           # the shared shoulder surface / exact union fade out ahead of x -30 (gone by -26)


RQ_X0, RQ_DX = -42.5, 9.3             # rev 10: the morph runs from x -42.5 right to the tail face (-51.8) as t^3


def rq_morph(x):
    """0 beside the C-pillar, 1 at the tail face: the rear flare's top becomes the tail-deck surface.
    rev 10 (r5 gate fixes 1/2): t^3 instead of a smoothstep ending flat at x -47.5 (r9) / -48 (r10 probe): there the hip
    crest dropped 0.3 uu and then levelled out again before the tail-top roll, so its normal tilted back, then up, then
    back into the roll = TWO reflections of the same thing along the hip (the zebra bullseye pair at shoulder_R px
    390/554, 472). With t^3 the crest's backward tilt grows monotonically into the tail-top roll (one reflection), the
    start is C2 (no curvature step) and the deck height is reached at the tail face."""
    t = np.clip((RQ_X0 - np.asarray(x, float)) / RQ_DX, 0.0, 1.0)
    return t * t * t


def rq_front(x):
    """1 behind x -28, 0 ahead of -25.5 (the rear flare's front end)"""
    return _smooth01((RQ_XF0 + RQ_DXF - np.asarray(x, float)) / RQ_DXF)


def rq_top(x, y):
    """the rear-quarter shoulder height H(x, y) and dH/d|y|: the rear flare's crown beside the C-pillar, morphing into the
    tail-deck surface behind it (rq_morph). Used for BOTH the flare's top and (over the flare) the lower body's top."""
    ay = np.abs(y)
    h, dh = rear_flare_top(ay)
    s_ = rq_morph(x)
    c_ = CROWN(x)
    h = h + s_ * ((TOPX(x) + c_ * (1.0 - (y / 38.0) ** 2)) - h)
    dh = (1.0 - s_) * dh + s_ * (-2.0 * c_ * ay / 1444.0)
    return h, dh


RQP_X0, RQP_X1 = -29.5, -33.5         # rev 10: hand-over from the flare union to the one-piece rear quarter (C2)


def rq_piece(x):
    """0 ahead of x -29.5, 1 behind x -33.5 (the C-pillar foot starts at x ~-34): the one-piece rear quarter's weight"""
    return _s5((RQP_X0 - np.asarray(x, float)) / (RQP_X0 - RQP_X1))


def flare_union_r(x):
    """flare / outer-master union radius: 2.2 at the front flare and the rear flare's front end; ~0 (an EXACT union) over
    the rear quarter, where the lower body's top is raised to the very same shoulder surface as the flare's top
    (lower_body(..., shoulder=True)). Two coincident or near-parallel surfaces must never be fillet-unioned: that is what
    bulged into the r4 plateau (two facets = two badge images). The C-pillar-foot cove is then the lower body / greenhouse
    cove (om_r), continuous all along the pillar and round its rear end."""
    f = rq_front(x)
    return 2.2 * (1.0 - f) + 0.05 * f


# rev 11 (gate leftover: the shoulder-shelf knot in front of the C-pillar): the lower body's top now rises to the
# shoulder surface from x -21 (C2 over 4.7 uu, i.e. along the rear flare's front-top round, which then lies just under
# it) instead of between x -26 and -30 behind that round, where the flat flare crown and the lower top ran 0.8 apart
# under a 2.2 union and bulged into a 0.17 uu dome. See _rear_flare_front_r for the union radius.
RF2_X0, RF2_DX = -21.0, 4.7


def rq_front2(x):
    return np.maximum(rq_front(x), _s5((RF2_X0 - np.asarray(x, float)) / RF2_DX))


def _shoulder_top(x, y):
    """rev 9/10: the lower body's top with the rear-quarter shoulder surface (rq_top) over the rear flare"""
    c = CROWN(x)
    top = TOPX(x) + c * (1.0 - (y / 38.0) ** 2)
    H, _ = rq_top(x, y)
    return top + rq_front2(x) * _smooth01((np.abs(y) - 24.5) / 2.0) * (H - top)   # ramp under the pillar (|y| < 31)


def lower_body(x, y, z, floor=True, shoulder=False, wide=False):
    c = CROWN(x)
    top = TOPX(x) + c * (1.0 - (y / 38.0) ** 2)
    nrm = np.sqrt(1 + TOPX.d(x) ** 2 + (2 * c * y / 1444.0) ** 2)
    if shoulder:      # rev 9: over the rear flare the top IS the shoulder surface (outer skin only)
        top = _shoulder_top(x, y)
        # rev 10: behind x -25.4 the top is normalised by its true slope (the shoulder crown / deck morph slopes in x and
        # |y|; the analytic term ignored them, so the 2.6 top roll changed radius along the hip). Ahead of it, where the
        # shoulder ramp is 0 and the crown constant, the numeric and analytic slopes agree: the front is untouched.
        m = np.asarray(x) < -25.4
        if np.any(m):
            xm, ym, e = x[m], y[m], 0.05
            gx = (_shoulder_top(xm + e, ym) - _shoulder_top(xm - e, ym)) / (2 * e)
            gy = (_shoulder_top(xm, ym + e) - _shoulder_top(xm, ym - e)) / (2 * e)
            nrm = np.array(nrm, float, copy=True)
            nrm[m] = np.sqrt(1 + gx * gx + gy * gy)
    d_top = (z - top) / nrm
    A = i_round(lower_plan(x, y, z, wide=wide), d_top, 2.6)
    return np.maximum(A, 4.0 - z) if floor else A


def _smooth01(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def zclip(x):
    """rev 5: body skin bottom edge - Z_SILL along the sides (unchanged), Z_RR across the tail. The drop happens
    between RR_X0 and RR_X1, i.e. inside the rear wheel arch, so the side view in front of the arch is untouched."""
    return Z_SILL + (Z_RR - Z_SILL) * _smooth01((RR_X0 - np.asarray(x, float)) / (RR_X0 - RR_X1))


def rear_bumper(x, y, z):
    """rev 5: cast body-colour rear bumper - the tail plan pushed back RB_P (and RB_SIDE proud of the body sides),
    a band from the skin edge Z_RR to RB_Z1 with a soft rounded top lip and a rounded bottom that tucks under.
    It only exists behind the rear arch (the arch cut trims its ends into the wheel opening)."""
    ay = np.abs(y)
    xs = x + RB_P
    side = (ay - (WPLAN(xs) + RB_SIDE)) / np.sqrt(1 + WPLAN.d(xs) ** 2)
    tail = (tail_x(9.0) - RB_P) - x
    plan = i_round(side, tail, 5.6)
    zb = np.abs(z - 0.5 * (Z_RR + RB_Z1)) - 0.5 * (RB_Z1 - Z_RR)
    b = i_round(plan, zb, 1.3)
    b = i_round(b, np.abs(y) - (NT_Y - 1.0), 1.5)   # rev 9: the bumper bar ends on a round cap 1 uu inside the tail notch
    #   (it used to be cut by the corner, leaving a sharp highlight nub where its ridge stopped)
    return i_round(b, x + 45.5, 1.0)


def greenhouse(x, y, z, floor=True):
    gs = (np.abs(y) - GW(z)) / GW_NORM
    gws = (x - WS_A[0]) * WS_N[0] + (z - WS_A[1]) * WS_N[1]
    gh = (x - HT_D[0]) * HT_N[0] + (z - HT_D[1]) * HT_N[1]
    rz = roof_z(x, y)
    gt = (z - rz) / np.sqrt(1 + ROOFX.d(x) ** 2 + (2 * ROOF_CROWN * y / ROOF_CW ** 2) ** 2)
    G = i_round(gs, gws, 2.8)
    G = i_round(G, gh, 3.2)
    G = i_round(G, gt, 4.0)
    if not floor:
        return G
    # rev 7 (spec 4b rule 16): the greenhouse floor was a HARD max at z 22.5. At the tail the outer-master blend
    # (u_round 1.1) reaches it, so the switch between the floor and the hatch plane printed a C0 crease right across the
    # tail top at z ~21.5-22.5 (a 30 deg normal jump: a horizontal 'fold' line in grazing light and a dark tick beside each
    # tail lamp). Behind x -38 the floor is now a rounded intersection; ahead of x -38 the field is bit-identical.
    hard = np.maximum(G, 22.5 - z)
    w = _smooth01((GH_FLOOR_X0 - x) / GH_FLOOR_DX)
    if not np.any(w > 0):
        return hard
    G2 = hard + w * (i_round(G, 22.5 - z, 1.2) - hard)
    return i_round(G2, GH_CUT_X - x, GH_CUT_R)


GH_CUT_X, GH_CUT_R = -48.4, 0.8     # rev 9: -49.6 -> -48.4 (round 4 fix 5: its rounded corner, 1.6 uu under the deck,
#   printed a second faint line on the hatch below the rear glass; now it sits inside the hatch-foot cove = one line)
GH_FLOOR_X0, GH_FLOOR_DX = -36.0, 9.0
OMR_X0, OMR_DX = -38.0, 9.0
OMR_REAR = 1.7


def om_r(x):
    """lower body / greenhouse fillet radius. rev 7 (round 2 review fix 3): 1.1 everywhere ahead of x -40 (unchanged);
    behind it it grows to 3.0, so the shallow concave crease where the tail deck meets the hatch-glass surround is a soft
    paint-filled cove, not a 1.1 uu valley that the mesher faceted into the dark wavy 'zipper' line under the rear glass."""
    return 1.1 + (OMR_REAR - 1.1) * _smooth01((OMR_X0 - np.asarray(x, float)) / OMR_DX)


def outer_master(x, y, z):
    return u_round(lower_body(x, y, z), greenhouse(x, y, z), om_r(x))


def cabin_field(x, y, z):
    """rev 9: the casting's outer volume WITHOUT hidden internal planes, for every INTERNAL offset (the body cavity and the
    interior clip). outer_master unions the lower body with a greenhouse whose floor is a slab at z 22.5; inside the cabin
    between z 22.5 and the lower-body top that union reports the skin only ~2.5 uu away (it measures to the hidden
    planes). Offset 2.2 (cavity) it left a knife-thin metal film across the cabin at belt level (r5 gate: 140 deg folds at
    z 23.8); offset 4.6 (interior clip) it cut the front seat backs and the steering-wheel rim away between z 22 and 29
    (a floating head-rest). Here the greenhouse is a column down to z 14 (walls vertical below the sill so they stay
    4.7 uu inside the body sides, cut 2.4 uu inside the tail like the outer master) unioned with the lower body: its
    zero set is the real outer surface and its interior has no hidden planes."""
    zc = 0.5 * (z + 22.5 + np.sqrt((z - 22.5) ** 2 + 4.0))          # smooth max(z, 22.5): walls vertical below the sill
    gs = (np.abs(y) - GW(zc)) / GW_NORM
    gws = (x - WS_A[0]) * WS_N[0] + (z - WS_A[1]) * WS_N[1]
    gh = (x - HT_D[0]) * HT_N[0] + (z - HT_D[1]) * HT_N[1]
    rz = roof_z(x, y)
    gt = (z - rz) / np.sqrt(1 + ROOFX.d(x) ** 2 + (2 * ROOF_CROWN * y / ROOF_CW ** 2) ** 2)
    G = i_round(i_round(i_round(gs, gws, 2.8), gh, 3.2), gt, 4.0)
    G = i_round(G, 14.0 - z, 2.0)
    G = i_round(G, GH_CUT_X - x, GH_CUT_R)
    return u_round(lower_body(x, y, z, floor=False), G, om_r(x))


FLARE_TOP = {X_FA: 25.0, X_RA: 25.9}
# rev 8 (round 3 review fixes 6/7): the rear flare top used to be a FLAT pad at z 25.9 ending on a hard inner wall at |y| 28,
# and the lower-body shoulder plus the 2.2 blend made a second flat at ~26.2 beside the C-pillar: two facets with a step
# between them (the doubled mirror image of the C-pillar badge) and a lumpy fold where the pad met the C-pillar base.
# Now the rear flare top is ONE surface: it rises gently inboard (slope FT_OUT_S from FT_OUT_Y, z 26.3 at |y| 33, the old
# inner height) into the C-pillar fillet, and inside the C-pillar (|y| < FT_IN_Y) it rolls down under the deck (C1 ramps),
# so no wall or corner of it sits near the skin. Outboard of |y| 37.6 (the flare lip and roll-over seen from the side)
# nothing changes.
FT_Y0, FT_H0, FT_C, FT_IN_Y, FT_IN_S, FT_W = 33.0, 25.85, 0.006, 25.0, 0.8, 1.5   # rev 9: roll-down 32 -> 25, inside the pillar
FT_LIP_Y, FT_LIP_W, FT_LIP_S = 37.6, 2.0, 0.6


def _c1ramp(t, w):
    """0 for t <= 0, t - w/2 for t >= w, quadratic between (C1); returns (value, slope)"""
    t = mx0(t)
    return np.where(t < w, t * t / (2.0 * w), t - 0.5 * w), np.minimum(t / w, 1.0)


def rear_flare_top(ay):
    """rear flare top height h(|y|) and dh/d|y|: a convex crown that steepens outward into the lip roll-over (no flat
    pad, no inflection), and inboard of FT_IN_Y a C1 roll-down that sinks it under the deck"""
    u = mx0(ay - FT_Y0)
    ri, si = _c1ramp(FT_IN_Y - ay, FT_W)
    return FT_H0 - FT_C * u * u - FT_IN_S * ri, -2.0 * FT_C * u + FT_IN_S * si


# rev 7 (spec 4b rule 14, round 2 review fix 5): behind the rear wheels the flare's lower rear corner tucks INBOARD (41 ->
# ~36.5, flush with the body-colour bumper) so from the chase camera the black rear tyres show below and beside the flares,
# like the R5 Turbo / 205 / Golf castings and Navvy. The tuck only moves the flare in Y: the side silhouette (XZ), the
# wheel positions and the hitbox are unchanged. It is full behind x -51 and below z 11, nothing ahead of x -45 or above z 21.
# rev 9 (round 4 review fixes 2/5): the rev 7 tuck pulled only the flare's LOWER rear corner in (z < 21) and rev 8 pulled
# the bumper corner in again below z 12, so from behind the tail's upper corners stood out over the tucked bumper like
# fins, and the two blends made a pinched lump under each lamp. Now the rear flare simply ENDS behind the wheel: over its
# full height it tapers from |y| 41 into the body side between x -46 and -50 (tangentially, then 1.5 uu inside it, so the
# exact union behind the C-pillar has nothing to fillet), and the tail corner is the body's own corner, dropping straight
# down like the R5 casting.
TUCK_X0, TUCK_X1, TUCK_IN = -45.0, -47.8, 1.5   # tangent (and 1.5 inside by -49.2) before the flare's own rear-end rounds start


def flare_tuck(x, z, F0):
    """how far the rear flare side is pulled in at x: it meets the body side TANGENTIALLY at TUCK_X1 (zero slope, zero
    gap), then sinks TUCK_IN inside it over 2 more uu - a seamless exact union, no crossing crease, no fillet"""
    side = WPLAN(x) + WSEC(z)
    t = (TUCK_X0 - x) / (TUCK_X0 - TUCK_X1)
    return (F0 - side) * _smooth01(t) + TUCK_IN * _smooth01((t - 1.0) * 2.0)


# rev 9 (round 4 review fix 3, lead ruling on rule 14): TAIL NOTCH. Behind each rear wheel, below the lamps, the tail
# corner (body, bumper, base lip and the rear liner) is cut back to |y| NT_Y with a 45 deg chamfer up to the full width,
# one subtractive cut with 1.2 uu rounds (no blended fields, so no pinched lump). From a 3/4-rear view at axle height the
# steel axle stub and the inner tyre show between tyre and body; from the chase camera the painted tail may hide the axle.
# The cut's front face lies inside the arch opening (x NT_X), so it never shows. The tail lamps (|y| <= 30.5, z >= 17.7)
# are untouched.
NT_X, NT_Y, NT_Z0, NT_W, NT_R = -46.0, 30.0, 11.5, 2.0, 1.4   # rev 10: cut-edge round 1.2 -> 1.4 (r5 gate fix 5)
NT_WALL = 4.5                          # zamac wall kept round the cut (the cavity stays this far from its faces)


def tail_notch(x, y, z, grow=0.0):
    """> 0 outside the cutter (material may stay), < 0 inside it. grow moves the cut faces outward (the base sits 0.3
    proud of the body skin)."""
    t = mx0(z - NT_Z0)
    ramp = np.where(t < NT_W, t * t / (2.0 * NT_W), t - 0.5 * NT_W)
    dy = np.minimum(t / NT_W, 1.0)
    side = ((NT_Y + grow + ramp) - np.abs(y)) / np.sqrt(1.0 + dy * dy)
    front = (x - (NT_X - mx0(z - 13.0))) / 1.4142                # front face leans back above z 13: stays behind the arch
    return i_round(side, front, 1.5)    # rev 10: 1.0 -> 1.5 (the notch's inner corner)


def flares(x, y, z):
    ay = np.abs(y)
    d = None
    for xw in (X_FA, X_RA):
        hl = 17.4 - (z - 4.0) * (2.9 / 21.0)
        dx = (np.abs(x - xw) - hl) / 1.0095
        if xw == X_RA:
            # rev 9: the shoulder surface shared with the lower body (rq_top): the crown beside the C-pillar MORPHS into
            # the tail-deck surface behind it, joined by an exact union - no 'ears', step, dip or fillet bulge
            h, dh = rq_top(x, y)
            dtop = (z - h) / np.sqrt(1.0 + dh * dh)
        else:
            dtop = z - FLARE_TOP[xw]
        side2d = i_round(dx, dtop, 3.2)
        dy = ay - (41.0 - (z - 10.0) * 0.07)
        if xw == X_RA:
            F0 = 41.0 - (z - 10.0) * 0.07
            tk = flare_tuck(x, z, F0)
            # rev 9: measured in |y| (not normalised by the taper's x-slope): the flare's 2.6 top-side round then has exactly
            # the body's |y| profile all along the taper, so where the taper meets the body side the two tops and rounds
            # coincide (exact union, seamless) - normalised, the round swept 3x wider in |y| on the steep taper and the
            # flare top dipped under the deck and popped back up at the tangent point (a small crease behind the pillar)
            dy = ay - (F0 - tk)
        rr_ = 1.8 if xw == X_FA else 1.8 + 0.8 * _smooth01((-42.5 - x) / 2.5)   # rev 9: = the body's 2.6 top edge BEFORE the taper
        #   starts (x -45), so all along the taper the flare's top edge is the body's edge shifted outward: it always encloses the
        #   body's (a smaller or larger flare edge crossed the body's 2.6 edge = a diagonal wrinkle across the hip), and where the
        f = i_round(side2d, dy, rr_)                                                #   tapered flare runs into it (no double edge)
        f = i_round(f, (23.5 if xw == X_RA else 28.0) - ay, 0.8)   # rev 9: inner top edge rounded 0.8; rear: inside the pillar   # rev 9: inner top edge rounded 0.8 (was a crisp max edge)
        f = np.maximum(f, 4.0 - z)
        if xw == X_RA:      # rev 5: behind the rear wheel the flare still ends at the sill (the tail skin drops lower)
            f = np.where(x < RR_X0 + 1.0, i_round(f, Z_SILL - z, 1.0), f)   # switch lies inside the arch cut
            # rev 9: once the taper has met the body side, sink the flare 0.2 uu inside the body (it was coincident with
            # the deck to a few hundredths and crossed it at a shallow angle where its own rear-end rounds began)
            f = f + 0.2 * _smooth01((TUCK_X1 - x) / 0.8)
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
    m = sd_rbox(x, y, z, (-1.4, 0.0, zc), (1.6, 5.8, 0.8), 0.75)       # rev 9: 0.55 -> 0.75 (r5 gate: torn slot corners)
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
HL_CAP_H = (0.45, 0.38)                                   # rev 11: lens cap rise (main, driving lamp)
HL_LENS_WRAP = 0.10                                       # rev 11: lens print runs 0.10 past the dome wall (into its foot fillet)
TL_Y, TL_Z, TL_HY, TL_HZ, TL_R, TL_RAISE = 25.5, 20.5, 5.0, 2.8, 1.3, 0.5
GRILLE_Z = (15.6, 17.3, 19.0)
LID_Y, LID_Z = 17.8, 12.2          # rev 7: 0.4 in / 0.6 down so the soft shut-line dent clears the lamp bosses and plate
#   rev 9 (round 4 fix 4): lid bottom 14.8 -> 12.2 = ON the bumper's top cove, so the side lines run down into the bumper
#   ledge and turn along it (one line, rounded corners) - no separate bottom groove 1.6 uu above the ledge, no pit


def lamp_bosses(x, y, z):
    ay = np.abs(y)
    xn = nose_x(z)
    hl = i_round(sd_rrect2(ay - HL_Y, z - HL_Z, HL_HY, HL_HZ, HL_R), x - (xn + HL_RAISE), 0.5)
    hl = np.maximum(hl, (xn - 3.0) - x)
    # rev 11 (owner 17 Oct: 'the front lights have issues with faces, normals or vertices'): each lens was a 0.35 uu
    # disc with a vertical wall, a 0.3 top round and a 0.2 foot fillet - all curvature, finer than the 0.25 uu mesher
    # cell, so the export faceted every dome edge into a ring of teeth. Each lens is now a shallow SPHERICAL CAP on the
    # bezel face (rise HL_CAP_H, meeting the face at ~25 deg) with a 0.35 foot fillet: a smooth moulded lens that
    # meshes cleanly; the pad print covers it to the fillet (HL_LENS_WRAP).
    k = 1.0 / math.sqrt(1.0 + 0.1 ** 2)                     # bezel-face normal (1, 0, 0.1): the nose leans back 0.1
    for (yc, r), hc in zip(HL_DOMES, HL_CAP_H):
        Rs = (r * r + hc * hc) / (2.0 * hc)
        cx = nose_x(HL_Z) + HL_RAISE - (Rs - hc) * k
        cz = HL_Z - (Rs - hc) * 0.1 * k
        dm = np.sqrt((x - cx) ** 2 + (ay - yc) ** 2 + (z - cz) ** 2) - Rs
        dm = np.maximum(dm, (xn - 1.0) - x)
        hl = u_round(hl, dm, 0.35)
    xt = tail_x(z)
    tl = i_round(sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY, TL_HZ, TL_R), (xt - TL_RAISE) - x, 0.45)
    tl = i_round(tl, x - (xt + 1.6), 0.4)          # rev 8: boss ends inside the 2.2 wall (was a 90 deg box in the cavity)
    return np.minimum(hl, tl)


def recesses(x, y, z, Oo):
    gr = None
    for zc in GRILLE_Z:
        g = sd_rrect2(y, z - zc, 12.6, 0.5, 0.48)
        gr = g if gr is None else np.minimum(gr, g)
    gr = np.maximum(np.maximum(gr, -(Oo + 0.8)), 50.0 - x)
    return gr


GROOVE_HW, GROOVE_DEPTH = 0.36, 0.55
MOOD = {"cx": -21.5, "cy": 0.0, "hx": 9.0, "hy": 15.5, "r": 3.2}
DOOR_FX, DOOR_RX = 19.8, -15.3
DOOR_PRINT_GAP = 0.12                  # rev 11: half-width of the tampo break at a door shut line


DOOR_F_ZEND, DOOR_F_RUNOUT = 25.6, 1.6


def grooves(x, y, z, Oo):
    ay = np.abs(y); hw = GROOVE_HW
    # rev 6 (spec 4b rule 16): the door-front line used to stop on a flat cap at z 25.6 right where the A-pillar base
    # slopes in, which undercut the surface into a hooked sliver (health check: (20.1, +-30.2, 25.6)). It now runs out:
    # full depth below z 24.0, getting shallower to nothing at z 25.6 - a cast line fading into the pillar fillet.
    gf = np.maximum.reduce([np.abs(x - DOOR_FX) - hw, Z_SILL - z, 30.0 - ay])                      # door front
    gf = np.maximum(gf, -(Oo + GROOVE_DEPTH * _smooth01((DOOR_F_ZEND - z) / DOOR_F_RUNOUT)))
    g = np.maximum.reduce([np.abs(x - DOOR_RX) - hw, Z_SILL - z, z - 35.4, 25.0 - ay])              # door rear
    g = np.minimum(g, np.maximum.reduce([np.abs(ay - 32.6) - hw, 24.4 - x, x - 55.0, 20.5 - z]))  # bonnet sides
    g = np.minimum(g, np.maximum.reduce([np.abs(x - 24.4) - hw, ay - 32.6, 21.5 - z]))           # cowl
    g = np.minimum(g, np.maximum.reduce([np.abs(z - 20.9) - hw, 50.5 - x, ay - 32.6]))           # bonnet lip
    mp = sd_rrect2(x - MOOD["cx"], y - MOOD["cy"], MOOD["hx"], MOOD["hy"], MOOD["r"])
    g = np.minimum(g, np.maximum(np.abs(mp) - hw, 37.0 - z))                                     # mood panel
    return np.minimum(np.maximum(g, -(Oo + GROOVE_DEPTH)), gf)


REAR_DENT_W, REAR_DENT_DEPTH = 1.0, 0.36     # rev 11 (gate leftover: tail shut lines' sawtooth walls + black-pit top caps):
#   2.0 uu wide, 0.36 deep like the door lines (rev 9 widened those for the same sawtooth); 1.7 uu land to the lamp bosses.
#   rev 8: 1.4 uu wide, 0.40 deep (was 2.0 x 0.45)
PLATE_EDGE = 1.5                             # plate panel walls blended over 1.5 uu (rev 9: 0.8 -> 1.5,
#   a soft 15 deg wall: under raking light from either side the end walls shade softly, no black slit)
PLATE_BOSS = 0.30                            # rev 10: raised plate boss height (PLATE_DEPTH recess retired)
SHUT_CORNER_R = 1.6
SHUT_ROLL_C, SHUT_ROLL_R = (-49.18, 23.09), 2.6   # rev 10: the tail-top roll at |y| 17.8 (centre x, z; radius): tail face
#   x -51.78, deck z 25.69, the lower body's 2.6 top round
SHUT_CAP_LEN = 2.0                          # rev 11: arc length over which the cap closes (was one half-width)
SHUT_CAP_TH = math.radians(28.0)            # rev 11: 45 -> 28 deg (the longer cap ends at ~72 deg, on the roll)
#   rev 10: 45 deg - the side lines end over that roll on a round cap (rev 8/9
#   ran them on into the rear-glass opening: the knot at the hatch-foot cove)


def _bell(t):
    """1 at t = 0 falling to 0 at |t| = 1 with zero slope at both ends: a groove profile with no lip and no floor edge"""
    t = np.clip(np.abs(t), 0.0, 1.0)
    u = 1.0 - t * t
    return u * u


def rear_dents(x, y, z):
    """rev 8 (round 3 review fix 4, spec 4b rules 12/16): the hatch shut lines and the plate panel are SOFT DENTS added to
    the outer surface field (no boolean lips, no blob ends).
      * shut line = one lid outline in the tail plane (sides at |y| LID_Y, bottom at LID_Z, 1.6 corner radius) as a 1.4 uu
        wide bell-profile dent, 0.40 deep. rev 8: narrower and moved 1.4 inboard so there are >= 1.5 uu of flat land to
        the tail-lamp lenses (rev 7: 0.3 uu - the right line merged with the lamp edge into a double groove). The sides no
        longer fade out across the tail-top round (that 1.2 uu depth ramp printed a bright end wall and a kink at macro):
        they run straight up the tail, over the top, across the deck and up the glass surround into the rear-glass opening,
        like the R5 / Golf tailgate lines, so the dent never ends on a visible surface.
      * plate panel = 0.4 uu recess whose walls blend over 0.8 uu (floor = the printed plate's black border)."""
    ay = np.abs(y)
    top = 60.0
    lid = sd_rrect2(ay, z - 0.5 * (LID_Z + top), LID_Y, 0.5 * (top - LID_Z), SHUT_CORNER_R)
    # rev 10 (r5 gate fix 3): the side lines no longer run on across the hatch-foot cove and up into the glass opening
    # (crossing the cove + the opening's round they crumpled into a faceted knot, even on a 0.1 uu mesh). They run up the
    # tail face and end half-way over the tail-top roll (a plain convex cylinder: no cove, no flat, no opening near) in a
    # ROUND CAP of the same bell profile, measured along the roll (arc length beyond the cap angle), so the cap is round
    # on the surface. (A first try capped them on the 0.65 uu deck strip between the roll and the cove: still faceted.)
    th = np.arctan2(z - SHUT_ROLL_C[1], SHUT_ROLL_C[0] - x)          # 0 = start of the roll (tail face), pi/2 = deck
    th = np.where(th < -0.5 * np.pi, th + 2.0 * np.pi, th)           # ahead of the roll (the rest of the car): no line
    # rev 11 (gate leftover: the cap still read as a black pit with toothed walls under the 6 deg proof sun, and the 0.3 uu
    # refinement cannot go finer under the rule-16 area guard): the cap is ELONGATED - the bell closes over SHUT_CAP_LEN
    # of arc instead of one half-width, starting at 28 deg (ends at ~72 deg, still on the convex roll): a groove that
    # shallows out smoothly instead of a round pit end.
    beyond = mx0(th - SHUT_CAP_TH) * SHUT_ROLL_R * (REAR_DENT_W / SHUT_CAP_LEN)
    d_lid = REAR_DENT_DEPTH * _bell(np.hypot(lid, beyond) / REAR_DENT_W)
    # rev 10 (r5 gate fix 6, tampo ruling): the plate panel is a RAISED 0.3 uu cast boss (the pad prints its top face) -
    # it was a 0.4 recess with the plate printed on its floor. Same outline and soft 1.5 uu walls; flat top >= 0.3 uu
    # round the print.
    pl = sd_rrect2(y, z - 18.6, 8.2, 2.3, 1.1)
    d_pl = -PLATE_BOSS * (1.0 - _smooth01((pl + 0.15) / PLATE_EDGE)) * _smooth01((-47.5 - x) / 1.0)
    return d_lid + d_pl


FRONT_DENT_W, FRONT_DENT_DEPTH = 1.0, 0.42   # rev 9: door / bonnet / mood-panel lines: soft U, 2.0 uu wide (0.7 half-width
#   faceted into a sawtooth edge on the export mesh in the 1024-spp side-glass proof)
BONNET_X, BONNET_Y, BONNET_Z, BONNET_R = 24.4, 32.6, 20.9, 1.6
DOOR_R_ZEND, DOOR_R_RUNOUT = 24.0, 1.8   # rev 9: the rear door line runs out below the belt (it kinked where it crossed the
#   shoulder cove and wobbled up the narrow B-pillar between the window rounds; 1:64 castings stop it at the window line)


def front_dents(x, y, z):
    """rev 9 (r5 spike/notch gate: the old door, bonnet and mood-panel grooves were boolean slots with 0.3 uu edge rounds
    and flat end caps - at the export density every edge became a crease that broke at its ends and corners, 127 torn
    crease vertices on the body). Each line is now a soft bell-profile dent on the outer field (no lips, no floor edge,
    paint pools in it), on the same lines as before:
      * door front (x 19.8, |y| > 30): runs from the sill up and out over z 24.0-25.6 into the A-pillar fillet;
      * door rear (x -15.3, |y| > 25): from the sill up the door, running out over z 22.2-24.0 below the belt;
      * bonnet: ONE closed outline (cowl x 24.4, sides |y| 32.6, lip z 20.9 on the nose, 1.6 corners) - no line ends;
      * mood panel: the closed rounded rectangle on the roof."""
    ay = np.abs(y)
    D, W_ = FRONT_DENT_DEPTH, FRONT_DENT_W
    df = _bell((x - DOOR_FX) / W_) * _smooth01((DOOR_F_ZEND - z) / DOOR_F_RUNOUT) * _smooth01((ay - 29.0) / 1.5)
    dr = _bell((x - DOOR_RX) / W_) * _smooth01((DOOR_R_ZEND - z) / DOOR_R_RUNOUT) * _smooth01((ay - 24.0) / 1.5)
    bon = i_round(i_round(BONNET_X - x, ay - BONNET_Y, BONNET_R), BONNET_Z - z, BONNET_R)
    db = _bell(bon / W_)
    mp = sd_rrect2(x - MOOD["cx"], y - MOOD["cy"], MOOD["hx"], MOOD["hy"], MOOD["r"])
    dm = _bell(mp / W_) * _smooth01((z - 36.5) / 1.0)
    return D * np.maximum.reduce([df, dr, db, dm])


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
    d = i_round(i_round(rho - RL_R, x - RL_XF, 0.7), RL_XB - x, 1.7)                  # rev 9: rim round 0.55 -> 0.7
    d = s_round(d, i_round(rho - (RL_R - 0.6), np.abs(x - RL_XF) - 0.4, 0.15), 0.3)   # lens seat (rev 9: 0.15 -> 0.3 rounds)
    return d


def rally_stalk(x, y, z):
    g = rally_geo()
    return sd_rbox(x, np.abs(y), z, (BAR_X + 0.3, RL_Y, g['bar_z'] + 1.15), (0.85, 0.85, 0.75), 0.3)


def rally_lens(x, y, z):
    g = rally_geo()
    ay = np.abs(y)
    rho = np.hypot(ay - RL_Y, z - g['zc'])
    sph = np.sqrt((x - (RL_XF - 6.2)) ** 2 + rho ** 2) - 6.55
    d = i_round(i_round(sph, rho - (RL_R - 0.45), 0.3), (RL_XF - 0.6) - x, 0.2)   # rev 9: rounded rim (was hard max)
    bars = np.maximum(np.minimum(np.abs(ay - RL_Y), np.abs(z - g['zc'])) - 0.16, rho - (RL_R - 0.7))
    bars = np.maximum(bars, (RL_XF + 0.25) - x)
    return s_round(d, np.maximum(bars, -(sph + 0.1)), 0.12)                      # rev 9: 0.05 -> 0.12 (soft moulded bars)


FFR_X0, FFR_X1 = -18.0, -20.0         # rev 11: angle-aware union radius behind here (ramped in), rear flare front end only
FFR_COS0 = 0.5                        # full radius once the two surfaces meet at >= 60 deg


def _rear_flare_front_r(x, y, z, Om, F):
    """rev 11 (gate leftover: the lumpy knot on the shoulder shelf in front of the C-pillar, x -25..-33, |y| 32-37,
    z ~26, zebra bullseyes). Ahead of the C-pillar the rear flare's flat crown stands only ~0.8 uu above the lower body's
    top, and the 2.2 uu flare union of those two near-PARALLEL surfaces bulged 0.17 uu over the crown (u_round of
    coincident surfaces adds 0.41 r): a dome on the shelf. The union radius there now scales with the angle between the
    two surfaces: the full 2.2 where the flare's front face meets the body side (~90 deg: the cove is unchanged), ~0
    where flare crown and body top run parallel (no bulge: an exact union of a surface hidden under the other)."""
    r = flare_union_r(x)
    w = _smooth01((FFR_X0 - np.asarray(x, float)) / (FFR_X0 - FFR_X1))
    m = (w > 0.0) & (np.asarray(x) > -36.0) & (np.abs(y) > 20.0) & (z > 8.0) & (np.minimum(Om, F) < 3.0)
    if not np.any(m):
        return r
    xm, ym, zm = x[m], y[m], z[m]
    e = 0.04
    def grad(f):
        g = np.stack([f(xm + e, ym, zm) - f(xm - e, ym, zm), f(xm, ym + e, zm) - f(xm, ym - e, zm),
                      f(xm, ym, zm + e) - f(xm, ym, zm - e)], 1)
        return g / np.maximum(np.linalg.norm(g, axis=1), 1e-9)[:, None]
    na = grad(lambda a, b, c: lower_body(a, b, c, shoulder=True))   # the lower body alone: in the greenhouse
    #   cove its normal stays parallel to the flare crown's (an Om normal there tilted, restored a radius and left a ridge)
    nb = grad(flares)
    c = np.clip((na * nb).sum(1), -1.0, 1.0)
    k = _s5((1.0 - c) / (1.0 - FFR_COS0))
    r = np.array(np.broadcast_to(r, np.shape(x)), float, copy=True)
    r[m] = r[m] * (1.0 - w[m] + w[m] * k)
    return r


def body_fields(x, y, z):
    A = lower_body(x, y, z, shoulder=True)               # rev 9: one shoulder surface for the lower body and the flare (fix 1)
    G = greenhouse(x, y, z)
    Om = u_round(A, G, om_r(x))
    F = flares(x, y, z)
    Oo = u_round(Om, F, _rear_flare_front_r(x, y, z, Om, F))   # rev 11: angle-aware radius at the rear flare's front
    # rev 10 (r5 gate fixes 1 + 2): behind x -29.5 the field hands over (C2 blend of two fields with the same top, side and
    # cove - only the top roll grows 1.8 -> 2.6) to the one-piece rear quarter: no flare union behind x -33.5
    w = rq_piece(x)
    m = w > 0.0
    if np.any(m):
        xm, ym, zm = x[m], y[m], z[m]
        Ow = u_round(lower_body(xm, ym, zm, shoulder=True, wide=True), G[m], om_r(xm))
        Oo = np.array(Oo, float, copy=True)
        Oo[m] = Oo[m] + w[m] * (Ow - Oo[m])
    Oo = u_round(Oo, bulge(x, y, z), 2.0)
    Oo = u_round(Oo, spoiler(x, y, z), 1.1)
    Oo = u_round(Oo, scoop(x, y, z), 0.9)
    # rev 5: cast body-colour rear bumper. rev 7: crease fillet 0.5 -> 1.1 (the 0.5 concave crease was two mesher cells and
    # zig-zagged along the bumper top line at macro); the paint now pools in a soft cove like a real casting's
    Oo = u_round(Oo, rear_bumper(x, y, z), 1.1)
    Oo = Oo + rear_dents(x, y, z)                        # rev 7: soft shut-line + plate dents (outer skin only)
    Oo = Oo + front_dents(x, y, z)                       # rev 9: door / bonnet / mood-panel lines as soft dents too
    # rev 5: hollow against the outer master WITHOUT its z 4 floor (identical above z 6.2; the tail skin now drops to Z_RR)
    # rev 9: against the true cabin field (no hidden greenhouse floor: it left a knife-thin metal film across the cabin)
    inner = cabin_field(x, y, z)
    # rev 9: the cavity stays NT_WALL inside the tail-notch faces (a thick cast corner round the cut, no hole)
    inner = i_round(inner, (NT_WALL - T_SHELL) - tail_notch(x, y, z), 1.0)
    S = np.maximum(Oo, -(inner + T_SHELL))
    S = s_round(S, arches(x, y, z), 1.1)
    S = i_round(S, zclip(x) - z, 0.9)
    S = s_round(S, tail_notch(x, y, z), NT_R)            # rev 9: tail notch behind the rear wheels (rule 14)
    S = s_round(S, np.maximum(BUMP_FX + 1.4 - x, z - BUMPER_TOP), 0.8)
    S = s_round(S, windows_zone(x, y, z), 1.0)
    S = u_round(S, lamp_bosses(x, y, z), 0.4)
    gr = recesses(x, y, z, Oo)
    S = s_round(S, gr, 0.35)
    S = u_round(S, mirror_nubs(x, y, z), 0.8)
    S = u_round(S, rally_bar(x, y, z), 0.9)
    m, zc = scoop_mouth(x, y, z)
    S = s_round(S, m, 0.7)                               # rev 9: 0.4 -> 0.7
    return S, Om, Oo


def body_sdf(x, y, z):
    return body_fields(x, y, z)[0]


# =============================================================================
#  WINDOW PIECE (one thick light-smoke moulding inside the shell)
# =============================================================================
GLASS_GROW = 1.4            # rev 9: each pane runs 1.4 uu past its opening edge under the paint (was 2.6, into the bends)
GLASS_RIM_R = 1.1           # rev 9: rim round = half the 2.3 thickness: a soft cast-plastic edge, no crisp crease


GLASS_GAP_SIDE = 0.38       # rev 10 (r5 gate fix 7): the side panes sit 0.38 (was 0.08) inside the shell's inner face, so the
#   pane never touches / interpenetrates the sill skin (no jagged pane-body line through translucent glass in UE)
GLASS_SILL_GROW = 1.0       # rev 10: the side panes run 1.0 further down under the sill (their rim and its tilted normals
#   sit 2.4 below the visible sill edge: on the r5 mesh the rim's vertex normals bled into the visible bottom of the
#   flat pane as a sawtooth in the zebra side-glass view)


def _pane(plane, foot, gap=GLASS_GAP):
    """one flat window pane: the 2.3 uu slab (gap + 2.2)..(gap + 4.5) uu under a greenhouse plane, inside its footprint"""
    slab = np.abs(plane + T_SHELL + gap + 0.5 * GLASS_T) - 0.5 * GLASS_T
    return i_round(slab, foot, GLASS_RIM_R)


def glass_sdf(x, y, z):
    """rev 9 (r5 spike/notch gate: 290 torn-crease vertices on the window piece). The piece used to be a 2.3 uu layer
    under outer_master, whose field carries the greenhouse's hidden z 22.5 floor slab and the 2.8-4.0 corner rounds:
    2.28-4.58 uu deep those give hard creases (the max() of two planes), and at the windscreen foot / side sills / hatch
    foot / roof edge the layer bent round the cowl, shoulder and roof - every pane edge was a grazing cut through a bend
    (91 deg spikes, 140 deg folds along the windscreen foot, a hidden strip under the roof cut off at |y| 19). Now every
    pane is a FLAT slab of its own greenhouse plane, 2.28-4.58 uu under it exactly as before inside the openings, ending
    1.4 uu past each opening edge (hidden under the paint) on one 1.1 uu rim round."""
    ay = np.abs(y)
    gs = (ay - GW(z)) / GW_NORM
    gws = (x - WS_A[0]) * WS_N[0] + (z - WS_A[1]) * WS_N[1]
    gh = (x - HT_D[0]) * HT_N[0] + (z - HT_D[1]) * HT_N[1]
    g = GLASS_GROW
    side = np.minimum(sd_poly(x, z, DOOR_SHR), sd_poly(x, z, QTR_SHR)) - R_SIDEWIN - g
    zs = z + GLASS_SILL_GROW                                 # rev 10: the footprint's bottom edge 1.0 lower
    side = np.minimum(side, np.minimum(sd_poly(x, zs, DOOR_SHR), sd_poly(x, zs, QTR_SHR)) - R_SIDEWIN - g)
    side = np.maximum(side, 12.0 - ay)                       # one pane per side (the other side is 50 uu away)
    u = (x - WS_A[0]) * WS_U[0] + (z - WS_A[1]) * WS_U[1]
    ws = sd_poly(u, y, WS_SHR) - R_WS - g
    ws = np.maximum(ws, -(gws + 9.0))                        # the windscreen plane only near the windscreen
    uh = (x - HT_D[0]) * HT_U[0] + (z - HT_D[1]) * HT_U[1]
    ht = sd_poly(uh, y, HT_SHR) - R_HT - g
    ht = np.maximum(ht, -(gh + 9.0))
    return np.minimum.reduce([_pane(gs, side, GLASS_GAP_SIDE), _pane(gws, ws), _pane(gh, ht)])


# =============================================================================
#  BASE (chassis) SDF  - black plastic: band under the sill, bumpers, wheel wells
# =============================================================================
RIVETS = [(45.0, 0.0), (-44.0, 0.0)]
TEXT_AREA = {"cx": -2.0, "cy": 0.0, "hx": 20.0, "hy": 12.0}
BAND_INSET = -0.30                   # rev 3: band stands 0.3 uu PROUD of the sill so it catches light as a black rocker


def exhaust_tip(x, y, z):
    """rev 5: a 2.2 uu (1.4 mm) tube with a 0.74 bore, ending just past the bumper face."""
    zc = EXH_Z + 0.06 * (x - EXH_X0)                  # tiny downturn towards the open end (x decreases)
    rho = np.hypot(y - EXH_Y, z - zc)
    tube = i_round(rho - EXH_R, np.maximum(EXH_X1 - x, x - EXH_X0), 0.3)       # rev 9: 0.18 -> 0.3
    return s_round(tube, i_round(rho - EXH_BORE, (EXH_X1 + 2.4) - x, 0.3), 0.25)   # rev 9: 0.12 -> 0.25, round bore floor


def base_sdf(x, y, z):
    ay = np.abs(y)
    plan8 = lower_plan(x, y, np.full_like(z, 8.2))
    # rev 5: along the sides the band is unchanged (Z_BOT..Z_SILL+0.5, 0.3 proud). Behind the rear wheels it becomes a
    # thin lip: its top drops inside the tail shell (LIP_TOP) and its face sits LIP_OUT out of the tail-panel line,
    # i.e. ~1.2 uu tucked under the body-colour bumper - a 3.4 uu black line from behind, no plinth.
    rw = _smooth01((-46.0 - x) / 3.5)
    zb1 = (Z_SILL + 0.5) + (LIP_TOP - (Z_SILL + 0.5)) * rw
    inset = BAND_INSET + (-LIP_OUT - BAND_INSET) * rw
    band = i_round(plan8 + inset, np.abs(z - 0.5 * (Z_BOT + zb1)) - 0.5 * (zb1 - Z_BOT), 1.1)
    plug = i_round(plan8 + T_SHELL + 0.35, np.abs(z - (Z_SILL + 1.2)) - 1.0, 0.5)
    plug = i_round(plug, -(x + 49.0), 0.8)           # rev 5: no plug in the tail (the shell comes down to Z_RR there)
    # rev 8: the corner tuck moves the skin in: band/lip stay 0.3 proud of it, the hidden plug stays 2.55 inside it
    B = u_round(band, plug, 0.4)
    # bumpers: the base wraps up into chunky front/rear bumpers
    plan10 = lower_plan(x, y, np.full_like(z, 10.0))
    # a bumper bar (z BAR_Z0..BUMPER_TOP) over a recessed chin/valance down to the base
    bump_z = np.abs(z - 0.5 * (BAR_Z0 + BUMPER_TOP)) - 0.5 * (BUMPER_TOP - BAR_Z0)
    val_z = np.abs(z - 0.5 * (Z_BOT + BAR_Z0 + 0.6)) - 0.5 * (BAR_Z0 + 0.6 - Z_BOT)
    fb = u_round(i_round(i_round(plan10 - 2.0, bump_z, 1.5), BUMP_FX - x, 1.2),
                 i_round(i_round(plan10 + 0.4, val_z, 1.1), BUMP_FX + 1.0 - x, 1.0), 0.5)
    bumpers = fb                     # rev 5: no black rear bumper/valance - the body paint wraps the tail (rule 11)
    B = u_round(B, bumpers, 0.8)
    strip = np.maximum(np.abs(z - 10.15) - 0.45, -(bumpers + 0.5))
    slot = i_round(sd_rrect2(y, z - 5.6, 15.0, 0.75, 0.65), -(fb + 0.9), 0.4)       # rev 9: rounded floor
    ind = np.maximum(sd_rrect2(ay - 26.0, z - 11.6, 3.0, 0.7, 0.6), -(fb + 0.5))
    # rev 6: the front valance opening on the car's right (y -21, z 5.6) that the owner has seen since rev 2. It used to
    # come from the old REAR exhaust cut, which tunnelled the whole length of the base and so also opened the front
    # valance; rev 5 deleted that cut and the opening with it. Restored as a blind 4.6 uu pocket in the front valance
    # only (same section, same 0.3 edge round), so the front end looks exactly as approved and nothing tunnels through.
    fpocket = i_round(sd_rrect2(y + 21.0, z - 5.6, 3.0, 1.2, 1.15), 52.0 - x, 0.4)  # rev 9: rounded floor
    # rev 9 (r5 gate: the bumper strip groove and indicator recesses were boolean cuts with 0.3 uu rounds that ended
    # abruptly at the bumper's side ends - torn creases at x 51-58.6, |y| 23-37): the valance slot and pocket stay cuts
    # (rounder), the strip and the indicator recesses become soft dents (same lines, no end caps; the strip runs out
    # behind the bumper's side wrap).
    B = s_round(B, np.minimum(slot, fpocket), 0.45)
    d_strip = 0.45 * _bell((z - 10.15) / 0.75) * _smooth01((x - 51.6) / 1.6)
    d_ind = 0.35 * (1.0 - _smooth01((sd_rrect2(ay - 26.0, z - 11.6, 3.0, 0.7, 0.6) + 0.1) / 0.7)) * _smooth01((x - 52.5) / 1.0)
    B = B + (d_strip + d_ind - d_strip * d_ind / 0.45)   # smooth OR of the two dents (no crease where they meet)
    # rev 6 (spec 4b rule 16): the bumper strip groove is cut wherever the base lies OUTSIDE the front bumper, so it also
    # sliced a 0.9 uu slot through the hidden plug (z 9.7-10.6, the whole car; sealed behind the front bumper: x 42-51,
    # |y| < 25, ~425 uu^3, health check: a closed inner void). Put the whole plug back: it sits >= 4 uu inside every
    # bumper face (plan inset 2.55 vs the bar 2.0 proud), so the visible 0.5 uu grooves on the bumper are untouched.
    B = np.minimum(B, plug)
    # rev 5: one small exhaust tip (bare zamac via Col R) out from under the lip, open end, slight downturn
    ex = exhaust_tip(x, y, z)
    B = u_round(B, ex, 0.5)
    # wheel notches
    for xw in (X_FA, X_RA):
        # rev 9 (rule 14): the REAR well opens in to the liner back wall (|y| 26.8; was 31.7, so the hidden plug buried the
        # axle stub up to 1.4 uu from the tyre). The front well is unchanged.
        yin = 26.8 if xw == X_RA else (WHEEL_Y - WHEEL_WD / 2 - 1.4)
        B = s_round(B, sd_rbox(x, ay, z, (xw, 50.0, 10.0), (ARCH_R - 0.2, 50.0 - yin, 12.0), 2.0), 0.6)
    # wheel-well liners (black) so the arches never show the empty body cavity
    # rev 6 (spec 4b rule 16): the liner ring (r 13.1-14.5) used to be clipped at the shell's INNER wall, which crossed
    # it almost tangentially at the arch tops and behind the rear wheels -> 0.15-0.4 uu knife fins (health check: x -46
    # / +45, |y| 31-34.5, z 19.5-21; x -39..-34 z 23.3; the tail at x -50 z 8-12). Now the ring is 1.0 thick (r 13.1-14.1,
    # same visible inner face) and is clipped 0.9 uu under the OUTER skin instead: it runs on into the zamac wall where it
    # is hidden (the arch opening is <= 12.92 at that depth, < 13.1), so no clip ever leaves a thin sliver.
    # rev 9 (round 4 review fix 2 + r5 gate: the ring/back-wall corners were hard max() edges, torn into zig-zags at
    # |y| 25.6 on every liner): each liner is ONE smooth cup - a 1.0 uu ring (r 13.1-14.1) and a 1.2 uu back wall (|y|
    # 25.6-26.8) with a 1.0 inside round and 0.4 rim rounds, the same 3.2 uu gap to the tyre all round. Behind the rear
    # tyre, below z 14, the ring is left out (fix 3 / rule 14: the pocket opens to the tail notch so the axle stub shows
    # from a 3/4-rear view at axle height); the back wall stays, so the arch never looks into the body cavity.
    Om = outer_master(x, y, z)
    for xw in (X_FA, X_RA):
        rr = np.hypot(x - xw, z - ARCH_Z)
        if xw == X_FA:
            # the front arch top runs through solid zamac above the cavity ceiling (~21.6), where clipping the ring under
            # the bonnet was a grazing cut (torn creases): the front ring is an arc with ROUND end caps that stops at
            # z ~22 (60 deg either side of the top), the back wall is clipped square under the skin as before
            ring = i_round(sd_arc(x - xw, z - ARCH_Z, 0.0, 0.0, ARCH_R + 0.7, 119.8, 420.2) - 0.5, 26.4 - ay, 0.4)
            back = i_round(np.abs(ay - 26.2) - 0.6, rr - (ARCH_R + 1.2), 0.5)
            cup = u_round(back, ring, 0.8)
        else:
            cup = s_round(i_round(rr - (ARCH_R + 1.2), 25.6 - ay, 1.0), i_round(rr - (ARCH_R + 0.2), 26.8 - ay, 1.0), 0.4)
        cup = i_round(cup, (Z_BOT + 1.0) - z, 0.5)
        if xw == X_RA:
            cup = s_round(cup, i_round(i_round(x - (X_RA - 8.0), z - 14.0, 1.5), 27.4 - ay, 0.6), 0.6)
        Lw = i_round(cup, Om + 0.9, 0.45)  # rounded clip: the ring's open edge ends on a full round (half its 1.0 thickness)
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
    # rev 9: the tail notch. rev 10: the base lip's cut end sits 0.3 INSIDE the body's notch face (was 0.3 proud: its end
    #   face stood out under the painted corner as a lit triangular wedge); the painted notch face reads as one slab
    B = s_round(B, tail_notch(x, y, z, grow=-0.3), 0.8 + 0.4 * _smooth01((11.0 - z) / 2.0))   # rev 10: 0.8 -> 1.2 on the
    #   lip (r5 gate fix 5: the crisp triangular wedge where the cut met the lip's tail face / bottom round; every visible
    #   notch edge now >= 1.0); 0.8 kept above z 11, where the cut crosses the 1.0 uu liner ring (a larger round pinched it)
    # rev 9 (rule 14 / lead ruling): behind each rear tyre the base's band + hidden plug stood as a black block between the
    # liner back wall (|y| 26.8) and the notch, up to z 11.4 - exactly in front of the axle stub from a 3/4-rear view at
    # axle height. Open it above the tail lip (z 6.4-13.5): the stub, the inner tyre and the back wall show through.
    wo = i_round(i_round(x - (X_RA - 9.0), 26.8 - ay, 0.6), np.abs(z - 9.95) - 3.55, 0.8)
    return s_round(B, wo, 0.5)


# =============================================================================
#  INTERIOR SDF (one colour moulding, seats + wheel + dash cast in)
# =============================================================================
QT_ZTOP, QT_SILL, QT_TOP = 33.4, 3.2, 0.4


def seat_back(x, y, z, cx, cy, cz, h, r, ang):
    xr, zr = rot_xz(x, z, cx, cz, ang)
    return sd_rbox(xr, y, zr, (cx, cy, cz), h, r)


def interior_sdf(x, y, z):
    ay = np.abs(y)
    tub = sd_rbox(x, y, z, (-10.75, 0.0, 12.0), (29.75, 30.0, 1.0), 1.0)  # rev 9: front edge 23.5 -> 19.0, under the dash (no strip)
    cush = sd_rbox(x, ay, z, (-3.0, 13.2, 15.0), (5.8, 5.6, 2.6), 1.8)
    back = seat_back(x, ay, z, -9.6, 13.2, 22.8, (1.7, 5.6, 8.0), 1.5, math.radians(-12))
    bol = seat_back(x, np.abs(ay - 13.2), z, -8.9, 5.1, 21.5, (1.5, 0.9, 6.6), 0.8, math.radians(-12))
    head = seat_back(x, ay, z, -11.5, 13.2, 31.6, (1.3, 3.4, 2.6), 1.25, math.radians(-12))   # rev 9: sunk 1.4 into the back (no undercut)
    seats = u_round(u_round(cush, back, 2.0), u_round(bol, head, 1.0), 1.8)        # rev 9: 1.0/0.6/0.6 -> 2.0/1.0/1.8
    # rev 7: the rear bench runs out to the side trim (|y| 26.5; the rear-arch humps below trim its outer ends) so the
    # C-pillar quarter windows look onto seat, not into the empty shell
    rc = sd_rbox(x, y, z, (-25.0, 0.0, 14.6), (5.2, 26.5, 3.2), 1.8)
    # wave 5: the rear bench back used to reach z 29.6, where the roof/rear-glass offset clip below shaved it into a free-floating
    # strip that showed through the rear window as a bright plank. Lower and thicker, so it is a seat back, not a rail.
    rbk = seat_back(x, y, z, -30.6, 0.0, 17.6, (2.2, 24.0, 6.0), 1.6, math.radians(-16))   # rev 9: top 24.4 -> 23.6 (clear of the trim ledge)   # rev 9: foot into the tub (no slot)
    # rev 7: two moulded head-rest bumps on the bench back (they read through the rear glass at chase distance)
    rhd = seat_back(x, np.abs(y), z, -31.9, 13.2, 24.4, (1.5, 4.2, 2.3), 1.3, math.radians(-16))
    rear = u_round(u_round(rc, rbk, 1.4), rhd, 1.5)                                  # rev 9: 1.0/0.8 -> 1.4/1.0
    # rev 7 (round 2 review fix 1): rear side trim behind the B-pillar - a moulded wall plus the rear wheel-arch hump, as in a
    # real one-piece tub. Before, the arch keep-clear cut below left nothing at |y| > 25 behind the quarter windows, so the
    # C-pillar window looked into the dark inside of the zamac shell (the 'black hole'). The trim tops out at z 23.0, under the
    # window piece (its footprint starts at z ~23.8), and the shell clip below trims it parallel to the body side. Front of
    # the B-pillar nothing changes (front-end renders untouched).
    # The quarter trim rail rises to z 27 behind the lower third of the C-pillar window (the window opening starts at z 26.4)
    # so that window always shows a lit moulded surface 1 uu behind the glass; all of the side trim is kept >= 1.0 uu
    # behind the window piece's inner face (shell offset 5.6 vs the glass inner face at 4.58).
    # rev 7: behind the front seats the shell clip uses the TRUE cabin field. outer_master is a union of the lower body
    # and the greenhouse whose floor is a slab at z 22.5; inside the cabin between z 22.5 and the lower-body top (~25)
    # the union reports the skin only ~2.7 uu away (it measures to the hidden internal planes), so the 4.6 uu clip
    # shaved every interior part flat across the belt line - the rear bench back became a loose 'plank' and nothing
    # could stand behind the side windows. The cabin field below has no internal planes (greenhouse without its floor,
    # bounded by the lower-body plan). Ahead of x -13 (front seats, dash, wheel: the front-hero view) nothing changes.
    # rev 9: the true cabin field everywhere (the front seat backs and the wheel rim were clipped away between z 22 and 29)
    Om = cabin_field(x, y, z)
    rr = np.hypot(x - X_RA, z - ARCH_Z)
    hump = i_round(np.abs(rr - 15.9) - 1.0, 25.4 - ay, 1.0)                       # rev 9: rounded inner edge
    wall = sd_rbox(x, ay, z, (-17.5, 31.5, 17.6), (5.0, 6.5, 6.2), 1.2)
    # rev 8 (round 3 review fix 3): the C-pillar quarter window showed a lit trim rail in its lower third under a black void
    # (the far side of the empty cabin). The quarter trim is now a moulded charcoal panel that fills the whole window
    # (z 16-33.4, x -34.3..-14.3). Its face leans in at the bottom (4.2 uu behind the glass at the window sill, 1.4 at the
    # top), so it reads as a moulded trim with a sill ledge, turned away from the high sun, not a flat lit slab.
    rail = i_round(sd_rrect2(x + 23.65, z - 24.7, 9.35, 8.7, 4.0), np.abs(ay - 28.5) - 6.5, 3.0)  # |y| 22-35, clipped (rev 9: r 1.6 -> 2.2 + r 4 side-view corners,
    #   rear end -34.3 -> -33.0: the hatch-side clip pinched its top-rear corner into a thin blade)
    side = u_round(u_round(hump, wall, 1.4), rail, 1.6)                              # rev 9: hard min -> fillets
    side = i_round(side, i_round(i_round(z - QT_ZTOP, 11.2 - z, 1.6), i_round(-46.0 - x, x + 11.5, 1.6), 1.6), 1.6)   # rev 9: front clip 12.5 -> 11.5 (was coplanar with the wall's front face)
    sb = QT_SILL * _smooth01((z - 22.5) / 4.0) - (QT_SILL - QT_TOP) * _smooth01((z - 26.4) / 7.0)   # rev 9: softer ledge ramp
    side = i_round(side, Om + 5.6 + sb, 1.6)                                       # rev 9: 0.8 -> 1.6
    rear = u_round(rear, side, 1.6)                                                  # rev 9: 1.0 -> 1.6
    # rev 5: the one-piece tub carries on behind the rear bench as a moulded boot floor (spec 4b rule 13: through the
    # rear glass you see the dark tub, not the black base slab / an empty hole)
    boot = sd_rbox(x, y, z, (-44.2, 0.0, 12.4), (4.6, 27.0, 1.2), 1.0)    # rev 9: rear end -50.8 -> -49.8, clear of the tail clip
    rear = u_round(rear, boot, 1.6)                                                  # rev 9: 1.2 -> 1.6
    # rev 3: the dash is a SOLID cowl block from the tub floor to z 24.4 (>= 12 uu of cast plastic, top face 14 uu deep),
    # not a plank, so no thin sheet can catch a specular sliver behind the windscreen
    # wave 5: the dash used to rise to z 24.4 and was then sliced flat by the windscreen offset below, which left a
    # slanted grey sheet parallel to the glass (plus skinny sliver triangles that caught the sun). It now tops out at
    # z 21.4, well under the glass, with a rounded cowl lip; the glove bin is a low pad, not a tower.
    dash = sd_rbox(x, y, z, (15.65, 0.0, 16.2), (5.15, 29.0, 5.2), 2.2)  # rev 9: foot 11.8 -> 11.0 (it is the tub front now),
    #   back face 9.2 -> 10.5: clear of the steering-wheel rim
    binn = sd_rbox(x, y, z, (14.0, 13.2, 22.2), (2.6, 5.0, 1.2), 1.15)   # rev 9: r 1.0 -> 1.15, 1.8 forward: clear of the wheel rim
    c = np.array([8.6, 13.2, 23.4]); a = np.array([-0.906, 0.0, 0.423])
    px, py, pz = x - c[0], y - c[1], z - c[2]
    pa = px * a[0] + py * a[1] + pz * a[2]
    qx, qy, qz = px - pa * a[0], py - pa * a[1], pz - pa * a[2]
    rho = np.sqrt(qx * qx + qy * qy + qz * qz)
    wheel = np.hypot(rho - 3.4, pa) - 1.05
    # rev 9 (r5 gate: torn creases where the thin spoke bar / hub met the rim): a 1:64 cast-in wheel is a thick rim over a
    # dished centre disc, no see-through spokes; the column runs into the disc on a 0.8 fillet
    disc = i_round(rho - 3.4, np.abs(pa + 0.3) - 0.55, 0.5)
    col = sd_capsule(x, y, z, tuple(c), (14.0, 13.2, 24.0), 1.3)
    steer = u_round(u_round(wheel, disc, 1.2), col, 1.2)
    cons = sd_rbox(x, y, z, (2.0, 0.0, 13.6), (9.0, 2.8, 2.2), 1.0)
    gear = u_round(sd_capsule(x, y, z, (4.0, 0.0, 14.5), (3.3, 0.0, 18.0), 0.45),
                   np.sqrt((x - 3.2) ** 2 + y ** 2 + (z - 18.5) ** 2) - 0.95, 0.6)
    # rev 9 (r5 spike/notch gate, 203 torn-crease vertices): every moulded part used to meet the tub floor / the dash in a
    # HARD min() - a 90 deg internal crease that the mesher tore into a zig-zag (seat feet, console, dash foot, bench).
    # One-piece moulding: each part is filleted into the tub (0.8) like a real injection-moulded tub.
    D = u_round(tub, seats, 2.0)
    D = u_round(D, rear, 1.3)
    D = u_round(D, dash, 1.6)
    D = u_round(D, binn, 1.4)
    D = u_round(D, cons, 1.8)
    D = u_round(D, gear, 0.9)
    D = u_round(D, steer, 1.4)
    # keep clear of the wheel-well liners and of the shell / window piece
    for xw in (X_FA, X_RA):
        D = s_round(D, i_round(np.hypot(x - xw, z - ARCH_Z) - (ARCH_R + 2.0), 25.0 - ay, 1.0), 0.8)   # rev 9: rounded keep-clear
    off = 2.6 + 2.0 * np.clip((z - 20.0) / 3.0, 0.0, 1.0)     # wave 5: a little more clearance up high (was 2.4 above z 24.5)
    return i_round(D, Om + off, 0.9)                           # rounded clip: no razor-flat cut sheet


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


def unfold_mesh(fn, V, T, name, thr=-0.05, rounds=6):
    """rev 5: the planar-dissolve + collapse decimation leaves folded (inverted) sliver triangles lying in flat panels;
    they render as thin black wedges (back faces / zero-distance AO) on the tail, the bumper, the stripes and the nose.
    Collapse the shortest edge of every triangle whose winding opposes the SDF gradient (or that has no area),
    reproject the merged vertex onto the surface, repeat. Off-surface parts (none here) are left alone."""
    t0 = time.time()
    bm = bmesh.new()
    vs = [bm.verts.new(tuple(v)) for v in V]
    for t in T:
        try:
            bm.faces.new([vs[int(i)] for i in t])
        except ValueError:
            pass
    n_first = n_last = 0
    for r in range(rounds):
        F = list(bm.faces)
        P = np.array([[l.vert.co[:] for l in f.loops] for f in F])
        n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); a = np.linalg.norm(n, axis=1)
        n /= np.maximum(a, 1e-12)[:, None]
        on = np.abs(eval_chunked(fn, P.reshape(-1, 3))).reshape(-1, 3).max(1) < 0.08
        g = sdf_grad(fn, P.mean(1), eps=0.05); g /= np.maximum(np.linalg.norm(g, axis=1), 1e-12)[:, None]
        bad = (((n * g).sum(1) < thr) | (a < 1e-8)) & on
        n_last = int(bad.sum())
        if r == 0:
            n_first = n_last
        if not n_last:
            break
        used, sel = set(), []
        for i in np.nonzero(bad)[0]:
            e = min(F[i].edges, key=lambda e: e.calc_length())
            if e.verts[0] in used or e.verts[1] in used:
                continue
            used.update(e.verts); sel.append(e)
        bmesh.ops.collapse(bm, edges=sel, uvs=False)
        moved = [v for v in used if v.is_valid and v.link_faces]
        if moved:
            Q = project(fn, np.array([v.co[:] for v in moved]), iters=3, maxstep=0.3)
            for v, q in zip(moved, Q):
                v.co = q
        tri = [f for f in bm.faces if len(f.verts) > 3]
        if tri:
            bmesh.ops.triangulate(bm, faces=tri)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.verts.index_update()
    V2 = np.array([v.co[:] for v in bm.verts], float).reshape(-1, 3)
    T2 = np.array([[v.index for v in f.verts] for f in bm.faces], np.int64).reshape(-1, 3)
    bm.free()
    log("  unfold %-12s inverted/degenerate tris %d -> %d (%d rounds), %d -> %d tris (%.1fs)" %
        (name, n_first, n_last, r + 1, len(T), len(T2), time.time() - t0))
    return V2, T2


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
    V2, T = unfold_mesh(fn, V2, T, name)          # rev 5: no folded sliver triangles (black wedges)
    N = sdf_grad(fn, V2, eps=normal_eps)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
    me2 = ob.data
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me2)
    log("  part %-14s %7d -> planar %7d -> %6d tris  (%.1fs)" % (name, ntri, nmid, len(T), time.time() - t0))
    return V2, T, N


# ---- rev 10: local adaptive refinement after the export collapse (r5 gate fixes 3 + 4 + 7) ------------------------------
# The exporter collapses the body shell to 250 k triangles (~0.45-0.7 uu facets on the small rounds). The tail's 1.4 uu
# shut-line dents, the lamp-boss edges and the tail-notch rounds are narrower than that: their walls came out as wavy /
# sawtooth highlights in the 1024-spp tail proofs (a 0.1 uu raw mesh of the same field is clean). Inside these zones every
# edge whose end normals differ by more than REFINE_DEG is split at its midpoint, the midpoint is put on the exact SDF and
# the triangles are re-cut conformingly (1->2 / 1->3 / 1->4: no T-junctions, no new boundary). No split may leave a child
# under 0.0135 uu^2 (rule-16 degenerate limit 0.01). Same method as build_Vortex.py r5b (REFINE_ZONES).
REFINE_DEG = 1.6
REFINE_MIN_CHILD_AREA = 0.0135
REFINE_ZONES = {
    # name: (x0, x1, |y|0, |y|1, z0, z1[, deg[, max edge]]) boxes in the un-raked casting frame (uu); a max edge length
    # also splits long edges along a feature whose normals do not turn lengthwise (the shut-line walls cast a stepped
    # shadow edge from 0.6 uu long facets under a raking sun)
    "BodyShell": [(-55.0, -48.6, 13.5, 32.8, 10.5, 25.6),     # tail face: shut lines, lamp-boss edges, plate boss (fix 4)
                  (-53.0, -46.0, 15.5, 20.2, 22.0, 28.5),     # shut lines over the tail-top roll + their caps (fix 3)
                  (-55.0, -47.5, 16.0, 19.6, 11.0, 28.5, None, 0.3),   # along both shut lines: <= 0.3 uu edges (fix 3/4;
                  #   rev 11: |y| 16.4-19.2 -> 16.0-19.6 for the 2.0 uu dent)
                  (-55.0, -43.5, 26.5, 40.5, 3.5, 15.0),      # tail notch edges, body + bumper (fix 5)
                  (-50.5, -42.0, 23.0, 39.5, 24.5, 27.5, 0.8, 0.4),   # hip top / deck morph behind the C-pillar (fix 2;
                  #   <= 0.4 uu edges: the 6 deg grazing sun drew the facet outlines of the flat deck into the highlight)
                  (-50.0, -30.0, 33.0, 42.0, 20.0, 27.5, 2.2),    # the hip's 2.6 roll, C-pillar foot to tail (fix 1/2)
                  (-55.0, -50.0, 19.7, 21.3, 17.4, 23.6, 1.0, 0.3),   # rev 11: tail-lamp boss inner wall (the wider
                  #   shut-line dent re-tessellated it: a short sawtooth in proof_clay_tail_R)
                  (50.5, 58.5, 15.3, 29.9, 13.8, 20.6, 1.4)],   # rev 11: headlamp bosses + lens domes (owner: lumpy
                  #   bezel edges, faceted dome walls)
    "Base": [(-56.0, -43.5, 26.5, 40.5, 1.0, 9.0)],           # tail notch through the base lip (fix 5)
    "Windows": [(-37.0, 16.0, 24.0, 33.5, 25.3, 28.5, 1.0)],  # side panes' visible bottom (fix 7; the rim below z 25.1
    #   stays as collapsed: refining its 1.1 uu half-round partly left a broken crease)
}


def _zone_deg(P, boxes, default):
    """per point: the refinement angle (deg) and max edge length (uu) of the boxes it falls in (else inf, inf)"""
    x, ay, z = P[:, 0], np.abs(P[:, 1]), P[:, 2]
    deg = np.full(len(P), np.inf); lmax = np.full(len(P), np.inf)
    for bx in boxes:
        x0, x1, y0, y1, z0, z1 = bx[:6]
        m = (x >= x0) & (x <= x1) & (ay >= y0) & (ay <= y1) & (z >= z0) & (z <= z1)
        deg[m] = np.minimum(deg[m], bx[6] if len(bx) > 6 and bx[6] else default)
        if len(bx) > 7:
            lmax[m] = np.minimum(lmax[m], bx[7])
    return deg, lmax


def refine_local(V, T, fn, boxes, max_deg=REFINE_DEG, rounds=3, name=""):
    """conforming adaptive midpoint refinement inside boxes (see REFINE_ZONES); returns V, T"""
    V = np.asarray(V, float).copy(); T = np.asarray(T, np.int64).copy()
    n0 = len(T)
    for rnd in range(rounds):
        nV, nT = len(V), len(T)
        N = sdf_grad(fn, V, eps=0.02)
        N /= np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
        E = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1)
        key = E[:, 0] * nV + E[:, 1]
        uk, inv = np.unique(key, return_inverse=True)
        ea, eb = uk // nV, uk % nV
        P = V[T]
        area = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
        eid = inv.reshape(3, nT).T
        ang = np.degrees(np.arccos(np.clip((N[ea] * N[eb]).sum(1), -1.0, 1.0)))
        mid = 0.5 * (V[ea] + V[eb])
        zdeg, zlen = _zone_deg(mid, boxes, max_deg)
        split = (ang > zdeg) | (np.linalg.norm(V[ea] - V[eb], axis=1) > zlen)
        for _ in range(8):
            cnt = split[eid].sum(1)
            child = np.where(cnt >= 2, area / 4.0, area / 2.0)
            bad = (cnt > 0) & (child < REFINE_MIN_CHILD_AREA)
            if not bad.any():
                break
            split[eid[bad].ravel()] = False
        if not split.any():
            break
        si = np.nonzero(split)[0]
        newid = np.full(len(uk), -1, np.int64)
        newid[si] = nV + np.arange(len(si))
        Vm = project(fn, mid[si], iters=3, maxstep=0.3)
        V = np.concatenate([V, Vm])
        ms = split[eid]
        mv = newid[eid]
        cnt = ms.sum(1)
        out = [T[cnt == 0]]
        for r in range(3):
            Tr = np.roll(T, -r, axis=1); msr = np.roll(ms, -r, axis=1); mvr = np.roll(mv, -r, axis=1)
            a, b, c = Tr[:, 0], Tr[:, 1], Tr[:, 2]
            m01, m12, m20 = mvr[:, 0], mvr[:, 1], mvr[:, 2]
            s1 = (cnt == 1) & msr[:, 0]
            out += [np.stack([a[s1], m01[s1], c[s1]], 1), np.stack([m01[s1], b[s1], c[s1]], 1)]
            s2 = (cnt == 2) & msr[:, 0] & msr[:, 1]
            if s2.any():
                A, B, C, M0, M1 = a[s2], b[s2], c[s2], m01[s2], m12[s2]
                out.append(np.stack([M0, B, M1], 1))
                d1 = np.linalg.norm(V[A] - V[M1], axis=1); d2 = np.linalg.norm(V[M0] - V[C], axis=1)
                q = d1 <= d2
                out += [np.stack([A[q], M0[q], M1[q]], 1), np.stack([A[q], M1[q], C[q]], 1),
                        np.stack([A[~q], M0[~q], C[~q]], 1), np.stack([M0[~q], M1[~q], C[~q]], 1)]
            if r == 0:
                s3 = cnt == 3
                out += [np.stack([a[s3], m01[s3], m20[s3]], 1), np.stack([m01[s3], b[s3], m12[s3]], 1),
                        np.stack([m20[s3], m12[s3], c[s3]], 1), np.stack([m01[s3], m12[s3], m20[s3]], 1)]
        T = np.concatenate(out)
        log("  refine %s round %d: %d edges split -> %d tris" % (name, rnd, len(si), len(T)))
    log("refine %-12s %d -> %d tris (+%d)" % (name, n0, len(T), len(T) - n0))
    return V, T


def refined(fn, name, V, T, N):
    """refine the named SDF part's REFINE_ZONES (no-op for other parts / an empty box-clipped part)"""
    if name not in REFINE_ZONES or len(T) == 0:
        return V, T, N
    V2, T2 = refine_local(V, T, fn, REFINE_ZONES[name], name=name)
    if len(T2) == len(T):
        return V, T, N
    N2 = sdf_grad(fn, V2, eps=0.02)
    return V2, T2, N2 / np.maximum(np.linalg.norm(N2, axis=1), 1e-12)[:, None]


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


AXLE_SEG = 20                        # = W.axle_head_geo's default seg, so the tube end rings coincide with the head shanks


def axle_tube(xc, zc, r, y_end, seg=AXLE_SEG, step=2.0):
    """rev 6 (spec 4b rule 16): steel axle tube from -y_end to +y_end with a ring every <= `step` uu (the old 2-ring tube
    was 64 needle triangles 78 uu long) and NO caps: its end rings sit exactly on the peened heads' shank rings
    (y_end = head y_outer - 1.2, same radius and segment count), so the export weld makes axle + heads one closed solid
    (no open tube ends, no hidden tube end inside a head)."""
    n = max(2, int(math.ceil(2.0 * y_end / step)) + 1)
    ys = np.linspace(-y_end, y_end, n)
    ang = 2.0 * np.pi * np.arange(seg) / seg
    cs, sn = np.cos(ang), np.sin(ang)
    V = np.concatenate([np.stack([xc + r * cs, np.full(seg, yv), zc + r * sn], 1) for yv in ys])
    N = np.tile(np.stack([cs, np.zeros(seg), sn], 1), (n, 1))
    T = []
    for i in range(n - 1):
        a0, a1 = i * seg, (i + 1) * seg
        for k in range(seg):
            k2 = (k + 1) % seg
            T += [(a0 + k, a1 + k, a1 + k2), (a0 + k, a1 + k2, a0 + k2)]
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


def uv1_tampo(ob, misc_mask_fn=None, side_band=False):
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
    if side_band:
        # rev 7 (round 2 review fix 2): on the body-side print band every face that is not a top/bottom face takes the SIDE
        # projection by which side of the car it is on, not by its normal. The stripes used to tear into ragged chips where
        # they cross the door-front shut line and the front flare's rear step (x 19-23): those groove walls / step faces
        # face +-X, so they fell into the front/rear islands (no ink) face by face. Now the print carries continuously over
        # the step like a real tampo pad (v = z, so the horizontal stripes stay straight; u only stretches across the step).
        cx, cy_, cz = cen[:, 0], cen[:, 1], cen[:, 2]
        band = (np.abs(cy_) >= 29.0) & (cz >= Z_SILL - 0.5) & (cz <= 24.5) & (cx > -46.0) & (cx < 50.5) & \
               ((np.abs(nz) < 0.7) | ((np.abs(nz) < 0.92) & (np.abs(cx - ROUNDEL['x']) < ROUNDEL['r'] + 1.5))) & \
               (cy_ * ny > -0.25)
        # rev 11 (owner: the door roundel 'feels off'): the roundel's top runs onto the door's top roll, whose faces tip past
        # nz 0.7 from z ~23.6 - they took the TOP projection (no roundel ink) and the disc + ring were cut off flat with a
        # ragged edge. Over the roundel the band takes faces up to nz 0.92, so the pad print wraps the roll (seen from the
        # side the roundel is a full circle). Elsewhere along the side nothing changes (no other side ink above z 17.5).
        cls[band & (cy_ > 0)] = 0
        cls[band & (cy_ < 0)] = 1
        # rev 11 (owner 17 Oct, headlamps: body-blue crescents between each lens and its bezel): the lens domes' walls and
        # the boss's rounded rim face +-Y / +-Z, so they fell into the side / top islands (no lamp ink) face by face - jagged
        # blue shards round every lens. Every face of the headlamp boss now takes the FRONT projection like a pad print
        # pressed onto it: the lens print wraps its dome wall, and the rim beyond the printed bezel is plain body colour.
        lamp = (np.abs(np.abs(cy_) - HL_Y) <= HL_HY + 0.3) & (np.abs(cz - HL_Z) <= HL_HZ + 0.3) & \
               (cx >= nose_x(cz) - 0.3) & (nx > -0.3)
        cls[lamp] = 3
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


def do_uvs(ob, misc_mask_fn=None, side_band=False):
    W.smart_uv(ob, "UV0", angle=60.0, margin=0.002)
    return uv1_tampo(ob, misc_mask_fn, side_band)


# =============================================================================
#  TAMPO (procedural UV1 livery "Old Faithful": 1991 rally-hatch graphics)
# =============================================================================
TAMPO_RES = 2048
INK = {   # sRGB 0-1 (tampo inks are opaque, matte-ish)
    'white': (0.94, 0.93, 0.89), 'yellow': (0.98, 0.76, 0.07), 'red': (0.86, 0.16, 0.08),
    'black': (0.045, 0.045, 0.05), 'silver': (0.74, 0.75, 0.76), 'lens': (0.96, 0.96, 0.93),
    'fog': (0.99, 0.85, 0.25), 'tail': (0.70, 0.035, 0.04), 'amber': (0.98, 0.52, 0.06),
    # rev 5 (appended LAST so every earlier ink keeps its registration offset): aged cream plate, dark lamp-rim red
    'plate': (0.90, 0.85, 0.66), 'taildk': (0.36, 0.02, 0.03),
    # rev 11 (appended LAST again): the roundel's red ring as its own plate, registered tight to the white disc
    'ring': (0.86, 0.16, 0.08),
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


def _seven_poly(tb, wd, x_foot, xl=-1.95, xr=2.0):
    """the italic roundel 7 in a 6-unit glyph box: top bar tb thick, a diagonal of constant horizontal width wd whose
    right edge ends at x_foot on the baseline"""
    a = (xr, 3.0 - tb + 0.12); b = (x_foot, -3.0)
    k = (a[0] - b[0]) / (a[1] - b[1])
    c = (x_foot - wd, -3.0)
    return [(xl, 3.0), (xr, 3.0), a, b, c, (c[0] + k * ((3.0 - tb) - c[1]), 3.0 - tb), (xl, 3.0 - tb)]


# rev 11 (owner 17 Oct: "the 7 isn't centred and feels off"). The old 7 centred its polygon's bounding box, but its ink
# centroid sat 0.14 right / 0.56 high (heavy top bar, italic shear pushing the bar right and the foot left), and its
# strokes were ~1.3 uu against the 0.75 ring. Now: strokes ~1.03 (bar) / ~1.1 (diagonal) = ~1.4x the ring, cap 5.4
# (was 5.6), a more upright diagonal (foot centred under the bar), and the ink CENTROID sits on the disc centre, lifted
# 0.15 uu (optical centre; clearances to the disc edge 0.96 top / 0.36 bottom - the foot no longer crowds the edge).
# The roundel also shrank 4.8 -> 4.45 and dropped 0.25 (see ROUNDEL): its top used to run onto the door's 2.6 top roll at
# z 24.4, where the faces tip past the side-band limit - the printed disc and ring were chopped off flat with a ragged
# edge, which made the whole roundel read lopsided. The 7 scales with it (RS), keeping its ~1.4x stroke-to-ring ratio.
RS = 4.45 / 4.8
SEVEN_H, SEVEN_SHEAR, SEVEN_LIFT = 5.4 * RS, 0.16, 0.15 * RS
SEVEN = _seven_poly(1.03 * RS / (SEVEN_H / 6.0), 1.22 * RS / (SEVEN_H / 6.0) / math.cos(math.radians(25.0)), -0.10)


def _seven_centroid():
    g = np.arange(-4.0, 4.0, 0.005)
    u, v = np.meshgrid(g, g)
    m = sd_poly(u - SEVEN_SHEAR * v, v, SEVEN) <= 0.0       # the sheared figure, glyph units
    return float(u[m].mean()), float(v[m].mean())


SEVEN_C = _seven_centroid()


def glyph_7(gx, gz, h=SEVEN_H):
    s = h / 6.0
    u = gx / s + SEVEN_C[0]
    v = (gz - SEVEN_LIFT) / s + SEVEN_C[1]
    return sd_poly(u - SEVEN_SHEAR * v, v, SEVEN) * s          # italic; ink centroid -> (0, SEVEN_LIFT)


def stripe(x, z, z0, z1, xr, xf):
    k = math.sqrt(1 + TAMPO_SLANT ** 2)
    dz = np.abs(z - 0.5 * (z0 + z1)) - 0.5 * (z1 - z0)
    dxf = (x - (xf + TAMPO_SLANT * (z - 12.0))) / k
    dxr = ((xr + TAMPO_SLANT * (z - 12.0)) - x) / k
    return np.maximum(dz, np.maximum(dxf, dxr))


PLATE_H, PLATE_T = 1.5, 0.30          # rev 11: cap height on the 2.84-tall field (was 2.0), stroke (was 0.40)
PLATE_W = 0.90                        # ink width of O / F / 9
PLATE_GAP, PLATE_SPACE = 0.36, 0.95   # the same ink gap between the letters of a word, a real word space


def _pseg(x, z, a, b, r):
    return sd_capsule(x, z, np.zeros_like(x), (a[0], a[1], 0.0), (b[0], b[1], 0.0), r)


def _plate_glyphs():
    """centre-line glyphs, uniform round strokes; each (sdf fn, ink x-extent lo, hi) about its own origin"""
    c = 0.5 * PLATE_T
    a = 0.5 * PLATE_W - c                 # centre-line half width
    b = 0.5 * PLATE_H - c                 # centre-line half height
    def O(x, z):
        return np.abs(sd_rrect2(x, z, a, b, 0.92 * a)) - c
    def F(x, z):
        d = _pseg(x, z, (-a, -b), (-a, b), c)
        d = np.minimum(d, _pseg(x, z, (-a, b), (a, b), c))
        return np.minimum(d, _pseg(x, z, (-a, 0.04), (a - 0.12, 0.04), c))
    bh = 0.62 * b                         # the 9: an open bowl in the top 2/3, a straight stem, a round tail
    zb, zt = b - bh, -b + a
    def N9(x, z):
        bowl = np.abs(sd_rrect2(x, z - zb, a, bh, 0.92 * a)) - c
        stem = _pseg(x, z, (a, zb), (a, zt), c)
        tail = sd_arc(x, z, 0.0, zt, a, -140.0, 0.0) - c
        return np.minimum(np.minimum(bowl, stem), tail)
    f1, s1 = (-0.30, b - 0.26), 0.08      # the 1: flag end, stem x
    def N1(x, z):
        return np.minimum(_pseg(x, z, (s1, -b), (s1, b), c), _pseg(x, z, (s1, b), f1, c))
    return [(O, -a - c, a + c), (F, -a - c, a + c), (N9, -a - c, a + c), (N1, f1[0] - c, s1 + c)]


def _plate_layout():
    """origins with even ink gaps + a word space, then the whole string centred on the plate by its INK bounding box
    (measured on a 0.004 uu raster)"""
    G = _plate_glyphs()
    xs, x = [], 0.0
    for i, (fn, lo, hi) in enumerate(G):
        if i:
            x += PLATE_SPACE if i == 2 else PLATE_GAP
        xs.append(x - lo)
        x += hi - lo
    gx, gz = np.meshgrid(np.arange(-1.0, x + 1.0, 0.004), np.arange(-1.2, 1.2, 0.004))
    d = np.full(gx.shape, 9.0)
    for (fn, _, _), x0 in zip(G, xs):
        d = np.minimum(d, fn(gx - x0, gz))
    ink = d <= 0.0
    cx = 0.5 * (gx[ink].min() + gx[ink].max()); cz = 0.5 * (gz[ink].min() + gz[ink].max())
    return [(fn, x0 - cx) for (fn, _, _), x0 in zip(G, xs)], -cz


PLATE_GLYPHS, PLATE_DZ = _plate_layout()


def plate_text(gx, gz):
    """'OF 91' on the plate; gx runs left->right as seen from behind, origin at the plate centre.
    rev 11 (owner 17 Oct: 'the 91 feels off-centre - centre it, smaller font'): rev 5 set h 2.0 (0.42 margins on the
    2.84 field), its ink box sat 0.10 left of centre, and the '1' (slot 1.49 + 1.49) jammed its flag into the '9'. Now
    cap height 1.5 (0.67 to the field edge), uniform 0.30 round strokes, the same 0.36 ink gap inside each word and a
    0.95 word space, the string centred by its ink bbox; the 9 = open bowl + straight stem + round tail (reads as a 9,
    not a g / 8 / 'J' at 1:64)."""
    d = None
    for fn, x0 in PLATE_GLYPHS:
        e = fn(gx - x0, gz - PLATE_DZ)
        d = e if d is None else np.minimum(d, e)
    return d


ROUNDEL = dict(x=2.6, z=19.35, r=4.45, ring=0.70)   # rev 11: was z 19.6, r 4.8, ring 0.75 (top now z 23.8, on the flat)
BADGE = dict(x=-35.5, z=31.2, h=2.3)   # rev 8: 1.2 up, 0.5 forward on the C-pillar - its clear-coat mirror image left the shoulder


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
        L.append(('ring', ring))
        gx = (x - ROUNDEL['x']) * rd; gz = z - ROUNDEL['z']
        disc = np.maximum(rnd - (ROUNDEL['r'] - ROUNDEL['ring'] + 0.05), -glyph_7(gx, gz))   # "7" knocked out
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
        # rev 11: the bezel prints the boss's whole flat face, ending where its 0.5 rim round starts (a crisp rounded edge
        # on the flat, not a wobbly one half-way down the round); each lens prints its whole dome (top + wall, to the
        # foot fillet) - no blue crescent; registered exactly to the cast bosses (see make_tampo)
        L.append(('silver', sd_rrect2(ay - HL_Y, z - HL_Z, HL_HY - 0.45, HL_HZ - 0.45, HL_R - 0.45)))
        L.append(('lens', np.hypot(ay - HL_DOMES[0][0], z - HL_Z) - (HL_DOMES[0][1] + HL_LENS_WRAP)))
        L.append(('fog', np.hypot(ay - HL_DOMES[1][0], z - HL_Z) - (HL_DOMES[1][1] + HL_LENS_WRAP)))
        L.append(('silver', np.maximum(np.abs(np.hypot(ay - HL_DOMES[0][0], z - HL_Z) - 0.7) - 0.18, 0.0 - 1.0)))
    elif region == 'rear':
        y, z = P['y'], P['z']
        ay = np.abs(y)
        # rev 5: printed lamps on the cast bosses - a dark-red rim (the pad prints the flat face only, so the boss's
        # rounded edge stays body colour), red lens, amber indicator at the outer end, a narrow white reverse lamp at
        # the inner end, hairline separators.
        rim = sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY - 0.35, TL_HZ - 0.35, 1.0)
        lens = sd_rrect2(ay - TL_Y, z - TL_Z, TL_HY - 0.75, TL_HZ - 0.75, 0.75)
        L.append(('taildk', rim))
        L.append(('tail', lens))
        L.append(('amber', np.maximum(lens, (TL_Y + 2.1) - ay)))
        L.append(('white', np.maximum(lens, ay - (TL_Y - 3.0))))
        L.append(('taildk', np.maximum(lens, np.minimum(np.abs(ay - (TL_Y + 2.1)), np.abs(ay - (TL_Y - 3.0))) - 0.14)))
        # rev 5: the plate - printed on the cast (recessed) plate panel: black border, aged cream field, black "OF 91"
        L.append(('black', sd_rrect2(y, z - 18.6, 7.55, 1.85, 0.55)))
        L.append(('plate', sd_rrect2(y, z - 18.6, 7.1, 1.42, 0.35)))
        L.append(('black', plate_text(-y, z - 18.6)))
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
    for ink in ('black', 'plate', 'taildk'):                          # rev 5: the small rear prints sit tighter
        reg[(ink, 'B')] = (0.4 * reg[(ink, 'B')][0], 0.4 * reg[(ink, 'B')][1])
    # rev 11b (review of the owner's plate note: "OF 91" sat ~0.27 uu LOW on the cream field because the field used the
    # 'plate' ink offset and the text/border the 'black' one): the plate is one small print, so field, border and text
    # register together and the centred text stays centred.
    reg[('plate', 'B')] = reg[('black', 'B')]
    # rev 11 (owner: the roundel 'feels off'): the ring printed with the red stripes' 0.3-0.5 uu offset against the
    # white key disc - a blue crescent on one side, red over white on the other. Ring now ~0.1 uu off the disc.
    for ink in ('silver', 'lens', 'fog'):                             # rev 11: headlamp prints sit exactly on their bosses
        reg[(ink, 'F')] = (0.0, 0.0)
    for side in ('L', 'R'):
        reg[('ring', side)] = (0.25 * reg[('ring', side)][0], 0.25 * reg[('ring', side)][1])
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
        # rev 11 (owner 17 Oct: a dark vertical band where the white stripe crosses the door shut line): the old 0.76 uu
        # wide x-band printed every ink at 35 % - a smeared blue band over the whole dent. A pad print crossing a shut
        # line leaves a THIN, CONSISTENT break where the pad cannot reach the bottom of the line: 0.24 uu wide, almost no
        # ink, anti-aliased, registered to the casting (the same break through every ink), full ink either side.
        if region == 'side':
            dgap = np.minimum(np.abs(Pm['x'] - DOOR_FX), np.abs(Pm['x'] - DOOR_RX))
            gapk = 1.0 - 0.92 * np.clip((DOOR_PRINT_GAP + 0.5 * px - dgap) / px, 0.0, 1.0)
        else:
            gapk = np.ones(len(idx[0]), np.float32)
        R_ = rgb[idx]; A_ = alpha[idx]; M_ = metal[idx]
        # evaluate each ink layer with its own registration offset
        for li, (ink, _) in enumerate(tampo_layers(region, Pm, rd)):
            dx, dz = reg[(ink, side)]
            Q = dict(Pm)
            Q[a0] = Pm[a0] - dx; Q[a1] = Pm[a1] - dz
            d = tampo_layers(region, Q, rd)[li][1] + wob
            cov = np.clip(0.5 - d / px, 0.0, 1.0) * dens * (1.0 - pin)
            cov = cov * gapk * 0.97
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
FLAKE_MODE = 'bold'                    # rev 11c (owner 17 Oct ~16:45: "the before flakes look way better"): 'bold' = the
                                       # r5b flake (850 cells, per-flake tilt in the metallic base); 'fine' = rev 11 sparkle
FLAKE_SPARKLE = 0.06                   # rev 11: weight of the additive flake glint (Vortex r5b: 0.08 x metallic)
FLAKE_SCALE = 850.0 if FLAKE_MODE == 'bold' else 1300.0   # rev 11 fine: 850 -> 1300 per m
FLAKE_TINT = (0.72, 0.84, 1.0)         # cool silver-blue metallic flake
FLAKE_GLINT_ROUGH = 0.16


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
    vor = N('ShaderNodeTexVoronoi'); vor.inputs['Scale'].default_value = FLAKE_SCALE
    L(tc.outputs['Object'], vor.inputs['Vector'])
    fl = N('ShaderNodeVectorMath'); fl.operation = 'MULTIPLY_ADD'
    L(vor.outputs['Color'], fl.inputs[0]); fl.inputs[1].default_value = (2, 2, 2); fl.inputs[2].default_value = (-1, -1, -1)
    fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; fs.inputs['Scale'].default_value = 0.12
    L(fl.outputs[0], fs.inputs[0])
    fa = N('ShaderNodeVectorMath'); fa.operation = 'ADD'
    L(geo.outputs['Normal'], fa.inputs[0]); L(fs.outputs[0], fa.inputs[1])
    fnrm = N('ShaderNodeVectorMath'); fnrm.operation = 'NORMALIZE'; L(fa.outputs[0], fnrm.inputs[0])
    # rev 11 (owner 17 Oct: "weird normal map" between the doors = grainy grit + dark speckle): the per-flake normal tilt
    # (+-0.12) used to go into the metallic BASE, so every flake tilted away from the light went dark - a coarse grit over
    # all the paint, darkest in the shut-line coves. Same clamp as build_Vortex.py r5b (flake_sparkle_only): the base
    # shades with the smooth surface normal; the flakes come back as a separate ADDITIVE glossy glint (tint x
    # FLAKE_SPARKLE, none under tampo ink) - a fine sparkle that can brighten, never darken.
    if FLAKE_MODE == 'bold':
        # rev 11c: the owner prefers the r5b look - flake tilt in the metallic base (bold grain + sparkle); under tampo
        # ink the flake tilt goes away (ink is flat)
        nmix = N('ShaderNodeMix'); nmix.data_type = 'VECTOR'
        L(ti.outputs['Alpha'], nmix.inputs['Factor']); L(fnrm.outputs[0], nmix.inputs[4]); L(geo.outputs['Normal'], nmix.inputs[5])
        L(nmix.outputs[1], bs.inputs['Normal'])
    else:
        gl = N('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = FLAKE_GLINT_ROUGH
        L(fnrm.outputs[0], gl.inputs['Normal'])
        noink = W._math(nt, 'SUBTRACT', 1.0, ti.outputs['Alpha'])
        gsc = N('ShaderNodeVectorMath'); gsc.operation = 'SCALE'; gsc.inputs[0].default_value = FLAKE_TINT
        L(W._math(nt, 'MULTIPLY', noink, FLAKE_SPARKLE), gsc.inputs['Scale'])
        L(gsc.outputs[0], gl.inputs['Color'])
        gadd = N('ShaderNodeAddShader')
        out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
        L(bs.outputs[0], gadd.inputs[0]); L(gl.outputs[0], gadd.inputs[1]); L(gadd.outputs[0], out.inputs['Surface'])
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
    fr = nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.56   # rev 8: polystyrene-like toy glazing (was 1.49): the thick clear piece reads as a surface
    mx = nt.nodes.new('ShaderNodeMixShader')
    # rev 6 (spec 4b rules 5/13): Fresnel only on the FRONT faces. On a back face Cycles inverts the IOR, so where the
    # thick piece wedges round the bottom of the rear glass the inner surface went total-internal-reflection = a mirror,
    # and the rear window rendered as an opaque dark sheet whatever the tint or interior colour. Without it the dark
    # tub (seat backs, boot floor) shows through the rear glass like the clear window piece of a real casting.
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    front = nt.nodes.new('ShaderNodeMath'); front.operation = 'SUBTRACT'; front.inputs[0].default_value = 1.0
    nt.links.new(geo.outputs['Backfacing'], front.inputs[1])
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MULTIPLY'
    nt.links.new(fr.outputs[0], fac.inputs[0]); nt.links.new(front.outputs[0], fac.inputs[1])
    nt.links.new(fac.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2])
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
           'Roughness', 0.65)       # rev 8: back near UE MI_ToyPlastic_Interior* (0.72); 0.42 gave a greige sheen on lit trim
    make_glass_material()


# =============================================================================
#  Build all parts
# =============================================================================
def build_body(coll, q):
    cell = 0.5 if q else 0.25
    parts = []
    # rev 5: domain floor 7.0 -> 4.0 (a whole number of cells, so the grid - and the front - stays where it was); budget
    # +2k for the new tail so the rest of the shell keeps its triangle density
    V, T, N = sdf_part("BodyShell", body_sdf, (-56.5, -43.5, 4.0), (60.5, 43.5, 44.5), cell,
                       target_tris=31000 if q else 66000)
    V, T, N = refined(body_sdf, "BodyShell", V, T, N)          # rev 10: local refinement (REFINE_ZONES)
    parts.append(dict(V=V, T=T, N=N, mat=0))
    g = rally_geo()
    c2 = 0.14 if q else 0.07
    lo = (RL_XB - 0.6, -RL_Y - RL_R - 0.6, g['zc'] - RL_R - 0.6)
    hi = (RL_XF + 0.9, RL_Y + RL_R + 0.6, g['zc'] + RL_R + 0.6)
    V, T, N = sdf_part("RallyPods", rally_pod, lo, hi, c2, 5200)     # rev 9: 2600 -> 5200 (rim + seat rounds need the faces)
    parts.append(dict(V=V, T=T, N=N, mat=1))
    V, T, N = sdf_part("RallyLens", rally_lens, lo, hi, c2, 2400)     # rev 9: 1200 -> 2400
    parts.append(dict(V=V, T=T, N=N, mat=2, col=np.tile(list(RALLY_TINT) + [1.0], (len(V), 1))))
    lo = (BAR_X - 1.6, -RL_Y - 1.4, g['bar_z']); hi = (BAR_X + 1.9, RL_Y + 1.4, g['bar_z'] + 2.4)
    V, T, N = sdf_part("RallyStalks", rally_stalk, lo, hi, c2, 400)
    parts.append(dict(V=V, T=T, N=N, mat=3))
    _separate_touching_parts(parts)
    return build_object("SM_HatchlingS_Body", parts, ["Paint", "Chrome", "Lamp", "Zamac"], coll)


def _separate_touching_parts(parts, tol=0.015, push=0.03):
    """rev 10: the rally pods / stalks are separate meshes that pass into the cast roof bar; where their intersection
    curves cross, a vertex of one part can land within the rule-16 near-duplicate distance (0.01 uu) of a vertex of
    another by chance (the r5b probe: one pair on the bar top at (2.2, -11.2, 41.7)). Such a vertex of a later (small)
    part is moved 0.03 uu inward along its own normal - it sits on the buried intersection curve, so nothing visible
    changes."""
    from mathutils.kdtree import KDTree
    for k in range(1, len(parts)):
        prev = np.concatenate([p["V"] for p in parts[:k]])
        kd = KDTree(len(prev))
        for i, v in enumerate(prev):
            kd.insert(tuple(v), i)
        kd.balance()
        V, N = parts[k]["V"], parts[k]["N"]
        hit = [i for i, v in enumerate(V) if kd.find(tuple(v))[2] < tol]
        if hit:
            V = V.copy(); V[hit] -= push * N[hit]; parts[k]["V"] = V
            log("  part %d: %d vertices within %.3f uu of an earlier part moved %.2f inward" % (k, len(hit), tol, push))


def build_base(coll, q):
    cell = 0.44 if q else 0.22
    V, T, N = sdf_part("Base", base_sdf, (-58.0, -40.0, 0.5), (61.5, 40.0, 26.0), cell,
                       target_tris=8000 if q else 13500)
    V, T, N = refined(base_sdf, "Base", V, T, N)                # rev 10: local refinement (REFINE_ZONES)
    col = np.zeros((len(V), 4)); col[:, 3] = 1.0
    for (rx, ry) in RIVETS:
        m = (np.hypot(V[:, 0] - rx, V[:, 1] - ry) < 2.25) & (V[:, 2] < Z_BOT + 0.4)
        col[m, 1] = 1.0
    # rev 5: the exhaust tip is bare zamac (Col R = steel, like the axles) where it shows outside the lip
    m = (np.hypot(V[:, 1] - EXH_Y, V[:, 2] - (EXH_Z + 0.06 * (V[:, 0] - EXH_X0))) < EXH_R + 0.3) & \
        (V[:, 0] < tail_x(EXH_Z) - LIP_OUT + 0.4)
    col[m, 0] = 1.0
    parts = [dict(V=V, T=T, N=N, mat=0, col=col)]
    for xw in (X_FA, X_RA):
        # rev 6: ringed tube that ends exactly on the head shanks (W01 head shank starts 1.2 inside y_outer)
        Va, Ta, Na = axle_tube(xw, AXLE_Z, AXLE_R, WHEEL_Y + W.AXLE_HEAD_Y_UU - 1.2)
        ca = np.zeros((len(Va), 4)); ca[:, 0] = 1.0; ca[:, 3] = 1.0
        parts.append(dict(V=Va, T=Ta, N=Na, mat=0, col=ca, rake=False))
        for (Vh, Th, Nh) in axle_heads(xw, AXLE_Z, WHEEL_Y + W.AXLE_HEAD_Y_UU):
            ch = np.zeros((len(Vh), 4)); ch[:, 0] = 1.0; ch[:, 3] = 1.0
            parts.append(dict(V=Vh, T=Th, N=Nh, mat=0, col=ch, rake=False))
    return build_object("SM_HatchlingS_Base", parts, ["Base"], coll)


def build_interior(coll, q):
    cell = 0.56 if q else 0.28
    V, T, N = sdf_part("Interior", interior_sdf, (-50.4, -33.0, 9.6), (24.0, 33.0, 36.0), cell,   # rev 5: x0 -42 -> -50.4 (grid-aligned)
                       target_tris=5000 if q else 60000)   # rev 9: 9000 -> 60000 (the exporter kept 40k; the filleted
    #   one-piece tub needs ~0.55 uu facets on its rounds to stay crease-free - r5 spike/notch gate)
    return build_object("SM_HatchlingS_Interior", [dict(V=V, T=T, N=N, mat=0)], ["Interior"], coll)


def build_windows(coll, q):
    cell = 0.4 if q else 0.22
    V, T, N = sdf_part("Windows", glass_sdf, (-52.0, -37.0, 21.0), (27.0, 37.0, 39.0), cell,
                       target_tris=2000 if q else 2900)
    V, T, N = refined(glass_sdf, "Windows", V, T, N)            # rev 10: local refinement (REFINE_ZONES)
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
                      "note": "black plastic band visible under the body sill in side view (spec 4b rule 4). Rev 5: behind the rear wheels it is only a thin lip (z %.1f-%.1f visible, tucked ~1.2 uu under the body-colour rear bumper) with one bare-zamac exhaust tip (Col R); there is no black rear bumper any more - the body paint wraps the tail down to z %.1f (spec 4b rule 11)" % (Z_BOT, Z_RR, Z_RR)},
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
        "tail_lamps": {"type": "cast bosses printed by the tampo (dark-red rim, red lens, amber indicator outer end, white reverse inner end); rev 5: printed plate (cream, black border, 'OF 91') between them, rev 10: on the top face of a raised 0.3 uu cast plate boss; cast body-colour rear bumper below",
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
                          "design": "1991 rally-hatch: white side band with yellow + red pinstripes (italic cut), red-ringed white door roundel with a knocked-out '7', red 'S' casting badge on the C-pillar, white twin bonnet stripes with red pinstripes, printed silver/white/yellow headlamps, black grille, red/amber/white tail lamps with a dark-red rim, cream rear plate printed 'OF 91' with a black border",
                          "flaws": "0.3-0.5 uu per-ink registration offsets, wobbly edges, density variation, pinholes, thin print in the door grooves",
                          "blend": "alpha = ink coverage; ink is matte-ish (roughness ~0.4, clearcoat reduced), metal_mask R = metallic silver ink"},
                "interior": {"color_linear": list(INTERIOR_LIN), "name": "charcoal",
                             "note": "rev 9: tub clipped by the true cabin field (front seat backs and wheel rim whole), cast-in wheel = rim over a dished disc; rev 8: mid-dark charcoal one-colour tub (spec 4b rule 13) with rear side trim + arch humps, a quarter-window trim panel and a widened rear bench, = INTERIORS['Charcoal'] in Tools/Assembly/import_castings.py (OldFaithful interior='Charcoal')"},
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
        "source": "SourceArt/Blender/HatchlingS/build_HatchlingS.py (rev 10: Opus rear pass 5b - one-piece rear quarter (long C2 flare taper, one hip roll), capped tailgate lines, raised plate boss, softer tail notch, local refinement of the tail / notch / side-pane bottoms; rev 9: Opus rear pass 5 - one-crown shoulder (no badge double image), straight-drop tail corners with a rear notch + open rear wells (axle stub visible at 3/4-rear axle height), tailgate lines into the bumper ledge, soft door/bonnet lines, flat window panes, true-cabin interior; r5 spike/notch gate 0 on every part)",
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
    tex = os.path.join(OPT['wip'], "textures") if OPT['wip'] else os.path.join(HERE, "textures")   # look-dev never touches shipped textures
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
    do_uvs(body, body_misc_mask, side_band=True)
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
    elif OPT['wip']:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OPT['wip'], ASSET + "_wip.blend"), compress=True)
    log("done in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
