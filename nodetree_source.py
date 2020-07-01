# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import os
from .nodetree_source_material import Material
import bpy


class NodeTreeSource:

    @classmethod
    def material_to_library(cls, context, scene_data):
        # add material to source library
        source = 'import bpy' + '\n\n'
        source += Material.to_source(context=context, scene_data=scene_data)
        # save source to file
        library_path = cls._material_library_path()
        source_file_name = Material.material_alias(material=Material.active_material_object(context=context)[0]) + '.py'
        source_file_name_full = os.path.join(library_path, source_file_name)
        if os.path.exists(source_file_name_full):
            bpy.ops.nodetree_source.messagebox('INVOKE_DEFAULT', message='Material with the same name already exists in the library!')
        else:
            with open(file=source_file_name_full, mode='w', encoding='utf8') as source_file:
                source_file.write(source)

    @staticmethod
    def _material_library_path():
        # return path to material library sources
        library_path = os.path.join(os.path.dirname(__file__), 'node_tree_lib')
        if not os.path.exists(library_path):
            os.makedirs(library_path)
        return library_path

    @staticmethod
    def material_to_text(context, scene_data):
        # show material as source in TEXT_EDITOR window
        source = 'import bpy' + '\n\n'
        source += Material.to_source(context=context, scene_data=scene_data)
        # create text object with source
        source_name = Material.active_material_object(context=context)[0].name
        text_block = scene_data.texts.get(source_name)
        if not text_block:
            text_block = scene_data.texts.new(name=source_name)
        text_block.from_string(string=source)
        text_block.select_set(line_start=0, char_start=0, line_end=0, char_end=0)
        text_block.current_line_index = 0
        # show text object in window
        show_in_area = None
        for area in context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                show_in_area = area
                break
        if not show_in_area:
            for area in context.screen.areas:
                if area.type not in ['PROPERTIES', 'OUTLINER']:
                    show_in_area = area
                    break
        if show_in_area:
            show_in_area.type = 'TEXT_EDITOR'
            show_in_area.spaces.active.text = text_block
