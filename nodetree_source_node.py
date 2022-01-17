# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import re
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
            'dimensions', 'height', 'inputs', 'internal_links', 'node_tree', 'outputs', 'rna_type', 'select',
            'shading_compatibility', 'show_options', 'show_preview', 'show_texture', 'type', 'width_hidden'
        ]
        # process first - because they influence on other attributes
        preordered_attributes = [attr for attr in ['mode', 'node_tree', 'parent'] if hasattr(node, attr)]
        # this attributes - complex
        complex_attributes = ['color_ramp', 'mapping']
        # get source
        source += BlTypesConversion.source_from_complex_type(
            value=node,
            excluded_attributes=excluded_attributes,
            preordered_attributes=preordered_attributes,
            complex_attributes=complex_attributes,
            parent_expr=node_alias,
            deep=deep
        )
        # inputs, outputs
        if node.type not in ['REROUTE']:
            # inputs
            if node.inputs:
                for index, c_input in enumerate(node.inputs):
                    if hasattr(c_input, 'default_value'):
                        excluded_attributes = [attr for attr in ['type', 'link_limit'] if hasattr(c_input, attr)]
                        if node.type in ('GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT'):
                            # for node groups - by index
                            source += BlTypesConversion.source_from_complex_type(
                                value=c_input,
                                excluded_attributes=excluded_attributes,
                                parent_expr=node_alias + '.inputs[' + str(index) + ']',
                                deep=deep
                            )
                        else:
                            # for simple nodes - by identifier
                            source += ('    ' * deep) + \
                                      'input_ = next((input_ for input_ in ' + node_alias + \
                                      '.inputs if input_.identifier==\'' + c_input.identifier + '\'), None)' + '\n'
                            source += ('    ' * deep) + 'if input_:' + '\n'
                            source += BlTypesConversion.source_from_complex_type(
                                value=c_input,
                                excluded_attributes=excluded_attributes,
                                parent_expr='input_',
                                deep=deep+1
                            )
            # outputs
            if node.outputs:
                for index, c_output in enumerate(node.outputs):
                    if hasattr(c_output, 'default_value'):
                        excluded_attributes = [attr for attr in ['type', 'link_limit'] if hasattr(c_output, attr)]
                        if node.type in ('GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT'):
                            # for node groups - by index
                            source += BlTypesConversion.source_from_complex_type(
                                value=c_output,
                                excluded_attributes=excluded_attributes,
                                parent_expr=node_alias + '.outputs[' + str(index) + ']',
                                deep=deep
                            )
                        else:
                            # for simple nodes - by identifier
                            source += ('    ' * deep) + \
                                      'output = next((output for output in ' + node_alias + \
                                      '.outputs if output.identifier==\'' + c_output.identifier + '\'), None)' + '\n'
                            source += ('    ' * deep) + 'if output:' + '\n'
                            source += BlTypesConversion.source_from_complex_type(
                                value=c_output,
                                excluded_attributes=excluded_attributes,
                                parent_expr='output',
                                deep=deep + 1
                            )
        return source

    @staticmethod
    def node_alias(node, deep=0):
        # get text node alias-name
        node_name = node.name.lower()
        node_name = ''.join((x if x.isalnum() else '_' for x in node_name))
        node_name = re.sub('_+', '_', node_name)
        node_name += '_' + str(deep)
        if node_name[0].isdigit():
            node_name = '_' + node_name
        return node_name
