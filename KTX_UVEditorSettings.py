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
import time
from datetime import datetime
from bpy.types import Menu, Panel
from bpy.props import StringProperty, BoolProperty


bl_info = {
    "name": "KTX UV Editor Settings",
    "description": "Quick way to change grid/colors/uv",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Image Editor > KTX",
    "warning": "",
    "wiki_url": "https://github.com/kostex/blenderscripts/",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Prefs"}



class KTXUVSETTINGS_PT_mainPanel(bpy.types.Panel):
    bl_label = "KTX UV Settings"
    bl_idname = "KTXUVSETTINGS_PT_mainPanel"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "KTX"

    def draw(self, context):
        scene = context.scene
        obj = context.object
        layout = self.layout

        layout.label(text="UVs")
        layout.prop(context.space_data.uv_editor,"show_texpaint", text='Show UV Overlay')
        layout.prop(context.preferences.themes['Default'].image_editor,"uv_shadow", text='UV Color')
        layout.label(text="Grid")
        layout.prop(context.preferences.themes['Default'].user_interface,"transparent_checker_primary", text="Checker Pri")
        layout.prop(context.preferences.themes['Default'].user_interface,"transparent_checker_secondary", text="Checker Sec")
        layout.prop(context.preferences.themes['Default'].user_interface,"transparent_checker_size", text="Checker Size")


classes = (
    KTXUVSETTINGS_PT_mainPanel,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()
