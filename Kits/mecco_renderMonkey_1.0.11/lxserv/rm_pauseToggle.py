#python

import lx
import lxu.command
import traceback

class pauseToggle(lxu.command.BasicCommand):
    
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.PAUSED = False
        
        self.dyna_Add('isPaused', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)
        
    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def CMD_EXE(self, msg, flags):
        pass

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
        
    def basic_Enable(self,msg):
        return True
    
    def cmd_Query(self, index, vaQuery):
        lx.out(self.dyna_Int(0, 0))
        return lx.result.OK
        
        
lx.bless(pauseToggle, "mecco.renderMonkey.paused")