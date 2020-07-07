# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_node_tree import NodeTree
from .nodetree_source_context import NodeTreeSourceContext


class Material:

    @classmethod
    def to_source(cls, context, scene_data):
        # convert active material to source
        source = '# MATERIAL' + '\n'
        active_material_object, material_type = cls.active_material_object(context=context)
        if active_material_object:
            material_name = cls.material_alias(material=active_material_object)
            source += cls._create_new_source(
                context=context,
                material_type=material_type,
                material_name=material_name
            ) + '\n'
            source += NodeTree.to_source(
                owner=active_material_object,
                node_tree=active_material_object.node_tree,
                parent_expr='node_tree'
            )
            source += cls._source_to_active(
                material_type=material_type,
                material_name=material_name
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

    @staticmethod
    def _source_to_active(material_type, material_name):
        # make created material active
        source = '\n' + '# TO ACTIVE' + '\n'
        if material_type == 'OBJECT':
            source += 'selected_objects = (obj for obj in bpy.data.objects if obj.select_get())' + '\n'
            source += 'for obj in selected_objects:' + '\n'
            source += ('    ' * 1) + 'obj.active_material = ' + material_name + '\n'
        elif material_type == 'WORLD':
            source += 'bpy.context.scene.world = ' + material_name + '\n'
        return source

    @classmethod
    def active_material_object(cls, context):
        # get active material object
        material_object = None
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if subtype == 'ShaderNodeTree' and subtype2 == 'OBJECT':
            material_object = (context.active_object.active_material, subtype2)
        elif subtype == 'ShaderNodeTree' and subtype2 == 'WORLD':
            material_object = (context.scene.world, subtype2)
        elif subtype == 'CompositorNodeTree':
            material_object = (context.scene, 'CONPOSITING')
        return material_object

    @staticmethod
    def external_items(material):
        # return external items list (textures,... etc)
        return NodeTree.external_items(
            node_tree=material.node_tree
        )

    @staticmethod
    def material_alias(material):
        # get text material alias-name
        material_name = material.name.lower()
        for ch in (' ', '.', '/'):
            material_name = material_name.replace(ch, '_')
        return material_name
