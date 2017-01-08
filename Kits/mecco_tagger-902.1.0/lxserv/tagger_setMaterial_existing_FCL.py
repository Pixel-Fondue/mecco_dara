# python

import lx, lxifc, lxu.command, modo, tagger

CMD_NAME = tagger.CMD_SET_EXISTING_FCL

def list_commands():
    timer = tagger.DebugTimer()

    fcl = []

    if tagger.selection.get_mode() != 'polygon':
        timer.end()
        return fcl

    tags_list = []

    existing_tags = tagger.items.get_all_masked_tags()
    recent_tags = tagger.scene.get_recent_pTags()

    if recent_tags:
        tags_list = [i for i in recent_tags if i in existing_tags]

    tags_list = tags_list + existing_tags

    if len(tags_list) > tagger.MAX_MASK_FCL:
        tags_list = tags_list[:tagger.MAX_MASK_FCL]

    # removes duplicates while maintainint list order
    tags_list = [ii for n,ii in enumerate(tags_list) if ii not in tags_list[:n]]

    if tags_list:
        for tag in tags_list:
            fcl.append('%s {%s} {%s}' % (tagger.CMD_PTAG_SET, tag[0], tag[1]))
    else:
        fcl.append("%s {%s}" % (tagger.CMD_NOOP, tagger.LABEL_NO_MASKS))

        timer.end()
        return fcl

    timer.end()
    return fcl


class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.QUERY,
                    'label': tagger.LABEL_QUERY,
                    'datatype': 'integer',
                    'value': '',
                    'fcl': list_commands,
                    'flags': ['query'],
                }
            ]

    def commander_notifiers(self):
        return [("select.event", "polygon +ldt"),("select.event", "item +ldt"), ("tagger.notifier", "")]


lx.bless(CommandClass, CMD_NAME)
