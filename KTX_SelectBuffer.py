# NOW HEAR THIS #
# This addon has been accepted in the blender addon contrib repositories #
# So you don't have to download this.. it's already in blender! #

bl_info = {
    "name": "KTX Selectbuffer",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 3),
    "blender": (2, 7, 0),
    "location": "View3D > Properties",
    "category": "3D View"}

import bpy
from bpy.types import Panel
from bpy.props import StringProperty

class Oldbuffer():
    data = []

class KTX_Selectbuffer_Mutate(bpy.types.Operator):
    bl_label = "select buffer mutate"
    bl_idname = "ktx.selectbuffer_mutate"
    bl_description = ("A.union(B) elements from both A and B\n"
                      "A.difference(B) elements in A but not in B\n"
                      "A.symmetric_difference(B) elements in either A or B but not both\n"
                      "A.intersection(B) elements common to A and B")

    operation = StringProperty()
    
    def execute(self, context):
        old_buffer=bpy.context.scene.ktx_selectbuffer
        emode = bpy.context.tool_settings.mesh_select_mode

        c_mode=bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        if emode[0]==True:
            all_vefs = bpy.context.object.data.vertices
        elif emode[1]==True:
            all_vefs = bpy.context.object.data.edges
        elif emode[2]==True:
            all_vefs = bpy.context.object.data.polygons

        selected_vefs = [vef for vef in all_vefs if vef.select]
        selected_vefs_buffer=[]
        for vef in selected_vefs:
            selected_vefs_buffer.append(vef.index)
        if self.operation == 'union':
            resulting_vefs = set(old_buffer.data).union(selected_vefs_buffer)
        elif self.operation == 'difference':
            resulting_vefs = set(old_buffer.data).difference(selected_vefs_buffer)
        elif self.operation == 'sym_difference':
            resulting_vefs = set(old_buffer.data).symmetric_difference(selected_vefs_buffer)
        elif self.operation == 'intersection':
            resulting_vefs = set(old_buffer.data).intersection(selected_vefs_buffer)
        elif self.operation == 'set':
            resulting_vefs = selected_vefs_buffer
        elif self.operation == 'clear':
            resulting_vefs = []
        old_buffer.data=resulting_vefs
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')         
        for vef in resulting_vefs:
             all_vefs[vef].select=True
        bpy.ops.object.mode_set(mode=c_mode)

        bpy.ops.ed.undo_push()

        return {'FINISHED'}


class KTX_Selectbuffer(bpy.types.Panel):
    bl_label = "KTX Selectbuffer"
    bl_idname = "ktx.selectbuffer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        obj = bpy.context.object
        layout = self.layout
        row = layout.row()
        col = row.column()
        if obj == None:
            col.label(text='Select/Create something first')
        else:
            if obj.type == 'MESH':
                c_mode = bpy.context.object.mode
                if c_mode == 'EDIT':
                    col.operator("ktx.selectbuffer_mutate", text="Set").operation = 'set'
                    col.operator("ktx.selectbuffer_mutate", text="Clear").operation = 'clear'
                    col.operator("ktx.selectbuffer_mutate", text="Union").operation = 'union'
                    col.operator("ktx.selectbuffer_mutate", text="Difference").operation = 'difference'
                    col.operator("ktx.selectbuffer_mutate", text="Symmetric Difference").operation = 'sym_difference'
                    col.operator("ktx.selectbuffer_mutate", text="Intersection").operation = 'intersection'
                else:
                    col.label(text='Enter EDIT Mode to use')
            else:
                col.label(text='Select a Mesh Object')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.ktx_selectbuffer = Oldbuffer()

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.ktx_selectbuffer

if __name__ == "__main__":
    register()
