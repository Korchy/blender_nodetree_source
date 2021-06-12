# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import os
from .nodetree_source_file_manager import FileManager
from .nodetree_source_node import Node


class NodeTree:

    @classmethod
    def to_source(cls, owner, node_tree, parent_expr='', deep=0, processed_node_groups=None):
        # get node tree source
        source = ''
        # list to control node groups - not to build the same node group more than once
        processed_node_groups = [] if processed_node_groups is None else processed_node_groups
        # inputs
        if node_tree.inputs:
            source += ('    ' * deep) + '# INPUTS' + '\n'
            for c_input in owner.inputs:
                source += ('    ' * deep) + parent_expr + str(deep) + '.inputs.new(\'' + c_input.bl_idname + '\', \'' + c_input.name + '\')' + '\n'
        # outputs
        if node_tree.outputs:
            source += ('    ' * deep) + '# OUTPUTS' + '\n'
            for c_output in owner.outputs:
                source += ('    ' * deep) + parent_expr + str(deep) + '.outputs.new(\'' + c_output.bl_idname + '\', \'' + c_output.name + '\')' + '\n'
        # nodes
        if node_tree.nodes:
            source += '    ' * deep + '# NODES' + '\n'
            # process first - because they influence on other nodes and must be created first
            preordered_nodes = [node for node in node_tree.nodes if node.type in ['FRAME']]
            # all other nodes
            nodes = [node for node in node_tree.nodes if node not in preordered_nodes]
            # first - preordered nodes, next - all other nodes
            all_nodes = preordered_nodes + nodes
            for node in all_nodes:
                if node.type == 'GROUP':
                    # node group
                    if node.node_tree and node.node_tree.name not in processed_node_groups:
                        source += ('    ' * deep) + parent_expr + str(deep + 1) + ' = bpy.data.node_groups.get(\'' + node.node_tree.name + '\')' + '\n'
                        source += ('    ' * deep) + 'if not ' + parent_expr + str(deep + 1) + ':' + '\n'
                        source += ('    ' * (deep + 1)) + 'node_tree' + str(deep + 1) + ' = bpy.data.node_groups.new(\'' + node.node_tree.name + '\', \'' + node_tree.bl_idname + '\')' + '\n'
                        source += cls.to_source(
                            owner=node,
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
                    source += Node.to_source(node=node, parent_expr='node_tree' + str(deep), deep=deep) + '\n'
        # links
        if node_tree.links:
            source += ('    ' * deep) + '# LINKS' + '\n'
            for link in node_tree.links:
                from_node_alias = Node.node_alias(node=link.from_node, deep=deep)
                to_node_alias = Node.node_alias(node=link.to_node, deep=deep)
                source += ('    ' * deep) + parent_expr + str(deep) + '.links.new(' \
                          + from_node_alias + '.outputs[' + str(list(link.from_node.outputs).index(link.from_socket)) + ']' + \
                          ', ' + to_node_alias + '.inputs[' + str(list(link.to_node.inputs).index(link.to_socket)) + ']' + \
                          ')' + '\n'
        return source

    @staticmethod
    def clear_source(parent_expr='', deep=0):
        # source for clear node tree
        source = ('    ' * deep) + 'for node in ' + parent_expr + '.nodes:' + '\n'
        source += ('    ' * (deep + 1)) + parent_expr + '.nodes.remove(node)' + '\n'
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
