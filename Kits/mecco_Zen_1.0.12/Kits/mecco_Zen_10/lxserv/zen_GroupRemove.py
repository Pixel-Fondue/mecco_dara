# python

import lx, lxifc, lxu.command, modo
from zen import CommanderClass

CMD_NAME = 'zen.groupRemove_Popup'
ALL = ('all', '(remove from all)')

class CommandClass(CommanderClass):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': 'group',
                    'label': 'Remove from Group',
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

        links_count = 0
        if group_id == ALL[0]:
            for item in modo.Scene().selected:
                itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
                rev_count = itemGraph.RevCount(item)
                links = set()
                for n in range(rev_count):
                    links.add(itemGraph.RevByIndex(item, n))
                for link in links:
                    itemGraph.DeleteLink(link, item)
                    links_count += 1

            modo.dialogs.alert("Removed from Groups", "Removed %s group relationships." % links_count)

        else:
            group = modo.Scene().item(group_id)
            itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
            for item in modo.Scene().selected:
                itemGraph.DeleteLink(group,item)

            modo.dialogs.alert("Removed from Group", "Removed '%s' items from '%s'." % (len(modo.Scene().selected), group.name))

    def list_groups(self):

        groups_set = set([ALL])

        for item in modo.Scene().selected:
            itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
            rev_count = itemGraph.RevCount(item)
            for n in range(rev_count):
                groups_set.add((itemGraph.RevByIndex(item, n).Ident(), itemGraph.RevByIndex(item, n).Name()))

        return sorted(list(groups_set), key=lambda x: x[1])


lx.bless(CommandClass, CMD_NAME)
