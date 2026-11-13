"""WingClampCap_F design space (aircraft frame). Run with freecadcmd/execute_code_headless."""
import FreeCAD as App, Part
V = App.Vector
W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/"

X0, ZS = 237.0, 142.0              # clamp station, spine axis height
SPAR = (237.8074, 176.2220)        # front spar axis (x,z); runs along Y
BX = (X0 - 10.0, X0 + 10.0)        # clamp bolt x (moved clear of the spar footprint 233.8..241.8)
BY = (-11.0, 11.0)
XB = X0 - 8.2                      # cross bolt x
ZSEAT, ZTOP_FL = 156.6, 160.0
ZXB = ZS + 21.8                    # cross-bolt head seat

def cyl(r, p, d, L):
    return Part.makeCylinder(r, L, V(*p), V(*d))

def space():
    b1 = Part.makeBox(29.0, 33.0, 18.0, V(X0 - 14.5, -16.5, ZS))
    b2 = Part.makeBox(15.0, 33.0, 23.8, V(X0 - 7.5, -16.5, ZS + 18.0))
    s = b1.fuse(b2)
    s = s.cut(cyl(7.075, (X0 - 20, 0, ZS), (1, 0, 0), 40))                       # spine bore
    s = s.cut(cyl(4.075, (SPAR[0], -20, SPAR[1]), (0, 1, 0), 40))                # spar bore
    for bx in BX:
        for by in BY:
            s = s.cut(cyl(1.7, (bx, by, ZS - 1), (0, 0, 1), 30))                 # clamp bolt holes
            s = s.cut(cyl(3.1, (bx, by, ZSEAT), (0, 0, 1), 10))                  # head counterbores
    s = s.cut(cyl(1.7, (XB, 0, ZS), (0, 0, 1), 30))                              # cross-bolt clearance (through)
    s = s.cut(cyl(2.0, (XB, 0, ZS + 6.7), (0, 0, 1), 6.2))                       # insert pocket
    s = s.cut(cyl(2.5, (XB, 0, ZXB), (0, 0, 1), 30))                             # driver access channel
    return s.removeSplitter()

if __name__ == "__main__":
    s = space()
    print("valid", s.isValid(), "vol", s.Volume, s.BoundBox)
    s.exportBrep(W + "clamp_space.brep")
