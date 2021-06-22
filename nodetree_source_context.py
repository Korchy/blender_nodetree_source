# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source


class NodeTreeSourceContext:

    @classmethod
    def context(cls, context):
        # get active material context info
        return cls._get_subtype(context=context), cls._get_subtype2(context=context)

    @staticmethod
    def _get_subtype(context):
        # material subtype
        if context.area and context.space_data.type == 'NODE_EDITOR':
            return context.space_data.tree_type
        else:
            return 'ShaderNodeTree'

    @staticmethod
    def _get_subtype2(context):
        # material subtype2
        if context.area and context.space_data.type == 'NODE_EDITOR':
            if context.object and context.object.type == 'LIGHT':
                return 'LIGHT'
            else:
                return context.space_data.shader_type
        else:
            return 'OBJECT'
