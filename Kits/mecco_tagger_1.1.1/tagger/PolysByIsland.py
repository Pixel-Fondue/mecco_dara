# python

# Adapted from James O'Hare's excellent code: https://gist.github.com/Farfarer/31148a78f392a831239d9b018b90330c

import lx, lxu.command, lxifc

class SetMarks (lxifc.Visitor):
    def __init__ (self, acc, mark):
        self.acc = acc
        self.mark = mark

    def vis_Evaluate (self):
        self.acc.SetMarks (self.mark)

class PolysByIsland (lxifc.Visitor):
    def __init__ (self, polygon, point, mark):
        self.polygon = polygon
        self.point = point
        self.mark = mark
        self.islands = []

    def vis_Evaluate (self):
        inner = set ()
        outer = set ()

        outer.add (self.polygon.ID ())

        while len(outer) > 0:
            polygon_ID = outer.pop ()

            self.polygon.Select (polygon_ID)
            self.polygon.SetMarks (self.mark)
            inner.add (polygon_ID)

            num_points = self.polygon.VertexCount ()
            for v in xrange (num_points):
                self.point.Select (self.polygon.VertexByIndex (v))
                num_polys = self.point.PolygonCount ()
                for p in xrange (num_polys):
                    vert_polygon_ID = self.point.PolygonByIndex (p)
                    if vert_polygon_ID not in inner:
                        outer.add (vert_polygon_ID)
        self.islands.append (inner)
