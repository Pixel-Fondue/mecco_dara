# python

import lx, lxu, modo

NAME_CMD = "zen.doubleClick"

def selectedIsMesh():
    try:
        return modo.Scene().selected[-1].type == 'mesh'
    except IndexError:
        return False

def setItemMode():
    lx.eval('select.typeFrom item;vertex;polygon;edge;pivot;center;ptag true')

def get_mode():
    sel_svc = lx.service.Selection()
    selitype = sel_svc.CurrentType (None)
    seltype = sel_svc.LookupName (selitype)
    return seltype


class CMD_Zen_doubleClick(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):

        mode = get_mode()

        if mode in ('item', None, 'link'):
            if selectedIsMesh():
                lx.eval("select.typeFrom polygon;vertex;edge;item;pivot;center;ptag true")
            else:
                lx.eval("select.itemHierarchy")
        elif mode == 'polygon':
            if lx.eval("query layerservice polys ? selected"):
                lx.eval("select.connect")
            else:
                setItemMode()
        elif mode == 'edge':
            if lx.eval("query layerservice edges ? selected"):
                lx.eval("select.loop")
            else:
                setItemMode()
        elif mode == 'vertex':
            if lx.eval("query layerservice verts ? selected"):
                lx.eval("select.connect")
            else:
                setItemMode()



lx.bless(CMD_Zen_doubleClick, NAME_CMD)
