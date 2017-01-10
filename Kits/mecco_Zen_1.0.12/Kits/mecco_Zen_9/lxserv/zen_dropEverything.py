# python

import lx, lxu, modo

NAME_CMD = "zen.dropEverything"

class CMD_Zen(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):
        lx.eval('select.drop item')
        lx.eval('select.drop channel')
        lx.eval('select.drop polygon')
        lx.eval('select.drop edge')
        lx.eval('select.drop vertex')
        lx.eval('tool.clearTask falloff')
        lx.eval('tool.clearTask axis')
        lx.eval('tool.clearTask snap')
        lx.eval('tool.drop')

lx.bless(CMD_Zen, NAME_CMD)
