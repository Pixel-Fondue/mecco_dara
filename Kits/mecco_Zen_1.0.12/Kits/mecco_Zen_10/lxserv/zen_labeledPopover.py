# python

import lx, lxifc, lxu.command

class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('hash', lx.symbol.sTYPE_STRING)
        self.dyna_Add('label', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        return self.dyna_String(1)

    def cmd_Execute(self,flags):
        lx.eval("attr.formPopover {%s}" % self.dyna_String(0))

lx.bless(CommandClass, "zen.labeledPopover")

class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('hash', lx.symbol.sTYPE_STRING)
        self.dyna_Add('label', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        return 'Map "%s" to key...' % self.dyna_String(1)

    def cmd_Execute(self,flags):
        lx.eval('cmds.mapKey {} "attr.formPopover {%s}" .global (stateless) .anywhere' % self.dyna_String(0))

lx.bless(CommandClass, "zen.labeledMapKey")
