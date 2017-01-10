#python

import metermade

args = lx.args()

if args:
    if args[0] == "hide":
        metermade.selectByPrefix("metermade")
        lx.eval('item.channel chanModify$draw off')
        lx.eval("item.channel group$visible off set mecco_metermade")
        
    elif args[0] == "show":
        metermade.selectByPrefix("metermade")
        lx.eval('item.channel chanModify$draw on')
        lx.eval("item.channel group$visible on set mecco_metermade")
        
#    elif args[0] == "hideSel":
#        items = lx.evalN("query sceneservice selection ? locator")
#        
#        groups = []
#        for item in items:
#            groups.extend( metermade.get_parent_assemblies(item) )
#            
#        lx.eval("select.drop item")
#        
#        for group in groups:
#            lx.eval("item.channel group$visible on set {%s}" % group)
#            
#        metermade.select_by_group_and_type(group,"cmMeasureAngle")
#        lx.eval('item.channel chanModify$draw off')
#        metermade.select_by_group_and_type(group,"cmMeasureDistance")
#        lx.eval('item.channel chanModify$draw off')
        
    else:
        lx.out("invalid argument: 'hide' or 'show'")
else:
    lx.out("script requires argument: 'hide' or 'show'")
    

lx.eval("select.drop item")