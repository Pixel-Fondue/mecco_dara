
import lx, lxifc, lxu.command, tagger

CMD_NAME = tagger.CMD_PTAG_QUICK_SELECT_POPUP

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
                    'flags': []
                }, {
                    'name': tagger.TAG,
                    'label': self.tag_label,
                    'datatype': 'string',
                    'value': '',
                    'popup': self.list_tags,
                    'flags': ['query'],
                }
            ]

    def commander_execute(self, msg, flags):
        if not self.commander_arg_value(1):
            return

        tagType = self.commander_arg_value(0, tagger.MATERIAL)
        tag = self.commander_arg_value(1)

        args = tagger.build_arg_string({
            tagger.TAGTYPE: tagType,
            tagger.TAG: tag
        })

        lx.eval(tagger.CMD_SELECT_ALL_BY_DIALOG + args)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def tag_label(self):
        tagType = self.commander_arg_value(0, tagger.MATERIAL)
        label = tagger.convert_to_tagType_label(tagType)

        return "%s %s" % (tagger.LABEL_SELECT_TAG, label)

    def list_tags(self):
        tagType = self.commander_arg_value(0, tagger.MATERIAL)
        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)

        tags = tagger.scene.all_tags_by_type(i_POLYTAG)

        return tags

    def commander_notifiers(self):
        return [('notifier.editAction',''), ("select.event", "item +ldt"), ("tagger.notifier", "")]


lx.bless(CommandClass, CMD_NAME)
