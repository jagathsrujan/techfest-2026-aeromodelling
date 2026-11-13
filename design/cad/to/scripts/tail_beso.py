import sys, os, json, time
import numpy as np
import fe, viz

W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/tail/"
OUT = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/"
os.makedirs(W, exist_ok=True)
ZS = 142.0
PINCH = (805.0, 865.0)
SPINE_R = 7.075

def regions(cent):
    x, y, z = cent.T
    r = np.hypot(y, z - ZS)
    collar = (abs(x - 805) < 6) | (abs(x - 865) < 6) | (x < 786) | (x > 940)
    nd = (r < SPINE_R + 1.6) & collar
    for px in PINCH:
        h = np.hypot(x - px, y)
        nd |= (h < 4.25) & (z < 135) | (h < 3.3)
    return nd

def build_cases(mesh, which=("S", "F", "K"), tol=0.12, use_surf=True):
    xyz = mesh["xyz"]; x, y, z = xyz.T
    r = np.hypot(y, z - ZS)
    collar = (abs(x - 805) < 6) | (abs(x - 865) < 6) | (x < 786) | (x > 940)
    bore = np.nonzero((abs(r - SPINE_R) < tol) & collar)[0]
    top = np.nonzero((z > 149.9) & (x >= 791) & (x <= 885) & (abs(y) <= 10.01))[0]
    slot = np.nonzero((abs(y - 1.6) < tol) & (x >= 826) & (x <= 844) & (z >= 150.9))[0]
    skid = np.nonzero((z < 119.6) & (x >= 925))[0]
    info = dict(n_bore=len(bore), n_top=len(top), n_slot=len(slot), n_skid=len(skid))
    def mk(nodes, F, c):
        f = fe.distribute(xyz[nodes], F, (0, 0, 0), c)
        return [(n, k + 1, f[j, k]) for j, n in enumerate(nodes) for k in range(3) if abs(f[j, k]) > 0]
    fix = [(bore, (1, 2, 3))]
    defs = {
        "S": dict(name="S_stab_down_8N", fix=fix, loads=mk(top, (0, 0, -8.0), (838, 0, 150))),
        "F": dict(name="F_fin_side_3N_lever80", fix=fix, loads=mk(slot, (0, 3.0, 0), (835, 0, 153 + 80))),
        "K": dict(name="K_skid_strike_15N", fix=fix, loads=mk(skid, (0, 0, 15.0), (946, 0, 119.5))),
    }
    return [defs[k] for k in which], info

def log_to(fn):
    f = open(fn, "a")
    def log(s):
        f.write(s + "\n"); f.flush(); print(s, flush=True)
    return log

if __name__ == "__main__":
    mode = sys.argv[1]
    vf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
    log = log_to(W + "log.txt")
    mesh = fe.mesh_brep(OUT + "work/tail_space.brep", W + "tail.msh", h=2.0, hmin=0.8)
    cent = mesh["xyz"][mesh["E"][:, :4]].mean(axis=1)
    design = ~regions(cent)
    log("mesh: %d nodes %d tets, design tets %d (%.0f%% of volume)" % (len(mesh["xyz"]), len(mesh["E"]), design.sum(), 100 * mesh["vol"][design].sum() / mesh["vol"].sum()))
    cases, info = build_cases(mesh); log(str(info))
    if mode == "test":
        fe.write_inp(W + "t.inp", mesh, np.ones(len(mesh["E"]), bool), cases)
        t, _ = fe.run_ccx("t", W, 6)
        en, st = fe.parse_dat(W + "t.dat", len(mesh["E"]), len(cases))
        for k, c in enumerate(cases):
            log("%s: max vM %.2f MPa  energy %.4g" % (c["name"], fe.vm(st[k]).max(), (en[k] * mesh["vol"]).sum()))
        log("ccx %.1fs" % t)
    else:
        t0 = time.time()
        res = fe.beso(mesh, design, cases, W, vf=vf, er=0.04, rmin=4.0, maxit=90, log=log)
        x = res["x"]
        np.savez_compressed(W + "tail_result.npz", x=x, design=design, xyz=mesh["xyz"], E=mesh["E"], hist=np.array(res["hist"]))
        viz.density_png(OUT + "tail_mount_density.png", mesh, x, design, "TailMount  BESO result (%.0f%% of designable volume)" % (100 * mesh["vol"][design & x].sum() / mesh["vol"][design].sum()))
        log("done in %.0fs; solid %.0f mm3 of %.0f" % (time.time() - t0, mesh["vol"][x].sum(), mesh["vol"].sum()))
