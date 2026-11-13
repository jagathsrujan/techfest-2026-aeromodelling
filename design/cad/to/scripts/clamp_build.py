exec(open("/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/scripts/cadlib.py").read())
doc = App.getDocument("TechfestPlane_revH")
body = doc.getObject("WingClampCap_F")
sp = doc.getObject("Params")
P = lambda a: float(sp.get(a))

# 1) remove old features (keep the LCS objects the assembly joints point to)
for f in reversed(list(body.Group)):
    if f.TypeId in ("Sketcher::SketchObject", "PartDesign::Pad", "PartDesign::Pocket"):
        doc.removeObject(f.Name)
doc.recompute()
keep = [f.Name for f in body.Group]
print("kept", keep)

bx, by = P("cap_bx"), P("cap_by")
sx = P("spar_f_ax") - P("sad_x1")          # spar axis x in cap frame (0.807)
sz = P("spar_f_az") - P("spine_z")         # spar axis z in cap frame (34.222)
ring_od, ylen = P("cap_ring_od"), P("cap_ylen")
pt, pyc = P("cap_plate_t"), P("cap_plate_yc")
bz0, bt, bhw = P("cap_bar_z0"), P("cap_bar_t"), P("cap_bar_hw")
by0, by1 = P("cap_bar_y0"), P("cap_bar_y1")
sod, shx = P("cap_spine_od"), P("cap_ring_hx")
rt, ry0 = P("cap_rib_t"), P("cap_rib_y0")
xbd, xbz = P("cap_xboss_d"), P("cap_xb_z")
xbx = P("xbolt_dx")
feat = []
def bind(sk, pairs):
    for n, e in pairs:
        sk.setExpression("Constraints." + n, e)

# 2) positive features ------------------------------------------------------------------
# spine half ring (cylinder along X, lower half removed later)
sk = new_sketch(body, "Sk_spinering", "YZ_Plane", 0)
add_circle(sk, 0, 0, sod, "c")
bind(sk, [("c_d", "Params.cap_spine_od")]); feat.append(sk)
pad(body, "SpineRing", sk, 2 * shx, mid=True)
bind_f = body.getObject("SpineRing"); bind_f.setExpression("Length", "2 * Params.cap_ring_hx")

# spar ring (cylinder along Y)
sk = new_sketch(body, "Sk_sparring", "XZ_Plane", 0)
add_circle(sk, sx, sz, ring_od, "c")
bind(sk, [("c_d", "Params.cap_ring_od"), ("c_cx", "Params.spar_f_ax - Params.sad_x1"), ("c_cy", "Params.spar_f_az - Params.spine_z")]); feat.append(sk)
f = pad(body, "SparRing", sk, ylen, mid=True); f.setExpression("Length", "Params.cap_ylen")

# two end plates (XZ plane, offset = -y so that y = +/-pyc) joining the spar ring down to the flange bars
for tag, yc in (("P", pyc), ("N", -pyc)):
    sk = new_sketch(body, "Sk_endplate_" + tag, "XZ_Plane", -yc)
    add_rect(sk, sx - ring_od / 2, bz0, sx + ring_od / 2, sz, "r")
    bind(sk, [("r_x0", "Params.spar_f_ax - Params.sad_x1 - Params.cap_ring_od / 2"), ("r_y0", "Params.cap_bar_z0"),
              ("r_w", "Params.cap_ring_od"), ("r_h", "Params.spar_f_az - Params.spine_z - Params.cap_bar_z0")])
    sk.setExpression(".AttachmentOffset.Base.z", ("-Params.cap_plate_yc" if tag == "P" else "Params.cap_plate_yc"))
    f = pad(body, "EndPlate_" + tag, sk, pt, mid=True); f.setExpression("Length", "Params.cap_plate_t")

# two flange bars (XY plane at z = bar bottom), carrying the 4 clamp bolts
for tag, (ya, yb) in (("P", (by0, by1)), ("N", (-by1, -by0))):
    sk = new_sketch(body, "Sk_bar_" + tag, "XY_Plane", bz0)
    add_rect(sk, -bhw, ya, bhw, yb, "r")
    if tag == "P":
        bind(sk, [("r_x0", "-Params.cap_bar_hw"), ("r_y0", "Params.cap_bar_y0"), ("r_w", "2 * Params.cap_bar_hw"), ("r_h", "Params.cap_bar_y1 - Params.cap_bar_y0")])
    else:
        bind(sk, [("r_x0", "-Params.cap_bar_hw"), ("r_y0", "-Params.cap_bar_y1"), ("r_w", "2 * Params.cap_bar_hw"), ("r_h", "Params.cap_bar_y1 - Params.cap_bar_y0")])
    sk.setExpression(".AttachmentOffset.Base.z", "Params.cap_bar_z0")
    f = pad(body, "Bar_" + tag, sk, bt); f.setExpression("Length", "Params.cap_bar_t")

# two ribs from the spine ring up to the bars
for tag, yc in (("P", ry0 + rt / 2), ("N", -(ry0 + rt / 2))):
    sk = new_sketch(body, "Sk_rib_" + tag, "XZ_Plane", -yc)
    add_rect(sk, -shx, 0, shx, bz0 + 0.4, "r")
    bind(sk, [("r_x0", "-Params.cap_ring_hx"), ("r_w", "2 * Params.cap_ring_hx"), ("r_h", "Params.cap_bar_z0 + 0.4")])
    sk.setExpression(".AttachmentOffset.Base.z", ("-(Params.cap_rib_y0 + Params.cap_rib_t / 2)" if tag == "P" else "(Params.cap_rib_y0 + Params.cap_rib_t / 2)"))
    f = pad(body, "Rib_" + tag, sk, rt, mid=True); f.setExpression("Length", "Params.cap_rib_t")

# cross-bolt boss
sk = new_sketch(body, "Sk_xboss", "XY_Plane", 5.0)
add_circle(sk, xbx, 0, xbd, "c")
bind(sk, [("c_d", "Params.cap_xboss_d"), ("c_cx", "Params.xbolt_dx")])
f = pad(body, "XBoss", sk, xbz - 5.0); f.setExpression("Length", "Params.cap_xb_z - 5")

# 3) cuts ---------------------------------------------------------------------------------
sk = new_sketch(body, "Sk_belowsplit", "XY_Plane", 0)
add_rect(sk, -30, -30, 30, 30, "r")
pocket(body, "SplitCut", sk, 20.0)     # removes everything below the spine axis plane

sk = new_sketch(body, "Sk_spinebore", "YZ_Plane", 0)
add_circle(sk, 0, 0, P("bore_d"), "c"); bind(sk, [("c_d", "Params.bore_d")])
pocket(body, "Spine_Bore", sk, through=True, mid=True)

sk = new_sketch(body, "Sk_sparbore", "XZ_Plane", 0)
add_circle(sk, sx, sz, P("spar_f_hole_p"), "c")
bind(sk, [("c_d", "Params.spar_f_hole_p"), ("c_cx", "Params.spar_f_ax - Params.sad_x1"), ("c_cy", "Params.spar_f_az - Params.spine_z")])
pocket(body, "Spar_Bore", sk, through=True, mid=True)

sk = new_sketch(body, "Sk_bolt_holes", "XY_Plane", 30)
k = 0
for sxs in (-1, 1):
    for sys_ in (-1, 1):
        add_circle(sk, sxs * bx, sys_ * by, P("m3_clear"), "h%d" % k)
        bind(sk, [("h%d_d" % k, "Params.m3_clear"), ("h%d_cx" % k, ("-" if sxs < 0 else "") + "Params.cap_bx"), ("h%d_cy" % k, ("-" if sys_ < 0 else "") + "Params.cap_by")])
        k += 1
pocket(body, "Bolt_Holes", sk, through=True, mid=True)

sk = new_sketch(body, "Sk_xbolt_clear", "XY_Plane", 30)
add_circle(sk, xbx, 0, P("m3_clear"), "c"); bind(sk, [("c_d", "Params.m3_clear"), ("c_cx", "Params.xbolt_dx")])
pocket(body, "XBoltClear_Cap", sk, through=True, mid=True)

sk = new_sketch(body, "Sk_xbolt_insert", "XY_Plane", 12.9)
add_circle(sk, xbx, 0, P("insert_d"), "c"); bind(sk, [("c_d", "Params.insert_d"), ("c_cx", "Params.xbolt_dx")])
pocket(body, "XBoltInsert_Cap", sk, 6.2)

doc.recompute()
# LCS bolt positions
for n, (sx_, sy_) in {"LCS_bolt1_F": (-1, -1), "LCS_bolt2_F": (1, -1), "LCS_bolt3_F": (-1, 1), "LCS_bolt4_F": (1, 1)}.items():
    l = body.getObject(n)
    l.Placement = App.Placement(V(sx_ * bx, sy_ * by, 14.6), l.Placement.Rotation)
body.Tip = body.getObject("XBoltInsert_Cap")
doc.recompute()
s = body.Shape
print("valid", s.isValid(), "vol", round(s.Volume, 1), "solids", len(s.Solids), s.BoundBox)
bad = []
for f in body.Group:
    if f.TypeId == "Sketcher::SketchObject":
        r = f.solve()
        fc = getattr(f, "FullyConstrained", "n/a")
        if r != 0 or len(f.MalformedConstraints) or fc is not True:
            bad.append((f.Name, r, len(f.MalformedConstraints), fc))
print("sketch problems:", bad)
print("state errors:", [f.Name for f in body.Group if "Invalid" in f.State or "Error" in str(f.State)])
