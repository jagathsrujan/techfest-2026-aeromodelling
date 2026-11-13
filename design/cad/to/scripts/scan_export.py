"""Step 1 of the clash scan: open the saved FCStd, walk the Assembly tree, export every leaf part in assembled
position to BREP + index.json (each part exactly once)."""
import sys, os, json
import FreeCAD as App
fcstd, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
doc = App.openDocument(fcstd)
asm = doc.getObject("Assembly")
idx = {}
def leaf(o):
    return o.isDerivedFrom("Part::Feature") or o.TypeId == "PartDesign::Body"
def add(name, shape):
    if shape.isNull() or shape.Volume < 1e-6:
        return
    base = name; k = 1
    while name in idx:
        k += 1; name = "%s#%d" % (base, k)
    fn = os.path.join(outdir, name.replace("/", "_") + ".brep")
    shape.exportBrep(fn)
    bb = shape.BoundBox
    idx[name] = dict(file=fn, bb=[bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax], vol=shape.Volume)
def walk(container, base):
    """container: App::Part (or linked part); base: placement of its local frame in the aircraft frame"""
    for c in container.Group:
        if c.TypeId == "App::Link":
            lo = c.LinkedObject
            pl = base.multiply(c.Placement)
            if lo is None:
                continue
            if lo.TypeId == "App::Part" or hasattr(lo, "Group") and not leaf(lo):
                walk(lo, pl)
            elif leaf(lo):
                s = c.Shape.copy()
                s.Placement = base.multiply(s.Placement)
                add(c.Name, s)
        elif c.TypeId in ("App::Part",):
            walk(c, base.multiply(c.Placement))
walk(asm, App.Placement())
json.dump(idx, open(os.path.join(outdir, "index.json"), "w"))
print("exported", len(idx), "total volume", round(sum(v["vol"] for v in idx.values())))
