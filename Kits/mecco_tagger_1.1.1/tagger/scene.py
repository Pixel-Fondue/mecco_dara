import modo, lx
import util
from debug import *
from var import *

def add_pTag_to_recent(pTag, tagType):
    old_tag = modo.Scene().sceneItem.getTags().get(SCENE_TAG_RECENT)
    if old_tag:
        tags_list = old_tag.split(TAG_SEP)
    else:
        tags_list = []

    tags_list = [TAGTYPE_SEP.join((tagType, pTag))] + tags_list

    # removes duplicates while maintainint list order
    tags_list = [ii for n,ii in enumerate(tags_list) if ii not in tags_list[:n]]

    if len(tags_list) > SCENE_TAG_RECENT_MAX:
        tags_list = tags_list[:SCENE_TAG_RECENT_MAX]

    modo.Scene().sceneItem.setTag(SCENE_TAG_RECENT, TAG_SEP.join(tags_list))

def get_recent_pTags():
    tags = modo.Scene().sceneItem.getTags().get(SCENE_TAG_RECENT)
    if tags:
        tags = tags.split(TAG_SEP)
        tags = [tuple(i.split(TAGTYPE_SEP)) for i in tags]
    return tags

def all_tags_by_type(i_POLYTAG):
    timer = DebugTimer()

    tags = set()
    for m in modo.Scene().meshes:
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))

    timer.end()
    return sorted(list(tags))

def all_tags():
    timer = DebugTimer()

    tags = set()

    for m in modo.Scene().meshes:
        for i_POLYTAG in (lx.symbol.i_POLYTAG_MATERIAL, lx.symbol.i_POLYTAG_PICK, lx.symbol.i_POLYTAG_PART):
            n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
            for i in range(n):
                tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))

    timer.end()
    return sorted(list(tags))

def meshes_with_pTag(pTag, i_POLYTAG):
    meshes = set()

    for m in modo.Scene().meshes:
        tags = set()
        n = m.geometry.internalMesh.PTagCount(i_POLYTAG)
        for i in range(n):
            tags.add(m.geometry.internalMesh.PTagByIndex(i_POLYTAG, i))
        if pTag in tags:
            meshes.add(m)

    return list(meshes)

def replace_tag(tagType, replaceTag, withTag):
    i_POLYTAG = util.convert_to_iPOLYTAG(tagType)
    meshes = meshes_with_pTag(replaceTag, i_POLYTAG)

    hitcount = 0
    for mesh in meshes:
        with mesh.geometry as geo:
            hitlist = set()
            for poly in geo.polygons:

                if tagType in [MATERIAL, PART]:
                    if poly.getTag(i_POLYTAG) == replaceTag:
                        hitlist.add(poly)
                        hitcount += 1

                elif tagType == PICK:
                    if not poly.getTag(i_POLYTAG):
                        continue

                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    if replaceTag in pickTags:
                        hitlist.add(poly)
                        hitcount += 1


        with mesh.geometry as geo:
            for poly in hitlist:

                if tagType in [MATERIAL, PART]:
                    poly.setTag(i_POLYTAG, withTag)

                elif tagType == PICK:
                    pickTags = set(poly.getTag(i_POLYTAG).split(";"))
                    pickTags.discard(replaceTag)
                    if withTag:
                        pickTags.add(withTag)
                    poly.setTag(i_POLYTAG, ";".join(pickTags))

    return hitcount
