# python

import lx, lxifc, lxu, modo
import tagger
from os.path import basename, splitext

CMD_NAME = tagger.CMD_SET_AUTO_QUICK

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
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):
        preset = self.commander_arg_value(0, tagger.RANDOM)
        selmode = tagger.selection.get_mode()

        if selmode == 'item':
            lx.eval("%s {%s}" % (tagger.CMD_SET_ITEM, preset))

        elif selmode in ['vertex', 'edge', 'polygon']:
            if preset.endswith(".lxp"):
                pTag = splitext(basename(preset))[0]

            elif not preset.endswith(".lxp"):
                pTag = tagger.DEFAULT_MATERIAL_NAME

            if tagger.shadertree.get_masks(pTags = {pTag: lx.symbol.i_POLYTAG_MATERIAL}):
                inc = 0
                while tagger.shadertree.get_masks(pTags = {pTag + str(inc): lx.symbol.i_POLYTAG_MATERIAL}):
                    inc += 1
                pTag = pTag + str(inc)

            lx.eval("?%s %s {%s}" % (tagger.CMD_SET_PTAG, pTag, preset))

lx.bless(CommandClass, CMD_NAME)
