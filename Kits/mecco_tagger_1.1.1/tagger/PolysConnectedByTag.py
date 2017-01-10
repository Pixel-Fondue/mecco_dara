#!/usr/bin/env python

# Adapted from James O'Hare's excellent ffr_expandByMat.py code:
# https://gist.github.com/Farfarer/c42ebd249602542a7369b4fd205f4fb5

import lx
import lxu.command
import lxifc
import modo
import traceback

from debug import *

class PolysConnectedByTag (lxifc.Visitor):
    def __init__ (self, polygon, edge, mark_mode_valid, i_POLYTAG):
        self.polygon = polygon
        self.edge = edge
        self.mark_mode_valid = mark_mode_valid

        self.polygonIDs = set ()

        self.tag = lx.object.StringTag ()
        self.tag.set (self.polygon)

        self.i_POLYTAG = i_POLYTAG
        self.tagValues = None

    def reset (self):
        self.polygonIDs = set ()

    def getPolyIDs (self):
        return self.polygonIDs

    def vis_Evaluate (self):
        inner_list = set ()
        outer_list = set ()

        this_polygon_ID = self.polygon.ID ()

        if self.tagValues == None:
            tagValues = self.tag.Get (self.i_POLYTAG)
        else:
            tagValues = self.tagValues

        if not tagValues:
            tagValues = []

        if not isinstance(tagValues, list):
            tagValues = tagValues.split(";")

        if this_polygon_ID not in outer_list:
            outer_list.add (this_polygon_ID)

            while len(outer_list) > 0:
                polygon_ID = outer_list.pop ()

                self.polygon.Select (polygon_ID)
                inner_list.add (polygon_ID)

                num_points = self.polygon.VertexCount ()
                polygon_points = [self.polygon.VertexByIndex (p) for p in xrange (num_points)]

                for p in xrange (num_points):
                    self.edge.SelectEndpoints (polygon_points[p], polygon_points[(p+1)%num_points])
                    if self.edge.test ():
                        for e in xrange (self.edge.PolygonCount ()):
                            edge_polygon_ID = self.edge.PolygonByIndex (e)
                            if edge_polygon_ID != polygon_ID:
                                if edge_polygon_ID not in outer_list and edge_polygon_ID not in inner_list:
                                    self.polygon.Select (edge_polygon_ID)

                                    tagStrings = self.tag.Get(self.i_POLYTAG)
                                    if not tagStrings:
                                        tagStrings = set()
                                    elif tagStrings:
                                        tagStrings = set(tagStrings.split(";"))

                                    # debug("tagStrings: %s, tagValues: %s" % (str(tagStrings), str(tagValues)))

                                    if self.polygon.TestMarks (self.mark_mode_valid) and ((tagStrings.intersection(set(tagValues))) or tagStrings == set(tagValues)):
                                        outer_list.add (edge_polygon_ID)

        self.polygonIDs.update (inner_list)
