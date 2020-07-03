# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from . import nodetree_source_library_items
from . import nodetree_source_library_ops
from . import nodetree_source_library_panel


bl_info = {
    'name': 'NodeTree Source Library',
    'category': 'All',
    'author': 'NodeTree Source',
    'version': (1, 0, 0),
    'blender': (2, 83, 0),
    'location': 'N-Panel > NodeTree Source Library',
    'wiki_url': '',
    'tracker_url': '',
    'description': 'NodeTree Source Library Distribution'
}


def register():
    nodetree_source_library_items.register()
    nodetree_source_library_ops.register()
    nodetree_source_library_panel.register()


def unregister():
    nodetree_source_library_panel.unregister()
    nodetree_source_library_ops.unregister()
    nodetree_source_library_items.unregister()


if __name__ == '__main__':
    register()
