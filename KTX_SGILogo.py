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
import bmesh


bl_info = {
    "name": "KTX SGI Logo",
    "description": "Create a Silicon Graphics Logo",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > Create",
    "warning": "",
    "wiki_url": "https://github.com/kostex/blenderscripts/",
#    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "3D View"}


EDIT_MODES = {'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE',
              'EDIT_METABALL', 'EDIT_TEXT', 'EDIT_ARMATURE'}


class KTXSGI_OT_Execute(bpy.types.Operator):
    bl_idname = "ktxsgi.execute"
    bl_label = "KTX Create SGI Logo"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "Creates the logo"

    short : bpy.props.FloatProperty(name="Gap",
        description="Gap between lines",
        default=1.0, min=0.01, max=10.0)

    long : bpy.props.FloatProperty(name="Length",
        description="Line Length",
        default=5.0, min=1.0, max=50.0)

    fillet : bpy.props.BoolProperty(name="Fillet",
        description="Fillet All Verts",
        default=True)

    fillet_rad : bpy.props.FloatProperty(name="Radius",
        description="Fillet Radius",
        default=0.5, min=0.0, max=5.0)

    fillet_segs : bpy.props.IntProperty(name="Segments",
        description="Fillet Radius Segments",
        default=3, min=1, max=10)

    curve : bpy.props.BoolProperty(name="Curve",
        description="On: Create Curve, Off: Create Edges",
        default=True)

    bevel_depth : bpy.props.FloatProperty(name="Depth",
        description="Bevel Depth",
        default=0.5)

    bevel_resolution : bpy.props.IntProperty(name="Resolution",
        description="Bevel Resolution",
        default=8)

    smooth : bpy.props.BoolProperty(name="Smoothing",
        description="Enable Smoothing",
        default=True)

    @classmethod
    def poll(self, context):
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'short', text="Gap between lines")
        col.prop(self, 'long', text="Line length")
        col.separator()
        col.prop(self, 'fillet', text="Fillet Verts")
        if self.fillet:
            col.prop(self, 'fillet_rad', text="Radius")
            col.prop(self, 'fillet_segs', text="Segments")
        col.separator()
        col.prop(self, 'curve', text="Create Curve")
        if self.curve:
            col.prop(self, 'bevel_depth', text="Bevel Depth")
            col.prop(self, 'bevel_resolution', text="Bevel Resolution")
        col.separator()
        col.prop(self, 'smooth', text="Smoothing")


    def execute(self, context):
        import math
        import bmesh

        bm=bmesh.new()
        me=bpy.data.meshes.new('KTX_SGI_Logo')
        ob=bpy.data.objects.new('KTX_SGI_Logo',me)
        bpy.context.scene.collection.objects.link(ob)

        mid = (self.long + self.short)/2

        verts = [
        (mid-self.short,mid,0),
        (-mid+self.short, mid,0),
        (-mid+self.short, -mid+self.short,0),
        (mid,-mid+self.short,0),
        (mid,mid-self.short,0),
        (mid,mid-self.short,self.long),
        (mid,-mid,self.long),
        (mid,-mid,self.short),
        (-mid+self.short,-mid,self.short),
        (-mid+self.short,-mid,self.short+self.long),
        (mid-self.short,-mid,self.short+self.long),
        (mid-self.short,mid-self.short,self.short+self.long),
        (-mid,mid-self.short,self.short+self.long),
        (-mid,-mid+self.short,self.short+self.long),
        (-mid,-mid+self.short,self.short),
        (-mid,mid,self.short),
        (-mid,mid,self.long),
        (mid-self.short,mid,self.long)
        ]

        for i in range(0,18):
          bm.verts.new(verts[i])
          bm.verts.ensure_lookup_table()
          if i>0:
            bm.edges.new((bm.verts[-2],bm.verts[-1]))

        bm.edges.new((bm.verts[0],bm.verts[-1]))
        bm.to_mesh(me)
        bpy.context.view_layer.objects.active=ob
        if self.fillet:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.bevel(vertex_only=True, offset=self.fillet_rad, segments=self.fillet_segs)
            bpy.ops.object.editmode_toggle()
        if self.curve:
            ob.select_set(True)
            bpy.ops.object.convert(target='CURVE')
            bpy.data.curves[ob.data.name].bevel_depth=self.bevel_depth
            bpy.data.curves[ob.data.name].bevel_resolution=self.bevel_resolution
        if self.smooth:
            bpy.ops.object.shade_smooth()
            me.use_auto_smooth = True
        bm.free()
        return {'FINISHED'}


class KTXSGI_PT_Panel(bpy.types.Panel):
    bl_label = "KosteX SGI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        new_col = self.layout.column
        new_col().column().operator("ktxsgi.execute", text="KTX SGI Logo")


classes = (
    KTXSGI_OT_Execute,
    KTXSGI_PT_Panel
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
