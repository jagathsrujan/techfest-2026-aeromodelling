import sys, os, json, time
import numpy as np
import fe, viz
from clamp_setup import X0, ZS, SPAR, BX, BY, XB, ZSEAT, ZXB

W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/clamp/"
OUT = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/"
os.makedirs(W, exist_ok=True)
SB = (SPAR[0], SPAR[1])


def regions(cent):
    x, y, z = cent.T
    nd = (np.hypot(y, z - ZS) < 7.075 + 1.6) & (abs(x - X0) <= 10)  # 1.6 shell round the spine bore (bearing length)
    nd |= (np.hypot(x - SB[0], z - SB[1]) < 4.075 + 1.6) & (abs(y) <= 14)   # 1.6 shell round the spar bore
    for bx in BX:
        for by in BY:
            h = np.hypot(x - bx, y - by)
            nd |= ((h < 1.7 + 1.6) | (h < 3.1 + 1.6) & (z >= ZSEAT - 0.01)) & (z >= ZSEAT - 3.8)   # bolt pad under/around the head
    nd |= (np.hypot(x - XB, y) < 4.5) & (z <= ZXB + 0.01) & (z >= ZS + 6.0)   # cross-bolt boss round the insert
    return nd


def surf_nodes(mesh):
    faces, _ = fe.tet_boundary_faces(mesh["E"])
    m = np.zeros(len(mesh["xyz"]), bool)
    m[np.unique(faces)] = True
    return m


def build_cases(mesh, which=("a", "b", "c"), tol=0.12, use_surf=True):
    xyz = mesh["xyz"]; sm = surf_nodes(mesh) if use_surf else np.ones(len(xyz), bool)
    x, y, z = xyz.T
    rspar = np.hypot(x - SB[0], z - SB[1])
    on_spar = sm & (abs(rspar - 4.075) < tol)
    up = np.nonzero(on_spar & (z - SB[1] > 0.5 * 4.075))[0]
    dn = np.nonzero(on_spar & (z - SB[1] < -0.5 * 4.075))[0]
    rsp = np.hypot(y, z - ZS)
    top_spine = np.nonzero(sm & (abs(rsp - 7.075) < tol) & (z - ZS > 0.5 * 7.075))[0]
    seats = []
    for bx in BX:
        for by in BY:
            h = np.hypot(x - bx, y - by)
            seats += list(np.nonzero(sm & (abs(z - ZSEAT) < 0.2) & (h < 3.15) & (h > 1.65))[0])
    seats = np.array(seats)
    info = dict(n_up=len(up), n_dn=len(dn), n_top=len(top_spine), n_seat=len(seats))
    cases = []
    def loads(nodes, F):
        f = fe.distribute(xyz[nodes], F, c=(SB[0], 0, SB[1]))
        return [(n, d + 1, f[k, d]) for k, n in enumerate(nodes) for d in range(3) if abs(f[k, d]) > 0]
    defs = {
        "a": dict(name="a_4g_lift_48N", fix=[(seats, (1, 2, 3))], loads=loads(up, (0, 0, 48.0))),
        "b": dict(name="b_lift_plus_couple_66N", fix=[(seats, (1, 2, 3))], loads=loads(up, (0, 0, 66.0))),
        "c": dict(name="c_3g_down_36N", fix=[(top_spine, (3,)), (seats, (1, 2))], loads=loads(dn, (0, 0, -36.0))),
    }
    for k in which:
        cases.append(defs[k])
    return cases, info


def log_to(fn):
    f = open(fn, "a")
    def log(s):
        f.write(s + "\n"); f.flush(); print(s, flush=True)
    return log


if __name__ == "__main__":
    mode = sys.argv[1]
    log = log_to(W + "log.txt")
    mesh = fe.mesh_brep(OUT + "work/clamp_space.brep", W + "clamp.msh", h=1.5, hmin=0.6)
    cent = mesh["xyz"][mesh["E"][:, :4]].mean(axis=1)
    nd = regions(cent)
    design = ~nd
    log("mesh: %d nodes %d tets, design tets %d (%.0f%% of volume), neg %d" % (
        len(mesh["xyz"]), len(mesh["E"]), design.sum(), 100 * mesh["vol"][design].sum() / mesh["vol"].sum(), mesh["nneg"]))
    if mode == "test":
        cases, info = build_cases(mesh)
        log(str(info))
        solid = np.ones(len(mesh["E"]), bool)
        fe.write_inp(W + "t.inp", mesh, solid, cases)
        t, tail = fe.run_ccx("t", W, 6)
        en, st = fe.parse_dat(W + "t.dat", len(mesh["E"]), len(cases))
        for k, c in enumerate(cases):
            log("%s: max vM %.2f MPa  energy %.4g" % (c["name"], fe.vm(st[k]).max(), (en[k] * mesh["vol"]).sum()))
        log("ccx time %.1fs" % t)
    else:
        cases, info = build_cases(mesh, ("b", "c"))
        log(str(info))
        t0 = time.time()
        res = fe.beso(mesh, design, cases, W, vf=0.15, er=0.04, rmin=3.4, maxit=90, log=log,
                      snap=lambda it, x: (viz.density_png(W + "snap_%02d.png" % it, mesh, x, design, "BESO it %d" % it)
                                          if it % 10 == 0 else None))
        x = res["x"]
        np.savez_compressed(W + "clamp_result.npz", x=x, design=design, xyz=mesh["xyz"], E=mesh["E"], hist=np.array(res["hist"]))
        viz.density_png(OUT + "clamp_F_density.png", mesh, x, design, "WingClampCap_F  BESO result (%.0f%% of designable volume)" % (100 * mesh["vol"][design & x].sum() / mesh["vol"][design].sum()))
        log("done in %.0fs; total solid volume %.0f mm3 of %.0f" % (time.time() - t0, mesh["vol"][x].sum(), mesh["vol"].sum()))
