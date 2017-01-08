#python

import lx, lxu, lxu.select, os, metermade

# get file path
PATH = os.path.dirname(lx.eval('query sceneservice scene.file ? current'))
# get parent dir
PATH = os.path.abspath(os.path.join(PATH,os.pardir))
# add stuff to path
PATH = os.path.join(PATH,"metermade")
    
ASSY = "_aGrp"
RIGS = [
    "Distance_X",
    "Distance_Y",
    "Distance_Z",
    "Distance_3D",
    "Angle_X",
    "Angle_Y",
    "Angle_Z",
    "Angle_3D"
]

n = lx.eval("query sceneservice item.N ?")
scene = lxu.select.SceneSelection().current()
for i in range(n):
    obj = scene.ItemLookup(lx.eval("query sceneservice item.id ? %s" % i))
    metermade.set_tag(obj,"MCMM","1")

for rig in RIGS:
    lx.eval("select.drop item")
    
    lx.out("selecting %s" % (rig+ASSY))
    lx.eval("select.item {%s} set" % (rig+ASSY))
    
    lx.out("saving to %s" % (os.path.join(PATH,rig+".lxp...")))
    lx.eval("item.selPresetSave locator {%s}" % (os.path.join(PATH,rig+".lxp")))
    lx.out("Success.")
    
try:
    lx.eval("scene.save")
    lx.out("Saved scene.")
except:
    lx.out("Unable to save scene.")
    
metermade.success("Update Successful","All new dimensions will use the updated rigs.\nNOTE: Existing dimensions will be unchanged.")