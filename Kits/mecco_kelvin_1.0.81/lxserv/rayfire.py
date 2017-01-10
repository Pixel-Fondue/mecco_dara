# python

def rayCast(self,targetItem=None):

        vServ = lx.service.View3Dport()
        vpIDX , x, y = vServ.Mouse()

        pos = norm = None

        if vpIDX != -1:

            if vpIDX > (vServ.Count() -1 ):
                return pos,norm

            view = lx.object.View3D(vServ.View(vpIDX))
            viewType = lxu.decodeID4(view.Space())

            if targetItem is None:
                if viewType == "MO3D":
                    try:
                        lx.eval('!!select.3DElementUnderMouse set')
                    except:
                        return pos,norm

                    selection = lxu.select.ItemSelection().current()

                    if len(selection) > 0:
                        #if selection[-1].Type() in [
                        #    self.scnSrv.ItemTypeLookup(lx.symbol.sITYPE_MESH),
                        #    self.scnSrv.ItemTypeLookup(lx.symbol.sITYPE_MESHINST)
                        #    ]:
                        targetItem = selection[-1]

                elif viewType == "PREV":
                    targetItem = lx.eval('query view3dservice element.over ? item')
                    lx.eval('select.item {%s} set' % targetItem)

            if targetItem != None:

                try:
                    pos,norm = view.To3DHit(x,y)
                except:
                    pass

        return pos,norm
