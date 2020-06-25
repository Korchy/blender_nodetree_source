# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_nodetree_source

from .nodetree_source_material import Material


class NodeTreeSource:

    @classmethod
    def to_source(cls, context, scene_data):
        # convert active material to source
        source = Material.to_source(context=context)
        if source:
            if context.preferences.addons[__package__].preferences.dest_type == 'Text':
                # show in TEXT_EDITOR window
                cls._to_text(
                    source_name=Material.active_material_object(context=context).name,
                    source=source,
                    context=context,
                    scene_data=scene_data
                )
            elif context.preferences.addons[__package__].preferences.dest_type == 'File':
                cls._to_file(
                    source_name=Material.active_material_object(context=context).name,
                    source=source,
                    dest_file=''
                )

    @staticmethod
    def _to_file(source_name, source, dest_file):
        # save source to external file

        # todo

        pass

    @staticmethod
    def _to_text(source_name, source, context, scene_data):
        # show in TEXT_EDITOR window
        # create text object with source
        text_block = scene_data.texts.get(source_name)
        if not text_block:
            text_block = scene_data.texts.new(name=source_name)
        text_block.from_string(string=source)
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
