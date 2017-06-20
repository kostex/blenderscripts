bl_info = {
    "name": "KTX Library NodeGroups",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > KTX Library NodeGroups",
    "description": "Add Single Selectable NodeGroup from KTX_Objects.blend File in your Scripts Folder",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.props import EnumProperty


class KTX_Lib_NodeGroups(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_ktx_lib_ngr"
    bl_label = "NodeGroup"
    bl_options = {'REGISTER', 'UNDO'}

    def ngr_options(self, context):
        import os
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            return [(ngr, ngr, "") for ngr in data_from.node_groups]

    ngrs = EnumProperty(items=ngr_options,
                        name="NodeGroups",
                        description="NodeGroups found in Library",
                        )

    def execute(self, context):
        import os
        scn = bpy.context.scene
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')
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


class KTXLib_add_ngr_menu(bpy.types.Menu):
    """"Define the menu"""
    bl_idname = "KTXLib_add_ngr_menu"
    bl_label = "KTX Library NodeGroups"

    def draw(self, context):
        import os
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for ngr in data_from.node_groups:
                layout.operator(KTX_Lib_NodeGroups.bl_idname,
                                text=ngr, icon="NODETREE").ngrs = ngr


# Registration
def menu_func(self, context):
    self.layout.menu(KTXLib_add_ngr_menu.bl_idname, icon='NODETREE')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)
    bpy.types.NODE_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    bpy.types.NODE_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()
