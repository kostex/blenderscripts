bl_info = {
    "name": "KTX RenderSlot",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 1),
    "blender": (2, 7, 0),
    "location": "Properties Editor > Render > Render",
    "category": "Render"}

import bpy,os
from bpy.props import IntProperty
from sys import platform

nullpath = '/nul' if platform == 'win32' else '/dev/null'

class SlotBuffer():
    data='00000000'

class KTX_RenderSlot(bpy.types.Operator):
    bl_label = "Select Render Slot"
    bl_idname = "ktx.renderslot"
    bl_description = "Select Render Slot"

    number = IntProperty()
    
    def execute(self, context):
        bpy.data.images['Render Result'].render_slots.active_index=self.number
        return {'FINISHED'}

class KTX_CheckSlots(bpy.types.Operator):
    bl_label = "Check Render Slots"
    bl_idname = "ktx.checkslots"
    bl_description = "Check Render Slots Occupation"

    def execute(self, context):
        img = bpy.data.images['Render Result']
        active = img.render_slots.active_index
        slots = ''
        i = 0
        for i in range(8):
            img.render_slots.active_index= i
            try:
                img.save_render(nullpath)
                slots = slots + '1'
            except:
                slots = slots + '0'

        bpy.context.scene.ktx_occupied_render_slots.data=slots
        img.render_slots.active_index= active
        return {'FINISHED'}


def ui(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment='LEFT'
        try:
            active=bpy.data.images['Render Result'].render_slots.active_index+1
            row.operator('ktx.checkslots',text='',icon='QUESTION')
            row.label('Current Render Slot: ' + str(active))
            row = layout.row(align=True)
            row.alignment='EXPAND'
            i = 0
            for i in range(8):
                if bpy.context.scene.ktx_occupied_render_slots.data[i] == '1':
                    row.operator('ktx.renderslot', text=str(i+1)+'*').number=i
                else:
                    row.operator('ktx.renderslot', text=str(i+1)).number=i
        except:
            row.label('No Render Slots available yet')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.RENDER_PT_render.prepend(ui)
    bpy.types.Scene.ktx_occupied_render_slots = SlotBuffer()

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.RENDER_PT_render.remove(ui)
    del bpy.types.Scene.ktx_occupied_render_slots

if __name__ == "__main__":
    register()
