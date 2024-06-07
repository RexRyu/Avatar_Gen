import bpy
import os
import glob
import sys

avatar_path = "output/"
avatar_list = glob.glob(avatar_path+"*")
#avatar_list = glob.glob(os.path.join(avatar_path, "*"))

for filename in avatar_list:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    
    bpy.ops.import_scene.obj(filepath=filename+"/"+os.path.basename(filename)+".obj")
    bpy.ops.export_scene.fbx(filepath=filename+"/"+os.path.basename(filename)+".fbx", embed_textures=True, path_mode='COPY')
    