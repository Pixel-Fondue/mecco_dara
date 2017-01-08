# python

import lx, modo

from add_items import *
from util import *
from var import *

def build(full_scene, include_environments, include_lumigons, headroom):
    group = fetch_by_tag(ULTRALIGHT_PGRP,type_='renderPassGroups')

    if not group:
        add_items({
            ULTRALIGHT_PGRP:{
                TAGS:[ULTRALIGHT, ULTRALIGHT_PGRP],
                NAME:message(ULTRALIGHT_PGRP),
                TYPE:"group",
                GTYP:"render"
            }
        })

    group = fetch_by_tag(ULTRALIGHT_PGRP,type_='renderPassGroups')

    for pass_ in [p for p in group.itemGraph('itemGroups').forward() if p.type == 'actionclip']:
        modo.Scene().removeItems(pass_)

    if full_scene:
        scope = modo.Scene().items()

    elif len(modo.Scene().selected) > 0:
        scope = modo.Scene().selected

    else:
        scope = modo.Scene().items()

    items = set()
    for item in scope:
        if item.type == 'renderOutput':
            continue
        if not include_environments and item.type == 'environment':
            continue
        if not include_lumigons and not item.isLocatorSuperType():
            continue

        light_channels = [l for l in item.channels() if l.storageType == 'light']
        if not light_channels:
            continue

        if light_channels[0].get() > 0 and not light_channels[0].revLinked:
            items.add(item)

    for item in items:
        # debug(item.name,True)
        channel = [l for l in item.channels() if l.storageType == 'light'][0]
        if channel not in group.groupChannels:
            group.addChannel(channel)

        actionclip = modo.Scene().addItem('actionclip')
        actionclip.name = " ".join((item.name, message("Pass")))
        actionclip.setTag(TAG, buildTag((ULTRALIGHT_PASS,item.id)))

        itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup('itemGroups'))
        itemGraph.AddLink(group,actionclip)

    for item in [i._item for i in group.groupChannels]:
        channel = [l for l in item.channels() if l.storageType == 'light'][0]
        for pass_ in [p for p in group.itemGraph('itemGroups').forward() if p.type == 'actionclip']:
            channel.set(0.0, action=pass_.name)

        value = channel.get()
        value =  value + (value * headroom)
        channel.set(value, action=fetch_by_tag(item.id).name)

    safe_edit_apply()

    return group

def destroy():
    hitlist = fetch_by_tag(ULTRALIGHT, True)

    if not hitlist:
        return

    modo.Scene().removeItems(hitlist[0])
    if len(hitlist) > 1:
        destroy()
