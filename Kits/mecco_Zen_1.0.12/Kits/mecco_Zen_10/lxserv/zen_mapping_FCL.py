# python

import lx, lxifc, lxu.command

FORMS = [
    {
        "label":"Zen Toolbox",
        "hash":"31757584531:sheet"
    }, {
        "label":"Zen Palettes List",
        "hash":"zen_palettesPopover:sheet"
    }, {
        "label":"Recent Tools",
        "hash":"55281439258:sheet"
    }, {
        "label":"Workplane Pie",
        "hash":"ZenPie_Workplane:sheet"
    }, {
        "label":"Snapping Pie",
        "hash":"ZenPie_Snapping:sheet"
    }, {
        "label":"Falloff Pie",
        "hash":"ZenPie_Falloff:sheet"
    }, {
        "label":"ActionCtr Pie",
        "hash":"ZenPie_ActionCtr:sheet"
    }, {
        "label":"Layout Frames Pie",
        "hash":"ZenPie_Frames:sheet"
    }
]

def list_commands():
    fcl = []
    for n, form in enumerate(sorted(FORMS, key=lambda k: k['label']) ):
        fcl.append("zen.labeledPopover {%s} {%s}" % (form["hash"], form["label"]))
        fcl.append("zen.labeledMapKey {%s} {%s}" % (form["hash"], form["label"]))

        if n < len(FORMS)-1:
            fcl.append('- ')

    return fcl


class CommandListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return CommandListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(CommandClass, "zen.mapping_FCL")
