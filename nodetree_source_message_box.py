# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_OT_messagebox(Operator):
    bl_idname = 'nodetree_source.messagebox'
    bl_label = ''

    message: StringProperty(
        name='message',
        description='message',
        default=''
    )
    width: IntProperty(
        name='width',
        default=400
    )
    word_wrap: BoolProperty(
        name='word_wrap',
        default=True
    )
    delimiter: StringProperty(
        name='delimiter',
        default='\n'
    )

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=self.width)

    def draw(self, context):
        layout = self.layout
        if self.word_wrap and self.delimiter in self.message:
            lines = self.message.split(self.delimiter)
            for line in lines:
                layout.label(text=line.strip())
        else:
            layout.label(text=self.message)
        layout.separator()


def register():
    register_class(NODETREE_SOURCE_OT_messagebox)


def unregister():
    unregister_class(NODETREE_SOURCE_OT_messagebox)
