#python

import lx, lxu, modo, tagger, traceback

_clipboard = {'material': None, 'part': None, 'pick': None}

_scope_popup = {
    'name': tagger.SCOPE,
    'label': tagger.LABEL_SCOPE,
    'datatype': 'string',
    'value': tagger.SCOPE_SELECTED,
    'popup': tagger.POPUPS_SCOPE,
    'flags': ['optional']
}

def paste(tagType=tagger.MATERIAL, connected=tagger.SCOPE_SELECTED):
    global _clipboard

    if not tagType:
        tagType = tagger.MATERIAL

    if not connected:
        connected = tagger.SCOPE_SELECTED

    args = {}
    args[tagger.TAG] = _clipboard[tagType]
    args[tagger.TAGTYPE] = tagType
    args[tagger.SCOPE] = connected

    if not args[tagger.TAG]:
        modo.dialogs.alert(
            tagger.DIALOGS_NOTHING_TO_PASTE[0],
            tagger.DIALOGS_NOTHING_TO_PASTE[1]
            )
        return

    lx.eval("!" + tagger.CMD_PTAG_SET + tagger.build_arg_string(args))

    notifier = tagger.Notifier()
    notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)



class CopyCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        global _clipboard

        polys = tagger.selection.get_polys()

        if polys:
            _clipboard['material'] = polys[-1].tags()['material']
            _clipboard['part'] = polys[-1].tags()['part']
            _clipboard['pick'] = polys[-1].tags()['pick']


class CopyMaskCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        masks = set()

        for i in modo.Scene().selected:
            if i.type == tagger.MASK:
                masks.add(i)

        if len(masks) < 1:
            modo.dialogs.alert(tagger.DIALOGS_NO_MASK_SELECTED)
            return

        if len(masks) > 1:
            modo.dialogs.alert(tagger.DIALOGS_TOO_MANY_MASKS)
            return

        mask = list(masks)[0]

        tagLabel = mask.channel(lx.symbol.sICHAN_MASK_PTYP).get()
        tagType = tagger.convert_to_tagType_string(tagLabel)
        tag = mask.channel(lx.symbol.sICHAN_MASK_PTAG).get()

        global _clipboard
        _clipboard[tagType] = tag


class PasteDialogCommandClass(tagger.Commander):
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
            },
            _scope_popup
        ]

    def commander_execute(self, msg, flags):
        paste(self.commander_arg_value(0), self.commander_arg_value(1))


class PasteMaterialCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [_scope_popup]

    def commander_execute(self, msg, flags):
        paste(tagger.MATERIAL, self.commander_arg_value(0))


class PastePartCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [_scope_popup]

    def commander_execute(self, msg, flags):
        paste(tagger.PART, self.commander_arg_value(0))


class PastePickCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [_scope_popup]

    def commander_execute(self, msg, flags):
        paste(tagger.PICK, self.commander_arg_value(0))


lx.bless(CopyCommandClass, tagger.CMD_PTAG_COPY)
lx.bless(CopyMaskCommandClass, tagger.CMD_PTAG_COPYMASK)
lx.bless(PasteDialogCommandClass, tagger.CMD_PTAG_PASTE_DIALOG)
lx.bless(PasteMaterialCommandClass, tagger.CMD_PTAG_PASTE_MAT)
lx.bless(PastePartCommandClass, tagger.CMD_PTAG_PASTE_PART)
lx.bless(PastePickCommandClass, tagger.CMD_PTAG_PASTE_SET)
