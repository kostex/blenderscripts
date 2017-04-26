bl_info = {
    "name": "KTX Bottle 2",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 7, 0),
    "location": "View3D > Tools > Create",
    "category": "3D View"}


import bpy, mathutils, bmesh
EDIT_MODES = {'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_METABALL', 'EDIT_TEXT', 'EDIT_ARMATURE'}

class KTXBottle2Sep(bpy.types.Operator):
    bl_idname="wm.ktx_bottle_2_sep"
    bl_label="KTX Create a Bottle and Cap"
    bl_options={'REGISTER','UNDO', 'PRESET'}

    hide_bottle = bpy.props.BoolProperty(name="Hide Bottle",
        description="Hide Bottle On/Off",
        default=False)
    hide_cap = bpy.props.BoolProperty(name="Hide Cap",
        description="Hide Cap On/Off",
        default=False)
    hide_bottle_body = bpy.props.BoolProperty(name="Hide Bottle Body",
        description="Hide Bottle Body On/Off",
        default=False)
    comp_bot = bpy.props.BoolProperty(name="Generate Complete Bottle",
        description="Generate Complete Bottle or only Threads",
        default=True)
    manual_bot = bpy.props.BoolProperty(name="Manual Bottle Body",
        description="Generate Manual Bottle Body or only two verts, ready for extruding",
        default=True)

    overall_scale = bpy.props.FloatProperty(name="Overall Scale",
        description="Overall Scale",
        default=0.1)
    v = bpy.props.IntProperty(name="Vertices",
        description="Cylinder divided into this many Vertices",
        default=12,min=3,max=24)
    thread_height = bpy.props.FloatProperty(name="Thread Height",
        description="Thread Height",
        default=0.5,min=0.1)
    thread_steps = bpy.props.IntProperty(name="Thread Steps",
        description="Thread Steps",
        default=28,min=1)
    neck_radius = bpy.props.FloatProperty(name="Neck Radius",
        description="Neck Radius",
        default=1.48,min=0.1)
    trap = bpy.props.FloatProperty(name="Trapezium Thread",
        description="Trapezium Thread",
        default=0.09,min=0.0)
    depth = bpy.props.FloatProperty(name="Depth",
        description="Depth",
        default=0.2,min=0.0)
    eoff_onoff = bpy.props.BoolProperty(name="Enlarge Cap",
        description="Enlarge Cap (to prevent intersection between threads",
        default=True)
    eoffset = bpy.props.IntProperty(name="Enlarge Cap Percentage",
        description="Percentage of Neck Radius",
        default=1)

    skip_onoff = bpy.props.BoolProperty(name="Step Thread Bottle",
        description="Step Thread Bottle",
        default=False)
    soffset = bpy.props.IntProperty(name="Skip Offset Bottle",
        description="Skip Offset Bottle",
        default=4)
    sckip_onoff = bpy.props.BoolProperty(name="Step Thread Cap",
        description="Step Thread Cap",
        default=False)
    scoffset = bpy.props.IntProperty(name="Skip Offset Cap",
        description="Skip Offset Cap",
        default=4)


    remdoub_onoff = bpy.props.BoolProperty(name="Remove Doubles",
        description="Remove Doubles On/Off",
        default=True)
    doubles = bpy.props.FloatProperty(name="Merge Verts Dist",
        description="Merge Verts Dist",
        default=0.01)
    smooth_onoff = bpy.props.BoolProperty(name="Smoothing",
        description="Smoothing Doubles On/Off",
        default=True)
    subs_onoff = bpy.props.BoolProperty(name="SubSurf",
        description="SubSurf On/Off",
        default=True)
    nl = bpy.props.FloatProperty(name="Neck Length",
        description="Neck Length",
        default=0.1,min=0.01)
    tl = bpy.props.FloatProperty(name="Top Length",
        description="Top Length",
        default=0.1,min=0.001)
    tt = bpy.props.FloatProperty(name="Top Tickness",
        description="Top Tickness",
        default=0.3,min=0.001)
    # h = bpy.props.FloatProperty(name="Bottle Height",
    #     description="Bottle Height",
    #     default=1.0,min=0.001)
    x1 = bpy.props.FloatProperty(name="X1",
        description="X1",
        default=2.11)
    z1 = bpy.props.FloatProperty(name="Z1",
        description="Z1",
        default=1.0)
    x2 = bpy.props.FloatProperty(name="X2",
        description="X2",
        default=1.58)
    z2 = bpy.props.FloatProperty(name="Z2",
        description="Z2",
        default=3.62)
    x3 = bpy.props.FloatProperty(name="X3",
        description="X3",
        default=1.0)
    z3 = bpy.props.FloatProperty(name="Z3",
        description="Z3",
        default=4.0)
    x4 = bpy.props.FloatProperty(name="X4",
        description="X4",
        default=3.01)
    z4 = bpy.props.FloatProperty(name="Z4",
        description="Z4",
        default=8.75)
    x5 = bpy.props.FloatProperty(name="X5",
        description="X5",
        default=0.5)
    z5 = bpy.props.FloatProperty(name="Z5",
        description="Z5",
        default=8.69)

    @classmethod
    def poll(self, context):
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))


    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'comp_bot')
        if self.comp_bot:
            col.prop(self, 'manual_bot')

        col.separator()
        col.prop(self, 'hide_bottle')
        col.prop(self, 'hide_bottle_body')
        col.prop(self, 'hide_cap')

        col.separator()
        col.prop(self, 'overall_scale')
        col.prop(self, 'v')
        col.prop(self, 'thread_height')
        col.prop(self, 'thread_steps')
        col.prop(self, 'neck_radius')
        col.prop(self, 'trap')
        col.prop(self, 'depth')
        if self.comp_bot:
            col.prop(self, 'nl')
            col.prop(self, 'tl')
            col.prop(self, 'tt')
            if self.manual_bot:
                col.separator()
                col.prop(self,'x1')
                col.prop(self,'z1')
                col.prop(self,'x2')
                col.prop(self,'z2')
                col.prop(self,'x3')
                col.prop(self,'z3')
                col.prop(self,'x4')
                col.prop(self,'z4')
                col.prop(self,'x5')
                col.prop(self,'z5')

        col.separator()
        col.prop(self, 'eoff_onoff')
        if self.eoff_onoff:
            col.prop(self, 'eoffset')
        col.separator()
        col.prop(self, 'skip_onoff')
        if self.skip_onoff:
            col.prop(self, 'soffset')
        col.prop(self, 'sckip_onoff')
        if self.sckip_onoff:
            col.prop(self, 'scoffset')
        col.separator()

        col.prop(self, 'remdoub_onoff')
        if self.remdoub_onoff: 
            col.prop(self, 'doubles')
        col.separator()
        col.prop(self, 'smooth_onoff')
        col.prop(self, 'subs_onoff')



    def execute(self,context):
       import math, bmesh
       from math import radians
#------midden
       bm=bmesh.new()
       v1=bm.verts.new((self.neck_radius, 0.0, self.thread_height))
       v2=bm.verts.new((self.neck_radius, 0.0, 0.0))
       bm.edges.new((v1,v2))
       bmesh.ops.spin(bm,geom=bm.verts[:]+bm.edges[:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,self.thread_height/self.v),angle=self.thread_steps * ((2.0 * math.pi)/self.v),steps=self.thread_steps,use_duplicate=0)
       bm.faces.ensure_lookup_table()
       gg=bm.faces[:]
       if self.skip_onoff:
           for i in range(0,self.thread_steps,self.soffset):
               gg.remove(bm.faces[i])

       bmesh.ops.inset_region(bm,faces=gg,thickness=self.thread_height/5.0,depth=0.0,use_boundary=1,use_even_offset=1,use_relative_offset=0,use_interpolate=0)
       bmesh.ops.inset_region(bm,faces=gg,thickness=self.trap,depth=self.depth,use_boundary=0,use_even_offset=1,use_relative_offset=0,use_interpolate=0)
#----------Bottom
       v1=bm.verts.new((self.neck_radius, 0.0, 0.0))
       bmesh.ops.spin(bm,geom=[v1],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,self.thread_height/self.v),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
       ret=bmesh.ops.extrude_edge_only(bm,edges=bm.edges[-self.v:])
       geom_new = ret["geom"]
       del ret
       verts_new=[ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
       bmesh.ops.translate(bm,verts=verts_new,vec=(0.0,0.0,-0.5))
       bmesh.ops.scale(bm,verts=verts_new,vec=(1.0,1.0,0.0))
#---------BottleBody
       if self.comp_bot:
           v1=bm.verts.new((self.neck_radius, 0.0, 0.0))
           v2=bm.verts.new((self.neck_radius, 0.0, -self.nl))
           bm.edges.new((v1,v2))
           bmesh.ops.spin(bm,geom=bm.verts[-2:]+bm.edges[-1:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
#----------Top
       aa=((self.thread_height/self.v)*self.thread_steps)+self.thread_height
       bb=self.thread_steps%self.v

       v1=bm.verts.new((self.neck_radius, 0.0, aa))
       bmesh.ops.rotate(bm,verts=[v1],cent=(0.0,0.0,0.0),matrix=mathutils.Matrix.Rotation(((2*math.pi)/self.v)*bb,3,'Z'))
       bmesh.ops.spin(bm,geom=[v1],axis=(0.0,0.0,-1.0),cent=(0,0,0),dvec=(0,0,-self.thread_height/self.v),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
       ret=bmesh.ops.extrude_edge_only(bm,edges=bm.edges[-self.v:])
       geom_new = ret["geom"]
       del ret
       verts_new=[ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
       bmesh.ops.scale(bm,verts=verts_new,vec=(1.0,1.0,0.0))
       ret_boven=bmesh.ops.translate(bm,verts=verts_new,vec=(0.0,0.0,aa))
#---------BottleInside
       if self.comp_bot:
           if self.tt >= self.neck_radius:
               self.tt = self.neck_radius - 0.001
           v1=bm.verts.new((self.neck_radius, 0.0, aa))
           v2=bm.verts.new((self.neck_radius, 0.0, aa+self.tl))
           v3=bm.verts.new((self.neck_radius-self.tt, 0.0, aa+self.tl))
           v4=bm.verts.new((self.neck_radius-self.tt, 0.0, aa))
           v5=bm.verts.new((self.neck_radius-self.tt, 0.0, 0.0))
           v6=bm.verts.new((self.neck_radius-self.tt, 0.0, -self.nl))
           bm.edges.new((v6,v5))
           bm.edges.new((v5,v4))
           bm.edges.new((v4,v3))
           bm.edges.new((v3,v2))
           bm.edges.new((v2,v1))
           bmesh.ops.spin(bm,geom=bm.verts[-6:]+bm.edges[-5:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0*math.pi),steps=self.v,use_duplicate=0)

#---------Generate Bottle
       
       if self.remdoub_onoff and self.doubles != 0.0:
           bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=self.doubles)

       bmesh.ops.scale(bm,vec=(self.overall_scale,self.overall_scale,self.overall_scale),verts=bm.verts[:])

       me = bpy.data.meshes.new("Bottle_Mesh")
       bm.to_mesh(me)
       bm.free()
       if self.smooth_onoff:
           pols = me.polygons
           for p in pols:
               p.use_smooth = True

       scene = bpy.context.scene
       obj = bpy.data.objects.new("Bottle", me)
       obj.location = bpy.context.scene.cursor_location
       obj.location.z = obj.location.z + (self.z5 + self.nl + self.depth)*self.overall_scale
       scene.objects.link(obj)
       if self.subs_onoff:
           obj.modifiers.new("subd", type='SUBSURF')
           obj.modifiers["subd"].levels = 2
           obj.modifiers["subd"].render_levels = 3

       bpy.context.scene.objects.active = obj
       if self.hide_bottle:
           bpy.context.object.hide = True
       else:
           bpy.context.object.hide = False


#------Dop/Cap
#------Draad/Thread

       if self.eoff_onoff:
           ca=(self.neck_radius/100.0)*self.eoffset
       else:
           ca=0.0

       bm=bmesh.new()
       v1=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, self.thread_height))
       v2=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, 0.0))
       bm.edges.new((v2,v1))
       bmesh.ops.spin(bm,geom=bm.verts[:]+bm.edges[:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,self.thread_height/self.v),angle=self.thread_steps * ((2.0 * math.pi)/self.v),steps=self.thread_steps,use_duplicate=0)
       bm.faces.ensure_lookup_table()
       gg=bm.faces[:]
       if self.sckip_onoff:
           for i in range(0,self.thread_steps,self.scoffset):
               gg.remove(bm.faces[i])
       bmesh.ops.inset_region(bm,faces=gg,thickness=self.thread_height/5.0,depth=0.0,use_boundary=1,use_even_offset=1,use_relative_offset=0,use_interpolate=0)
       bmesh.ops.inset_region(bm,faces=gg,thickness=self.trap,depth=self.depth,use_boundary=0,use_even_offset=1,use_relative_offset=0,use_interpolate=0)
#----------Bottom
       v1=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, 0.0))
       bmesh.ops.spin(bm,geom=[v1],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,self.thread_height/self.v),angle=(2.0*math.pi),steps=self.v,use_duplicate=0)
       ret=bmesh.ops.extrude_edge_only(bm,edges=bm.edges[-self.v:])
       geom_new = ret["geom"]
       del ret
       verts_new=[ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
       bmesh.ops.translate(bm,verts=verts_new,vec=(0.0,0.0,-0.5))
       bmesh.ops.scale(bm,verts=verts_new,vec=(1.0,1.0,0.0))
#----------Top
       aa=((self.thread_height/self.v)*self.thread_steps)+self.thread_height
       bb=self.thread_steps%self.v

       v1=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, aa))
       bmesh.ops.rotate(bm,verts=[v1],cent=(0.0,0.0,0.0),matrix=mathutils.Matrix.Rotation(((2*math.pi)/self.v)*bb,3,'Z'))
       bmesh.ops.spin(bm,geom=[v1],axis=(0.0,0.0,-1.0),cent=(0,0,0),dvec=(0,0,-self.thread_height/self.v),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)

       ret=bmesh.ops.extrude_edge_only(bm,edges=bm.edges[-self.v:])
       geom_new = ret["geom"]
       del ret
       verts_new=[ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
       bmesh.ops.scale(bm,verts=verts_new,vec=(1.0,1.0,0.0))
       ret_boven=bmesh.ops.translate(bm,verts=verts_new,vec=(0.0,0.0,aa))
#---------Cap Inside
       if self.comp_bot:
           v1=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, aa))
           v2=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, aa+self.tl))
           v3=bm.verts.new((self.neck_radius+self.depth-self.tt+ca, 0.0, aa+self.tl))
           v4=bm.verts.new((0.0, 0.0, aa+self.tl))
           bm.edges.new((v4,v3))
           bm.edges.new((v3,v2))
           bm.edges.new((v2,v1))
           bmesh.ops.spin(bm,geom=bm.verts[-4:]+bm.edges[-3:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
#---------CapBody
           v1=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, 0.0))
           v2=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, -self.depth))
           v3=bm.verts.new((self.neck_radius+self.depth*2.0+ca, 0.0, -self.depth))
           v4=bm.verts.new((self.neck_radius+self.depth*2.0+ca, 0.0, aa+self.tl+self.depth))
           v5=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, aa+self.tl+self.depth))
           v6=bm.verts.new((0.0, 0.0, aa+self.tl+self.depth))
           bm.edges.new((v6,v5))
           bm.edges.new((v5,v4))
           bm.edges.new((v4,v3))
           bm.edges.new((v3,v2))
           bm.edges.new((v2,v1))
           bmesh.ops.spin(bm,geom=bm.verts[-6:]+bm.edges[-5:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)


#---------Generate Cap
       
       if self.remdoub_onoff and self.doubles != 0.0:
           bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=self.doubles)

       bmesh.ops.scale(bm,vec=(self.overall_scale,self.overall_scale,self.overall_scale),verts=bm.verts[:])

       me = bpy.data.meshes.new("Cap_Mesh")
       bm.to_mesh(me)
       bm.free()
       if self.smooth_onoff:
           pols = me.polygons
           for p in pols:
               p.use_smooth = True

       scene = bpy.context.scene
       obj = bpy.data.objects.new("Cap", me)
       obj.location = bpy.context.scene.cursor_location
       obj.location.z = obj.location.z + (self.thread_height/2 + self.z5 + self.nl + self.depth)*self.overall_scale
       scene.objects.link(obj)
       if self.subs_onoff:
           obj.modifiers.new("subd", type='SUBSURF')
           obj.modifiers["subd"].levels = 2
           obj.modifiers["subd"].render_levels = 3
   
       bpy.context.scene.objects.active = obj
       bpy.ops.object.mode_set(mode='EDIT')
       bpy.ops.mesh.select_all(action='SELECT')
       bpy.ops.mesh.normals_make_consistent(inside=False)
       bpy.ops.object.editmode_toggle()

       if self.hide_cap:
           bpy.context.object.hide = True
       else:
           bpy.context.object.hide = False


#------Bottle Body

       if self.comp_bot:
           bm=bmesh.new()

           v1=bm.verts.new((self.neck_radius, 0.0, -self.nl))
           v2=bm.verts.new((self.neck_radius, 0.0, -self.nl-self.depth))
           bm.edges.new((v1,v2))
           if self.manual_bot:
               y=-self.nl-self.depth
               v3=bm.verts.new((self.neck_radius+self.x1, 0.0, y-self.z1))
               v4=bm.verts.new((self.neck_radius+self.x2, 0.0, y-self.z2))
               v5=bm.verts.new((self.neck_radius+self.x3, 0.0, y-self.z3))
               v6=bm.verts.new((self.neck_radius+self.x4, 0.0, y-self.z4))
               v7=bm.verts.new((self.neck_radius+self.x5, 0.0, y-self.z5))
               v8=bm.verts.new((0.0, 0.0, y-self.z5))
               bm.edges.new((v2,v3))
               bm.edges.new((v3,v4))
               bm.edges.new((v4,v5))
               bm.edges.new((v5,v6))
               bm.edges.new((v6,v7))
               bm.edges.new((v7,v8))


           bmesh.ops.scale(bm,vec=(self.overall_scale,self.overall_scale,self.overall_scale),verts=bm.verts[:])

           me = bpy.data.meshes.new("BottleBody_Mesh")
           bm.to_mesh(me)
           bm.free()

           scene = bpy.context.scene
           obj = bpy.data.objects.new("BottleBody", me)
           obj.location = bpy.context.scene.cursor_location
           obj.location.z = obj.location.z + (self.z5 + self.nl + self.depth)*self.overall_scale
           scene.objects.link(obj)

           obj.modifiers.new("spin", type="SCREW")
           obj.modifiers["spin"].steps=self.v
           if self.smooth_onoff:
               obj.modifiers["spin"].use_smooth_shade=True
           else:
               obj.modifiers["spin"].use_smooth_shade=False

           obj.modifiers.new("solidify", type="SOLIDIFY")
           obj.modifiers["solidify"].thickness=self.tt*self.overall_scale
           obj.modifiers["solidify"].use_rim=False
           obj.modifiers["solidify"].use_flip_normals=False
           obj.modifiers["solidify"].use_even_offset=False

           if self.subs_onoff:
               obj.modifiers.new("subd", type="SUBSURF")
               obj.modifiers["subd"].levels = 2
               obj.modifiers["subd"].render_levels = 3


           bpy.context.scene.objects.active = obj

           if self.hide_bottle_body:
               bpy.context.object.hide = True
           else:
               bpy.context.object.hide = False


       return {'FINISHED'}


class KTXPanel_2( bpy.types.Panel ):
    bl_label = "KosteX Bottle 2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))

    
    def draw( self, context ):
        scn = context.scene
        layout = self.layout
        new_col = self.layout.column
        new_col().column().operator("wm.ktx_bottle_2_sep")



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
