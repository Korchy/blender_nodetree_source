# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class
from .nodetree_source_library import NodeTreeSourceLibrary


class NODETREE_SOURCE_lib_items(PropertyGroup):

    name: StringProperty()


def register():
    register_class(NODETREE_SOURCE_lib_items)
    WindowManager.nodetree_source_lib_items = CollectionProperty(type=NODETREE_SOURCE_lib_items)
    WindowManager.nodetree_source_lib_active_item = IntProperty(
        name='active item',
        default=0
    )
    NodeTreeSourceLibrary.init_library_items(context=bpy.context)


def unregister():
    NodeTreeSourceLibrary.clear_library_items(context=bpy.context)
    del WindowManager.nodetree_source_lib_active_item
    del WindowManager.nodetree_source_lib_items
    unregister_class(NODETREE_SOURCE_lib_items)
