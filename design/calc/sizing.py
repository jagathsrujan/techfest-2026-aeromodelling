"""Sizing for the Techfest 2026 payload plane (rev G: carbon spine + V-funnel hopper (team concept), flat S1223 wing,
13 in folding prop on a nose pod, 16-ball design load). rev F numbers kept in sizing_revF.py.
Frame: X aft from firewall front face, Y to starboard, Z up from fuselage belly. Units mm, g.
Masses are estimates until parts are weighed; edit ITEMS and re-run."""
import math

rho, g, nu = 1.225, 9.81, 1.5e-5

# ---- Wing (Selig S1223, constant chord, 2 panels + fuselage carry-through)
b, c = 1190.0, 240.0
S = b * c
AR = b / c
x_le = 170.0
CLmax = 1.8                           # 3D, S1223 (0.9 x ~2.0 section at Re ~150k, interp.)
cg_frac = 0.28
x_cg = x_le + cg_frac * c

# ---- Payload hopper: symmetric 60 deg V, 2 balls wide, rows 2-3-4 (18 slots), centred 12 mm AHEAD of the
#      design CG so the parked plane always rests tail-down (prop and nose stay off the ground)
ball_d, ball_m = 43.0, 45.0
x_hop = x_cg - 12.0
bay_front, bay_rear = x_hop - 121.0, x_hop + 121.0     # hopper top, outer (bottom = x_hop +/- 49)

# ---- Tail
lt = 600.0                            # CG -> horizontal tail AC
Sh_b, Sh_c = 500.0, 155.0
Sh = Sh_b * Sh_c - 54.0 * 55.0         # minus elevator centre gap at the fin (Y ±27)
Sv_h, Sv_root, Sv_tip = 160.0, 170.0, 120.0
Sv = Sv_h * (Sv_root + Sv_tip) / 2


def lift_slope(ar):
    return 2 * math.pi * ar / (2 + math.sqrt(ar ** 2 + 4))


a_w, a_t = lift_slope(AR), lift_slope(Sh_b / Sh_c)
deps = 2 * a_w / (math.pi * AR)
eta = 0.9
Vh = Sh * lt / (S * c)
Vv = Sv * lt / (S * b)
dh_fus = -0.04                        # fuselage destabilising shift (interp.)
h_np = 0.25 + eta * Vh * (a_t / a_w) * (1 - deps) + dh_fus

# ---- Mass items: (name, g, x)
x_batt = 58.0                         # battery in nose pod X 8-108
ITEMS = [
    ("motor ~35 mm class for 13 in prop (interp.)", 75, -21),
    ("13 in folding prop + spinner yoke (interp.)", 35, -52),
    ("battery 3S", 95, x_batt),
    ("ESC (in nose pod)", 25, 40),
    ("receiver (in nose pod)", 10, 85),
    ("nose pod shell + firewall", 25, 60),
    ("spine tube 16x14 carbon, 943 mm", 55, 475),
    ("printed wing clamps (front + rear) + bolts", 20, x_le + 100),
    ("wing (flat, continuous 10 mm spar)", 175, x_le + 0.40 * c),
    ("servos ail x2", 18, x_le + 67),
    ("servos ele+rud (on spine, ahead of wing)", 18, 152),
    ("servo load-port lids", 9, 486),
    ("servo side gates", 9, 96),
    ("hopper (2 mm depron/PETG skins, ridge floor)", 40, x_hop),
    ("side gates + port lids + linkages + chute", 25, x_hop + 120),
    ("tail mount + tail skid", 8, 900),
    ("tail surfaces (500 stab + fin)", 43, x_cg + 630),
    ("pushrods (carbon, 2 x 750 mm)", 10, 520),
    ("wiring/misc", 20, 150),
]
W_empty = sum(m for _, m, _ in ITEMS)
cg_empty = sum(m * x for _, m, x in ITEMS) / W_empty

if __name__ == "__main__":
    print(f"Wing: S={S/1e4:.2f} dm2  AR={AR:.2f}  MAC={c:.0f}  LE x={x_le:.0f}")
    print(f"Hopper centre x {x_hop:.0f} (top {bay_front:.0f}..{bay_rear:.0f})  battery centre x {x_batt:.0f}")
    print(f"Tail: Sh={Sh/1e4:.2f} dm2 Vh={Vh:.2f} | Sv={Sv/1e4:.2f} dm2 Vv={Vv:.3f}")
    print(f"Neutral point {h_np*100:.1f}% MAC (x {x_le+h_np*c:.0f})")
    print(f"Design CG {cg_frac*100:.0f}% MAC (x {x_cg:.0f}); static margin {(h_np-cg_frac)*100:.1f}%")
    print(f"Estimated empty CG x {cg_empty:.0f} ({(cg_empty-x_le)/c*100:.1f}% MAC), W_empty {W_empty} g")
    for n in (6, 8, 10, 12, 16):
        W = W_empty + ball_m * n
        q = W / 1000 * g / (S / 1e6)
        vs = math.sqrt(2 * q / (rho * CLmax))
        print(f"{n:2d} balls AUW {W} g  WL {W/(S/1e4):.1f} g/dm2  Vs {vs:.1f} m/s  Vcr {1.4*vs:.1f}  "
              f"Re {1.4*vs*c/1000/nu/1e3:.0f}k  qual {ball_m*n*100/W_empty:.1f}  T/W(max) {W_empty/W:.2f}")
