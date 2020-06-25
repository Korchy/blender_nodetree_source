# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_material import Material


class NodeTreeSource:

    @classmethod
    def to_source(cls, context):
        # convert active material to source
        print(Material.get_subtype(context=context))
        print(Material.get_subtype2(context=context))
        # print(context.space_data.tree_type)
        pass

    @classmethod
    def get_active_material(cls, context):
        # get active material from context

        pass
