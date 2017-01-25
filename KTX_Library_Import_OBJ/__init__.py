bl_info = {
        "name": "KTX Library Import .OBJ",
		"version": (2, 0),
		"blender": (2, 67, 0),
		"location": "View3D > Add > Mesh > KTX Library Import .OBJ",
		"description": "Asset Library of the .obj files in the addon's folder",
        "category": "Add Mesh"}        
 
import bpy
import os

folderDict = {}


# Fetching the path to Blender's addons directory
path_to_addons = os.path.sys.path[1]
if 'addons' not in path_to_addons:
    path_to_addons = os.path.sys.path[0]

# Full path to "\addons\add_mesh_asset_library\assets\" -directory
# full_path_to_directory = os.path.join(path_to_addons, 'add_mesh_asset_library', 'assets')
full_path_to_directory = '/Volumes/DataPartition/DataDocuments/Blender/_Obj'

class opOBJImporter( bpy.types.Operator ):
    filename = bpy.props.StringProperty()
    bl_idname = "bpt.obj_importer"
    bl_label = "Import .OBJ file"
     
    def execute( self, context ):
        bpy.ops.import_scene.obj(filepath=self.filename)
        return {'FINISHED'}

class subMenuClass(bpy.types.Menu):
    bl_label = "Asset Library Submenu"
    bl_idname = "asset_library_submenu"
    
    # Set the menu operators and draw functions
    def draw(self, context):
        layout = self.layout
        folderName = self.bl_idname.split('.')[1]
        print (folderName)
        dir = os.path.join(full_path_to_directory, folderName)
        addOperatorsToLayout(dir, layout)    
                
def addOperatorsToLayout(dir, layout):
    file_list = os.listdir(dir)
    for name in file_list:
        if name[-3:] == 'obj':
            filename = os.path.join(dir, name)
            layout.operator("bpt.obj_importer", text="" + name, icon="MESH_ICOSPHERE").filename = filename

def createSubMenu(folderName):
    class InheritedClass(subMenuClass):
        bl_idname = "asset_library_submenu" + "." + folderName
        
    return InheritedClass
  
# Creates a menu for global 3D View
class customMenu(bpy.types.Menu):
    bl_label = "KTX Library Import .OBJ"
    bl_idname = "view3D.asset_library"
    
    # Set the menu operators and draw functions
    def draw(self, context):
       
        layout = self.layout
 
        # access this operator as a submenu
        # get list of all files in directory
        file_list = os.listdir(full_path_to_directory)
         
        # reduce the list to files ending in 'obj'
        # using 'list comprehensions'
        obj_list = [item for item in file_list if item[-3:] == 'obj']
        
        file_list = os.listdir(full_path_to_directory)
        for name in file_list:
            if os.path.isdir(os.path.join(full_path_to_directory, name)):
                layout.menu(folderDict[name], text="" + name, icon="FILE_FOLDER")
                
        addOperatorsToLayout(full_path_to_directory, layout)

		
def menu_draw(self, context):
    layout = self.layout
    layout.menu(customMenu.bl_idname, icon='MOD_SCREW')


def register():
    bpy.utils.register_class( opOBJImporter )
    bpy.utils.register_class( customMenu )
    file_list = os.listdir(full_path_to_directory)
    for name in file_list:
        if os.path.isdir(os.path.join(full_path_to_directory, name)):
            newMenuClass = createSubMenu(name)
            bpy.utils.register_class(newMenuClass)
            folderDict[name] = newMenuClass.bl_idname
    bpy.types.INFO_MT_mesh_add.append(menu_draw)


def unregister():
    bpy.utils.unregister_class( customMenu )
    bpy.utils.unregister_class( opOBJImporter )
    bpy.types.INFO_MT_mesh_add.remove(menu_draw)

if __name__ == "__main__":
    register()
