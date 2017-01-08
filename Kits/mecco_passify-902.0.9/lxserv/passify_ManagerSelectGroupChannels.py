# python

import lx, lxu.command, passify

class commandClass(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        lx.eval('select.drop channel')
        try:
            lx.eval('group.scan mode:sel type:chan grpType:pass')
            lx.eval('tool.set channel.haul on')
        except:
            pass

    def arg_UIValueHints(self, index):
        return Notifiers()

    def basic_Enable(self,msg):
        try:
            group = lx.eval('group.current group:? type:pass')
        except:
            return False

        if group:
            return True

        return False

class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction','')]

lx.bless(commandClass, passify.CMD_MANAGER_HAUL_GROUP_CHANNELS)
