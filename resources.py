import os
from typing import List
import bpy
from bpy.types import Object
import bpy.utils.previews
import json
from enum import Enum

class ListObject():

    class ObjectType(Enum):
        ITEM = 1,
        BLOCK = 2

    mc_path: str
    mc_name: str
    object_type: ObjectType

    def __init__(self, path, name):
        self.mc_path = path
        self.mc_name = name.split(".")[0]
        self.object_type = self.getType(path)

    def getType(self, path):
        if "minecraft:" in path:
            return self.ObjectType.BLOCK
        else:
            return self.ObjectType.ITEM

    def getAsPath(self):
        block_paths = {
            "minecraft:block": "minecraft/textures/block",
            "minecraft:item": "minecraft/textures/item"
        }
        item_paths = {
            "block": "minecraft/textures/block",
            "item": "minecraft/textures/item"
        }
        texture_split = self.mc_path.split("/")
        print(texture_split)
        try:
            if (self.object_type == self.ObjectType.BLOCK):
                path = block_paths[texture_split[0]] + "/" + texture_split[1] + ".png"
            if (self.object_type == self.ObjectType.ITEM):
                path = item_paths[texture_split[0]] + "/" + texture_split[1] + ".png"
        except:
            path = "NOT FOUND"
        return path

class AssetLoader():
    object_list: list = []

    def __init__(self):
        self.loadObjects()

    def getObjects(self):
        return self.object_list

    def loadObjects(self):
        path = 'minecraft/models/item'

        json_files = [pos_json for pos_json in os.listdir(
            path) if pos_json.endswith('.json')]
        for json_filename in json_files:
            with open(path + "/" + json_filename) as json_file:
                print("Loading: " + json_filename)
                json_dict = json.load(json_file)
                if "textures" in json_dict:
                    if "texture" in json_dict["textures"]:
                        texture = json_dict["textures"]["texture"]
                        texture_object = ListObject(texture, json_filename)
                        self.object_list.append(texture_object)
                    if "layer0" in json_dict["textures"]:
                        layer = json_dict["textures"]["layer0"]
                        layer_object = ListObject(layer, json_filename)
                        self.object_list.append(layer_object)


def init():
    global image_collections
    image_collections = {}
    icons_init()


def icons_init():
    global image_collections
    my_icons_dir = os.path.join(os.path.dirname(
        __file__), "minecraft/textures/item")
    png_files = [pos_png for pos_png in os.listdir(
        my_icons_dir) if pos_png.endswith('.png')]

    collections = ["items", "blocks"]

    for collection in collections:
        image_collections[collection] = bpy.utils.previews.new()

    # json_files = [pos_json for pos_json in os.listdir(self.path) if pos_json.endswith('.json')]

    assets = AssetLoader()
    for asset in assets.object_list:
        print(asset.mc_path)
        image_collections["items"].load(asset.mc_name, asset.getAsPath(), 'IMAGE')

    # for png in png_files:
    #     item_name = os.path.split(png)[0]
    #     image_collections["items"].load(
    #         png, os.path.join(my_icons_dir, png), 'IMAGE')


def register():
    print("test")
    init()


def unregister():
    global image_collections
    for image in image_collections.values():
        bpy.utils.previews.remove(image)
    image_collections.clear()


if __name__ == "__main__":
    register()
