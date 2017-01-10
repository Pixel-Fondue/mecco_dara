#python

import re, metermade

if lx.eval("select.count vertex ?") != 2:
    metermade.die(
        "Metermade: Select exactly two verts.",
        "Select two vertices to add a linear dimension."
    )
    
LOC_A = "A_"
LOC_B = "B_"
LOC_AA = "AA_"
RIG_PREFIX = "Distance_"

args = lx.args()
RIG_SUFFIX = args[0] if args else "3D"

MESH = lx.eval("query layerservice layer.id ? selected")
VERTS = lx.eval("query layerservice verts ? selected")

# Let's get this party started.

metermade.create_mm_group()

lx.eval("view3d.overlay true")

lx.eval("mecco.metermade.getRig %s" % (RIG_PREFIX + RIG_SUFFIX))
lx.eval("item.parent %s %s 0" % (metermade.get_latest_group_id(),metermade.get_mm_group_id()))

lx.eval("select.typeFrom item true")
lx.eval("select.drop item")

A = metermade.get_latest_item(LOC_A)
lx.eval("select.subItem %s set" % A)
lx.eval("select.subItem %s add" % MESH)
lx.eval("constraintGeometry vert pos")

lx.eval("item.channel cmGeometryConstraint$indexA %s" % VERTS[0])

lx.eval("select.drop item")

B = metermade.get_latest_item(LOC_B)
lx.eval("select.subItem %s set" % B)
lx.eval("select.subItem %s add" % MESH)
lx.eval("constraintGeometry vert pos")

lx.eval("item.channel cmGeometryConstraint$indexA %s" % VERTS[1])

lx.eval("select.drop item")
lx.eval("select.subItem {%s} set" % metermade.get_latest_item(LOC_AA))
lx.eval("tool.set TransformMoveItem on")