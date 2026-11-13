import math
exec(open("/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/scripts/cadlib.py").read())
doc = App.getDocument("TechfestPlane_revH")
body = doc.getObject("MotorMount")
sp = doc.getObject("Params")
# parameters (rows >= 250)
newp = [("mmp_hub_r", HUB_R, "motor mount: hub radius"), ("mmp_hub_t", HUB_T, "motor mount: hub plate thickness"),
        ("mmp_spoke_w", SPOKE_W, "motor mount: spoke width"), ("mmp_pod_pad_d", 9.4, "pod bolt pad OD"),
        ("mmp_mot_pad_d", 8.0, "motor bolt pad OD"), ("mmp_zmax", 6.5, "pads built to here, trimmed by the tilted motor face")]
row = 269
for a, v, d in newp:
    try:
        sp.get(a)
        # existing alias: just update
        sp.set(sp.getCellFromAlias(a), str(v))
    except Exception:
        sp.set("A%d" % row, d); sp.set("B%d" % row, str(v)); sp.setAlias("B%d" % row, a); row += 1
doc.recompute()
P = lambda a: float(sp.get(a))

# remove old plate + the two trimming pockets (we re-create the pockets after the new pads)
for n in ["MotorHolesTilt", "MotorFaceCut", "Plate", "Sk_plate"]:
    o = body.getObject(n)
    if o: doc.removeObject(n)
for f in list(body.Group):
    if f.Name.startswith("Sk_pad") or f.Name.startswith("Sk_hub") or f.Name.startswith("Sk_spokes") or f.Name.startswith("Sk_podpads") or f.Name.startswith("Sk_motpads") or f.Name.startswith("Sk_podholes") or f.Name in ("Hub", "Spokes", "PodPads", "MotPads", "PodHoles"):
        doc.removeObject(f.Name)
doc.recompute()
solids = [f for f in body.Group if f.TypeId.startswith("PartDesign::") and f.TypeId in ("PartDesign::Pad", "PartDesign::Pocket")]
print("remaining solid features", [f.Name for f in solids])
if not solids:
    body.Tip = None

pb = P("mm_bc") / 2 / math.sqrt(2)          # pod bolt offset (15.556)
mx, my = P("mm_pat_x") / 2, P("mm_pat_y") / 2
hub_r, hub_t, sw = P("mmp_hub_r"), P("mmp_hub_t"), P("mmp_spoke_w")

sk = new_sketch(body, "Sk_hub", "XY_Plane", 0)
add_circle(sk, 0, 0, 2 * hub_r, "c"); sk.setExpression("Constraints.c_d", "2 * Params.mmp_hub_r")
f = pad(body, "Hub", sk, hub_t); f.setExpression("Length", "Params.mmp_hub_t")

sk = new_sketch(body, "Sk_spokes", "XY_Plane", 0)
for k, (sxx, syy) in enumerate([(1, 1), (-1, 1), (-1, -1), (1, -1)]):
    ux, uy = sxx / math.sqrt(2), syy / math.sqrt(2)
    nx, ny = -uy, ux
    s0, s1 = 9.5, math.hypot(pb, pb)
    pts = [(ux * s0 + nx * sw / 2, uy * s0 + ny * sw / 2), (ux * s1 + nx * sw / 2, uy * s1 + ny * sw / 2),
           (ux * s1 - nx * sw / 2, uy * s1 - ny * sw / 2), (ux * s0 - nx * sw / 2, uy * s0 - ny * sw / 2)]
    # polygon order must be consistent (counter-clockwise or not is fine for sketches)
    add_poly(sk, pts, "s%d" % k)
f = pad(body, "Spokes", sk, P("mm_t"))

sk = new_sketch(body, "Sk_podpads", "XY_Plane", 0)
k = 0
for sxx in (-1, 1):
    for syy in (-1, 1):
        add_circle(sk, sxx * pb, syy * pb, P("mmp_pod_pad_d"), "p%d" % k)
        sk.setExpression("Constraints.p%d_d" % k, "Params.mmp_pod_pad_d")
        k += 1
f = pad(body, "PodPads", sk, P("mmp_zmax")); f.setExpression("Length", "Params.mmp_zmax")

sk = new_sketch(body, "Sk_motpads", "XY_Plane", 0)
k = 0
for sxx in (-1, 1):
    for syy in (-1, 1):
        add_circle(sk, sxx * mx, syy * my, P("mmp_mot_pad_d"), "m%d" % k)
        sk.setExpression("Constraints.m%d_d" % k, "Params.mmp_mot_pad_d")
        k += 1
f = pad(body, "MotPads", sk, P("mmp_zmax")); f.setExpression("Length", "Params.mmp_zmax")

# re-create the two original pockets from their existing sketches
f1 = body.newObject("PartDesign::Pocket", "MotorFaceCut"); f1.Profile = body.getObject("Sk_motorface_cut"); f1.Type = 1; f1.Reversed = True; f1.Refine = True
f2 = body.newObject("PartDesign::Pocket", "MotorHolesTilt"); f2.Profile = body.getObject("Sk_motorholes_tilt"); f2.Type = 1; f2.Reversed = False; f2.Refine = True
sk = new_sketch(body, "Sk_podholes", "XY_Plane", 10)
k = 0
for sxx in (-1, 1):
    for syy in (-1, 1):
        add_circle(sk, sxx * pb, syy * pb, P("m3_clear"), "h%d" % k)
        sk.setExpression("Constraints.h%d_d" % k, "Params.m3_clear")
        k += 1
pocket(body, "PodHoles", sk, through=True, mid=True)
doc.recompute()
s = body.Shape
print("valid", s.isValid(), "vol", round(s.Volume, 1), "solids", len(s.Solids))
bad = []
for f in body.Group:
    if f.TypeId == "Sketcher::SketchObject":
        r = f.solve(); fc = getattr(f, "FullyConstrained", "n/a")
        if r != 0 or len(f.MalformedConstraints) or fc is not True: bad.append((f.Name, r, len(f.MalformedConstraints), fc))
print("sketch problems", bad)
g = doc.getObject("L_MotorMount").Shape
print("global bbox", g.BoundBox, round(g.Volume, 1))
