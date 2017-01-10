# python

import lx, lxu.command, modo, passify


class commandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        mode = self.dyna_String(0)

        if mode == passify.GROUP:
            the_group = lx.eval('group.current group:? type:pass')
            if the_group:
                modo.Scene().removeItems(the_group)

        if mode == passify.PASS:
            the_pass = lx.eval('layer.active layer:? type:pass')
            if the_pass:
                modo.Scene().removeItems(the_pass)

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def arg_UIValueHints(self, index):
        return Notifiers()

    def basic_Enable(self,msg):
        if self.dyna_String(0) == passify.GROUP:
            try:
                lx.eval('group.current group:? type:pass')
                return True
            except:
                return False
        elif self.dyna_String(0) == passify.PASS:
            try:
                lx.eval('layer.active layer:? type:pass')
                return True
            except:
                return False

        return False

class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction','')]

lx.bless(commandClass, passify.CMD_MANAGER_DELETE)
