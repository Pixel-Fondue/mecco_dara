#python

import lx
import lxifc
import lxu.command
import modo

CMD_NAME_FCL = "cropper.listPasses"
CMD_NAME_ACTIVATE = "cropper.activatePass"

GROUP_NAME = 'mecco_regions'
NONE = "none"

def list_passes():
        try:
            modo.Scene().item(GROUP_NAME)
        except:
            return []

        graph_kids = modo.Scene().item(GROUP_NAME).itemGraph('itemGroups').forward()
        passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

        passes_list = []
        for pass_ in passes:
            passes_list.append(CMD_NAME_ACTIVATE + " {%s}" % pass_.id)

        passes_list.append(CMD_NAME_ACTIVATE + " {%s}" % NONE)
        passes_list.append('- ')
        passes_list.append("cropper.clearAll")

        return passes_list


class cropper_fcl(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class cmd_cropper_fcl(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('cmds', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

        self.not_svc = lx.service.NotifySys()
        self.notifier = None

    def cmd_NotifyAddClient (self, argument, object):
        if self.notifier is None:
            self.notifier = self.not_svc.Spawn ("cropper.notifier", '')
            self.notifier.AddClient (object)

    def cmd_NotifyRemoveClient (self, object):
        if self.notifier is not None:
            self.notifier.RemoveClient (object)
            
    def arg_UIValueHints(self, index):
        if index == 0:
            return cropper_fcl(list_passes())
        return Cropper_FCL_Notifiers()

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass


class cmd_cropper_activate(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('id', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        id_ = self.dyna_String(0) if self.dyna_IsSet(0) else None

        if id_ == NONE:
            return "(none)"

        if id_ != NONE:
            try:
                return modo.Scene().item(id_).name
            except:
                return "error: invalid crop id"

    def cmd_Execute(self,flags):
        id_ = self.dyna_String(0) if self.dyna_IsSet(0) else None

        if id_ == NONE:
            graph_kids = modo.Scene().item(GROUP_NAME).itemGraph('itemGroups').forward()
            passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

            for pass_ in passes:
                pass_.actionClip.SetActive(0)

        if id_ != NONE:
            try:
                lx.eval("view3d.projection cam")
                lx.eval("view3d.renderCamera")
                modo.Scene().item(id_).actionClip.SetActive(1)
            except NameError:
                return lx.symbol.e_FAILED

class Cropper_FCL_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('cropper.notifier','')]

lx.bless(cmd_cropper_fcl, CMD_NAME_FCL)
lx.bless(cmd_cropper_activate, CMD_NAME_ACTIVATE)
