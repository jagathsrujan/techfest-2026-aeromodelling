"""Rev J: remove the golf-ball cargo system and replace the hopper with a plain fuselage.

Run inside the FreeCAD GUI with TechfestPlane_revH.FCStd open and active:
    exec(open(".../design/cad/scripts/build_revJ.py").read())
It saves the result as TechfestPlane_revJ.FCStd (rev H on disk is not touched) and writes revJ_BOM.csv.

Fuselage geometry (aircraft frame, mm): a 0.6 mm LW-PLA box shell, 60 wide, under the spine.
Side profile X,Z: (104,134) (138.4,70) (280,70) (424,128) (424,134); plan taper 60 -> 20 wide from X 280 to 424.
It reuses the hopper's front wall plane (nose pod mate) and the two spine saddles with their insert pockets,
so the nose pod, wing clamps, spine and servo mounts bolt on exactly as in rev H.
"""
import csv, os, math
import FreeCAD, Part
V = FreeCAD.Vector
doc = FreeCAD.ActiveDocument
assert doc.Name == "TechfestPlane_revH", doc.Name
CAD = os.path.dirname(doc.FileName)
asm = doc.getObject("Assembly")
hop = doc.getObject("Hopper")
old = hop.Shape.copy()

# ---------------- masses / positions of what is removed (for the BOM and CG)
bom = list(csv.DictReader(open(os.path.join(CAD, "release_revH", "BOM_revH_release.csv"))))
unit = {}
for r in bom:
    if r["unit_mass_g"] not in ("", None) and r["part"] not in unit:
        unit[r["part"]] = float(r["unit_mass_g"])
M0 = float([r for r in bom if r["part"].startswith("TOTAL")][0]["total_mass_g"])
CG0 = V(*[float([r for r in bom if r["part"] == k][0]["total_mass_g"]) for k in ("CG_X_mm", "CG_Y_mm", "CG_Z_mm")])
def com(s):
    v = sum(x.Volume for x in s.Solids); c = V()
    for x in s.Solids: c += x.CenterOfMass * (x.Volume / v)
    return c
REMOVE_ASSY = ["A_ChuteAssy", "A_GateUnit_R", "A_GateUnit_L", "A_LidUnit_R", "A_LidUnit_L", "A_GateServoAssy",
               "A_LidServoAssy", "A_FairingAssy", "A_FairingTailAssy"]
REMOVE_CHILD = [("A_HopperAssy", "L_I_ChuteHopper_0"), ("A_HopperAssy", "L_I_ChuteHopper_1"),
                ("A_NoseAssy", "L_I_Fair_P"), ("A_NoseAssy", "L_I_Fair_N")]
removed = []  # (label, mass, com)
def note(a, child):
    lab = child.getLinkedObject(True).Label
    s = asm.getSubObject("%s.%s." % (a, child.Name), retType=0)
    removed.append((lab, unit[lab], com(s)))
for a in REMOVE_ASSY:
    for c in doc.getObject(a).LinkedObject.Group:
        if c.TypeId == "App::Link": note(a, c)
for a, c in REMOVE_CHILD:
    note(a, doc.getObject(c))
hop_old_m = unit["Hopper"]; hop_old_c = com(asm.getSubObject("A_HopperAssy.L_Hopper.", retType=0))
print("removed items:", len(removed), "mass %.1f g" % sum(m for _, m, _ in removed))

# ---------------- new fuselage solid
T = 0.6
XF_TOP, XF_BOT, ZTOP = 104.0, 176.0, 134.0          # hopper front wall line (kept: nose pod mates to it)
ZB, X_TAPER, X_END, Z_END, HW, HW_END = 70.0, 280.0, 424.0, 128.0, 30.0, 10.0
S = 4000.0
def half(n, p):
    """solid filling the half-space on the +n side of the plane through p"""
    n = V(n); n.normalize()
    b = Part.makeBox(S, S, S, V(-S / 2, -S / 2, 0))
    b.Placement = FreeCAD.Placement(V(p), FreeCAD.Rotation(V(0, 0, 1), n))
    return b
a_f = V(XF_BOT - XF_TOP, 0, -ZTOP)                    # direction down the front wall
n_front = V(-ZTOP, 0, -(XF_BOT - XF_TOP))             # outward (forward/down) normal of the front wall
a_r = V(X_END - X_TAPER, 0, Z_END - ZB); n_rear = V(a_r.z, 0, -a_r.x)
PLANES = [(n_front, V(XF_TOP, 0, ZTOP)), (V(0, 0, -1), V(0, 0, ZB)), (n_rear, V(X_TAPER, 0, ZB)),
          (V(0, 0, 1), V(0, 0, ZTOP)), (V(1, 0, 0), V(X_END, 0, 0)),
          (V(0, 1, 0), V(0, HW, 0)), (V(0, -1, 0), V(0, -HW, 0)),
          (V(HW - HW_END, X_END - X_TAPER, 0), V(X_TAPER, HW, 0)), (V(HW - HW_END, -(X_END - X_TAPER), 0), V(X_TAPER, -HW, 0))]
def hull(d, skip=()):
    s = Part.makeBox(600, 200, 300, V(0, -100, -50))
    for i, (n, p) in enumerate(PLANES):
        nn = V(n); nn.normalize()
        s = s.cut(half(nn, V(p) - nn * (0 if i in skip else d)))
    return s
O = hull(0.0)
shell = O.cut(hull(T))
pieces = [shell]
# ring frames under the two wing saddles and one mid-way: carry wing and landing loads round the section
for xf in (237.0, 287.5, 338.0):
    slab = Part.makeBox(1.2, 200, 300, V(xf - 0.6, -100, -50))
    pieces.append(O.common(slab).cut(hull(7.0)))
# deck doublers under the saddles
for x0, x1 in ((218.0, 256.0), (327.0, 349.0)):
    pieces.append(O.common(Part.makeBox(x1 - x0, 36, 2.4, V(x0, -18, ZTOP - 2.4))))
# the two spine saddles of the hopper, with half-bores and insert pockets, taken unchanged
for x0, x1 in ((221.0, 253.0), (330.0, 346.0)):
    pieces.append(old.common(Part.makeBox(x1 - x0, 31, 8.9, V(x0, -15.5, ZTOP - 0.61))))
fus = pieces[0]
for p in pieces[1:]:
    fus = fus.fuse(p)
# pod bolt pass-holes: whatever the hopper front wall had open inside the new wall, open here too
nn = V(n_front); nn.normalize()
wall = O.common(half(nn, V(XF_TOP, 0, ZTOP) - nn * T))
plugs = wall.cut(old)
print("front-wall openings copied: %.1f mm3 in %d pieces" % (plugs.Volume, len(plugs.Solids)),
      [(round(s.BoundBox.Center.y, 1), round(s.BoundBox.Center.z, 1), round(s.Volume, 1)) for s in plugs.Solids])
holes = [s for s in plugs.Solids if s.Volume < 40]
for h in holes:
    fus = fus.cut(h)
fus = fus.removeSplitter()
assert fus.isValid() and len(fus.Solids) == 1, (fus.isValid(), len(fus.Solids))
bb = fus.BoundBox
print("FUSELAGE V %.0f mm3 = %.1f g  X %.1f..%.1f Y %.1f..%.1f Z %.1f..%.1f" % (fus.Volume, fus.Volume * 0.55 / 1000, bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax))

# ---------------- become rev J
doc.saveAs(os.path.join(CAD, "TechfestPlane_revJ.FCStd"))
# joints that reference removed sub-assemblies
rm_set = set(REMOVE_ASSY)
jg = [o for o in asm.Group if o.TypeId == "Assembly::JointGroup"][0]
for j in list(jg.Group):
    refs = [getattr(j, a)[0].Name for a in ("Reference1", "Reference2") if hasattr(j, a) and getattr(j, a) and getattr(j, a)[0]]
    if any(r in rm_set for r in refs):
        print("delete joint", j.Label); doc.removeObject(j.Name)
def drop_link(l):
    doc.removeObject(l.Name)
bodies_maybe = set()
for a in REMOVE_ASSY:
    A = doc.getObject(a); part = A.LinkedObject
    doc.removeObject(a)
    for c in list(part.Group):
        if c.TypeId == "App::Link":
            bodies_maybe.add(c.getLinkedObject(True).Name); drop_link(c)
    try: part.removeObjectsFromDocument()
    except Exception: pass
    doc.removeObject(part.Name)
for a, c in REMOVE_CHILD:
    drop_link(doc.getObject(c))
for bn in sorted(bodies_maybe):
    b = doc.getObject(bn)
    if b is None or b.TypeId != "PartDesign::Body": continue
    users = [u.Name for u in b.InList if u.TypeId == "App::Link"]
    if users: continue
    try:
        b.removeObjectsFromDocument(); doc.removeObject(bn); print("deleted body", bn)
    except Exception as e:
        print("could not delete body", bn, e)

# hopper body -> fuselage body (same object, same mating LCSs, new solid)
src = doc.addObject("Part::Feature", "Fuselage_src"); src.Shape = fus; src.ViewObject.Visibility = False
keep_lcs = ("LCS_saddle_f", "LCS_saddle_r", "LCS_pod", "LCS_skid")
for o in list(hop.Group):
    if o.TypeId == "PartDesign::CoordinateSystem":
        if o.Name in keep_lcs:
            pl = o.Placement; print("keep", o.Name, "support", [(s[0].Name) for s in (o.AttachmentSupport or [])], o.MapMode)
        else:
            doc.removeObject(o.Name)
feats = [o for o in hop.Group if o.TypeId != "PartDesign::CoordinateSystem" and not o.isDerivedFrom("App::Origin")]
fb = hop.newObject("PartDesign::FeatureBase", "FuselageBase")
fb.BaseFeature = src
hop.Tip = fb
for o in reversed(feats):
    try: doc.removeObject(o.Name)
    except Exception as e: print("keep feature", o.Name, e)
hop.Label = "Fuselage"
fb.ViewObject.Visibility = True
fb.ViewObject.ShapeColor = (0.35, 0.55, 0.85)
# belly skid follows the new bottom
sk = doc.getObject("L_BellySkid")
sk.setExpression("Placement", None) if "Placement" in [e[0] for e in sk.ExpressionEngine] else None
for e in list(sk.ExpressionEngine):
    sk.setExpression(e[0], None)
p = sk.Placement; p.Base = p.Base + V(0, 0, ZB); sk.Placement = p
n = doc.recompute()
print("recompute", n, "fuselage body V %.0f valid %s" % (hop.Shape.Volume, hop.Shape.isValid()))
print("solve", asm.solve())
print("errors", [o.Name for o in doc.Objects if "Invalid" in o.State or "Error" in o.State])

# ---------------- rev J baseline BOM (mass and CG by difference from rev H)
fus_m = hop.Shape.Volume * 0.55 / 1000
fus_c = com(asm.getSubObject("A_HopperAssy.L_Hopper.", retType=0))
dM = fus_m - hop_old_m - sum(m for _, m, _ in removed)
mom = CG0 * M0 + fus_c * fus_m - hop_old_c * hop_old_m
for _, m, c in removed: mom = mom - c * m
cnt = {}
for l, _, _ in removed: cnt[l] = cnt.get(l, 0) + 1
rows = []
for r in bom:
    p = r["part"]
    if p.startswith("TOTAL") or p.startswith("CG_"): continue
    r = dict(r)
    if p == "Hopper":
        r.update(part="Fuselage", unit_volume_mm3=round(hop.Shape.Volume, 1), unit_mass_g=round(fus_m, 3), total_mass_g=round(fus_m, 3))
    elif cnt.get(p):
        q = int(r["qty"]) - cnt.pop(p)
        if q <= 0: continue
        r["qty"] = q; r["total_mass_g"] = round(q * float(r["unit_mass_g"]), 3)
    rows.append(r)
total = sum(float(r["total_mass_g"]) for r in rows)
cg = mom * (1.0 / (M0 + dM))
print("leftover removed counts (should be empty):", cnt)
print("REV J EMPTY MASS %.1f g (sum of rows) / %.1f g (by difference)   CG X %.1f Y %.1f Z %.1f" % (total, M0 + dM, cg.x, cg.y, cg.z))
with open(os.path.join(CAD, "revJ_BOM.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(bom[0].keys())); w.writeheader(); w.writerows(rows)
    blank = {k: "" for k in bom[0].keys()}
    for k, v in (("TOTAL EMPTY (no payload)", round(total, 2)), ("CG_X_mm", round(cg.x, 1)), ("CG_Y_mm", round(cg.y, 1)), ("CG_Z_mm", round(cg.z, 1))):
        w.writerow(dict(blank, part=k, total_mass_g=v))
doc.save()
print("SAVED", doc.FileName)
