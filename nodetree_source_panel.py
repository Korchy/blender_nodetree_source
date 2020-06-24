# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_PT_panel(Panel):
    bl_idname = 'NODETREE_SOURCE_PT_panel'
    bl_label = 'nodetree_source'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'nodetree_source'

    def draw(self, context):
        self.layout.operator('nodetree_source.main', icon='BLENDER', text='nodetree_source execute')


def register():
    register_class(NODETREE_SOURCE_PT_panel)


def unregister():
    unregister_class(NODETREE_SOURCE_PT_panel)
