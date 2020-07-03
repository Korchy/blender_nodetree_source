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

    export_path: StringProperty(
        name='Export Path',
        subtype='DIR_PATH',
        default='D:/'
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text='Export')
        box.prop(self, property='export_path')


def register():
    register_class(NODETREE_SOURCE_preferences)


def unregister():
    unregister_class(NODETREE_SOURCE_preferences)
