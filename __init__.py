# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from . import nodetree_source_ops
from . import nodetree_source_panel
from . import nodetree_source_preferences
from . import nodetree_source_message_box
from . import nodetree_source_library_items
from . import nodetree_source_library_ops
from . import nodetree_source_library_panel
from .addon import Addon


bl_info = {
    'name': 'NodeTree Source',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 2, 2),
    'blender': (2, 93, 0),
    'location': 'N-Panel > NodeTree Source',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-nodetree-source/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-nodetree-source/',
    'description': 'Converting Node Tree to Python source code'
}


def register():
    if not Addon.dev_mode():
        nodetree_source_message_box.register()
        nodetree_source_ops.register()
        nodetree_source_panel.register()
        nodetree_source_preferences.register()
        nodetree_source_library_items.register()
        nodetree_source_library_ops.register()
        nodetree_source_library_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] +
              ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        nodetree_source_library_panel.unregister()
        nodetree_source_library_ops.unregister()
        nodetree_source_library_items.unregister()
        nodetree_source_preferences.unregister()
        nodetree_source_panel.unregister()
        nodetree_source_ops.unregister()
        nodetree_source_message_box.unregister()


if __name__ == '__main__':
    register()
