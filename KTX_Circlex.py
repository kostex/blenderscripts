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

import bpy
import bmesh
import math, mathutils
from math import radians


bl_info = {
	"name": "KTX Circlex",
	"description": "Create an inward extruding/rotating Circloid object",
	"author": "Roel Koster, @koelooptiemanna, irc:kostex",
	"version": (1, 0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Tools > Create",
	"warning": "",
	"wiki_url": "https://github.com/kostex/blenderscripts/",
#    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
	"category": "3D View"}


EDIT_MODES = {'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE',
			  'EDIT_METABALL', 'EDIT_TEXT', 'EDIT_ARMATURE'}


class KTXCIRCLEX_OT_Sep(bpy.types.Operator):
	bl_idname = "ktxcirclex.sep"
	bl_label = "KTX Create Circloid"
	bl_options = {'REGISTER', 'UNDO', 'PRESET'}
	bl_description = "Creates the circloid"

	own : bpy.props.BoolProperty(name="Own",
		description="Use own mesh",
		default=False)

	verts : bpy.props.IntProperty(name="Vertices",
		description="Circle divided into this many Vertices",
		default=60, min=3, max=360)

	steps : bpy.props.IntProperty(name="Steps",
		description="Number of extrusions",
		default=50, min=1)

	uni_scale : bpy.props.BoolProperty(name="Uni Scale",
		description="Use same X,Y,Z Scale",
		default=True)

	scale_x : bpy.props.FloatProperty(name="Scale X",
		description="Scale X Factor after each Extrude",
		default=0.984)

	scale_y : bpy.props.FloatProperty(name="Scale Y",
		description="Scale Y Factor after each Extrude",
		default=0.984)

	scale_z : bpy.props.FloatProperty(name="Scale Z",
		description="Scale Z Factor after each Extrude",
		default=0.984)

	rotation_x : bpy.props.FloatProperty(name="Rotation X",
		description="Rotation Angle X after each Extrude",
		default=2.46)

	x1 : bpy.props.FloatProperty(name="X",
		description="X Translation after each Extrude",
		default=0.0)

	y1 : bpy.props.FloatProperty(name="Y",
		description="Y Translation after each Extrude",
		default=0.0)

	z1 : bpy.props.FloatProperty(name="Z",
		description="Z Translation after each Extrude",
		default=0.0)

	x2 : bpy.props.FloatProperty(name="Rot Pivot X",
		description="Pivot Center X for Rotation",
		default=0.0)

	y2 : bpy.props.FloatProperty(name="Rot Pivot Y",
		description="Pivot Center Y for Rotation",
		default=0.0)

	z2 : bpy.props.FloatProperty(name="Rot Pivot Z",
		description="Pivot Center Z for Rotation",
		default=0.0)

	smooth_onoff : bpy.props.BoolProperty(name="Smoothing",
		description="Smoothing On/Off",
		default=False)

	subs_onoff : bpy.props.BoolProperty(name="Subdivide",
		description="Subdiv Modifier On/Off",
		default=False)

	solid_onoff : bpy.props.BoolProperty(name="Solidify",
		description="Solidify Modifier On/Off",
		default=False)

	sol_thickness : bpy.props.FloatProperty(name="Thickness",
		description="Solidify Thickness",
		default=0.05)

	@classmethod
	def poll(self, context):
		return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
				(context.area.spaces.active.type == 'VIEW_3D'))

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'own', text="Own Mesh")
		if not self.own:
			col.prop(self, 'verts', text="Circle Verts")
		col.prop(self, 'steps', text="Extrusion Steps")
		col.separator()
		col.prop(self, 'uni_scale', text="Universal Scale")
		col.prop(self, 'scale_x', text="X Scale")
		if not self.uni_scale:
			col.prop(self, 'scale_y', text="Y Scale")
		col.separator()
		col.prop(self, 'rotation_x', text="Rotation")
		col.prop(self, 'x2', text="Pivot Point X")
		col.prop(self, 'y2', text="Pivot Point Y")
		col.prop(self, 'z2', text="Pivot Point Z")
		col.separator()
		col.prop(self, 'x1', text="Translation X")
		col.prop(self, 'y1', text="Translation Y")
		col.prop(self, 'z1', text="Translation Z")
		col.separator()
		col.prop(self, 'smooth_onoff', text="Smoothing")
		col.prop(self, 'subs_onoff', text="Subdivision")
		col.prop(self, 'solid_onoff', text="Solidify")
		if self.solid_onoff:
			col.prop(self, 'sol_thickness', text="Thickness")


	def execute(self, context):
		import math
		import bmesh
		from math import radians

		if self.uni_scale:
			ys=self.scale_x
			zs=self.scale_x
		else:
			ys=self.scale_y
			zs=self.scale_z
		bm=bmesh.new()
		if self.own:
			me = bpy.context.object.data
			bm.from_mesh(me)
		else:
			v1=bm.verts.new((1,0,0))
			bmesh.ops.spin(bm, geom=bm.verts[:], axis=(0.0, 0.0, 1.0), cent=(0,0,0), dvec=(0,0,0), angle=math.radians(360), steps=self.verts, use_duplicate=0)
			bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.001)
		bm.faces.ensure_lookup_table()
		edges_new = bm.edges[:]
		for i in range(self.steps):
			ret=bmesh.ops.extrude_edge_only(bm, edges=edges_new)
			geom_new = ret["geom"]
			del ret
			verts_new = [ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
			edges_new = [ele for ele in geom_new if isinstance(ele, bmesh.types.BMEdge)]
			bmesh.ops.translate(bm, verts=verts_new, vec=(self.x1, self.y1, self.z1))
			bmesh.ops.scale(bm, verts=verts_new, vec=(self.scale_x, ys, zs))
			bmesh.ops.rotate(bm, verts=verts_new, cent=(self.x2, self.y2, self.z2), matrix=mathutils.Matrix.Rotation(math.radians(self.rotation_x), 3, 'X'))

		me=bpy.data.meshes.new("KTX_Circlex")
		bm.to_mesh(me)
		bm.free()

		me.use_auto_smooth = True
		if self.smooth_onoff:
			pols = me.polygons
			for p in pols:
				p.use_smooth = True
				
		scene=bpy.context.scene
		obj=bpy.data.objects.new("KTX_Circlex", me)
		scene.collection.objects.link(obj)
		if self.subs_onoff:
			obj.modifiers.new("subd", type='SUBSURF')
			obj.modifiers["subd"].levels = 2
			obj.modifiers["subd"].render_levels = 3
		if self.solid_onoff:
			obj.modifiers.new("solid", type='SOLIDIFY')
			obj.modifiers["solid"].thickness = self.sol_thickness

		return {'FINISHED'}


class KTXCIRCLEX_PT_Panel(bpy.types.Panel):
	bl_label = "KosteX Circlex"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_context = "objectmode"

	@classmethod
	def poll(self, context):
		return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
				(context.area.spaces.active.type == 'VIEW_3D'))

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		new_col = self.layout.column
		new_col().column().operator("ktxcirclex.sep", text="KTX Circlex")


classes = (
	KTXCIRCLEX_OT_Sep,
	KTXCIRCLEX_PT_Panel
)

def register():
	from bpy.utils import register_class

	for cls in classes:
		register_class(cls)


def unregister():
	from bpy.utils import unregister_class

	for cls in classes:
		unregister_class(cls)


if __name__ == "__main__":
	register()
