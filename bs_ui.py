from typing import Type
from . import resources
import bpy
import os

class BS_UL_spawner_item(bpy.types.UIList):
    def draw_item(self, context: 'Context', layout: bpy.types.UILayout, data: 'AnyType', item: 'AnyType', icon: int, active_data: 'AnyType', active_property: str, index: int, flt_flag: int):
        # icon_id = resources.image_collection["test"]["test"].icon_id
        icon_name = item.name.split(".")[0]
        try:
            layout.label(text=icon_name, icon_value=resources.image_collections["items"][icon_name].icon_id)
        except:
            layout.label(text=icon_name)

class BS_PT_spawner(bpy.types.Panel):
    bl_label = "Spawner"
    bl_space_type = "VIEW_3D"
    bl_category = "Blenderstands"
    bl_region_type = "UI"

    def draw(self, context : bpy.context):
        layout = self.layout
        prop = context.scene.bs_props
        layout.template_list("BS_UL_spawner_item", "Spawner", prop, "item_list", prop, "item_index")
        row = layout.row()
        row.operator("blenderstands.add_item",
                     text="Add")
        row.operator("blenderstands.clear_items",
                     text="Clear")

class BS_PT_Main(bpy.types.Panel):
    bl_idname = "pn_main"
    bl_label = "Exporter"
    bl_category = "Blenderstands"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.label(text="Location Data", icon="ORIENTATION_LOCAL")
        row.operator("blenderstands.save_location_data",
                     text="Export")

class ItemListAsset(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty()
    description : bpy.props.StringProperty()

class SceneProps(bpy.types.PropertyGroup):
    item_list : bpy.props.CollectionProperty(type=ItemListAsset)
    item_index : bpy.props.IntProperty(default=0)

classes = (BS_PT_Main, BS_PT_spawner, BS_UL_spawner_item, ItemListAsset, SceneProps)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.bs_props = bpy.props.PointerProperty(type=SceneProps)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.bs_props

if __name__ == "__main__":
    register()