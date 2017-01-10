# python

import lx, lxu.command, traceback, passify, lxifc

class cmd_setup_class(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('full_scene', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('include_environments', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('include_lumigons', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('headroom', lx.symbol.sTYPE_PERCENT)

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label(passify.message("full_scene"))
        if index == 1:
            hints.Label(passify.message("include_environments"))
        if index == 2:
            hints.Label(passify.message("include_lumigons"))
        if index == 3:
            hints.Label(passify.message("headroom"))

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.attr_SetInt(2, 1)
            self.attr_SetFlt(3, 0.2)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def cmd_Flags (self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def CMD_EXE(self, msg, flags):
        full_scene = self.dyna_Bool(0) if self.dyna_IsSet(0) else True
        include_environments = self.dyna_Bool(1) if self.dyna_IsSet(1) else True
        include_lumigons = self.dyna_Bool(2) if self.dyna_IsSet(2) else True
        headroom = self.dyna_Float(3) if self.dyna_IsSet(3) else 0.0

        passify.ultralight.build(full_scene, include_environments, include_lumigons, headroom)

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def basic_Enable(self,msg):
        return True

lx.bless(cmd_setup_class, passify.CMD_ULTRALIGHT_SETUP)
