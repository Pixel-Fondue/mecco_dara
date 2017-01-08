# python

import lx, lxu.command, lxifc, modo, traceback, tagger

def flood_select(i_POLYTAG):
    layer_svc = lx.service.Layer ()
    layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_ACTIVE | lx.symbol.f_LAYERSCAN_MARKPOLYS))
    if not layer_scan.test ():
        return

    sel_svc = lx.service.Selection ()
    polygon_pkts = []

    mesh_svc = lx.service.Mesh()
    mark_mode_selected = mesh_svc.ModeCompose (lx.symbol.sMARK_SELECT, None)
    mark_mode_valid = mesh_svc.ModeCompose (None, 'hide lock')

    for n in xrange (layer_scan.Count ()):
        mesh = lx.object.Mesh (layer_scan.MeshBase (n))
        if not mesh.test ():
            continue

        polygon_count = mesh.PolygonCount ()
        if polygon_count == 0:
            continue

        polygon = lx.object.Polygon (mesh.PolygonAccessor ())
        if not polygon.test ():
            continue

        edge = lx.object.Edge (mesh.EdgeAccessor ())
        if not edge.test ():
            continue

        visitor = tagger.PolysConnectedByTag (polygon, edge, mark_mode_valid, i_POLYTAG)
        polygon.Enumerate (mark_mode_selected, visitor, 0)

        sel_type_polygon = sel_svc.LookupType (lx.symbol.sSELTYP_POLYGON)
        sel_svc.Drop (sel_type_polygon)
        poly_pkt_trans = lx.object.PolygonPacketTranslation (sel_svc.Allocate (lx.symbol.sSELTYP_POLYGON))
        sel_svc.StartBatch ()
        for polygonID in visitor.getPolyIDs ():
            sel_svc.Select (sel_type_polygon, poly_pkt_trans.Packet (polygonID, mesh))
        sel_svc.EndBatch ()

    layer_scan.Apply ()


class FloodMaterialCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        flood_select(lx.symbol.i_POLYTAG_MATERIAL)


class FloodPartCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        flood_select(lx.symbol.i_POLYTAG_PART)


class FloodSetCommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        flood_select(lx.symbol.i_POLYTAG_PICK)


lx.bless(FloodMaterialCommandClass, tagger.CMD_FLOOD_SELECT_MATERIAL)
lx.bless(FloodPartCommandClass, tagger.CMD_FLOOD_SELECT_PART)
lx.bless(FloodSetCommandClass, tagger.CMD_FLOOD_SELECT_SET)
