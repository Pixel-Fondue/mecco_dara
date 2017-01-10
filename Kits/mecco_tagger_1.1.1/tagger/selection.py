#python

import modo, lx, items
from PolysConnectedByTag import *
from var import *
from debug import *


def get_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False


def get_polys(connected=SCOPE_SELECTED):
    """Returns a list of all implicitly selected polys in all active layers.
    If in poly mode, returns selected polys. If in edge or vertex mode,
    returns all polys adjacent to all selected components.

    :param connected: If True, returns all polys connected to the selection."""

    timer = DebugTimer()

    result = set()
    scene = modo.scene.current()

    for layer in items.get_active_layers():

        if get_mode() == 'polygon':
            if layer.geometry.polygons.selected:
                for p in layer.geometry.polygons.selected:
                    result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'edge':
            if layer.geometry.edges.selected:
                for e in layer.geometry.edges.selected:
                    for p in e.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'vertex':
            if layer.geometry.edges.selected:
                for v in layer.geometry.vertices.selected:
                    for p in v.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)

        elif get_mode() == 'ptag':
            return []
        else:
            return []

        if connected == SCOPE_CONNECTED:
            result = island(result)
        elif connected == SCOPE_FLOOD:
            result = flood(result)

    timer.end()
    return list(result)

def get_ptags(i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,connected=SCOPE_SELECTED):
    """Returns a list of all pTags for currently selected polys in all active layers.

    :param i_POLYTAG: type of tag to return (str), e.g. lx.symbol.i_POLYTAG_MATERIAL
    :param connected: extend selection to connected polys (bool)
    """

    timer = DebugTimer()

    r = set()
    pp = get_polys(connected)
    if pp:
        for p in pp:
            tags = set(p.getTag(i_POLYTAG).split(";"))
            r.update(tags)

    timer.end()
    return list(r)


def island(seed_polys):
    polyIsland = set()
    checked = set()
    toCheck = set()

    for poly in seed_polys:

        if poly in polyIsland:
            continue

        polyIsland.add( poly )
        checked.add( poly )
        toCheck.add( poly )

        while toCheck:
            poly = toCheck.pop()
            for polyN in poly.neighbours:
                if not polyN in checked:
                    checked.add( polyN )
                    if not polyN in polyIsland:
                        polyIsland.add( polyN )
                        toCheck.add( polyN )

    return polyIsland


def flood(seed_polys, i_POLYTAG):
    seed_polys = set(seed_polys)

    polyIsland = set()
    checked = set()
    toCheck = set()

    for poly in seed_polys:
        tag = poly.getTag(i_POLYTAG)
        if not tag:
            return island(seed_polys)

        tags = set(tag.split(";"))
        if not tags:
            return island(seed_polys)

        if poly in polyIsland:
            continue

        polyIsland.add( poly )
        checked.add( poly )
        toCheck.add( poly )

        while toCheck:
            poly = toCheck.pop()

            for polyN in poly.neighbours:
                if not tags.intersection(set(polyN.getTag(i_POLYTAG).split(";"))):
                    continue
                if not polyN in checked:
                    checked.add( polyN )
                    if not polyN in polyIsland:
                        polyIsland.add( polyN )
                        toCheck.add( polyN )

    return polyIsland
