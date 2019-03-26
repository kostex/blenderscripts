bl_info = {
    "name": "KTX Efficient Render Animation",
    "author": "Roel Koster",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties->Render",
    "description": "Skip same frames when rendering animation",
    "warning": "",
    "wiki_url": "",
    "category": "Render"
}


import bpy
import subprocess
from bpy.types import Panel
from bpy.props import StringProperty
import signal

abort = None

def handler(signum, frame):
    global abort
    abort = True
    print("\nAbort Render")
#    signal.default_int_handler(signum, frame)


class KTXRENDERSKIP_OT_Render(bpy.types.Operator):
    bl_label = "Render and skip"
    bl_idname = "ktxrenderskip.render"
    bl_description = "Render each frame and skip/copy same as previous"

    engine : StringProperty()

    def execute(self, context):
        global abort
        signal.signal(signal.SIGINT, handler)
        abort = False
        start = bpy.data.scenes['Scene'].frame_start
        end = bpy.data.scenes['Scene'].frame_end
        render_range = list(range(start, end))
        all_obj_fcurves = {}
        for obj in bpy.data.objects:
            obj_fcurves = {}

            try:
                obj.animation_data.action.fcurves
            except AttributeError:
                print("--|'%s' is not animated" % obj.name)
                continue

            print("\n--> '%s' is animated at frames:" % obj.name)

            for fr in list(range(start, end + 1)):
                fc_evals = [c.evaluate(fr)
                            for c in obj.animation_data.action.fcurves]
                obj_fcurves.update({int(fr): fc_evals})
                print(fr, end=", ")
            print()

            all_obj_fcurves.update({obj.name: obj_fcurves})

        still_frames = set(render_range)
        for obj in all_obj_fcurves.keys():
            obj_animated_frames = []
            for i, fr in enumerate(sorted(all_obj_fcurves[obj].keys())):
                if i != 0:
                    if all_obj_fcurves[obj][fr] != all_obj_fcurves[obj][fr_prev]:
                        obj_animated_frames.append(fr)
                fr_prev = fr

            still_frames = still_frames - set(obj_animated_frames)

        print("\nFound %d still frames" % len(still_frames))
        print(sorted(still_frames), end="\n\n")

        filepath = bpy.context.scene.render.filepath

        for fr in render_range:
            if abort:
                break
            if fr not in still_frames or fr == render_range[0]:
                bpy.context.scene.frame_set(fr)
                bpy.context.scene.render.filepath = filepath + '%04d' % fr
                if self.engine == "opengl":
                    bpy.ops.render.opengl(write_still=True)
                else:
                    bpy.ops.render.render(write_still=True)
            else:
                scene = bpy.context.scene
                abs_filepath = scene.render.frame_path(frame=scene.frame_current)
                abs_path = '/'.join(abs_filepath.split('/')[:-1]) + '/'
                print("Frame %d is still, copying from equivalent" % fr)
                subprocess.call(['cp', abs_path + '%04d.png' %
                                 (fr - 1), abs_path + '%04d.png' % fr])

        bpy.context.scene.render.filepath = filepath
        signal.signal(signal.SIGINT, signal.default_int_handler)
        return {'FINISHED'}


class KTXRENDERSKIP_PT_Panel(bpy.types.Panel):
    bl_label = "KTX Render Skip"
    bl_idname = "KTXRENDERSKIP_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        col.label(text="Start blender from terminal to interact!")
        col.label(text="Render Animation:")
        col.operator("ktxrenderskip.render", text="OpenGL Engine").engine = "opengl"
        col.operator("ktxrenderskip.render", text="Current Engine").engine = "current"


classes = (
    KTXRENDERSKIP_OT_Render,
    KTXRENDERSKIP_PT_Panel
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
