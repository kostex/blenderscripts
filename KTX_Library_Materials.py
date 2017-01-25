bl_info = {
    "name": "KTX Library Materials",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > KTX Library Materials",
    "description": "Add Single Selectable Material from KTX_Objects.blend File in your Scripts Folder",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }


import bpy
from bpy.props import EnumProperty


class KTX_Lib_Materials(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_ktx_lib_mat"
    bl_label = "Material"
    bl_options = {'REGISTER', 'UNDO'}

    def mat_options(self,context):
     import os
     filepath = os.path.join(os.path.sys.path[1],'KTX_Objects.blend')
     with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
      return [(mat,mat,"") for mat in data_from.materials]

    mats = EnumProperty(items = mat_options,
              name="Materials",
              description="Materials found in Library",
             )

    def execute(self, context):
     import os
     scn = bpy.context.scene
     filepath = os.path.join(os.path.sys.path[1],'KTX_Objects.blend')
     with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
      data_to.materials = [name for name in data_from.materials if name.startswith(self.mats)]
     for mat in data_to.materials:
      if mat is not None:
       ao = bpy.context.active_object
       if ao:
        if hasattr(ao.data, 'materials'):
         if len(ao.data.materials) == 0:
          ao.data.materials.append(mat)
         else:
          ao.material_slots[ao.active_material_index].material = mat
        else:
         filepath = os.path.join(filepath,'Materials')
         bpy.ops.wm.append(mat,filepath)
     return {'FINISHED'}


class KTXLib_add_mat_menu(bpy.types.Menu):
    """"Define the menu"""
    bl_idname = "KTXLib_add_mat_menu"
    bl_label = "KTX Library Materials"
    
    def draw(self,context):
     import os
     filepath = os.path.join(os.path.sys.path[1],'KTX_Objects.blend')

     layout = self.layout
     layout.operator_context = 'INVOKE_REGION_WIN'
     with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
      for mat in data_from.materials:
       layout.operator(KTX_Lib_Materials.bl_idname, text=mat,icon="MATERIAL").mats = mat


# Registration
def menu_func(self, context):
    self.layout.menu(KTXLib_add_mat_menu.bl_idname, icon='MATERIAL')

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
