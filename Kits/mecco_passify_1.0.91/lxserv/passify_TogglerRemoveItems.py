# python

import lx, lxu.command, traceback, passify, lxifc

class cmd_remove_from_layer(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        passify.toggler.remove_selected()

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def arg_UIValueHints(self, index):
        return Notifiers()

    def basic_Enable(self,msg):
        try:
            if passify.get_selected_and_maskable() and passify.fetch_by_tag(passify.TOGGLER_PGRP,type_='renderPassGroups'):
                return True
        except:
            return False
        return False


class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [
          ("select.event", "item +l")
        ]

lx.bless(cmd_remove_from_layer, passify.CMD_TOGGLER_REMOVE)
