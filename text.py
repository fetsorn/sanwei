# /Volumes/HD-PATU3/Applications/Blender.app/Contents/MacOS/Blender --background --python ./text.py --render-frame 1 -- ./test1 100 128 "你好"

import bpy
import sys
import math
import os
from typing import Tuple

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Args
output_file_path = str(sys.argv[sys.argv.index('--') + 1])
resolution_percentage = int(sys.argv[sys.argv.index('--') + 2])
num_samples = int(sys.argv[sys.argv.index('--') + 3])
hanzi = str(sys.argv[sys.argv.index('--') + 4])

# Scene Building

## Reset
## clean objects
for item in bpy.data.objects:
    bpy.data.objects.remove(item)

## load fonts
# bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Songti.ttc")

scene = bpy.data.scenes["Scene"]

## set the scene, create text
body: str = hanzi 
name: str = "text"
align_x: str = 'CENTER'
align_y: str = 'CENTER'
size: float = 5.0
# font_name: str = "STSongti-SC-Black"
extrude: float = 0.1
space_line: float = 1.0
location: Tuple[float, float, float] = (0.0, 0.0, 0.0)
rotation: Tuple[float, float, float] = (90.0, 0.0, 0.0)

new_text_data: bpy.types.Curve = bpy.data.curves.new(name=name, type='FONT')

new_text_data.body = body
new_text_data.align_x = align_x
new_text_data.align_y = align_y
new_text_data.size = size
new_text_data.font = bpy.data.fonts[font_name]
new_text_data.space_line = space_line
new_text_data.extrude = extrude

new_object: bpy.types.Object = bpy.data.objects.new(name, new_text_data)
scene.collection.objects.link(new_object)

new_object.location = location
new_object.rotation_euler = (math.pi * rotation[0] / 180.0, math.pi * rotation[1] / 180.0, math.pi * rotation[2])

# add material
name1: str = "Material"
use_nodes: bool = True
make_node_tree_empty: bool = True
material = bpy.data.materials.new(name1)
material.use_nodes = use_nodes
nodes1 = material.node_tree.nodes
for node in nodes1:
    nodes1.remove(node)
mat = material

# prepare to color material
nodes = mat.node_tree.nodes
links = mat.node_tree.links
output_node = nodes.new(type='ShaderNodeOutputMaterial')
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
# basic 
base_color: Tuple[float, float, float, float] = (0.6, 0.6, 0.6, 1.0)
subsurface: float = 0.0
subsurface_color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 1.0)
subsurface_radius: Tuple[float, float, float] = (1.0, 0.2, 0.1)
metallic: float = 0.0
specular: float = 0.5
specular_tint: float = 0.0
roughness: float = 0.5
anisotropic: float = 0.0
anisotropic_rotation: float = 0.0
sheen: float = 0.0
sheen_tint: float = 0.5
clearcoat: float = 0.0
clearcoat_roughness: float = 0.03
ior: float = 1.45
transmission: float = 0.0
transmission_roughness: float = 0.0
## override gold
# base_color=(1.00, 0.71, 0.22, 1.0)
# metallic=1.0
# specular=0.5
# roughness=0.1
## override blue
# base_color=(0.1, 0.2, 0.6, 1.0)
# metallic=0.5
# specular=0.5
# roughness=0.9
## override pink
base_color=(0.8, 0.7, 0.9, 1.0)
metallic=0.5
specular=0.5
roughness=0.9

# apply material
principled_node.inputs['Base Color'].default_value = base_color
principled_node.inputs['Subsurface'].default_value = subsurface
principled_node.inputs['Subsurface Color'].default_value = subsurface_color
principled_node.inputs['Subsurface Radius'].default_value = subsurface_radius
principled_node.inputs['Metallic'].default_value = metallic
principled_node.inputs['Specular'].default_value = specular
principled_node.inputs['Specular Tint'].default_value = specular_tint
principled_node.inputs['Roughness'].default_value = roughness
principled_node.inputs['Anisotropic'].default_value = anisotropic
principled_node.inputs['Anisotropic Rotation'].default_value = anisotropic_rotation
principled_node.inputs['Sheen'].default_value = sheen
principled_node.inputs['Sheen Tint'].default_value = sheen_tint
principled_node.inputs['Clearcoat'].default_value = clearcoat
principled_node.inputs['Clearcoat Roughness'].default_value = clearcoat_roughness
principled_node.inputs['IOR'].default_value = ior
principled_node.inputs['Transmission'].default_value = transmission
principled_node.inputs['Transmission Roughness'].default_value = transmission_roughness

links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
new_object.data.materials.append(mat)

## create camera
bpy.ops.object.camera_add(location=(10.0, -7.0, 0.0))
camera_object = bpy.context.object

## add track to constraint
constraint = camera_object.constraints.new(type='TRACK_TO')
constraint.target = new_object
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

## set camera params
lens: float = 50.0
fstop: float = 1.4
### Simulate Sony's FE 85mm F1.4 GM
camera = camera_object.data
camera.sensor_fit = 'HORIZONTAL'
camera.sensor_width = 36.0
camera.sensor_height = 24.0
camera.lens = lens
camera.dof.use_dof = True
camera.dof.focus_object = new_object
camera.dof.aperture_fstop = fstop
camera.dof.aperture_blades = 11

## Lights
## create sun light

location1: Tuple[float, float, float] = (0.0, 0.0, 5.0)
rotation1: Tuple[float, float, float] = (90.0, 0.0, 0.0)
bpy.ops.object.light_add(type='SUN', location=location1, rotation=rotation1)

# Render Setting
scene.render.resolution_percentage = resolution_percentage
scene.render.filepath = output_file_path

## set cycles
use_denoising: bool = True
use_motion_blur: bool = False
use_transparent_bg: bool = False
scene.camera = camera_object

scene.render.image_settings.file_format = 'PNG'
scene.render.engine = 'CYCLES'
scene.render.use_motion_blur = use_motion_blur

scene.render.film_transparent = use_transparent_bg
scene.view_layers[0].cycles.use_denoising = use_denoising

scene.cycles.samples = num_samples

