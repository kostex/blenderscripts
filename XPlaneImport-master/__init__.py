#---------------------------------------------------------------------------
#
#  Import an X-Plane .obj file into Blender 2.9x
#
# Original: Dave Prue <dave.prue@lahar.net>
# Adapted: Roel Koster <koelooptiemanna@gmail.com>
#
# MIT License
#
# Copyright (c) 2017 David C. Prue
# Copyright (c) 2021 Roel Koster
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#---------------------------------------------------------------------------

bl_info = {
    "name": "Import X-Plane OBJ",
    "author": "Roel Koster <koelooptiemanna@gmail.com",
    "version": (1,0,3),
    "blender": (2,80,0),
    "api": 36273,
    "location": "File > Import/Export > XPlane",
    "description": "Import X-Plane obj files",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export"
}


import bpy
from . import XP_import


def menu_func(self, context):
    self.layout.operator(XP_import.XPlaneImport.bl_idname, text="X-Plane Object (.obj)")

def register():
    from bpy.utils import register_class
    register_class(XP_import.XPlaneImport)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
    from bpy.utils import unregister_class
    unregister_class(XP_import.XPlaneImport)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
    register()
