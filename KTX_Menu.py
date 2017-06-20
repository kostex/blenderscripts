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

if "bpy" in locals():
    import imp
#    imp.reload(KTXMenu_set_viewport_color)
# else:
#    import KTXMenu_set_viewport_color


bl_info = {
    "name": "KTX Custom 3DView Menu",
    "description": "Add a selection of commands to Alt-Q in 3D viewport",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 3, 2),
    "blender": (2, 7, 0),
    "location": "View3D > Properties",
    "warning": "",
    "wiki_url": "https://github.com/kostex/blenderscripts/",
#   "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "3D View"}


class KTXMoveToWorldOrigin(bpy.types.Operator):
    bl_label = "Move to World Origin"
    bl_description = "Move to world origin"
    bl_idname = "wm.ktx_move_to_world_origin"

    def execute(self, context):
        bpy.context.active_object.location = (0, 0, 0)
        return {'FINISHED'}


# Creates a menu for global 3D View
class KTXCustom3DViewMenu(bpy.types.Menu):
    bl_label = "KTX Menu"
    bl_idname = "view3D.ktx_custom_3dview_menu"

    # Set the menu operators and draw functions
    def draw(self, context):
        layout = self.layout

        layout.operator("view3D.view_all")
        layout.operator("view3d.view_selected")
        layout.operator("view3D.localview")
        layout.operator("view3D.view_center_cursor")
        layout.operator("view3d.view_center_pick")
        layout.operator("view3d.view_lock_to_active")
        layout.operator("view3d.view_lock_clear")
        layout.operator("view3d.fly")
        layout.operator("view3d.camera_to_view")
        layout.operator("view3d.viewnumpad")
        layout.separator()
        layout.operator("object.origin_set",
                        text="Geometry to Origin").type = 'GEOMETRY_ORIGIN'
        layout.operator("object.origin_set",
                        text="Origin to Geometry").type = 'ORIGIN_GEOMETRY'
        layout.operator("object.origin_set",
                        text="Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
        layout.operator("view3d.snap_cursor_to_selected")
        layout.operator("object.randomize_transform")
        layout.operator("object.align")
        layout.separator()
        layout.operator("wm.ktx_move_to_world_origin")

addon_keymaps = []


def register():
    bpy.utils.register_class(KTXCustom3DViewMenu)
    bpy.utils.register_class(KTXMoveToWorldOrigin)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
    kmi.properties.name = 'view3D.ktx_custom_3dview_menu'
    addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_class(KTXCustom3DViewMenu)
    bpy.utils.unregister_class(KTXMoveToWorldOrigin)
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del addon_keymaps[:]

if __name__ == "__main__":
    register()
