#python

import metermade

items = lx.evalN("query sceneservice selection ? locator")

groups = []
for item in items:
    groups.extend( metermade.get_parent_assemblies(item) )

lx.eval("select.drop item")

for group in groups:
    lx.eval("select.item {%s} add" % group)
    
lx.eval("!item.delete group")