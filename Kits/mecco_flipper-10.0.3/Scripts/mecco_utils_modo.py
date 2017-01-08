#python
import sys
import lx
import lxu
from mecco_utils_contexts import catch


# returns current scene as an lxu.object.Scene instance
GetScene = lxu.select.SceneSelection().current


def GetItemsOfType(nameFilter, *itemTypes):
    """ Returns all items in scene of *itemTypes (item type strings or ints),
        matching nameFilter string. Empty string or None will match all items. """
    scene = GetScene()
    items = []
    nameFilter = str() or nameFilter
    for itemType in itemTypes:
        with catch('item type "%s" not found' % itemType, False, LookupError):
            if type(itemType) == str:
                itemType = svc_scene.ItemTypeLookup(itemType)
            if type(svc_scene.ItemTypename(itemType)) is type(None):
                raise LookupError

            num = scene.ItemCount(itemType)
            for n in xrange(num):
                item = scene.ItemByIndex(itemType, n)
                if nameFilter in item.UniqueName():
                    items.append(item)
    return items



def InitXfrms(item):
    """ Initializes zero-transforms for a given item.
        item = lx.object.Item or
               lxu.object.Item instance """
    with catch("InitXfrms %s" % item.UniqueName(), True):
        #get a chanWrite interface
        scene = GetScene()
        chanRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
        chanWrite = lx.object.ChannelWrite(chanRead)

        #get a locator interface for item
        loc = lx.object.Locator(item)

        #scale
        try:
            scl = loc.GetTransformItem(lx.symbol.iXFRM_SCALE)
        except LookupError:
            scl = loc.AddTransformItem(lx.symbol.iXFRM_SCALE)[0]
        #position
        try:
            pos = loc.GetTransformItem(lx.symbol.iXFRM_POSITION)
        except LookupError:
            pos = loc.AddTransformItem(lx.symbol.iXFRM_POSITION)[0]
        #rotation
        try:
            rot = loc.GetTransformItem(lx.symbol.iXFRM_ROTATION)
        except LookupError:
            rot = loc.AddTransformItem(lx.symbol.iXFRM_ROTATION)[0]

        #write zeroes...
        for chanIdx in range(2, 5):
            chanWrite.Double(scl, chanIdx, 1.0)
            chanWrite.Double(pos, chanIdx, 0.0)
            chanWrite.Double(rot, chanIdx, 0.0)

def MakeInstance(item, transform):
    """ Creates an instance of input item based on the input transform
        item =  lx.object.Item or
                lxu.object.Item instance
        transforms = transform for new instances

        A transform is a tuple of tuples for the scale, rotation
        and position of the new instance:
        (
            (scl_x, scl_y, scl_z),
            (rot_x, rot_y, rot_z),
            (pos_x, pos_y, pos_x),
        )

        returns the new instance
    """

    scene = GetScene()
    chanRead = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
    chanWrite = lx.object.ChannelWrite(chanRead)

    #create a new instance of the mesh item
    inst = scene.ItemInstance(item)

    #set the instance to be a child of the mesh
    inst.SetParent(item)

    #initialize transforms for the instance
    InitXfrms(inst)

    #get a locator interface for the instance
    loc = lx.object.Locator(inst)
    t_items = ( loc.GetTransformItem(lx.symbol.iXFRM_SCALE),
                loc.GetTransformItem(lx.symbol.iXFRM_ROTATION),
                loc.GetTransformItem(lx.symbol.iXFRM_POSITION))

    for a, b in enumerate(t_items):
        #a = (0, 1, 2)
        #b = transform item
        b = lx.object.Item(b)
        for xfrmIdx, chanIdx in zip(range(3), range(2,5)):
            # lx.out("chanIdx: %s" % chanIdx)
            # lx.out("xfrmIdx: %s" % xfrmIdx)
            chanWrite.Double(b, chanIdx, transform[a][xfrmIdx])

    return inst