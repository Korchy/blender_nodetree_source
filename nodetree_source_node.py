# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_bl_types_conversion import BlTypesConversion


class Node:

    @classmethod
    def to_source(cls, node, parent_expr='', deep=0):
        # get node source
        source = ''
        node_alias = cls.node_alias(node=node, deep=deep)
        source += ('    ' * deep) + node_alias + ' = ' + parent_expr + '.nodes.new(\'' + node.bl_idname + '\')' + '\n'
        # attributes
        # don't process
        excluded_attributes = [
            'dimensions', 'height', 'hide', 'inputs', 'internal_links', 'node_tree', 'outputs', 'rna_type', 'select',
            'shading_compatibility', 'show_options', 'show_preview', 'show_texture', 'type', 'width_hidden'
        ]
        # process first - because they influence on other attributes
        preordered_attributes = [attr for attr in ['mode', 'node_tree', 'parent'] if hasattr(node, attr)]
        # this attributes - complex
        complex_attributes = ['mapping']
        # get source
        source += BlTypesConversion.source_from_complex_type(
            value=node,
            excluded_attributes=excluded_attributes,
            preordered_attributes=preordered_attributes,
            complex_attributes=complex_attributes,
            parent_expr=('    ' * deep) + node_alias,
            deep=deep
        )
        # inputs
        if node.type not in ['REROUTE']:
            if node.inputs:
                for index, c_input in enumerate(node.inputs):
                    if hasattr(c_input, 'default_value'):
                        input_value_str = BlTypesConversion.source_by_type(item=c_input, value=c_input.default_value)
                        if input_value_str is not None:
                            source += ('    ' * deep) + node_alias + '.inputs[' + str(index) + '].default_value = ' + input_value_str + '\n'
            # outputs
            if node.outputs:
                for index, c_output in enumerate(node.outputs):
                    if hasattr(c_output, 'default_value'):
                        output_value_str = BlTypesConversion.source_by_type(item=c_output, value=c_output.default_value)
                        if output_value_str is not None:
                            source += ('    ' * deep) + node_alias + '.outputs[' + str(index) + '].default_value = ' + output_value_str + '\n'
        return source

    @staticmethod
    def node_alias(node, deep=0):
        # get text node alias-name
        node_name = node.name.lower()
        for ch in (' ', '.', '/'):
            node_name = node_name.replace(ch, '_')
        node_name += '_' + str(deep)
        return node_name
