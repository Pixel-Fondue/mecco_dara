# python

import lx, modo
import util

def create_master_pass_group(groups,delimeter="_x_"):
    """
    By Adam O'Hern for Mechanical Color

    Creates a pass group by multiplying any number of existing pass groups by each other.
    For example, you may have one pass group containing color variations, and another containing
    camera angles. This function could combine them such that the resulting pass group contains
    every camera angle for every color variation.
    """

    scene = modo.Scene()

    channels = set()
    for group in groups:

        for channel in group.groupChannels:
            channels.add(channel)

        groupItems = [i for i in group.itemGraph('itemGroups').forward() if i.type != 'actionclip']
        for item in groupItems:
            for channel in item.channels():
                channels.add(channel)

            transformItems = [i for i in item.itemGraph('xfrmCore').reverse() if i.type in ('scale', 'rotation', 'translation')]
            for transformItem in transformItems:
                for channel in transformItem.channels():
                    channels.add(channel)

        for action in [i for i in groups[0].itemGraph('itemGroups').forward() if i.type == lx.symbol.a_ACTIONCLIP]:
            action.actionClip.SetActive(0)

    master_group = scene.addGroup(delimeter.join([g.name for g in groups]),'render')

    for channel in channels:
        master_group.addChannel(channel)

    combine(master_group,groups,channels,len(groups))

    return master_group


def combine(master_group, groups, channels, max_depth, depth=0, passname_parts=[], delimeter="_"):
    """
    By Adam O'Hern for Mechanical Color

    Recursively walks a list of render pass groups to create every possible combination, excluding disabled passes.
    Intended for use with create_master_pass_group() function.
    """
    if not isinstance(groups,list) and not isinstance(groups,set):
        groups = [groups]

    if depth < max_depth:
        passes = [i for i in groups[0].itemGraph('itemGroups').forward() if i.type == lx.symbol.a_ACTIONCLIP]

        for p in passes:
            if p.actionClip.Enabled():
                p.actionClip.SetActive(1)

                subgroups = [g for g in groups]
                del subgroups[0]

                combine(master_group,subgroups,channels,max_depth,depth+1,passname_parts+[p.name])

                p.actionClip.SetActive(0)

    elif depth == max_depth:
        layer_name = delimeter.join(passname_parts)
        lx.eval('group.layer group:{%s} name:{%s} transfer:false grpType:pass' % (master_group.name,layer_name))
        for c in channels:
            try:
                #Set channel to its current value; sets channel to 'edit' layer for absorption into the new pass.
                c.set(c.get())
            except:
                util.debug('Something went wrong setting channel "%s".' % (c.name))

        safe_edit_apply()
