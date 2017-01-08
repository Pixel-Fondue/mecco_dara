# python

import lx, modo, lxu.command, traceback, passify

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('state', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('query', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        state = self.dyna_Int(0) if self.dyna_IsSet(0) else None

        if state == None:
            state = 0 if lx.eval('layer.autoAdd state:?') == 'on' else 1

        if state == 0:

            lx.eval('layer.autoAdd state:off')
            preset = lx.eval('scheme.loadPreset ?')
            lx.eval('scheme.loadPreset %s' % preset)

        if state == 1:

            active_group = lx.eval('group.current group:? type:pass')

            if not active_group:
                modo.dialogs.alert('error',passify.message('no_active_pass'))
                return lx.symbol.e_FAILED

            color = lx.eval('user.value mecco_passify_autoAddColor ?')
            lx.eval('layer.autoAdd state:on')
            lx.eval('pref.value color.backdrop {%s}' % color)
            lx.eval('pref.value color.deformers {%s}' % color)

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 1:
            if lx.eval('layer.autoAdd state:?') == 'on':
                va.AddInt(1)
            else:
                va.AddInt(0)
        return lx.result.OK

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

lx.bless(myGreatCommand, passify.CMD_MANAGER_AUTOADD)
