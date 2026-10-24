"""
build_Wheel_W03_Lug.py -- MODEL '93 shared wheel design W03_Lug (chunky off-road lug tyre, black, yellow hub).

The wheel geometry lives in ../Navvy/build_navvy.py (build_wheel), because it is authored together with
the Navvy casting that first uses it. This wrapper builds ONLY the wheel from an empty scene:
  * saves Wheel_W03_Lug.blend
  * exports export/SM_Wheel_W03_Lug.fbx (spec section 2 settings, origin at wheel centre, axle along Y)
  * writes Wheel_W03_Lug.json
  * renders preview/wheel_solo_34.png and preview/wheel_solo_face.png

Run (headless):
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup --python build_Wheel_W03_Lug.py
Extra options after "--" are passed through (e.g. -- --no-render, --samples 64, --pct 50).
Building the Navvy casting (build_navvy.py) also re-exports this wheel and renders preview/wheel_close.png.
"""
import os
import sys
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'Navvy', 'build_navvy.py')

if '--' not in sys.argv:
    sys.argv.append('--')
if '--wheel-only' not in sys.argv:
    sys.argv.append('--wheel-only')
runpy.run_path(SRC, run_name='__main__')
