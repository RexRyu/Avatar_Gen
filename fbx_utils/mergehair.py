import fbx
from FbxCommon import InitializeSdkObjects, LoadScene, SaveScene
from pathlib import Path
import os

def main(head, hair, config, out):
    manager, head_scene = InitializeSdkObjects()
    hair_scene = fbx.FbxScene.Create(manager, "")

    try:
        LoadScene(manager, head_scene, str(Path(head).resolve()))
        LoadScene(manager, hair_scene, str(Path(hair).resolve()))
        
        # 머리 붙이기
        destination_node_name = os.path.splitext(os.path.basename(head))[0]
        destination_node = find(head_scene.GetRootNode(), destination_node_name) # : head
        print(destination_node,"d_node_head")
        if destination_node is None:
            print("none")
            return

        for i in range(hair_scene.GetRootNode().GetChildCount()):
            child = hair_scene.GetRootNode().GetChild(i)
            print(child,"child")
            destination_node.AddChild(child)
            child.LclScaling.Set(fbx.FbxDouble3(config["sx"], config["sy"], config["sz"]))
            child.LclTranslation.Set(fbx.FbxDouble3(config["x"], config["y"], config["z"]))
            child.LclRotation.Set(fbx.FbxDouble3(config["a"], config["b"], config["c"]))

        hair_scene.GetRootNode().DisconnectAllSrcObject()

        for i in range(hair_scene.GetSrcObjectCount()):
            obj = hair_scene.GetSrcObject(i)
            if obj == hair_scene.GetRootNode() or obj.GetName() == 'GlobalSettings':
                continue
            obj.ConnectDstObject(head_scene)

        hair_scene.DisconnectAllSrcObject()

        SaveScene(manager, head_scene, str(Path(out).resolve()), pEmbedMedia=True)
    finally:
        head_scene.Destroy()
        hair_scene.Destroy()
        manager.Destroy()


def find(node, name):
    if node.GetName() == name:
        return node

    for i in range(node.GetChildCount()):
        found = find(node.GetChild(i), name)
        if found is not None:
            return found

    return None


if __name__ == '__main__':
    main()
