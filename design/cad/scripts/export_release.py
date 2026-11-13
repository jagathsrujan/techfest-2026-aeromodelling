"""Export the manufacturing release of one revision (env REV, default J; REV=H for the cargo version).

Run headless:  freecadcmd design/cad/scripts/export_release.py
Writes design/cad/release_revH/:
  printed/   one STEP + STL per 3D-printed part (part's own frame)
  laser/     one STEP per laser-cut part (nested DXF sheets are in ../laser_dxf)
  carbon/    cut_list.csv for carbon tubes/rods and other cut stock
  assembly/  full-aircraft STEP (every part in flight position)
  BOM_revH_release.csv   masses recomputed from the current solids
  release_report.txt     checks (validity, envelope, mass, CG)
"""
import csv, os, sys, time
import FreeCAD, Part, MeshPart

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
CAD = os.path.dirname(HERE)
REV = os.environ.get("REV", "J")
SRC = os.path.join(CAD, "TechfestPlane_rev%s.FCStd" % REV)
OUT = os.path.join(CAD, "release_rev%s" % REV)
for d in ("printed", "laser", "carbon", "assembly"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

rep = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); sys.stdout.flush(); rep.append(s)

doc = FreeCAD.openDocument(SRC)
bodies = {o.Label: o for o in doc.Objects if o.TypeId == "PartDesign::Body"}
rows = list(csv.DictReader(open(os.path.join(CAD, "rev%s_BOM.csv" % REV))))
old_total = float([r for r in rows if r["part"].startswith("TOTAL")][0]["total_mass_g"])
old_cg = {r["part"]: float(r["total_mass_g"]) for r in rows if r["part"].startswith("CG_")}

# ---- global positions of every leaf body (through links / sub-assemblies)
asm = [o for o in doc.Objects if o.TypeId == "Assembly::AssemblyObject"][0]
leaves = []  # (body label, global matrix)
def walk(obj, mat, depth=0):
    for name in obj.getSubObjects():
        r = obj.getSubObject(name, retType=1, matrix=mat)
        if not r or r[0] is None:
            continue
        sobj, m = r
        lo, lm = sobj.getLinkedObject(True, m, False)
        if lo.TypeId == "PartDesign::Body":
            leaves.append((lo.Label, lm))
        elif lo.TypeId in ("App::Part", "Assembly::AssemblyObject", "App::LinkGroup") or lo.isDerivedFrom("App::Part"):
            walk(lo, lm, depth + 1)
walk(asm, FreeCAD.Matrix())
say("leaf bodies placed in assembly:", len(leaves))

def gshape(label, m):
    s = bodies[label].Shape.copy()
    # body.Shape already carries the body's own Placement; lm from the walk includes it too
    s.Placement = FreeCAD.Placement()
    s = s.transformed(m)
    return s

placed = [(l, gshape(l, m)) for l, m in leaves]
comp = Part.makeCompound([s for _, s in placed])
bb = comp.BoundBox
say("walker envelope  X %.1f..%.1f  Y %.1f..%.1f  Z %.1f..%.1f" % (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax))
ref = Part.getShape(asm).BoundBox
say("Part.getShape    X %.1f..%.1f  Y %.1f..%.1f  Z %.1f..%.1f" % (ref.XMin, ref.XMax, ref.YMin, ref.YMax, ref.ZMin, ref.ZMax))
say("SPAN (Y extent) = %.2f mm  (rule: <= 1200)" % bb.YLength)

# ---- BOM refresh: volumes from the live solids, mass = volume * density
count = {}
for l, _ in leaves:
    count[l] = count.get(l, 0) + 1
new_rows, dM, dMx, dMy, dMz = [], 0.0, 0.0, 0.0, 0.0
def com(label):
    ss = [so for l, s in placed if l == label for so in s.Solids]
    v = sum(s.Volume for s in ss)
    c = FreeCAD.Vector()
    for s in ss:
        c += s.CenterOfMass * (s.Volume / v)
    return c
for r in rows:
    p = r["part"]
    if p.startswith("TOTAL") or p.startswith("CG_"):
        continue
    r = dict(r)
    b = bodies.get(p)
    if b is not None and float(r["density"]) > 0:
        v_old, v_new = float(r["unit_volume_mm3"]), b.Shape.Volume
        if abs(v_new - v_old) / max(v_old, 1) > 0.003:
            q = int(r["qty"]); rho = float(r["density"])
            m_old = float(r["total_mass_g"]); m_new = v_new * rho / 1000 * q
            c = com(p) if p in count else None
            say("CHANGED %-16s V %.0f -> %.0f mm3, mass %.2f -> %.2f g" % (p, v_old, v_new, m_old, m_new))
            r["unit_volume_mm3"] = round(v_new, 1); r["unit_mass_g"] = round(v_new * rho / 1000, 3); r["total_mass_g"] = round(m_new, 3)
            if c is not None:
                dM += m_new - m_old; dMx += (m_new - m_old) * c.x; dMy += (m_new - m_old) * c.y; dMz += (m_new - m_old) * c.z
    new_rows.append(r)
# link counts vs BOM quantities (information only)
for r in new_rows:
    if r["part"] in count and r["make"] != "buy" and count[r["part"]] != int(r["qty"]):
        say("NOTE qty differs for", r["part"], "BOM", r["qty"], "model", count[r["part"]])
total = sum(float(r["total_mass_g"]) for r in new_rows)
cgx = (old_total * old_cg["CG_X_mm"] + dMx) / (old_total + dM)
cgy = (old_total * old_cg["CG_Y_mm"] + dMy) / (old_total + dM)
cgz = (old_total * old_cg["CG_Z_mm"] + dMz) / (old_total + dM)
say("EMPTY MASS %.1f g (was %.1f)  rule: <= 1000" % (total, old_total))
say("CG X %.1f (was %.1f)  Y %.1f  Z %.1f" % (cgx, old_cg["CG_X_mm"], cgy, cgz))
with open(os.path.join(OUT, "BOM_rev%s_release.csv" % REV), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(new_rows)
    blank = {k: "" for k in rows[0].keys()}
    for k, v in (("TOTAL EMPTY (no payload)", round(total, 2)), ("CG_X_mm", round(cgx, 1)), ("CG_Y_mm", round(cgy, 1)), ("CG_Z_mm", round(cgz, 1))):
        w.writerow(dict(blank, part=k, total_mass_g=v))

# ---- per-part files
cut = []
STOCK = {"Spine": "CF tube OD 14 / ID 12", "Spar_Front": "CF tube OD 8 / ID 6", "Spar_Rear": "CF rod/tube OD 4",
         "Pushrod_Ele": "CF rod OD 2 (length = straight run inside the spine)", "Pushrod_Rud": "CF rod OD 2 (length = straight run inside the spine)",
         "Pushrod_AilR": "CF rod OD 2 (overall length incl. end bends)", "Pushrod_AilL": "CF rod OD 2 (overall length incl. end bends)",
         "BellySkid": "polycarbonate sheet 1 mm, 98 x 40"}
BED = (325, 320, 325)
for r in new_rows:
    p, make = r["part"], r["make"]
    b = bodies.get(p)
    if b is None or make == "buy":
        continue
    s = b.Shape
    ok = s.isValid() and len(s.Solids) >= 1
    d = sorted([s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength])
    if make == "print":
        s.exportStep(os.path.join(OUT, "printed", p + ".step"))
        MeshPart.meshFromShape(Shape=s, LinearDeflection=0.05, AngularDeflection=0.35, Relative=False).write(os.path.join(OUT, "printed", p + ".stl"))
        fits = all(a <= b_ for a, b_ in zip(d, sorted(BED)))
        say("PRINT %-18s x%s %-16s valid %s  %.0fx%.0fx%.0f  %.1f g  fits_bed %s" % (p, r["qty"], r["material"], ok, d[2], d[1], d[0], float(r["unit_mass_g"]), fits))
    elif make == "laser":
        s.exportStep(os.path.join(OUT, "laser", p + ".step"))
        say("LASER %-18s x%s %-16s valid %s  %.0fx%.0fx%.1f" % (p, r["qty"], r["material"], ok, d[2], d[1], d[0]))
    elif make == "cut":
        stock = STOCK.get(p, "%.1f x %.1f" % (d[1], d[0]))
        cut.append({"part": p, "qty": r["qty"], "material": r["material"], "length_mm": round(d[2], 1),
                    "stock": stock, "unit_mass_g": r["unit_mass_g"]})
        say("CUT   %-18s x%s %-16s L %.1f  section %.1f x %.1f" % (p, r["qty"], r["material"], d[2], d[1], d[0]))
with open(os.path.join(OUT, "carbon", "cut_list.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cut[0].keys())); w.writeheader(); w.writerows(cut)

# ---- assembly STEP (flat compound, every part in flight position)
t = time.time()
comp.exportStep(os.path.join(OUT, "assembly", "TechfestPlane_rev%s_assembly.step" % REV))
say("assembly STEP written, %d solids, %.0f s" % (len(comp.Solids), time.time() - t))
open(os.path.join(OUT, "release_report.txt"), "w").write("\n".join(rep) + "\n")
print("DONE")
