# python

import lx, lxifc, lxu, modo
import tagger
from os.path import basename, splitext

CMD_NAME = tagger.CMD_SET_PTAG

def material_tags_list():
    return tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL)

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAG,
                    'label': tagger.LABEL_TAG,
                    'datatype': 'string',
                    'value': "",
                    'flags': [],
                    'sPresetText': material_tags_list
                }, {
                    'name': tagger.PRESET,
                    'label': tagger.LABEL_PRESET,
                    'datatype': 'string',
                    'value': tagger.RANDOM,
                    'popup': tagger.presets.presets_popup,
                    'flags': ['optional', 'query']
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }, {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': ['optional']
                }, {
                    'name': tagger.WITH_EXISTING,
                    'label': tagger.LABEL_WITH_EXISTING,
                    'datatype': 'string',
                    'value': tagger.USE,
                    'popup': tagger.POPUPS_WITH_EXISTING,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        pTag = self.commander_arg_value(0)
        preset = self.commander_arg_value(1, tagger.RANDOM)
        connected = self.commander_arg_value(2, tagger.SCOPE_FLOOD)
        tagType = self.commander_arg_value(3, tagger.MATERIAL)
        withExisting = self.commander_arg_value(4)

        if preset == tagger.RANDOM:
            preset = None

        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

        if not pTag:
            if not preset:
                pTag = tagger.DEFAULT_MATERIAL_NAME

            elif not preset.endswith(".lxp"):
                pTag = tagger.DEFAULT_MATERIAL_NAME

            elif preset.endswith(".lxp"):
                pTag = splitext(basename(preset))[0]

        # find any existing masks for this pTag
        existing_masks = tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG })

        # tag the polys
        args = tagger.build_arg_string({
            tagger.TAGTYPE: tagType,
            tagger.TAG: pTag,
            tagger.SCOPE: connected
        })
        lx.eval("!" + tagger.CMD_PTAG_SET + args)

        # build a new mask if we need one
        if not existing_masks:
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)
            tagger.shadertree.move_to_base_shader(new_mask)

        elif existing_masks and withExisting == tagger.USE:
            pass

        elif existing_masks and withExisting == tagger.KEEP:
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)
            tagger.shadertree.move_to_base_shader(new_mask)

        elif existing_masks and withExisting == tagger.REMOVE:
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)
            tagger.shadertree.move_to_base_shader(new_mask)
            
            tagger.safe_removeItems(existing_masks, True)

        elif existing_masks and withExisting == tagger.CONSOLIDATE:
            new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag, preset = preset)
            tagger.shadertree.move_to_base_shader(new_mask)

            consolidation_masks = tagger.shadertree.consolidate(pTags = { pTag: i_POLYTAG })
            new_mask.setParent(consolidation_masks[pTag])
            tagger.shadertree.move_to_top(new_mask)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CommandClass, CMD_NAME)
