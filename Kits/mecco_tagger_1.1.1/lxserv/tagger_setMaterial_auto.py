#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_MATERIAL


class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        selmode = tagger.selection.get_mode()

        if selmode == 'item':
            lx.eval("?%s" % tagger.CMD_SET_ITEM)

        elif selmode in ['vertex', 'edge', 'polygon']:
            lx.eval("?%s" % tagger.CMD_SET_PTAG)


lx.bless(CommandClass, NAME_CMD)
