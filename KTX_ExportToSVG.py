# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
	"name": "KTX SVG Exporter",
	"description": "Export Active Curve to SVG file",
	"author": "Roel Koster, @koelooptiemanna, irc:kostex",
	"version": (1, 0, 7),
	"blender": (2, 80, 0),
	"location": "Properties > Scene",
	"warning": "",
	"wiki_url": "https://github.com/kostex/blenderscripts/",
	"tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
	"category": "Scene"}


import bpy, os, math
from bpy.types import Panel
from bpy.props import StringProperty, IntProperty

def fcol_to_icol(fcol):
	icol=max(0, min(255, int(math.floor(fcol * 256.0))))
	return icol

def bcol_to_rgb(bcol):
	fcol = "#" + \
		"%0.2X" % fcol_to_icol(bcol[0]) + \
		"%0.2X" % fcol_to_icol(bcol[1]) + \
		"%0.2X" % fcol_to_icol(bcol[2])
	return fcol


class KTXSVGOUT_OT_ExportToSVG(bpy.types.Operator):
	"""Export to SVG"""
	bl_idname = "ktxsvgout.exporttosvg"
	bl_label = "Export"

	def execute(self, context):
		import bpy,os
		scale = context.scene.ktx_svg_out_scale
		f=open(context.scene.ktx_svg_out_file,"w+")
		f.write('<svg>')
		for selcurv in bpy.context.selected_objects:
			curve=selcurv.data.name
			if len(selcurv.material_slots) > 0:
				fcol=bcol_to_rgb(bpy.data.materials[selcurv.material_slots[0].name].diffuse_color)
			else:
				fcol="#000"
			f.write('<path id="' + curve + '" fill="' + fcol + '" stroke="none" d="')
			c = bpy.data.curves[curve]
			for s in c.splines:
				line = "M " + str(s.bezier_points[0].co[0] * scale) + "," + str(-s.bezier_points[0].co[1] * scale) + " C "
				for i in range(0,len(s.bezier_points)-1):
					line = line + str(s.bezier_points[i].handle_right[0] * scale) + "," + str(-s.bezier_points[i].handle_right[1] * scale) + " "
					line = line + str(s.bezier_points[i+1].handle_left[0] * scale) + "," + str(-s.bezier_points[i+1].handle_left[1] * scale) + " "
					line = line + str(s.bezier_points[i+1].co[0] * scale) + "," + str(-s.bezier_points[i+1].co[1] * scale) + " "
				if s.use_cyclic_u:
					line = line + str(s.bezier_points[i+1].handle_right[0] * scale) + "," + str(-s.bezier_points[i+1].handle_right[1] * scale) + " "
					line = line + str(s.bezier_points[0].handle_left[0] * scale) + "," + str(-s.bezier_points[0].handle_left[1] * scale) + " "
					line = line + str(s.bezier_points[0].co[0] * scale) + "," + str(-s.bezier_points[0].co[1] * scale)
					line = line + " Z"
				line = line + "\r\n"
				f.write(line)
			f.write('"/>')
		f.close()

		return {'FINISHED'}


class KTXSVGOUT_PT_Panel(bpy.types.Panel):
	"""Creates a Panel in the scene context of the properties editor"""
	bl_label = "KTX Export to SVG"
	bl_idname = "KTXSVGOUT_PT_Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
#	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout

		scene = context.scene

		layout.prop(scene, "ktx_svg_out_file", text="SVG Output File")
		layout.prop(scene, "ktx_svg_out_scale", text="Scale")
		if bpy.context.active_object.type == "CURVE":
			layout.operator("ktxsvgout.exporttosvg")

classes = (
	KTXSVGOUT_OT_ExportToSVG,
	KTXSVGOUT_PT_Panel
)

def register():
	bpy.types.Scene.ktx_svg_out_file = StringProperty(default="output.svg", subtype="FILE_PATH", description="File")
	bpy.types.Scene.ktx_svg_out_scale = IntProperty(default=100, description="Scale Factor")
	from bpy.utils import register_class

	for cls in classes:
		register_class(cls)


def unregister():
	del bpy.types.Scene.ktx_svg_out_scale
	del bpy.types.Scene.ktx_svg_out_file
	from bpy.utils import unregister_class

	for cls in classes:
		unregister_class(cls)


if __name__ == "__main__":
	register()
