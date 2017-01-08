#python

import math, metermade

if lx.eval("select.count vertex ?") != 2:
    metermade.die(
        "Metermade: Select exactly two verts.",
        "Select two vertices representing a known distance."
    )

MESH = lx.eval("query layerservice layer.id ? selected")
LAYER = lx.eval("query layerservice layers ? main")
VERTS = lx.eval("query layerservice verts ? selected")

A = lx.eval("query layerservice vert.wpos ? %s" % VERTS[0])
B = lx.eval("query layerservice vert.wpos ? %s" % VERTS[1])
C = [0,0,0]

for i in [0,1,2]:
    C[i] = A[i]-B[i]
    
D = math.sqrt(C[0]*C[0] + C[1]*C[1] + C[2]*C[2])
lx.out("current distance: %s" % D)

E = metermade.quick_user_value("metermade_scaleToKnown_target","distance","known distance",D)
lx.out("desired distance: %s" % E)

scaleFactor = E/D

lx.out("Scale factor: %s%%" % (scaleFactor*100))

lx.eval("item.refSystem %s" % MESH)
lx.eval("select.drop vertex")

lx.eval("tool.set TransformScale on")
lx.eval("tool.set actr.origin on")
lx.eval("tool.setAttr xfrm.transform SX %s" % scaleFactor);
lx.eval("tool.setAttr xfrm.transform SY %s" % scaleFactor);
lx.eval("tool.setAttr xfrm.transform SZ %s" % scaleFactor);
lx.eval("tool.doApply");
lx.eval("tool.set TransformScale off");

for vert in VERTS:
    lx.eval("select.element {%s} vertex add index:%s" % (LAYER,vert))
    
lx.eval("item.refSystem {}")