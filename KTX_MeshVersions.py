bl_info = {
    "name": "KTX Mesh Versions",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 1),
    "blender": (2, 7, 0),
    "location": "View3D > Properties",
    "category": "3D View"}

import bpy,time
from datetime import datetime
from bpy.types import Menu, Panel
from bpy.props import StringProperty, BoolProperty, IntProperty


class KTX_MeshSelect(bpy.types.Operator):
    bl_label = "select mesh"
    bl_idname = "ktx.meshversions_select"
    
    m_index = StringProperty()
    
    def execute(self, context):
        c_mode=bpy.context.object.mode
        if c_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        obj = context.object
        obj.data = bpy.data.meshes[self.m_index]
        bpy.ops.object.mode_set(mode=c_mode)
        return {'FINISHED'}

class KTX_MeshFake(bpy.types.Operator):
    bl_label = "mesh fake user"
    bl_idname = "ktx.meshversions_fakeuser"
    
    m_index = StringProperty()
    
    def execute(self, context):
        me=bpy.data.meshes
        if me[self.m_index].use_fake_user:
            me[self.m_index].use_fake_user=False
        else:
            me[self.m_index].use_fake_user=True

        return {'FINISHED'}


class KTX_MeshCreate(bpy.types.Operator):
    bl_label = "Create Mesh Version"
    bl_idname = "ktx.meshversions_create"
    
    def execute(self, context):
        defpin = bpy.context.scene.ktx_defpin
        obj = context.object
        if obj.type=='MESH':
            obj_name=obj.name
            c_mode=bpy.context.object.mode
            me=obj.data
            if c_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            new_mesh=me.copy()
            (dt, micro) = datetime.now().strftime('_%Y-%m-%d:%H:%M:%S#%f').split('#')
            dt = "%s#%04d" % (dt, int(micro) / 1000)
            new_mesh.name=obj_name+dt
            obj.data=new_mesh
            obj.data.use_fake_user=defpin
            bpy.ops.object.mode_set(mode=c_mode)

        return {'FINISHED'}


class KTX_Mesh_Versions(bpy.types.Panel):
    bl_label = "KTX Mesh Versions"
    bl_idname = "ktx.meshversions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        scene = context.scene
        obj = context.object

        layout = self.layout
        row = layout.row()
        col = row.column()
        if obj == None:
            col.label(text='Select/Create something first')
        else:
            if obj.type == 'MESH':
                col.operator("ktx.meshversions_create", text="Create a Version of Current Object")
                col.prop(scene, "ktx_defpin")
                box = layout.box()
                box.label("Versions of Active Object: " + obj.name)
                len_obj=len(obj.name)
                for m in bpy.data.meshes:
                    len_m=len(m.name)
                    if m.name[:len_obj] == obj.name and (len(m.name) == len_obj+25 or len(m.name) == len_obj):
                        row = box.row()
                        row.operator("ktx.meshversions_select",text=m.name).m_index = m.name
                        if bpy.data.meshes[m.name].use_fake_user:
                            row.operator("ktx.meshversions_fakeuser",text="",icon="PINNED").m_index = m.name
                        else:
                            row.operator("ktx.meshversions_fakeuser",text="",icon="UNPINNED").m_index = m.name
            else:
                col.label(text='Select a Mesh Object')


def register():
    bpy.types.Scene.ktx_defpin = bpy.props.BoolProperty(name="Auto Pinning", description="When Adding Default Pin On/Off", default=False)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.ktx_defpin

if __name__ == "__main__":
    register()
