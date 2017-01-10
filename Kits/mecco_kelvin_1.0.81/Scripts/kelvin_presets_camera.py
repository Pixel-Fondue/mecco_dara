#python
import modo

evt = lx.args()[0]

if evt == 'beforeCreate':
   try:
       hitlist = []
       for i in modo.Scene().iterItems():
           if i.type == 'camera':
               hitlist.append(i)

       if len(hitlist) == 1 and hitlist[0].name == "Camera":
           for i in hitlist:
               modo.scene.current().removeItems(i)
   except:
       lx.out("finished")

elif evt == 'onCreate':
   pass

elif evt == 'onDo':
   pass

elif evt == 'onDrop':
   pass
