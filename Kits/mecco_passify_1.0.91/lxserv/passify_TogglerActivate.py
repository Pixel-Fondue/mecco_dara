# python

import lx, lxifc, lxu.command, modo, passify

class cmd_passify_activate(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('pass_id', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        item_id = self.dyna_String(0) if self.dyna_IsSet(0) else None
        item_id = item_id if item_id != passify.NONE else None

        if item_id == None:
            return "(%s)" % passify.message("none")

        if item_id != None:
            try:
                return modo.Scene().item(item_id).name
            except:
                return "%s: %s" % (passify.message("error"), passify.message("invalid_pass_id"))

    def cmd_Execute(self,flags):
        item_id = self.dyna_String(0) if self.dyna_IsSet(0) else None

        if item_id == passify.NONE:
            graph_kids = passify.fetch_by_tag(passify.TOGGLER_PGRP,type_='renderPassGroups').itemGraph('itemGroups').forward()
            passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

            for p in passes:
                p.actionClip.SetActive(0)

        if item_id != passify.NONE:
            try:
                passify.safe_edit_apply()
                modo.Scene().item(item_id).actionClip.SetActive(1)
            except NameError:
                return lx.symbol.e_FAILED

lx.bless(cmd_passify_activate, passify.CMD_TOGGLER_ACTIVATE)
