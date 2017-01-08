# python

import lx, lxu, modo

NAME_CMD = "zen.dropEverything"

def setItemMode(mode):
    lx.eval('select.typeFrom %s;item;vertex;polygon;edge;pivot;center;ptag true' % mode)

def selMode():
    if lx.eval("select.typeFrom vertex;edge;polygon;item;pivot;center;ptag ?"):
        return 'vertex'

    elif lx.eval("select.typeFrom edge;vertex;polygon;item;pivot;center;ptag ?"):
        return 'edge'

    elif lx.eval("select.typeFrom polygon;vertex;edge;item;pivot;center;ptag ?"):
        return 'polygon'

    elif lx.eval("select.typeFrom ptag;vertex;polygon;item;pivot;center;edge ?"):
        return 'ptag'

    elif lx.eval("select.typeFrom item;vertex;polygon;edge;pivot;center;ptag ?"):
        return 'item'

    elif lx.eval("select.typeFrom pivot;vertex;polygon;item;edge;center;ptag ?"):
        return 'pivot'

    elif lx.eval("select.typeFrom center;vertex;polygon;item;pivot;edge;ptag ?"):
        return 'center'


class CMD_Zen(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):
        mode = selMode()

        lx.eval('select.drop item')
        lx.eval('select.drop channel')
        lx.eval('select.drop polygon')
        lx.eval('select.drop edge')
        lx.eval('select.drop vertex')
        lx.eval('tool.clearTask falloff')
        lx.eval('tool.clearTask axis')
        lx.eval('tool.clearTask snap')
        lx.eval('tool.drop')

        print mode
        setItemMode(mode)

lx.bless(CMD_Zen, NAME_CMD)
