# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source


class Material:

    @staticmethod
    def get_subtype(context):
        # material subtype
        if context.area and context.space_data.type == 'NODE_EDITOR':
            return context.space_data.tree_type
        else:
            return 'ShaderNodeTree'

    @staticmethod
    def get_subtype2(context):
        # material subtype2
        if context.area and context.space_data.type == 'NODE_EDITOR':
            return context.space_data.shader_type
        else:
            return 'OBJECT'
