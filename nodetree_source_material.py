# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import re
from .nodetree_source_node_tree import NodeTree
from .nodetree_source_context import NodeTreeSourceContext


class Material:

    @classmethod
    def to_source(cls, context):
        # convert active material to source
        source = '# MATERIAL' + '\n'
        active_material_object = cls.active_material_object(context=context)
        subtype, subtype2 = NodeTreeSourceContext.context(context=context)
        if active_material_object:
            # create new material
            material = active_material_object.node_group if subtype == 'GeometryNodeTree' \
                else active_material_object
            material_name_original = material.name
            material_name = cls.material_alias(material=material)   # validated name as variable
            src_new, deep = cls._create_new_source(
                subtype=subtype,
                subtype2=subtype2,
                material_name=material_name,
                material_name_original=material_name_original
            )
            source += src_new + '\n'
            # material node tree
            node_tree = active_material_object.node_group if subtype == 'GeometryNodeTree' \
                else active_material_object.node_tree
            source += NodeTree.to_source(
                node_tree=node_tree,
                parent_expr='node_tree',
                deep=deep
            )
            # to active
            source += cls._source_to_active(
                subtype=subtype,
                subtype2=subtype2,
                material_name=material_name,
                deep=deep
            )
        return source

    @staticmethod
    def _create_new_source(subtype, subtype2, material_name, material_name_original):
        # create new material by type - source
        source = ''
        deep = 0
        # header
        if subtype == 'ShaderNodeTree' and subtype2 == 'OBJECT':
            source = material_name + ' = bpy.data.materials.new(name=\'' + \
                     material_name_original.replace('\'', '\\\'') + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif subtype == 'ShaderNodeTree' and subtype2 == 'LIGHT':
            deep = 1
            source = 'if bpy.context.scene.render.engine == \'CYCLES\':' + '\n'
            source += ('    ' * deep) + \
                'selected_objects = (obj for obj in bpy.data.objects' + '\n' + \
                ('    ' * (deep + 1)) + 'if obj.select_get() and obj.type == \'LIGHT\' and obj.data.use_nodes)' \
                + '\n'
            source += ('    ' * deep) + 'for obj in selected_objects:' + '\n'
            deep += 1
            source += ('    ' * deep) + 'obj.data.use_nodes = True' + '\n'
            source += ('    ' * deep) + 'node_tree' + str(deep) + ' = ' + 'obj.data.node_tree' + '\n'
        elif subtype == 'ShaderNodeTree' and subtype2 == 'WORLD':
            source = material_name + ' = bpy.data.worlds.new(name=\'' + material_name + '\')' + '\n'
            source += material_name + '.use_nodes = True' + '\n'
            source += 'node_tree0 = ' + material_name + '.node_tree' + '\n'
        elif subtype == 'GeometryNodeTree':
            deep += 1
            source += 'node_tree' + str(deep) + ' = bpy.data.node_groups.get(\'' + material_name + '\')' + '\n'
            source += 'if not node_tree' + str(deep) + ':' + '\n'
            source += ('    ' * deep) + 'node_tree' + str(deep) + ' = bpy.data.node_groups.new(\'' + \
                material_name + '\', \'GeometryNodeTree\')' + '\n'
        elif subtype == 'CompositorNodeTree':
            source = 'node_tree0 = bpy.context.scene.node_tree' + '\n'
            source += 'bpy.context.scene.use_nodes = True' + '\n'
        return source, deep

    @staticmethod
    def _source_to_active(subtype, subtype2, material_name, deep=0):
        # make created material active
        source = '\n' + ('    ' * deep) + '# TO ACTIVE' + '\n'
        if subtype == 'ShaderNodeTree' and subtype2 == 'OBJECT':
            source += ('    ' * deep) + 'selected_objects = (obj for obj in bpy.data.objects if obj.select_get())' \
                      + '\n'
            source += ('    ' * deep) + 'for obj in selected_objects:' + '\n'
            source += ('    ' * (deep + 1)) + 'obj.active_material = ' + material_name + '\n'
        elif subtype == 'ShaderNodeTree' and subtype2 == 'LIGHT':
            # everything made in _create_new_source
            pass
        elif subtype == 'ShaderNodeTree' and subtype2 == 'WORLD':
            source += ('    ' * deep) + 'bpy.context.scene.world = ' + material_name + '\n'
        elif subtype == 'GeometryNodeTree':
            deep = 0
            source += ('    ' * deep) + \
                'selected_objects = (obj for obj in bpy.data.objects if obj.select_get())' + '\n'
            source += ('    ' * deep) + 'for obj in selected_objects:' + '\n'
            source += ('    ' * (deep + 1)) + \
                'modifier = obj.modifiers.new(name=\'' + material_name + '\', type=\'NODES\')' + '\n'
            source += ('    ' * (deep + 1)) + 'modifier.node_group = node_tree' + str(deep + 1) + '\n'
        elif subtype == 'CompositorNodeTree':
            # everything made in _create_new_source
            pass
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
        elif subtype == 'GeometryNodeTree':
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
        material_name = ''.join((x if x.isalnum() else '_' for x in material_name))
        material_name = re.sub('_+', '_', material_name)
        if material_name[0].isdigit():
            material_name = '_' + material_name
        return material_name
