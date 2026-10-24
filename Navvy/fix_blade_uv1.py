"""fix_blade_uv1.py - re-lay the Navvy blade's UV1 (tampo) with the wave 4 build_navvy.uv1_blade and re-export ONLY
SM_Navvy_Blade.fbx, without rebuilding (and so without any chance of changing) the casting itself.

  blender -b SourceArt/Blender/Navvy/navvy.blend --python SourceArt/Blender/Navvy/fix_blade_uv1.py

Backups of the previous .blend / FBX are in _backup_wave4/. The function body is read from build_navvy.py so there is one
source of truth; the mesh geometry, UV0, materials and normals are untouched."""
import os
import re
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(bpy.data.filepath))
src = open(os.path.join(HERE, 'build_navvy.py'), encoding='utf-8').read()
m = re.search(r'def uv1_blade\(ob\):.*?(?=\ndef uv1_bottom)', src, re.S)
exec(m.group(0), globals())

ob = bpy.data.objects['SM_Navvy_Blade']
loc = ob.location.copy()
uv1_blade(ob)
for o in bpy.data.objects:
    o.select_set(False)
ob.select_set(True)
bpy.context.view_layer.objects.active = ob
ob.location = (0.0, 0.0, 0.0)
bpy.ops.export_scene.fbx(filepath=os.path.join(HERE, 'export', 'SM_Navvy_Blade.fbx'), use_selection=True, apply_unit_scale=True,
                         apply_scale_options='FBX_SCALE_UNITS', axis_forward='X', axis_up='Z', bake_space_transform=True,
                         mesh_smooth_type='FACE', use_tspace=True, add_leaf_bones=False, object_types={'MESH'},
                         use_mesh_modifiers=True)
ob.location = loc
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'navvy.blend'), compress=True)
print('blade UV1 re-laid and exported')
