# python

import lx, lxifc, lxu.command, modo, passify

def list_passes():
    try:
        group = passify.fetch_by_tag(passify.ULTRALIGHT_PGRP,type_='renderPassGroups')
    except:
        return []

    if group == None:
        return []

    graph_kids = group.itemGraph('itemGroups').forward()
    passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

    passes_list = []
    for p in passes:
        passes_list.append(passify.CMD_ULTRALIGHT_ACTIVATE + " {%s}" % p.id)

    passes_list.append(passify.CMD_ULTRALIGHT_ACTIVATE + " {%s}" % passify.NONE)

    return passes_list


class passify_fcl(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class cmd_passify_fcl(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.not_svc = lx.service.NotifySys()
        self.notifier = None

    def cmd_NotifyAddClient (self, argument, object):
        if self.notifier is None:
            self.notifier = self.not_svc.Spawn ("passify.notifier", '')
            self.notifier.AddClient (object)

    def cmd_NotifyRemoveClient (self, object):
        if self.notifier is not None:
            self.notifier.RemoveClient (object)

    def arg_UIValueHints(self, index):
        if index == 0:
            return passify_fcl(list_passes())
        return Passify_FCL_Notifiers()

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(cmd_passify_fcl, passify.CMD_ULTRALIGHT_FCL)

class Passify_FCL_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('passify.notifier','')]
