# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import AddonPreferences
from bpy.props import EnumProperty
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_preferences(AddonPreferences):
    bl_idname = __package__

    dest_type: EnumProperty(
        name='Dest Type',
        items=[
            ('Text', 'Text', 'Text'),
            ('File', 'File', 'File'),
        ],
        default='Text'
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text='Export to')
        row = layout.row()
        row.prop(self, property='dest_type', expand=True)


def register():
    register_class(NODETREE_SOURCE_preferences)


def unregister():
    unregister_class(NODETREE_SOURCE_preferences)
