"""Generic FEM verification (C3D10) of a rebuilt part. verify(name, brep, build_cases, h, outdir)"""
import os, json, numpy as np
import fe, viz
OUT = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/"

def verify(name, brep, build_cases, h=1.0, hmin=0.4, limit=17.5, E_mod=4000.0, tag="", which=None, excl=1.5):
    W = OUT + "work/%s/" % name
    os.makedirs(W, exist_ok=True)
    mesh = fe.mesh_brep(brep, W + "v.msh", h=h, hmin=hmin, order=2)
    kw = dict(which=which) if which else {}
    cases, info = build_cases(mesh, tol=0.05, use_surf=False, **kw)
    solid = np.ones(len(mesh["E"]), bool)
    fe.write_inp(W + "v.inp", mesh, solid, cases, E_mod=E_mod, out="frd")
    t, tail = fe.run_ccx("v", W, 8)
    U, S = fe.parse_frd(W + "v.frd", len(mesh["xyz"]), len(cases))
    res = dict(part=name, nodes=len(mesh["xyz"]), tets=len(mesh["E"]), volume_mm3=float(mesh["vol"].sum()), sel=info, cases={})
    worst = None
    from scipy.spatial import cKDTree
    for k, c in enumerate(cases):
        s = fe.vm(S[k])
        umax = float(np.linalg.norm(U[k], axis=1).max())
        # nodes directly at a support or at an applied load are numerical hot spots (ideal rigid support / point loads):
        # report the raw maximum and the maximum outside a 1.5 mm zone around them
        sup = np.array(sorted(set([n for nodes, d in c["fix"] for n in nodes] + [n for n, d, v in c["loads"]])))
        far = cKDTree(mesh["xyz"][sup]).query(mesh["xyz"])[0] > excl
        vm_excl = float(s[far].max())
        # robust peak: 99.5th percentile of node values, plus the raw max
        res["cases"][c["name"]] = dict(vm_max=float(s.max()), vm_max_excl=vm_excl, vm_p995=float(np.percentile(s, 99.5)), u_max_mm=umax,
                                      vm_max_at=[round(float(v), 1) for v in mesh["xyz"][int(s.argmax())]])
        viz.stress_png(OUT + "%s_stress_%s%s.png" % (name, c["name"], tag), mesh, s, "%s  case %s" % (name, c["name"]), limit)
        if worst is None or s.max() > worst[1].max():
            worst = (c["name"], s)
    res["worst_case"] = worst[0]
    res["pass_raw"] = all(v["vm_max"] <= limit for v in res["cases"].values())
    res["pass"] = all(v["vm_max_excl"] <= limit for v in res["cases"].values())
    res["exclusion_mm"] = excl
    json.dump(res, open(OUT + "%s_fem%s.json" % (name, tag), "w"), indent=1)
    np.savez_compressed(W + "v_result%s.npz" % tag, xyz=mesh["xyz"], E=mesh["E"], S=np.array([fe.vm(s) for s in S]))
    return res
