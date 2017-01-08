# python

import lx, modo, lxu.command, traceback, passify

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('group', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        group = self.dyna_String(0) if self.dyna_IsSet(0) else None
        group = passify.fetch_by_tag(group,type_='renderPassGroups').id if group else None

        if not group:
            try:
                group = lx.eval('group.current group:? type:pass')
            except:
                group = None

        arg = " group:{%s}" % group if group else ""

        try:
            lx.eval('render.animationDialog%s' % arg)
        except:
            return lx.symbol.e_ABORT

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def arg_UIValueHints(self, index):
        return Notifiers()

    def basic_Enable(self,msg):
        group = self.dyna_String(0) if self.dyna_IsSet(0) else None
        if group:
            try:
                group = passify.fetch_by_tag(group,type_='renderPassGroups').id
            except:
                return False

        try:
            group = group if group else lx.eval('group.current group:? type:pass')
        except:
            return False

        if group:
            return True

        return False

class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction','')]

lx.bless(myGreatCommand, passify.CMD_RENDER_ANIM)
