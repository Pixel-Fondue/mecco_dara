#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.cleanupItemsList'

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('del_empty_meshes', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('del_empty_groups', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('del_unused_tlocs', lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("Delete empty mesh items")
        if index == 1:
            hints.Label("Delete empty group locators")
        if index == 2:
            hints.Label("Delete unused texture locators")

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.attr_SetInt(2, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            del_empty_meshes = self.dyna_String(0) if self.dyna_IsSet(0) else True
            del_empty_groups = self.dyna_String(1) if self.dyna_IsSet(1) else True
            del_unused_tlocs = self.dyna_String(2) if self.dyna_IsSet(2) else True

            hitlist = set()

            if del_empty_meshes:
                for i in modo.Scene().locators:
                	if i.type == 'mesh' and not i.geometry.numPolygons:
                		hitlist.add(i)

            if del_empty_groups:
                for i in modo.Scene().locators:
                	if i.type == 'groupLocator' and not i.children():
                		hitlist.add(i)

            if del_unused_tlocs:
                for i in modo.Scene().locators:
                    if i.type == 'txtrLocator' and len(i.itemGraph('shadeLoc').reverse()) == 0:
                        hitlist.add(i)

            for hit in hitlist:
                # TD SDK removeItems() method crashes on some groups. This is more robust.
                lx.eval("item.delete item:{%s}" % hit.id)


        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
