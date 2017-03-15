bl_info = {
    "name": "KTX RenderSlot",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 0),
    "blender": (2, 7, 0),
    "location": "Properties Editor > Render > Render",
    "category": "Render"}

import bpy
from bpy.props import IntProperty

class KTX_RenderSlot(bpy.types.Operator):
    bl_label = "Select Render Slot"
    bl_idname = "ktx.renderslot"
    bl_description = ("Select Render Slot")

    number = IntProperty()
    
    def execute(self, context):
        bpy.data.images['Render Result'].render_slots.active_index=self.number
        return {'FINISHED'}


def ui(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='EXPAND'
        a=bpy.data.images['Render Result'].render_slots.active_index+1
        row.label('Current Render Slot: ' + str(a))
        row = layout.row(align=True)
        row.alignment='EXPAND'
        row.operator('ktx.renderslot', text='1').number=0
        row.operator('ktx.renderslot', text='2').number=1
        row.operator('ktx.renderslot', text='3').number=2
        row.operator('ktx.renderslot', text='4').number=3
        row.operator('ktx.renderslot', text='5').number=4
        row.operator('ktx.renderslot', text='6').number=5
        row.operator('ktx.renderslot', text='7').number=6
        row.operator('ktx.renderslot', text='8').number=7


def register():
    bpy.utils.register_module(__name__)
    bpy.types.RENDER_PT_render.prepend(ui)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.RENDER_PT_render.remove(ui)
if __name__ == "__main__":
    register()
