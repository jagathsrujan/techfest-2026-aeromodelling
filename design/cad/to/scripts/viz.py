"""Matplotlib renderer for tet meshes (no GL needed): 4-view panels of density or stress."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib import cm, colors
from fe import tet_boundary_faces

VIEWS = {"iso": (28, -58), "front": (0, -90), "top": (90, -90), "side": (0, 0)}


def _rot(elev, azim):
    e, a = np.radians(elev), np.radians(azim)
    # camera looks along -d where d = (cos e cos a, cos e sin a, sin e); build right/up vectors
    d = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    up0 = np.array([0, 0, 1.0]) if abs(d[2]) < 0.99 else np.array([0, 1.0, 0])
    right = np.cross(up0, d); right /= np.linalg.norm(right)
    up = np.cross(d, right)
    return right, up, d


def panel(ax, xyz, faces, fcol, view):
    right, up, d = _rot(*VIEWS[view])
    P = xyz[faces]                        # nf,3,3
    n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
    nn = np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    n = n / nn
    # outward orientation: flip so normal faces camera when visible
    facing = n @ d
    sgn = np.where(facing < 0, -1, 1)
    n = n * sgn[:, None]
    vis = (n @ d) > -0.02
    light = np.array([0.4, -0.3, 0.9]); light /= np.linalg.norm(light)
    sh = 0.45 + 0.55 * np.clip(n @ light, 0, 1)
    depth = (P.mean(axis=1) @ d)
    order = np.argsort(depth)
    order = order[vis[order]]
    xy = np.stack([P[order] @ right, P[order] @ up], axis=2)
    col = fcol[order, :3] * sh[order][:, None]
    pc = PolyCollection(xy, facecolors=col, edgecolors=col * 0.8, linewidths=0.15)
    ax.add_collection(pc)
    ax.set_xlim(xy[..., 0].min() - 1, xy[..., 0].max() + 1)
    ax.set_ylim(xy[..., 1].min() - 1, xy[..., 1].max() + 1)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(view, fontsize=9)


def density_png(path, mesh, solid, design, title, extra=""):
    xyz, E = mesh["xyz"], mesh["E"]
    faces, own = tet_boundary_faces(E, solid)
    col = np.where(design[own][:, None], np.array([[0.95, 0.55, 0.15]]), np.array([[0.35, 0.45, 0.65]]))
    fig = plt.figure(figsize=(12, 9), dpi=110)
    for k, v in enumerate(["iso", "front", "top", "side"]):
        ax = fig.add_subplot(2, 2, k + 1)
        panel(ax, xyz, faces, col, v)
    fig.suptitle(title + "   (orange = optimised region, blue = kept non-design region)" + extra, fontsize=10)
    fig.savefig(path, facecolor="white"); plt.close(fig)


def stress_png(path, mesh, vmn, title, vmax=17.5, views=("iso", "front", "top", "side"), cmap="turbo"):
    """vmn: nodal von Mises (nnode). Faces coloured by mean corner-node value; > vmax drawn magenta."""
    xyz, E = mesh["xyz"], mesh["E"]
    faces, own = tet_boundary_faces(E)
    val = vmn[faces].mean(axis=1)
    cmap_ = cm.get_cmap(cmap)
    col = cmap_(np.clip(val / vmax, 0, 1))
    col[val > vmax] = [0.85, 0.0, 0.85, 1]
    fig = plt.figure(figsize=(12, 9) if len(views) > 1 else (7, 6), dpi=110)
    for k, v in enumerate(views):
        ax = fig.add_subplot(2, 2, k + 1) if len(views) > 1 else fig.add_subplot(1, 1, 1)
        panel(ax, xyz, faces, col, v)
    sm = cm.ScalarMappable(norm=colors.Normalize(0, vmax), cmap=cmap_)
    cb = fig.colorbar(sm, ax=fig.axes, shrink=0.6, label="von Mises [MPa] (magenta = above %.1f)" % vmax)
    fig.suptitle("%s   max %.2f MPa" % (title, vmn.max()), fontsize=10)
    fig.savefig(path, facecolor="white"); plt.close(fig)
