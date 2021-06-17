import os
import bpy

def init():
    global image_collections
    image_collections = {}
    icons_init()

def icons_init():
    global image_collections
    my_icons_dir = os.path.join(os.path.dirname(__file__), "minecraft/textures/item")
    png_files = [pos_png for pos_png in os.listdir(my_icons_dir) if pos_png.endswith('.png')]

    collections = ["items", "blocks"]

    for collection in collections:
        image_collections[collection] = bpy.utils.previews.new()

    # json_files = [pos_json for pos_json in os.listdir(self.path) if pos_json.endswith('.json')]

    for png in png_files:
        item_name = os.path.split(png)[0]
        image_collections["items"].load(png, os.path.join(my_icons_dir, png), 'IMAGE')
    

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