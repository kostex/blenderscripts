bl_info = {
    "name": "KTX KML to XYZ",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Properties",
    "description": "Imports KML CSV and converts to XYZ",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
import os, csv
import math, bmesh
from bpy.types import UIList, Operator, Menu, Panel, PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty, IntProperty, FloatProperty


def to_xyz(lat, lon, alt):
    x = math.cos(lat) * math.cos(lon) * alt
    y = math.cos(lat) * math.sin(lon) * alt
    z = math.sin(lat) * alt
    return x, y, z

def ktxkmltoxyz_init(self, context):
    scene = context.scene
    scene.ktx_filelist1.clear()
    try:
        entries = os.listdir(context.scene.ktx_kmltoxyz_path1)
        for entry in entries:
            if entry.endswith('.kml'):
                line=scene.ktx_filelist1.add()
                line.name = entry
    except:
        print("KML_KML_to_XYZ: File not found")

    return None

class KTXKMLTOXYZ_File(PropertyGroup):
    name : StringProperty(
        name="Filename",
        description="Filename",
        default="")
    enabled : BoolProperty()


class KTXKMLTOXYZ_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='FILE')
            layout.prop(item, "enabled", text="", index=index)
        elif self.layout.type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='FILE')


class KTXKMLTOXYZ_OT_Init(bpy.types.Operator):
    bl_label = "Initialize KML to XYZ"
    bl_idname = "ktxkmltoxyz.init"
    bl_description = "Initialise the addon"

    def execute(self, context):
        ktxkmltoxyz_init(self, context)
        return {'FINISHED'}

class KTXKMLTOXYZ_OT_Select(bpy.types.Operator):
    bl_label = "Select"
    bl_idname = "ktxkmltoxyz.select"
    bl_description = "Process the selected CSV File"

    def execute(self, context):
        scene = context.scene
        for item in scene.ktx_filelist1:
            if item.enabled:
            #    item = scene.ktx_filelist[scene.ktx_fileindex]
            #            print(item.name)
                mesh = bpy.data.meshes.new(item.name)
                obj = bpy.data.objects.new(item.name, mesh)
                scene.collection.objects.link(obj)
                bm = bmesh.new()
                with open(scene.ktx_kmltoxyz_path1+item.name) as csv_file:
                    fieldnames = ['Longitude','Latitude','Altitude']
                    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                    first = True
                    for row in csv_reader:
                        if first:
                            first = False
                        else:
                            lat = math.radians(float(row['Latitude']))
                            lon = math.radians(float(row['Longitude']))
                            alt = float(row["Altitude"])/scene.ktx_height_scale1 + scene.ktx_earth_size1
                            if alt == scene.ktx_earth_size1:
                                alt = scene.ktx_earth_size1 + 0.00001
                            x, y, z = to_xyz(lat, lon, scene.ktx_earth_size1)
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


class KTXKMLTOXYZ_PT_mainPanel(bpy.types.Panel):
    bl_label = "KTX KML to XYZ"
    bl_idname = "KTXKMLTOXYZ_PT_mainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.prop(scene,"ktx_earth_size1",text="Earth Size")
        layout.prop(scene,"ktx_height_scale1",text="Elevation Scale")
        layout.prop(scene,"ktx_kmltoxyz_path1",text="Path")
        layout.operator("ktxkmltoxyz.init", text="Refresh")
        layout.template_list('KTXKMLTOXYZ_UL_List', "", scene, "ktx_filelist1", scene, "ktx_fileindex1")
        layout.operator("ktxkmltoxyz.select", text="Select")


# Registration

classes = {
    KTXKMLTOXYZ_File,
    KTXKMLTOXYZ_UL_List,
    KTXKMLTOXYZ_PT_mainPanel,
    KTXKMLTOXYZ_OT_Init,
    KTXKMLTOXYZ_OT_Select,
}

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.ktx_earth_size1 = FloatProperty(name="Set Earth Size", default=100.0)
    bpy.types.Scene.ktx_height_scale1 = FloatProperty(name="Set Elevation Scale (kml=328100)", default=100000)
    bpy.types.Scene.ktx_kmltoxyz_path1 = StringProperty(description="Set Search Path for CSV", default="//Users/kostex/Aliases/SD_Downloads",subtype="DIR_PATH",update=ktxkmltoxyz_init)
    bpy.types.Scene.ktx_filelist1 = CollectionProperty(type = KTXKMLTOXYZ_File)
    bpy.types.Scene.ktx_fileindex1 = IntProperty(name="Index for ktx_filelist1", default = 0)



def unregister():
    from bpy.utils import unregister_class
    del bpy.types.Scene.ktx_fileindex1
    del bpy.types.Scene.ktx_filelist1
    del bpy.types.Scene.ktx_kmltoxyz_path1
    del bpy.types.Scene.ktx_earth_size1
    del bpy.types.Scene.ktx_height_scale1

    for cls in classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()
    ktxkmltoxyz_init()
