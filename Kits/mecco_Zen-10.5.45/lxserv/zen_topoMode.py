# python

import lx, modo, lxu.command, traceback, lxifc

CMD_NAME = 'zen.topoMode'

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
            state = 0 if lx.eval('view3d.topology ?') else 1

        if state == 0:

            lx.eval('tool.set const.bg off')
            lx.eval('view3d.topology 0')

        if state == 1:

            lx.eval('tool.set const.bg on')
            lx.eval('tool.attr const.bg geometry point')
            lx.eval('view3d.topology 1')

        notifier = Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DISABLE)


    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 1:
            try:
                if lx.eval('view3d.topology ?'):
                    va.AddInt(1)
                else:
                    va.AddInt(0)
            except:
                va.AddInt(0)
        return lx.result.OK

    def arg_UIValueHints(self, index):
        return cmd_Notifiers()

    def basic_Enable(self,msg):
        return True

class cmd_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('zen.topoNotifier',''),]

class Notifier(lxifc.Notifier):
    masterList = {}

    def noti_Name(self):
        return "zen.topoNotifier"

    def noti_AddClient(self,event):
        self.masterList[event.__peekobj__()] = event

    def noti_RemoveClient(self,event):
        del self.masterList[event.__peekobj__()]

    def Notify(self, flags):
        for event in self.masterList:
            evt = lx.object.CommandEvent(self.masterList[event])
            evt.Event(flags)

lx.bless(Notifier, "zen.topoNotifier")
lx.bless(myGreatCommand, CMD_NAME)
