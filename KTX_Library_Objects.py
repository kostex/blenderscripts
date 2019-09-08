bl_info = {
    "name": "KTX Library Objects",
    "author": "Roel Koster",
    "version": (1, 4, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > KTX Library Objects",
    "description": "Add Single Selectable Object from KTX_Objects.blend File in your Scripts Folder",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.props import EnumProperty


class KTXLIB_OT_Objects(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "ktxlib.objects"
    bl_label = "Object"
    bl_options = {'REGISTER', 'UNDO'}

    def mode_options(self, context):
        import os
        filepath = os.path.normpath('/Users/kostex/Aliases/Dropbox/_AppSetLinks/Blender/Libraries/KTX_Objects.blend')
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            return [(ob, ob, "") for ob in data_from.objects]

    source : EnumProperty(items=mode_options,
                          name="Objects",
                          description="Objects found in Library",
                          )

    def execute(self, context):
        import os
        scn = bpy.context.scene
        filepath = os.path.normpath('/Users/kostex/Aliases/Dropbox/_AppSetLinks/Blender/Libraries/KTX_Objects.blend')
        with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
            data_to.objects = [
                name for name in data_from.objects if name == self.source]
        for obj in data_to.objects:
            if obj is not None:
                scn.collection.objects.link(obj)
                obj.location=bpy.data.scenes[0].cursor.location
        return {'FINISHED'}


class KTXLIB_MT_ObjectsMenu(bpy.types.Menu):
    """"Define the menu"""
    bl_idname = "KTXLIB_MT_ObjectsMenu"
    bl_label = "KTX Library Objects"

    def draw(self, context):
        import os
        filepath = os.path.normpath('/Users/kostex/Aliases/Dropbox/_AppSetLinks/Blender/Libraries/KTX_Objects.blend')

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for ob in data_from.objects:
                layout.operator(KTXLIB_OT_Objects.bl_idname,
                                text=ob, icon="MESH_ICOSPHERE").source = ob


# Registration
classes = (
    KTXLIB_OT_Objects,
    KTXLIB_MT_ObjectsMenu
)

def menu_func(self, context):
    self.layout.menu(KTXLIB_MT_ObjectsMenu.bl_idname, icon='MOD_SCREW')


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
