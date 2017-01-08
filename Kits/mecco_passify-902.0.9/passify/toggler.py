# python

import lx, modo

from add_items import *
from util import *
from var import *

def build():
    passify_items = {
        TOGGLER_PGRP:{
            TAGS:[TOGGLER, TOGGLER_PGRP],
            NAME:message(TOGGLER_PGRP),
            TYPE:"group",
            GTYP:"render"
        }
    }

    return add_items(passify_items)

def destroy():
    hitlist = fetch_by_tag(TOGGLER, True)
    if not hitlist:
        return
    modo.Scene().removeItems(hitlist[0])
    if len(hitlist) > 1:
        destroy()

def add_selected():
    group = fetch_by_tag(TOGGLER_PGRP,type_='renderPassGroups')
    items = get_selected_and_maskable()

    for item in items:
        channel = item.channel('render')
        if channel not in group.groupChannels:
            group.addChannel(channel)

        channel = item.channel('visible')
        if channel not in group.groupChannels:
            group.addChannel(channel)

        actionclip = modo.Scene().addItem('actionclip')
        actionclip.name = " ".join((item.name, message("Pass")))
        actionclip.setTag(TAG, buildTag((TOGGLER_PASS,item.id)))

        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.AddLink(group,actionclip)

    for item in [i._item for i in group.groupChannels]:
        for pass_ in [p for p in group.itemGraph('itemGroups').forward() if p.type == 'actionclip']:
            item.channel('render').set(2, action=pass_.name)
            item.channel('visible').set(3, action=pass_.name)

        item.channel('render').set(1, action=fetch_by_tag(item.id).name)
        item.channel('visible').set(1, action=fetch_by_tag(item.id).name)

    safe_edit_apply()

def remove_selected():
    group = fetch_by_tag(TOGGLER_PGRP,type_='renderPassGroups')

    for item in get_selected_and_maskable():
        channel = item.channel('render')
        if channel not in group.groupChannels:
            group.removeChannel('render', item)

        actionclip = fetch_by_tag(item.id)
        if actionclip != None:
            modo.Scene().removeItems(actionclip)
