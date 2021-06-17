import bpy
import bpy_extras
import json
import os
import math
import mathutils
from bpy_extras.io_utils import ExportHelper, axis_conversion
from bpy.props import StringProperty


class Vector3():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, l: list):
        return cls(l[0], l[1], l[2])

    # In Minecraft Y axis is up. So Z and Y are swapped
    def toJSON(self):
        vectorTemplate = {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
        return vectorTemplate

    def __str__(self):
        return "x={0} y={1} z={2}".format(self.x, self.y, self.z)

class Keyframe():
    def __init__(self, frame: int, location: Vector3 = Vector3(), rotation: Vector3 = Vector3()):
        self.frame = frame
        self.location = location
        self.rotation = rotation

    def toJSON(self):
        keyframeTemplate = {
            "frame": self.frame,
            "location": self.location.toJSON(),
            "rotation": self.rotation.toJSON()
        }
        return keyframeTemplate


class ArmourstandObject():
    def __init__(self, item: str, location: Vector3 = Vector3(), rotation: Vector3 = Vector3(), keyframes: list = []):
        self.item = item
        self.location = location
        self.rotation = rotation
        self.keyframes = keyframes
        
    

    # This is possibly bad to do for each object, SOLUTION: collecting locations of all objects with 1 for loop iteration
    def getKeyframes(self, obj):
        scene = bpy.context.scene
        keyframes: list = []
        for f in range(scene.frame_start, scene.frame_end):
            scene.frame_set(f)
            keyframe = Keyframe(f, self.getWorldLocation(self, obj),
                                self.getWorldRotation(self, obj))
            keyframes.append(keyframe)
        return keyframes

    def getWorldLocation(self, obj: bpy.types.Object):
        wm = obj.matrix_world
        loc = wm.to_translation()
        return Vector3(-loc.x, loc.z, loc.y) # Altered for MC co-ordinate system

    def getWorldRotation(self, obj: bpy.types.Object):
        wm = obj.matrix_world
        rot = wm.to_euler('XZY')
        return Vector3(-rot.x, -rot.z, -rot.y) # Altered for MC co-ordinate system

    @classmethod
    def fromBlenderObject(cls, obj: bpy.types.Object):

        # Local Object Data
        locL = Vector3.from_list(obj.location)
        rotL = Vector3.from_list(obj.rotation_euler)

        # World Object Data (Parents Applied)
        locW = cls.getWorldLocation(cls, obj)
        rotW = cls.getWorldRotation(cls, obj)

        # Ensures duplicated object names don't include numbers eg. stone.001
        name = obj.name.split(".")[0]

        # Get Keyframes
        keyframes = cls.getKeyframes(cls, obj)

        return cls(name, locW, rotW, keyframes)

    def toJSON(self):
        locationTemplate = {
            "name": self.item,
            "location": self.location.toJSON(),
            "rotation": self.rotation.toJSON(),
            "keyframes": list(map(lambda it: it.toJSON(), self.keyframes))
        }
        return locationTemplate


class ArmouststandObjectList():
    armourstandList: list = []

    def add(self, obj: ArmourstandObject):
        self.armourstandList.append(obj)

    def clear(self):
        self.armourstandList.clear()

    def toJSONLIST(self):
        return list(map(lambda it: it.toJSON(), self.armourstandList))

class OP_Save_Location_Data(bpy.types.Operator, ExportHelper):
    bl_idname = "blenderstands.save_location_data"
    bl_label = "Save Armourstand Location Data"
    bl_options = {"REGISTER"}

    filename_ext = ".json"

    def execute(self, context):
        filepath = self.filepath
        AList: ArmourstandObjectList = ArmouststandObjectList()
        for obj in bpy.context.selected_objects:
            AList.add(ArmourstandObject.fromBlenderObject(obj))
        f = open(filepath, 'w')
        f.truncate(0)
        json.dump(AList.toJSONLIST(), f)
        f.close()
        AList.clear()
        print("[Blenderstands] Armourstand exported!")
        return {"FINISHED"}

class OP_Save_Animation_Data(bpy.types.Operator):
    bl_idname = "blenderstands.save_animation_data"
    bl_label = "Save Armourstand Animation Data"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {"FINISHED"}

class OP_Add_Item(bpy.types.Operator):
    bl_idname = "blenderstands.add_item"
    bl_label = "Add new item to list"
    bl_options = {"REGISTER"}

    path = 'minecraft/models/item'

    def execute(self, context):
        prop = context.scene.bs_props
        json_files = [pos_json for pos_json in os.listdir(self.path) if pos_json.endswith('.json')]
        for json in json_files:
            item = prop.item_list.add()
            item.name = json
            item.description = "desc"

        return {"FINISHED"}

class OP_Clear_Items(bpy.types.Operator):
    bl_idname = "blenderstands.clear_items"
    bl_label = "Clears all items in the list"
    bl_options = {"REGISTER"}


    def execute(self, context):
        prop = context.scene.bs_props
        item = prop.item_list
        for i in range(len(item)-1,-1,-1):
            item.remove(i)
        return {"FINISHED"}

classes = (OP_Save_Animation_Data, OP_Save_Location_Data, OP_Add_Item, OP_Clear_Items)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
