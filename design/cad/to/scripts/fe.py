"""Small FEM + BESO toolkit for phase 5 (runs in FreeCAD's bundled python, no gmsh module needed).

gmsh (command line) meshes a BREP, we read the .msh ourselves, write CalculiX decks, run ccx,
parse .dat/.frd, and run a BESO loop (hard-kill / soft-kill, sensitivity filter, history average).
All coordinates are in the aircraft frame (mm). Units: mm, N, MPa (so mass is in tonne/mm3; not needed).
"""
import os, subprocess, time, json
import numpy as np

BIN = "/Applications/FreeCAD.app/Contents/Resources/bin"
GMSH = BIN + "/gmsh"
CCX = BIN + "/ccx"

# ---------------------------------------------------------------- meshing
def mesh_brep(brep, msh, h, hmin=None, order=1, curv=12):
    geo = msh[:-4] + ".geo"
    hmin = hmin or h / 3.0
    with open(geo, "w") as f:
        f.write('Merge "%s";\n' % brep)
        f.write("Mesh.CharacteristicLengthMax=%g;\nMesh.CharacteristicLengthMin=%g;\n" % (h, hmin))
        f.write("Mesh.MeshSizeFromCurvature=%d;\nMesh.ElementOrder=%d;\nMesh.MshFileVersion=2.2;\n" % (curv, order))
        f.write("Mesh.Algorithm3D=1;\nMesh.Optimize=1;\nMesh 3;\nSave \"%s\";\n" % msh)
    r = subprocess.run([GMSH, geo, "-", "-v", "2"], capture_output=True, text=True)
    if not os.path.exists(msh):
        raise RuntimeError("gmsh failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    return read_msh(msh)


def read_msh(path):
    nodes = {}
    elems = []
    with open(path) as f:
        lines = f.read().split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith("$Nodes"):
            n = int(lines[i + 1])
            for k in range(n):
                p = lines[i + 2 + k].split()
                nodes[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
            i += n + 2
        elif lines[i].startswith("$Elements"):
            n = int(lines[i + 1])
            for k in range(n):
                p = lines[i + 2 + k].split()
                t = int(p[1])
                if t in (4, 11):
                    nt = int(p[2])
                    elems.append([int(v) for v in p[3 + nt:]])
            i += n + 2
        i += 1
    ids = sorted(nodes)
    idx = {nid: k for k, nid in enumerate(ids)}
    xyz = np.array([nodes[n] for n in ids])
    order10 = len(elems[0]) == 10
    E = np.array([[idx[v] for v in e] for e in elems], dtype=int)
    # positive volume check on corner nodes
    a, b, c, d = (xyz[E[:, k]] for k in range(4))
    vol6 = np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a)
    neg = vol6 < 0
    if neg.any():
        if order10:
            raise RuntimeError("negative tet10 orientation: %d" % neg.sum())
        E[neg, 1], E[neg, 2] = E[neg, 2].copy(), E[neg, 1].copy()
    vol = np.abs(vol6) / 6.0
    return dict(xyz=xyz, E=E, vol=vol, order10=order10, nneg=int(neg.sum()))


def tet_boundary_faces(E, mask=None):
    """Return boundary faces (corner node triples) of the element subset, and the owning element of each."""
    sel = np.arange(len(E)) if mask is None else np.nonzero(mask)[0]
    f = np.concatenate([E[sel][:, [0, 1, 2]], E[sel][:, [0, 1, 3]], E[sel][:, [0, 2, 3]], E[sel][:, [1, 2, 3]]])
    own = np.tile(sel, 4)
    key = np.sort(f, axis=1)
    _, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    keep = cnt[inv.ravel()] == 1
    return f[keep], own[keep]


# ---------------------------------------------------------------- load helpers
def distribute(xyz, F, M=(0, 0, 0), c=(0, 0, 0)):
    """Nodal forces on points xyz equal to resultant force F and moment M about point c (equal weights)."""
    F = np.asarray(F, float); M = np.asarray(M, float); c = np.asarray(c, float)
    n = len(xyz)
    g = xyz.mean(axis=0)
    r = xyz - g
    L = M - np.cross(g - c, F)
    I = np.zeros((3, 3))
    for v in r:
        I += np.dot(v, v) * np.eye(3) - np.outer(v, v)
    w = np.linalg.lstsq(I, L, rcond=None)[0]
    return F / n + np.cross(w, r)


# ---------------------------------------------------------------- ccx deck
def ccx_order(E):
    """gmsh tet10 -> ccx C3D10 node order."""
    return E[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]]


def write_inp(path, mesh, solid_mask, cases, E_mod=4000.0, nu=0.35, soft=1e-3, out="dat", elset_energy=True):
    """cases: list of dict(name, fix=[(nodes_idx, (d1,d2..))], loads=[(node_idx, dof, val)...])
    solid_mask: bool per element (True = full stiffness). out: 'dat' (ENER+S per element) or 'frd' (nodal S)."""
    xyz, E = mesh["xyz"], mesh["E"]
    o10 = mesh["order10"]
    with open(path, "w") as f:
        f.write("*NODE, NSET=NALL\n")
        for i, p in enumerate(xyz):
            f.write("%d,%.6f,%.6f,%.6f\n" % (i + 1, p[0], p[1], p[2]))
        f.write("*ELEMENT, TYPE=%s, ELSET=EALL\n" % ("C3D10" if o10 else "C3D4"))
        EE = ccx_order(E) if o10 else E
        for i, e in enumerate(EE):
            f.write("%d,%s\n" % (i + 1, ",".join(str(v + 1) for v in e)))
        # element sets
        def wset(name, ids, kind="ELSET"):
            f.write("*%s, %s=%s\n" % (kind, kind, name))
            ids = list(ids)
            for k in range(0, len(ids), 12):
                f.write(",".join(str(v) for v in ids[k:k + 12]) + ",\n")
        sol = np.nonzero(solid_mask)[0] + 1
        sft = np.nonzero(~solid_mask)[0] + 1
        wset("ESOL", sol)
        f.write("*MATERIAL, NAME=MSOL\n*ELASTIC\n%g,%g\n" % (E_mod, nu))
        f.write("*SOLID SECTION, ELSET=ESOL, MATERIAL=MSOL\n")
        if len(sft):
            wset("ESOFT", sft)
            f.write("*MATERIAL, NAME=MSOFT\n*ELASTIC\n%g,%g\n" % (E_mod * soft, nu))
            f.write("*SOLID SECTION, ELSET=ESOFT, MATERIAL=MSOFT\n")
        for c in cases:
            f.write("*STEP\n*STATIC\n*BOUNDARY, OP=NEW\n")
            for nodes, dofs in c["fix"]:
                for n in nodes:
                    for d in dofs:
                        f.write("%d,%d,%d\n" % (n + 1, d, d))
            f.write("*CLOAD, OP=NEW\n")
            for n, d, v in c["loads"]:
                f.write("%d,%d,%.6g\n" % (n + 1, d, v))
            if out == "dat":
                f.write("*EL PRINT, ELSET=EALL\nENER\n*EL PRINT, ELSET=EALL\nS\n")
            else:
                f.write("*NODE FILE\nU,S\n")
            f.write("*END STEP\n")


def run_ccx(job, cwd, threads=6):
    env = dict(os.environ, OMP_NUM_THREADS=str(threads), CCX_NPROC_EQUATION_SOLVER=str(threads))
    t = time.time()
    r = subprocess.run([CCX, "-i", job], cwd=cwd, capture_output=True, text=True, env=env)
    if not os.path.exists(os.path.join(cwd, job + (".dat" if True else ""))) and "error" in (r.stdout + r.stderr).lower():
        raise RuntimeError(r.stdout[-3000:] + r.stderr[-1000:])
    return time.time() - t, r.stdout[-1500:]


def parse_dat(path, nelem, nsteps):
    """Return (ener[nsteps][nelem], stress[nsteps][nelem,6 (xx,yy,zz,xy,xz,yz)] averaged over int points)."""
    ener = [np.zeros(nelem) for _ in range(nsteps)]
    sts = [np.zeros((nelem, 6)) for _ in range(nsteps)]
    cnt_e = [np.zeros(nelem) for _ in range(nsteps)]
    cnt_s = [np.zeros(nelem) for _ in range(nsteps)]
    mode = None
    es = -1; ss = -1
    with open(path) as f:
        for ln in f:
            s = ln.strip()
            if "internal energy density" in s:
                mode = "e"; es += 1; continue
            if s.startswith("stresses (elem"):
                mode = "s"; ss += 1; continue
            if not s:
                continue
            p = s.split()
            try:
                vals = [float(v) for v in p]
            except ValueError:
                mode = None
                continue
            if mode == "e" and len(vals) == 3 and es < nsteps:
                k = int(vals[0]) - 1
                ener[es][k] += vals[2]; cnt_e[es][k] += 1
            elif mode == "s" and len(vals) == 8 and ss < nsteps:
                k = int(vals[0]) - 1
                sts[ss][k] += vals[2:8]; cnt_s[ss][k] += 1
    for i in range(nsteps):
        ener[i] /= np.maximum(cnt_e[i], 1)
        sts[i] /= np.maximum(cnt_s[i], 1)[:, None]
    return ener, sts


def vm(s):
    """von Mises from [xx,yy,zz,xy,xz,yz] (or any order of shears, symmetric formula)."""
    sxx, syy, szz, a, b, c = (s[..., i] for i in range(6))
    return np.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3 * (a * a + b * b + c * c))


def parse_frd(path, nnode, nsteps):
    """Nodal U and S (frd order xx,yy,zz,xy,yz,zx). Returns U[nsteps][nnode,3], S[nsteps][nnode,6]."""
    U = []; S = []
    cur = None
    with open(path) as f:
        for ln in f:
            if ln.startswith(" -4"):
                name = ln.split()[1]
                cur = name
                arr = np.zeros((nnode, 6 if name == "STRESS" else 3))
                if name == "STRESS":
                    S.append(arr)
                elif name == "DISP":
                    U.append(arr)
                else:
                    cur = None
            elif ln.startswith(" -1") and cur:
                nid = int(ln[3:13])
                n = 6 if cur == "STRESS" else 3
                vals = [float(ln[13 + 12 * k:25 + 12 * k]) for k in range(n)]
                (S if cur == "STRESS" else U)[-1][nid - 1, :n] = vals
            elif ln.startswith(" -3"):
                cur = None
    return U, S


# ---------------------------------------------------------------- BESO
def beso(mesh, design, cases, workdir, vf=0.33, er=0.03, rmin=3.0, maxit=80, E_mod=4000.0, soft=1e-3,
         threads=6, log=print, snap=None, case_w=None, ar_max=0.01):
    """design: bool per element (True = may be removed). cases as in write_inp. Returns dict with x history."""
    from scipy.spatial import cKDTree
    from scipy.sparse import coo_matrix
    xyz, E, vol = mesh["xyz"], mesh["E"], mesh["vol"]
    cent = xyz[E[:, :4]].mean(axis=1)
    ne = len(E)
    tree = cKDTree(cent)
    pairs = tree.query_pairs(rmin, output_type="ndarray")
    d = np.linalg.norm(cent[pairs[:, 0]] - cent[pairs[:, 1]], axis=1)
    w = rmin - d
    r = np.concatenate([pairs[:, 0], pairs[:, 1], np.arange(ne)])
    c = np.concatenate([pairs[:, 1], pairs[:, 0], np.arange(ne)])
    ww = np.concatenate([w, w, np.full(ne, rmin)])
    W = coo_matrix((ww, (r, c)), shape=(ne, ne)).tocsr()
    wsum = np.asarray(W.sum(axis=1)).ravel()
    x = np.ones(ne, bool)
    Vdes0 = vol[design].sum()
    ncase = len(cases)
    case_w = case_w or [1.0] * ncase
    hist = []
    alpha_old = None
    comp_hist = []
    job = "beso"
    for it in range(maxit):
        write_inp(os.path.join(workdir, job + ".inp"), mesh, x, cases, E_mod=E_mod, soft=soft)
        t, tail = run_ccx(job, workdir, threads)
        ener, _ = parse_dat(os.path.join(workdir, job + ".dat"), ne, ncase)
        alpha = np.zeros(ne)
        comp = 0.0
        for k in range(ncase):
            en = ener[k].copy()
            en[~x] /= soft            # soft-kill: evaluate as if solid
            comp += case_w[k] * (ener[k] * vol).sum()
            alpha += case_w[k] * en / max((ener[k] * vol)[x].sum(), 1e-30)   # normalise each case
        alpha_f = (W @ alpha) / wsum
        if alpha_old is not None:
            alpha_f = 0.5 * (alpha_f + alpha_old)
        alpha_old = alpha_f.copy()
        vcur = vol[design & x].sum() / Vdes0
        vnext = max(vcur * (1 - er), vf)
        # BESO update with an admission-ratio limit (stops the flip-flopping of the plain sorted threshold)
        idx = np.nonzero(design)[0]
        add_cand = idx[~x[idx]]
        add_cand = add_cand[np.argsort(-alpha_f[add_cand])]
        cadd = np.cumsum(vol[add_cand]) / Vdes0
        add = add_cand[:np.searchsorted(cadd, ar_max)] if len(add_cand) else add_cand
        xn = x.copy(); xn[add] = True
        keep = idx[xn[idx]]
        keep = keep[np.argsort(-alpha_f[keep])]
        ckeep = np.cumsum(vol[keep]) / Vdes0
        nk = np.searchsorted(ckeep, vnext) + 1
        xn[keep[nk:]] = False
        changed = int((xn != x).sum())
        x = xn
        comp_hist.append(comp)
        vfrac = vol[design & x].sum() / Vdes0
        log("it %2d  ccx %.1fs  compliance %.4g  design-vol %.3f  changed %d" % (it, t, comp, vfrac, changed))
        hist.append((it, comp, vfrac, changed))
        if snap:
            snap(it, x)
        if vfrac <= vf + 1e-3 and it >= 5 and len(comp_hist) > 5:
            rec = comp_hist[-5:]
            if (max(rec) - min(rec)) / np.mean(rec) < 0.01 and changed < 0.003 * len(idx):
                log("converged")
                break
    return dict(x=x, hist=hist, cent=cent, design=design)
