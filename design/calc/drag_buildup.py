"""Rev H parasitic drag build-up at cruise (16 balls, ~9.8 m/s): where the drag is and what fairing the hopper buys.
Component CD values are textbook estimates (Hoerner, interp.); use for ranking, not absolute numbers.
Run: python3 drag_buildup.py"""
import math
rho, g = 1.225, 9.81
S = 1.190 * 0.240
AUW = 0.770 + 16 * 0.045
V = 9.8
q = 0.5 * rho * V * V
CL = AUW * g / (q * S)
AR, e = 1.190 ** 2 / S, 0.96

# (name, reference area m2, CD on that area)
hop_front = 0.118 * 0.134                      # hopper max frontal area
pod_front = 0.060 * 0.080
common = [
    ("wing profile (S1223, Re~150k)", S, 0.018),
    ("stab + fin (flat plate, wetted ~0.20 m2)", 0.20, 0.010),
    ("spine tube aft of wing (16 mm x 0.55 m, cyl)", 0.016 * 0.55, 1.0 * 0.5),   # x0.5: partly in wake / interference
    ("tail mount, horns, pushrod exits", 0.0015, 1.0),
    ("motor + spinner + folded-hub wake", 0.0010, 0.6),
]
variants = {
    "current: box hopper + small pod (blunt shoulders, flat bottom, sharp edges)":
        [("pod (60x80)", pod_front, 0.25), ("hopper exposed face (box, sharp edges)", hop_front - pod_front, 0.75)],
    "faired: pod widened to hopper section, elliptic nose, R12 edges, tapered tail cone on chute":
        [("faired fuselage pod (fineness ~3.3, Cd_frontal)", hop_front, 0.16)],
}
for name, fus in variants.items():
    parts = common + fus
    cd0 = sum(a * cd / S for _, a, cd in parts) * 1.10          # +10% interference/leakage (interp.)
    cdi = CL * CL / (math.pi * AR * e)
    CD = cd0 + cdi
    P = q * S * CD * V
    print(f"\n== {name}\n  CL {CL:.2f}  CD0 {cd0:.4f}  CDi {cdi:.4f}  L/D {CL/CD:.1f}  P_air {P:.1f} W  drag {q*S*CD*1000/g:.0f} gf")
    for n, a, cd in parts:
        print(f"    {n:58s} dCD {a*cd/S:.4f}  ({a*cd/S/CD*100:4.1f}% of total)")
