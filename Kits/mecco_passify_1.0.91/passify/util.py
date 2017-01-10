# python

import lx, modo
from var import *
from inspect import currentframe, getouterframes
from os.path import basename

def selected_channels():
    """Returns a list of tuples containing item id, channel index, and channel name for all selected channels"""
    q = lx.evalN("query sceneservice selection ? channels")
    return [t[1:-1].split(",") for t in q]

def is_enabled(cmd_string) :
    """Returns True if the supplied modo command is enabled.

    :param cmd_string: command to test, e.g. 'edit.apply'
    :type cmd_string: str"""

    msg = lx.service.Message().Allocate()
    cmd = lx.service.Command().SpawnFromString(cmd_string)[2]
    try:
      cmd.Enable(msg)
    except RuntimeError, e:
      if e.message == 'bad result: CMD_DISABLED':
         return False
      raise
    return True

def safe_edit_apply():
    '''Runs an edit.apply without throwing any errors.'''
    if is_enabled('edit.apply'):
        try:
            lx.eval('!edit.apply')
            return True
        except:
            return False

def safe_edit_discard():
    '''Runs an edit.apply without throwing any errors.'''
    if is_enabled('edit.discard'):
        try:
            lx.eval('!edit.discard')
            return True
        except:
            return False

def message(key_string):
    """Retreive from passify message table."""
    return lx.eval('query messageservice msgfind ? @passify@%s@' % key_string)

def buildTag(parts_list):
    """Concatenate tags comprised of multiple parts."""
    return TAG_SEP.join(parts_list)

def fetch_tagged(type_=None):
    """Returns a list of modo items with PSFY tags.

    :param type_: search only for items of type - improves performance
    :type type_: str 'renderPassGroups', 'groups', 'locators', 'meshes', 'cameras', or 'actors'"""

    tagged = set()
    if type_:
        for i in getattr(modo.Scene(), type_):
            if i.hasTag(TAG):
                tagged.add(i)
    if not type_:
        for i in modo.Scene().iterItems():
            if i.hasTag(TAG):
                tagged.add(i)
    return tagged

def fetch_by_tag(tags, list_=False, type_=None):
    """Looks for an item in the current scene containing any of the supplied PSFY tags.
    Returns the first item encountered by default, or a list if list param is True.
    (Note: PSFY tags are hyphen-separated lists.)

    :param tags: PSFY tag to find
    :type tags: str or list

    :param list_: return a list instead of first encounter
    :type list_: bool

    :param type_: search only for items of type - improves performance
    :type type_: str 'renderPassGroups', 'groups', 'locators', 'meshes', 'cameras', or 'actors'"""

    tags = [tags] if isinstance(tags, str) else tags
    found = set()

    for i in fetch_tagged(type_):
        if [t for t in tags if t in i.getTags()[TAG].split(TAG_SEP)]:
            if not list_:
                return i
            found.add(i)

    return list(found) if found else None

def reorder(item,mode=TOP):
    """Reorders a modo item to the top or bottom of its parent hierarchy.

    :param item: message to display
    :type item: modo item

    :param mode: where to place within parent
    :type mode: "top" or "bottom" """

    index = len(item.parent.children())-1 if mode == TOP else 0
    item.setParent(item.parent, index)

def debug(message_string, do_break=False):
    """Prints a debug message in the Event Log if DEBUG is True.
    Throws a dialog with the same message if BREAKPOINTS and do_break are True.

    :param message_string: message to display
    :type message_string: str

    :param do_break: throw dialog
    :type do_break: bool"""


    (frame, filename, line_number, function_name, lines, index) = getouterframes(currentframe())[1]
    message = "%s line %s: %s" % (basename(filename), line_number, str(message_string))

    if BREAKPOINTS and do_break:
        modo.dialogs.alert("breakpoint", message)
    if DEBUG:
        lx.out("debug: " + message)

def deactivate_passes(pass_group):
    """Deactivates all passes in supplied pass group.

    :param pass_group: item(s) to test for maskability
    :type pass_group: modo item object or list of objects
    """
    graph_kids = pass_group.itemGraph('itemGroups').forward()
    for p in [i for i in graph_kids if i.type == 'actionclip']:
        p.actionClip.SetActive(0)

def get_selected_and_maskable():
    """Returns a list of object(s) that can be masked."""

    items = modo.Scene().selected

    r = set()
    for item in items:
        if test_maskable(item):
            r.add(item)

    r = list(r)

    return r

def test_maskable(items):

    """Returns True if an item or items can be masked by shader tree masks.
    e.g. Mesh items return True, Camera items return False

    :param items: item(s) to test for maskability
    :type items: object or list of objects
    """

    if not isinstance(items,(list, tuple)):
        items = [items]

    hst_svc = lx.service.Host ()
    scn_svc = lx.service.Scene ()
    hst_svc.SpawnForTagsOnly ()

    r = list()
    for item in items:
        if item.isLocatorSuperType():
            item = item.internalItem

            type = scn_svc.ItemTypeName (item.Type ())

            factory = hst_svc.LookupServer (lx.symbol.u_PACKAGE, type, 1)

            for i in range (factory.TagCount ()):
                if (factory.TagByIndex (i)[0]== lx.symbol.sPKG_IS_MASK):
                    r.append(True)
                else:
                    r.append(False)
        else:
            r.append(False)

    if len(r) == 1:
        return r[0]
    return r
