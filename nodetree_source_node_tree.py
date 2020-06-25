# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

# import sys
# from .file_manager import FileManager
# from .node_io import *
# from .node_common import NodeCommon
# from .node_shader_cycles import *
# from .node_compositor import *
from .nodetree_source_node import Node


class NodeTree:

    @classmethod
    def to_source(cls, node_tree):
        # get node tree source
        source = ''
        # inputs
        if node_tree.inputs:
            source += '# INPUTS' + '\n'
            for c_input in node_tree.inputs:
                source += c_input.rna_type.identifier + '\n'   # NodeSocketInterfaceXXX
        # outputs
        if node_tree.outputs:
            source += '# OUTPUTS' + '\n'
            for c_output in node_tree.outputs:
                source += c_output.rna_type.identifier + '\n'   # NodeSocketInterfaceXXX
        # nodes
        if node_tree.nodes:
            source += '# NODES' + '\n'
            for node in node_tree.nodes:
                source += Node.to_source(node=node) + '\n'
        # links
        if node_tree.links:
            source += '# LINKS' + '\n'
            for link in node_tree.links:
                from_node_alias = Node.node_alias(link.from_node)
                to_node_alias = Node.node_alias(link.to_node)
                source += 'node_tree.links.new(' \
                          + from_node_alias + '.outputs[' + str(list(link.from_node.outputs).index(link.from_socket)) + ']' + \
                          ', ' + to_node_alias + '.inputs[' + str(list(link.to_node.inputs).index(link.to_socket)) + ']' + \
                          ')' + '\n'
        return source

    # @staticmethod
    # def has_node_groups(node_tree):
    #     # return True if node_tree has NodeGroup nodes
    #     return any(node.type == 'GROUP' for node in node_tree.nodes)
    #
    # @classmethod
    # def external_items(cls, node_tree):
    #     # returns external items (textures,... etc) list
    #     rez = []
    #     for node in node_tree.nodes:
    #         if node.type == 'GROUP':
    #             rez.extend(cls.external_items(node_tree=node.node_tree))
    #         elif node.type == 'TEX_IMAGE' and node.image:
    #             rez.append({
    #                 'path': FileManager.abs_path(node.image.filepath),
    #                 'name': node.image.name
    #             })
    #         elif node.type == 'SCRIPT' and node.mode == 'EXTERNAL' and node.filepath:
    #             rez.append({
    #                 'path': FileManager.abs_path(node.filepath)
    #             })
    #     return rez
