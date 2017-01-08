# python

import lx, modo, lxu.command, traceback, passify

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        lx.eval('group.edit add chan pass')

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
        group = None

        try:
            group = lx.eval('group.current group:? type:pass')
        except:
            return False

        if group:
            return True

        return False


class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [("select.event", "item +l"),("select.event", "channel +l")]

lx.bless(myGreatCommand, passify.CMD_MANAGER_CHANNELSADD)
