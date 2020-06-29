# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_node_tree import NodeTree


class Material:

    @classmethod
    def to_source(cls, context, scene_data):
        # convert active material to source
        source = '# MATERIAL' + '\n'
        active_material_object, material_type = cls.active_material_object(context=context)
        if active_material_object:
            source += cls._create_new_source(
                context=context,
                material_type=material_type,
                material_name=cls.material_alias(material=active_material_object)
            ) + '\n'
            source += NodeTree.to_source(
                node_tree=active_material_object.node_tree,
                parent_expr='node_tree'
            )
        return source

    @staticmethod
    def _create_new_source(context, material_type, material_name):
        # create new material by type - source
        source = ''
        if material_type == 'OBJECT':
            source = material_name + ' = bpy.data.materials.new(name=\'' + material_name + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif material_type == 'WORLD':
            source = material_name + ' = bpy.data.worlds.new(name=\'' + material_name + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif material_type == 'CONPOSITING':
            source = 'node_tree0 = bpy.context.scene.node_tree' + '\n'
            source += 'bpy.context.scene.use_nodes = True' + '\n'
        source += NodeTree.clear_source(parent_expr='node_tree0')
        return source

    @classmethod
    def active_material_object(cls, context):
        # get active material object
        material_object = None
        if cls.get_subtype(context=context) == 'ShaderNodeTree'\
                and cls.get_subtype2(context=context) == 'OBJECT':
            material_object = (context.active_object.active_material, cls.get_subtype2(context=context))
        elif cls.get_subtype(context=context) == 'ShaderNodeTree'\
                and cls.get_subtype2(context=context) == 'WORLD':
            material_object = (context.scene.world, cls.get_subtype2(context=context))
        elif cls.get_subtype(context=context) == 'CompositorNodeTree':
            material_object = (context.scene, 'CONPOSITING')
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

    @staticmethod
    def material_alias(material):
        # get text material alias-name
        material_name = material.name.lower()
        for ch in (' ', '.', '/'):
            material_name = material_name.replace(ch, '_')
        return material_name
