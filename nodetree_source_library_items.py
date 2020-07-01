# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.props import CollectionProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_library_items(PropertyGroup):

    name: StringProperty()


def register():
    register_class(NODETREE_SOURCE_library_items)
    WindowManager.nodetree_source_library_items = CollectionProperty(type=NODETREE_SOURCE_library_items)
    WindowManager.nodetree_source_library_active_item = IntProperty(
        name='active item',
        default=0
    )


def unregister():
    del WindowManager.nodetree_source_library_active_item
    del WindowManager.nodetree_source_library_items
    unregister_class(NODETREE_SOURCE_library_items)
