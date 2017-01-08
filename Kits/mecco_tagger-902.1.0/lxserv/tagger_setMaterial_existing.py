# python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_EXISTING

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        connected = self.commander_arg_value(0, tagger.SCOPE_SELECTED)

        masks = set()

        for i in modo.Scene().selected:
            if i.type == 'mask':
                masks.add(i)

        if len(masks) < 1:
            modo.dialogs.alert(tagger.DIALOGS_NO_MASK_SELECTED[0], tagger.DIALOGS_NO_MASK_SELECTED[1])
            return

        if len(masks) > 1:
            modo.dialogs.alert(tagger.DIALOGS_TOO_MANY_MASKS[0], tagger.DIALOGS_TOO_MANY_MASKS[1])
            return

        mask = list(masks)[0]

        if not mask.channel(lx.symbol.sICHAN_MASK_PTAG).get():
            modo.dialogs.alert(tagger.DIALOGS_NO_PTAG_FILTER)
            return

        if mask.channel(lx.symbol.sICHAN_MASK_PTAG).get() == "(none)":
            modo.dialogs.alert(tagger.DIALOGS_NONE_PTAG_FILTER)
            return

        tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
        tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

        args = tagger.build_arg_string({
            tagger.TAGTYPE: tagger.convert_to_tagType_string(tagLabel),
            tagger.TAG: tag,
            tagger.SCOPE: connected
        })
        lx.eval("!" + tagger.CMD_PTAG_SET + args)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CommandClass, NAME_CMD)
