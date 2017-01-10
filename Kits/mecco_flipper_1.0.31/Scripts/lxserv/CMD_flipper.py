#python
import sys
import lx
import lxu
import lxifc
import re
from math import ceil, floor, pi, sin, cos
from copy import deepcopy
import mm_tags
from mecco_utils_contexts import catch
from mecco_utils_modo import MakeInstance, GetScene
from mecco_utils_main import StrToInt

def exclog(script=''):
    """ Outputs error to log """
    lx.out("Exception \"%s\" on line %d: %s" % (sys.exc_value, sys.exc_traceback.tb_lineno, script))


""" Constants """
"""####"""


""" Names """
NAME_CMD_MIRROR_CREATE  = "mecco.flipper.create"
NAME_CMD_MIRROR_CONVERT = "mecco.flipper.convert"
NAME_CMD_MIRROR_COMMIT  = "mecco.flipper.commit"
NAME_CMD_MIRROR_EDIT    = "mecco.flipper.edit"

NAME_CMDARG_X           = "X"
NAME_CMDARG_Y           = "Y"
NAME_CMDARG_Z           = "Z"
NAME_CMDARG_EXISTING    = "existing"
NAME_CMDARG_TOLERANCE   = "tolerance"

NAME_ITEM_NAME          = "Flipper Item"

NAME_TAG                = "MRRO"

NAME_PTAG_INSTANCES     = "Flipper Instances"

"""####"""


""" Symbols """
s_ACTIONLAYER_EDID          = lx.symbol.s_ACTIONLAYER_EDIT
s_ACTIONLAYER_SETUP         = lx.symbol.s_ACTIONLAYER_SETUP
sTYPE_STRING                = lx.symbol.sTYPE_STRING
sTYPE_INTEGER               = lx.symbol.sTYPE_INTEGER
sTYPE_BOOL                  = lx.symbol.sTYPE_BOOLEAN
sTYPE_FLOAT                 = lx.symbol.sTYPE_FLOAT
sTYPE_DISTANCE              = lx.symbol.sTYPE_DISTANCE
sITYPE_GROUP                = lx.symbol.sITYPE_GROUP
sITYPE_MESHINST             = lx.symbol.sITYPE_MESH
sITYPE_MESHINST             = lx.symbol.sITYPE_MESHINST
sSELTYP_ITEM                = lx.symbol.sSELTYP_ITEM
sGRAPH_MESHINST             = lx.symbol.sGRAPH_MESHINST
fCMDARG_OPTIONAL            = lx.symbol.fCMDARG_OPTIONAL
fCMDARG_QUERY               = lx.symbol.fCMDARG_QUERY
fCMDARG_DYNAMIC_DEFAULTS    = lx.symbol.fCMDARG_DYNAMIC_DEFAULTS
fCMD_UI                     = lx.symbol.fCMD_UI
fCMD_UNDO                   = lx.symbol.fCMD_UNDO
fCMD_MODEL                  = lx.symbol.fCMD_MODEL
f_LAYERSCAN_PRIMARY         = lx.symbol.f_LAYERSCAN_PRIMARY
f_LAYERSCAN_EDIT            = lx.symbol.f_LAYERSCAN_EDIT
f_MESHEDIT_GEOMETRY         = lx.symbol.f_MESHEDIT_GEOMETRY
iPTYP_FACE                  = lx.symbol.iPTYP_FACE
iXFRM_POSITION              = lx.symbol.iXFRM_POSITION
iXFRM_ROTATION              = lx.symbol.iXFRM_ROTATION
iXFRM_SCALE                 = lx.symbol.iXFRM_SCALE
"""####"""

""" Global services """
svc_scene = lx.service.Scene()
svc_msg   = lx.service.Message()
svc_layer = lx.service.Layer()
svc_sel   = lx.service.Selection()
mo        = svc_msg.Allocate()
"""####"""

""" Selection types """
iSELTYP_ITEM = svc_sel.LookupType(sSELTYP_ITEM)
"""####"""


""" Global properties """
"""####"""


""" Item type integers """
iTYPE_LOCATOR   = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_LOCATOR)
iTYPE_GROUP     = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_GROUP)
iTYPE_MESH      = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_MESH)
iTYPE_MESHINST  = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_MESHINST)
"""####"""


""" Basic functions """
def FlipperXfrms(x, y, z):
    zeroes = (0.0, 0.0, 0.0)
    transforms = []
    bools = []
    for x in range(x+1):
        for y in range(y+1):
            for z in range(z+1):
                _t = ([-1.0 if n else 1.0 for n in (x, y, z)], zeroes, zeroes)
                transforms.append(_t)
                bools.append((x, y, z))
    return transforms[1:], bools[1:]

def FlipperConvert(x, y, z, items):
    transforms, bools = FlipperXfrms(x, y, z)
    for item in items:
        if item.TestType(iTYPE_MESH):
            name = item.Name()
            tag = "%s%s%s" % (x, y, z)
            mm_tags.set_tag(item, NAME_TAG, tag)
            for t, b in zip(transforms, bools):
                inst = MakeInstance(item, t)
                inst.SetName("%s (%s)" % (name, NAME_ITEM_NAME))
                tag = "%s%s%s" % b
                mm_tags.set_tag(inst, NAME_TAG, tag)

def CreateDefaultGeo(x, y, z):

    lx.eval("layer.new")

    lx.eval("script.run {macro.scriptservice:32235710027:macro}")
    lx.eval("poly.subdivide flat")

    layerIdx = lx.eval("query layerservice layer.index ? main")

    verts = lx.evalN("query layerservice verts ? all")
    verts_remove = []

    lx.out(x, y, z)
    for v in verts:
        pos = lx.eval("query layerservice vert.pos ? %s" % v)
        # lx.out("%s: %s" % (v, pos))

        for a, p in zip((x, y, z), pos):
            if a and (p < 0.0):
                verts_remove.append(v)
                break

    lx.eval("select.drop vertex")
    for v in verts_remove:
        lx.eval("select.element {%s} vertex add %s" % (layerIdx, v))

    lx.eval("delete")

"""####"""


class CMD_Flipper_Create(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME_CMDARG_X, sTYPE_BOOL)
        self.dyna_Add(NAME_CMDARG_Y, sTYPE_BOOL)
        self.dyna_Add(NAME_CMDARG_Z, sTYPE_BOOL)

    def cmd_Flags(self):
        return fCMD_MODEL | fCMD_UNDO
    def cmd_Interact(self):
        pass
    def cmd_Execute(self,flags):
        """ Create a new mesh item and run the "convert" command on it.
        """
        x, y, z = [self.dyna_Int(n, 0) for n in range(3)]

        lx.eval("select.drop item locator")

        CreateDefaultGeo(x, y, z)

        itemId = lx.eval("query layerservice layer.id ? main")
        scene = GetScene()
        item = scene.ItemLookup(itemId)
        FlipperConvert(x, y, z, (item,))
        return lx.result.OK


class CMD_Flipper_Convert(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME_CMDARG_X, sTYPE_BOOL)
        self.dyna_Add(NAME_CMDARG_Y, sTYPE_BOOL)
        self.dyna_Add(NAME_CMDARG_Z, sTYPE_BOOL)


    def cmd_Flags(self):
        return fCMD_MODEL | fCMD_UNDO
    def cmd_Interact(self):
        pass
    def cmd_Execute(self,flags):
        """ Get current selection.
            For each locator-type item in the selection (meshes only?):
            Create one instance for each axis we're mirroring.
            Do this by creating one "transform-tuple" matrix for each axis,
            and then running MakeInstance using those matrices.
        """

        x, y, z = [self.dyna_Int(n, 0) for n in range(3)]
        selection = lxu.select.ItemSelection().current()
        FlipperConvert(x, y, z, selection)

        return lx.result.OK


    def cmd_Query(self,index,vaQuery):
        return lx.result.OK


class CMD_Flipper_Commit(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME_CMDARG_TOLERANCE, sTYPE_DISTANCE)
        self.basic_SetFlags(0, fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return fCMD_MODEL | fCMD_UNDO
    def cmd_Interact(self):
        pass
    def cmd_Execute(self, flags):
        #get the current scene and selection
        scene           = GetScene()
        selection       = lxu.select.ItemSelection().current()

        #get ItemGraph interface for instances
        inst_sceneGraph = scene.GraphLookup(sGRAPH_MESHINST)
        inst_itemGraph  = lx.object.ItemGraph(inst_sceneGraph)

        DEFAULT_TOLERANCE = lx.eval('user.value {mecco_flipper_mergeDist} ?')
        tol = self.dyna_Float(0, DEFAULT_TOLERANCE)

        for item in selection:
            #make sure it's of the right type
            if not item.TestType(iTYPE_MESH):
                continue

            #make sure it's got the right tag
            try:
                tagData = mm_tags.get_tag(item, NAME_TAG)
            except:
                continue

            #if we made it this far everything must be ok
            item_ident = item.Ident()

            #first thing we need to do is clear the "mirror" flag:
            lx.eval("select.drop polygon")
            lx.eval("select.editSet {%s} remove {}" % NAME_PTAG_INSTANCES)

            selectionList = [item_ident, ]

            #build list of idents for children
            child_idents = [m.Ident() for m in item.SubList()]

            inst_idents = []
            flips = []
            #grab all instances that are also children

            for n in range(inst_itemGraph.FwdCount(item)):
                #get the instance for this index
                inst = inst_itemGraph.FwdByIndex(item, n)
                inst_ident = inst.Ident()
                #make sure instance is a child
                if inst_ident in child_idents:
                    inst_idents.append(inst_ident)
                    if mm_tags.get_tag(inst, NAME_TAG).count("1") in (1, 3):
                        flips.append(inst_ident)

            new_meshes = []
            for ident in inst_idents:
                lx.eval("select.drop item")
                lx.eval("select.item {%s} set" % ident)
                lx.eval("item.setType Mesh")
                if ident in flips:
                    lx.eval("poly.flip")

                new_ident = lx.eval1("query sceneservice selection ? mesh")
                new_meshes.append(new_ident)

            lx.eval("select.drop item")
            for ident in new_meshes:
                lx.eval("select.item {%s} add" % ident)


            #all instances selected, convert to meshes and assign ptag
            """ temporary workaround:
                the layer.mergeMeshes command causes a crash
                when you undo. The workaround is to select
                only the former instances, cut their polygons,
                delete the items, and paste them into the
                first item.
            """
            """ START BUGGED CODE """
            # selectionList.extend(
            #    lx.evalN(
            #        "query sceneservice selection ? mesh"
            #        )
            #    )
            # lx.eval("select.drop item")
            # for ident in selectionList:
            #    lx.eval("select.item {%s} add" % ident)
            # lx.eval("layer.mergeMeshes true")
            """ END BUGGED CODE / START WORKAROUND """
            lx.eval("select.type polygon")
            lx.eval("select.polygon add 0 subdiv 0")
            lx.eval("select.editSet {%s} add {}" % NAME_PTAG_INSTANCES)
            lx.eval("cut")
            lx.eval("select.type item")
            lx.eval("item.delete")
            lx.eval("select.item {%s} set" % item_ident)
            lx.eval("select.type polygon")
            lx.eval("paste")
            lx.eval("select.drop polygon")
            """ END WORKAROUND """

            lx.eval("select.edge add bond equal")
            lx.eval("vert.merge fixed dist:%s morph:true disco:false" % tol)
            lx.eval("select.drop edge")
        lx.eval("select.type item")
        return lx.result.OK
    def cmd_Query(self, index, vaQuery):
        pass


class CMD_Flipper_Edit(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return fCMD_MODEL | fCMD_UNDO
    def cmd_Interact(self):
        pass
    def cmd_Execute(self,flags):
        scene = GetScene()
        selection = lxu.select.ItemSelection().current()
        selectionIdents = []
        for item in selection:
            if not item.TestType(iTYPE_MESH):
                continue
            try:
                tagData = mm_tags.get_tag(item, NAME_TAG)
            except LookupError:
                continue
            ident = item.Ident()
            name = item.UniqueName()
            x, y, z = [StrToInt(c) for c in tagData]

            transforms, bools = FlipperXfrms(x, y, z)

            selectionIdents.append(ident)
            lx.eval("select.item {%s} set" % ident)
            lx.eval("select.drop polygon")
            lx.eval("select.useSet {%s} select" % NAME_PTAG_INSTANCES)
            lx.eval("delete")

            for t, b in zip(transforms, bools):
                inst = MakeInstance(item, t)
                inst.SetName("%s (%s)" % (name, NAME_ITEM_NAME))
                tag = "%s%s%s" % b
                mm_tags.set_tag(inst, NAME_TAG, tag)

        for ident in selectionIdents:
            lx.eval("select.item {%s} add" % ident)

        return lx.result.OK
    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(CMD_Flipper_Create, NAME_CMD_MIRROR_CREATE)
lx.bless(CMD_Flipper_Convert, NAME_CMD_MIRROR_CONVERT)
lx.bless(CMD_Flipper_Commit, NAME_CMD_MIRROR_COMMIT)
lx.bless(CMD_Flipper_Edit, NAME_CMD_MIRROR_EDIT)
