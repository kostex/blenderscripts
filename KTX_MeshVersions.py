bl_info = {
    "name": "KTX Mesh Versions UIList",
    "author": "Roel Koster, @koelooptiemanna, irc:kostex",
    "version": (1, 1, 2),
    "blender": (2, 7, 0),
    "location": "View3D > Properties",
    "category": "3D View"}

import bpy,time
from datetime import datetime
from bpy.types import Menu, Panel
from bpy.props import StringProperty, BoolProperty, IntProperty


class KTX_MeshList(bpy.types.UIList):

    show_linked_only = bpy.props.BoolProperty(name="Only Show Linked", default=True, options=set(), description="Show all or belonging meshes")

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        self.use_filter_show = True
        self.use_filter_invert = False

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row=layout.row(align=True)
            row.operator("ktx.meshversions_select",text="",icon='RIGHTARROW').m_index = item.name
            row.prop(item,"name", text="", icon='MESH_DATA')
            if item.users == 0:
                row.operator("ktx.meshversions_remove", text="", icon='X').m_index = item.name
            icon='PINNED' if item.use_fake_user else 'UNPINNED'
            row.prop(item, "use_fake_user", text="", icon=icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon = 'MESH_DATA')

    def draw_filter(self, context, layout):
        row=layout.row()
#        row.prop(self, "filter_name", text="")
        row.prop(self,"show_linked_only", text="", icon="FILTER")
        if context.object != None:
            if context.object.type=='MESH':
                if context.object.ktx_object_id=='-':
                    row.operator("ktx.meshversions_init")
                else:
                    row.operator("ktx.meshversions_create")
            else:
                row.label("Cleanup Mode")
        else:
            row.label("Cleanup Mode")

    def filter_items(self, context, data, propname):
        helper = bpy.types.UI_UL_list
        collection = getattr(data, propname)
        flt_flags = [self.bitflag_filter_item] * len(collection)
        if context.object != None:
            if self.show_linked_only:
                self.filter_name=context.object.ktx_object_id
                flt_flags = helper.filter_items_by_name(self.filter_name, self.bitflag_filter_item, collection, "ktx_mesh_id", reverse=False)
            
        flt_neworder=[]

        return flt_flags, flt_neworder


class KTX_MeshInit(bpy.types.Operator):
    bl_label = "Initialise Mesh Versioning"
    bl_idname = "ktx.meshversions_init"
    bl_description = "Initialise the current object to support versioning"

    def execute(self, context):
        unique_id=str(time.time())
        context.object.data.ktx_mesh_id=context.object.ktx_object_id=unique_id
        return {'FINISHED'}

class KTX_MeshSelect(bpy.types.Operator):
    bl_label = "Select Mesh"
    bl_idname = "ktx.meshversions_select"
    bl_description = "Link the selected mesh to the current object"
    
    m_index = StringProperty()
    
    def execute(self, context):
        c_mode=bpy.context.object.mode
        if c_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        obj = context.object
        obj.data = bpy.data.meshes[self.m_index]
        bpy.ops.object.mode_set(mode=c_mode)
        return {'FINISHED'}

class KTX_MeshRemove(bpy.types.Operator):
    bl_label = "Remove Mesh"
    bl_idname = "ktx.meshversions_remove"
    bl_description = "Remove/Delete the selected mesh"
    
    m_index = StringProperty()
    
    def execute(self, context):
        bpy.data.meshes.remove(bpy.data.meshes[self.m_index])
        return {'FINISHED'}

class KTX_MeshCreate(bpy.types.Operator):
    bl_label = "Create Mesh Version"
    bl_idname = "ktx.meshversions_create"
    bl_description=("Create a copy of the mesh data of the current object\n"
                    "and set it as active")

    def execute(self, context):
        defpin = bpy.context.scene.ktx_defpin
        obj = context.object
        if obj.type=='MESH':
            c_mode=bpy.context.object.mode
            me=obj.data
            if c_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            new_mesh=me.copy()
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
        if obj != None:
            if obj.type == 'MESH':
                layout.label("Assigned mesh: " + obj.data.name)
        layout.template_list("KTX_MeshList", "", bpy.data, "meshes", context.scene, "ktx_list_index")
        

def register():
    bpy.types.Object.ktx_object_id = bpy.props.StringProperty(name="KTX Object ID", description="Unique ID to 'link' one object to multiple meshes",default='-')
    bpy.types.Mesh.ktx_mesh_id = bpy.props.StringProperty(name="KTX Mesh ID", description="Unique ID to 'link' multiple meshes to one object",default='_')
    bpy.types.Scene.ktx_defpin = bpy.props.BoolProperty(name="Auto Pinning", description="When creating a copy set pinning to ON automatically (FAKE_USER=TRUE)", default=False)
    bpy.types.Scene.ktx_list_index = bpy.props.IntProperty(name="Index for KTX_MeshList", default = 0)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Mesh.ktx_mesh_id
    del bpy.types.Object.ktx_object_id
    del bpy.types.Scene.ktx_defpin
    del bpy.types.Scene.ktx_list_index
if __name__ == "__main__":
    register()
