# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_node import Node


class NodeTree:

    @classmethod
    def to_source(cls, node_tree, parent_expr='', deep=0):
        # get node tree source
        source = ''
        # inputs
        # if node_tree.inputs:
        #     source += ('    ' * deep) + '# INPUTS' + '\n'
        #     for c_input in node_tree.inputs:
        #         source += ('    ' * deep) + c_input.rna_type.identifier + '\n'  # NodeSocketInterfaceXXX
        # # outputs
        # if node_tree.outputs:
        #     source += ('    ' * deep) + '# OUTPUTS' + '\n'
        #     for c_output in node_tree.outputs:
        #         source += ('    ' * deep) + c_output.rna_type.identifier + '\n'  # NodeSocketInterfaceXXX
        # nodes
        if node_tree.nodes:
            source += '    ' * deep + '# NODES' + '\n'
            for node in node_tree.nodes:
                if node.type == 'GROUP':
                    # node group
                    source += ('    ' * deep) + parent_expr + str(deep + 1) + ' = bpy.data.node_groups.get(\'' + node.node_tree.name + '\')' + '\n'
                    source += ('    ' * deep) + 'if not ' + parent_expr + str(deep + 1) + ':' + '\n'
                    source += cls.to_source(node_tree=node.node_tree, parent_expr=parent_expr, deep=deep + 1) + '\n'
                    # source += ('    ' * deep) + 'node_group' + str(deep) + ' = node_groups.new(\'' + node.node_tree.name + '\', \'ShaderNodeTree\')' + '\n'
                    source += Node.to_source(node=node, parent_expr='node_tree' + str(deep), deep=deep) + '\n'

                else:
                    # simple node
                    source += Node.to_source(node=node, parent_expr='node_tree' + str(deep), deep=deep) + '\n'
        # links
        if node_tree.links:
            source += ('    ' * deep) + '# LINKS' + '\n'
            for link in node_tree.links:
                from_node_alias = Node.node_alias(link.from_node)
                to_node_alias = Node.node_alias(link.to_node)
                source += ('    ' * deep) + parent_expr + str(deep) + '.links.new(' \
                          + from_node_alias + '.outputs[' + str(list(link.from_node.outputs).index(link.from_socket)) + ']' + \
                          ', ' + to_node_alias + '.inputs[' + str(list(link.to_node.inputs).index(link.to_socket)) + ']' + \
                          ')' + '\n'
        return source

    @staticmethod
    def clear_source(parent_expr=''):
        # source for clear node tree
        source = 'for node in ' + parent_expr + '.nodes:' + '\n'
        source += '    ' + parent_expr + '.nodes.remove(node)' + '\n'
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
