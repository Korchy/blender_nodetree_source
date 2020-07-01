# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Panel, UIList
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_PT_panel_3d_view(Panel):
    bl_idname = 'NODETREE_SOURCE_PT_panel_3d_view'
    bl_label = 'NodeTree Source Bilder'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NodeTree Source'

    def draw(self, context):
        layout = self.layout
        layout.operator('nodetree_source.material_to_text', icon='NODETREE')
        layout.operator('nodetree_source.material_to_library', icon='PACKAGE')


class NODETREE_SOURCE_PT_panel_shader_editor(Panel):
    bl_idname = 'NODETREE_SOURCE_PT_panel_shader_editor'
    bl_label = 'NodeTree Source Builder'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeTree Source'

    def draw(self, context):
        layout = self.layout
        layout.operator('nodetree_source.material_to_text', icon='NODETREE')
        layout.operator('nodetree_source.material_to_library', icon='PACKAGE')


def register():
    register_class(NODETREE_SOURCE_PT_panel_3d_view)
    register_class(NODETREE_SOURCE_PT_panel_shader_editor)


def unregister():
    unregister_class(NODETREE_SOURCE_PT_panel_shader_editor)
    unregister_class(NODETREE_SOURCE_PT_panel_3d_view)
