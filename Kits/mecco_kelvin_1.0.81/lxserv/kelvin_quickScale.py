#python

import lx, lxu, modo, traceback

NAME_CMD = "kelvin.quickScale"

def get_active_layers():
    """Returns a list of all currently active mesh layers (regardless of selection state)."""

    lyr_svc = lx.service.Layer ()
    scan = lx.object.LayerScan (lyr_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE))
    itemCount = scan.Count ()
    if itemCount > 0:
            items = [modo.Mesh( scan.MeshItem(i) ) for i in range(itemCount)]
    scan.Apply ()

    return items

def boundingBoxMax(bounding_boxes):
    boundingBoxMax = [[0,0,0],[0,0,0]]
    boundingBoxMax[0][0] = min([i[0][0] for i in bounding_boxes])
    boundingBoxMax[0][1] = min([i[0][1] for i in bounding_boxes])
    boundingBoxMax[0][2] = min([i[0][2] for i in bounding_boxes])
    boundingBoxMax[1][0] = max([i[1][0] for i in bounding_boxes])
    boundingBoxMax[1][1] = max([i[1][1] for i in bounding_boxes])
    boundingBoxMax[1][2] = max([i[1][2] for i in bounding_boxes])
    return boundingBoxMax

class CMD_kelvin(lxu.command.BasicCommand):

    _last_used = 1.0

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("width", lx.symbol.sTYPE_DISTANCE)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    @classmethod
    def set_last_used(cls, value):
        cls._last_used = value

    def cmd_DialogInit(self):
        self.attr_SetFlt(0, self._last_used)

    def basic_Execute(self, msg, flags):
        try:
            targetSize = self.dyna_Float(0) if self.dyna_IsSet(0) else 1.0
            self.set_last_used(targetSize)

            bboxes = [i.geometry.boundingBox for i in get_active_layers()]
            bbox = boundingBoxMax(bboxes)
            currentSize = bbox[1][0] - bbox[0][0]
            ratio = targetSize / currentSize

            originalRef = lx.eval("item.refSystem ?")

            lx.eval("item.refSystem")
            lx.eval("select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true")
            lx.eval("tool.set actr.origin on")

            lx.eval("tool.set TransformScale on")
            lx.eval("tool.attr xfrm.transform SX %s" % str(float(ratio)))
            lx.eval("tool.attr xfrm.transform SY %s" % str(float(ratio)))
            lx.eval("tool.attr xfrm.transform SZ %s" % str(float(ratio)))
            lx.eval("tool.apply")
            lx.eval("tool.set TransformScale off")

            if originalRef:
                lx.eval("item.refSystem {%s}" % originalRef)
            else:
                lx.eval("item.refSystem {}")

            lx.eval("tool.clearTask axis")
            lx.eval("select.typeFrom item;pivot;center;edge;polygon;vertex;ptag true")

        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
