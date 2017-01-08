#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_ITEM

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.PRESET,
                    'label': tagger.LABEL_PRESET,
                    'datatype': 'string',
                    'value': tagger.RANDOM,
                    'popup': tagger.presets.presets_popup(),
                    'flags': ['optional']
                }, {
                    'name': tagger.WITH_EXISTING,
                    'label': tagger.LABEL_WITH_EXISTING,
                    'datatype': 'string',
                    'value': tagger.KEEP,
                    'popup': tagger.POPUPS_WITH_EXISTING,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        preset = self.commander_arg_value(0)
        withExisting = self.commander_arg_value(1)

        if preset == tagger.RANDOM:
            preset = None

        if not withExisting:
            withExisting = tagger.KEEP

        items = tagger.items.get_selected_and_maskable()

        for item in items:

            existing_masks = tagger.shadertree.get_masks(item)

            if existing_masks and withExisting == 'use':
                return

            elif existing_masks and withExisting == 'remove':
                tagger.shadertree.seek_and_destroy(item)

            elif existing_masks and withExisting == 'consolidate':
                tagger.shadertree.consolidate(item)

            mask = tagger.shadertree.build_material( item, preset = preset )
            tagger.shadertree.move_to_base_shader(mask)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        
lx.bless(CommandClass, NAME_CMD)
