import lx, modo
import lxu.command
import traceback

CMD_NAME = "cropper.regionToggle"

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        #command accepts an argument
        self.dyna_Add('query', lx.symbol.sTYPE_BOOLEAN) #or sTYPE_FLOAT
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags (self):
        #make the command undoable
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        r = modo.Scene().renderItem.channel('region').get()
        modo.Scene().renderItem.channel('region').set(1 if r == 0 else 0)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
            if modo.Scene().renderItem.channel('region').get():
                va.AddInt(1)
            else:
                va.AddInt(0)
        return lx.result.OK

    def arg_UIValueHints(self, index):
        return Cropper_Channel_Notifiers()

    def basic_Enable(self,msg):
        return True


class Cropper_Channel_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('channel.event','+v region')]

lx.bless(myGreatCommand, CMD_NAME)
