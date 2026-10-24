"""shading_check_rear.py - the pipeline's grazing-light check (Tools/Assembly/shading_check.py, unmodified) with extra
REAR views whose low key light actually rakes the tail (round 2 review fix 6: the stock 'rear34' view puts the sun on the
far, front side of the car, so the tail sat in shadow and was never grazed).

  blender -b --factory-startup --python shading_check_rear.py -- <export dir> [more dirs] --out DIR
          [--paint r,g,b] [--views front34,rear34_rake,rear34_side,rear_low]

Extra views (camera az/el as in shading_check; sun 6 deg above the horizon, azimuth = camera az + 'sun'):
  rear34_rake  camera behind-right (-142, 14); sun from az -100: skims ACROSS the tail panel (80 deg incidence) - every
               dent, crease or facet on the tail, bumper and hatch shows as a streak
  rear34_side  same camera; sun from behind-left (az 170): skims along the right flank, flare and quarter window
  rear_low     low chase-side camera (-168, 5); sun from az -105: rakes the tail, bumper, lip and the tucked flares
"""
import os
import sys

TOOLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "Tools", "Assembly"))
sys.path.insert(0, TOOLS)
import shading_check as SC   # noqa: E402

SC.VIEWS.update({
    "rear34_rake": dict(az=-142.0, el=14.0, dist=3.5, sun=42.0),
    "rear34_side": dict(az=-142.0, el=14.0, dist=3.5, sun=-48.0),
    "rear_low": dict(az=-168.0, el=5.0, dist=3.2, sun=63.0),
})
if "--views" not in sys.argv:
    sys.argv += ["--views", "front34,rear34_rake,rear34_side,rear_low"]
SC.main()
