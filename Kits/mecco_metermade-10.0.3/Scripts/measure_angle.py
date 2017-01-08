#python

import re, metermade

if lx.eval("select.count vertex ?") != 3:
    metermade.die(
        "Metermade: Select exactly three verts.",
        "Select three vertices to add an angular dimension."
    )

LOC_A = "A_"
LOC_B = "B_"
LOC_C = "C_"
LOC_OFFSET = "offset_"
RIG_PREFIX = "Angle_"

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

i = -1
for loc in [LOC_A,LOC_B,LOC_C]:
    i = i+1
    lx.eval("select.subItem %s set" % metermade.get_latest_item(loc))
    lx.eval("select.subItem %s add" % MESH)
    lx.eval("constraintGeometry vert pos")

    lx.eval("item.channel cmGeometryConstraint$indexA %s" % VERTS[i])

    lx.eval("select.drop item")

    
lx.eval("select.subItem {%s} set" % metermade.get_latest_item(LOC_OFFSET))
lx.eval("tool.set TransformMoveItem on")