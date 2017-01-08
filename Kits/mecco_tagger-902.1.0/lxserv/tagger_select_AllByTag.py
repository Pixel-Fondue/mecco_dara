# python

import lx, lxu, lxifc, modo, tagger, traceback

def _args_tagType():
    return {
        'name': tagger.TAGTYPE,
        'label': tagger.LABEL_TAGTYPE,
        'datatype': 'string',
        'value': tagger.MATERIAL,
        'popup': tagger.POPUPS_TAGTYPES,
        'flags': [],
    }

def _args_tag():
    return {
            'name': tagger.TAG,
            'label': tagger.LABEL_TAG,
            'datatype': 'string',
            'value': '',
            'sPresetText': tagger.scene.all_tags,
            'flags': ['optional'],
        }

def select_all_by_tag(tagType, tag):
    i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

    tags = []

    if tag:
        tags = tag.split(";")

    elif not tag:
        tagStrings = tagger.selection.get_ptags(i_POLYTAG)
        for tagString in tagStrings:
            tags.extend(tagString.split(";"))

    for tag in tags:
        if tagType in ['material', 'part']:
            lx.eval("select.polygon add %s face {%s}" % (tagType, tag))
        elif tagType == 'pick':
            lx.eval("select.useSet {%s} select" % tag)


class SelAllByDialogCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [ _args_tagType(), _args_tag() ]

    def commander_execute(self, msg, flags):
        select_all_by_tag(self.commander_arg_value(0), self.commander_arg_value(1))


class SelAllByMatCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [ _args_tag() ]

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            return "%s %s: %s" % (tagger.LABEL_SELECT_ALL, tagger.LABEL_MATERIAL, self.commander_arg_value(0))

    def commander_execute(self, msg, flags):
        select_all_by_tag('material', self.commander_arg_value(0))


class SelAllByPartCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [ _args_tag() ]

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            return "%s %s: %s" % (tagger.LABEL_SELECT_ALL, tagger.LABEL_PART, self.commander_arg_value(0))

    def commander_execute(self, msg, flags):
        select_all_by_tag('part', self.commander_arg_value(0))


class SelAllBySetCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [ _args_tag() ]

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            return "%s %s: %s" % (tagger.LABEL_SELECT_ALL, tagger.LABEL_PICK, self.commander_arg_value(0))

    def commander_execute(self, msg, flags):
        select_all_by_tag('pick', self.commander_arg_value(0))


lx.bless(SelAllByDialogCommandClass, tagger.CMD_SELECT_ALL_BY_DIALOG)
lx.bless(SelAllByMatCommandClass, tagger.CMD_SELECT_ALL_BY_MATERIAL)
lx.bless(SelAllByPartCommandClass, tagger.CMD_SELECT_ALL_BY_PART)
lx.bless(SelAllBySetCommandClass, tagger.CMD_SELECT_ALL_BY_SET)
