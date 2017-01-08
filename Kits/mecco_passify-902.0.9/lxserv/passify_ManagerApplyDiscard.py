# python

import lx, lxu.command, modo, passify, traceback


class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def CMD_EXE(self, msg, flags):
        mode = self.dyna_String(0)

        if mode == passify.APPLY:
            passify.safe_edit_apply()
            try:
                lx.eval('!passify.ManagerAutoAdd 0')
            except:
                pass

        if mode == passify.DISCARD:
            passify.safe_edit_discard()
            try:
                lx.eval('!passify.ManagerAutoAdd 0')
            except:
                pass

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        try:
            return passify.is_enabled('edit.apply')
        except Exception:
            lx.out(traceback.format_exc())

    def arg_UIValueHints(self, index):
        return Channel_Notifiers()

lx.bless(commandClass, passify.CMD_MANAGER_APPLY_DISCARD)


class Channel_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.editAction','')]
