# python

import modo
from util import *
from var import *

def add_items(items_dict):

    # debug("add_items", True)

    for i in fetch_tagged():
        if i.getTags()[TAG] in items_dict:
            items_dict[i.getTags()[TAG]]["item"] = i

    # debug("fetched tagged items", True)

    for k, v in {k:v for k, v in items_dict.iteritems() if "item" not in v}.iteritems():
        items_dict[k]["item"] = modo.Scene().addItem(v[TYPE])
        items_dict[k]["item"].name = v[NAME]

        tag = buildTag(v[TAGS]) if TAGS in v else TAG_DEFAULT
        items_dict[k]["item"].setTag(TAG, tag)

        if GTYP in v:
            items_dict[k]["item"].setTag('GTYP',v[GTYP])

        if CHANNELS in v:
            for channel, value in v[CHANNELS].iteritems():
                items_dict[k]["item"].channel(channel).set(value)

    # debug("created all items", True)

    for k, v in {k:v for k, v in items_dict.iteritems() if PARENT in v}.iteritems():
        items_dict[k]["item"].setParent(fetch_by_tag(v[PARENT]))

    for k, v in {k:v for k, v in items_dict.iteritems() if REORDER in v}.iteritems():
        reorder(items_dict[k]["item"],v[REORDER])

    # debug("parented items", True)

    for k, v in {k:v for k, v in items_dict.iteritems() if ITEMGRAPHS in v}.iteritems():

        # debug("adding item graph links for " + k, True)
        links = v[ITEMGRAPHS] if hasattr(v[ITEMGRAPHS], '__iter__') else [v[ITEMGRAPHS]]

        for i in links:
            # debug("linking %s to %s via %s" % (items_dict[k]["item"].id, fetch_by_tag(i[1]).id, i[0]), True)
            itemGraph = lx.object.ItemGraph(modo.Scene().GraphLookup(i[0]))
            itemGraph.AddLink(items_dict[k]["item"],fetch_by_tag(i[1]))

    # debug("item graphs added", True)

    for k, v in {k:v for k, v in items_dict.iteritems() if GROUPCHANNELS in v}.iteritems():
        for channel_tuple in v[GROUPCHANNELS]:
            channel = fetch_by_tag(channel_tuple[0]).channel(channel_tuple[1])
            if channel not in items_dict[k]["item"].groupChannels:
                items_dict[k]["item"].addChannel(channel)

    # debug("group channels added", True)

    for k, v in {k:v for k, v in items_dict.iteritems() if CHANNELWRITE in v}.iteritems():
        for channel_tuple in v[CHANNELWRITE]:
            fetch_by_tag(channel_tuple[0]).channel(channel_tuple[1]).set(channel_tuple[2], action=v["item"].name)

    safe_edit_apply()
    # debug("channels written to passes", True)

    # debug("end add_items", True)
    return items_dict
