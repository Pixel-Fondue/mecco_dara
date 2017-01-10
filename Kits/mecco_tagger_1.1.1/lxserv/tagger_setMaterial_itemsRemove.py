#python

import lx, lxu, modo, tagger, traceback

NAME_CMD = tagger.CMD_SET_ITEM_REMOVE

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        items = tagger.items.get_selected_and_maskable()
        tagger.shadertree.seek_and_destroy(items)

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        
lx.bless(CommandClass, NAME_CMD)
