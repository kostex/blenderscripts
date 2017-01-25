bl_info = {
    "name": "KTX Node Tools",
	"author": "Roel Koster, kostex (irc), koelooptiemanna",
	"version": (1 ,2),
	"blender": (2, 75, 0),
	"location": "Node Editor Toolbar Texture Tab and Add Menu (Shift A)",
	"description": "Quick Tools from the Node Editor",
	"category": "Node"
}

import bpy
from bpy.types import Operator, Panel, Menu
from bpy.props import EnumProperty, BoolProperty, IntProperty, StringProperty

# thanks to NodeWrangler for nwcheck,nwbase
def nw_check(context):
    space = context.space_data
    valid = False
    if space.type == 'NODE_EDITOR' and space.node_tree is not None:
        valid = True
        
    return valid    

class NWBase:
    @classmethod
    def poll(cls, context):
        return nw_check(context)

class KTXImageTextureMenu(Operator,NWBase):
    bl_idname="wm.ktx_node_imtexmenu"
    bl_label="Create Image Texture Node"
    bl_options = {'REGISTER','UNDO'}

    imgSize = EnumProperty(
        name = "Image Size",
        description="Image Size",
        items=(
            ("I_0128","128 x 128","128x128 Image Map"),
            ("I_0256","256 x 256","256x256 Image Map"),
            ("I_0512","512 x 512","512x512 Image Map"),
            ("I_1024","1024 x 1024","1024x1024 Image Map"),
            ("I_2048","2048 x 2048","2048x2048 Image Map"),
            ("I_4096","4096 x 4096","4096x4096 Image Map"),
            ("I_8192","8192 x 8192","8192x8182 Image Map")
        )
    )
    name = StringProperty(
         name = "Name"
    )
    coldat = BoolProperty(
         name = "Non-Color Data"
    )
    alpha = BoolProperty(
         name = "Alpha"
    )
    flo = BoolProperty(
         name = "32bit Float"
    )
    appsize = BoolProperty(
        name = "Append Size to Name"
    )
    uvadd = BoolProperty(
        name = "Add UV Mapping Nodes"
    )

    def execute(self, context):
        scn = context.scene
        size = self.imgSize[-4:]
        imName=self.name
        if self.appsize:
           imName=imName+"_"+size
        newImage=bpy.data.images.new(imName,int(size),int(size),self.alpha,self.flo,0)
        mat=bpy.context.active_object.active_material
        tree=mat.node_tree
        nodes=tree.nodes
        links=tree.links
        xloc=0
        yloc=0
        for node in nodes:
            if node.select:
              xloc=node.location.x-400
              yloc=node.location.y
  
        node_image=nodes.new("ShaderNodeTexImage")
        node_image.image=bpy.data.images.get(newImage.name)
        node_image.width=300
        node_image.location.x=xloc
        node_image.location.y=yloc
        
        if self.coldat:
            node_image.color_space='NONE'

        if self.uvadd:
           node_coords=nodes.new("ShaderNodeTexCoord")
           node_mapping=nodes.new("ShaderNodeMapping")
           links.new(node_mapping.outputs[0],node_image.inputs[0])
           links.new(node_coords.outputs[2],node_mapping.inputs[0])
           node_mapping.location.x=xloc-400
           node_mapping.location.y=yloc
           node_coords.location.x=xloc-600
           node_coords.location.y=yloc

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class KTXSetViewportColorFromSelectedNode(bpy.types.Operator):
    bl_idname = "wm.ktx_set_viewport_color_from_selected_node"
    bl_label = "Set Viewport Color"
    bl_option = {'REGISTER', 'UNDO'}

    def execute(self, context):
     mat=bpy.context.active_object.material_slots.data.active_material
     nodetree=mat.node_tree
     nodes=nodetree.nodes
     links=nodetree.links
     for node in nodes:
      col=[]
      if node.select and node.type=='BSDF_DIFFUSE' and node.inputs[0].is_linked==False:
       col=node.inputs[0].default_value
       mat.diffuse_color=(col[0],col[1],col[2])
     return {'FINISHED'}


class KTXAddMixGlossy(bpy.types.Operator):
    bl_idname = "wm.ktx_add_mix_glossy"
    bl_label = "Add Mix and Glossy Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     mat=bpy.context.active_object.active_material
     tree=mat.node_tree
     nodes=tree.nodes
     links=tree.links
     for node in nodes:
      if node.select:
       link_to=node.outputs[0].links[0].to_socket
       node_mix=nodes.new('ShaderNodeMixShader')
       node_mix.inputs[0].default_value=0.1
       node_mix.location.x = node.location.x + 200
       node_mix.location.y = node.location.y
       node_mix.select=False

       node_glossy=nodes.new('ShaderNodeBsdfGlossy')
       node_glossy.inputs[1].default_value=0
       node_glossy.location.x = node.location.x
       node_glossy.location.y = node.location.y - 150
       node_glossy.select=False

       links.remove(node.outputs[0].links[0])
       links.new(node.outputs[0],node_mix.inputs[1])
       links.new(node_glossy.outputs[0],node_mix.inputs[2])
       links.new(node_mix.outputs[0],link_to)
     return {'FINISHED'}

class KTXAddMixGlossyFresnel(bpy.types.Operator):
    bl_idname = "wm.ktx_add_mix_glossy_fresnel"
    bl_label = "Add Mix and Glossy Nodes with Fresnel Control"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     mat=bpy.context.active_object.active_material
     tree=mat.node_tree
     nodes=tree.nodes
     links=tree.links
     for node in nodes:
      if node.select:
       link_to=node.outputs[0].links[0].to_socket
       node.location.x = node.location.x - 200
       node_mix=nodes.new('ShaderNodeMixShader')
       node_mix.inputs[0].default_value=0.1
       node_mix.location.x = node.location.x + 200
       node_mix.location.y = node.location.y
       node_mix.select=False

       node_glossy=nodes.new('ShaderNodeBsdfGlossy')
       node_glossy.inputs[1].default_value=0
       node_glossy.location.x = node.location.x
       node_glossy.location.y = node.location.y - 150
       node_glossy.select=False

       node_fresnel=nodes.new('ShaderNodeFresnel')
       node_fresnel.location.x = node.location.x
       node_fresnel.location.y = node.location.y + 150
       node_fresnel.select=False

       links.remove(node.outputs[0].links[0])
       links.new(node_fresnel.outputs[0],node_mix.inputs[0])
       links.new(node.outputs[0],node_mix.inputs[1])
       links.new(node_glossy.outputs[0],node_mix.inputs[2])
       links.new(node_mix.outputs[0],link_to)
     return {'FINISHED'}

class KTXNodesPanel(bpy.types.Panel):
    bl_label = "KTX Image Node"
    bl_idname = "SCENE_KTX_layout"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "Texture"
    

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("wm.ktx_node_imtexmenu")

class KTXNodeMenu(bpy.types.Menu):
    bl_idname = "wm.ktx_node_menu"
    bl_label = "KTX Nodes"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.ktx_node_imtexmenu")
        layout.operator("wm.ktx_add_mix_glossy")
        layout.operator("wm.ktx_add_mix_glossy_fresnel")
        layout.operator("wm.ktx_set_viewport_color_from_selected_node")

def menu_func(self, context):
    self.layout.menu("wm.ktx_node_menu")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.NODE_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.NODE_MT_add.remove(menu_func)

if __name__ == "__main__":
    register()
