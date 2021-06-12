# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .nodetree_source import NodeTreeSource
from .nodetree_source_context import NodeTreeSourceContext


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
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if subtype == 'ShaderNodeTree'\
                and subtype2 == 'OBJECT'\
                and context.active_object\
                and context.active_object.active_material\
                and context.active_object.active_material.node_tree:
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'WORLD'\
                and context.scene.world\
                and context.scene.world.use_nodes:
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'LIGHT'\
                and context.scene.render.engine == 'CYCLES'\
                and context.active_object.data.use_nodes:
            return True
        elif subtype == 'CompositorNodeTree'\
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
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if subtype == 'ShaderNodeTree'\
                and subtype2 == 'OBJECT'\
                and context.active_object\
                and context.active_object.active_material\
                and context.active_object.active_material.node_tree:
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'WORLD'\
                and context.scene.world\
                and context.scene.world.use_nodes:
            return True
        elif subtype == 'ShaderNodeTree'\
                and subtype2 == 'LIGHT'\
                and context.scene.render.engine == 'CYCLES'\
                and context.active_object.data.use_nodes:
            return True
        elif subtype == 'CompositorNodeTree'\
                and context.scene.use_nodes:
            return True
        else:
            return False


class NODETREE_SOURCE_OT_library_to_add_on(Operator):
    bl_idname = 'nodetree_source.library_to_add_on'
    bl_label = 'Distribute Library as Add-on'
    bl_description = 'Export NodeTree Source library as separate add-on'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeTreeSource.library_to_add_on(
            context=context
        )
        return {'FINISHED'}


def register():
    register_class(NODETREE_SOURCE_OT_material_to_text)
    register_class(NODETREE_SOURCE_OT_material_to_library)
    register_class(NODETREE_SOURCE_OT_library_to_add_on)


def unregister():
    unregister_class(NODETREE_SOURCE_OT_library_to_add_on)
    unregister_class(NODETREE_SOURCE_OT_material_to_library)
    unregister_class(NODETREE_SOURCE_OT_material_to_text)
