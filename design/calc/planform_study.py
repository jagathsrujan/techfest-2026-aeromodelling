"""Rev H wing planform study: span fixed at 1190 mm (rule 1.2 m), S1223.
Prandtl lifting line (Glauert sine series) for the span load; checks span efficiency, where the wing stalls first,
and cruise/climb power at the 16-ball AUW. Section data are approximate S1223 values at low Re (interp.).
Run: python3 planform_study.py"""
import math
import numpy as np

rho, g, nu = 1.225, 9.81, 1.5e-5
b = 1.190                      # m
a0 = 5.7                       # section lift slope /rad (interp.)
aL0 = math.radians(-10.0)      # S1223 zero-lift angle (interp.)
AUW = 0.770 + 16 * 0.045       # kg: phase 4b target empty + 16 balls


def clmax_re(re):
    """S1223 section CLmax vs Re (interp. from UIUC low-Re data trend)."""
    return float(np.interp(re, [60e3, 100e3, 150e3, 200e3, 300e3], [1.70, 1.88, 1.98, 2.05, 2.15]))


def cd0_re(re):
    """S1223 section profile drag near cruise cl ~1.0 (interp.)."""
    return float(np.interp(re, [60e3, 100e3, 150e3, 200e3, 300e3], [0.030, 0.022, 0.018, 0.016, 0.014]))


def lifting_line(chord, twist, alpha, n=60):
    """chord(y), twist(y) callables over y in [-b/2, b/2]; returns y, local cl, CL, CDi, e, S."""
    th = np.linspace(1e-4, math.pi - 1e-4, n)
    y = -b / 2 * np.cos(th)
    c = np.array([chord(abs(v)) for v in y])
    tw = np.array([twist(abs(v)) for v in y])
    k = np.arange(1, n + 1)
    M = np.sin(np.outer(th, k)) * (4 * b / (a0 * c))[:, None] + np.sin(np.outer(th, k)) * k / np.sin(th)[:, None]
    A = np.linalg.solve(M, alpha + tw - aL0)
    gamma = 2 * b * (np.sin(np.outer(th, k)) @ A)          # circulation / V
    cl = 2 * gamma / c
    yy = np.linspace(0, b / 2, 400)
    S = 2 * np.trapezoid([chord(v) for v in yy], yy)
    AR = b * b / S
    CL = A[0] * math.pi * AR
    delta = sum((kk) * (A[kk - 1] / A[0]) ** 2 for kk in range(2, n + 1))
    e = 1 / (1 + delta)
    return y, c, cl, CL, CL * CL / (math.pi * AR * e), e, S


def planform(name, chord, twist, tip_h=0.0, extra_g=0.0):
    # angle that gives CL = 1.0, and the angle at which the first section reaches its local CLmax
    def at(alpha):
        return lifting_line(chord, twist, alpha)
    lo, hi = -0.3, 0.6
    y, c, cl, CL, CDi, e, S = at(0.0)
    # stall: find alpha where max(cl/clmax_local) = 1 at the stall speed of that CL
    for _ in range(40):
        mid = (lo + hi) / 2
        y, c, cl, CL, CDi, e, S = at(mid)
        V = math.sqrt(2 * AUW * g / (rho * S * max(CL, 0.1)))
        ratio = cl / np.array([clmax_re(V * ci / nu) for ci in c])
        if ratio.max() > 1:
            hi = mid
        else:
            lo = mid
    CLmax3d = CL
    i_stall = int(np.argmax(ratio))
    y_stall = abs(y[i_stall]) / (b / 2)
    Vs = math.sqrt(2 * AUW * g / (rho * S * CLmax3d))
    # end plates / winglets: effective-span gain (Hoerner/Whitcomb approx), e_eff = e (1 + 1.9 h/b)
    e_eff = e * (1 + 1.9 * tip_h / b)
    AR = b * b / S
    # cruise at 1.4 Vs, climb at 1.25 Vs
    out = []
    for f in (1.25, 1.4):
        V = f * Vs
        CLc = 2 * AUW * g / (rho * V * V * S)
        mac = S / b
        cd0 = cd0_re(V * mac / nu) + 0.012          # + fuselage/hopper/tail parasitic (interp.)
        CD = cd0 + CLc * CLc / (math.pi * AR * e_eff)
        P = 0.5 * rho * V ** 3 * S * CD
        out.append((V, CLc, CD, CLc / CD, P))
    print(f"\n== {name}")
    print(f"  S {S*100:.2f} dm2  AR {AR:.2f}  e {e:.3f}  e_eff {e_eff:.3f}  extra mass {extra_g:.0f} g")
    print(f"  3D CLmax {CLmax3d:.2f}  Vs {Vs:.2f} m/s  first stall at {y_stall*100:.0f}% semispan")
    for (V, CLc, CD, LD, P), lab in zip(out, ("climb 1.25Vs", "cruise 1.4Vs")):
        print(f"  {lab}: V {V:.1f} m/s  CL {CLc:.2f}  L/D {LD:.1f}  P_air {P:.1f} W")
    return dict(name=name, e=e_eff, CLmax=CLmax3d, Vs=Vs, ystall=y_stall, LD=out[1][3], P=out[1][4])


if __name__ == "__main__":
    S0 = 1.190 * 0.240
    rect = lambda y: 0.240
    flat = lambda y: 0.0

    def taper(cr, ct, y_brk):
        return lambda y: cr if y <= y_brk else cr + (ct - cr) * (y - y_brk) / (b / 2 - y_brk)

    def washout(deg, y_brk):
        return lambda y: 0.0 if y <= y_brk else -math.radians(deg) * (y - y_brk) / (b / 2 - y_brk)

    # same area as rect: centre panel to y_brk at cr, outer taper to ct
    yb, lam = 0.300, 0.60
    cr = S0 / (2 * (yb + (b / 2 - yb) * (1 + lam) / 2))
    res = [
        planform("A  rect 240 (current)", rect, flat),
        planform("B  rect 240 + 2 deg washout outer", rect, washout(2, yb)),
        planform(f"C  rect to 300 then taper 0.6 ({cr*1e3:.0f}->{lam*cr*1e3:.0f}), same S", taper(cr, lam * cr, yb), flat),
        planform("D  C + 2 deg washout", taper(cr, lam * cr, yb), washout(2, yb)),
        planform("E  B + 50 mm tip plates (2 x 3 g)", rect, washout(2, yb), tip_h=0.050, extra_g=6),
        planform("F  D + 50 mm tip plates", taper(cr, lam * cr, yb), washout(2, yb), tip_h=0.050, extra_g=6),
    ]
