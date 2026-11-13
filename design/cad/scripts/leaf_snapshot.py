"""Record every leaf part of the assembly (label, volume, global centre of mass) and compare snapshots.

    SNAP=before freecadcmd design/cad/scripts/leaf_snapshot.py     # writes to/work/snap_before.json
    SNAP=after  freecadcmd design/cad/scripts/leaf_snapshot.py     # writes snap_after.json and prints the diff vs before
Env REV picks the model (default J).  All prints are prefixed SNAPSHOT.
"""
import json, os
import FreeCAD
CAD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REV = os.environ.get("REV", "J"); TAG = os.environ.get("SNAP", "after")
WORK = os.path.join(CAD, "to", "work"); os.makedirs(WORK, exist_ok=True)
def P(*a): print("SNAPSHOT", *a, flush=True)
doc = FreeCAD.openDocument(os.path.join(CAD, "TechfestPlane_rev%s.FCStd" % REV))
asm = [o for o in doc.Objects if o.TypeId == "Assembly::AssemblyObject"][0]
leaves = []
def walk(obj, mat):
    for name in obj.getSubObjects():
        r = obj.getSubObject(name, retType=1, matrix=mat)
        if not r or r[0] is None: continue
        sobj, m = r
        lo, lm = sobj.getLinkedObject(True, m, False)
        if lo.TypeId == "PartDesign::Body" or lo.TypeId == "Part::Feature":
            s = lo.Shape.copy(); s.Placement = FreeCAD.Placement(); s = s.transformed(lm)
            if not s.Solids: continue
            v = sum(x.Volume for x in s.Solids); c = FreeCAD.Vector()
            for x in s.Solids: c += x.CenterOfMass * (x.Volume / v)
            leaves.append([lo.Label, round(v, 2), round(c.x, 3), round(c.y, 3), round(c.z, 3)])
        elif lo.isDerivedFrom("App::Part"): walk(lo, lm)
walk(asm, FreeCAD.Matrix())
leaves.sort()
json.dump(leaves, open(os.path.join(WORK, "snap_%s.json" % TAG), "w"))
P(TAG, "leaves:", len(leaves), "objects in document:", len(doc.Objects), "solve:", asm.solve())
ref = os.path.join(WORK, "snap_before.json")
if TAG != "before" and os.path.exists(ref):
    old = json.load(open(ref)); bad = 0; used = [False] * len(leaves)
    for o in old:
        best = None
        for i, n in enumerate(leaves):
            if used[i] or n[0] != o[0]: continue
            d = max(abs(n[2] - o[2]), abs(n[3] - o[3]), abs(n[4] - o[4]))
            if best is None or d < best[0]: best = (d, i)
        if best is None: P("MISSING", o); bad += 1; continue
        used[best[1]] = True
        if best[0] > 0.01 or abs(leaves[best[1]][1] - o[1]) > 0.1:
            P("MOVED/CHANGED", o, "->", leaves[best[1]]); bad += 1
    for i, n in enumerate(leaves):
        if not used[i]: P("EXTRA", n); bad += 1
    P("compare with before: %d leaves before, %d now, %d differences -> %s" % (len(old), len(leaves), bad, "PASS" if bad == 0 else "FAIL"))
