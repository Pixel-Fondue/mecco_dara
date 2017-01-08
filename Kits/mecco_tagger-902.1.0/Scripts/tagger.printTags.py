# python

import modo

for p in modo.Mesh().geometry.polygons.selected:
    lx.out(p.tags())
