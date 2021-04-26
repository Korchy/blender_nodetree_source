# Sebastian Grans
# sebastian.grans@gmail.com
# https://github.com/SebastianGrans
#
# 
# Project GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_node_tree import NodeTree
from .nodetree_source_material import Material

class Light:
    @classmethod 
    def to_source(cls, context):
        source = ''
        source += cls.header()
        source += cls.light_specs(context)
        source += NodeTree.to_source(
            owner=None,
            node_tree=context.active_object.data.node_tree,
            parent_expr='node_tree'
        )
        return source

    @staticmethod
    def header():
        source = 'import bpy' + '\n'
        source += 'from mathutils import Color' + '\n'
        source += 'bpy.context.active_object.data.use_nodes = True' + '\n'
        source += 'bpy.context.active_object.data.node_tree.nodes.clear()' + '\n'
        source += 'node_tree0 = bpy.context.active_object.data.node_tree' + '\n'

        return source

    @classmethod
    def light_specs(cls, context):
        '''Also copy the properties of the light. E.g., power, radius, area, etc.'''

        source = ''

        source += 'bpy.context.active_object.data.color = ' \
            + repr(context.active_object.data.color) + '\n'
        source += 'bpy.context.active_object.data.energy = ' \
            + repr(context.active_object.data.energy) + '\n'
        source += 'bpy.context.active_object.data.cycles.max_bounces = ' \
            + repr(context.active_object.data.cycles.max_bounces) + '\n'
        source += 'bpy.context.active_object.data.cycles.cast_shadow = ' \
            + repr(context.active_object.data.cycles.cast_shadow) + '\n'
        source += 'bpy.context.active_object.data.cycles.use_multiple_importance_sampling = ' \
            + repr(context.active_object.data.cycles.use_multiple_importance_sampling) + '\n'
        source += 'bpy.context.active_object.data.cycles.is_portal = ' \
            + repr(context.active_object.data.cycles.is_portal) + '\n'
        
        # Type specific
        light_type = context.active_object.data.type 
        source += 'bpy.context.active_object.data.type = ' + repr(light_type) + '\n'
        if light_type == 'POINT':
            source += 'bpy.context.active_object.data.shadow_soft_size = ' \
                + repr(context.active_object.data.shadow_soft_size) + '\n'
        if light_type == 'SUN':
            source += 'bpy.context.active_object.data.shadow_soft_size = ' \
                + repr(context.active_object.data.angle) + '\n'
        if light_type == 'SPOT':
            source += 'bpy.context.active_object.data.shadow_soft_size = ' \
                + repr(context.active_object.data.shadow_soft_size) + '\n'
            source += 'bpy.context.active_object.data.spot_size = ' \
                + repr(context.active_object.data.spot_size) + '\n'
            source += 'bpy.context.active_object.data.spot_blend = ' \
                + repr(context.active_object.data.spot_blend) + '\n'
        if light_type == 'AREA':
            source += 'bpy.context.active_object.data.shadow_soft_size = ' \
                + repr(context.active_object.data.shadow_soft_size) + '\n'

        return source


