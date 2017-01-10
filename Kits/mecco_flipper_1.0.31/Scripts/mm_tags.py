#python
import lx
import lxu

def get_tags(item, names=True):
    """ Get a list of string tags (if any) attached to an item. Requires an item object as input.

        item    - item object
        names   - if True (default), function returns a list of just tag names.
                  If False, returns a dictionary of tag names as keys and tag
                  data as values.

    """
    if names:
        tags = []
    else:
        tags = {}

    tag = lx.object.StringTag(item)
    for x in range(tag.Count()):
        tagID, tagdata = tag.ByIndex(x)
        tagname = lxu.decodeID4(tagID)
        if names:
            tags.append(tagname)
        else:
            tags[tagname] = tagdata
    return tags


def get_tag(item, tagname):
    """ Get the value of a string tag attached to an item. Requires an item object as input.

        item    - item object.
        tagname - the four character .

    """
    tagID = lxu.lxID4(tagname)
    if not tagID:
        raise LookupError("Can't create tagID")
    tag = lx.object.StringTag(item)
    return tag.Get(tagID)


def set_tag(item, tagname, tagval):
    """ Create or set a string tag on an item. Requires an item object as input.

        item    -  item object.
        tagname - the four character tagID.
        tagval  - The string value to be stored under the tag.

    """
    tagID = lxu.lxID4(tagname)
    if not tagID:
        raise LookupError("Can't create tagID")
    if tagID:
        tag = lx.object.StringTag(item)
        tag.Set(tagID, tagval)