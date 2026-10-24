"""
build_Vortex.py  -  MODEL '93 / CozyCarGame, Slice 1A                  (rebuild v2, 14 Oct 2026)
==================================================================================================
Die-cast casting "Vortex" (STREAKLINE, the poster car and THE LOOK TARGET). Class Wedge,
hitbox 128 x 82 x 30 uu, wheels W02_Fan.

v1 was rejected by the owner ("looks like a shrunken realistic sports-car model"). v2 is designed
as a 1993 1:64 die-cast TOY, to spec 4b:
  * cast, not assembled: one thick zamac shell, fat pillars (>= 5 uu) and a thick roof skin at the
    glass edge, body sides with draft and a tucked sill, every detail cast in as soft grooves
    (doors, bonnet lid, closed pop-up lamp lids, louvres, side-scoop fins), mirrors = tiny nubs
  * soft edges: every edge rounded 0.8-2 uu; grooves ~0.5 deep, rounded, paint-filled
  * era wheels: one-piece chrome fan disc + black plastic ring (../Wheel_W02_Fan), generous arches
    (3 uu tyre gap), thin steel axles with peened heads showing at the hub centres
  * visible base: a 4 uu band of black plastic below the sill all round, chin + diffuser, two
    rivets, a plain text panel, axles visible in their channels underneath
  * one light-smoke window moulding 2 uu thick, inset in the openings; one-colour interior tub
  * TAMPO on UV1 (generated here, preview/Vortex_tampo.png): twin lime/white stripes over the
    bonnet, roof and deck, lime/white/pink sill stripes, a "VORTEX" logotype on the doors, a
    printed rear plate; slight registration offsets and print imperfections
  * toy stance: tall-ish chunky wedge, wheels ~10 % oversized, short overhangs, 4 uu ground gap

Original design (signal-stack rule): knife-edge nose, closed pop-up lamp lids, plain doors, side
scoops ahead of the rear wheels, low cab-forward glasshouse, rear louvres, small ducktail.

Rear pass (Opus, 16-17 Oct 2026; spec 4b rules 11-16, refs Docs/Reference/DieCast/rear_ref_01/02): the body colour
wraps the whole tail down to a thin dark base lip (the base is tucked 3.6 uu inside the bumper and narrowed behind
the rear wheels); the tail is one soft casting with a shallow lamp-band dish and plate dish that take the TAMPO
(black lamp band, red lamp blocks, small VORTEX, black plate '93'); two tiny chrome exhaust nubs under the bumper;
the tail corners stay up at the sill line so the tyre bottoms show from the chase camera; behind the cab the deck
drops into an unprinted recessed engine bay - a steep rear window in its front wall (thick moulding, cab visible),
a raised engine lid with the louvres cast through it - while the sail panels keep the fastback silhouette.
r2 geometry gate fixes (raw surface-nets faults at the export grid, see the inline 'r2' notes): scoop fin ends,
groove floors/lips, lamp recess + lens edges, door-line ends, arch lip, window-moulding flange cuts, axle heads +
watertight subdivided axle tubes, base narrowing knife step, steering hub pinch.
r3 (17 Oct 2026, reviewer round-2 fixes; see the inline 'r3' notes): side-window openings are exact rounded quads
whose cut stops 1.6 uu outboard of the cab side (no scallops, no notch in the haunch at the C-pillar foot); the side
glass is a fair slab parallel to the cab side (no S-shaped lumpy shell); the rocker step fades out behind the rear
wheel (no crease at the tail corners) and the lower tail corners tuck in and lift 1.7 uu (tyres read from behind);
side / deck stripes end cleanly on flat panels; bay floor 1.6 lower so the rear window fills the bay wall (24 x 5.7);
a cast interior bulkhead closes the cab behind it (dark Black tub); tail = two cast lamp pods + plate panel between
them + small VORTEX on the bumper + one centred twin-bore exhaust (no full-width black band, no separate plate below,
no twin nubs), the tail pad printed slightly off-register.
r4 (17 Oct 2026, reviewer round-3 fixes; inline 'r4' notes): every visible radius is now above the ~0.43 uu facets of the
shipped mesh - scoop rebuilt (exact rounded outline, 1.0 lip, 0.9 floor round, full-bullnose fins with 0.6 root
fillets); door lines are one smooth swept valley ending on the shoulder crest; side-window rear-lower corner raised
(z 25.9) with a deeper rear cap and a 0.8 lip; side glass in-curve spread over 3.5 uu; tail lamp dishes moved inboard,
softer, shallower outboard, no flutes, tail faces forced to the rear UV1 chart and the lens ink fills the dish; two
separate exhaust tips; smoke glass + matt dark tub; front lens back face clear of the recess floor. The exporter's
Vortex normals are 'authored' (analytic SDF, corner-guarded) since r4.
r5b (17 Oct 2026, the r5 gate's fixes 1-8, inline 'r5b' notes): enamel flake clamp (no dark flake blotch); cab-to-haunch
fillet radius set by |y| (constant along each side: no reflection 'dashes'); parting ridge removed; door lines = one
constant section with round caps, front line on a level land across the flare; side glass = ruled lean pane, trim only
under the zamac; local conforming refinement after the export collapse (sail crest, cab band, door lines; REFINE_ZONES);
rear wells 24.0 deep + bright steel axles (stub visible from the 3/4 rear at axle height); softer quarter lift, base
tucked to |y| 25 behind the rear wheels; tampo band ends cut once through all inks, 4x edge supersampling.
r5 (17 Oct 2026, reviewer round-4 fixes + the r5 spike/notch gate; inline 'r5' notes): side-window cut runs along the
cab-side normal with an exact convex outline (rpoly_inner) - no roof tongue / shard at the C-pillar; door lines wider,
shallower, self-similar run-outs on the flat side (clear of the rocker step and the nub); scoop fins start behind a
smooth ramp; every crease the gate flagged rounded at the source (rivets, exhaust end + correctly bored tips, arch wells,
axle channels, rocker step fading into the arches, lamp recess / groove / louvre lips, base chin slot + exhaust channel,
filleted tub + solid cast steering wheel, glass flanges); per-pane glass (windows Col.R = rear pane: dark, low-reflect)
+ dark-grey tub; tampo off the rocker step, off the scoop lip and off the ducktail behind the bay.

Builds everything from an empty scene, exports export/SM_Vortex_<Part>.fbx (spec 2 settings),
writes Vortex.json, saves Vortex.blend, renders previews under the Navvy stage (identical camera,
light and deck) incl. a family shot with Navvy imported from its FBX.

Run headless:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup
      --python build_Vortex.py -- [--quick] [--norender] [--noexport] [--shots hero,family]
                                   [--samples N] [--pct N]
  --quick = coarse SDF grid + 50 % / 32 spp renders (iteration, spec 4b rule 10)

Conventions: Blender metres at game scale (1 uu = 0.01 m), front +X, left +Y, up +Z, origin at
ground level centred between the axles. Every cast part is a signed distance field in uu, meshed
with surface nets, decimated to budget, analytic normals (toolkit in ../Wheel_W02_Fan).
"""
import bpy, bmesh, math, os, sys, json, time, importlib.util
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = "Vortex"
UU = 0.01

_WPATH = os.path.join(os.path.dirname(HERE), "Wheel_W02_Fan", "build_Wheel_W02_Fan.py")
_spec = importlib.util.spec_from_file_location("build_Wheel_W02_Fan", _WPATH)
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

Prof, smoothstep, softplus_r = W.Prof, W.smoothstep, W.softplus_r
u_round, i_round, s_round, smin_poly = W.u_round, W.i_round, W.s_round, W.smin_poly
sd_rbox, sd_rrect2, sd_poly, sd_rpoly = W.sd_rbox, W.sd_rrect2, W.sd_poly, W.sd_rpoly
sd_capsule, sd_ellipsoid, round_corners, sd_seg2 = W.sd_capsule, W.sd_ellipsoid, W.round_corners, W.sd_seg2


def log(*a):
    print("[Vortex]", *a, flush=True)


def smoother(e0, e1, x):
    """r5b: C2 'smootherstep' (6t^5 - 15t^4 + 10t^3). A plain smoothstep is only C1: where it drives a fillet radius or
    a surface offset, its curvature jumps at both ends, which the gloss coat shows as a crease line / a dash in a
    reflection (the r5 haunch 'dash marks' sat on the ends of the cab-fillet widening, x -6 and x -19)"""
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * t * (t * (6.0 * t - 15.0) + 10.0)


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    o = dict(quick=False, render=True, export=True, shots=None, samples=None, pct=None, livery="classof93",
             hide=[], suffix="")
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--quick": o["quick"] = True
        elif a == "--norender": o["render"] = False
        elif a == "--noexport": o["export"] = False
        elif a == "--shots": o["shots"] = argv[i + 1].split(","); i += 1
        elif a == "--samples": o["samples"] = int(argv[i + 1]); i += 1
        elif a == "--pct": o["pct"] = int(argv[i + 1]); i += 1
        elif a == "--livery": o["livery"] = argv[i + 1]; i += 1
        elif a == "--hide": o["hide"] = argv[i + 1].split(","); i += 1
        elif a == "--suffix": o["suffix"] = argv[i + 1]; i += 1
        i += 1
    return o


OPT = parse_args()
Q = OPT["quick"]

# =============================================================================
#  Casting constants (uu, Blender axes)
# =============================================================================
WR, WW = W.WHEEL_RADIUS_UU, W.WHEEL_WIDTH_UU     # 9.8, 6.4
X_FA, X_RA = 34.0, -34.0                         # axles, wheelbase 68, origin centred
AXLE_Z = WR
WY = 34.6                                        # wheel centre |y| (show face 37.8)
AR, ARZ = 12.1, 10.1                             # arch radius / centre z: 2.6 uu over the tyre
WELL = 29.6                                      # inner wheel-well wall |y|
# r5 (lead ruling, rule 14): the REAR wells' inner wall sits 1.8 further inboard (27.8) behind x -27.5, so the steel axle
# shows as a 3.6 uu stub between the tyre's inner face (31.4) and the well / base instead of 1.8 uu deep in shadow
# r5b (gate fix 6): from the board's 3/4-rear camera (az -150, ~axle height) the line of sight to the right stub crosses
# the plane of the tyre's inner face (|y| 31.4) 1.73 uu rearward per uu outward, so every stub point outboard of
# |y| ~25.7 is hidden behind the tyre itself (measured: only a sub-pixel glint showed). The rear wells' inner wall now
# sits at |y| 24.0 (was 27.8): ~1.7 uu of bright steel stub shows past the tyre's rear edge and out under the lifted
# rear quarter. The deeper well is plain cast metal (dark from the side, like the deep wells of rear_ref_02).
WELL_R_DEEP = 5.6


def well_y(x):
    return WELL - WELL_R_DEEP * smoother(-24.5, -29.5, x)
X_NOSE, X_TAIL = 61.0, -58.0
Z_BOT = 7.6                                      # body shell bottom edge (base band below)
BASE_Z0 = 3.6                                    # base underside: 3.6 uu ground clearance
BASE_TOP = 8.8
# r5b (gate fix 7): 25.0 (was 28.6). With the r5 quarter lift the base's outer wall behind each rear wheel stood fully
# exposed as a black block from the low 3/4 rear; it now sits ~1.5 uu inboard of the painted valance's side, tucked under
# the casting (rule 11: a thin dark lip, never a block)
BASE_REAR_HALF = 25.0                            # base half width behind the rear wheels
BASE_TAIL_IN = 3.6                               # base rear end = X_TAIL + this (tucked 1.8 uu inside the bumper)
HITBOX = {"center": [0.0, 0.0, 15.0], "extent": [64.0, 41.0, 15.0]}   # 128 x 82 x 30 (spec)
RIVETS_X = (45.0, -45.0)
AXLE_R = 0.72
SHELL = 2.0                                      # zamac wall thickness at the openings

# ---- plan / side / section profiles -----------------------------------------
W_ = Prof([X_TAIL, -55.5, -51, -45, -39, -33, -27, -21, -15, -9, -3, 5, 13, 21, 28, 34, 40, 46, 51, 54.6, 58.0, X_NOSE],
          [34.6, 36.3, 38.0, 39.7, 39.9, 39.9, 39.7, 39.0, 38.1, 37.6, 37.4, 37.4, 37.6, 38.1, 38.6, 38.9, 38.9, 38.3,
           37.1, 35.5, 32.6, 28.4])
# shoulder crest: fender tops just clear the arches; low at the doors, haunches over the rear
HS_ = Prof([X_TAIL, -55.5, -51, -45, -39, -33, -27, -21, -15, -9, -3, 3, 9, 15, 21, 27, 34, 40, 45, 49.5, 53.5,
            57.5, X_NOSE],
           [23.8, 24.6, 25.2, 25.6, 25.7, 25.6, 25.1, 24.2, 23.3, 22.8, 22.6, 22.5, 22.5, 22.7, 23.0, 23.4, 23.8,
            23.4, 22.2, 20.3, 17.6, 14.6, 11.8])
# centreline: a convex wedge bonnet rising from the knife-edge nose to the windscreen; a flat
# engine deck; a small ducktail. (Hidden under the cab between x -18 and 22.)
HC_ = Prof([X_TAIL, -56.0, -53.0, -49.0, -44.0, -38.0, -32.0, -26.0, -18.0, -8.0, 2.0, 12.0, 22.0, 26.0, 30.0, 34.0,
            38.0, 42.0, 46.0, 50.0, 53.8, 57.5, X_NOSE],
           [24.4, 25.1, 24.9, 24.3, 23.9, 23.8, 24.0, 24.4, 24.8, 23.0, 22.6, 22.8, 23.1, 22.7, 22.2, 21.6, 20.9, 19.9,
            18.6, 17.0, 15.2, 13.1, 10.8])
WC_ = Prof([X_TAIL, -20, 20, 56, X_NOSE], [5.6, 5.6, 5.3, 4.6, 4.0])      # crest inset from the side
ROLL_ = Prof([X_TAIL, -40, 0, 40, 56, X_NOSE], [1.0, 1.1, 1.1, 1.1, 0.9, 0.7])
# cab: roof-edge half width, crown, side slope
YR_ = Prof([-40, -32, -24, -16, -8, 0, 8, 16, 22, 26], [31.5, 30.0, 28.0, 26.2, 25.2, 24.9, 25.2, 26.5, 27.8, 29.0])
CR, KS = 0.9, 1.55
PARTING_RIDGE = 0.0          # r5b: was 0.07 (see cabin())


def _cab_profile(x):
    L1 = 23.1 + (22.0 - x) * 0.50                # windscreen (~27 deg), close to the bonnet wedge
    L2 = 29.75 - 0.0022 * (x + 3.0) ** 2         # roof
    L3 = 29.4 + (x + 12.0) * 0.27                # rear slope over the louvres
    return smin_poly(smin_poly(L1, L2, 3.0), L3, 4.5)


_xs = np.linspace(-64, 66, 4096)
PC_ = Prof(_xs, _cab_profile(_xs))


DRAFT_Z0, DRAFT_K, DRAFT_SOFT = 12.5, 0.065, 1.0
DRAFT_SOFT_X = (22.0, 22.6)          # |x| where the soft draft onset is full / gone (inside the arch openings)


def _ramp_c2(t, a):
    """C2 smooth max(t, 0): equals t for t >= a, 0 for t <= -a (integral of a smootherstep over [-a, a])"""
    u = np.clip((t + a) / (2.0 * a), 0.0, 1.0)
    return np.where(t >= a, t, 2.0 * a * (u ** 6 - 3.0 * u ** 5 + 2.5 * u ** 4))


def tuck(z, x=None):
    """rocker step (0.75 uu inset below z 11.6, a crisp shadow line), the sill tucks under
    another 0.8, and the whole side has ~3.7 deg of draft above z 12.5.
    Owner notes 17 Oct (V4, zebra shard teeth on the lower door just above the rocker step, x +4..+13, z 12.5-13.5):
    the draft started with a hard slope break at z 12.5 (0.065 -> a 3.7 deg normal jump along one line). In that
    near-flat band every triangle straddling the line interpolated across the jump, so the zebra stripes broke into
    triangular teeth. Between the arches (x passed) the draft now starts on a C2 ramp over z 11.5-13.5 (the surface
    moves <= 0.01 uu); ahead of the front arch and behind the rear arch it is unchanged."""
    hard = DRAFT_K * np.maximum(z - DRAFT_Z0, 0.0)
    if x is None:
        dr = hard
    else:
        w = smoother(DRAFT_SOFT_X[1], DRAFT_SOFT_X[0], np.abs(x))
        dr = hard + w * DRAFT_K * (_ramp_c2(z - DRAFT_Z0, DRAFT_SOFT) - np.maximum(z - DRAFT_Z0, 0.0))
    return 0.75 * smoothstep(11.95, 11.25, z) + 0.8 * smoothstep(9.8, 7.6, z) + dr


def tuck_d(z, e=0.02):
    return (tuck(z + e) - tuck(z - e)) / (2 * e)


# r3 (tail-corner crease, reviewer fix 2 + rule 14): the crisp rocker step used to run on round the rear quarter and die
# into the tail as a notch (x -55, |y| 31.9, z 11.5) = the dark slit under the side stripe at both tail corners. Behind
# the rear wheel the step now fades out and is replaced by a smooth 1.1 uu undercut below z 12.5, so the lower tail
# corners tuck in (more black tyre shows from behind) without any crease.
STEP_FADE = (-50.5, -47.0)                       # x where the rocker step is gone / still full
TAIL_UNDERCUT = 1.4


def arch_d(x, z):
    """distance (x, z) to the nearer wheel-arch circle (negative inside the arch)"""
    return np.minimum(np.hypot(x - X_FA, z - ARZ), np.hypot(x - X_RA, z - ARZ)) - AR


def tuck_xz(x, z):
    f = smoothstep(STEP_FADE[0], STEP_FADE[1], x)              # 1 in front of the fade, 0 at the tail
    # r5 (mesh-health spike/notch gate): the crisp 0.75 rocker step used to run straight into the arch lip round, where
    # the crease dead-ended in a torn notch (x 21.6, |y| 37.4, z 11.5); it now fades out over the last ~2 uu before
    # each arch, so the arch lip cuts a plain surface
    step = 0.75 * smoothstep(11.95, 11.25, z) * smoothstep(1.1, 3.0, arch_d(x, z))
    return tuck(z, x) - step * (1.0 - f) + TAIL_UNDERCUT * smoothstep(12.5, 8.4, z) * (1.0 - f)


def tuck_xz_d(x, z, e=0.02):
    return (tuck_xz(x, z + e) - tuck_xz(x, z - e)) / (2 * e)


def arch_flare(x, z):
    """0..1 ring round each arch: the cast fender lip stands proud of the side"""
    dF = np.hypot(x - X_FA, z - ARZ) - AR
    dR = np.hypot(x - X_RA, z - ARZ) - AR
    d = np.minimum(dF, dR)
    # r2: the lip plateau starts at d 0.9 (was 0.6), outside the 0.9 arch round - where the two met the lip pinched
    # below the export grid (front arch, x 25.1 |y| 38.9 z 19.4)
    return smoothstep(3.6, 0.9, d) * smoothstep(7.2, 10.5, z)


FLARE = 0.6
ARCH_ROUND = 0.9


FLARE_DOOR_CLEAR = 1.15 + 0.25                  # flare is 0 within this distance ahead of the front door line
FLARE_DOOR_FADE = 4.0                            # ... and comes back over this distance toward the front arch


def flare_door_land(x, z):
    """r5b (gate fix 3): the FRONT door line ran down the outer ramp of the front arch's fender flare (0.6 proud,
    falling ~18 deg rearward across the groove), so one groove wall stood ~3x taller than the other and the line read
    as a lens 2x wider than the rear one. r5b held the flare level across the groove (a 'land'); owner notes 17 Oct (V3):
    the land's two compressed ramps read as a NEW lens-shaped dimple ahead of the line and a soft bump behind it.
    Now the front arch's flare simply runs out before it reaches the line: 0 within FLARE_DOOR_CLEAR (groove half width
    + 0.25) ahead of the line and everywhere behind it, back to full over FLARE_DOOR_FADE (4 uu, a <= 6 deg ramp) toward
    the arch. The groove sits on the plain door like the rear line - same section, same walls - and the lower rear of
    the front fender lip is a little lower (its flare fades out toward the door). Rear arch / front of the front arch
    unchanged."""
    f = arch_flare(x, z)
    xl, k = DOOR_LINES[0]
    s = (x - (xl - k * (z - 12.0))) / math.sqrt(1.0 + k * k)
    fade = smoother(FLARE_DOOR_CLEAR, FLARE_DOOR_CLEAR + FLARE_DOOR_FADE, s)
    return np.where(x > 5.0, f * fade, f)


def barrel(z):
    """a little vertical crown on the body sides (cast surfaces are never dead flat)"""
    t = (z - 16.5) / 7.0
    return 0.45 * np.clip(1.0 - t * t, 0.0, 1.0)


# =============================================================================
#  Body SDF
# =============================================================================
def hull_H(x, ay):
    Wx = W_(x); Hs = HS_(x); Hc = HC_(x); wc = WC_(x); roll = ROLL_(x)
    yc = Wx - wc
    t = np.clip(ay / yc, 0.0, 1.0)
    s = smoothstep(0.30, 1.0, t)
    inner = Hc + (Hs - Hc) * s
    u = np.maximum(ay - yc, 0.0) / wc
    outer = Hs - roll * u ** 1.7
    return np.where(ay < yc, inner, outer)


def hull_top_d(x, ay, z, e=0.05):
    H = hull_H(x, ay)
    hx = (hull_H(x + e, ay) - hull_H(x - e, ay)) / (2 * e)
    hy = (hull_H(x, ay + e) - hull_H(x, np.maximum(ay - e, 0.0))) / (ay + e - np.maximum(ay - e, 0.0))
    return (z - H) / np.sqrt(1.0 + hx * hx + hy * hy)


def x_front(ay, z):
    return X_NOSE - 0.0034 * ay * ay - 0.5 * softplus_r(9.4 - z, 0.8)


def x_tail(ay, z):
    return X_TAIL + 0.09 * (24.0 - z) + 0.0018 * ay * ay + tail_relief(ay, z)


# ---- REAR (Opus rear pass, 16 Oct 2026; spec 4b rules 11-15) -----------------------------------------------
# Real early-90s wedge castings from behind (Docs/Reference/DieCast/rear_ref_01/02): the body colour wraps the whole
# tail down to a thin dark base line; the lamps are a printed black/red band on a soft cast panel; the plate is a
# printed panel on the bumper; two tiny exhaust nubs poke out under the bumper. So the tail is ONE soft casting:
# shallow dished panels (slopes < 25 deg so every face stays in the UV1 rear chart and takes the print), no crisp
# recesses and no separate lamp parts.
Z_BOT_REAR = 5.5                                 # paint wraps down the tail to here; the base lip shows below
X_DROP0, X_DROP1 = -46.8, -51.8                  # the body bottom eases from Z_BOT to its tail values between these x
Z_CORNER = 9.6                                   # r3: tail-corner bottom (was Z_BOT 7.6): lifted 2.0 so the tyres read
Z_WHEEL_OPEN = 11.0                              # r5: quarter bottom behind the rear wheels, |y| > 30 (see z_bot)
# r3 tail (reviewer fix 6, originality): no full-width black band any more. Two separate soft cast LAMP PODS (deeper
# dishes, fix 7) flank a cast plate panel between them; the small VORTEX is printed on the plain body-colour bumper
# below; ONE centred twin-bore exhaust replaces the two nubs. Pod outline in (|y|, z), a wedge-raked quad.
# r4 (reviewer round-3 fix 4): the outboard end of each pod moves 1.7 inboard (|y| 31.6 -> 29.9) so the whole dish sits
# on the flat of the tail - its end wall used to fall onto the start of the 3.2 tail-to-side corner round, where the
# forward dish displacement folded into a dark scalloped wall; the dish walls are softer (transition 2.0 wide, was 1.15:
# ~0.9 lip and floor radii instead of ~0.3) and the corners rounder (1.6)
POD = [(18.0, 16.5), (29.6, 16.85), (29.9, 21.65), (18.5, 21.3)]
POD_R, POD_D = 1.6, 0.72                         # pod corner radius, dish depth
POD_W = 1.0                                      # half width of the dish wall transition (in pod_sd)
LF_Z = (18.15, 19.95)                            # (r3 cast lens flutes - unused since r4, see tail_relief)
PL_C, PL_H, PL_D = (0.0, 18.95), (7.4, 2.05), 0.35     # cast plate panel between the pods (shallow dish)
# r4 (reviewer round-3 fix 7): two DISTINCT round cast pipe tips side by side (1.5 uu apart, each bored) instead of
# two siamesed pipes with a bridge (read as a chrome dog-bone); a touch lower so the pipe tops clear the valance
EX_W, EX_Z, EX_R = 2.45, 4.6, 0.85               # half width over both pipes, centre z, pipe radius (chrome)
EX_BORE_Y, EX_BORE_R = 1.6, 0.42                # r5: bore 0.42 (was 0.47): a 0.43 wall the rim can roll over                 # pipe / bore centres at y = +-1.6, bore radius


def z_bot(x, ay):
    """body bottom edge: across the middle of the tail the painted valance drops to Z_BOT_REAR (a thin dark base lip
    shows below it); behind the rear wheels the outer corners LIFT to Z_CORNER, so from the chase camera the black tyre
    bottoms and their inner faces show under the quarters on both sides (rule 14, refs rear_ref_02 /
    ref_hw_renault5turbo_1991_canada_b)"""
    zc = Z_BOT_REAR + (Z_CORNER - Z_BOT_REAR) * smoothstep(26.0, 32.5, ay)
    zb = Z_BOT + (zc - Z_BOT) * smoothstep(X_DROP0, X_DROP1, x)
    # r5 (lead designer ruling on rules 11 + 14): from a 3/4-rear view at axle height the steel axle must show between
    # the tyre and the body. Measured: the ray from the axle stub (|y| 29-31, z 9.8) to a 3/4-rear camera passes just
    # inboard of the tyre and then under the rear quarter behind the arch, whose bottom sat at z 7.6-9.6 - it hid the
    # stub. Outboard of |y| 30 the quarter's bottom now lifts to Z_WHEEL_OPEN (11.0, above the axle top 10.5) from the
    # arch's rear edge back: the rear tyres stand free behind the arches like the open quarters of rear_ref_02. The
    # painted valance between them (|y| < 27.6) is untouched, so straight behind the tail still hides the axle (allowed).
    # r5b (gate fix 7): the lift rose over only 2.4 uu of |y| (27.6 -> 30), a near-vertical step that read as a squared
    # tab at the tail's lower corner; it now rises over 5 uu (26.5 -> 31.5) on a C2 ramp, and hull() normalises the
    # bottom-edge distance by this slope, so the 1.0 round really is ~1 uu all along the corner
    lift = smoother(26.5, 31.5, ay) * smoother(-44.6, -45.9, x)        # complete before the arch edge (x -46.1)
    return np.maximum(zb, zb + (Z_WHEEL_OPEN - zb) * lift)


def z_bot_d(x, ay, z, e=0.03):
    """r5b: (z_bot - z) normalised by the bottom edge's slope (a true distance where the lift ramps up)"""
    gy = (z_bot(x, ay + e) - z_bot(x, np.maximum(ay - e, 0.0))) / (ay + e - np.maximum(ay - e, 0.0))
    gx = (z_bot(x + e, ay) - z_bot(x - e, ay)) / (2 * e)
    return (z_bot(x, ay) - z) / np.sqrt(1.0 + gx * gx + gy * gy)


def pod_sd(ay, z):
    return sd_rpoly(ay, z, POD, POD_R)


def tail_relief(ay, z):
    """forward displacement (uu) of the tail surface: two lamp-pod dishes with cast lens flutes, the plate dish"""
    # r4: the dish shallows toward its outboard end (0.72 -> 0.32 deep), so under a raking sun the outboard end wall
    # casts a short, graded shadow instead of a dark pocket; no cast flutes any more (their ridges notched that shadow
    # into a scallop) - the lens is a smooth cast dish and the print does the rest
    pod = smoothstep(POD_W, -POD_W, pod_sd(ay, z)) * (1.0 - 0.55 * smoothstep(23.5, 29.9, ay))
    plate = smoothstep(0.75, -0.65, sd_rrect2(ay - PL_C[0], z - PL_C[1], PL_H[0], PL_H[1], 1.1))
    return POD_D * pod + PL_D * plate


def hull(x, ay, z):
    dW = W_.d(x); dt = tuck_xz_d(x, z)
    side = W_(x) - tuck_xz(x, z) + FLARE * flare_door_land(x, z) + barrel(z)
    d_side = (ay - side) / np.sqrt(1.0 + dW * dW + dt * dt)
    t = 9.4 - z
    spd = 0.5 * (1.0 + t / np.sqrt(t * t + 0.64))
    d_front = (x - x_front(ay, z)) / np.sqrt(1.0 + (0.0068 * ay) ** 2 + (0.5 * spd) ** 2)
    d_rear = (x_tail(ay, z) - x) / np.sqrt(1.0081 + (0.0036 * ay) ** 2)
    h = i_round(d_side, d_front, 4.4)
    h = i_round(h, d_rear, 3.2)
    h = i_round(h, hull_top_d(x, ay, z), 1.25)
    h = i_round(h, z_bot_d(x, ay, z), 1.0)       # r5b: normalised (was z_bot - z)
    return h


def cabin(x, ay, z):
    Pc = PC_(x); dPc = PC_.d(x)
    yr = YR_(x); dyr = YR_.d(x)
    q = ay / yr
    Zt = Pc - CR * q * q
    gx = dPc + 2.0 * CR * q * q / yr * dyr
    gy = -2.0 * CR * ay / (yr * yr)
    d_top = (z - Zt) / np.sqrt(1.0 + gx * gx + gy * gy)
    Ze = Pc - CR
    d_sd = (ay - yr - (Ze - z) / KS) * (KS / math.sqrt(1.0 + KS * KS))
    c = i_round(d_top, d_sd, 1.9)
    # faint die parting line along the roof sides (spec 4b rule 7): a 0.07 uu ridge on the edge bisector
    # r5b (gate rule 16 (d), 'faint wavy dark ripples just under the roof rail'): a 0.07 high, 0.2 wide ridge is far
    # below the shipped ~0.45 uu facets - it could only alias into ripples. Removed from the casting (PARTING_RIDGE 0);
    # rule 7 calls the seam 'occasional', so this casting has none
    if PARTING_RIDGE > 0.0:
        xw = smoothstep(-13.0, -9.0, x) * smoothstep(11.0, 7.0, x)
        c = c - PARTING_RIDGE * xw * np.exp(-((d_top - d_sd) / 0.2) ** 2)
    return np.maximum(c, np.maximum(14.0 - z, np.maximum(x - 26.0, -40.0 - x)))


def nubs(x, ay, z):
    """tiny cast mirror nubs at the A-pillar foot (spec 4b rule 1: no separate thin mirrors)"""
    return sd_ellipsoid(x, ay, z, (17.6, 29.4, 23.6), (1.8, 1.25, 1.05))


# ---- REAR DECK (Opus rear pass r2, 17 Oct 2026; rules 1, 12, 13; refs rear_ref_01/02 + ref_loose_tops_tails_ebay_b)
# Real early-90s mid-engine wedge castings seen from the chase camera: the fastback is carried back by two thick cast
# sail panels, and between them the deck drops into a recessed, UNPRINTED engine bay; at its front a steep, thick
# clear rear window shows the dark cab; in the bay sits a raised engine lid with the louvres cast through it. The
# sails keep the old fastback line, so the side silhouette and the hitbox do not move.
# r3 (reviewer fix 3, rule 13): the bay floor drops 1.6 so the rear window can be ~1.7x taller and fill the wall
# (24 x 5.7 uu, was 22.8 x 3.3) - no frame round it that reads as a scoop bezel. The walls keep their r2 positions at
# the deck (XW0 / XR0 / TR_Y re-referenced to the new floor height).
TR_Z = 19.3                                      # bay floor (r2: 20.9)
TR_Y, TR_DRAFT = 13.91, 0.18                     # bay half width at the floor, side-wall draft (uu per uu up)
XW0, XW_K = -19.88, 0.55                         # window wall: x = XW0 + XW_K (z - TR_Z) (leans forward ~61 deg)
XR0, XR_K = -42.46, 0.9                          # bay rear wall: x = XR0 - XR_K (z - TR_Z) (leans back)
TR_LIP = 0.9                                     # rounded cast lip all round the bay
RWIN_Y, RWIN_Z0, RWIN_Z1, RWIN_R = 12.0, 20.6, 26.3, 1.6     # rear window opening in the wall (|y|, z range, corner)
LID_X0, LID_X1, LID_Y, LID_TOP = -40.0, -21.6, 10.8, 20.7   # raised engine lid in the bay


def x_wall(z):
    return XW0 + XW_K * (z - TR_Z)


def tray_vol(x, ay, z):
    """the air volume of the engine bay (negative inside): subtracted from the shell with a rounded lip"""
    d_side = (ay - (TR_Y + TR_DRAFT * (z - TR_Z))) / math.sqrt(1.0 + TR_DRAFT ** 2)
    d_front = (x - x_wall(z)) / math.sqrt(1.0 + XW_K ** 2)
    d_rear = ((XR0 - XR_K * (z - TR_Z)) - x) / math.sqrt(1.0 + XR_K ** 2)
    plan = i_round(i_round(d_side, d_front, 2.0), d_rear, 2.0)
    return i_round(plan, TR_Z - z, 1.1)


def engine_lid(x, ay, z):
    cx = 0.5 * (LID_X0 + LID_X1)
    return sd_rbox(x, ay, z, (cx, 0.0, TR_Z), (0.5 * (LID_X1 - LID_X0), LID_Y, LID_TOP - TR_Z), 0.9)


def tray_mask(x, ay, z):
    return (x > -50.0) & (x < -10.0) & (ay < 19.5) & (z > TR_Z - 2.4)


RF_CAB = (1.8, 3.0)                  # cab-to-haunch fillet radius: ahead / at the C-pillar foot
RF_RAMP_F, RF_RAMP_R = (-3.0, -12.0), (-28.0, -18.0)
RF_MODE, RF_RAMP_Y = "y", (23.5, 27.0)


def shape_outer(x, ay, z):
    """the cast outer shape (hull + cab + engine bay + lid); shared by the body and the window moulding"""
    # r3: the cab-to-haunch fillet widens from 1.8 to 3.0 at the C-pillar foot (x -8..-22): there the haunch rises into
    # the steep cab side and the 1.8 fillet was a narrow V valley that rendered as a dark wedge under the side window's
    # rear corner (reviewer round 2, "black wedge at the C-pillar"); a broad cast fillet catches the light instead
    # r5b (gate fix 2, the dark 'dash marks' on the haunch in corner_R): traced by ray-casting the dash pixels - they sit
    # on the haunch top (x -7..-3.4 and -18..-16) and their reflections land on the window's dark top lip; present in a
    # raw undecimated render too (field, not mesh). The fillet radius was switched 1.8 -> 3.0 ALONG x (C1 smoothsteps
    # ending at x -6 / -19): a fillet whose radius changes along its length twists, and the twist pinched that
    # reflection into short dashes (C2 ramps over 9-10 uu still left a faint one; a constant radius left none).
    # RF_MODE 'y': the radius now depends on |y| only - 1.8 across the windscreen base (|y| < 23.5, front unchanged),
    # a constant 3.0 along every side fillet (cab / C-pillar / sail to haunch)
    if RF_MODE == "y":
        rf = RF_CAB[0] + (RF_CAB[1] - RF_CAB[0]) * smoother(*RF_RAMP_Y, ay)
    else:
        rf = RF_CAB[0] + (RF_CAB[1] - RF_CAB[0]) * smoother(*RF_RAMP_F, x) * smoother(*RF_RAMP_R, x)
    o = u_round(hull(x, ay, z), cabin(x, ay, z), rf)
    m = tray_mask(x, ay, z)
    if np.any(m):
        o = o.copy()
        om = s_round(o[m], tray_vol(x[m], ay[m], z[m]), TR_LIP)
        o[m] = u_round(om, engine_lid(x[m], ay[m], z[m]), 0.35)
    return o


def body_outer(x, ay, z):
    o = shape_outer(x, ay, z)
    m = (x > 14) & (x < 21.5) & (ay > 26.5) & (ay < 32.5) & (z > 21.0) & (z < 26.5)
    if np.any(m):
        o = o.copy()
        o[m] = u_round(o[m], nubs(x[m], ay[m], z[m]), 0.55)
    return o


def arches(x, ay, z):
    # r5 (spike/notch gate): the arch roof meets the inner well wall in a 0.8 fillet (was a hard 90 deg corner whose
    # crease dead-ended at the arch ends and at the axle channels)
    dF = i_round(np.hypot(x - X_FA, z - ARZ) - AR, WELL - ay, 0.8)
    dR = i_round(np.hypot(x - X_RA, z - ARZ) - AR, well_y(x) - ay, 0.8)
    return np.minimum(dF, dR)


def axle_channels(x, ay, z):
    """slots in the body underside so the steel axles sit in the open, visible from below"""
    # r5 (spike/notch gate): every channel edge rounded 0.5 (were hard box corners at the well wall)
    dF = i_round(np.abs(x - X_FA) - 1.5, z - (AXLE_Z + 1.3), 0.5)
    dR = i_round(np.abs(x - X_RA) - 1.5, z - (AXLE_Z + 1.3), 0.5)
    return i_round(np.minimum(dF, dR), ay - WELL - 0.5, 0.5)


def cavity(x, ay, z, outer):
    # r5 (spike/notch gate, seen through the side windows): the cab cavity's bounding planes meet in 0.6 rounds (its hard
    # floor / side / end corners left a torn crease at (23, 28.6, 9.7))
    box = i_round(i_round(9.6 - z, ay - 28.6, 0.6), np.maximum(x - 23.0, -24.0 - x), 0.6)
    return i_round(outer + SHELL, box, 0.6)


# ---- side scoop (ahead of the rear wheel) ----------------------------------------
# r4 (reviewer round-3 fix 1, the owner's "black bad faces"): the shipped body is collapsed to ~0.4 uu edges in this
# area (measured on the r3 export), so every radius here must be well above that or the facets read as zig-zag
# highlights / sawtooth edges. The scoop is rebuilt as a clean cast shape:
#   * outline = an EXACT rounded quad (sd_rpoly, r 1.8): the old 3-4 segment polyline corners put kinks into the
#     recess wall that read as the sawtooth boundary
#   * lip round 1.0 (was 0.75), floor-to-wall round 0.9 (was 0.4)
#   * three thick fins with FULL bullnose crests (half thickness = crest radius = 0.55, was a 0.84 slab with 0.3
#     lips) and 0.6 smooth-min root fillets (was 0.28), crest 0.65 under the skin
SCOOP_Q = [(-5.6, 21.2), (-9.4, 12.9), (-19.6, 12.9), (-19.4, 21.7)]      # convex (x, z) quad, corners rounded
SCOOP_QR = 1.8
SCOOP_LIP, SCOOP_FLOOR_R = 1.0, 0.9
SCOOP_FINS = (15.2, 17.6, 19.9)
FIN_HT, FIN_ROOT, FIN_TOP = 0.55, 0.6, 0.65
FIN_X0 = -11.0                # r5: fin noses (x); the scoop floor is ~1.5 deep there


def scoop_sd(x, z):
    return sd_rpoly(x, z, SCOOP_Q, SCOOP_QR)


def scoop_fields(x, ay, z):
    side = W_(x) - tuck(z)
    depth = 0.6 + 2.7 * smoothstep(-6.5, -17.0, x)
    sd = scoop_sd(x, z)
    region = i_round(sd, (side - depth) - ay, SCOOP_FLOOR_R)
    fins = np.full(x.shape, 50.0)
    for zf in SCOOP_FINS:
        fins = np.minimum(fins, np.abs(z - zf) - FIN_HT)
    fins = i_round(fins, ay - (side - FIN_TOP), FIN_HT)            # full bullnose crest
    # r5 (reviewer round-4 fix 6, the hooked / melted leading edge): the fins used to rise out of the shallow front of
    # the ramp floor right at the slanted leading wall, so each fin tip broke the wall into a hook. They now start
    # FIN_X0 behind the front, as three clean rounded noses standing ~0.8 proud of a floor that is already 1.5 deep;
    # the leading part of the scoop is one smooth ramp, its outline one convex rounded curve
    fins = i_round(fins, x - FIN_X0, FIN_HT)
    # the fins run 0.9 into the walls and the floor and fuse with them through the root fillet
    fins = np.maximum(fins, sd - 0.9)
    fins = np.maximum(fins, (side - depth - 0.9) - ay)
    return region, fins


# ---- window openings ---------------------------------------------------------
WS_POLY = [(21.0, -22.2), (21.0, 22.2), (9.4, 20.0), (9.4, -20.0)]
# r3 (reviewer fix 1, the owner's "black bad faces"): the side-window opening was a 3-segment polyline round
# (round_corners nseg 3): every corner was a fan of 30-deg kinks, which the slanted cab side stretched into the torn,
# scalloped C-pillar cut-out seen from behind. It is now an exact rounded quad (sd_rpoly: true circular corners).
# The top edge now follows the roof line down toward the C-pillar (0.75-0.9 uu under the roof-edge line Ze(x) all
# along: the r2 top-rear corner at (-10.6, 27.9) sat ABOVE Ze and bit into the roof's corner round) and the rear-lower
# corner moves up/forward off the haunch fillet. Front half unchanged. Convex, so sd_rpoly gives exact rounds.
# r4 (reviewer round-3 fix 3): the rear-lower corner moves up 1.5 (-14.0, 24.4 -> 25.9). Measured (sill_scan): at the
# old corner the C-pillar fillet bulges 0.7-1.2 uu outboard of the cab-side plane, more than the capped cut clears, so
# the cut ended in a hooked lip with a dark pocket under it. Along the new sill the fillet is <= 0.2 uu proud (and the
# cap reaches a little further at the rear, win_side), so the opening passes cleanly through the cab wall all round.
# Front half unchanged.
SW_QUAD = [(15.4, 23.6), (9.0, 27.9), (-2.0, 27.75), (-10.0, 26.9), (-14.0, 25.9)]
SIDE_CUT_CAP_REAR = 0.9       # r4: the cap grows by this toward the rear-lower corner (x -9 -> -14), see win_side()
SW_R = 1.45
SIDE_CUT_CAP = 1.6            # the cut stops 1.6 uu outboard of the cab-side plane (never notches the haunch)
SIDE_LIP = 0.8                # r4: lip round of the side openings
# r5 (reviewer round-4 fix 1): the side-window outline in (x, z measured ON the cab-side plane), one convex polygon whose
# corners are rounded EXACTLY by SW5_R (rpoly_sd: the inner polygon is clipped half-plane by half-plane, so no edge can
# invert the way SW_QUAD did). Front end (A-pillar) where r4's visible edge was; the top line drops 0.3-0.9 at the rear
# half so the opening's top lip sits on the shoulder of the roof round instead of on its nearly flat top; rear end at
# x -11.9 on the C-pillar flat; the sill one straight line.
SW5_POLY = [(11.35, 24.05), (11.35, 26.35), (9.0, 28.0), (0.0, 27.65), (-7.5, 27.05), (-12.15, 25.75), (-12.15, 24.95), (-11.0, 24.3)]
SW5_R = 1.1
CAB_NZ = 1.0 / math.sqrt(1.0 + KS * KS)     # z component of the cab-side normal (0.54): the cut runs along it
CUT_IN = 3.9                  # how far the cut reaches inward (uu along the normal): through the 2 uu skin into the air


def rpoly_inner(poly, r):
    """inner polygon of a convex polygon offset inward by r, clipped half-plane by half-plane (edges that vanish under
    the offset simply drop out, instead of inverting like offset_convex's line intersections)"""
    P = np.asarray(poly, float)
    if 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]) < 0:
        P = P[::-1].copy()
    lo, hi = P.min(0) - 10.0, P.max(0) + 10.0
    Q = [np.array([lo[0], lo[1]]), np.array([hi[0], lo[1]]), np.array([hi[0], hi[1]]), np.array([lo[0], hi[1]])]
    n = len(P)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        e = (b - a) / np.linalg.norm(b - a)
        nin = np.array([-e[1], e[0]])                      # inward normal (CCW polygon)
        c0 = float(nin @ a) + r                            # keep points with nin.p >= c0
        out = []
        for k in range(len(Q)):
            p, q = Q[k], Q[(k + 1) % len(Q)]
            fp, fq = float(nin @ p) - c0, float(nin @ q) - c0
            if fp >= 0:
                out.append(p)
            if (fp >= 0) != (fq >= 0):
                out.append(p + (q - p) * (fp / (fp - fq)))
        Q = out
    return np.array(Q)


_SW5_IN = None


def win_outline(x, zf):
    global _SW5_IN
    if _SW5_IN is None:
        _SW5_IN = rpoly_inner(SW5_POLY, SW5_R)
    return W.sd_poly(x, zf, _SW5_IN) - SW5_R


def win_ws(x, y, z):
    return np.maximum(sd_rpoly(x, y, WS_POLY, 2.6), np.maximum(20.0 - z, 5.5 - x))


def cab_side_d(x, ay, z):
    """signed distance (+ outboard) to the cab-side surface of cabin(): ay = yr(x) + (Pc(x) - CR - z) / KS, a ruled
    surface (straight in section, single-curved in plan), normalised by its full gradient"""
    yr = YR_(x); dyr = YR_.d(x); pc = PC_(x); dpc = PC_.d(x)
    s = ay - yr - (pc - CR - z) / KS
    gx = dyr + dpc / KS
    return s / np.sqrt(1.0 + gx * gx + 1.0 / (KS * KS))


def win_side(x, ay, z):
    """r5 (reviewer round-4 fix 1, the right C-pillar 'black spike shard'): the side-window cut is a prism pushed through
    the cab side ALONG ITS NORMAL (not along y any more), outline = one exact, closed, convex rounded curve (win_outline).
    Measured on r4 (sections x -10 / -4 / +4): the old cut ran horizontally (along y) and its top edge sat 0.9-1.6 uu up
    in the 1.9 roof round, where the roof skin is nearly horizontal: the horizontal cut met it at ~25 deg and left a thin
    roof TONGUE 0.3 uu thick overhanging the glass, whose tip the 0.17 grid tore into the shard / stepped lip. The r4
    outline itself was broken too: SW_QUAD with r 1.45 collapsed under the inward offset (dent in the sill, bump in the
    top line). Cutting along the cab-side normal, every lip meets the surface at >= 60 deg (90 deg on the flat side) and
    the walls pass through the 2 uu skin into the cab air, where the cut ends (CUT_IN, never inside zamac).
    r3/r4 kept: the cut is CAPPED outboard of the cab-side plane (never notches the haunch), deeper cap at the rear-lower
    corner where the C-pillar fillet stands proud."""
    d = cab_side_d(x, ay, z)
    c = win_outline(x, z - d * CAB_NZ)
    c = i_round(c, -CUT_IN - d, 0.6)                         # inner end, in the cab air
    cap = SIDE_CUT_CAP + SIDE_CUT_CAP_REAR * smoothstep(-8.0, -12.0, x)
    return i_round(c, d - cap, 1.2)     # a broad round: no hooked lip at the sill ends


def win_rear(x, y, z):
    """r2: the rear window is an opening in the steep bay front wall (not a slot in the fastback any more)"""
    zc, hh = 0.5 * (RWIN_Z0 + RWIN_Z1), 0.5 * (RWIN_Z1 - RWIN_Z0)
    d_wall = (x - x_wall(z)) / math.sqrt(1.0 + XW_K ** 2)
    # only the wall itself: 0.9 into the bay air (enough for the cut), 2.6 into the cab - never the engine lid
    return np.maximum(sd_rrect2(y, z - zc, RWIN_Y, hh, RWIN_R), np.maximum(-0.9 - d_wall, d_wall - 2.6))


# ---- grooves (panel lines, lids, louvres) ------------------------------------
GROOVE_HW, GROOVE_D = 0.30, 0.5
if Q:
    GROOVE_HW = 0.34                 # keep panel lines resolvable on the coarse look-dev grid
BONNET_POLY = [(27.0, -13.4), (52.4, -10.2), (52.4, 10.2), (27.0, 13.4)]
LID_C, LID_H = (46.6, 22.0), (5.2, 3.3)
LV_X0, LV_N, LV_P, LV_HW, LV_Y = -23.8, 7, 2.4, 0.6, 8.4      # r2: louvres cast through the engine lid (r3 pitch 2.4)


def bonnet_sd(x, ay):
    return sd_rpoly(x, ay, BONNET_POLY, 2.4)


def groove_band(x, ay, z):
    """signed distance to the panel-line bands (negative inside a groove), before depth limiting.
    r4: the door lines are no longer here - see door_lines()"""
    g = np.full(x.shape, 50.0)
    # bonnet lid (= the Mood Paint panel) and the two closed pop-up lamp lids
    m = (x > 24) & (x < 57) & (z > 10)
    if np.any(m):
        d = np.abs(bonnet_sd(x[m], ay[m])) - GROOVE_HW
        lid = np.abs(sd_rrect2(x[m] - LID_C[0], ay[m] - LID_C[1], LID_H[0], LID_H[1], 1.4)) - GROOVE_HW
        g[m] = np.minimum(g[m], np.minimum(d, lid))
    # (r2: no engine-cover outline groove any more - the lid is a real raised casting in the recessed bay)
    return g


# r4 (reviewer round-3 fix 2): the two DOOR LINES are one constant swept profile pressed into the surface - a smooth
# (1 - u^2)^3 valley, u = distance to the line / DOOR_GW - instead of a 0.6 wide box slot with 0.2 / 0.3 rounds. The
# slot's walls were steeper than the ~0.4 uu facets of the shipped mesh, so they came out as wobbling, torn dark lines
# (and dark wavy cracks on the sails from the chase camera). The valley is 0.45 deep, its lips ~0.9 radius, its floor
# ~0.33, it reads ~1.2 uu wide, it is the same width everywhere it runs (side, shoulder) and it tapers out softly at
# both ends (below the rocker step, just over the shoulder crest). Paint pools along its floor (Col.G, pooling_mask).
DOOR_LINES = ((21.2, 0.10), (-3.0, 0.05))        # x at z 12, lean (x per z)
# r5 (reviewer round-4 fix 4): wider + shallower valley (half width 1.15, depth 0.40: floor radius ~0.55, was ~0.33 -
# below the ~0.43 uu facets, hence the lumpy, varying width), so it reads an even ~1.1 uu wide everywhere
DOOR_GW, DOOR_GD = 1.15, 0.40
DOOR_Z_END = (12.35, 14.3, 18.7, 20.7)            # (r5 tapers, unused since r5b)
DOOR_CAPS = (13.75, 19.7)                        # cap centres z (groove spans z 12.6 .. 20.85)
# owner notes 17 Oct (V5): r5b's lower cap centre 13.15 put the groove's round, up-facing end (z 12.0-13.2) across the
# printed sill band - through the pink pinstripe (12.1-12.5) and the lime's lower edge - so the band was holed by a
# sun-lit body-colour chip. Both lines now end at z 12.6, the lime band's lower edge: the pinstripe runs on unbroken
# below them, the lime / white band and the logo are parted by the grooves (door_print_break)


def door_profile(x, ay, z):
    """0..1 groove profile of the two door lines (1 = floor centre), with the end tapers.
    r5 (reviewer round-4 fix 4): both ends now taper out ON THE FLAT SIDE: the bottom run-out sits wholly above the
    rocker step (r4 faded across the 0.75 step = the bulb at the rocker), the top run-out ends at z 20.7, ~2 uu below
    the shoulder crest and 3 uu below the mirror nub (r4 ran onto the crest, where from the chase camera the line read
    as a bright wire running into the nub). A side-only guard (|y| > 34) keeps it off the shoulder top."""
    # the run-outs are self-similar: depth ~ w and width ~ sqrt(w), so the floor radius stays ~0.55 all the way to a
    # pointed end (a depth-only fade left a round spoon / 'bulb' at each end)
    # r5b (gate fix 3): the r5 run-outs (2 uu each, width ~ sqrt) made each line a lens. Now every line is ONE constant
    # section swept along a straight segment between two cap centres (DOOR_CAPS): u = distance to the SEGMENT, so the
    # groove keeps its full width and depth to the end and closes in a round cap of radius DOOR_GW (1.15 uu long) on the
    # flat side - bottom cap clear of the rocker step, top cap below the shoulder roll. Same section front and rear.
    z0, z1 = DOOR_CAPS
    w = smoothstep(34.0, 35.5, ay)
    p = np.zeros(x.shape)
    for xl, k in DOOR_LINES:
        ux, uz = -k / math.sqrt(1.0 + k * k), 1.0 / math.sqrt(1.0 + k * k)
        px, pz = xl - k * (z0 - 12.0), z0
        L = (z1 - z0) * math.sqrt(1.0 + k * k)
        t = np.clip((x - px) * ux + (z - pz) * uz, 0.0, L)
        s2 = (x - (px + t * ux)) ** 2 + (z - (pz + t * uz)) ** 2
        u2 = np.minimum(s2 / (DOOR_GW * DOOR_GW), 1.0)
        p = np.maximum(p, (1.0 - u2) ** 3)
    return p * w


def door_lines(x, ay, z, outer):
    """inward displacement (uu) added to the body SDF; limited to the outer skin (the cavity wall behind stays put)"""
    return DOOR_GD * door_profile(x, ay, z) * smoothstep(-1.4, -0.8, outer)


def door_mask(x, ay, z):
    return (ay > 23.0) & (x > -6.5) & (x < 24.5) & (z > 9.6) & (z < 25.8)


GROOVE_FLOOR_R, GROOVE_LIP = 0.28, 0.42      # r5 (spike/notch gate, lamp-lid / bonnet corners on the steep nose): 0.2 / 0.3


def grooves(x, ay, z, outer):
    # r2: the groove floor meets its walls in a 0.2 uu round (paint-filled cast groove, rule 2) instead of a sharp
    # corner: where a groove crosses a steep or doubly curved surface (lamp-lid corners at the nose, bonnet corners
    # at the windscreen) the sharp floor corner pinched into slivers thinner than the export grid
    return i_round(groove_band(x, ay, z), -(outer + GROOVE_D), GROOVE_FLOOR_R)


def louvre_band(x, ay):
    k = np.clip(np.round((LV_X0 - x) / LV_P), 0, LV_N - 1)
    xi = LV_X0 - LV_P * k
    return sd_rrect2(x - xi, ay, LV_HW, LV_Y, 0.55)


def pooling_mask(V):
    """0..1 per vertex: paint pooled in panel lines and louvre slots (Col.G)"""
    x, ay, z = V[:, 0], np.abs(V[:, 1]), V[:, 2]
    d = np.minimum(groove_band(x, ay, z), np.where((x > -43) & (x < -21) & (z > TR_Z - 1.5), louvre_band(x, ay), 50.0))
    # r4: the door lines pool along their soft valley floor (a smooth band, no crumbly edge)
    door = np.where(door_mask(x, ay, z), smoothstep(0.35, 0.9, door_profile(x, ay, z)), 0.0)
    return np.maximum(smoothstep(0.32, -0.12, d), door)


def louvres(x, ay, z, outer):
    # r5 (spike/notch gate): rounded slot floor (was a hard floor whose corners notched at the slot ends)
    return i_round(louvre_band(x, ay), -(outer + 1.0), 0.4)


# ---- front lamp recesses (the tail's lamp band / plate are soft dishes in x_tail, see tail_relief) -------
FL_C, FL_H = (19.4, 8.85), (4.6, 0.72)           # front parking lamps (ay, z)


def recesses(x, ay, z):
    xf = x_front(ay, z)
    # r2: 0.2 round in the recess floor corner (its sharp end corner on the curved nose pinched on the export grid)
    # r5 (spike/notch gate, the recess bottom edge where the nose tucks under): floor round 0.35 (was 0.2)
    return i_round(sd_rrect2(ay - FL_C[0], z - FL_C[1], FL_H[0], FL_H[1], 0.6), (xf - 0.7) - x, 0.35)


def body_sdf(x, y, z):
    ay = np.abs(y)
    outer = body_outer(x, ay, z)
    B = outer.copy()
    B = s_round(B, arches(x, ay, z), ARCH_ROUND)
    B = s_round(B, axle_channels(x, ay, z), 0.5)
    sm = (x < -3.5) & (x > -23) & (ay > 30) & (z < 23) & (z > 11)
    if np.any(sm):
        reg, fins = scoop_fields(x[sm], ay[sm], z[sm])
        b = s_round(B[sm], reg, SCOOP_LIP)
        B[sm] = u_round(b, fins, FIN_ROOT)
    cm = (x > -26) & (x < 25) & (ay < 30) & (z > 8.5)
    if np.any(cm):
        B[cm] = s_round(B[cm], cavity(x[cm], ay[cm], z[cm], outer[cm]), 0.4)
    wm = (x > -24) & (x < 25) & (z > 18) & (ay < 31)
    if np.any(wm):
        wd = np.minimum(win_ws(x[wm], y[wm], z[wm]), win_rear(x[wm], y[wm], z[wm]))
        B[wm] = s_round(B[wm], wd, 0.5)
        # r4: the side openings get a 0.8 lip (was 0.5, finer than the shipped facets: a wobbling highlight on the sill)
        B[wm] = s_round(B[wm], win_side(x[wm], ay[wm], z[wm]), SIDE_LIP)
    lm = (x > -43) & (x < -21) & (ay < 11) & (z > TR_Z - 1.5)
    if np.any(lm):
        B[lm] = s_round(B[lm], louvres(x[lm], ay[lm], z[lm], outer[lm]), 0.35)
    rm = x > 55
    if np.any(rm):
        B[rm] = s_round(B[rm], recesses(x[rm], ay[rm], z[rm]), 0.5)      # r5: lip 0.5 (was 0.3)
    gm = (x > 24) & (x < 57) & (z > 10)
    if np.any(gm):
        B[gm] = s_round(B[gm], grooves(x[gm], ay[gm], z[gm], outer[gm]), GROOVE_LIP)
    dm = door_mask(x, ay, z)
    if np.any(dm):
        B[dm] = B[dm] + door_lines(x[dm], ay[dm], z[dm], outer[dm])
    return B


# =============================================================================
#  Body detail parts (separate SDFs so their materials get clean borders)
# =============================================================================
def lens_front(x, y, z):
    ay = np.abs(y); xf = x_front(ay, z)
    # r2: 0.25 round on the lens plate edges (a sharp plate end gave a non-manifold edge on the 0.06 grid)
    # r4: the plate's back face sits 0.06 IN FRONT of the recess floor (xf - 0.64; was xf - 0.78, 0.08 behind it). The two
    # shells used to intersect along the floor, and the r4 export put a lens vertex within 1e-4 m of a body vertex there
    # (near-duplicate gate fail at 58.9, 15.6, 8.3). The visible front face moves 0.02 uu (xf - 0.20, was - 0.22).
    return i_round(sd_rrect2(ay - FL_C[0], z - FL_C[1], FL_H[0] - 0.12, FL_H[1] - 0.1, 0.5),
                   np.abs(x - (xf - 0.42)) - 0.22, 0.2)


def exhaust_tip_x():
    return float(x_tail(0.0, Z_BOT_REAR)) - 1.5


def exhaust_sdf(x, y, z):
    """r4: two separate round cast pipe tips (y = +-1.6), each with a bore, poking ~1.5 uu out from under the bumper"""
    tip = exhaust_tip_x()
    r = np.hypot(np.abs(y) - EX_BORE_Y, z - EX_Z)
    # r5 (spike/notch gate): the inner end (inside the base's exhaust channel, seen from below) is a full round cap
    tube = np.maximum(i_round(r - EX_R, tip - x, 0.24), i_round(r - EX_R, x - (tip + 5.0), 0.75))
    # r5: the bore is drilled 1.4 deep from the VISIBLE end with a rounded bottom (r4's half-space ran the other way:
    # it bored the hidden inner end open - a 0.14-lipped hole the spike/notch gate flagged - and left the tip closed)
    bore = i_round(r - EX_BORE_R, x - (tip + 1.4), 0.3)
    return s_round(tube, bore, 0.2)


def rivet_sdf(x, y, z, xr):
    # r5 (spike/notch gate): a revolved rounded puck (exact SDF, 0.6 edge radius) with a broad, shallow peen dimple;
    # the r4 head was an (inexact) ellipsoid cut flat at its equator with a 0.12-rounded pin-prick dimple. Same
    # footprint (r 2.0) and drop below the base (0.76)
    zc = BASE_Z0 - 0.33
    head = sd_rrect2(np.hypot(x - xr, y), z - zc, 2.0, 0.43, 0.6)
    dimple = np.sqrt((x - xr) ** 2 + y * y + (z - (zc - 0.43 - 1.35)) ** 2) - 1.6
    return s_round(head, dimple, 0.4)


def axle_head_sdf(x, y, z, xa, side):
    """peened mushroom head on the axle end, sitting in the hub's centre hole"""
    yc = side * (WY + W.HUB_FACE_Y)
    # r2: a whole ellipsoid (its inner half sits in the hub boss) - the old flat 0.05 uu base flange was thinner than
    # the grid and lay on the tube's end cap (zero-area specks, 3+-face edges); the tube now ends inside the head
    head = sd_ellipsoid(x, y, z, (xa, yc, AXLE_Z), (1.2, 0.6, 1.2))
    # sd_ellipsoid returns 0 at its exact centre (a lattice point -> a one-point void speck): an inner ball keeps the
    # core negative without touching the surface
    head = np.minimum(head, np.sqrt((x - xa) ** 2 + (y - yc) ** 2 + (z - AXLE_Z) ** 2) - 0.5)
    # r2: a wider, softer peen dimple (the old 0.62 ball grazed the dome top and left a knife-edge rim)
    dimple = np.sqrt((x - xa) ** 2 + (y - (yc + side * 1.3)) ** 2 + (z - AXLE_Z) ** 2) - 0.95
    return s_round(head, dimple, 0.22)


# =============================================================================
#  BASE (chassis): black plastic, the band below the sill, chin, diffuser, underside detail
# =============================================================================
def base_sdf(x, y, z):
    ay = np.abs(y)
    dW = W_.d(x)
    d_side = (ay - (W_(x) - 2.2)) / np.sqrt(1.0 + dW * dW)
    d_front = x - (X_NOSE - 0.0034 * ay * ay - 1.25)
    # rear: the base stops 1.8 uu inside the painted tail and only shows as a thin dark lip under the bumper
    # (rule 11); in front of the rear arches it is unchanged
    d_rear = (X_TAIL + BASE_TAIL_IN + 0.0018 * ay * ay) - x
    plan = i_round(i_round(d_side, d_front, 4.2), d_rear, 3.2)
    # behind the rear wheels the base narrows inside the wheel inner faces (|y| 31.4), so from behind the black
    # tyres and their inner faces show under the painted quarters instead of a full-width black slab (rule 14)
    # r2: the narrowing happens INSIDE the rear wheel notch (x -45.7..-22.3, where |y| > 29 is cut anyway), so no
    # knife step is left where the notch's rear wall used to meet the narrowing (x -45.7, |y| 35.5-35.9)
    plan = i_round(plan, ay - (BASE_REAR_HALF + 12.0 * smoothstep(-40.0, -28.0, x)), 1.6)
    slab = np.maximum(BASE_Z0 - z, z - BASE_TOP)
    B = i_round(plan, slab, 0.85)
    # moulded detail standing 0.5-0.7 proud of the underside
    det = np.full(x.shape, 50.0)
    for xr in RIVETS_X:                                                       # rivet bosses
        r = np.hypot(x - xr, y)
        det = np.minimum(det, np.maximum(np.maximum(r - 3.3, 2.0 - r), np.maximum((BASE_Z0 - 0.6) - z, z - (BASE_Z0 + 0.5))))
    tp = sd_rrect2(x - 2.0, y, 17.0, 11.5, 2.0)                               # text panel border
    det = np.minimum(det, np.maximum(np.abs(tp) - 0.45, np.maximum((BASE_Z0 - 0.5) - z, z - (BASE_Z0 + 0.5))))
    for yc in (19.5, -19.5):                                                  # stiffening ribs
        det = np.minimum(det, sd_rbox(x, y, z, (2.0, yc, BASE_Z0), (19.0, 0.55, 0.55), 0.4))
    for yc in (5.0, 15.5, 21.0):                                              # diffuser strakes (under the tail,
        det = np.minimum(det, sd_rbox(x, ay, z, (-49.5, yc, BASE_Z0 + 0.6), (3.2, 0.45, 1.0), 0.35))   # not past it)
    for xa in (X_FA, X_RA):                                                   # axle clips
        for yc in (9.0, 21.0):
            det = np.minimum(det, sd_rbox(x, ay, z, (xa, yc, BASE_Z0 - 0.1), (3.2, 1.6, 0.6), 0.5))
    rib = np.maximum(np.abs(np.mod(x + 30.0, 2.4) - 1.2) - 0.36, np.maximum(np.abs(x + 30.0) - 4.6, ay - 8.5))
    det = np.minimum(det, np.maximum(rib, np.maximum((BASE_Z0 - 0.45) - z, z - (BASE_Z0 + 0.5))))
    B = u_round(B, det, 0.3)
    # plain recessed decal area for "STREAKLINE . VORTEX . 1993 . MADE IN ..."
    B = s_round(B, np.maximum(sd_rrect2(x - 2.0, y, 16.3, 10.8, 1.5), z - (BASE_Z0 + 0.22)), 0.12)
    # chin intake slot with three dividers, across the front face of the base
    xf = X_NOSE - 0.0034 * ay * ay - 1.25
    # r5 (spike/notch gate): the slot's back wall and the divider roots are filleted (0.4 / 0.3) and the slot lip is
    # 0.35 (was hard corners + a 0.2 lip: the divider creases dead-ended on the 0.15 grid)
    slot = i_round(sd_rrect2(ay, z - 5.55, 15.0, 0.95, 0.6), (xf - 1.6) - x, 0.4)
    div = np.minimum(np.abs(ay - 5.0), np.abs(ay - 10.0)) - 0.45
    slot = i_round(slot, -div, 0.3)
    B = s_round(B, slot, 0.35)
    # wheel notches round the tyres, axle troughs, exhaust cut-outs, rivet holes
    for xa in (X_FA, X_RA):
        wl = WELL if xa > 0 else well_y(x)                                         # r5: deeper rear wells
        notch = i_round(np.abs(x - xa) - (AR - 0.4), (wl - 0.6) - ay, 0.6)     # r5: rounded inner corner
        B = s_round(B, notch, 1.0)
        trough = i_round(i_round(np.abs(x - xa) - 1.6, ay - (wl - 0.6), 0.5), z - (AXLE_Z + 0.2), 0.5)   # r5: rounded
        B = s_round(B, trough, 0.5)      # r5: lip 0.5 (was 0.35)
    # exhaust channel; r5 (spike/notch gate): its blind end rounded 0.6, lip 0.4 (were hard / 0.25)
    ex = i_round(sd_rrect2(y, z - EX_Z, EX_W + 0.25, EX_R + 0.25, EX_R + 0.2), x - (X_TAIL + 7.0), 0.6)
    B = s_round(B, ex, 0.4)
    for xr in RIVETS_X:
        # r5 (spike/notch gate): the rivet holes' rims are rounded 0.35 (were hard cylinder cuts)
        B = s_round(B, np.hypot(x - xr, y) - 2.0, 0.35)
    return B


# =============================================================================
#  INTERIOR (one-colour moulded tub: seats, dash, wheel, console, door cards, engine)
# =============================================================================
def rot_xz(x, z, cx, cz, ang):
    c, s = math.cos(ang), math.sin(ang)
    dx, dz = x - cx, z - cz
    return cx + c * dx + s * dz, cz - s * dx + c * dz


def seat(x, y, z, yc):
    cush = sd_rbox(x, y, z, (-3.4, yc, 12.0), (5.0, 4.7, 1.7), 1.3)
    xr, zr = rot_xz(x, z, -8.6, 12.6, math.radians(-17.0))
    back = sd_rbox(xr, y, zr, (-8.8, yc, 18.6), (1.6, 4.7, 6.4), 1.4)
    head = sd_rbox(xr, y, zr, (-8.9, yc, 25.3), (1.4, 2.9, 1.5), 1.2)
    bol = np.minimum(sd_capsule(xr, y, zr, (-8.0, yc - 4.2, 13.4), (-8.0, yc - 4.2, 21.6), 1.05),
                     sd_capsule(xr, y, zr, (-8.0, yc + 4.2, 13.4), (-8.0, yc + 4.2, 21.6), 1.05))
    cb = np.minimum(sd_capsule(x, y, z, (-7.2, yc - 4.2, 13.2), (1.2, yc - 4.2, 13.0), 1.0),
                    sd_capsule(x, y, z, (-7.2, yc + 4.2, 13.2), (1.2, yc + 4.2, 13.0), 1.0))
    # r5 (spike/notch gate): back and cushion bolsters fuse in a 0.6 fillet (was a hard union)
    s = u_round(u_round(u_round(cush, back, 0.9), u_round(bol, cb, 0.6), 0.6), head, 0.7)
    return s


def interior_sdf(x, y, z):
    ay = np.abs(y)
    # r5 (spike/notch gate on the tub, seen through the glass): every part now fuses with a fillet (the r4 tub was hard
    # unions - floor/door card/seat creases that dead-ended), floor slab corners 0.58 (were 0.4), lever 0.5 thick
    d = sd_rbox(x, y, z, (0.5, 0.0, 10.25), (21.5, 26.8, 0.7), 0.66)                      # tub floor
    d = u_round(d, sd_rbox(x, ay, z, (2.5, 26.0, 15.5), (16.5, 1.0, 5.6), 0.8), 0.6)       # door cards
    d = u_round(d, sd_rbox(x, ay, z, (0.0, 24.6, 17.6), (7.5, 1.2, 0.8), 0.6), 0.7)         # armrests
    d = u_round(d, seat(x, y, z, 10.6), 0.6)
    d = u_round(d, seat(x, y, z, -10.6), 0.6)
    con = sd_rbox(x, y, z, (3.0, 0.0, 12.4), (10.5, 2.8, 2.2), 1.0)
    lever = sd_capsule(x, y, z, (5.4, 0.0, 14.2), (4.6, 0.0, 16.6), 0.5)
    knob = np.sqrt((x - 4.6) ** 2 + y ** 2 + (z - 16.9) ** 2) - 0.85
    d = u_round(d, u_round(u_round(con, lever, 0.45), knob, 0.35), 0.6)
    dash = sd_rbox(x, y, z, (15.6, 0.0, 16.4), (3.6, 25.6, 4.8), 1.8)
    hood = sd_rbox(x, y, z, (13.4, 10.6, 21.6), (2.3, 4.6, 1.2), 0.9)                     # binnacle (LHD)
    d = u_round(d, u_round(dash, hood, 0.7), 0.7)
    # chunky steering wheel, cast in (left-hand drive, +Y)
    a = np.array([-0.906, 0.0, 0.423])
    cx, cy, cz = 10.2, 10.6, 19.8
    px, py, pz = x - cx, y - cy, z - cz
    h = px * a[0] + py * a[1] + pz * a[2]
    qx, qy, qz = px - h * a[0], py - h * a[1], pz - h * a[2]
    # r5 (spike/notch gate, 17 flags on the r4 wheel's thin spokes / rim): a SOLID cast toy wheel - a fat rim (0.85)
    # round a dished web 0.7 thick, hub boss, column; every join filleted. (r4: 0.62 rim + 0.42 spokes, hard unions)
    rq = np.sqrt(qx * qx + qy * qy + qz * qz)
    ring = np.sqrt((rq - 3.3) ** 2 + h * h) - 0.85
    web = i_round(np.abs(h + 0.25) - 0.35, rq - 3.3, 0.3)
    hub = i_round(rq - 1.3, np.abs(h - 0.1) - 0.6, 0.45)
    col = sd_capsule(x, y, z, (cx, cy, cz), (14.2, cy, 18.0), 0.7)
    sw = u_round(u_round(u_round(ring, web, 0.5), hub, 0.4), col, 0.45)
    d = u_round(d, sw, 0.7)         # r2: the hub corner kissed the binnacle corner (a pinch thinner than the grid): fuse
    # r3 (reviewer fix 3, rule 13): a cast rear BULKHEAD closes the cab behind the rear window - nothing bright (roof
    # liner, bonnet stripes seen through the windscreen) can show through the glass any more; what you see is the dark
    # one-colour tub: the bulkhead with two seat-back shells and headrests moulded into it
    d = u_round(d, bulkhead(x, y, z), 0.8)
    return d


BH_X, BH_T = -12.2, 1.3        # bulkhead rear face x (vertical), thickness


def bulkhead(x, y, z):
    """VERTICAL, so seen from the chase camera it mirrors the dark bay floor, not the bright sky (a wall leaning
    parallel to the window caught the sunset sky and read light grey even in black plastic)"""
    ay = np.abs(y)
    wall = np.abs(x - (BH_X + 0.5 * BH_T)) - 0.5 * BH_T
    sh = np.full(x.shape, 50.0)
    for yc in (10.6, -10.6):
        back = sd_rbox(x, y, z, (BH_X + 0.1, yc, 18.7), (0.85, 4.5, 5.6), 1.1)
        head = sd_rbox(x, y, z, (BH_X + 0.2, yc, 24.35), (0.75, 2.8, 1.25), 0.7)
        sh = np.minimum(sh, u_round(back, head, 0.5))
    b = u_round(wall, sh, 0.4)
    # bounded by the cab: the floor, inside the side glass (cab-side plane - 3.0), up into the roof skin (Pc - 1.3)
    # r4: + 4.4 (was 3.0) - clear of the deeper side-glass in-curve (no glass/bulkhead intersection)
    # r5 (spike/notch gate): the bounding planes meet in 0.6 rounds (were hard corners at the top / side)
    lim = i_round(i_round(9.6 - z, z - (PC_(x) - 1.3), 0.8), i_round(ay - 25.4, cab_side_d(x, ay, z) + 4.4, 0.8), 0.8)
    return i_round(b, lim, 0.8)


# =============================================================================
#  WINDOWS: one light-smoke moulding, 2.05 uu thick, inset 0.55 below the body surface
# =============================================================================
GLASS_FLANGE = 1.5            # how far the moulding runs on under the zamac past each opening edge (as before)
GLASS_FLANGE_REAR = 0.8       # r2 rear window: its header under the roof edge is short
# r4: extra in-curve at the side glass's rear-top, where the C-pillar leans in: the glass met the zamac there at a grazing
# angle and the two meshes' intersection line read as a torn edge at the opening's rear-top corner
GLASS_REAR_IN = 0.8           # (r4 in-curve: unused since r5b, see glass_side_sdf)
GLASS_INSET0, GLASS_LEAN, GLASS_Z0 = 0.55, 0.13, 24.05      # r5b: ruled lean of the side pane
GLASS_LEAN_NORM = math.sqrt((1.0 - GLASS_LEAN * CAB_NZ) ** 2 + GLASS_LEAN ** 2
                            + 2.0 * (1.0 - GLASS_LEAN * CAB_NZ) * GLASS_LEAN * CAB_NZ)
GLASS_TRIM = (0.15, 0.3)      # r5b: trim offset under the outer skin, round (was 0.3 / 0.7: active across the pane)


def glass_rear_region(x, y, z):
    """r2 rear window moulding: the wall opening + flange, cut at the bisector between the wall and the roof skin
    (a clean plane - the flange never wraps round the roof-edge lip)"""
    ay = np.abs(y)
    zc, hh = 0.5 * (RWIN_Z0 + RWIN_Z1), 0.5 * (RWIN_Z1 - RWIN_Z0)
    d_wall = (x - x_wall(z)) / math.sqrt(1.0 + XW_K ** 2)
    d_roof = (PC_(x) - CR * (ay / YR_(np.clip(x, -40.0, 26.0))) ** 2) - z
    # r5 (spike/notch gate): the flange outline meets the wall slab and the roof bisector in 0.5 rounds (were hard)
    r = i_round(sd_rrect2(y, z - zc, RWIN_Y, hh, RWIN_R) - GLASS_FLANGE_REAR,
                np.maximum(-0.9 - d_wall, d_wall - 2.7), 0.5)
    return i_round(r, 0.7 * (d_wall - d_roof), 0.5)


def glass_side_sdf(x, ay, z, o):
    """r3 (reviewer fix 1): the side glass is a FAIR slab parallel to the cab-side plane (straight in section, gently
    single-curved in plan), 2.05 thick, its outer face 0.55 in from the cab side. The r2 glass was an offset of the
    whole outer shape: across the window it followed the cab side -> shoulder fillet (an S-curve that also waved with
    the shoulder line), so its reflections broke up like a lumpy shell. Trimmed 0.3 under the zamac skin so the
    flange can never break the surface where the roof edge / C-pillar curve in."""
    d = cab_side_d(x, ay, z)
    # r5b (gate fix 4, zebra sawtooth on the side glass): the r3/r4 in-curves (0.9 + 0.7 + 0.8 uu smoothsteps in z and x)
    # bent the visible pane by ~20 deg with a ~2.3 uu radius right at the sill, and the 0.7 trim round against the
    # outer shape was active over the WHOLE pane (o + 0.3 > -0.7 everywhere at 0.55 inset), printing the haunch fillet
    # and roof round onto the glass. The 24 k glass part could only facet that: notched stripes. The pane is now a ruled
    # LEAN: inset = 0.55 + GLASS_LEAN * (zf - 24.05) (zf = height measured on the cab-side plane), i.e. flat in every
    # section, only the cab side's gentle plan curve remains. Measured clearance to the outer skin over the visible
    # opening (win_outline < -0.3): >= 0.50 uu everywhere (glassclr), so the trim (0.15 under the skin, round 0.3) only
    # acts within 0.3 uu of the opening edge at the A-pillar top corner, under the lip, and on the hidden flange
    tl = GLASS_LEAN
    F = (d * (1.0 - tl * CAB_NZ) + GLASS_INSET0 + tl * (z - GLASS_Z0)) / GLASS_LEAN_NORM
    slab = np.abs(F + 1.025) - 1.025
    # r5: the r5 outline, measured on the cab-side plane like the cut (win_side)
    reg = i_round(win_outline(x, z - d * CAB_NZ) - GLASS_FLANGE, (YR_(x) - 2.0) - ay - GLASS_FLANGE, 0.5)
    g = i_round(slab, reg, 0.9)
    return i_round(g, o + GLASS_TRIM[0], GLASS_TRIM[1])


def glass_sdf(x, y, z):
    ay = np.abs(y)
    o = shape_outer(x, ay, z)
    shell = np.abs(o + 1.575) - 1.025
    reg = np.minimum(win_ws(x, y, z) - GLASS_FLANGE, glass_rear_region(x, y, z))
    # r2: the flange cuts are rounded (0.9): they sit under the zamac, and a sharp cut corner where the moulding
    # turns under the bonnet/sill gave single non-manifold edges on the export grid
    g = i_round(shell, reg, 0.9)
    # r3: + the fair side glass (one moulding: the windscreen flange and the side slab fuse under the A-pillar)
    # (r5: the windscreen flange / side slab fillet 0.6, was 0.3 - a crease that broke up at the A-pillar top)
    return u_round(g, glass_side_sdf(x, ay, z, o), 0.8)


# =============================================================================
#  Mesh assembly
# =============================================================================
def mirror_part(V, T, N):
    V2 = V.copy(); V2[:, 1] *= -1
    T2 = T[:, ::-1].copy()
    if N.ndim == 3:
        N2 = N[:, ::-1, :].copy(); N2[..., 1] *= -1
    else:
        N2 = N.copy(); N2[:, 1] *= -1
    return V2, T2, N2


def both_sides(V, T, N):
    V2, T2, N2 = mirror_part(V, T, N)
    return np.concatenate([V, V2]), np.concatenate([T, T2 + len(V)]), np.concatenate([N, N2])


def axle_tube(xc, zc, r, hl, seg=16, step=1.2):
    """r2: one watertight steel axle along Y: rings every <= 1.2 uu (the old 74 uu long side quads were 260:1
    slivers) and both end caps fanned to a centre vertex that SHARE the rim vertices (the old caps were loose
    rings: holes + duplicate vertices). Returns V, T and per-corner normals (side radial, caps axial)."""
    n = int(math.ceil(2 * hl / step)) + 1
    ys = np.linspace(-hl, hl, n)
    a = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ring = np.stack([np.cos(a), np.zeros(seg), np.sin(a)], 1)
    V = np.concatenate([np.stack([xc + r * ring[:, 0], np.full(seg, yv), zc + r * ring[:, 2]], 1) for yv in ys]
                       + [[[xc, -hl, zc], [xc, hl, zc]]])
    c0, c1 = n * seg, n * seg + 1
    T, NC = [], []
    for i in range(n - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            p, q, r_, s_ = i * seg + k, i * seg + k2, (i + 1) * seg + k2, (i + 1) * seg + k
            T += [(p, s_, r_), (p, r_, q)]
            NC += [(ring[k], ring[k], ring[k2]), (ring[k], ring[k2], ring[k2])]
    ny0, ny1 = np.array([0.0, -1.0, 0.0]), np.array([0.0, 1.0, 0.0])
    for k in range(seg):
        k2 = (k + 1) % seg
        T += [(c0, k, k2), (c1, (n - 1) * seg + k2, (n - 1) * seg + k)]
        NC += [(ny0, ny0, ny0), (ny1, ny1, ny1)]
    T = np.array(T); NC = np.array(NC, float)
    P = V[T]
    fn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
    flip = (fn * NC.mean(1)).sum(1) < 0
    T[flip] = T[flip][:, ::-1]; NC[flip] = NC[flip][:, ::-1]
    return V, T, NC


# ---- r5b: local adaptive refinement after the export collapse ------------------------------------------------------------
# (gate fixes 4 + 5) The exporter collapses the body to 250 k and the windows to 24 k triangles; along the sail crest,
# the cab-side rounds above/below the side window and the door-line grooves that left ~0.45-0.7 uu facets whose normals
# turn 8-15 deg per edge: a sawtoothed shadow edge off the crest under a 6 deg sun, stepped zebra stripes on the cab band
# and the glass. Inside these zones every edge whose end normals differ by more than REFINE_DEG is split at its midpoint,
# the midpoint goes onto the exact SDF, and the triangles are re-cut conformingly (1->2 / 1->3 / 1->4: no T-junctions,
# no new boundary). A split is refused where a child would fall under 0.0135 uu^2 (the rule-16 degenerate limit is 0.01).
REFINE_DEG = 1.6
REFINE_MIN_CHILD_AREA = 0.0135         # uu^2: no refined child under this (rule-16 degenerate limit 0.01)
REFINE_ZONES = {
    # name: list of (x0, x1, |y|0, |y|1, z0, z1) boxes (uu)
    "Vortex_Body": [(-16.5, 14.5, 21.5, 36.5, 20.0, 30.5, 0.9),  # cab side band above / below the side window (fix 4)
                    (-14.0, 13.0, 27.8, 31.5, 22.4, 24.8, 0.45), # the sill band right under the window (zebra teeth)
                    (-24.0, 24.0, 33.0, 41.0, 10.3, 13.0, 1.2),  # door panel: rocker step transition
                    (-24.0, 24.0, 33.0, 41.0, 11.4, 14.2, 0.4),  # owner V4: door panel above the step (draft onset)
                    (-24.0, 24.0, 33.0, 39.5, 19.5, 23.8, 1.2),  # door panel: shoulder roll
                    (-44.0, -4.0, 17.0, 31.5, 22.0, 31.5),       # sail crest + C-pillar (fix 5)
                    (17.5, 23.8, 33.0, 40.5, 11.0, 22.0),        # front door line (fix 3)
                    (-6.6, -0.4, 33.0, 40.5, 11.0, 22.0)],       # rear door line (fix 3)
    "Vortex_Windows": [(-15.5, 14.0, 19.0, 32.5, 20.5, 31.0)],   # side glass + its flanges
}


def _zone_deg(P, boxes, default):
    """per point: the refinement threshold (deg) of the box it falls in (box tuples may carry a 7th value), else inf"""
    x, ay, z = P[:, 0], np.abs(P[:, 1]), P[:, 2]
    deg = np.full(len(P), np.inf)
    for bx in boxes:
        x0, x1, y0, y1, z0, z1 = bx[:6]
        m = (x >= x0) & (x <= x1) & (ay >= y0) & (ay <= y1) & (z >= z0) & (z <= z1)
        deg[m] = np.minimum(deg[m], bx[6] if len(bx) > 6 else default)
    return deg


def refine_local(V, T, fn, boxes, max_deg=None, rounds=3, name=""):
    """conforming adaptive midpoint refinement inside boxes (see REFINE_ZONES); returns V, T"""
    max_deg = REFINE_DEG if max_deg is None else max_deg
    V = np.asarray(V, float).copy(); T = np.asarray(T, np.int64).copy()
    n0 = len(T)
    for rnd in range(rounds):
        nV, nT = len(V), len(T)
        N = W._unit(W.sdf_grad(fn, V, eps=0.02))
        E = np.sort(np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]), 1)
        key = E[:, 0] * nV + E[:, 1]
        uk, inv = np.unique(key, return_inverse=True)
        ea, eb = uk // nV, uk % nV
        P = V[T]
        area = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
        eid = inv.reshape(3, nT).T                                    # edge k of tri t: (v_k, v_k+1)
        ang = np.degrees(np.arccos(np.clip((N[ea] * N[eb]).sum(1), -1.0, 1.0)))
        mid = 0.5 * (V[ea] + V[eb])
        split = ang > _zone_deg(mid, boxes, max_deg)
        # r5b: area guard per triangle - a 1-edge split halves the triangle, a 2- or 3-edge split leaves quarters; any
        # triangle whose smallest child would fall under REFINE_MIN_CHILD_AREA drops all its splits (iterated: dropping
        # one edge changes the neighbour's pattern)
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
        Vm = W.project(fn, mid[si], iters=3, maxstep=0.3)
        V = np.concatenate([V, Vm])
        ms = split[eid]                                               # (nT, 3)
        mv = newid[eid]
        cnt = ms.sum(1)
        out = [T[cnt == 0]]
        for r in range(3):                                            # rotate so the pattern is canonical
            Tr = np.roll(T, -r, axis=1); msr = np.roll(ms, -r, axis=1); mvr = np.roll(mv, -r, axis=1)
            a, b, c = Tr[:, 0], Tr[:, 1], Tr[:, 2]
            m01, m12, m20 = mvr[:, 0], mvr[:, 1], mvr[:, 2]
            s1 = (cnt == 1) & msr[:, 0]                               # only edge (a,b) split
            out += [np.stack([a[s1], m01[s1], c[s1]], 1), np.stack([m01[s1], b[s1], c[s1]], 1)]
            s2 = (cnt == 2) & msr[:, 0] & msr[:, 1]                   # edges (a,b) and (b,c) split
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
    log("refine %-16s %d -> %d tris (+%d)" % (name, n0, len(T), len(T) - n0))
    return V, T


def refine_part(name, fn, V, T):
    """lab / build hook: refine the named SDF part's zones (name as in REFINE_ZONES, or Body / Windows)"""
    key = name if name in REFINE_ZONES else "Vortex_" + name
    if key not in REFINE_ZONES:
        return V, T
    return refine_local(V, T, fn, REFINE_ZONES[key], name=key)


def refined_normals(fn, V, T, N_in):
    """normals for a refined part in the same form the mesher returned (per-corner if it gave per-corner)"""
    N = W._unit(W.sdf_grad(fn, V, eps=0.02))
    if np.ndim(N_in) == 3:
        NC, _ = W.corner_normals(fn, V, T, N, eps=0.02)
        return NC
    return N


AMBER = (1.0, 0.42, 0.02, 1.0)
CLEAR = (0.95, 0.94, 0.88, 1.0)
RED = (0.78, 0.015, 0.02, 1.0)


def _refined(fn, name, V, T, N):
    V2, T2 = refine_part(name, fn, V, T)
    if len(T2) == len(T):
        return V, T, N
    return V2, T2, refined_normals(fn, V2, T2, N)


def build_body(coll):
    c = 0.28 if Q else 0.17
    V, T, N = W.sdf_part("Vortex_Body", body_sdf, (-60.5, -41.5, 4.3), (63.0, 41.5, 31.0), c,
                         target_tris=70000, symmetric=True, normal_eps=0.02)
    V, T, N = _refined(body_sdf, "Body", V, T, N)        # r5b: local refinement (REFINE_ZONES)
    parts = []
    mood = ((bonnet_sd(V[:, 0], np.abs(V[:, 1])) < -GROOVE_HW - 0.05) & (V[:, 2] > 12.0)).astype(float)
    pool = pooling_mask(V)
    col = np.stack([mood, pool, np.zeros_like(mood), np.ones_like(mood)], 1)
    parts.append(dict(V=V, T=T, N=N, mat=0, col=col))
    cs = 0.1 if Q else 0.06
    tip = exhaust_tip_x()
    Ve, Te, Ne = W.sdf_part("Exhaust", exhaust_sdf, (tip - 0.6, -EX_W - 0.8, EX_Z - 1.6),
                            (tip + 5.6, EX_W + 0.8, EX_Z + 1.6), cs, 4000, symmetric=True)   # r5: 1200 (rolled rims need the facets)
    parts.append(dict(V=Ve, T=Te, N=Ne, mat=1))
    Vf, Tf, Nf = W.sdf_part("LensF", lens_front, (57.0, 13.5, 7.2), (61.5, 25.0, 10.5), cs, 900, symmetric=False)  # r5: 500
    Vf, Tf, Nf = both_sides(Vf, Tf, Nf)
    cf = np.where((np.abs(Vf[:, 1]) > 21.4)[:, None], [AMBER], [CLEAR])
    parts.append(dict(V=Vf, T=Tf, N=Nf, mat=2, col=cf))
    # (no separate rear lens parts any more: the tail lamps are TAMPO on the cast lamp-band dish, rule 12)
    for xa, hl in ((X_FA, WY + W.HUB_FACE_Y), (X_RA, WY + W.HUB_FACE_Y)):
        Va, Ta, Na = axle_tube(xa, AXLE_Z, AXLE_R, hl - 0.25)        # ends 0.25 inside each peened head
        parts.append(dict(V=Va, T=Ta, N=Na, mat=3))
        for side in (1.0, -1.0):
            yc = side * hl
            Vh, Th, Nh = W.sdf_part("AxleHead", lambda x, y, z, xa=xa, side=side: axle_head_sdf(x, y, z, xa, side),
                                    (xa - 1.6, min(yc, yc + side * 1.0) - 0.9, AXLE_Z - 1.6),
                                    (xa + 1.6, max(yc, yc + side * 1.0) + 0.9, AXLE_Z + 1.6), 0.05, 260,
                                    symmetric=False, normal_eps=0.01)
            parts.append(dict(V=Vh, T=Th, N=Nh, mat=3))
    for xr in RIVETS_X:
        Vv, Tv, Nv = W.sdf_part("Rivet", lambda x, y, z, xr=xr: rivet_sdf(x, y, z, xr),
                                (xr - 2.6, -2.6, BASE_Z0 - 1.4), (xr + 2.6, 2.6, BASE_Z0 + 0.6), 0.05, 600,  # r5: 360
                                symmetric=True)
        parts.append(dict(V=Vv, T=Tv, N=Nv, mat=3))
    return W.build_object("SM_Vortex_Body", parts, ["Paint", "Chrome", "Lamp", "Zamac"], coll)


def build_base(coll):
    c = 0.3 if Q else 0.15
    V, T, N = W.sdf_part("Vortex_Base", base_sdf, (-58.5, -39.0, 2.4), (61.0, 39.0, 10.5), c,
                         target_tris=13000, symmetric=True, planar_deg=0.0)
    return W.build_object("SM_Vortex_Base", [dict(V=V, T=T, N=N, mat=0)], ["Base"], coll)


def build_windows(coll):
    c = 0.26 if Q else 0.14
    V, T, N = W.sdf_part("Vortex_Windows", glass_sdf, (-25.0, -33.5, 16.0), (23.5, 33.5, 30.5), c,
                         target_tris=2900, symmetric=True, planar_deg=0.0)
    V, T, N = _refined(glass_sdf, "Windows", V, T, N)    # r5b: local refinement (REFINE_ZONES)
    m = rear_pane_mask(V)       # r5: Col.R = 1 on the rear pane (per-pane tint, see GLASS_TINT_REAR)
    col = np.stack([m, np.zeros_like(m), np.zeros_like(m), np.ones_like(m)], 1)
    return W.build_object("SM_Vortex_Windows", [dict(V=V, T=T, N=N, mat=0, col=col)], ["Glass"], coll)


def build_interior(coll):
    c = 0.3 if Q else 0.16
    V, T, N = W.sdf_part("Vortex_Interior", interior_sdf, (-22.5, -28.0, 9.0), (22.5, 28.0, 27.5), c,
                         target_tris=9000, symmetric=False)
    return W.build_object("SM_Vortex_Interior", [dict(V=V, T=T, N=N, mat=0)], ["Interior"], coll)


# =============================================================================
#  UVs  (UV0 = smart unwrap; UV1 = tampo layout, unchanged from v1 so the series texture
#  convention stays: left side U 0-0.5, right side U 0.5-1, top strip above)
# =============================================================================
UVX0, UVX1, UVY = 64.0, -64.0, 41.0
UV_S = 0.5 / 128.0
UV_T = 1.0 / 128.0
TOP_V0 = 0.30
FRONT_U0, REAR_U0, FR_V0 = 0.55, 0.05, 0.17


def tail_pad_faces(cen, nrm):
    """r4 (reviewer round-3 fix 4): faces of the tail pad area (lamp pods, plate panel, bumper) that face rearward at
    all go to the REAR chart. The lower wall of each pod dish tilts up (nz > 0.45) and its end walls tilt sideways, so
    the normal-only classification sent them to the top / side charts, which carry no ink there: a body-colour band
    and a crumbly line along the pod floor. Same chart and mapping as before - only these faces change chart."""
    x, ay, z = cen[:, 0], np.abs(cen[:, 1]), cen[:, 2]
    return (x < X_TAIL + 4.5) & (ay < 31.0) & (z > 11.0) & (z < 23.2) & (nrm[:, 0] < -0.2)


def door_side_faces(cen, nrm):
    """owner notes 17 Oct (V5): faces inside the door-line grooves always take their SIDE chart. The groove's lower
    cap wall faces up (nz ~0.5 where it meets the draft), so the normal-only rule sent a few of its faces to the TOP
    chart, which carries no ink there: a body-colour chip in the pink / lime band at the rear line's lower end"""
    x, ay, z = cen[:, 0], np.abs(cen[:, 1]), cen[:, 2]
    m = door_mask(x, ay, z)
    out = np.zeros(len(cen), bool)
    out[m] = (door_profile(x[m], ay[m], z[m]) > 0.005) & (np.abs(nrm[m, 1]) > 0.3)
    return out


def uv1_tampo(ob, hidden_fn=None, rear_fn=None, side_fn=None):
    me = ob.data
    nP = len(me.polygons)
    nrm = np.empty(nP * 3); me.polygons.foreach_get("normal", nrm); nrm = nrm.reshape(-1, 3)
    cen = np.empty(nP * 3); me.polygons.foreach_get("center", cen); cen = cen.reshape(-1, 3) / UU
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3) / UU
    li = np.empty(len(me.loops), np.int64); me.loops.foreach_get("vertex_index", li)
    lt = np.empty(nP, np.int64); me.polygons.foreach_get("loop_total", lt)
    fol = np.repeat(np.arange(nP), lt)
    nx, ny, nz = nrm[:, 0], nrm[:, 1], nrm[:, 2]
    cls = np.full(nP, 5)
    top = nz >= 0.45
    side = ~top & (np.abs(ny) >= 0.45)
    cls[side & (ny > 0)] = 0
    cls[side & (ny < 0)] = 1
    cls[top] = 2
    rest = ~top & ~side
    cls[rest & (nx > 0.4)] = 3
    cls[rest & (nx < -0.4)] = 4
    if rear_fn is not None:
        cls[rear_fn(cen, nrm)] = 4
    if side_fn is not None:
        sf = side_fn(cen, nrm)
        cls[sf & (ny > 0)] = 0
        cls[sf & (ny <= 0)] = 1
    if hidden_fn is not None:
        cls[hidden_fn(cen)] = 5
    c = cls[fol]; p = co[li]
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    u = np.zeros(len(li)); v = np.zeros(len(li))
    m = c == 0; u[m] = UV_S * (UVX0 - x[m]); v[m] = 0.02 + UV_S * z[m]
    m = c == 1; u[m] = 0.5 + UV_S * (x[m] - UVX1); v[m] = 0.02 + UV_S * z[m]
    m = c == 2; u[m] = UV_T * (UVX0 - x[m]); v[m] = TOP_V0 + UV_T * (UVY - y[m])
    m = c == 3; u[m] = FRONT_U0 + UV_S * (y[m] + UVY); v[m] = FR_V0 + UV_S * z[m]
    m = c == 4; u[m] = REAR_U0 + UV_S * (UVY - y[m]); v[m] = FR_V0 + UV_S * z[m]
    m = c == 5; u[m] = 0.96 + 0.04 * (UVX0 - x[m]) / 128.0; v[m] = 0.96 + 0.04 * (y[m] + UVY) / 82.0
    uv = me.uv_layers.new(name="UV1")
    uv.data.foreach_set("uv", np.stack([u, v], 1).ravel())
    me.uv_layers.active = me.uv_layers["UV0"]
    return np.bincount(cls, minlength=6).tolist()


def mood_uv1_rect():
    P = np.array(BONNET_POLY)
    x0, x1 = P[:, 0].min(), P[:, 0].max(); y0, y1 = P[:, 1].min(), P[:, 1].max()
    return [round(UV_T * (UVX0 - x1), 5), round(TOP_V0 + UV_T * (UVY - y1), 5),
            round(UV_T * (UVX0 - x0), 5), round(TOP_V0 + UV_T * (UVY - y0), 5)]


def body_hidden(cen):
    o = W.eval_chunked(lambda a, b, c: body_outer(a, np.abs(b), c), cen)
    bay = W.eval_chunked(lambda a, b, c: tray_vol(a, np.abs(b), c), cen)
    # r2: the engine bay (floor, walls, lid, louvres) is unprinted: its faces are parked off the tampo charts
    return (o < -1.05) | (cen[:, 2] < z_bot(cen[:, 0], np.abs(cen[:, 1])) + 0.2) | ((bay < 0.5) & (cen[:, 2] > TR_Z - 1.0))


def base_uv1(ob):
    me = ob.data
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3) / UU
    li = np.empty(len(me.loops), np.int64); me.loops.foreach_get("vertex_index", li)
    p = co[li]
    u = (p[:, 0] - UVX1) / 128.0
    v = (UVY - p[:, 1]) / 82.0
    uv = me.uv_layers.new(name="UV1")
    uv.data.foreach_set("uv", np.stack([u, v], 1).ravel())
    me.uv_layers.active = me.uv_layers["UV0"]


def copy_uv0_to_uv1(ob):
    me = ob.data
    a = np.empty(len(me.loops) * 2); me.uv_layers["UV0"].data.foreach_get("uv", a)
    uv = me.uv_layers.new(name="UV1"); uv.data.foreach_set("uv", a)
    me.uv_layers.active = me.uv_layers["UV0"]


# =============================================================================
#  TAMPO  (spec 4b rule 6): every ink layer is a 2D SDF in car space, rasterised into the
#  UV1 charts, offset per layer + side (registration 0.3-0.5 uu), with ragged edges and pinholes.
# =============================================================================
INK = {   # sRGB
    "lime": (0.714, 1.0, 0.0),
    "white": (0.965, 0.955, 0.925),
    "pink": (1.0, 0.16, 0.52),
    "dark": (0.075, 0.035, 0.12),
    "outline": (0.075, 0.035, 0.12),
    "red": (0.85, 0.06, 0.05),
    "amber": (1.0, 0.50, 0.04),
    "black": (0.032, 0.030, 0.034),      # tail band + plate (neutral black ink)
}
LIVERIES = {
    # paint = linear Base Color of the metallic enamel, flake = its sparkle tint
    "classof93": dict(paint=(0.150, 0.030, 0.50, 1.0), flake=(0.70, 0.55, 1.0, 1.0),
                      # r3 (rule 13, reviewer fix 3): dark tub = UE "Black" (import_castings.INTERIORS); the assembly
                      # agent is asked to switch ClassOf93's interior from "Grey" to "Black" to match
                      # r5 (fix 5, lead ruling): dark-grey tub, not black (INTERIOR_R5)
                      interior=(0.22, 0.22, 0.225, 1.0), number="93"),
}


def _vnoise(shape, cells, seed):
    """smooth value noise 0..1 on an image grid (bilinear over a random lattice)"""
    rng = np.random.default_rng(seed)
    h, w = shape
    gy, gx = cells
    g = rng.random((gy + 2, gx + 2))
    ys = np.linspace(0, gy, h)[:, None]; xs = np.linspace(0, gx, w)[None, :]
    y0 = np.floor(ys).astype(int); x0 = np.floor(xs).astype(int)
    fy = ys - y0; fx = xs - x0
    fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)
    a = g[y0, x0]; b = g[y0, x0 + 1]; c = g[y0 + 1, x0]; d = g[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


# ---- logotype "VORTEX": an original chunky italic, built from strokes ------------------
LOGO_H, LOGO_SW = 4.3, 0.56          # cap height, stroke half-width (uu)


def _letters(s, t):
    """SDF of the word VORTEX in a local frame: s along the reading direction from the word
    start, t up from the baseline. Returns (sdf, total_width)."""
    h, w = LOGO_H, LOGO_SW
    d = np.full(s.shape, 50.0)
    x0 = 0.0
    gap = 0.62
    def bar(a0, a1, b0, b1):
        return sd_rrect2(s - (a0 + a1) / 2.0, t - (b0 + b1) / 2.0, (a1 - a0) / 2.0, (b1 - b0) / 2.0, 0.18)
    def seg(p, q):
        return sd_seg2(s, t, p, q) - w
    # V
    wl = 3.5
    d = np.minimum(d, np.minimum(seg((x0 + w, h - w), (x0 + wl / 2, w)), seg((x0 + wl / 2, w), (x0 + wl - w, h - w))))
    x0 += wl + gap
    # O
    wl = 3.6
    ring = np.abs(sd_rrect2(s - (x0 + wl / 2), t - h / 2, wl / 2 - w, h / 2 - w, 1.0)) - w
    d = np.minimum(d, ring)
    x0 += wl + gap
    # R
    wl = 3.4
    stem = bar(x0, x0 + 2 * w, 0.0, h)
    bowl = np.abs(sd_rrect2(s - (x0 + wl / 2 - 0.1), t - (h * 0.73), wl / 2 - w - 0.1, h * 0.27 - w + 0.05, 0.75)) - w
    bowl = np.maximum(bowl, x0 + 0.6 - s)
    leg = seg((x0 + wl * 0.42, h * 0.48), (x0 + wl - w, w))
    d = np.minimum(d, np.minimum(np.minimum(stem, bowl), leg))
    x0 += wl + gap
    # T
    wl = 3.6
    d = np.minimum(d, np.minimum(bar(x0, x0 + wl, h - 2 * w, h), bar(x0 + wl / 2 - w, x0 + wl / 2 + w, 0.0, h)))
    x0 += wl + gap
    # E
    wl = 3.1
    e = np.minimum(bar(x0, x0 + 2 * w, 0.0, h), bar(x0, x0 + wl, h - 2 * w, h))
    e = np.minimum(e, np.minimum(bar(x0, x0 + wl * 0.84, h / 2 - w, h / 2 + w), bar(x0, x0 + wl, 0.0, 2 * w)))
    d = np.minimum(d, e)
    x0 += wl + gap
    # X
    wl = 3.6
    d = np.minimum(d, np.minimum(seg((x0 + w, h - w), (x0 + wl - w, w)), seg((x0 + w, w), (x0 + wl - w, h - w))))
    x0 += wl
    return d, x0


# ---- digits for the number (segment style, chunky) -------------------------------------
def _digit(s, t, ch, h, w):
    wl = h * 0.62
    def bar(a0, a1, b0, b1):
        return sd_rrect2(s - (a0 + a1) / 2.0, t - (b0 + b1) / 2.0, (a1 - a0) / 2.0, (b1 - b0) / 2.0, w * 0.6)
    top = bar(0, wl, h - 2 * w, h); mid = bar(0, wl, h / 2 - w, h / 2 + w); bot = bar(0, wl, 0, 2 * w)
    lt = bar(0, 2 * w, h / 2, h); lb = bar(0, 2 * w, 0, h / 2); rt = bar(wl - 2 * w, wl, h / 2, h)
    rb = bar(wl - 2 * w, wl, 0, h / 2)
    segs = {"9": (top, mid, bot, lt, rt, rb), "3": (top, mid, bot, rt, rb), "7": (top, rt, rb),
            "1": (rt, rb), "0": (top, bot, lt, lb, rt, rb)}[ch]
    d = segs[0]
    for sg in segs[1:]:
        d = np.minimum(d, sg)
    return d, wl


def _number(s, t, txt, h, w, gap):
    d = np.full(s.shape, 50.0); x0 = 0.0
    for ch in txt:
        dd, wl = _digit(s - x0, t, ch, h, w)
        d = np.minimum(d, dd); x0 += wl + gap
    return d, x0 - gap


def livery_side(x, z, sgn, xr=None, zr=None):
    """ink layers on one side (sgn +1 = left, -1 = right) as {ink: sdf}; x, z in uu.
    r5b (gate fix 8): xr, zr = the UN-shifted car coordinates of the same texels. Every band END (the raked tail cut,
    the cut parallel to the scoop's leading edge, the resume cut behind the rear arch, the scoop keep-out) is evaluated
    there, so it is ONE straight edge through white, lime and pink; only the band bodies carry each ink's 0.3-0.5 uu
    registration offset (they shift along / across the band, the ends do not fan out)"""
    if xr is None:
        xr, zr = x, z
    L = {}
    # r3 (reviewer fix 2): the stripes end in a clean raked cut at x -52.4 on the flat of the rear quarter (they used to
    # run into the tail-corner round, where the side/rear chart split chopped them into a ragged edge); front unchanged
    run = np.maximum(xr - 61.0, ((SIDE_STRIPE_END + 0.22 * (zr - 13.0)) - xr) / math.sqrt(1.0 + 0.22 ** 2))
    # twin side stripes above the rocker step, nose to tail (the arches interrupt them)
    # r5 (lead ruling: a pad cannot print across a deep step): the pink pinstripe sat across the top of the 0.75 rocker
    # step (z 11.73-12.17 vs the step at 11.25-11.95); it now sits wholly on the flat above it, under a lime band that
    # starts 0.5 higher (top edge and the white line unchanged)
    lime = np.maximum(np.abs(z - 13.6) - 1.0, run)
    white = np.maximum(np.abs(z - 15.25) - 0.33, run)
    pink = np.maximum(np.abs(z - 12.32) - 0.2, run)
    # logotype on the door: reading direction s (left side reads front -> rear), italic shear
    # owner notes 17 Oct (V5): the 4.3-tall word (23.9 uu + outline + shear) was longer than the door between the two
    # shut lines (~22.4 uu), so its first / last letter ran into a groove on each side (left: V into the front line,
    # X into the rear; right: X across the front line). The word is now LOGO_SCALE (0.87) of its r5b size on the same
    # baseline, centred per side (LOGO_XC) so its outline clears each door-line print break by >= 0.3 uu; the speed
    # lines scale with it and still trail across the next shut line, where the print parts cleanly (door_print_break)
    k = LOGO_SCALE
    xc = LOGO_XC[1 if sgn > 0 else -1]
    s0 = sgn * (xc - x)
    t = z - 16.55
    sh = 0.24
    ls, wid = _letters((s0 + k * wid_half() - sh * t) / k, t / k)
    ls = ls * k
    # speed lines trailing the logo toward the rear
    s_end = k * wid_half()
    sl_all = np.full(np.shape(x), 50.0)
    for tt, ln in ((0.45, 4.4), (1.75, 3.3), (3.05, 2.2)):
        tt, ln = k * tt, k * ln
        # each line starts SPEED_LINE_CLEAR past the far edge of the next door line's print break (r5b: 1.3 after the
        # word, which left a sliver of each line on the door and the rest across the groove)
        if SPEED_LINE_START == "break":
            xl, kk = DOOR_LINES[1] if sgn > 0 else DOOR_LINES[0]
            zt = 16.55 + tt
            x_far = xl - kk * (zt - 12.0) - sgn * (DOOR_PRINT_GAP + SPEED_LINE_CLEAR)
            s_a = sgn * (xc - x_far) + sh * tt                 # line start in the sheared s frame
        else:
            s_a = s_end + 1.3 * k
        sl = sd_rrect2(s0 - (s_a + ln / 2.0) + sh * tt, t - tt, ln / 2.0, 0.36 * k, 0.3 * k)
        sl_all = np.minimum(sl_all, sl)
    # (no pad print into the front wheel arch: the lines stop ARCH_PRINT_CLEAR short of the arch edge)
    if ARCH_PRINT_CLEAR is not None:
        sl_all = np.maximum(sl_all, ARCH_PRINT_CLEAR - arch_d(xr, zr))
    # tampo pads cannot print into the scoop. r5 (reviewer round-4 fix 6): the keep-out now clears the scoop's 1.0 lip
    # round (margin 1.3, was 0.5): r4 printed onto the lip, whose faces fall into other UV1 charts, so the stripe ended
    # on triangle edges (the jagged, pixel-stepped edge). The sill band (lime / white / pink) also stops in front of the
    # scoop with a cut parallel to its leading edge and does not resume until behind the rear axle - under the scoop
    # it could only have been printed on the lip (and in r4 left a sliver between the scoop and the rear arch)
    keep_out = -(scoop_sd(xr, zr) - SCOOP_PRINT_MARGIN)
    xl = SCOOP_Q[1][0] + (zr - SCOOP_Q[1][1]) * (SCOOP_Q[0][0] - SCOOP_Q[1][0]) / (SCOOP_Q[0][1] - SCOOP_Q[1][1])
    # r5b (gate fix 8): the band resumed with a vertical cut at x -34 (inside the arch opening, on no surface at all);
    # it now resumes on a raked cut just behind the rear arch lip + flare plateau (RESUME_CUT, parallel-ish to the tail cut)
    kl = (SCOOP_Q[0][0] - SCOOP_Q[1][0]) / (SCOOP_Q[0][1] - SCOOP_Q[1][1])
    kr = RESUME_CUT[1]
    gap = -np.maximum(((RESUME_CUT[0] + kr * (zr - 12.1)) - xr) / math.sqrt(1.0 + kr * kr),
                      (xr - (xl + SCOOP_PRINT_MARGIN + 0.15)) / math.sqrt(1.0 + kl * kl))
    band_out = np.maximum(keep_out, gap)
    L["outline"] = np.maximum(ls - 0.42, keep_out)
    L["white"] = np.maximum(np.minimum(np.maximum(white, gap), ls), keep_out)
    L["lime"] = np.maximum(np.minimum(np.maximum(lime, gap), sl_all), keep_out)
    L["pink"] = np.maximum(pink, band_out)
    # owner notes 17 Oct (V5): a pad print breaks cleanly across a shut line. Every side ink stops in a straight,
    # casting-registered gap along each door line (un-shifted car space, like the band ends), so the sill band, the
    # VORTEX logotype and the speed lines read as one print laid across the doors and parted by the grooves
    brk = door_print_break(xr, zr)
    for k in L:
        L[k] = np.maximum(L[k], -brk)
    return L


DOOR_PRINT_GAP = 0.70         # half width of the unprinted break along each door line (groove half width 1.15)
DOOR_PRINT_Z0 = 12.6          # the break runs straight down to the groove's lower end and stops square there


def door_print_break(x, z):
    """signed distance (uu, side view x/z) to the print break along the two door lines (negative inside the break):
    the groove's centre segment from its top cap centre straight down to DOOR_PRINT_Z0, widened by DOOR_PRINT_GAP and
    cut square at DOOR_PRINT_Z0 (where the groove ends; the pinstripe below is printed on the flat)"""
    d = np.full(np.shape(x), 50.0)
    z0, z1 = DOOR_PRINT_Z0, DOOR_CAPS[1]
    for xl, k in DOOR_LINES:
        ux, uz = -k / math.sqrt(1.0 + k * k), 1.0 / math.sqrt(1.0 + k * k)
        px, pz = xl - k * (z0 - 12.0), z0
        L = (z1 - z0) * math.sqrt(1.0 + k * k)
        t = np.clip((x - px) * ux + (z - pz) * uz, 0.0, L)
        d = np.minimum(d, np.hypot(x - (px + t * ux), z - (pz + t * uz)))
    return np.maximum(d - DOOR_PRINT_GAP, DOOR_PRINT_Z0 - z)


_WIDTH = None
LOGO_SCALE = 0.87             # owner notes 17 Oct (V5): door logotype scale (r5b: 1.0 = 4.3 uu cap height)
SPEED_LINE_START = "break"    # 'word': 1.3 uu after the word (r5b); 'break': past the next door line's print break
SPEED_LINE_CLEAR = 0.3        # gap between a door line's print break and the speed lines behind it
ARCH_PRINT_CLEAR = 1.0        # speed lines stop this far from the wheel-arch edge
LOGO_XC = {1: 9.35, -1: 7.8}  # word centre x per side (+1 left, -1 right; r5b: 9.4 both) - fitted between the breaks
SIDE_STRIPE_END = -52.4
SCOOP_PRINT_MARGIN = 1.3      # r5: print-free margin round the scoop outline (its lip round is 1.0)
RESUME_CUT = (-47.4, 0.31)    # r5b: band resumes behind the rear arch at x = -47.4 + 0.31 (z - 12.1) (>= 1.4 uu off the arch)
# r5 (reviewer round-4 fix 7): the deck stripes end at the front of the print-free engine-bay zone (x -14). r4 ran them
# on behind the bay, so fragments were printed on the narrow ducktail between the louvres and the tail lip - a strip a
# pad cannot reach past the bay walls
DECK_STRIPE_END = -14.0


def wid_half():
    global _WIDTH
    if _WIDTH is None:
        _WIDTH = _letters(np.zeros(1), np.zeros(1))[1]
    return _WIDTH / 2.0


def livery_top(x, y):
    L = {}
    ay = np.abs(y)
    # r3: the deck stripes end square on the flat deck, 2-3 uu short of the ducktail lip (front end unchanged)
    run = np.maximum(x - 63.0, DECK_STRIPE_END - x)
    L["lime"] = np.maximum(np.abs(ay - 5.3) - 2.25, run)
    L["white"] = np.maximum(np.abs(ay - 8.4) - 0.4, run)
    # racing roundel on the roof, read from the car's left
    rx, rr = -3.0, 4.7
    disc = np.hypot(x - rx, y) - rr
    L["outline"] = disc - 0.42
    L["white"] = np.minimum(np.maximum(L["white"], -(disc - 0.42)), disc)
    L["lime"] = np.maximum(L["lime"], -(disc - 0.42))
    # small STREAKLINE chevron on the nose, in the gap between the stripes
    chev = np.maximum(np.abs(y) * 0.9 + (x - 57.9) - 0.0, -(np.abs(y) * 0.9 + (x - 57.9) + 1.15))
    chev = np.maximum(chev, np.maximum(np.abs(y) - 2.3, 54.0 - x))
    L["white"] = np.minimum(L["white"], chev)
    num, wn = _number(np.zeros(1), np.zeros(1), "93", 4.4, 0.5, 0.6)
    # seen from the left side of the car the number reads with the front to the left:
    # local s = rx - x... rotate so it reads from above with the nose to the left
    d, _ = _number(-y + wn / 2.0, (x - rx) + 2.2, "93", 4.4, 0.5, 0.6)       # reads upright from the front (wave 4: was 180 deg out)
    L["dark"] = d
    # r2: a pad print cannot reach into the recessed engine bay: the stripes stop at its lip (roof in front, ducktail
    # deck behind), like the bare recesses of the real castings (rear_ref_01/02)
    bay = sd_rrect2(x - BAY_PRINT[0], y, BAY_PRINT[1], BAY_PRINT[2], 2.5)
    for k in L:
        L[k] = np.maximum(L[k], -bay)
    return L


BAY_PRINT = (-30.85, 16.85, 15.6)     # print-free plan rect over the bay: centre x, half length, half width (uu)


REAR_PRINT_SHIFT = (0.38, -0.22)     # r3 (fix 7): the tail pad lands 0.38 uu toward car-right, 0.22 low vs the casting


def livery_rear(y, z):
    """Tail print (rule 12), read from behind (image left = car left), on the r3 cast shapes: each lamp pod printed
    red with an amber inner third and a thin black bezel line; the plate panel between the pods printed black with
    a white '93'; a small white VORTEX on the plain body-colour bumper below. The whole pad is offset from the casting
    by REAR_PRINT_SHIFT (plus the per-ink 0.3-0.5 uu registration drift of make_tampo), so at macro the ink sits
    visibly off the cast lens edges like a real pad print."""
    y = y + REAR_PRINT_SHIFT[0]          # car-right = -y: print shifted toward -y
    z = z - REAR_PRINT_SHIFT[1]
    L = {}
    ay = np.abs(y)
    pod = pod_sd(ay, z)
    amber_cut = ay - 21.4                                  # amber inner part: |y| < 21.4 (r4: pods 1.7 shorter)
    # r4 (reviewer round-3 fix 4): the lens ink fills the WHOLE dish - floor and walls up to just past mid-wall
    # (pod_sd < +0.35) - and the thin black bezel line sits on the upper wall / lip (pod_sd 0.2 .. 0.62), overlapping
    # under the red so no body colour can open up between them; the per-ink drift on this pad is 0.05-0.12 uu (was
    # 0.3-0.5 per ink, which let red and black part by up to ~1 uu) on top of the pad's 0.44 uu offset
    L["black"] = np.minimum(np.abs(pod - 0.41) - 0.21,
                            sd_rrect2(y - PL_C[0], z - PL_C[1], PL_H[0] - 0.55, PL_H[1] - 0.45, 0.6))
    lens = pod - 0.35
    L["red"] = np.maximum(lens, -(amber_cut + 0.2))         # red runs 0.2 under the amber (printed after it)
    L["amber"] = np.maximum(lens, amber_cut)
    # plate number 2.2 uu; small logotype, cap height 1.7 uu, centred on the bumper below the plate
    num, wn = _number(np.zeros(1), np.zeros(1), "93", 2.2, 0.34, 0.45)
    d, _ = _number(-(y - PL_C[0]) + wn / 2.0, z - (PL_C[1] - 1.1), "93", 2.2, 0.34, 0.45)
    k = 1.7 / LOGO_H
    s = (-y) / k + wid_half()
    t = (z - 13.55) / k
    lt, _ = _letters(s - 0.24 * t, t)
    L["white"] = np.minimum(lt * k, d)
    return L


PRINT_ORDER = ("outline", "pink", "lime", "white", "dark")
TAMPO_GRIT = 0.03             # r5b: edge wobble amplitude (uu; was 0.07 = +-0.6 texel: read as stair-stepping)
TAMPO_SS = 4                  # r5b: edge super-sampling (4 x 4 per texel)
REAR_ORDER = ("black", "red", "amber", "white")


def make_tampo(path, res=4096, seed=1993):
    """Rasterise the livery into the UV1 charts -> RGBA PNG (straight alpha, sRGB colour)."""
    t0 = time.time()
    rng = np.random.default_rng(seed)
    H = Wd = res
    img = np.zeros((H, Wd, 4), np.float32)
    px = 1.0 / res
    v = (np.arange(H) + 0.5) / H
    u = (np.arange(Wd) + 0.5) / Wd
    grit = _vnoise((H, Wd), (res // 6, res // 6), seed) - 0.5          # ragged ink edges
    pin = _vnoise((H, Wd), (res // 3, res // 3), seed + 7)              # pinholes / thin ink
    blot = _vnoise((H, Wd), (24, 24), seed + 11)                        # ink density drift

    def chart(rows, cols, to_car, layers_fn, uu_per_px, order=PRINT_ORDER, rng=rng, drift=(0.3, 0.5), raw=False):
        vv = v[rows][:, None]; uu = u[cols][None, :]
        A = np.broadcast_to(uu, (len(rows), len(cols))); Bv = np.broadcast_to(vv, (len(rows), len(cols)))
        sub = img[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        gr = grit[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        ph = pin[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        bl = blot[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        p, q = to_car(A, Bv)

        def lay(pp, qq, off):
            return layers_fn(pp - off[0], qq - off[1], pp, qq) if raw else layers_fn(pp - off[0], qq - off[1])
        for ink in order:
            ang = rng.uniform(0, 2 * np.pi); mag = rng.uniform(*drift)
            off = (mag * math.cos(ang), mag * math.sin(ang))
            layers = lay(p, q, off)
            if ink not in layers:
                continue
            d = layers[ink] + gr * TAMPO_GRIT
            cov = np.clip(0.5 - d / uu_per_px, 0.0, 1.0)
            # r5b (gate fix 8, tampo ruling: vector-sharp edges): every texel the edge passes through is re-rasterised
            # from TAMPO_SS x TAMPO_SS sub-samples (= the masks rendered at 4x and box-downsampled)
            ii, jj = np.nonzero(np.abs(d) < 1.5 * uu_per_px)
            if len(ii):
                acc = np.zeros(len(ii))
                o = (np.arange(TAMPO_SS) + 0.5) / TAMPO_SS - 0.5
                g0 = gr[ii, jj] * TAMPO_GRIT
                for su in o:
                    for sv in o:
                        ps, qs = to_car(A[ii, jj] + su / Wd, Bv[ii, jj] + sv / H)
                        ds = lay(ps, qs, off)[ink] + g0
                        acc += np.clip(0.5 - ds / (uu_per_px / TAMPO_SS), 0.0, 1.0)
                cov[ii, jj] = acc / (TAMPO_SS * TAMPO_SS)
            cov *= np.clip(1.0 - np.maximum(ph - 0.955, 0.0) * 40.0, 0.0, 1.0)    # rare pinholes
            cov *= 0.94 + 0.06 * bl
            col = np.array(INK[ink], np.float32) * (0.97 + 0.03 * bl[..., None])
            a = cov[..., None]
            sub[..., :3] = sub[..., :3] * (1 - a) + col * a
            sub[..., 3:] = sub[..., 3:] * (1 - a) + a

    # side charts: V 0.02 .. 0.02 + 31/256, left U 0..0.5, right U 0.5..1
    r0 = int(0.02 * H); r1 = int((0.02 + UV_S * 31.0) * H) + 1
    rows = np.arange(r0, r1)
    upx_s = 1.0 / (UV_S * res)
    chart(rows, np.arange(0, Wd // 2), lambda U, Vv: (UVX0 - U / UV_S, (Vv - 0.02) / UV_S),
          lambda a, b, c, d: livery_side(a, b, 1.0, c, d), upx_s, raw=True)
    chart(rows, np.arange(Wd // 2, Wd), lambda U, Vv: ((U - 0.5) / UV_S + UVX1, (Vv - 0.02) / UV_S),
          lambda a, b, c, d: livery_side(a, b, -1.0, c, d), upx_s, raw=True)
    # top chart: V 0.30 .. 0.94
    rows = np.arange(int(TOP_V0 * H), int((TOP_V0 + UV_T * 82.0) * H) + 1)
    chart(rows, np.arange(0, Wd), lambda U, Vv: (UVX0 - U / UV_T, UVY - (Vv - TOP_V0) / UV_T),
          lambda a, b: livery_top(a, b), 1.0 / (UV_T * res))
    # rear chart: U 0.05 .. 0.37, V 0.17 .. 0.29 (y from the rear: U = 0.05 + (41 - y)/256)
    rows = np.arange(int(FR_V0 * H), int((FR_V0 + UV_S * 30.0) * H) + 1)
    cols = np.arange(int(REAR_U0 * Wd), int((REAR_U0 + UV_S * 82.0) * Wd) + 1)
    # (own ink order and own registration RNG, so the side / top prints stay exactly as before)
    chart(rows, cols, lambda U, Vv: (UVY - (U - REAR_U0) / UV_S, (Vv - FR_V0) / UV_S),
          lambda a, b: livery_rear(a, b), upx_s, order=REAR_ORDER, rng=np.random.default_rng(seed + 64),
          drift=(0.05, 0.12))       # r4: the tail pad prints as one, 0.44 uu off the casting (REAR_PRINT_SHIFT)
    im = bpy.data.images.new("Vortex_tampo", Wd, H, alpha=True, float_buffer=False)
    im.colorspace_settings.name = 'sRGB'
    im.alpha_mode = 'STRAIGHT'
    im.pixels.foreach_set(img.ravel())
    im.filepath_raw = path
    im.file_format = 'PNG'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save()
    bpy.data.images.remove(im)
    log("tampo %s (%dx%d) in %.1fs" % (os.path.basename(path), res, res, time.time() - t0))


# =============================================================================
#  Sidecar
# =============================================================================
CAMBER_TOE = {"FL": (0.4, -0.3), "FR": (-0.3, 0.25), "RL": (0.25, 0.35), "RR": (-0.45, -0.2)}


def ue(p):
    return [round(float(p[0]), 3), round(float(-p[1]), 3), round(float(p[2]), 3)]


def write_sidecar(objs, path, tris, uvcounts):
    bb = {k: W.bbox_uu(o) for k, o in objs.items()}
    b = bb["Body"]
    data = {
        "casting": "Vortex", "class": "Wedge", "brand": "STREAKLINE", "version": "v2 (die-cast rebuild, 14 Oct 2026)",
        "units": "uu, UE axes (X fwd, Y right, Z up); origin at ground level centred between the axles",
        "length": round(b[1] - b[0], 2), "width": round(max(b[3] - b[2], 2 * (WY + 3.2)), 2), "height": round(b[5], 2),
        "hitbox": HITBOX,
        "wheel_design": "W02_Fan", "wheel_radius": WR, "wheel_width": WW,
        "wheelbase": X_FA - X_RA, "track_front": 2 * WY, "track_rear": 2 * WY,
        "wheels": {"FL": ue([X_FA, WY, AXLE_Z]), "FR": ue([X_FA, -WY, AXLE_Z]),
                   "RL": ue([X_RA, WY, AXLE_Z]), "RR": ue([X_RA, -WY, AXLE_Z])},
        "wheel_mesh_note": "SM_Wheel_W02_Fan is authored as a LEFT wheel (show face to UE -Y); yaw the right wheels 180 deg (never mirror: the vanes are swept).",
        "wheel_camber_toe_deg_preview": CAMBER_TOE,
        "arches": {"radius": AR, "centre_z": ARZ, "tyre_gap_top": round(ARZ + AR - 2 * WR, 2), "well_wall_abs_y": WELL},
        "ground_clearance": BASE_Z0,
        "parts": {"Body": "SM_Vortex_Body", "Base": "SM_Vortex_Base", "Windows": "SM_Vortex_Windows",
                  "Interior": "SM_Vortex_Interior"},
        "feature": {"type": "MoodPaint", "panel": "bonnet",
                    "mask": "SM_Vortex_Body vertex colour Col.R = 1 on the bonnet lid (Paint faces), 0 elsewhere",
                    "uv1_rect": mood_uv1_rect(),
                    "panel_rect_uu": {"x": [27.0, 52.6], "half_width_rear": 13.6, "half_width_front": 10.4,
                                      "corner_radius": 2.4}},
        "slots": {"Body": ["Paint", "Chrome", "Lamp", "Zamac"], "Base": ["Base"], "Windows": ["Glass"],
                  "Interior": ["Interior"]},
        "lamp_tint": "Body vertex colour 'Col' on Lamp faces (front only): amber = outer front parking lamps, clear "
                     "white = inner. The lamps are CAST shapes coloured by printed ink: render Lamp as satin printed ink "
                     "tinted by Col (not glass). The TAIL lamps have no Lamp faces: they are tampo (UV1 rear chart) on the "
                     "Paint slot, printed on two cast lamp-pod dishes.",
        "chrome": "two separate round bored exhaust tips under the tail centre (y = +-1.6) only",
        "axles": {"part": "Body", "slot": "Zamac (r5b: bright bare steel, preview tint 0.86 / roughness 0.10)",
                  "radius": AXLE_R, "z": AXLE_Z, "x": [X_FA, X_RA], "rear_well_inner_wall_abs_y": WELL - WELL_R_DEEP,
                  "half_length": WY + W.HUB_FACE_Y,
                  "note": "thin steel axles in open channels under the body/base (visible from below); peened "
                          "mushroom heads at |y| = %.2f sit in the W02 hub centre holes" % (WY + W.HUB_FACE_Y)},
        "rivets": {"part": "Body", "slot": "Zamac", "x": list(RIVETS_X),
                   "note": "two peened rivet heads under the base (body posts through the base); KO pops the base off"},
        "base_text_area_uu": {"center": [2.0, 0.0], "half": [16.3, 10.8], "z": BASE_Z0 + 0.22,
                              "text": "STREAKLINE . VORTEX . 1993 . MADE IN ...  (decal; the panel is moulded plain)"},
        "tampo": {"preview_texture": "SourceArt/Blender/Vortex/preview/Vortex_tampo_%s.png" % OPT["livery"],
                  "layout": "UV1 charts (see uv.UV1_body_windows); RGBA, straight alpha, sRGB",
                  "livery_classof93": "metallic grape enamel; lime + white twin stripes over bonnet/roof/deck; lime sill "
                                      "band with white + pink pinstripes and a raked lime flash into the scoop; white "
                                      "'VORTEX' logotype with dark outline + lime speed lines on the doors; tail: two "
                                      "cast lamp pods printed red with amber inner thirds and a thin black bezel line, "
                                      "a black plate with white '93' on the cast panel between them, a small white "
                                      "VORTEX on the body-colour bumper; the deck stripes stop at the unprinted recessed "
                                      "engine bay (x -14, nothing printed behind it); the sill band stops ahead of "
                                      "the side scoop and resumes behind the rear axle; the side stripes end in a raked "
                                      "cut ahead of the tail corners",
                  "imperfections": "per-ink registration offset 0.3-0.5 uu per side, ragged edges, pinholes, density drift; "
                                           "the tail pad sits (0.38, -0.22) uu off the cast lamp/plate shapes"},
        "normals": "authored (analytic SDF gradients). Import normals, do not recompute.",
        "glass": "r5 per-pane tint: SM_Vortex_Windows vertex colour Col.R = 1 on the rear pane, 0 on windscreen + side "
                 "glass. Preview: windscreen/side light smoke 0.745 per surface (~55 %%), rear pane dark smoke 0.40 per "
                 "surface (~16 %%) with low mirror reflectance (F0 ~0.5 %%). UE M_ToyGlass should darken and de-gloss "
                 "by Col.R the same way; interior a 0.22 dark grey (not 'Black', rule 5: tub legible from the front)."
                 .replace("%%", "%"),
        "nanite": {"Body": True, "Base": True, "Interior": True, "Windows": False},
        "uv": {
            "UV0": "smart unwrap per part, non-overlapping (wear, grain, chips)",
            "UV1_body_windows": "tampo layout from the box x[-64,64] y[-41,41] uu (Blender axes): left side U 0-0.5 "
                                "(front at U 0, as seen from the left), right side U 0.5-1 (front at U 1), sides "
                                "V = 0.02 + z/256; top strip U = (64 - x)/128 (front at U 0), V = 0.30 + (41 - y)/128 "
                                "(seen from above with the nose to the left); front faces U = 0.55 + (y + 41)/256, rear "
                                "faces U = 0.05 + (41 - y)/256, both V = 0.17 + z/256; hidden faces parked at U,V 0.96-1. "
                                "Blender UV (V up); the UE importer flips V so the painted image reads the same.",
            "UV1_base": "projection from below, readable from below with the front to the right: U = (x + 64)/128, "
                        "V = (41 - y)/82",
            "UV1_interior": "copy of UV0",
            "body_uv1_face_counts[left,right,top,front,rear,hidden]": uvcounts,
        },
        "measured_bbox_uu_blender_axes": bb,
        "tris": tris,
        "source": "SourceArt/Blender/Vortex/build_Vortex.py",
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log("sidecar", os.path.basename(path))


# =============================================================================
#  Preview: Navvy's stage, Navvy's camera numbers (targets lowered for the lower car)
# =============================================================================
SHOTS = {
    "hero_34_front": dict(az=34.0, el=9.5, dist=6.0, lens=100, target=(0.10, 0.0, 0.135), focus=(0.38, 0.39, 0.12),
                          fstop=0.7, sun=(-12.0, 24.0)),
    "side_profile": dict(az=90.0, el=3.0, dist=8.2, lens=135, target=(0.01, 0.0, 0.15), focus=(0.0, 0.40, 0.14),
                         fstop=2.0, sun=(48.0, 28.0)),
    "rear_34": dict(az=-138.0, el=11.0, dist=6.6, lens=100, target=(-0.04, 0.0, 0.14), focus=(-0.58, -0.40, 0.15),
                    fstop=0.9, sun=(-150.0, 26.0)),
    "top_down": dict(top=True, dist=6.4, lens=100, target=(0.01, 0.0, 0.0), focus=(0.0, 0.0, 0.28), fstop=5.6,
                     sun=(110.0, 42.0)),
    "underside": dict(under=True, az=-30.0, el=-62.0, dist=6.8, lens=100, target=(0.01, 0.0, 0.10),
                      focus=(0.0, 0.0, 0.05), fstop=4.0, sun=(90.0, -20.0)),
    # family shot: the hero camera pulled back, Navvy parked on the next board, same light
    "family": dict(az=34.0, el=9.5, dist=9.6, lens=100, target=(-0.10, -0.55, 0.16), focus=(0.10, -0.25, 0.14),
                   fstop=1.4, sun=(-12.0, 24.0)),
    "cab_check": dict(az=25.0, el=26.0, dist=4.2, lens=100, target=(0.04, 0.0, 0.2), focus=(0.10, 0.12, 0.22),
                      fstop=4.0, sun=(-12.0, 24.0)),
    "wheel_close": dict(az=62.0, el=10.0, dist=2.4, lens=100, target=(X_FA * UU, WY * UU, AXLE_Z * UU),
                        focus=(X_FA * UU, (WY + 3) * UU, AXLE_Z * UU), fstop=2.2, sun=(80.0, 28.0)),
}
NAVVY_PARK = ((-0.30, -1.30, 0.0), -8.0)        # location (m), yaw (deg) for the family shot


def stage_wheels(wheel_ob, coll):
    wheels = []
    for key, (wx, wy, yaw) in {"FL": (X_FA, WY, 0.0), "FR": (X_FA, -WY, 180.0),
                               "RL": (X_RA, WY, 0.0), "RR": (X_RA, -WY, 180.0)}.items():
        o = bpy.data.objects.new("Wheel_" + key, wheel_ob.data)
        o.location = (wx * UU, wy * UU, AXLE_Z * UU)
        cam, toe = CAMBER_TOE[key]
        sgn = 1.0 if wy > 0 else -1.0
        o.rotation_euler = Euler((math.radians(cam) * sgn, 0.0, math.radians(yaw + toe)), 'XYZ')
        W.link(o, coll)
        wheels.append(o)
    return wheels


def render_previews(sc, objs, wheels, shots):
    STAGE = W.STAGE_OPT
    STAGE['samples'] = OPT['samples'] or (32 if Q else 96)
    STAGE['pct'] = OPT['pct'] or (50 if Q else 100)
    W.setup_render(sc)
    rig = W.setup_stage(sc)
    navvy = None
    for name in shots:
        cfg = SHOTS[name]
        if name == "family":
            if navvy is None:
                navvy = W.import_navvy(location=NAVVY_PARK[0], yaw_deg=NAVVY_PARK[1])
            for o in navvy.children_recursive:
                o.hide_render = o.name.startswith("SM_Wheel_W03_Lug")
        elif navvy is not None:
            for o in navvy.children_recursive:
                o.hide_render = True
        suffix = ("_q" if Q else "") + OPT["suffix"]
        W.render_shot(sc, rig, os.path.join(HERE, "preview", "Vortex_%s%s.png" % (name, suffix)), cfg)


# r4 (reviewer round-3 fix 5, rule 5 + 13): a light-SMOKE window moulding, ~45 % transmission through the part
# (0.67 per surface; the old preview glass was ~91 % clear), and a matt, darker one-colour tub, so the rear window reads
# as a dark tub from every angle - also with the low sun shining straight in through it. UE: Glass tint 0.67 and the
# Class of '93 interior = "Black" (import_castings.py, assembly agent).
GLASS_TINT = (0.67, 0.68, 0.70, 1.0)
INTERIOR_ROUGH = 0.78
# r5 (reviewer round-4 fixes 3 + 5, lead ruling on rules 5 + 13): PER-PANE tint on the one window moulding. Windows
# vertex colour Col.R = 1 on the rear pane (rear_pane_mask), 0 on the windscreen + side glass.
#   windscreen / side glass: light smoke 0.745 per surface (~55 % through the part) -> the tub reads from the front hero
#   rear pane: dark smoke 0.40 per surface (~16 %), low mirror reflectance (specular level 0.3, a touch of blur), so from
#   the chase cam and the oblique rear / C-pillar views it reads as a dark tub, never as the sunlit deck mirrored in it
# and the tub is a dark-grey moulding (0.22 linear: between UE "Charcoal" 0.11 and "Grey" 0.30; 0.11 still read black
# behind the windscreen in the hero sweep), matt, so seats and wheel read through the windscreen. UE: M_ToyGlass should darken + de-gloss by vertex colour R (assembly agent; noted in the sidecar).
GLASS_TINT_FRONT = (0.745, 0.755, 0.77, 1.0)     # ~55 % through the part
GLASS_TINT_REAR = (0.40, 0.40, 0.42, 1.0)
GLASS_SPEC_REAR, GLASS_ROUGH_REAR = 0.3, 0.04
GLASS_IOR_REAR = 1.05         # r5: 1.15 = F0 0.5 % (1.49: 3.9 %) - the transmission lobe's mirror ignores the specular
                              # level; owner notes V2: 1.05 (F0 0.06 %, total internal reflection only past 72 deg)
INTERIOR_R5 = (0.22, 0.22, 0.225, 1.0)        # dark grey (look-dev sweep 0.11 / 0.18 / 0.22 / 0.24; UE: a 0.22 grey)
# owner notes 17 Oct (V1, windscreen read as a dark teal slab from the front hero): the look-dev renders ran with Cycles'
# refractive caustics OFF, so every light path that reached the tub THROUGH the glass after a bounce (deck / body / sky
# fill through the windscreen) was dropped - only the direct sun lit the cab, and the tub read near-black behind ~55 %
# glass whatever its grey (sweep: tub 0.22 / 0.30 / 0.34 / 0.45 and tint 0.745 / 0.80 changed the hero windscreen by
# < 6 levels; caustics on: +18 levels, seat backs and wheel read). The game lights the cab through its translucent glass
# too, so review_rear_r5.py renders with refractive caustics ON (this flag). Tub (0.22 grey) and front tint unchanged.
PREVIEW_REFRACTIVE_CAUSTICS = True


def rear_pane_mask(V):
    """1 on the rear window moulding (in the bay's front wall), 0 on the windscreen and side glass.
    Owner notes 17 Oct (V2, the tan plank in the rear pane): r5 cut at x < -14.5, but the 2.7 uu thick rear moulding
    leans forward and its INNER face runs on to x ~ -12.9 at the top, so that strip took the light front-pane values
    (tint 0.745, IOR 1.49). Seen from a 3/4-rear camera, rays entering the dark outer face were totally internally
    reflected at that strip and left again toward the sunlit deck: a bright tan, ragged-edged patch. The rear moulding
    is now everything behind x -11.5 inboard of |y| 18 (the side glass is at |y| > 21 and ends at x -13.7)"""
    return ((V[:, 0] < -11.5) & (np.abs(V[:, 1]) < 18.0)).astype(float)


COAT_ROUGH = 0.085
AXLE_STEEL, AXLE_STEEL_ROUGH = (0.86, 0.86, 0.87, 1.0), 0.10      # r5b: bright bare steel (axles, heads, rivets)
FLAKE_SPARKLE = 0.08          # r5b: weight of the additive flake glint (see flake_sparkle_only)
FLAKE_BASE_KEEP = 0.0         # r5b: fraction of the flake tilt left in the metallic base (0 = smooth base)
PAINT_ROUGH_ADD = 0.0         # r5b: added to the enamel's base roughness


def flake_sparkle_only(mat):
    """r5b (gate fix 1, the dark blotch under the side window's rear-lower corner): diagnosed by re-rendering
    cpillar_R / corner_R from the r5 export with (a) the flake NORMAL perturbation at 0 -> blotch gone, (b) the flake
    COLOUR off -> blotch stays. The enamel fed the per-flake random normals (+-0.15) into the metallic base itself, so
    in grazing light every flake tilted away from the sun went black: a dark speckled patch on any surface near the
    terminator (here the cab-to-haunch fillet). Clamp: the metallic base shades with the smooth surface normal, and the
    sparkle comes back as a separate ADDITIVE glossy glint (flake tint x 0.08, scaled by the metal amount, i.e. none on
    tampo ink): it can brighten, never darken. Variant sweep (preview/opus_rear_r5b/paintdiag, pA-pG): a 0.30 glint
    lifted the whole hero ~10 levels (front colour shift); keeping 35 % of the tilt in the base left a dotted dark
    streak along reflection edges; this setting (pG) is within ~4 levels of r5 on the nose and leaves no blotch. UE
    M_ToyPaint: never perturb the base normal per flake - make the flake an additive sparkle term (assembly agent)."""
    nt = mat.node_tree
    pb = nt.nodes.get("Principled BSDF")
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    lk = [l for l in nt.links if l.to_node == pb and l.to_socket.name == "Normal"]
    if not lk:
        return
    flake_n = lk[0].from_socket
    if FLAKE_BASE_KEEP > 0.0:
        # keep a fraction of the per-flake tilt in the metallic base (look-dev knob; 0 = smooth base)
        for n in nt.nodes:
            if n.type == 'VECT_MATH' and n.operation == 'SCALE' and not n.inputs['Scale'].is_linked:
                n.inputs['Scale'].default_value = n.inputs['Scale'].default_value * FLAKE_BASE_KEEP
    else:
        nt.links.remove(lk[0])
    if PAINT_ROUGH_ADD:
        rl = [l for l in nt.links if l.to_node == pb and l.to_socket.name == "Roughness"]
        ra = nt.nodes.new('ShaderNodeMath'); ra.operation = 'ADD'; ra.inputs[1].default_value = PAINT_ROUGH_ADD
        if rl:
            nt.links.new(rl[0].from_socket, ra.inputs[0])
        else:
            ra.inputs[0].default_value = pb.inputs["Roughness"].default_value
        nt.links.new(ra.outputs[0], pb.inputs["Roughness"])
    try:
        gl = nt.nodes.new('ShaderNodeBsdfGlossy')
    except Exception:
        gl = nt.nodes.new('ShaderNodeBsdfAnisotropic')
    gl.location = (pb.location.x, pb.location.y - 700)
    if "Roughness" in gl.inputs:
        gl.inputs["Roughness"].default_value = 0.16
    nt.links.new(flake_n, gl.inputs["Normal"])
    sc = nt.nodes.new('ShaderNodeVectorMath'); sc.operation = 'SCALE'
    tint = mat.get("flake_tint", (0.70, 0.55, 1.0))
    sc.inputs[0].default_value = tint[:3]
    ml = [l for l in nt.links if l.to_node == pb and l.to_socket.name == "Metallic"]
    if ml:
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'
        nt.links.new(ml[0].from_socket, mm.inputs[0]); mm.inputs[1].default_value = FLAKE_SPARKLE
        nt.links.new(mm.outputs[0], sc.inputs['Scale'])
    else:
        sc.inputs['Scale'].default_value = 0.82 * FLAKE_SPARKLE
    nt.links.new(sc.outputs[0], gl.inputs["Color"])
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(pb.outputs[0], add.inputs[0]); nt.links.new(gl.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs["Surface"])


def preview_materials(liv, tampo_path):
    p = W.make_slot_material("Paint", paint=liv["paint"], flake=liv["flake"], tampo=tampo_path)
    # r4 (reviewer round-3 fix 6): the "short dark scratch streaks" on the haunches are NOT texture or wear - they
    # vanish with the clear coat off (streak test in the r4 report): they are mirror images of the deck's dark board
    # gaps in a 0.045-rough coat curved over the haunch. Thick toy enamel is not a mirror: coat roughness 0.085 blurs
    # them into soft gradients (still a high gloss).
    pb = p.node_tree.nodes.get("Principled BSDF")
    pb.inputs["Coat Roughness"].default_value = COAT_ROUGH
    p["flake_tint"] = tuple(float(c) for c in liv["flake"][:3])
    flake_sparkle_only(p)
    for slot in ("Chrome", "Lamp", "Zamac", "Base", "Tire", "Hub"):
        W.make_slot_material(slot)
    # r5b (gate fix 6, lead ruling on rule 14): the steel axles / peened heads / rivets read as BRIGHT bare steel (was a
    # 0.62 grey at roughness 0.24: in the rear wells it rendered as a sub-pixel glint). UE: a Vortex-only bright steel
    # MI on the Body's Zamac slot (Tint ~0.86, Roughness ~0.10) - handed to the assembly agent; M_Zamac is shared with
    # Navvy and is not touched here.
    zb = bpy.data.materials["Zamac"].node_tree.nodes.get("Principled BSDF")
    zb.inputs["Base Color"].default_value = AXLE_STEEL
    zb.inputs["Roughness"].default_value = AXLE_STEEL_ROUGH
    g = W.make_slot_material("Glass", glass=GLASS_TINT_FRONT, glass_shadow=GLASS_TINT_FRONT)
    # r5: per-pane tint / gloss driven by the windows' vertex colour Col.R (1 = rear pane)
    nt = g.node_tree
    gb = nt.nodes.get("Principled BSDF")
    vc = nt.nodes.new('ShaderNodeVertexColor'); vc.location = (-900, 200)
    try:
        vc.layer_name = "Col"
    except Exception:
        pass
    sep = nt.nodes.new('ShaderNodeSeparateColor'); sep.location = (-700, 200)
    nt.links.new(vc.outputs['Color'], sep.inputs[0])

    def _mix_into(sock, a, b, color):
        mx = nt.nodes.new('ShaderNodeMix'); mx.location = (-450, 200)
        mx.data_type = 'RGBA' if color else 'FLOAT'
        nt.links.new(sep.outputs[0], mx.inputs['Factor'])
        ia, ib = (6, 7) if color else (2, 3)
        mx.inputs[ia].default_value = a; mx.inputs[ib].default_value = b
        nt.links.new(mx.outputs[2 if color else 0], sock)
    _mix_into(gb.inputs["Base Color"], GLASS_TINT_FRONT, GLASS_TINT_REAR, True)
    if "Specular IOR Level" in gb.inputs:
        _mix_into(gb.inputs["Specular IOR Level"], 0.5, GLASS_SPEC_REAR, False)
    _mix_into(gb.inputs["Roughness"], 0.015, GLASS_ROUGH_REAR, False)
    _mix_into(gb.inputs["IOR"], 1.49, GLASS_IOR_REAR, False)
    tr = [n for n in nt.nodes if n.type == 'BSDF_TRANSPARENT'][0]
    _mix_into(tr.inputs["Color"], GLASS_TINT_FRONT, GLASS_TINT_REAR, True)
    m = W.make_slot_material("Interior", interior=INTERIOR_R5)
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Roughness"].default_value = INTERIOR_ROUGH
    if "Specular IOR Level" in bs.inputs:
        bs.inputs["Specular IOR Level"].default_value = 0.3


def main():
    t0 = time.time()
    sc = W.reset_scene()
    liv = LIVERIES[OPT["livery"]]
    tampo_path = os.path.join(HERE, "preview", "Vortex_tampo_%s.png" % OPT["livery"])
    make_tampo(tampo_path, res=2048 if Q else 4096)
    preview_materials(liv, tampo_path)
    coll = W.get_coll("Vortex")
    body = build_body(coll)
    base = build_base(coll)
    win = build_windows(coll)
    inter = build_interior(coll)
    objs = {"Body": body, "Base": base, "Windows": win, "Interior": inter}
    tris = {k: W.tri_count(o) for k, o in objs.items()}
    log("tris", tris)
    for o in objs.values():
        W.smart_uv(o, "UV0", angle=60.0, margin=0.002)
    uvc = uv1_tampo(body, body_hidden, tail_pad_faces, door_side_faces)
    uv1_tampo(win)
    base_uv1(base)
    copy_uv0_to_uv1(inter)
    wcoll = W.get_coll("PreviewWheels")
    wheel = W.build_wheel(name="W02_Fan_preview", coll=wcoll, quick=Q)
    tris["Wheel_W02_Fan"] = W.tri_count(wheel)
    if OPT["export"] and not Q:
        for k, o in objs.items():
            W.export_fbx(o, os.path.join(HERE, "export", o.name + ".fbx"))
        write_sidecar(objs, os.path.join(HERE, ASSET + ".json"), tris, uvc)
    wheel.hide_render = True
    wheel.hide_set(True)
    wheels = stage_wheels(wheel, wcoll)
    for k in OPT["hide"]:                      # look-dev: --hide Windows,Body ...
        if k in objs:
            objs[k].hide_render = True
    log("geometry done in %.1fs" % (time.time() - t0))
    if OPT["render"]:
        shots = OPT["shots"] or ["hero_34_front", "family", "side_profile", "rear_34", "top_down", "underside",
                                 "wheel_close"]
        shots = [{"hero": "hero_34_front", "side": "side_profile", "rear": "rear_34", "top": "top_down"}.get(s, s)
                 for s in shots]
        render_previews(sc, objs, wheels, shots)
    if not Q:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, ASSET + ".blend"), compress=True)
    log("done; total %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
