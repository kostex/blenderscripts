bl_info = {
    "name": "KTX Tools",
    "author": "Roel Koster",
    "version": (3, 6),
    "blender": (2, 7, 0),
    "location": "View3D > Tools",
    "category": "3D View"}


import bpy, mathutils, math, random, colorsys, bmesh, operator
from mathutils import Vector


class KTXAssignRandomDiffuseColors(bpy.types.Operator):
    
    bl_idname = "wm.ktx_assign_random_diffuse_colors"
    bl_label = "Rnd Diff. Colors"
    bl_options = {'REGISTER', 'UNDO'}

    random_seed = bpy.props.IntProperty(name="Random Seed",
        description="Seed value for the random generator",
        min=0,
        max=10000,
        default=0)

    rgb_or_hsv = bpy.props.BoolProperty(
        name="RGB/HSV",
        description="RGB or Select to choose HSV",
        default=False)
    
    rminmax = bpy.props.FloatVectorProperty(
        size=2,
        name="RH Min/Max Values",
        description="Red or Hue Min/Max Values",
        default=(0.0, 1.0), min=0.0, max=1.0)

    gminmax = bpy.props.FloatVectorProperty(
        size=2,
        name="GS Min/Max Values",
        description="Green or Saturation Min/Max Values",
        default=(0.0, 1.0), min=0.0, max=1.0)

    bminmax = bpy.props.FloatVectorProperty(
        size=2,
        name="BV Min/Max Values",
        description="Blue or Value Min/Max Values",
        default=(0.0, 1.0), min=0.0, max=1.0)


    def execute(self, context):
        import random
        from random import uniform
        random.seed(self.random_seed)

        for obj in bpy.context.selected_objects:
         if (obj.type=='MESH' or obj.type=='CURVE'):
          r=uniform(self.rminmax[0],self.rminmax[1])
          g=uniform(self.gminmax[0],self.gminmax[1])
          b=uniform(self.bminmax[0],self.bminmax[1])
          m=obj.active_material
          if self.rgb_or_hsv:
           col=colorsys.hsv_to_rgb(r,g,b)
           m.node_tree.nodes[1].inputs[0].default_value=(col[0],col[1],col[2],1)
           obj.active_material.diffuse_color=(col)
          else:
           m.node_tree.nodes[1].inputs[0].default_value=(r,g,b,1)
           obj.active_material.diffuse_color=(r,g,b)
        return {'FINISHED'}

class KTXAddRandomCubes(bpy.types.Operator):
    bl_idname = "wm.ktx_add_random_cubes"
    bl_label = "Rnd Cubes"
    bl_options = {"REGISTER", "UNDO"}

    random_seed = bpy.props.IntProperty(name="Random Seed",
        description="Seed value for the random generator",
        min=0,
        max=10000,
        default=0)

    count = bpy.props.IntProperty(name="Count",
        description="Number of Cubes",
        default=20, min=3, max=1000)

    uniformscale = bpy.props.BoolProperty(name="UniScale",
        description="Uniform Scale",
        default=True)

    minsize = bpy.props.FloatProperty(name="MinSize",
        description="Minumum Cube Size",
        default=0.1, min=0.01, max=20.0)

    maxsize = bpy.props.FloatProperty(name="MaxSize",
        description="Maximum Cube Size",
        default=0.1, min=0.01, max=20.0)

    span = bpy.props.FloatVectorProperty(name="Span",
        description="Distribution Area",
        default=(1.0, 1.0, 1.0), min=0.01, max=200.0)

    rotation = bpy.props.FloatVectorProperty(name="Rotation",
        description="Rotation",
        default=(0.0, 0.0, 0.0), min=-3.141592, max=3.141592, subtype='EULER')

    def execute(self, context):
        import random
        from random import uniform
        random.seed(self.random_seed)
        for i in range (1,self.count):
            fspan=Vector(uniform(-val, val) for val in self.span)

            frotation=Vector(uniform(-val, val) for val in self.rotation)

            xrand=uniform(self.minsize,self.maxsize)
            yrand=uniform(self.minsize,self.maxsize)
            zrand=uniform(self.minsize,self.maxsize)
            if self.uniformscale:
               fsize=Vector((xrand,xrand,xrand))
            else:
               fsize=Vector((xrand,yrand,zrand))

            bpy.ops.mesh.primitive_cube_add(location=fspan, rotation=frotation)
            ob=bpy.context.object
            ob.name='Kuub'
            ob.scale=fsize
        return {'FINISHED'}

class KTXAddRandomCopies(bpy.types.Operator):
    bl_idname = "wm.ktx_add_random_copies"
    bl_label = "Rnd Copies"
    bl_options = {"REGISTER", "UNDO"}

    random_seed = bpy.props.IntProperty(name="Random Seed",
        description="Seed value for the random generator",
        min=0,
        max=10000,
        default=0)

    linkedcopy = bpy.props.BoolProperty(name="Linked",
        description="Make a Linked copy",
        default=False)

    count = bpy.props.IntProperty(name="Count",
        description="Number of Cubes",
        default=20, min=3, max=1000)

    uniformscale = bpy.props.BoolProperty(name="UniScale",
        description="Uniform Scale",
        default=True)

    minsize = bpy.props.FloatProperty(name="MinSize",
        description="Minimum Size",
        default=1.0, min=0.001, max=20.0)

    maxsize = bpy.props.FloatProperty(name="MaxSize",
        description="Maximum Size",
        default=1.0, min=0.001, max=20.0)

    span = bpy.props.FloatVectorProperty(name="Span",
        description="Distribution Area",
        default=(1.0, 1.0, 1.0), min=0.01, max=200.0)

    rotation = bpy.props.FloatVectorProperty(name="Rotation",
        description="Rotation",
        default=(0.0, 0.0, 0.0), min=-3.141592, max=3.141592, subtype='EULER')

    def execute(self, context):
       import random
       from random import uniform
       random.seed(self.random_seed)
       obj=bpy.context.active_object
       if obj:
        for i in range (1,self.count):
            fspan=Vector(uniform(-val, val) for val in self.span)

            frotation=Vector(uniform(-val, val) for val in self.rotation)

            xrand=uniform(self.minsize,self.maxsize)
            yrand=uniform(self.minsize,self.maxsize)
            zrand=uniform(self.minsize,self.maxsize)
            if self.uniformscale:
               fsize=Vector((xrand,xrand,xrand))
            else:
               fsize=Vector((xrand,yrand,zrand))

            bpy.ops.object.duplicate(linked=self.linkedcopy)
            obj=bpy.context.active_object
            obj.location=fspan
            obj.scale=fsize
            obj.rotation_euler=frotation
       return {'FINISHED'}

class KTXAssignMaterials(bpy.types.Operator):
    bl_idname = "wm.ktx_assign_materials"
    bl_label = "Add Deflt Mtrls"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     for obj in bpy.context.selected_objects:
      if (obj.type=='MESH' or obj.type=='CURVE'):
       mat=bpy.data.materials.new(obj.name)
       obj.active_material=mat
       obj.material_slots[0].material.use_nodes=True
     return {'FINISHED'}

class KTXAddGlossyMixShaders(bpy.types.Operator):
    bl_idname = "wm.ktx_add_glossy_mix_shaders"
    bl_label = "Add G/M Shaders"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     unique_mats=[]
     for obj in bpy.context.selected_objects:
      obj_mat_name=obj.material_slots[0].name
      if not obj_mat_name in unique_mats:
       unique_mats.append(obj_mat_name)

     for mat in bpy.data.materials:
      if mat.name in unique_mats:
       tree=mat.node_tree
       nodes=tree.nodes
       links=tree.links
       nodes[0].location.x = nodes[0].location.x + 200
       node_glossy=nodes.new('ShaderNodeBsdfGlossy')
       node_glossy.location=(10,150)
       node_glossy.inputs[1].default_value=0
       node_mix=nodes.new('ShaderNodeMixShader')
       node_mix.location=(300,300)
       node_mix.inputs[0].default_value=random.randint(0,20)/100
       links.new(nodes[1].outputs[0],node_mix.inputs[1])
       links.new(node_glossy.outputs[0],node_mix.inputs[2])
       links.new(node_mix.outputs[0],nodes[0].inputs[0])
     return {'FINISHED'}

class KTXAddSubsurfCreases(bpy.types.Operator):
    bl_idname = "wm.ktx_add_subsurf_creases"
    bl_label = "Add SubSurf Crsd"
    bl_options = {'REGISTER', 'UNDO'}

    sub = bpy.props.BoolProperty(name="Sub Surface",
        description="Add Sub Surface",
        default=False)

    viewlevels = bpy.props.IntProperty(name="View Levels",
        description="Viewport Levels",
        default=3, min=1, max=4)

    renderlevels = bpy.props.IntProperty(name="Render Levels",
        description="Render Levels",
        default=3, min=1, max=4)

    creasevalue = bpy.props.FloatProperty(name="Crease Value",
        description="Crease Value",
        default=0.9, min=0.0, max=1.0)

    def execute(self, context):
     for obj in bpy.data.objects:
      if obj.type=='MESH':
       if self.sub:
        mod1=obj.modifiers.new('sub','SUBSURF')
        mod1.levels=self.viewlevels
        mod1.render_levels=self.renderlevels
       for i in obj.data.edges:
        i.crease=self.creasevalue
     return {'FINISHED'}

class KTXSetViewportColor(bpy.types.Operator):
    bl_idname = "wm.ktx_set_viewport_color"
    bl_label = "Set View Color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     obj=bpy.context.active_object
     col=obj.material_slots[0].material.node_tree.nodes[1].inputs[0].default_value
     obj.active_material.diffuse_color=(col[0],col[1],col[2])
     return {'FINISHED'}

class KTXEraseAllMaterials(bpy.types.Operator):
    bl_idname = "wm.ktx_erase_all_materials"
    bl_label = "Erase Unused Mtrls"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     bmat=bpy.data.materials
     for mat in bmat:
#      mat.use_fake_user=False
      if mat.users < 1:
       bmat.remove(mat)
     return {'FINISHED'}

class KTXEraseUnusedTextures(bpy.types.Operator):
    bl_idname = "wm.ktx_erase_unused_textures"
    bl_label = "Erase Unused Txtrs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     img_names = []
     textures = bpy.data.textures
     for tex in textures:
      if tex.type == 'IMAGE':  
       img_names.append(tex.image.name)
     imgs = bpy.data.images
     for image in imgs:
      name = image.name
      if name not in img_names:
       image.user_clear()
     return {'FINISHED'}

class KTXEraseUnusedPalettes(bpy.types.Operator):
    bl_idname = "wm.ktx_erase_unused_palettes"
    bl_label = "Erase Unused Palettes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
     bpal=bpy.data.palettes
     for pal in bpal:
      pal.use_fake_user=False
      if pal.users < 1:
       bpal.remove(pal)
     return {'FINISHED'}

class KTXFunction(bpy.types.Operator):
    bl_idname="wm.ktx_function"
    bl_label="KTX Function"
    bl_options={'REGISTER','UNDO'}

    startx=bpy.props.FloatProperty(name="X min",
        description="X minimum value",
        default=-math.pi)
    endx=bpy.props.FloatProperty(name="X max",
        description="X maximum value",
        default=math.pi)
    starty=bpy.props.FloatProperty(name="Y min",
        description="Y minimum value",
        default=-math.pi)
    endy=bpy.props.FloatProperty(name="Y max",
        description="Y maximum value",
        default=math.pi)
    stepsx=bpy.props.IntProperty(name="Faces along X",
        description="How many faces in X direction",
        default=20)
    stepsy=bpy.props.IntProperty(name="Faces along Y",
        description="How many faces in Y direction",
        default=20)
    func=bpy.props.StringProperty(name="Function",
        description="Function to evaluate",
        default="math.sin(x)*math.cos(y)")

    def execute(self,context):
        msh=bpy.data.meshes.new('KTX Function')
        obj=bpy.data.objects.new('KTX Function',msh)
        bpy.data.scenes[0].objects.link(obj)
        bm=bmesh.new()

        if hasattr(bm.verts, "ensure_lookup_table"): 
            bm.verts.ensure_lookup_table()

        incx=(self.endx-self.startx)/self.stepsx
        incy=(self.endy-self.starty)/self.stepsy

        y=self.starty
        r=0
        while r<=self.stepsy:
            x=self.startx
            c=0
            while c<=self.stepsx:
                z=eval(self.func)
                bm.verts.new((x,y,z))
                c+=1
                x+=incx
            r+=1
            y+=incy

        offsetx=0
        r=0
        while r<self.stepsy:
            c=0
            while c<self.stepsx:
                bm.verts.ensure_lookup_table()
                f=[bm.verts[offsetx+c+1+self.stepsx],bm.verts[offsetx+c],bm.verts[offsetx+c+1],bm.verts[offsetx+c+2+self.stepsx]]
                bm.faces.new(f)
                c+=1
            r+=1
            offsetx+=self.stepsx
            offsetx+=1

        bm.to_mesh(msh)
        obj.data.update()
        return {'FINISHED'}

class KTXCylinders(bpy.types.Operator):
    bl_idname="wm.ktx_cylinders"
    bl_label="KTX Cylinders"
    bl_options={'REGISTER','UNDO'}

    mesh=bpy.props.BoolProperty(name="Mesh/Curve",
        description="on=Mesh, off=Curve",
        default=True)
    startrad=bpy.props.FloatProperty(name="Start Radius",
        description="Cylinder Start Radius",
        default=0.01,min=0.001,precision=4,step=1)
    sizefactor=bpy.props.FloatProperty(name="Size Factor",
        description="Multiplication Factor",
        default=1.7,precision=4,step=1)
    count=bpy.props.IntProperty(name="Count",
        description="Number of Circles",
        default=8)
    segments=bpy.props.IntProperty(name="Cylinder Segments",
        description="Number of Circle Segments",
        default=32)
    startheight=bpy.props.FloatProperty(name="Start Height",
        description="Cylinder Start Height",
        default=0.01,precision=4,step=1)
    heightmode=bpy.props.BoolProperty(name="Height Mode",
        description="off=Increment, on=Multiplication",
        default=True)
    heightfactor=bpy.props.FloatProperty(name="Height Factor",
        description="Cylinder Height Inc. Factor",
        default=1.1,precision=4,step=1)
    heightoption=bpy.props.BoolProperty(name="Height Option",
        description="off=from center, on=from bottom",
        default=True)
    angle=bpy.props.FloatProperty(name="Calculated Angle",
        description="Angle is Calculated",
        default=1.00000,precision=4)


    def execute(self,context):
        angle=math.asin(((self.startrad*self.sizefactor)-self.startrad)/((self.startrad*self.sizefactor)+self.startrad))
        x=self.startrad/math.sin(angle)
        self.angle=math.degrees(angle)
        rad=self.startrad
        height=self.startheight
        for number_of_cylinders in range(0,self.count):
           if self.heightoption:
              z=height/2
           else:
              z=0
           if self.mesh:
            bpy.ops.mesh.primitive_cylinder_add(vertices=self.segments, radius=rad, depth=height, location=(x,0,z))
           else:
            bpy.ops.curve.primitive_bezier_circle_add(radius=rad, location=(x,0,0))
            obj=bpy.context.active_object
            obj.data.extrude=height
            obj.data.dimensions='2D'
            obj.data.fill_mode='BOTH'
           rad_old=rad
           rad*=self.sizefactor
           x+=rad_old+rad
           if self.heightmode:
              height*=self.heightfactor
           else:
              height+=self.heightfactor
        return {'FINISHED'}

class KTXCylinderGrid(bpy.types.Operator):
    bl_idname="wm.ktx_cylinder_grid"
    bl_label="KTX Cylinder Grid"
    bl_options={'REGISTER','UNDO'}

    mesh=bpy.props.BoolProperty(name="Mesh/Curve",
        description="on=Mesh, off=Curve",
        default=True)
    radius=bpy.props.FloatProperty(name="Radius",
        description="Cylinder Radius",
        default=0.01,min=0.001,precision=4,step=1)
    radsup=bpy.props.FloatProperty(name="Radius Supplement",
        description="Cylinder Radius Extra",
        default=0.0,precision=4,step=0.01)
    height=bpy.props.FloatProperty(name="Height",
        description="Cylinder Height",
        default=0.01,precision=4,step=1)
    segments=bpy.props.IntProperty(name="Cylinder Segments",
        description="Number of Circle Segments",
        default=32)
    countx=bpy.props.IntProperty(name="Count X",
        description="Number of Cylinders on X-axis",
        default=8)
    county=bpy.props.IntProperty(name="Count Y",
        description="Number of Cylinders on Y-axis",
        default=8)

    def execute(self,context):
        x=0
        y=0
        for v in range(0,self.county):
           if operator.mod(v,2)==0:
              x=0
           else:
              x=self.radius
           for u in range(0,self.countx):
              if self.mesh:
               bpy.ops.mesh.primitive_cylinder_add(vertices=self.segments, radius=self.radius+self.radsup, depth=self.height, location=(x,y,0))
              else:
               bpy.ops.curve.primitive_bezier_circle_add(radius=self.radius+self.radsup, location=(x,y,0))
               obj=bpy.context.active_object
               obj.data.extrude=self.height
               obj.data.dimensions='2D'
               obj.data.fill_mode='BOTH'
              x+=2*self.radius
           y+=2*self.radius*math.sqrt(0.75)

        return {'FINISHED'}

class KTXObjectGrid(bpy.types.Operator):
    bl_idname="wm.ktx_object_grid"
    bl_label="KTX Object Grid"
    bl_options={'REGISTER','UNDO'}

    linkedcopy = bpy.props.BoolProperty(name="Linked Copies",
        description="Make a Linked copy",
        default=False)
    trisq = bpy.props.BoolProperty(name="Triangular or Square",
        description="on=Triangular, off=Square",
        default=True)

    radius=bpy.props.FloatProperty(name="Triangular Distance",
        description="Triangular Distance",
        default=0.01,min=0.001,precision=4,step=0.1)
    countx=bpy.props.IntProperty(name="Count X",
        description="Number of Cylinders on X-axis",
        default=8)
    county=bpy.props.IntProperty(name="Count Y",
        description="Number of Cylinders on Y-axis",
        default=8)

    def execute(self,context):
       x=0
       y=0
       obj=bpy.context.active_object
       if obj:
        for v in range(0,self.county):
         if self.trisq:
           if operator.mod(v,2)==0:
              x=0
           else:
              x=self.radius
         else:
           x=0
         for u in range(0,self.countx):
              if not (u==0 and v==0):
               bpy.ops.object.duplicate(linked=self.linkedcopy)
               obj=bpy.context.active_object
               obj.location=(x,y,0)
              x+=2*self.radius
         if self.trisq:
          y+=2*self.radius*math.sqrt(0.75)
         else:
          y+=2*self.radius
       return {'FINISHED'}

class KTXPolarArray(bpy.types.Operator):
    bl_idname="wm.ktx_polar_array"
    bl_label="KTX Polar Array"
    bl_options={'REGISTER','UNDO'}

    linkedcopy = bpy.props.BoolProperty(name="Linked Copies",
        description="Make a Linked copy",
        default=False)
    startang=bpy.props.FloatProperty(name="Start Angle",
        description="Start Angle",
        default=0.0)
    endang=bpy.props.FloatProperty(name="End Angle",
        description="End Angle",
        default=360.0)
    count=bpy.props.IntProperty(name="Number of Items",
        description="Number of Arrayed Items",
        default=8)
   

    def execute(self,context):
      inc=(360/self.count)
      angle=math.radians(self.startang)
      obj=bpy.context.active_object
      while angle <= self.endang:
        x=math.sin(math.radians(angle))
        y=math.cos(math.radians(angle))
        bpy.ops.object.duplicate(linked=self.linkedcopy)
        obj=bpy.context.active_object
        obj.rotation_euler=(0,0,math.radians(-angle))
        angle+=inc
      return {'FINISHED'}



class KTXPolarArray_old(bpy.types.Operator):
    bl_idname="wm.ktx_polar_array_old"
    bl_label="KTX Polar Array Old"
    bl_options={'REGISTER','UNDO'}

    linkedcopy = bpy.props.BoolProperty(name="Linked Copies",
        description="Make a Linked copy",
        default=False)
    startang=bpy.props.FloatProperty(name="Start Angle",
        description="Start Angle",
        default=0.0)
    endang=bpy.props.FloatProperty(name="End Angle",
        description="End Angle",
        default=360.0)
    count=bpy.props.IntProperty(name="Number of Items",
        description="Number of Arrayed Items",
        default=8)
   

    def execute(self,context):
      inc=(360/self.count)
      angle=math.radians(self.startang)
      obj=bpy.context.active_object
      while angle <= self.endang:
        x=math.sin(math.radians(angle))
        y=math.cos(math.radians(angle))
        bpy.ops.object.duplicate(linked=self.linkedcopy)
        obj=bpy.context.active_object
        obj.location=(x,y,0)
        obj.rotation_euler=(0,0,math.radians(-angle))
        angle+=inc
      return {'FINISHED'}

class KTXSpiralCircles(bpy.types.Operator):
    bl_idname="wm.ktx_spiral_circles"
    bl_label="KTX Circles on a spiral"
    bl_options={'REGISTER','UNDO'}

    cadd = bpy.props.BoolProperty(name="Add Circles",
        description="Add Circles to Spiral",
        default=False)
    ctype = bpy.props.BoolProperty(name="Segm.Circle/Curve",
        description="on=Segmented Circle, off=Bezier Circle",
        default=False)
    linkedcopy = bpy.props.BoolProperty(name="Linked Copies",
        description="Make a Linked copy",
        default=False)
    startrad = bpy.props.FloatProperty(name="Start Radius",
        description="Start Radius",
        default=1.0)
    rincrement=bpy.props.FloatProperty(name="Radius Increment",
        description="Radius Increment",
        default=0.1)

    startang=bpy.props.FloatProperty(name="Start Angle",
        description="Start Angle",
        default=0.0)
    endang=bpy.props.FloatProperty(name="End Angle",
        description="End Angle",
        default=360.0)
    increment=bpy.props.FloatProperty(name="Angle Increment",
        description="Angle Increment",
        default=10.0)
    zincrement=bpy.props.FloatProperty(name="Z Increment",
        description="Z Increment",
        default=0.0)
    height=bpy.props.FloatProperty(name="Circle Height",
        description="Curve Circle Extrude Height",
        default=0.1)
    csegments=bpy.props.IntProperty(name="Circle Segments",
        description="Circle Segments",
        default=16)


    def twopcircle(self,point_1,point_2):
       origin_x=(point_1[0]+point_2[0])/2.0
       origin_y=(point_1[1]+point_2[1])/2.0
       a=math.pow((point_2[0]-point_1[0]),2)
       b=math.pow((point_2[1]-point_1[1]),2)
       radius=math.sqrt(a+b)/2.0
       return(origin_x,origin_y,radius)

    def circle(self,origin_x,origin_y,origin_z,radius,segments):
       for angle in range(0,round(360+segments),round(360/segments)):
         x=origin_x+math.cos(math.radians(angle))*radius
         y=origin_y+math.sin(math.radians(angle))*radius
         s.verts.new((x,y,0))
         if not (angle==0 or angle==round(360+segments)):
            s.edges.new((s.verts[-2],s.verts[-1]))
       return('True')

    def execute(self,context):
       import math, bmesh
       from math import radians
       msh=bpy.data.meshes.new('KTX Spiral')
       obj=bpy.data.objects.new('KTX Spiral',msh)
       bpy.data.scenes[0].objects.link(obj)
       s=bmesh.new()
       angle=self.startang
       r=self.startrad
       z=self.zincrement
       while angle<=self.endang:
         x=math.cos(math.radians(angle))*r
         y=math.sin(math.radians(angle))*r
         s.verts.new((x,y,z))
         if angle>self.startang:
          s.verts.ensure_lookup_table()
          s.edges.new((s.verts[-2],s.verts[-1]))
          circ=self.twopcircle(s.verts[-2].co,s.verts[-1].co)
          bpy.ops.curve.primitive_bezier_circle_add(radius=circ[2], location=(circ[0],circ[1],z))
          obj1=bpy.context.active_object
          obj1.data.extrude=self.height
          obj1.data.dimensions='2D'
          obj1.data.fill_mode='BOTH'

         r+=self.rincrement
         angle+=self.increment
         z+=self.zincrement


       s.to_mesh(msh)
       obj.data.update()
       return {'FINISHED'}


class KTXPolish(bpy.types.Operator):
    bl_idname = "wm.ktx_polish"
    bl_label = "Polish"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.03
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].segments = 2
        bpy.context.object.modifiers["Bevel"].profile = 1
        bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
        bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
        bpy.ops.object.modifier_remove(modifier="Subsurf")
        bpy.ops.object.subdivision_set(level=2)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.shade_smooth()
        bpy.ops.object.mode_set(mode = 'SCULPT')
        bpy.ops.sculpt.dynamic_topology_toggle()
        bpy.ops.sculpt.symmetrize()
        return {'FINISHED'}

class KTXTriTangle(bpy.types.Operator):
    bl_idname = "wm.ktx_tri_tangle"
    bl_label = "Create Ordered Tangle Triangle"
    bl_options = {'REGISTER','UNDO'}

    angletype = bpy.props.BoolProperty(name="Sharp Corner Angle",
        description="Sharp (60) or NonSharp (30) Corner Angle",
        default=False)

    vx = bpy.props.FloatProperty(name="Size X (mm)",
        description="Length of Side",
        default=44)
    vy = bpy.props.FloatProperty(name="Size Y (mm)",
        description="Height of Side",
        default=44)
    r = bpy.props.FloatProperty(name="Corner Radius",
        description="Corner Radius (mm)",
        default=4, min=0.0)

    bevel = bpy.props.BoolProperty(name="Bevel Corners",
        description="Bevel Corners",
        default=True)
    bevelr = bpy.props.FloatProperty(name="Bevel Radius",
        description="Bevel Radius",
        default=4.0, min=0.0)
    beveltype = bpy.props.BoolProperty(name="Only Long Edges",
        description="Bevel only the long edges",
        default=True)

    smooth = bpy.props.BoolProperty(name="Smooth",
        description="Smooth Surfaces",
        default=True)
    edgesplit = bpy.props.BoolProperty(name="Edge Split",
        description="Edge Split",
        default=False)

    sl = bpy.props.FloatProperty(name="Saw Length (mm)",
        description="Saw Length",
        default=0.0)


    def execute(self,context):
       from math import radians
       alpha = math.radians(90) - math.acos(1/3)
       a = (self.vy/100) / 2.0
       b = a * math.tan(alpha)
       c = a / math.cos(alpha)
       d = b + c
       e = (self.vx/100) / math.cos(math.radians(30))
       h = d + e
       f = math.sqrt(3) * h
       g = f
       h = d + e
       i1 = 2 * g * math.sqrt(3)
       i2 = i1 - e

       vx1 = (self.vx/100) - (2 * self.r)/100 + (2 * self.r * math.sin(radians(45)))/100

       factorx = i1 / (self.vx/100)
       i1x = factorx * vx1
       i2x = i1x - e

       g1 = math.tan(radians(30)) * 0.5 * i1x
       sharpdist = (self.vx/100) / math.tan(radians(30))

       if self.angletype:
        _a1x = g1-(self.vx/100)
        _a1y    = (0.5 * i1x) - sharpdist
        _b1x = g1
        _b1y = (0.5 * i1x)
        _c1x = g1
        _c1y = (-0.5 * i1x)
        _d1x = g1 - (self.vx/100)
        _d1y = (-0.5 * i1x) + sharpdist
        _z = (self.vy / 200)
        self.sl = i1x*100
       else:
        _a1x = g1-(self.vx/100)
        _a1y	= (0.5 * i1x) - sharpdist
        _b1x = g1
        _b1y = (0.5 * i1x) - e
        _c1x = g1
        _c1y = (-0.5 * i1x)
        _d1x = g1 - (self.vx/100)
        _d1y = (-0.5 * i1x) + sharpdist - e
        _z = (self.vy / 200)
        self.sl = i2x*100

       verts = [(_a1x,_a1y,_z),(_b1x,_b1y,_z),(_c1x,_c1y,_z),(_d1x,_d1y,_z),(_a1x,_a1y,-_z),(_b1x,_b1y,-_z),(_c1x,_c1y,-_z),(_d1x,_d1y,-_z)]
       faces = [(0,3,2,1),(1,2,6,5),(5,6,7,4),(3,0,4,7),(2,3,7,6),(0,1,5,4)]


       me = bpy.data.meshes.new('OrdTri_Mesh')
       me.from_pydata(verts,[],faces)
       me.update()

       ob = bpy.data.objects.new('OrdTri',me)
       ob.location = (0,0,0)
       bpy.context.scene.objects.link(ob)
       ob.select=True
       bpy.context.scene.objects.active=ob
       if self.smooth:
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth=True
       if self.bevel:
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].offset_type = 'WIDTH'
        bpy.context.object.modifiers["Bevel"].segments = 5
        bpy.context.object.modifiers["Bevel"].width = self.bevelr/100
        if self.beveltype:
         bpy.context.object.modifiers["Bevel"].limit_method='WEIGHT'
         me.use_customdata_edge_bevel = True
         me.edges[3].bevel_weight=1.0
         me.edges[6].bevel_weight=1.0
         me.edges[7].bevel_weight=1.0
         me.edges[10].bevel_weight=1.0
       if self.edgesplit:
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers['EdgeSplit'].split_angle = 3.14159

       bpy.ops.object.duplicate(linked=True)
       obj=bpy.context.active_object
       obj.rotation_euler=(0,0,math.radians(120))

       bpy.ops.object.duplicate(linked=True)
       obj1=bpy.context.active_object
       obj1.rotation_euler=(0,0,math.radians(240))

       ob.select=True
       obj.select=True
       obj1.select=True
       bpy.ops.object.duplicate_move_linked()
       bpy.ops.transform.rotate(value=math.radians(180), axis=(0,0,1))
       bpy.ops.transform.rotate(value=math.radians(70.5287793655), axis=(1,0,0))
       bpy.ops.object.duplicate_move_linked()
       bpy.ops.transform.rotate(value=math.radians(120), axis=(0,0,1))
       bpy.ops.object.duplicate_move_linked()
       bpy.ops.transform.rotate(value=math.radians(120), axis=(0,0,1))


       return {'FINISHED'}

class KTXSpiroGraph2(bpy.types.Operator):
    bl_idname="wm.ktx_spirograph_2"
    bl_label="KTX Make a Spirograph 2"
    bl_options={'REGISTER','UNDO', 'PRESET'}

    fact1 = bpy.props.FloatProperty(name="Factor 1",
        description="Factor 1",
        default=5.0)
    fact2 = bpy.props.FloatProperty(name="Factor 2",
        description="Factor 2",
        default=28.0)
    fact3 = bpy.props.FloatProperty(name="Factor 3",
        description="Factor 3",
        default=7.0)
    fact4 = bpy.props.FloatProperty(name="Factor 4",
        description="Factor 4",
        default=8.0)
    fact5 = bpy.props.FloatProperty(name="Factor 5",
        description="Factor 5",
        default=0.0)
    fact6 = bpy.props.FloatProperty(name="Factor 6",
        description="Factor 6",
        default=12.0)

    functx = bpy.props.StringProperty(name="Function x",
        description="Function x",
        default="f1*math.cos(f2*a)+f3*math.sin(f4*a)+f5*math.cos(f6*a)")
    functy = bpy.props.StringProperty(name="Function y",
        description="Function y",
        default="f1*math.sin(f2*a)+f3*math.cos(f4*a)+f5*math.sin(f6*a)")
    functz = bpy.props.StringProperty(name="Function z",
        description="Function z",
        default="f5*math.sin(f6*a)")

    endangle=bpy.props.IntProperty(name="Angle",
        description="Angle",
        default=3600)
    increment=bpy.props.FloatProperty(name="Angle Increment",
        description="Angle Increment",
        default=1.0)


    def execute(self,context):
       import math, bmesh
       from math import radians
       msh=bpy.data.meshes.new('KTX Spiral')
       obj=bpy.data.objects.new('KTX Spiral',msh)
       bpy.data.scenes[0].objects.link(obj)
       s=bmesh.new()
       z=0.0
       angle=0.0
       f1=self.fact1/10
       f2=self.fact2/10
       f3=self.fact3/10
       f4=self.fact4/10
       f5=self.fact5/10
       f6=self.fact6/10

       while angle<=self.endangle:
#         x=self.fact7/10*math.cos(math.radians(angle))+self.fact1/10*math.sin(self.fact2/10*math.radians(angle))+self.fact3/10*math.cos(self.fact4/10*math.radians(angle))+self.fact5/10*math.cos(self.fact6/10*math.radians(angle))
#         y=self.fact7/10*math.sin(math.radians(angle))+self.fact1/10*math.cos(self.fact2/10*math.radians(angle))+self.fact3/10*math.sin(self.fact4/10*math.radians(angle))+self.fact5/10*math.sin(self.fact6/10*math.radians(angle))
         a=math.radians(angle)
         x=eval(self.functx)
         y=eval(self.functy)
         z=eval(self.functz)

         s.verts.new((x,y,z))
         if angle > 0:
          s.verts.ensure_lookup_table()
          s.edges.new((s.verts[-2],s.verts[-1]))
         if angle>self.endangle:
          s.verts.ensure_lookup_table()
          s.edges.new((s.verts[-2],s.verts[-1]))

         angle+=self.increment

       s.to_mesh(msh)
       obj.data.update()
       return {'FINISHED'}


class KTXObjLib(bpy.types.Operator):
    bl_idname="wm.ktx_objlib"
    bl_label="KTX Object Library"
    bl_options={'REGISTER','UNDO'}

    def mode_options(self,context):
      import os
      filepath = os.path.join(os.path.sys.path[1],'KTX_Objects.blend')
      with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
        return [(ob,ob,"") for ob in data_from.objects]


    count=bpy.props.EnumProperty(items=mode_options,
        description="KTX Object Library",
        name="Objects found in Library")


    def execute(self,context):
      import os
      scn = bpy.context.scene
      filepath = os.path.join(os.path.sys.path[1],'KTX_Objects.blend')
      with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
       data_to.objects = [name for name in data_from.objects if name.startswith(self.count)]
      for obj in data_to.objects:
       if obj is not None:
        scn.objects.link(obj)
      return {'FINISHED'}

class KTXBottle(bpy.types.Operator):
    bl_idname="wm.ktx_bottle_1"
    bl_label="KTX Create a Bottle and Cap"
    bl_options={'REGISTER','UNDO', 'PRESET'}

    expert_mode = bpy.props.BoolProperty(name="Expert Mode",
        description="Tweak bottle/cap shape On/Off",
        default=False)
    hide_bottle = bpy.props.BoolProperty(name="Hide Bottle",
        description="Hide Bottle On/Off",
        default=False)
    hide_cap = bpy.props.BoolProperty(name="Hide Cap",
        description="Hide Cap On/Off",
        default=False)
    comp_bot = bpy.props.BoolProperty(name="Generate Complete Bottle",
        description="Generate Complete Bottle or only Threads",
        default=True)

    overall_scale = bpy.props.FloatProperty(name="Overall Scale",
        description="Overall Scale",
        default=0.1)
    v = bpy.props.IntProperty(name="Vertices",
        description="Cylinder divided into this many Vertices",
        default=12,min=3,max=24)
    thread_height = bpy.props.FloatProperty(name="Thread Height",
        description="Thread Height",
        default=1.0)
    thread_steps = bpy.props.IntProperty(name="Thread Steps",
        description="Thread Steps",
        default=28)
    neck_radius = bpy.props.FloatProperty(name="Neck Radius",
        description="Neck Radius",
        default=2.0)
    trap = bpy.props.FloatProperty(name="Trapezium Thread",
        description="Trapezium Thread",
        default=0.15)
    depth = bpy.props.FloatProperty(name="Depth",
        description="Depth",
        default=0.44)
    eoff_onoff = bpy.props.BoolProperty(name="Enlarge Cap",
        description="Enlarge Cap (to prevent intersection between threads",
        default=False)
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
        default=False)
    subs_onoff = bpy.props.BoolProperty(name="SubSurf",
        description="SubSurf On/Off",
        default=True)
    nl = bpy.props.FloatProperty(name="Neck Length",
        description="Neck Length",
        default=0.1)
    x1 = bpy.props.FloatProperty(name="x1",
        description="x1",
        default=4.0,)
    z1 = bpy.props.FloatProperty(name="z1",
        description="z1",
        default=2.09)
    x2 = bpy.props.FloatProperty(name="x2",
        description="x2",
        default=4.0)
    z2 = bpy.props.FloatProperty(name="z2",
        description="z2",
        default=5.0)
    x3 = bpy.props.FloatProperty(name="x3",
        description="x3",
        default=3.4)
    z3 = bpy.props.FloatProperty(name="z3",
        description="z3",
        default=15.0)
    x4 = bpy.props.FloatProperty(name="x4",
        description="x4",
        default=2.0)
    z4 = bpy.props.FloatProperty(name="z4",
        description="z4",
        default=15.0)
    x5 = bpy.props.FloatProperty(name="x5",
        description="x5",
        default=1.2)
    z5 = bpy.props.FloatProperty(name="z5",
        description="z5",
        default=15.0)
    tl = bpy.props.FloatProperty(name="Top Length",
        description="Top Length",
        default=0.1,min=0.001)
    tt = bpy.props.FloatProperty(name="Top Tickness",
        description="Top Tickness",
        default=0.3,min=0.001)
    x6 = bpy.props.FloatProperty(name="x6",
        description="x6",
        default=3.14)
    z6 = bpy.props.FloatProperty(name="z6",
        description="z6",
        default=2.0)
    x7 = bpy.props.FloatProperty(name="x7",
        description="x7",
        default=2.7)
    z7 = bpy.props.FloatProperty(name="z7",
        description="z7",
        default=12.0)
    x8 = bpy.props.FloatProperty(name="x8",
        description="x8",
        default=1.9)
    z8 = bpy.props.FloatProperty(name="z8",
        description="z8",
        default=14.0)

    x9 = bpy.props.FloatProperty(name="x9",
        description="x9",
        default=1.9)
    z9 = bpy.props.FloatProperty(name="z9",
        description="z9",
        default=4.5)
    x10 = bpy.props.FloatProperty(name="x10",
        description="x10",
        default=0.1)
    z10 = bpy.props.FloatProperty(name="z10",
        description="z10",
        default=5.0)

    @classmethod
    def poll(self, context):
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'comp_bot')
        if self.comp_bot:
            col.prop(self, 'expert_mode')
        col.separator()
        col.prop(self, 'hide_bottle')
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
        if self.expert_mode and self.comp_bot:
            col.label(text='Bottle Outside Shape')
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
            col.label(text='Bottle Inside Shape')
            col.prop(self,'x6')
            col.prop(self,'z6')
            col.prop(self,'x7')
            col.prop(self,'z7')
            col.prop(self,'x8')
            col.prop(self,'z8')
            col.separator()
            col.label(text='Cap Shape')
            col.prop(self,'x9')
            col.prop(self,'z9')
            col.prop(self,'x10')
            col.prop(self,'z10')



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
#       bm.edges.ensure_lookup_table()
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
           v3=bm.verts.new((self.neck_radius+self.x1, 0.0, -self.z1))
           v4=bm.verts.new((self.neck_radius+self.x2, 0.0, -self.z2))
           v5=bm.verts.new((self.neck_radius+self.x3, 0.0, -self.z3))
           v6=bm.verts.new((self.neck_radius+self.x4, 0.0, -self.z4))
           v7=bm.verts.new((self.neck_radius+self.x5, 0.0, -self.z5))
           v8=bm.verts.new((0.0, 0.0, -self.z5))
           bm.edges.new((v1,v2))
           bm.edges.new((v2,v3))
           bm.edges.new((v3,v4))
           bm.edges.new((v4,v5))
           bm.edges.new((v5,v6))
           bm.edges.new((v6,v7))
           bm.edges.new((v7,v8))
           bmesh.ops.spin(bm,geom=bm.verts[-8:]+bm.edges[-7:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
#----------Top
       aa=((self.thread_height/self.v)*self.thread_steps)+self.thread_height
       bb=self.thread_steps%self.v

       v1=bm.verts.new((self.neck_radius, 0.0, aa))
       bmesh.ops.rotate(bm,verts=[v1],cent=(0.0,0.0,0.0),matrix=mathutils.Matrix.Rotation(((2*math.pi)/self.v)*bb,3,'Z'))
       bmesh.ops.spin(bm,geom=[v1],axis=(0.0,0.0,-1.0),cent=(0,0,0),dvec=(0,0,-self.thread_height/self.v),angle=(2.0 * math.pi),steps=self.v,use_duplicate=0)
#       bm.edges.ensure_lookup_table()
       ret=bmesh.ops.extrude_edge_only(bm,edges=bm.edges[-self.v:])
       geom_new = ret["geom"]
       del ret
       verts_new=[ele for ele in geom_new if isinstance(ele, bmesh.types.BMVert)]
       bmesh.ops.scale(bm,verts=verts_new,vec=(1.0,1.0,0.0))
       ret_boven=bmesh.ops.translate(bm,verts=verts_new,vec=(0.0,0.0,aa))
#---------BottleInside
       if self.comp_bot:
           if self.tt >= self.neck_radius:
               self.tt = self.neck_radius - 0.1
           v1=bm.verts.new((self.neck_radius, 0.0, aa))
           v2=bm.verts.new((self.neck_radius, 0.0, aa+self.tl))

           v3=bm.verts.new((self.neck_radius-self.tt, 0.0, aa+self.tl))
           v3a=bm.verts.new((self.neck_radius-self.tt, 0.0, aa-self.tl))

           v4=bm.verts.new((self.neck_radius-self.tt, 0.0, -1.0))
           v4a=bm.verts.new((self.neck_radius-self.tt, 0.0, -1.2))

           v5=bm.verts.new((self.neck_radius+self.x6, 0.0, -self.z6))
           v6=bm.verts.new((self.neck_radius+self.x7, 0.0, -self.z7))
           v7=bm.verts.new((self.neck_radius+self.x8, 0.0, -self.z8))
           v8=bm.verts.new((0.0, 0.0, -self.z8))
           bm.edges.new((v8,v7))
           bm.edges.new((v7,v6))
           bm.edges.new((v6,v5))
           bm.edges.new((v5,v4a))
           bm.edges.new((v4a,v4))
           bm.edges.new((v4,v3a))
           bm.edges.new((v3a,v3))
           bm.edges.new((v3,v2))
           bm.edges.new((v2,v1))

           bmesh.ops.spin(bm,geom=bm.verts[-10:]+bm.edges[-9:],axis=(0.0,0.0,1.0),cent=(0,0,0),dvec=(0,0,0.0),angle=(2.0*math.pi),steps=self.v,use_duplicate=0)

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
       obj.location.z = (obj.location.z + self.z5)*self.overall_scale
       scene.objects.link(obj)
       if self.subs_onoff:
           obj.modifiers.new("subd", type='SUBSURF')
           obj.modifiers['subd'].levels = 3

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
#       bm.edges.ensure_lookup_table()
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

#       bm.edges.ensure_lookup_table()
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
           v2=bm.verts.new((self.neck_radius+self.depth+ca, 0.0, -self.nl))
           v3=bm.verts.new((self.neck_radius+self.depth+self.tt+ca, 0.0, self.nl))
           v4=bm.verts.new((self.neck_radius+self.depth+self.x9+ca, 0.0, self.z9))
           v5=bm.verts.new((self.neck_radius+self.depth+self.x10+ca, 0.0, self.z10))
           v6=bm.verts.new((0.0, 0.0, self.z10))
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
       obj.location.z = (obj.location.z + self.thread_height/2 + self.z5)*self.overall_scale
       scene.objects.link(obj)
       if self.subs_onoff:
           obj.modifiers.new("subd", type='SUBSURF')
           obj.modifiers['subd'].levels = 3
       
       bpy.context.scene.objects.active = obj
       bpy.ops.object.mode_set(mode='EDIT')
       bpy.ops.mesh.select_all(action='SELECT')
       bpy.ops.mesh.normals_make_consistent(inside=False)
       bpy.ops.object.editmode_toggle()

       if self.hide_cap:
           bpy.context.object.hide = True
       else:
           bpy.context.object.hide = False

       return {'FINISHED'}




class KTXBottle2(bpy.types.Operator):
    bl_idname="wm.ktx_bottle_2"
    bl_label="KTX Create a Bottle and Cap v2"
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
        default=1.0)
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
        default=1.0,min=0.1)
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

    x1 = bpy.props.FloatProperty(name="X1",
        description="X1",
        default=1.0)
    z1 = bpy.props.FloatProperty(name="Z1",
        description="Z1",
        default=1.0)
    x2 = bpy.props.FloatProperty(name="X2",
        description="X2",
        default=2.0)
    z2 = bpy.props.FloatProperty(name="Z2",
        description="Z2",
        default=2.0)
    x3 = bpy.props.FloatProperty(name="X3",
        description="X3",
        default=1.0)
    z3 = bpy.props.FloatProperty(name="Z3",
        description="Z3",
        default=4.0)
    x4 = bpy.props.FloatProperty(name="X4",
        description="X4",
        default=1.0)
    z4 = bpy.props.FloatProperty(name="Z4",
        description="Z4",
        default=5.0)
    x5 = bpy.props.FloatProperty(name="X5",
        description="X5",
        default=0.5)
    z5 = bpy.props.FloatProperty(name="Z5",
        description="Z5",
        default=5.0)

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
           obj.modifiers['subd'].levels = 3

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
           obj.modifiers['subd'].levels = 3
   
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
               obj.modifiers["subd"].levels = 3


           bpy.context.scene.objects.active = obj

           if self.hide_bottle_body:
               bpy.context.object.hide = True
           else:
               bpy.context.object.hide = False


       return {'FINISHED'}







class KTXPanel( bpy.types.Panel ):
    bl_label = "KosteX Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "KTX"
    bl_context = "objectmode"
    
    def draw( self, context ):
        scn = context.scene
        layout = self.layout
        new_col = self.layout.column
        new_col().column().operator("wm.ktx_bottle_1")
        new_col().column().operator("wm.ktx_bottle_2")
        new_col().column().separator()
        new_col().column().operator("wm.ktx_tri_tangle")
        new_col().column().operator("wm.ktx_function")
        new_col().column().operator("wm.ktx_cylinders")
        new_col().column().operator("wm.ktx_cylinder_grid")
        new_col().column().operator("wm.ktx_object_grid")
        new_col().column().operator("wm.ktx_polar_array")
        new_col().column().operator("wm.ktx_spiral_circles")
        new_col().column().operator("wm.ktx_spirograph_2")
        new_col().column().operator("wm.ktx_add_random_cubes")
        new_col().column().operator("wm.ktx_add_random_copies")
        new_col().column().separator()
        new_col().column().operator("wm.ktx_objlib")
        new_col().column().separator()
        new_col().column().operator("wm.ktx_erase_all_materials")
        new_col().column().operator("wm.ktx_erase_unused_textures")
        new_col().column().operator("wm.ktx_erase_unused_palettes")
        new_col().column().separator()
        new_col().column().operator("wm.ktx_add_subsurf_creases")
        new_col().column().operator("wm.ktx_polish")
        new_col().column().separator()
        new_col().column().operator("wm.ktx_assign_materials")
        new_col().column().operator("wm.ktx_assign_random_diffuse_colors")
        new_col().column().operator("wm.ktx_add_glossy_mix_shaders")
        new_col().column().operator("wm.ktx_set_viewport_color")



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
