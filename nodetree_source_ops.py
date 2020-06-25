# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .nodetree_source import NodeTreeSource
from .nodetree_source_material import Material


class NODETREE_SOURCE_OT_to_source(Operator):
    bl_idname = 'nodetree_source.to_source'
    bl_label = 'Node Tree to Source'
    bl_description = 'Convert node tree to source'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSource.to_source(
            context=context
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
    register_class(NODETREE_SOURCE_OT_to_source)


def unregister():
    unregister_class(NODETREE_SOURCE_OT_to_source)
