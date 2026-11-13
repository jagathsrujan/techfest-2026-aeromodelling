"""Helpers to build fully-constrained PartDesign features from plain numbers (run inside FreeCAD)."""
import FreeCAD as App, Part, Sketcher
V = App.Vector


def plane(body, role):
    for f in body.Origin.OriginFeatures:
        if f.Role == role:
            return f
    raise KeyError(role)


def new_sketch(body, name, plane_role, offset=0.0):
    sk = body.newObject("Sketcher::SketchObject", name)
    sk.AttachmentSupport = [(plane(body, plane_role), "")]
    sk.MapMode = "FlatFace"
    sk.AttachmentOffset = App.Placement(V(0, 0, offset), App.Rotation())
    return sk


def _dim(sk, kind, a, pa, b, pb, val, name):
    if b is None:
        c = Sketcher.Constraint(kind, a, val)
    else:
        c = Sketcher.Constraint(kind, a, pa, b, pb, val)
    i = sk.addConstraint(c)
    if name:
        sk.renameConstraint(i, name)
    return i


def _pos(sk, gid, pid, axis, val, name):
    """lock coordinate of a point to val (distance from origin); zero -> PointOnObject on the axis."""
    if abs(val) < 1e-9:
        sk.addConstraint(Sketcher.Constraint("PointOnObject", gid, pid, -1 if axis == "y" else -2))
        return
    kind = "DistanceX" if axis == "x" else "DistanceY"
    _dim(sk, kind, -1, 1, gid, pid, val, name)


def add_rect(sk, x0, y0, x1, y1, tag):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    ids = [sk.addGeometry(Part.LineSegment(V(*pts[i], 0), V(*pts[(i + 1) % 4], 0)), False) for i in range(4)]
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint("Coincident", ids[i], 2, ids[(i + 1) % 4], 1))
    sk.addConstraint(Sketcher.Constraint("Horizontal", ids[0]))
    sk.addConstraint(Sketcher.Constraint("Horizontal", ids[2]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ids[1]))
    sk.addConstraint(Sketcher.Constraint("Vertical", ids[3]))
    _pos(sk, ids[0], 1, "x", x0, tag + "_x0")
    _pos(sk, ids[0], 1, "y", y0, tag + "_y0")
    _dim(sk, "DistanceX", ids[0], 1, ids[0], 2, x1 - x0, tag + "_w")
    _dim(sk, "DistanceY", ids[1], 1, ids[1], 2, y1 - y0, tag + "_h")
    return ids


def add_circle(sk, cx, cy, d, tag):
    g = sk.addGeometry(Part.Circle(V(cx, cy, 0), V(0, 0, 1), d / 2.0), False)
    _dim(sk, "Diameter", g, 0, None, 0, d, tag + "_d")
    _pos(sk, g, 3, "x", cx, tag + "_cx")
    _pos(sk, g, 3, "y", cy, tag + "_cy")
    return g


def add_poly(sk, pts, tag):
    n = len(pts)
    ids = [sk.addGeometry(Part.LineSegment(V(*pts[i], 0), V(*pts[(i + 1) % n], 0)), False) for i in range(n)]
    for i in range(n):
        sk.addConstraint(Sketcher.Constraint("Coincident", ids[i], 2, ids[(i + 1) % n], 1))
    for i, (p, q) in enumerate(zip(pts, pts[1:] + pts[:1])):
        if abs(p[1] - q[1]) < 1e-9:
            sk.addConstraint(Sketcher.Constraint("Horizontal", ids[i]))
        elif abs(p[0] - q[0]) < 1e-9:
            sk.addConstraint(Sketcher.Constraint("Vertical", ids[i]))
    for i, p in enumerate(pts):
        _pos(sk, ids[i], 1, "x", p[0], "%s_x%d" % (tag, i))
        _pos(sk, ids[i], 1, "y", p[1], "%s_y%d" % (tag, i))
    return ids


def check(sk):
    sk.recompute()
    r = sk.solve()
    try:
        dof = sk.solve()
    except Exception:
        dof = r
    fc = getattr(sk, "FullyConstrained", None)
    return r, len(sk.MalformedConstraints), fc


def pad(body, name, sk, length, mid=False, rev=False):
    f = body.newObject("PartDesign::Pad", name)
    f.Profile = sk
    f.Length = length
    f.Midplane = mid
    f.Reversed = rev
    f.Refine = True
    sk.Visibility = False
    return f


def pocket(body, name, sk, length=None, through=False, mid=False, rev=False):
    f = body.newObject("PartDesign::Pocket", name)
    f.Profile = sk
    if through:
        f.Type = 1
    else:
        f.Length = length
    f.Midplane = mid
    f.Reversed = rev
    f.Refine = True
    sk.Visibility = False
    return f
