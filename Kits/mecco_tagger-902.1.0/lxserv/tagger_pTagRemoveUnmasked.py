# python

import lx, lxu.command, lxifc, traceback, modo, tagger

CMD_NAME = tagger.CMD_PTAG_REMOVE_UNMASKED

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

        hitcount = 0
        tagCounter = 0
        for pTag in tagger.scene.all_tags_by_type(i_POLYTAG):
            if not tagger.shadertree.get_masks( pTags = { pTag: i_POLYTAG }):
                hitcount += tagger.scene.replace_tag(tagType, pTag, "")
                tagCounter += 1

        try:
            modo.dialogs.alert(
                tagger.DIALOGS_UNTAGGED_POLYS_COUNT[0],
                tagger.DIALOGS_UNTAGGED_POLYS_COUNT[1] % (tagCounter, hitcount)
            )
        except:
            pass

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
