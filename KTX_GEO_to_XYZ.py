bl_info = {
    "name": "KTX GEO to XYZ",
    "author": "Roel Koster",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Properties",
    "description": "Imports GEO CSV and converts to XYZ",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
import os, csv
import math, bmesh
from bpy.types import UIList, Operator, Menu, Panel, PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty, IntProperty


def to_xyz(lat, lon, alt):
    x = math.cos(lat) * math.cos(lon) * alt
    y = math.cos(lat) * math.sin(lon) * alt
    z = math.sin(lat) * alt
    return x, y, z

def ktxgeotoxyz_init(self, context):
    scene = context.scene
    scene.ktx_filelist.clear()
    try:
        entries = os.listdir(context.scene.ktx_geotoxyz_path)
        for entry in entries:
            if entry.endswith('.csv'):
                line=scene.ktx_filelist.add()
                line.name = entry
    except:
        print("KTX_GEO_to_XYZ: File not found")

    return None

class KTXGEOTOXYZ_File(PropertyGroup):
    name : StringProperty(
        name="Filename",
        description="Filename",
        default="")
    enabled : BoolProperty()


class KTXGEOTOXYZ_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='FILE')
            layout.prop(item, "enabled", text="", index=index)
        elif self.layout.type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='FILE')


class KTXGEOTOXYZ_OT_Init(bpy.types.Operator):
    bl_label = "Initialize GEO to XYZ"
    bl_idname = "ktxgeotoxyz.init"
    bl_description = "Initialise the addon"

    def execute(self, context):
        ktxgeotoxyz_init(self, context)
        return {'FINISHED'}

class KTXGEOTOXYZ_OT_Select(bpy.types.Operator):
    bl_label = "Select"
    bl_idname = "ktxgeotoxyz.select"
    bl_description = "Process the selected CSV File"

    def execute(self, context):
        scene = context.scene
        for item in scene.ktx_filelist:
            if item.enabled:
            #    item = scene.ktx_filelist[scene.ktx_fileindex]
            #            print(item.name)
                mesh = bpy.data.meshes.new(item.name)
                obj = bpy.data.objects.new(item.name, mesh)
                scene.collection.objects.link(obj)
                bm = bmesh.new()
                with open(scene.ktx_geotoxyz_path+item.name) as csv_file:
                    fieldnames = ['Timestamp','UTC','Callsign','Position','Altitude','Speed','Direction']
                    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                    first = True
                    for row in csv_reader:
                        if first:
                            first = False
                        else:
                            posdata = row['Position'].split(",")
                            lat = math.radians(float(posdata[0]))
                            lon = math.radians(float(posdata[1]))
                            alt = float(row["Altitude"])/500000 + 10
                            if alt == 10:
                                alt = 10.00001
                            x, y, z = to_xyz(lat, lon, 10)
                            bm.verts.new((x,y,z))
                            x, y, z = to_xyz(lat, lon, alt)
                            bm.verts.new((x,y,z))
                bm.verts.ensure_lookup_table()
                for i in range(3,len(bm.verts)-1,2):
                    face = [bm.verts[i-3],bm.verts[i-2],bm.verts[i],bm.verts[i-1]]
                    bm.faces.new(face)

                bm.to_mesh(mesh)
                obj.data.update()
        return {'FINISHED'}


class KTXGEOTOXYZ_PT_mainPanel(bpy.types.Panel):
    bl_label = "KTX GEO to XYZ"
    bl_idname = "KTXGEOTOXYZ_PT_mainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.prop(scene,"ktx_geotoxyz_path",text="Path")
        layout.operator("ktxgeotoxyz.init", text="Refresh")
        layout.template_list('KTXGEOTOXYZ_UL_List', "", scene, "ktx_filelist", scene, "ktx_fileindex")
        layout.operator("ktxgeotoxyz.select", text="Select")


# Registration

classes = {
    KTXGEOTOXYZ_File,
    KTXGEOTOXYZ_UL_List,
    KTXGEOTOXYZ_PT_mainPanel,
    KTXGEOTOXYZ_OT_Init,
    KTXGEOTOXYZ_OT_Select,
}

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.ktx_geotoxyz_path = StringProperty(description="Set Search Path for CSV", default="//Users/kostex/Aliases/SD_Downloads",subtype="DIR_PATH",update=ktxgeotoxyz_init)
    bpy.types.Scene.ktx_filelist = CollectionProperty(type = KTXGEOTOXYZ_File)
    bpy.types.Scene.ktx_fileindex = IntProperty(name="Index for ktx_filelist", default = 0)



def unregister():
    from bpy.utils import unregister_class
    del bpy.types.Scene.ktx_fileindex
    del bpy.types.Scene.ktx_filelist
    del bpy.types.Scene.ktx_geotoxyz_path

    for cls in classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()
    ktxgeotoxyz_init()
