"""NACA 4412 (rev D) vs Selig S1223 (benchmark: Nitte Aero Club wing) on our span-limited wing.
Section data are approximate published values at Re ~150-200k (interp.); 3D CLmax taken as 0.9 x 2D.
Run: python3 airfoil_trade.py"""
import math
from sizing import S, c, b, W_empty, rho, g, x_le

AIRFOILS = {
    #            CLmax_2D  Cm_c/4  Cd_cruise  t/c   camber
    "NACA 4412": (1.40, -0.09, 0.015, 0.12, 0.04),
    "S1223":     (2.00, -0.25, 0.025, 0.121, 0.081),
}
LT = 0.600                 # CG -> HT AC (m)
SH_NOW = 0.0555            # rev D stab + elevators (m^2)
CLT_MAX_TRIM = 0.4         # flat-plate tail lift coefficient we allow for trim (interp.)
BALL = 45

for name, (clmax2d, cm, cd, tc, cam) in AIRFOILS.items():
    clmax = 0.9 * clmax2d
    print(f"\n== {name}: 3D CLmax {clmax:.2f}, Cm {cm}")
    for n in (10, 12, 16):
        W = (W_empty + BALL * n) / 1000 * g
        vs = math.sqrt(2 * W / (rho * S / 1e6 * clmax))
        v = 1.3 * vs
        q = 0.5 * rho * v ** 2
        m_wing = q * S / 1e6 * c / 1000 * cm               # N.m (nose-down negative)
        tail_force = -m_wing / LT                          # downforce on tail to trim, N
        cl_t = tail_force / (q * SH_NOW)
        sh_req = tail_force / (q * CLT_MAX_TRIM)
        print(f"  {n:2d} balls: AUW {W/g*1000:.0f} g  Vs {vs:.1f} m/s  V(1.3Vs) {v:.1f}  "
              f"tail trim force {tail_force:.2f} N ({tail_force/W*100:.0f}% of W)  "
              f"tail CL on rev D stab {cl_t:.2f}  stab needed for CLt<= {CLT_MAX_TRIM}: {sh_req*100:.2f} dm2")

# Payload that keeps stall at or below the rev D 10-ball value (7.1 m/s) with S1223
clmax = 0.9 * AIRFOILS["S1223"][0]
W_allow = 0.5 * rho * 7.1 ** 2 * S / 1e6 * clmax / g * 1000
print(f"\nS1223 at Vs 7.1 m/s lifts {W_allow:.0f} g -> {int((W_allow - W_empty) // BALL)} balls (bay holds 16)")
