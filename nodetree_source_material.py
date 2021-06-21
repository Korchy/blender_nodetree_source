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
        active_material_object = cls.active_material_object(context=context)
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        print(subtype, subtype2)
        if active_material_object:
            material_name = cls.material_alias(material=active_material_object.node_group) \
                if subtype == 'GeometryNodeTree' \
                else cls.material_alias(material=active_material_object)
            src_new, deep = cls._create_new_source(
                subtype=subtype,
                subtype2=subtype2,
                material_name=material_name
            )
            source += src_new + '\n'
            node_tree = active_material_object.node_group if subtype == 'GeometryNodeTree' \
                else active_material_object.node_tree
            source += NodeTree.to_source(
                node_tree=node_tree,
                parent_expr='node_tree',
                deep=deep
            )
            source += cls._source_to_active(
                material_type=subtype2,
                material_name=material_name,
                deep=deep
            )
        return source

    @staticmethod
    def _create_new_source(subtype, subtype2, material_name):
        # create new material by type - source
        source = ''
        deep = 0
        if subtype == 'ShaderNodeTree' and subtype2 == 'OBJECT':
            source = material_name + ' = bpy.data.materials.new(name=\'' + material_name + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif subtype == 'ShaderNodeTree' and subtype2 == 'LIGHT':
            deep = 1
            source = 'if bpy.context.active_object and bpy.context.active_object.type == "LIGHT":' + '\n'
            source += ('    ' * deep) + material_name + ' = bpy.context.active_object.data' + '\n'
            source += ('    ' * deep) + material_name + '.use_nodes = True' + '\n'
            source += ('    ' * deep) + 'node_tree' + str(deep) + ' = ' + material_name + '.node_tree' + '\n'
        elif subtype == 'GeometryNodeTree':
            # deep = 1
            # source += 'node_tree' + str(deep) + ' = bpy.data.node_groups.get(\'' + material_name + '\')' + '\n'
            # source += 'if not node_tree' + str(deep) + ':' + '\n'
            # source += ('    ' * deep) + 'node_tree' + str(deep) + ' = bpy.data.node_groups.new(\'' + \
            #     material_name + '\', \'GeometryNodeTree\')' + '\n'
            source += ('    ' * deep) + 'node_tree' + str(deep) + ' = bpy.data.node_groups.new(\'' + \
                material_name + '\', \'GeometryNodeTree\')' + '\n'
        elif subtype == 'ShaderNodeTree' and subtype2 == 'WORLD':
            source = material_name + ' = bpy.data.worlds.new(name=\'' + material_name + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif subtype == 'CompositorNodeTree':
            source = 'node_tree0 = bpy.context.scene.node_tree' + '\n'
            source += 'bpy.context.scene.use_nodes = True' + '\n'
        source += NodeTree.clear_source(
            parent_expr='node_tree' + str(deep),
            deep=deep
        )
        return source, deep

    @staticmethod
    def _source_to_active(material_type, material_name, deep=0):
        # make created material active
        source = '\n' + '# TO ACTIVE' + '\n'
        if material_type == 'OBJECT':
            source += ('    ' * deep) + 'selected_objects = (obj for obj in bpy.data.objects if obj.select_get())' \
                      + '\n'
            source += ('    ' * deep) + 'for obj in selected_objects:' + '\n'
            source += ('    ' * (deep + 1)) + 'obj.active_material = ' + material_name + '\n'
        elif material_type == 'WORLD':
            source += ('    ' * deep) + 'bpy.context.scene.world = ' + material_name + '\n'
        return source

    @classmethod
    def active_material_object(cls, context):
        # get active material object
        material_object = None
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if subtype == 'ShaderNodeTree' and subtype2 == 'OBJECT':
            material_object = context.active_object.active_material
        if subtype == 'ShaderNodeTree' and subtype2 == 'LIGHT':
            material_object = context.active_object.data
        elif subtype == 'ShaderNodeTree' and subtype2 == 'WORLD':
            material_object = context.scene.world
        elif subtype == 'GeometryNodeTree' and subtype2 == 'OBJECT':
            material_object = context.active_object.modifiers.active
        elif subtype == 'CompositorNodeTree':
            material_object = context.scene
        return material_object

    @staticmethod
    def external_items(material):
        # return external items list (textures,... etc)
        node_tree = material.node_group if material.bl_rna.name == 'Nodes Modifier' else material.node_tree
        return NodeTree.external_items(
            node_tree=node_tree
        )

    @staticmethod
    def material_alias(material):
        # get text material alias-name
        material_name = material.name.lower()
        for ch in (' ', '.', '/'):
            material_name = material_name.replace(ch, '_')
        return material_name
