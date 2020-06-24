# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_preferences(AddonPreferences):
    bl_idname = __package__

    pref1: StringProperty(
        name='pref1',
        default='nodetree_source'
    )

    def draw(self, context):
        self.layout.prop(self, 'pref1')


def register():
    register_class(NODETREE_SOURCE_preferences)


def unregister():
    unregister_class(NODETREE_SOURCE_preferences)
