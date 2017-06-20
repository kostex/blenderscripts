bl_info = {
    "name": "KTX Library Objects",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > KTX Library Objects",
    "description": "Add Single Selectable Object from KTX_Objects.blend File in your Scripts Folder",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.props import EnumProperty


class KTX_Lib_Objects(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_ktx_lib_object"
    bl_label = "Object"
    bl_options = {'REGISTER', 'UNDO'}

    def mode_options(self, context):
        import os
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            return [(ob, ob, "") for ob in data_from.objects]

    source = EnumProperty(items=mode_options,
                          name="Objects",
                          description="Objects found in Library",
                          )

    def execute(self, context):
        import os
        scn = bpy.context.scene
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')
        with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.objects = [
                name for name in data_from.objects if name.startswith(self.source)]
        for obj in data_to.objects:
            if obj is not None:
                scn.objects.link(obj)
        return {'FINISHED'}


class KTXLib_add_object_menu(bpy.types.Menu):
    """"Define the menu"""
    bl_idname = "KTXLib_add_object_menu"
    bl_label = "KTX Library Objects"

    def draw(self, context):
        import os
        filepath = os.path.join(os.path.sys.path[1], 'KTX_Objects.blend')

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for ob in data_from.objects:
                layout.operator(KTX_Lib_Objects.bl_idname,
                                text=ob, icon="MESH_ICOSPHERE").source = ob

# Registration


def menu_func(self, context):
    self.layout.menu(KTXLib_add_object_menu.bl_idname, icon='MOD_SCREW')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
