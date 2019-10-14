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

import bpy,re
from bpy.types import Panel
from bpy.props import StringProperty


bl_info = {
	"name": "KTX Image/Font Paths",
	"description": "Show/Edit All Image and Font Paths Directly",
	"author": "Roel Koster, @koelooptiemanna, irc:kostex",
	"version": (1, 0, 2),
	"blender": (2, 80, 0),
	"location": "Properties > Scene",
	"warning": "",
	"wiki_url": "https://github.com/kostex/blenderscripts/",
	"tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
	"category": "Scene"}


class KTXIMAGEFONTPATHS_OT_RemoveSlashDots(bpy.types.Operator):
	"""Remove all \.."""
	bl_idname = "ktximagefontpaths.removeslashdots"
	bl_label = "Remove Slashdots"

	def execute(self, context):
		for i in bpy.data.images:
			i.filepath=re.sub('\.\./','',i.filepath)
		for i in bpy.data.fonts:
			if i.filepath != '<builtin>':
				i.filepath=re.sub('\.\./','',i.filepath)
		return {'FINISHED'}


class KTXIMAGEFONTPATHS_OT_Regex(bpy.types.Operator):
	"""Search and replace paths with regex"""
	bl_idname = "ktximagefontpaths.regex"
	bl_label = "Search/Replace"

	def execute(self, context):
		scene = context.scene
		for i in bpy.data.images:
			i.filepath=re.sub(scene.ktx_searchfield, scene.ktx_replacefield,i.filepath)
		for i in bpy.data.fonts:
			if i.filepath != '<builtin>':
				i.filepath=re.sub(scene.ktx_searchfield, scene.ktx_replacefield,i.filepath)
		return {'FINISHED'}


class KTXIMAGEFONTPATHS_PT_Panel(bpy.types.Panel):
	"""Creates a Panel in the scene context of the properties editor"""
	bl_label = "Image/Font Paths"
	bl_idname = "KTXIMAGEFONTPATHS_PT_Panel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def draw(self, context):
		layout = self.layout

		scene = context.scene

		layout.label(text=" Images:")

		for i in bpy.data.images:
			if i.filepath != '':
				layout.prop(i,"filepath", text="")

		layout.label(text=" Fonts:")

		for f in bpy.data.fonts:
			if f.filepath != '<builtin>':
				layout.prop(f,"filepath", text="")

		layout.label(text=" Tools:")

		layout.operator("ktximagefontpaths.removeslashdots")
		layout.prop(scene, "ktx_searchfield", text="Search")
		layout.prop(scene, "ktx_replacefield", text="Replace")
		layout.operator("ktximagefontpaths.regex")

classes = (
	KTXIMAGEFONTPATHS_OT_RemoveSlashDots,
	KTXIMAGEFONTPATHS_OT_Regex,
	KTXIMAGEFONTPATHS_PT_Panel
)

def register():
	bpy.types.Scene.ktx_searchfield = StringProperty(default='', description="Search for (regex)")
	bpy.types.Scene.ktx_replacefield = StringProperty(default='', description="Replace with (regex)")
	from bpy.utils import register_class

	for cls in classes:
		register_class(cls)


def unregister():
	del bpy.types.Scene.ktx_searchfield
	del bpy.types.Scene.ktx_replacefield
	from bpy.utils import unregister_class

	for cls in classes:
		unregister_class(cls)


if __name__ == "__main__":
	register()
