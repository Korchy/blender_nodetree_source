# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from mathutils import Vector, Color
from bpy.types import bpy_prop_array
from .nodetree_source_bl_types_conversion import *


class Node:

    @classmethod
    def to_source(cls, node):
        # get node source
        source = ''
        node_alias = cls.node_alias(node=node)
        source += node_alias + ' = node_tree.nodes.new(\'' + node.bl_idname + '\')' + '\n'
        # inputs
        if node.inputs:
            source += '# NODE INPUTS' + '\n'
            for index, c_input in enumerate(node.inputs):
                if hasattr(c_input, 'default_value'):
                    source += node_alias + '.inputs[' + str(index) + '].default_value = ' + cls._value_by_type(value=c_input.default_value) + '\n'
        # outputs
        if node.outputs:
            source += '# NODE OUTPUTS' + '\n'
            for index, c_output in enumerate(node.outputs):
                if hasattr(c_output, 'default_value'):
                    source += node_alias + '.outputs[' + str(index) + '].default_value = ' + cls._value_by_type(value=c_output.default_value) + '\n'
        # attributes
        excluded_attributes = [
            'dimensions', 'height', 'hide', 'inputs', 'internal_links', 'name', 'outputs', 'parent', 'rna_type', 'select',
            'shading_compatibility', 'show_options', 'show_preview', 'show_texture', 'type', 'width_hidden'
        ]
        attributes = [
            attr for attr in dir(node) if
            not attr.startswith('__')
            and (not attr.startswith('bl_') or attr == 'bl_idname')
            and attr not in excluded_attributes
            and hasattr(node, attr)
            and not callable(getattr(node, attr))
            and not node.is_property_readonly(attr)
        ]
        if attributes:
            source += '# ATTRIBUTES' + '\n'
            for attribute in attributes:
                # convert by types
                if isinstance(getattr(node, attribute), (Vector, Color)):
                    # source += node_alias + '.' + attribute + ' = ' + tuple(getattr(node, attribute)) + '\n'
                    source += node_alias + '.' + attribute + ' = ' + BLColor.to_str(value=getattr(node, attribute)) + '\n'
                elif isinstance(getattr(node, attribute), (int, float, bool, set)):
                    source += node_alias + '.' + attribute + ' = ' + str(getattr(node, attribute)) + '\n'
                elif isinstance(getattr(node, attribute), str):
                    if getattr(node, attribute):
                        source += node_alias + '.' + attribute + ' = ' + str(getattr(node, attribute)) + '\n'
                else:
                    # undefined
                    print(attribute, ' (', type(getattr(node, attribute)), ') ', ': ', getattr(node, attribute))
        return source

    @staticmethod
    def node_alias(node):
        # get text node alias-name
        return node.name.replace(' ', '_').replace('.', '_').lower()

    @staticmethod
    def _value_by_type(value):
        # value as string by type
        if isinstance(value, bpy_prop_array):
            return BLbpy_prop_array.to_str(value=value)
        elif isinstance(value, (int, float, bool, set, str)):
            return str(value)
        else:
            print('ERR: Undefined type value', value, type(value))
            return None
