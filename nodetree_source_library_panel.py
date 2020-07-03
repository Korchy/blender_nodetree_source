# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Panel, UIList
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_LIB_PT_panel_3d_view(Panel):
    bl_idname = 'NODETREE_SOURCE_LIB_PT_panel_3d_view'
    bl_label = 'NodeTree Source Library'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NodeTree Source'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            listtype_name='NODETREE_SOURCE_LIB_UL_lib_items',
            list_id='nodetree_source_lib_items',
            dataptr=context.window_manager,
            propname='nodetree_source_lib_items',
            active_dataptr=context.window_manager,
            active_propname='nodetree_source_lib_active_item'
        )
        col = row.column(align=True)
        col.operator('nodetree_source_lib.remove_material', icon='REMOVE', text='')


class NODETREE_SOURCE_LIB_PT_panel_shader_editor(Panel):
    bl_idname = 'NODETREE_SOURCE_LIB_PT_panel_shader_editor'
    bl_label = 'NodeTree Source Library'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'NodeTree Source'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            listtype_name='NODETREE_SOURCE_LIB_UL_lib_items',
            list_id='nodetree_source_lib_items1',
            dataptr=context.window_manager,
            propname='nodetree_source_lib_items',
            active_dataptr=context.window_manager,
            active_propname='nodetree_source_lib_active_item'
        )
        col = row.column(align=True)
        col.operator('nodetree_source_lib.remove_material', icon='REMOVE', text='')


class NODETREE_SOURCE_LIB_UL_lib_items(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        op = layout.operator('nodetree_source_lib.material_from_library', icon='BRUSH_DATA', text='')
        op.material_id = index
        layout.label(text=item.name)
        layout.label(text='', icon='MATERIAL')


def register():
    register_class(NODETREE_SOURCE_LIB_UL_lib_items)
    register_class(NODETREE_SOURCE_LIB_PT_panel_3d_view)
    register_class(NODETREE_SOURCE_LIB_PT_panel_shader_editor)


def unregister():
    unregister_class(NODETREE_SOURCE_LIB_PT_panel_shader_editor)
    unregister_class(NODETREE_SOURCE_LIB_PT_panel_3d_view)
    unregister_class(NODETREE_SOURCE_LIB_UL_lib_items)
