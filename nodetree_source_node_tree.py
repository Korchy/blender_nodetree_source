# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
import os
from .nodetree_source_bl_types_conversion import BlTypesConversion
from .nodetree_source_file_manager import FileManager
from .nodetree_source_node import Node


class NodeTree:

    @classmethod
    def to_source(cls, node_tree, parent_expr='', deep=0, processed_node_groups=None):
        # get node tree source
        source = ''
        # clear node tree
        source += cls.clear_source(parent_expr=parent_expr, deep=deep)
        # list to control node groups - not to build the same node group more than once
        processed_node_groups = [] if processed_node_groups is None else processed_node_groups
        # inputs
        if bpy.app.version < (4, 0, 0):
            if node_tree.inputs:
                source += ('    ' * deep) + '# INPUTS' + '\n'
                for c_input in node_tree.inputs:
                    source += ('    ' * deep) + 'input = ' + parent_expr + str(deep) + \
                              '.inputs.new(\'' + c_input.bl_socket_idname + '\', \'' + c_input.name + '\')' + '\n'
                    source += BlTypesConversion.source_from_complex_type(
                        value=c_input,
                        excluded_attributes=['NWViewerSocket'],
                        parent_expr='input',
                        deep=deep
                    )
        else:
            inputs = [socket for socket in node_tree.interface.items_tree if socket.in_out == 'INPUT']
            if inputs:
                source += ('    ' * deep) + '# INPUTS' + '\n'
                for c_input in inputs:
                    source += ('    ' * deep) + 'input = ' + parent_expr + str(deep) \
                              + '.interface.new_socket(name=\'' + c_input.name + '\', '\
                              + 'socket_type=\'' + c_input.bl_socket_idname + '\', ' \
                              + 'in_out=\'INPUT\'' \
                              + ')' + '\n'
                    source += BlTypesConversion.source_from_complex_type(
                        value=c_input,
                        excluded_attributes=['NWViewerSocket'],
                        parent_expr='input',
                        deep=deep
                    )
        # outputs
        if bpy.app.version < (4, 0, 0):
            if node_tree.outputs:
                source += ('    ' * deep) + '# OUTPUTS' + '\n'
                for c_output in node_tree.outputs:
                    source += ('    ' * deep) + 'output = ' + parent_expr + str(deep) + \
                              '.outputs.new(\'' + c_output.bl_socket_idname + '\', \'' + c_output.name + '\')' + '\n'
                    source += BlTypesConversion.source_from_complex_type(
                        value=c_output,
                        excluded_attributes=['NWViewerSocket'],
                        parent_expr='output',
                        deep=deep
                    )
        else:
            outputs = [socket for socket in node_tree.interface.items_tree if socket.in_out == 'OUTPUT']
            if outputs:
                source += ('    ' * deep) + '# OUTPUTS' + '\n'
                for c_output in outputs:
                    source += ('    ' * deep) + 'output = ' + parent_expr + str(deep) \
                              + '.interface.new_socket(name=\'' + c_output.name + '\', '\
                              + 'socket_type=\'' + c_output.bl_socket_idname + '\', ' \
                              + 'in_out=\'OUTPUT\'' \
                              + ')' + '\n'
                    source += BlTypesConversion.source_from_complex_type(
                        value=c_output,
                        excluded_attributes=['NWViewerSocket'],
                        parent_expr='output',
                        deep=deep
                    )
        # nodes
        if node_tree.nodes:
            source += '    ' * deep + '# NODES' + '\n'
            # process first - because they influence on other nodes and must be created first
            #   'FRAME' - when creating node, if it is in frame, frame must be already exists
            #   'REPEAT_OUTPUT' - from "Repeat Zone" block, needs to be first because
            #       1. when creating items - automatically creates inputs/outputs on both repeat zone nodes
            #       2. when Repeat Input node creates it needs to call pair_with_output()
            #           function with previously created Repeat Output node in parameter
            #   'SIMULATION_OUTPUT' - from "Simulation Zone" block, needs to be first because
            #       1. when creating items - automatically creates inputs/outputs on both simulation zone nodes
            #       2. when Simulation Input node creates it needs to call pair_with_output()
            #           function with previously created Repeat Output node in parameter
            preordered_nodes = [node for node in node_tree.nodes
                                if node.type in ['FRAME', 'REPEAT_OUTPUT', 'SIMULATION_OUTPUT']]
            # all other nodes
            nodes = [node for node in node_tree.nodes if node not in preordered_nodes]
            # first - preordered nodes, next - all other nodes
            all_nodes = preordered_nodes + nodes
            for node in all_nodes:
                if node.type == 'GROUP':
                    # node group
                    if node.node_tree and node.node_tree.name not in processed_node_groups:
                        source += ('    ' * deep) + parent_expr + str(deep + 1) + \
                                  ' = bpy.data.node_groups.get(\'' + node.node_tree.name + '\')' + '\n'
                        source += ('    ' * deep) + 'if not ' + parent_expr + str(deep + 1) + ':' + '\n'
                        source += ('    ' * (deep + 1)) + 'node_tree' + str(deep + 1) + \
                            ' = bpy.data.node_groups.new(\'' + node.node_tree.name + '\', ' + \
                            '\'' + node_tree.bl_idname + '\')' + '\n'
                        source += cls.to_source(
                            node_tree=node.node_tree,
                            parent_expr=parent_expr,
                            deep=deep + 1,
                            processed_node_groups=processed_node_groups
                        ) + '\n'
                        processed_node_groups.append(node.node_tree.name)
                    source += Node.to_source(
                        node=node,
                        parent_expr='node_tree' + str(deep),
                        deep=deep
                    ) + '\n'
                else:
                    # simple node
                    source += Node.to_source(
                        node=node,
                        parent_expr='node_tree' + str(deep),
                        deep=deep
                    ) + '\n'
        # links
        if node_tree.links:
            source += ('    ' * deep) + '# LINKS' + '\n'
            for link in node_tree.links:
                from_node_alias = Node.node_alias(node=link.from_node, deep=deep)
                to_node_alias = Node.node_alias(node=link.to_node, deep=deep)
                source += ('    ' * deep) + parent_expr + str(deep) + '.links.new(' + \
                    from_node_alias + '.outputs[' + str(list(link.from_node.outputs).index(link.from_socket)) + ']' + \
                    ', ' + to_node_alias + '.inputs[' + str(list(link.to_node.inputs).index(link.to_socket)) + ']' + \
                    ')' + '\n'
        return source

    @staticmethod
    def clear_source(parent_expr='', deep=0):
        # source for clear node tree
        source = ('    ' * deep) + 'for node in ' + parent_expr + str(deep) + '.nodes:' + '\n'
        source += ('    ' * (deep + 1)) + parent_expr + str(deep) + '.nodes.remove(node)' + '\n'
        return source

    @classmethod
    def external_items(cls, node_tree):
        # returns external items (textures,... etc) list
        rez = []
        if node_tree:
            for node in node_tree.nodes:
                if node.type == 'GROUP':
                    rez.extend(cls.external_items(node_tree=node.node_tree))
                elif node.type in ['TEX_IMAGE', 'TEX_ENVIRONMENT'] and node.image:
                    rez.append({
                        'type': 'TEXTURE',
                        'path': FileManager.abs_path(node.image.filepath),
                        'name': node.image.name
                    })
                elif node.type == 'SCRIPT' and node.mode == 'EXTERNAL' and node.filepath:
                    rez.append({
                        'type': 'SCRIPT',
                        'path': FileManager.abs_path(node.filepath),
                        'name': os.path.basename(node.filepath)
                    })
        return rez
