# python

import lx, lxu.command, lxifc, traceback, modo, tagger
from operator import ior

CMD_NAME = tagger.CMD_PTAG_REMOVEALL
DEFAULTS = [tagger.PART, '', False]


class PolyTaggerClass (lxifc.Visitor):
    def __init__ (self, polygon, mark_mode_valid, i_POLYTAG):
        self.i_POLYTAG = i_POLYTAG
        self.polygon = polygon
        self.mark_mode_valid = mark_mode_valid

        self.polygonIDs = set ()

        self.tag = lx.object.StringTag ()
        self.tag.set (self.polygon)

    def reset (self):
        self.polygonIDs = set ()

    def getPolyIDs (self):
        return self.polygonIDs

    def vis_Evaluate (self):
        if self.polygon.TestMarks (self.mark_mode_valid):
            self.tag.Set (self.i_POLYTAG, None)


class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.PART,
                    'popup': tagger.POPUPS_TAGTYPES_WITH_ALL,
                    'flags': [],
                }, {
                    'name': tagger.SCOPE,
                    'label': tagger.LABEL_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED_ITEMS,
                    'popup': tagger.POPUPS_REMOVE_ALL_SCOPE,
                    'flags': [],
                }
            ]

    def basic_Icon(self):
        if self.commander_arg_value(0):
            if self.commander_arg_value(0) == tagger.MATERIAL:
                return 'tagger.removeAllByMaterial'
            elif self.commander_arg_value(0) == tagger.PART:
                return 'tagger.removeAllByPart'
            elif self.commander_arg_value(0) == tagger.PICK:
                return 'tagger.removeAllBySet'

        return 'tagger.pTagRemoveAll'

    def basic_ButtonName(self):
        if self.commander_arg_value(0):
            label = []
            label.append(tagger.LABEL_REMOVE_ALL)
            label.append(tagger.convert_to_tagType_label(self.commander_arg_value(0)))
            label.append(tagger.LABEL_TAGS)
            return " ".join(label)

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0)
        scope = self.commander_arg_value(1)

        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)
        scope_label = tagger.LABEL_SCOPE_SELECTED_ITEMS if scope == tagger.SCOPE_SELECTED_ITEMS else tagger.LABEL_SCOPE_SCENE

        safety = modo.dialogs.yesNo(
            tagger.DIALOGS_REMOVE_ALL_TAGS[0],
            tagger.DIALOGS_REMOVE_ALL_TAGS[1] % (tagType.title(), scope_label.lower())
            )

        if safety == 'no':
            return

        poly_count = 0
        tag_count = 0

        if scope == tagger.SCOPE_SCENE:
            lx.eval("select.drop item")
            lx.eval("select.itemType mesh")

        layer_svc = lx.service.Layer ()
        layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_EDIT))
        if not layer_scan.test ():
            return

        mesh_svc = lx.service.Mesh ()
        mark_mode_valid = mesh_svc.ModeCompose (None, 'hide lock')

        for n in xrange (layer_scan.Count ()):
            mesh = lx.object.Mesh (layer_scan.MeshEdit(n))

            if not mesh.test ():
                continue

            polygon_count = mesh.PolygonCount ()
            if polygon_count == 0:
                continue

            polygon_accessor = lx.object.Polygon (mesh.PolygonAccessor ())
            if not polygon_accessor.test ():
                continue

            visitor = PolyTaggerClass (polygon_accessor, mark_mode_valid, i_POLYTAG)
            polygon_accessor.Enumerate (mark_mode_valid, visitor, 0)

            layer_scan.SetMeshChange (n, lx.symbol.f_MESHEDIT_POL_TAGS)

        if scope == tagger.SCOPE_SCENE:
            lx.eval("select.drop item")
            modo.Scene().meshes[0].select()

        layer_scan.Apply ()

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


lx.bless(CommandClass, CMD_NAME)
