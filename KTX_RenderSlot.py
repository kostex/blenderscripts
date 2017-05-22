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
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty
from sys import platform
from bpy.app.handlers import persistent


bl_info = {
    "name": "KTX RenderSlot",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 2, 4),
    "blender": (2, 7, 0),
    "location": "Properties Editor > Render > Render",
    "category": "Render"}


nullpath = '/nul' if platform == 'win32' else '/dev/null'


class OccupiedSlots:
    data = '00000000'


class KTX_RenderSlot(Operator):
    bl_label = "Select Render Slot"
    bl_idname = "ktx.renderslot"
    bl_description = ("Select Render Slot\n"
                      "Note: Dot next to number means slot has image data\n"
                      "[x] is active slot")

    number = IntProperty()

    def execute(self, context):
        bpy.data.images['Render Result'].render_slots.active_index = self.number

        return {'FINISHED'}


@persistent
def checkslots(scene):
    img = bpy.data.images['Render Result']
    active = img.render_slots.active_index
    slots = ''
    for i in range(8):
        img.render_slots.active_index = i
        try:
            img.save_render(nullpath)
            slots = slots + '1'
        except:
            slots = slots + '0'

    bpy.context.scene.ktx_occupied_render_slots.data = slots
    if bpy.context.scene.ktx_auto_advance_slot:
        active += 1
        if active == 8:
            active = 0
    img.render_slots.active_index = active


def ui(self, context):
    scn = context.scene
    layout = self.layout
    row = layout.row(align=True)
    row.alignment = 'LEFT'
    try:
        active = bpy.data.images['Render Result'].render_slots.active_index
        row.prop(scn, 'ktx_auto_advance_slot', 'Auto Advance')
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        for i in range(8):
            is_active = bool(i == active)
            test_active = bool(scn.ktx_occupied_render_slots.data[i] == '1')
            icons = "LAYER_ACTIVE" if test_active else "BLANK1"
            label = "[{}]".format(str(i + 1)) if is_active else str(i + 1)
            row.operator('ktx.renderslot', text=label, icon=icons).number = i
    except:
        row.label(text="No Render Slots available yet", icon="INFO")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.RENDER_PT_render.prepend(ui)
    bpy.types.Scene.ktx_auto_advance_slot = BoolProperty(default=False, description="Auto Advance to Next Slot after a Render")
    bpy.types.Scene.ktx_occupied_render_slots = OccupiedSlots

    bpy.app.handlers.render_post.append(checkslots)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.RENDER_PT_render.remove(ui)
    del bpy.types.Scene.ktx_occupied_render_slots
    del bpy.types.Scene.ktx_auto_advance_slot

    bpy.app.handlers.render_post.remove(checkslots)


if __name__ == "__main__":
    register()
