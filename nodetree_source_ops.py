# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .nodetree_source import NodeTreeSource
from .nodetree_source_material import Material


class NODETREE_SOURCE_OT_material_to_text(Operator):
    bl_idname = 'nodetree_source.material_to_text'
    bl_label = 'Material to Text'
    bl_description = 'Convert material to source'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSource.material_to_text(
            context=context,
            scene_data=bpy.data
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'OBJECT'\
                and context.active_object\
                and context.active_object.active_material\
                and context.active_object.active_material.node_tree:
            return True
        elif Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'WORLD'\
                and context.scene.world\
                and context.scene.world.use_nodes:
            return True
        elif Material.get_subtype(context=context) == 'CompositorNodeTree'\
                and context.scene.use_nodes:
            return True
        else:
            return False


class NODETREE_SOURCE_OT_material_to_library(Operator):
    bl_idname = 'nodetree_source.material_to_library'
    bl_label = 'Material to Library'
    bl_description = 'Add material to source library'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSource.material_to_library(
            context=context,
            scene_data=bpy.data
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'OBJECT'\
                and context.active_object\
                and context.active_object.active_material\
                and context.active_object.active_material.node_tree:
            return True
        elif Material.get_subtype(context=context) == 'ShaderNodeTree'\
                and Material.get_subtype2(context=context) == 'WORLD'\
                and context.scene.world\
                and context.scene.world.use_nodes:
            return True
        elif Material.get_subtype(context=context) == 'CompositorNodeTree'\
                and context.scene.use_nodes:
            return True
        else:
            return False


def register():
    register_class(NODETREE_SOURCE_OT_material_to_text)
    register_class(NODETREE_SOURCE_OT_material_to_library)


def unregister():
    unregister_class(NODETREE_SOURCE_OT_material_to_library)
    unregister_class(NODETREE_SOURCE_OT_material_to_text)
