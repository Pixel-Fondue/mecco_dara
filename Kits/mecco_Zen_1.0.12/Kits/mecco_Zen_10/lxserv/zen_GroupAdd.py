# python

import lx, lxifc, lxu.command, modo
from zen import CommanderClass

CMD_NAME = 'zen.groupAdd_Popup'
NEW = ('new', '(new group)')

class CommandClass(CommanderClass):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': 'group',
                    'label': 'Add to Group',
                    'datatype': 'string',
                    'default': '',
                    'values_list_type': 'popup',
                    'values_list': self.list_groups,
                    'flags': ['query'],
                }
            ]

    def commander_execute(self, msg, flags):
        if not self.commander_arg_value(0):
            return

        group_id = self.commander_arg_value(0)

        if group_id == NEW[0]:
            lx.eval('?group.create {} mode:selItems')
            return

        else:
            group = modo.Scene().item(group_id)
            itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
            for item in [i for i in modo.Scene().selected if i.superType != None]:
                itemGraph.AddLink(group,item)

            modo.dialogs.alert("Added Items to Group", "Added %s selected items to '%s'." % (len(modo.Scene().selected), group.name))

    def list_groups(self):

        groups_list = [NEW]
        groups_list += sorted([(i.id, i.name) for i in modo.Scene().items('group')], key=lambda x: x[1])
        return groups_list


lx.bless(CommandClass, CMD_NAME)
