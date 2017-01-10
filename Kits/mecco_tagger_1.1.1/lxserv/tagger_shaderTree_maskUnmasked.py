# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_SHADERTREE_MASK_UNMASKED

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': [],
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

        counter = 0
        for pTag in tagger.scene.all_tags_by_type(i_POLYTAG):
            if not tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG }):
                new_mask = tagger.shadertree.build_material(i_POLYTAG = i_POLYTAG, pTag = pTag)
                counter += 1

        modo.dialogs.alert(
            tagger.DIALOGS_MASKED_TAGS_COUNT[0],
            tagger.DIALOGS_MASKED_TAGS_COUNT[1] % counter
        )

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CommandClass, CMD_NAME)
