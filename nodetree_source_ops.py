# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class NODETREE_SOURCE_OT_main(Operator):
    bl_idname = 'nodetree_source.main'
    bl_label = 'nodetree_source: main'
    bl_description = 'nodetree_source - main operator'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print('nodetree_source.main - executed')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def register():
    register_class(NODETREE_SOURCE_OT_main)


def unregister():
    unregister_class(NODETREE_SOURCE_OT_main)
