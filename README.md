# BlenderScripts

My Collection of Blender 3D python scripts.
Got any questions? Contact me.. glad to help!

### Disclaimer
Please be aware that Clone/Download won't give you a Blender installation file.
Just copy the files you want to your scripts folder.

### Noteworthy Addons
**KTX_Bottle_2.py**
An addon to generate a threaded bottle and cap. Lots of parameters to tweak.
This is the only file needed when you want the Bottle/Cap script.
_Watch me creating one [here](https://www.youtube.com/watch?v=kT9oI_CdcBA)_

**KTX_Tools.py**
A collection of unrelated tools I've created through the years.. mostly for testing/training purposes.
(Holds both version 1 and 2 of the Bottle/Cap script.)

**KTX_MeshVersions.py**
An addon to save/restore versions of meshes during editing.
_Watch me using the addon [here](https://www.youtube.com/watch?v=bcxVqEOMXgw)_
>This addon has been added to [Blender Contrib](https://git.blender.org/gitweb/gitweb.cgi/blender-addons-contrib.git/blob/HEAD:/object_mesh_versions.py). No need to download anymore, unless you want latest versions or branches

**KTX_Selectbuffer.py**
An addon to enable a select buffer. Select something, add it to a buffer. Select others and do a boolean selection on the previous selection.
_Watch me using the addon [here](https://www.youtube.com/watch?v=I8Xc9U37f0Q)_
>This addon has been added to [Blender Contrib](https://git.blender.org/gitweb/gitweb.cgi/blender-addons-contrib.git/blob/HEAD:/mesh_selectbuffer.py). No need to download anymore, unless you want latest versions or branches

**KTX_RenderSlot.py**
An addon to add a quick Render slot selection in the render panel and show which renderslots are already occupied.
>This addon has been added to [Blender Contrib](https://git.blender.org/gitweb/gitweb.cgi/blender-addons-contrib.git/blob/HEAD:/render_renderslot.py). No need to download anymore, unless you want latest versions or branches

### Notes
* KTX_Library_* will add themselves to your ADD MESH menu
* KTX_Library_Materials.py needs KTX_Objects.blend (put your own materials in that blend file)
* KTX_Library_NodeGroups.py needs KTX_Objects.blend (put your own nodegroups in that blend file)
* KTX_Library_Objects.py needs KTX_Objects.blend (put your own objects in that blend file)
* KTX_Library_Import_OBJ holds a script to import OBJ files.. but you have to edit the script and change line 22 to point to your OBJ folder
* KTX_Tools.py only needs KTX_Objects.blend if you want to use the simple version of KTX Object Library inside it
