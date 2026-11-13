import FreeCAD as App, Part
V = App.Vector
W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/"
YC, ZC = 0.0, 110.0           # thrust axis (aircraft frame), runs along X (forward = -X)
XR, XF, XRING = 0.0, -4.0, -12.0   # rear face (on pod), motor face, forward limit of the standoff ring
PODB = [(sy * 15.5563, ZC + sz * 15.5563) for sy in (-1, 1) for sz in (-1, 1)]   # pod bolts (Y,Z)
MOTB = [(sy * 9.5, ZC + sz * 8.0) for sy in (-1, 1) for sz in (-1, 1)]           # motor bolts (Y,Z)

def cylx(r, y, z, x0, x1):
    return Part.makeCylinder(r, abs(x1 - x0), V(min(x0, x1), y, z), V(1, 0, 0))

def space():
    s = cylx(25, YC, ZC, XF, XR)
    ring = cylx(25, YC, ZC, XRING, XF).cut(cylx(18.5, YC, ZC, XRING, XF))
    s = s.fuse(ring)
    for y, z in PODB:
        s = s.cut(cylx(1.7, y, z, XRING - 1, XR + 1))
        s = s.cut(cylx(3.2, y, z, XRING - 1, XF - 0.01))     # driver / head clearance in front of the plate
    for y, z in MOTB:
        s = s.cut(cylx(1.7, y, z, XRING - 1, XR + 1))
    return s.removeSplitter()

s = space()
print("valid", s.isValid(), "vol", s.Volume, s.BoundBox)
s.exportBrep(W + "motor_space.brep")
