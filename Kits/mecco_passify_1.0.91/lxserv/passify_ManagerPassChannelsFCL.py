# python

import lx, lxifc, lxu.command, modo, passify

def list_passes():
    try:
        group = lx.eval('group.current group:? type:pass')
        group = modo.Scene().item(group)
    except:
        return []

    item_ids = set()
    for c in group.groupChannels:
        item = c.item
        if item.type in ('translation', 'rotation', 'scale'):
            item = c.item.itemGraph('xfrmCore').forward()[0]
        item_ids.add(item.id)

    channels_dict = {}
    for item_id in item_ids:
        channels_dict[item_id] = set()

    if len(group.groupChannels) == 0:
        return []

    for c in group.groupChannels:
        item = c.item
        if item.type in ('translation', 'rotation', 'scale'):
            item = c.item.itemGraph('xfrmCore').forward()[0]

        if any(x in c.name for x in ['.R', '.G', '.B']):
            colorGroup = [i for i in group.groupChannels if (i.item.id == c.item.id and i.name.split('.')[0] == c.name.split('.')[0])]
            print colorGroup

            if len(colorGroup) == 3:
                channels_dict[item.id].add((c.item.id, c.name.split('.')[0]))
            else:
                channels_dict[item.id].add((c.item.id, c.name))
        else:
            channels_dict[item.id].add((c.item.id, c.name))

    fcl = []
    for item_id, channels_list in channels_dict.iteritems():
        fcl.append('- ' + modo.Scene().item(item_id).name)
        for channel_tuple in sorted(channels_list, key=lambda tup: tup[1]):
            fcl.append('item.channel item:{%s} name:{%s} value:?' % (channel_tuple[0], channel_tuple[1]))

    return fcl


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

lx.bless(cmd_passify_fcl, passify.CMD_MANAGER_PASS_CHANNELS_FCL)

class Passify_FCL_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction',''),("select.event", "item +l")]
