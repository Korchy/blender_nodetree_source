# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source


class Material:

    @staticmethod
    def to_source(context):
        # convert active material to source
        source = 'x'

        return source

    @classmethod
    def active_material(cls, context):
        # get active material (material object)
        material_object = None
        if cls.get_subtype(context=context) == 'ShaderNodeTree'\
                and cls.get_subtype2(context=context) == 'OBJECT':
            material_object = context.active_object.active_material
        elif cls.get_subtype(context=context) == 'ShaderNodeTree'\
                and cls.get_subtype2(context=context) == 'WORLD':
            material_object = context.scene.world
        elif cls.get_subtype(context=context) == 'CompositorNodeTree':
            material_object = context.scene
        return material_object

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
