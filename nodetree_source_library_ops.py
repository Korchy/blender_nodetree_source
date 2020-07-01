# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .nodetree_source_library import NodeTreeSourceLibrary
from .nodetree_source_material import Material


class NODETREE_SOURCE_LIBRARY_OT_material_from_library(Operator):
    bl_idname = 'nodetree_source_library.material_from_library'
    bl_label = 'Material from Library'
    bl_description = 'Get material from NodeTree Source library'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSourceLibrary.material_from_library(
            context=context,
            scene_data=bpy.data
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):

        # todo - correct without Material class, maybe make separate class "nodetree_context"

        if Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'OBJECT'\
                and context.active_object:
            return True
        elif Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'WORLD':
            return True
        elif Material.get_subtype(context=context) == 'CompositorNodeTree'\
                and context.scene.use_nodes:
            return True
        else:
            return False


class NODETREE_SOURCE_LIBRARY_OT_remove_material(Operator):
    bl_idname = 'nodetree_source_library.remove_material'
    bl_label = 'Remove material from Library'
    bl_description = 'Remove material from NodeTree Source library'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSourceLibrary.remove_material_from_library(
            context=context,
            scene_data=bpy.data
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if 0 <= context.window_manager.nodetree_source_library_active_item < len(context.window_manager.nodetree_source_library_items):
            return True
        else:
            return False


def register():
    register_class(NODETREE_SOURCE_LIBRARY_OT_material_from_library)
    register_class(NODETREE_SOURCE_LIBRARY_OT_remove_material)


def unregister():
    unregister_class(NODETREE_SOURCE_LIBRARY_OT_remove_material)
    unregister_class(NODETREE_SOURCE_LIBRARY_OT_material_from_library)
