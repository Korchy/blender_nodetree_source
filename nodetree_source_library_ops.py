# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
from bpy.props import IntProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .nodetree_source_library import NodeTreeSourceLibrary
from .nodetree_source_context import NodeTreeSourceContext


class NODETREE_SOURCE_LIB_OT_material_from_library(Operator):
    bl_idname = 'nodetree_source_lib.material_from_library'
    bl_label = 'Add Material from Library'
    bl_description = 'Get material from NodeTree Source library'
    bl_options = {'REGISTER', 'UNDO'}

    material_id: IntProperty(
        default=-0
    )

    def execute(self, context):
        # add material from source library to scene
        active_material_id = context.window_manager.nodetree_source_lib_active_item
        if active_material_id != self.material_id:
            context.window_manager.nodetree_source_lib_active_item = self.material_id
        material_alias = context.window_manager.nodetree_source_lib_items[context.window_manager.nodetree_source_lib_active_item].name
        NodeTreeSourceLibrary.material_from_library(
            context=context,
            material_alias=material_alias
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if subtype == 'ShaderNodeTree'\
                and subtype2 == 'OBJECT'\
                and context.active_object:
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'WORLD':
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'LIGHT'\
                and context.scene.render.engine == 'CYCLES'\
                and context.active_object\
                and context.active_object.type == 'LIGHT':
            return True
        elif subtype == 'CompositorNodeTree'\
                and context.scene.use_nodes:
            return True
        else:
            return False


class NODETREE_SOURCE_LIB_OT_remove_material(Operator):
    bl_idname = 'nodetree_source_lib.remove_material'
    bl_label = 'Remove material from Library'
    bl_description = 'Remove material from NodeTree Source library'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSourceLibrary.remove_material_from_library(
            context=context,
            scene_data=bpy.data
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Removed material can not be restored!')
        layout.label(text='Are you sure?')

    @classmethod
    def poll(cls, context):
        if 0 <= context.window_manager.nodetree_source_lib_active_item < len(context.window_manager.nodetree_source_lib_items):
            return True
        else:
            return False


def register():
    register_class(NODETREE_SOURCE_LIB_OT_material_from_library)
    register_class(NODETREE_SOURCE_LIB_OT_remove_material)


def unregister():
    unregister_class(NODETREE_SOURCE_LIB_OT_remove_material)
    unregister_class(NODETREE_SOURCE_LIB_OT_material_from_library)
