# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

# Blender types conversion
# Blender types with prefix BL

import re
import sys
from mathutils import Vector, Color


class BlTypesConversion:

    @staticmethod
    def source_by_type(item, value, parent_expr='', deep=0):
        # value as string by type
        if isinstance(value, Vector):
            return BLVector.to_source(value=value, parent_expr=parent_expr, deep=deep)
        elif isinstance(value, Color):
            return BLColor.to_source(value=value, parent_expr=parent_expr, deep=deep)
        elif isinstance(value, (int, float, bool, set)):
            return ('    ' * deep) + ((parent_expr + ' = ') if parent_expr else '') + str(value)
        elif isinstance(value, str):
            value_escaped = value.translate(str.maketrans({'\'': r'\'', '\\': r'\\'}))  # escape some characters (', \)
            return ('    ' * deep) + ((parent_expr + ' = ') if parent_expr else '') + '\'' + value_escaped + '\''
        elif hasattr(sys.modules[__name__], 'BL' + value.__class__.__name__):
            value_class = getattr(sys.modules[__name__], 'BL' + value.__class__.__name__)
            return value_class.to_source(value=value, parent_expr=parent_expr, deep=deep)
        else:
            print('ERR: Undefined type: item = ', item,
                  'value = ', value, ' (', type(value), ')',
                  'item_class = ', item.__class__.__name__,
                  'value_class = ', value.__class__.__name__,
                  'parent_expr = ', parent_expr
                  )
            return None

    @staticmethod
    def source_from_complex_type(value, excluded_attributes: list = None,
                                 preordered_attributes: list = None,
                                 complex_attributes: list = None, parent_expr='', deep=0):
        # excluded attributes - don't process them (ex: type, select)
        excluded_attributes = excluded_attributes if excluded_attributes is not None else []
        # preordered attributes - need to be processed first because when changed - change another attributes (ex: mode)
        preordered_attributes = preordered_attributes if preordered_attributes is not None else []
        preordered_attributes = [
            attr for attr in preordered_attributes if
            hasattr(value, attr)
            and getattr(value, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(value, attr), str) and not getattr(value, attr))  # don't add attributes == '' (empty string)
            and (not value.is_property_readonly(attr) or attr in complex_attributes)
        ]
        # complex attributes - can be readonly but must be processed inside themselves  (ex: mapping)
        complex_attributes = complex_attributes if complex_attributes is not None else []
        attributes = [
            attr for attr in dir(value) if
            hasattr(value, attr)
            and not attr.startswith('__')
            and (not attr.startswith('bl_') or attr == 'bl_idname')
            and attr not in excluded_attributes
            and attr not in preordered_attributes  # don't add preorderd attributes, added first manually
            and not callable(getattr(value, attr))
            and getattr(value, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(value, attr), str) and not getattr(value,
                                                                           attr))  # don't add attributes == '' (empty string)
            and (not value.is_property_readonly(attr) or attr in complex_attributes)
        ]
        source = ''
        # first - preordered attributes, next - all other attributes
        all_attributes = preordered_attributes + attributes
        for attribute in all_attributes:
            source_cond = ('    ' * deep) + 'if hasattr(' + parent_expr + ', \'' + attribute + '\'):' + '\n'
            source_expr = BlTypesConversion.source_by_type(
                item=attribute,
                value=getattr(value, attribute),
                parent_expr=parent_expr + '.' + attribute,
                deep=deep + 1
            )
            if source_expr is not None:
                source += source_cond + source_expr + ('' if source_expr[-1:] == '\n' else '\n')
        return source


class TupleType:
    # common class for tuple-type types

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + ((parent_expr + ' = ') if parent_expr else '') + str(tuple(value))


class BLColor(TupleType):
    pass


class BLVector(TupleType):
    pass


class BLMatrix:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ''
        for i in range(len(value)):
            source += (', ' if source else '') + str(tuple(value.row[i]))
        source = '(' + source + ')'
        return ('    ' * deep) + parent_expr + ' = ' + source


class BLbpy_prop_array(TupleType):
    pass


class BLEuler(TupleType):
    # maybe not right convert as tuple, Euler((x=0.0, y=0.0, z=0.0), order='XYZ') converts as (0.0, 0.0, 0.0)
    # at 2.83 - works
    pass


class BLbpy_prop_collection:
    # collection of properties
    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ''
        for item_index, item in enumerate(value):
            source_expr = BlTypesConversion.source_by_type(
                item=item,
                value=value[item_index],
                parent_expr=parent_expr + '[' + str(item_index) + ']',
                deep=deep
            )
            if source_expr is not None:
                source += source_expr
        return source


class BLScene:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') + 'bpy.data.scenes.get(\'' + value.name + '\')'


class BLObject:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') + 'bpy.data.objects.get(\'' + value.name + '\')'


class BLImage:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ('    ' * deep) + 'if \'' + value.name + '\' not in bpy.data.images:' + '\n'
        source += ('    ' * (
                    deep + 1)) + 'if os.path.exists(os.path.join(external_items_dir, \'' + value.name + '\')):' + '\n'
        source += ('    ' * (
                    deep + 2)) + 'bpy.data.images.load(os.path.join(external_items_dir, \'' + value.name + '\'))' + '\n'
        source += ('    ' * deep) + (
            (parent_expr + ' = ') if parent_expr else '') + 'bpy.data.images.get(\'' + value.name + '\')'
        return source


class BLImageTexture:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ('    ' * deep) + 'image_texture = bpy.data.textures.get(\'' + value.name + '\')' + '\n'
        source += ('    ' * deep) + 'if not image_texture:' + '\n'
        source += ('    ' * (deep + 1)) + \
            'image_texture = bpy.data.textures.new(name=\'' + value.name + '\', type=\'' + value.type + '\')' + '\n'
        source += BlTypesConversion.source_from_complex_type(
            value=value,
            preordered_attributes=['use_color_ramp'],
            complex_attributes=['color_ramp'],
            parent_expr='image_texture',
            deep=deep + 1
        )
        source += ('    ' * deep) + parent_expr + ' = image_texture' + '\n'
        return source


class BLBlendTexture(BLImageTexture):
    pass


class BLCloudsTexture(BLImageTexture):
    pass


class BLDistortedNoiseTexture(BLImageTexture):
    pass


class BLMagicTexture(BLImageTexture):
    pass


class BLMarbleTexture(BLImageTexture):
    pass


class BLMusgraveTexture(BLImageTexture):
    pass


class BLNoiseTexture(BLImageTexture):
    pass


class BLStucciTexture(BLImageTexture):
    pass


class BLVoronoiTexture(BLImageTexture):
    pass


class BLWoodTexture(BLImageTexture):
    pass


class BLCacheFile:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ('    ' * deep) + 'if \'' + value.name + '\' not in bpy.data.cache_files:' + '\n'
        source += ('    ' * (deep + 1)) + \
            'if os.path.exists(os.path.join(external_items_dir, \'' + value.name + '\')):' + '\n'
        source += ('    ' * (deep + 2)) + \
            'bpy.ops.cachefile.open(os.path.join(external_items_dir, \'' + value.name + '\'))' + '\n'
        source += ('    ' * deep) + \
            ((parent_expr + ' = ') if parent_expr else '') + 'bpy.data.cache_files.get(\'' + value.name + '\')'
        return source


class BLText:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') + 'bpy.data.texts.get(\'' + value.name + '\')'


class BLParticleSystem:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') \
               + 'bpy.context.active_object.particle_systems.get(\'' + value.name + '\')'


class BLShaderNodeTree:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') + 'bpy.data.node_groups.get(\'' + value.name + '\')'


class BLCompositorNodeTree(BLShaderNodeTree):
    pass


class BLGeometryNodeTree(BLShaderNodeTree):
    pass


class BLNodeFrame:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return ('    ' * deep) + \
               ((parent_expr + ' = ') if parent_expr else '') \
               + 'node_tree' + str((deep - 1) if deep > 0 else deep) + '.nodes.get(\'' + value.name + '\')'


class BLCurveMapping:
    # mapping and curves

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        # complex attributes - can be readonly but must be processed inside themselves
        return BlTypesConversion.source_from_complex_type(
            value=value,
            complex_attributes=['curves'],
            parent_expr=parent_expr,
            deep=deep
        )


class BLCurveMap:
    # curve and points

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        return BlTypesConversion.source_from_complex_type(
            value=value,
            complex_attributes=['points'],
            parent_expr=parent_expr,
            deep=deep
        )


class BLCurveMapPoint:
    # point

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ('    ' * deep) + \
            'if ' + parent_expr.strip()[-2:][:1] + ' >= len(' + parent_expr.strip()[:-3] + '):' + '\n'
        source += ('    ' * (deep + 1)) + \
            parent_expr.strip()[:-3] + '.new(' + str(value.location.x) + ', ' + str(value.location.y) + ')' + '\n'
        source += BlTypesConversion.source_from_complex_type(
            value=value,
            parent_expr=parent_expr,
            deep=deep
        )
        return source


class BLCurveProfile(BLCurveMap):
    # curve

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = ('    ' * deep) + 'for i in range(' + str(len(value.points) - 2) + '):' + '\n'
        source += ('    ' * (deep + 1)) + parent_expr + '.points.add(x=0.0, y=0.0)' + '\n'
        source += BlTypesConversion.source_from_complex_type(
            value=value,
            complex_attributes=['points'],
            parent_expr=parent_expr,
            deep=deep
        )
        return source


class BLCurveProfilePoint:
    # point

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        source = BlTypesConversion.source_from_complex_type(
            value=value,
            parent_expr=parent_expr,
            deep=deep
        )
        return source


class BLColorRamp:
    # color ramp

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        # complex attributes - can be readonly but must be processed inside themselves
        return BlTypesConversion.source_from_complex_type(
            value=value,
            complex_attributes=['elements'],
            parent_expr=parent_expr,
            deep=deep
        )


class BLColorRampElement:
    # color ramp element

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        current_element = re.search('\[([\d]+)\]', parent_expr).group(1)
        elements = re.search('(.+)\[',parent_expr).group(1)
        source = ('    ' * deep) + 'if ' + current_element + ' >= len(' + elements + '):' + '\n'
        source += ('    ' * (deep + 1)) + elements + '.new(' + str(value.position) + ')' + '\n'
        source += BlTypesConversion.source_from_complex_type(
            value=value,
            parent_expr=parent_expr,
            deep=deep
        )
        return source


class BLGeometryNodeRepeatOutput:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        node_str = '.'.join(parent_expr.split('.')[:-1])
        from .nodetree_source_node import Node
        return ('    ' * deep) + \
            node_str + '.pair_with_output(' + Node.node_alias(node=value, deep=deep-1) + ')'


class BLRepeatItem:

    @classmethod
    def to_source(cls, value, parent_expr='', deep=0):
        current_element = re.search('\[([\d]+)\]', parent_expr).group(1)
        elements = re.search('(.+)\[', parent_expr).group(1)
        # return 'element=' + current_element + ' elements=' + elements
        source = ('    ' * deep) + 'if ' + current_element + ' >= len(' + elements + '):' + '\n'
        source += ('    ' * (deep + 1)) + elements + '.new(socket_type=\'' + value.socket_type + '\', name=\'' + value.name + '\')' + '\n'
        return source


class BLGeometryNodeSimulationOutput(BLGeometryNodeRepeatOutput):
    pass


class BLSimulationStateItem(BLRepeatItem):
    pass
