# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import sys
from mathutils import Vector, Color
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
            for index, c_input in enumerate(node.inputs):
                if hasattr(c_input, 'default_value'):
                    input_value_str = cls._value_by_type(item=c_input, value=c_input.default_value)
                    if input_value_str is not None:
                        source += node_alias + '.inputs[' + str(index) + '].default_value = ' + input_value_str + '\n'
        # outputs
        if node.outputs:
            for index, c_output in enumerate(node.outputs):
                if hasattr(c_output, 'default_value'):
                    output_value_str = cls._value_by_type(item=c_output, value=c_output.default_value)
                    if output_value_str is not None:
                        source += node_alias + '.outputs[' + str(index) + '].default_value = ' + output_value_str + '\n'
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
            for attribute in attributes:
                # convert by types
                # don't save empty strings
                if isinstance(getattr(node, attribute), str) and not getattr(node, attribute):
                    continue
                # don't save None attributes
                if getattr(node, attribute) is None:
                    continue
                # get string alias of an attribute
                attribute_value_str = cls._value_by_type(item=attribute, value=getattr(node, attribute))
                if attribute_value_str is not None:
                    source += node_alias + '.' + attribute + ' = ' + attribute_value_str + '\n'
        return source

    @staticmethod
    def node_alias(node):
        # get text node alias-name
        return node.name.replace(' ', '_').replace('.', '_').lower()

    @staticmethod
    def _value_by_type(item, value):
        # value as string by type
        if isinstance(value, Vector):
            return BLVector.to_source(value=value)
        elif isinstance(value, Color):
            return BLColor.to_source(value=value)
        elif isinstance(value, (int, float, bool, set)):
            return str(value)
        elif isinstance(value, str):
            return '\'' + value + '\''
        elif hasattr(sys.modules[__name__], 'BL' + value.__class__.__name__):
            value_class = getattr(sys.modules[__name__], 'BL' + value.__class__.__name__)
            return value_class.to_source(value=value)
        else:
            print('ERR: Undefined type: item = ', item,
                  'value = ', value, ' (', type(value), ')',
                  'item_class = ', item.__class__.__name__,
                  'value_class = ', value.__class__.__name__
                  )
            return None
