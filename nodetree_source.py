# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

import os
from shutil import copyfile, copytree, make_archive
import tempfile
from .nodetree_source_material import Material
from .nodetree_source_library import NodeTreeSourceLibrary
from .nodetree_source_file_manager import FileManager
import bpy


class NodeTreeSource:

    @classmethod
    def library_to_add_on(cls, context):
        # export library to separate add-on
        dest_path = FileManager.abs_path(context.preferences.addons[__package__].preferences.export_path)
        if dest_path and os.path.exists(dest_path):
            with tempfile.TemporaryDirectory() as temp_dir:
                folder_to_zip = FileManager.abs_path(os.path.join(temp_dir, NodeTreeSourceLibrary.idname))
                folder_to_zip_content = FileManager.abs_path(os.path.join(temp_dir, NodeTreeSourceLibrary.idname, NodeTreeSourceLibrary.idname))
                os.makedirs(folder_to_zip)
                # copy library source to zip folder
                copytree(NodeTreeSourceLibrary.library_path(), os.path.join(folder_to_zip_content, NodeTreeSourceLibrary.idname))
                # copy .py files
                py_files = [
                    'nodetree_source_library.py', 'nodetree_source_library_items.py', 'nodetree_source_library_ops.py',
                    'nodetree_source_library_panel.py', 'nodetree_source_context.py'
                ]
                for py_file in py_files:
                    copyfile(os.path.join(os.path.dirname(FileManager.abs_path(__file__)), py_file), os.path.join(folder_to_zip_content, py_file))
                # init file with renaming
                copyfile(os.path.join(os.path.dirname(FileManager.abs_path(__file__)), 'nodetree_source_library_template_init.py'), os.path.join(folder_to_zip_content, '__init__.py'))
                # make add-on archive
                arch = make_archive(os.path.join(dest_path, NodeTreeSourceLibrary.idname), 'zip', folder_to_zip)
                bpy.ops.nodetree_source.messagebox('INVOKE_DEFAULT', message='Add-on created in:\n' + arch)
        else:
            bpy.ops.nodetree_source.messagebox('INVOKE_DEFAULT', message='Please, specify the existed path for export.')

    @classmethod
    def material_to_library(cls, context, scene_data):
        # add material to source library
        source = ''
        material = Material.active_material_object(context=context)[0]
        # save source to file
        library_path = NodeTreeSourceLibrary.library_path()
        source_file_alias = Material.material_alias(material=material)
        source_file_name = source_file_alias + '.py'
        source_file_path = os.path.join(library_path, source_file_name)
        if os.path.exists(source_file_path):
            bpy.ops.nodetree_source.messagebox('INVOKE_DEFAULT', message='Material with the same name already exists in the library!')
        else:
            # get material source
            # header
            external_items_list = Material.external_items(
                material=material
            )
            source += cls._header(has_external=bool(external_items_list), material_name=source_file_alias)
            # material data
            source += Material.to_source(context=context, scene_data=scene_data)
            # write to file
            with open(file=source_file_path, mode='w', encoding='utf8') as source_file:
                source_file.write(source)
            # external items (textures,... etc)
            if external_items_list:
                external_items_path = os.path.join(library_path, source_file_alias)
                os.makedirs(external_items_path)
                for item in external_items_list:
                    if os.path.exists(item['path']):
                        copyfile(item['path'], os.path.join(external_items_path, item['name']))
            # add to library list
            library_item = context.window_manager.nodetree_source_lib_items.add()
            library_item.name = source_file_alias

    @classmethod
    def material_to_text(cls, context, scene_data):
        # show material as source in TEXT_EDITOR window
        material = Material.active_material_object(context=context)[0]
        source_file_alias = Material.material_alias(material=material)
        # header
        external_items_list = Material.external_items(
            material=material
        )
        source = cls._header(has_external=bool(external_items_list), material_name=source_file_alias)
        # material data
        source += Material.to_source(context=context, scene_data=scene_data)
        # create text object with source
        text_block = scene_data.texts.get(material.name)
        if not text_block:
            text_block = scene_data.texts.new(name=material.name)
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

    @staticmethod
    def _header(material_name, has_external=False):
        # header for material source
        header = 'import bpy' + '\n'
        if has_external:
            header += 'import os' + '\n'
            header += '\n'
            header += 'external_items_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ' + \
                      '\'' + NodeTreeSourceLibrary.idname + '\', ' + \
                      '\'' + material_name + '\')' + \
                      '\n'
        header += '\n'
        return header
