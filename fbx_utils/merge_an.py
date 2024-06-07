import glob
import os
import json
import random
import bpy

from mergehair import main as mergehair
from mergebody import main as mergebody

def get_random_file(path, extension="*.fbx"):
    files = glob.glob(os.path.join(path, extension))
    return os.path.basename(random.choice(files))

def load_config(config_path, key):
    with open(config_path, "r") as json_file:
        config = json.load(json_file)
        return config.get(key)

def apply_transformations():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def export_glb(filepath):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_selected=False,
        export_apply=True,
        export_texture_dir="textures"  # Set the texture export directory if needed
    )

def main():
    body_path = "fbx_utils/body/"
    hair_path = "fbx_utils/hair/"
    avatar_path = "output/"

    # Randomly select a body and hair file
    body = get_random_file(body_path)
    hair = get_random_file(hair_path)

    # Print the selected body and hair files
    print(f"Selected body file: {body}")
    print(f"Selected hair file: {hair}")

    # Load configurations
    body_name = os.path.splitext(body)[0]
    config_body = load_config("fbx_utils/config_body.json", body_name)

    hair_name = os.path.splitext(hair)[0]
    config_hair = load_config("fbx_utils/config_hair.json", hair_name)

    avatar_list = glob.glob(avatar_path + "*")

    for filename in avatar_list:
        head_fbx = os.path.join(filename, os.path.basename(filename) + ".fbx")
        hair_fbx = os.path.join(filename, os.path.basename(filename) + "-hair.fbx")
        merged_fbx = os.path.join(filename, os.path.basename(filename) + "-merge.fbx")
        merged_glb = os.path.join(filename, os.path.basename(filename) + "-merge.glb")

        # Merge hair with head
        mergehair(head=head_fbx, hair=os.path.join(hair_path, hair), config=config_hair, out=hair_fbx)

        # Merge body with head and hair
        mergebody(head=hair_fbx, body=os.path.join(body_path, body), config=config_body, out=merged_fbx)

        # Clear all data to avoid conflicts and import the merged FBX
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.fbx(filepath=merged_fbx)

        # Apply transformations
        apply_transformations()

        # Export as .glb file
        export_glb(merged_glb)

if __name__ == "__main__":
    main()
