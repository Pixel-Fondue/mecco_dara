#python 

import lx, lxu, lxu.select, re, sys

GROUP_NAME = "mecco_metermade"
GROUPLOC_NAME = "dimensions"

def get_tags(item, namesOnly=True):
    
    if namesOnly:
        tags = []
    else:
        tags = {}

    tag = lx.object.StringTag(item)
    for x in range(tag.Count()):
        tagID, tagdata = tag.ByIndex(x)
        tagname = lxu.decodeID4(tagID)
        if namesOnly:
            tags.append(tagname)
        else:
            tags[tagname] = tagdata
    return tags

def set_tag(item, tagname, tagval):
    
    tagID = lxu.lxID4(tagname)
    if not tagID:
        raise LookupError("Can't create tagID")
    if tagID:
        tag = lx.object.StringTag(item)
        tag.Set(tagID, tagval)

def die(title="metermade",msg="I thought I thaw a puddy tat."):
    lx.eval('dialog.setup warning')
    lx.eval('dialog.title {%s}' % title)
    lx.eval('dialog.msg {%s}' % msg)
    lx.eval('dialog.open')
    sys.exit()

def success(title="metermade",msg="Operation completed successfully."):
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {%s}' % title)
    lx.eval('dialog.msg {%s}' % msg)
    lx.eval('dialog.open')

def quick_user_value(valHandle, valType='string', nicename='', default=''):
    if lx.eval('query scriptsysservice userValue.isDefined ? %s' % valHandle) == 0:
        lx.eval('user.defNew %s %s' % (valHandle, valType))

    try:
        lx.eval('user.def %s username {%s}' % (valHandle, nicename))
        lx.eval('user.def %s type %s' % (valHandle, valType))
        lx.eval('user.value %s {%s}' % (valHandle, default))
        lx.eval('user.value %s' % valHandle)
        return lx.eval('user.value %s value:?' % valHandle)
    except:
        return False

def get_parent_assemblies(item):
    """ "item" is a single item ident string or disambiguated name
        returns list of assemblies item belongs to """
    groups = []
    _groups = lx.evalN("query sceneservice locator.groups ? {%s}" % item)
    for _group in _groups:
        if "assembly" in lx.evalN("query sceneservice group.tags ? {%s}" % _group):
            groups.append(_group)
    return groups

def selectByPrefix(prefix):
    item_id = False
    lx.eval('select.drop item')
    n = lx.eval("query sceneservice item.N ?")
    # Loop through the items in the scene
    
    for i in range(n):
        # Get the item name
        item_name = lx.eval("query sceneservice item.name ? %s" % i)
        item_type = lx.eval("query sceneservice item.type ? %s" % i)
        selectedSomething = False
        
        scene = lxu.select.SceneSelection().current()
        obj = scene.ItemLookup(lx.eval("query sceneservice item.id ? %s" % i))
        tags = get_tags(obj)
        
        if item_name.startswith(prefix) and "MCMM" in tags:
            # Get the item ID
            item_id = lx.eval("query sceneservice item.id ? %s" % i)
            lx.eval('select.subItem {%s} add' % item_id)
            selectedSomething = True
            
    return selectedSomething

def select_by_group_and_type(group,itype):
    item_id = False
    lx.eval('select.drop item')
    n = lx.eval("query sceneservice item.N ?")
    # Loop through the items in the scene
    
    for i in range(n):
        # Get the item name
        item_groups = lx.eval("query sceneservice locator.groups ? {%s}" % i)
        item_type = lx.eval("query sceneservice item.type ? %s" % i)
        selectedSomething = False
        if group in item_groups and item_type == itype:
            # Get the item ID
            item_id = lx.eval("query sceneservice item.id ? %s" % i)
            lx.eval('select.subItem {%s} add' % item_id)
            selectedSomething = True
            
    return selectedSomething

def get_mm_group_id():
    item_id = False
    n = lx.eval("query sceneservice item.N ?")
    # Loop through the items in the scene
    
    for i in range(n):
        # Get the item name
        item_name = lx.eval("query sceneservice item.name ? %s" % i)
        if item_name == GROUP_NAME:
            # Get the item ID
            item_id = lx.eval("query sceneservice item.id ? %s" % i)
            break
    return item_id

def create_mm_group():
    item_id = get_mm_group_id()
    if item_id != False:
        lx.eval('select.item %s set' % item_id)
    else:
        lx.eval('!!group.create %s mode:empty' % GROUP_NAME)
        
#WORK IN PROGRESS
#def create_mm_gloc(grouploc_name):
#    item_id = get_mm_group_id()
#    if item_id != False:
#        lx.eval('select.item %s set' % item_id)
#    else:
#        lx.eval('item.create groupLocator %s' % grouploc_name)

def select_mm_group():
    item_id = get_mm_group_id()
    if item_id != False:
        lx.eval('select.item %s set' % item_id)
        return True
    else:
        return False

def get_latest_group_id():
    item_id = False
    n = lx.eval("query sceneservice item.N ?")-1
    # Loop through the items in the scene
    
    while n >= 0:
        # Get the item name
        itemType = lx.eval("query sceneservice item.type ? %s" % n)
        if itemType == "group":
            # Get the item ID
            item_id = lx.eval("query sceneservice item.id ? %s" % n)
            break
        n = n-1
    return item_id
    
def get_latest_item(username):
    item_id = False
    n = lx.eval("query sceneservice item.N ?")-1
    # Loop through the items in the scene
    
    while n >= 0:
        # Get the item name
        itema = lx.eval("query sceneservice item.name ? %s" % n)
        itemb = re.sub(r'\(.*?\)', '', itema)
        itemc = itemb.replace(" ","")
        if itemc.startswith(username):
            # Get the item ID
            item_id = lx.eval("query sceneservice item.id ? %s" % n)
            lx.out("match: %s" % item_id)
            break
        n = n-1
    return item_id