# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_PT_panel_3d_view(Panel):
    bl_idname = 'NODETREE_SOURCE_PT_panel_3d_view'
    bl_label = 'NodeTree Source'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'nodetree_source'

    def draw(self, context):
        self.layout.operator('nodetree_source.to_source', icon='NODETREE')


class NODETREE_SOURCE_PT_panel_shader_editor(Panel):
    bl_idname = 'NODETREE_SOURCE_PT_panel_shader_editor'
    bl_label = 'NodeTree Source'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'nodetree_source'

    def draw(self, context):
        self.layout.operator('nodetree_source.to_source', icon='NODETREE')


def register():
    register_class(NODETREE_SOURCE_PT_panel_3d_view)
    register_class(NODETREE_SOURCE_PT_panel_shader_editor)


def unregister():
    unregister_class(NODETREE_SOURCE_PT_panel_shader_editor)
    unregister_class(NODETREE_SOURCE_PT_panel_3d_view)
