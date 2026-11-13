import sys, os, json, time
import numpy as np
import fe, viz
from motor_setup_consts import *

W = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/work/motor/"
OUT = "/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/to/"
os.makedirs(W, exist_ok=True)
HUB_X = -4.0 - 49.0                      # prop hub 49 mm ahead of the motor face


def default_geom():
    d = np.array([1.0, 0, 0])
    return dict(dir_pod=d, dir_mot=d, pod=[np.array([XR, y, z]) for y, z in PODB], mot=[np.array([XR, y, z]) for y, z in MOTB],
                hub=np.array([HUB_X, YC, ZC]), face_c=np.array([XF, YC, ZC]))


def dist_line(P, a, d):
    v = P - a
    return np.linalg.norm(v - np.outer(v @ d, d), axis=1)


def regions(cent):
    x, y, z = cent.T
    nd = np.zeros(len(cent), bool)
    for py, pz in PODB:
        h = np.hypot(y - py, z - pz)
        nd |= (h < 1.7 + 1.6) & (x >= XF - 0.01) | (h < 4.7) & (x >= XF - 0.01)
    for my, mz in MOTB:
        h = np.hypot(y - my, z - mz)
        nd |= (h < 1.7 + 1.6)
    return nd


def build_cases(mesh, which=("T", "Sy", "Sz"), tol=0.12, use_surf=True, geom=None):
    g = geom or default_geom()
    xyz = mesh["xyz"]
    dp, dm = g["dir_pod"], g["dir_mot"]
    mot = np.zeros(len(xyz), bool)
    for a in g["mot"]:
        mot |= abs(dist_line(xyz, a, dm) - 1.7) < tol
    mot_n = np.nonzero(mot)[0]
    seats = np.zeros(len(xyz), bool)
    for a in g["pod"]:
        r = dist_line(xyz, a, dp)
        front = (xyz - a) @ (-dp) > 2.0                     # front (motor) side of the plate
        seats |= (r > 1.75) & (r < 3.1) & front
    seat_n = np.nonzero(seats)[0]
    # seat nodes must sit on the front face: take the front-most layer of each annulus
    keep = []
    for a in g["pod"]:
        m = seats & (dist_line(xyz, a, dp) < 3.2)
        idx = np.nonzero(m)[0]
        if len(idx):
            fr = ((xyz[idx] - a) @ (-dp))
            keep += list(idx[fr > fr.max() - 0.45])
    seat_n = np.array(sorted(set(keep)))
    info = dict(n_motor=len(mot_n), n_seat=len(seat_n))
    def mk(F, M=(0, 0, 0), c=None):
        c = g["hub"] if c is None else c
        f = fe.distribute(xyz[mot_n], F, M, c)
        return [(n, k + 1, f[j, k]) for j, n in enumerate(mot_n) for k in range(3) if abs(f[j, k]) > 0]
    face_c = g["face_c"]
    fwd = -dm
    defs = {
        "T": dict(name="T_thrust8N_torque0.3Nm", fix=[(seat_n, (1, 2, 3))], loads=mk(8.0 * fwd, 300.0 * fwd, face_c)),
        "Sy": dict(name="Sy_side30N_at_hub", fix=[(seat_n, (1, 2, 3))], loads=mk((0, 30.0, 0))),
        "Sz": dict(name="Sz_side30N_at_hub", fix=[(seat_n, (1, 2, 3))], loads=mk((0, 0, 30.0))),
    }
    return [defs[k] for k in which], info


def log_to(fn):
    f = open(fn, "a")
    def log(s):
        f.write(s + "\n"); f.flush(); print(s, flush=True)
    return log


if __name__ == "__main__":
    mode = sys.argv[1]
    vf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    log = log_to(W + "log.txt")
    mesh = fe.mesh_brep(OUT + "work/motor_space.brep", W + "motor.msh", h=1.2, hmin=0.5)
    cent = mesh["xyz"][mesh["E"][:, :4]].mean(axis=1)
    design = ~regions(cent)
    log("mesh: %d nodes %d tets, design tets %d (%.0f%% of volume)" % (len(mesh["xyz"]), len(mesh["E"]), design.sum(), 100 * mesh["vol"][design].sum() / mesh["vol"].sum()))
    cases, info = build_cases(mesh)
    log(str(info))
    if mode == "test":
        fe.write_inp(W + "t.inp", mesh, np.ones(len(mesh["E"]), bool), cases)
        t, _ = fe.run_ccx("t", W, 6)
        en, st = fe.parse_dat(W + "t.dat", len(mesh["E"]), len(cases))
        for k, c in enumerate(cases):
            log("%s: max vM %.2f MPa  energy %.4g" % (c["name"], fe.vm(st[k]).max(), (en[k] * mesh["vol"]).sum()))
    else:
        t0 = time.time()
        res = fe.beso(mesh, design, cases, W, vf=vf, er=0.04, rmin=2.6, maxit=90, log=log)
        x = res["x"]
        np.savez_compressed(W + "motor_result.npz", x=x, design=design, xyz=mesh["xyz"], E=mesh["E"], hist=np.array(res["hist"]))
        viz.density_png(OUT + "motor_mount_density.png", mesh, x, design, "MotorMount  BESO result (%.0f%% of designable volume)" % (100 * mesh["vol"][design & x].sum() / mesh["vol"][design].sum()))
        log("done in %.0fs; total solid volume %.0f mm3 of %.0f" % (time.time() - t0, mesh["vol"][x].sum(), mesh["vol"].sum()))
