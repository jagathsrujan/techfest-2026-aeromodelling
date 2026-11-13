import FreeCAD as App, Part
V = App.Vector
W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/"
ZS = 142.0
XA, XB = 780.0, 946.0
PINCH = (805.0, 865.0)
def cylx(r, x0, x1, y=0, z=ZS): return Part.makeCylinder(r, x1 - x0, V(x0, y, z), V(1, 0, 0))
def cylz(r, x, y, z0, z1): return Part.makeCylinder(r, z1 - z0, V(x, y, z0), V(0, 0, 1))
def space():
    s = Part.makeBox(XB - XA, 22, 150 - 131, V(XA, -11, 131))                 # sleeve envelope
    s = s.fuse(Part.makeBox(20, 11, 3, V(825, -5.5, 150)))                    # fin tower
    s = s.fuse(Part.makeBox(21, 10, 11.5, V(925, -5, 119.5)))                 # skid (to Z 119.5 ... fused into sleeve)
    for px in PINCH:
        s = s.fuse(cylz(4.25, px, 0, 127.5, 135))                              # insert boss under the sleeve
    s = s.cut(cylx(7.075, XA - 1, XB + 1))                                    # spine bore
    s = s.cut(Part.makeBox(18, 3.2, 3, V(826, -1.6, 151)))                     # fin slot
    for px in PINCH:
        s = s.cut(cylz(1.7, px, 0, 126, 154))                                  # pinch bolt holes
    s = s.cut(Part.makeBox(28, 30, 13, V(872, -15, 134.5)))                    # rod exit window (kept open)
    return s.removeSplitter()
s = space(); print("valid", s.isValid(), "vol", s.Volume, s.BoundBox, len(s.Solids))
s.exportBrep(W + "tail_space.brep")
