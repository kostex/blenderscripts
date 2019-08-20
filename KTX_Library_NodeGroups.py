bl_info = {
	"name": "KTX Library NodeGroups",
	"author": "Roel Koster",
	"version": (1, 2),
	"blender": (2, 80, 0),
	"location": "View3D > Add > Mesh > KTX Library NodeGroups",
	"description": "Add Single Selectable NodeGroup from KTX_Objects.blend File in your Scripts Folder",
	"warning": "",
	"wiki_url": "",
	"category": "Add Mesh",
}


import bpy
from bpy.props import EnumProperty


class KTXLIB_OT_NodeGroups(bpy.types.Operator):
	"""Create a new Mesh Object"""
	bl_idname = "ktxlib.nodegroups"
	bl_label = "NodeGroup"
	bl_options = {'REGISTER', 'UNDO'}

	def ngr_options(self, context):
		import os
		filepath = os.path.join(bpy.utils.resource_path('USER'), 'scripts/addons/KTX_Objects.blend')
		with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
			return [(ngr, ngr, "") for ngr in data_from.node_groups]

	ngrs : EnumProperty(items=ngr_options,
						name="NodeGroups",
						description="NodeGroups found in Library",
						)

	def execute(self, context):
		import os
		scn = bpy.context.scene
		filepath = os.path.join(bpy.utils.resource_path('USER'), 'scripts/addons/KTX_Objects.blend')
		with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
			data_to.node_groups = [
				name for name in data_from.node_groups if name.startswith(self.ngrs)]
		for ngr in data_to.node_groups:
			if ngr is not None:
				ao = bpy.context.active_object
				if ao:
					if ao.material_slots.items() == []:
						new = bpy.data.materials.new('KTX_NewMat')
						new.use_nodes = True
						newmat = ao.data.materials.append(new)
					piet = ao.active_material.node_tree.nodes.new(
						"ShaderNodeGroup")
					piet.node_tree = data_to.node_groups[0]
		return {'FINISHED'}


class KTXLIB_MT_NodeGroupsMenu(bpy.types.Menu):
	""""Define the menu"""
	bl_idname = "KTXLIB_MT_NodeGroupsMenu"
	bl_label = "KTX Library NodeGroups"

	def draw(self, context):
		import os
		filepath = os.path.join(bpy.utils.resource_path('USER'), 'scripts/addons/KTX_Objects.blend')

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
			for ngr in data_from.node_groups:
				layout.operator(KTXLIB_OT_NodeGroups.bl_idname,
								text=ngr, icon="NODETREE").ngrs = ngr


# Registration
classes = (
	KTXLIB_OT_NodeGroups,
	KTXLIB_MT_NodeGroupsMenu
)

def menu_func(self, context):
	self.layout.menu(KTXLIB_MT_NodeGroupsMenu.bl_idname, icon='NODETREE')


def register():
	from bpy.utils import register_class

	for cls in classes:
		register_class(cls)
#	bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
	bpy.types.NODE_MT_add.append(menu_func)


def unregister():
	from bpy.utils import unregister_class

	for cls in classes:
		unregister_class(cls)
#	bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
	bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
	register()
