# Benchmark: Nitte Aero Club (Boeing National Aeromodelling Competition 2024-25 winners)

Source: `IIT-Madras-Boeing-SnapYT.App.mp4` (4 min, 640×360). It covers the competition at IIITDM Kancheepuram, 25–26 Jan 2025. I read it frame by frame; the audio is mostly music and adds no technical detail. Key frames are saved in [benchmark/](benchmark/).

The video doesn't give any dimensions, so everything below is read from the images. Treat sizes as approximate.

## What they built

| Area | What the video shows | Frame |
|---|---|---|
| Layout | High wing on top of a box fuselage, conventional tail, tractor prop in the nose | `nitte_airframe_tail.png` |
| **Airfoil** | **Strongly undercambered, very high-lift section** (S1223 / E423 class): thick, highly cambered top with a concave bottom, clearly visible in the tip rib | `nitte_wing_ribs_tip.png` |
| Wing structure | Built-up: **lightened lattice ribs** at ~60–70 mm spacing (truss cut-outs, white, looks laser-cut or printed), a solid sheeted leading edge (D-box) and a flat trailing-edge strip. Constant chord, no visible dihedral | both |
| Covering | **Clear film** (laminating/shrink type) bonded to the rib tops *and* bottoms so it holds the undercamber | `nitte_wing_ribs_tip.png` |
| Wing attachment | One-piece wing held on top of the fuselage with **rubber bands**, so it breaks away in a crash | `nitte_airframe_tail.png` |
| Fuselage | Slab-sided **white foam-board box**, tapering in plan to the tail, servos and linkages on the outside | `nitte_airframe_tail.png` |
| Tail | **Large** flat-plate stabiliser and fin (foam board), big elevator and rudder, mounted straight on the fuselage end | `nitte_airframe_tail.png` |
| Landing gear | **None.** Hand launch, belly landing on dirt | `nitte_belly_landing.png` |
| Flying | Hand-launched by one thrower, steady climb-out, flown high and slow, belly landing within the field | sheets 4–6 |

## What it means for us (reasoning)
1. **Their biggest advantage is the airfoil.** Our span is capped at 1.2 m, so payload is lift-limited, and lift at a safe speed is CLmax × area.
   - NACA 4412 gives a 3D CLmax of about 1.26. S1223 gives about 1.8, roughly 40% more lift from the same wing.
   - From [calc/airfoil_trade.py](calc/airfoil_trade.py):
     - At the same stall speed as rev D's 10-ball load (7.1 m/s), an S1223 wing lifts about 1.62 kg, which is ~20 balls. The bay holds 16.
     - Carrying **16 balls (AUW ≈ 1.43 kg)**, the S1223 wing stalls at **6.7 m/s**. That's *slower* than rev D with 10 balls.
     - The qualifier score goes from ~64 to ~**102**, and the main round earns 160 pts per trip instead of 100.
2. **The price is a strong nose-down pitching moment** (Cm ≈ −0.25 vs −0.09).
   - The tail has to push down with ~9% of the weight just to trim. On the rev D stab that means a tail CL of ~0.51, which is too high for a flat plate.
   - That explains their large tail. We grow the stab from 5.55 to **7.5 dm²** (500 × 155 mm), which raises Vh from 0.49 to 0.66.
   - Static margin rises to ~15% at the 28% CG, which suits a beginner.
3. **Induced drag goes up.** At AR 5 and CL ≈ 1.1, wing drag roughly doubles, to ~230 g at 9 m/s.
   - Our thrust cap (~700 g static) still leaves ~1.5–2 m/s climb, so this is fine.
   - Launches need a firm, level throw at full throttle.
4. **Lattice ribs and clear film** are the lightest practical way to build an undercambered wing.
   - Film only holds the concave bottom if it's glued to every rib bottom, so a foam-core wing would struggle with this airfoil.
   - Our balsa / 3D-printer kit can do it: laser-cut or CNC-cut 2 mm balsa ribs, or LW-PLA printed ribs.
5. **Foam-board box fuselage + belly landing + hand launch** matches rev D, which confirms the no-gear decision. Their prop sits on the normal nose line; ours is raised so the prop clears the ground on our flat-belly landing.
6. **Rubber-band wing mount.** We can't copy it directly, because our top hatch sits between the wing roots. The same breakaway idea works with **nylon M4 wing bolts** at the rear pins, which shear in a cartwheel instead of breaking the spar bulkhead.

## Changes adopted → rev E

| # | Change | Why |
|---|---|---|
| E1 | Airfoil **NACA 4412 → Selig S1223** (root = tip), same chord 240, span 1190, incidence +2° *(re-check incidence after the first glides)*, dihedral 3° | ~40% more lift. 16-ball design load at a lower stall speed |
| E2 | **Horizontal stab 400 × 145 → 500 × 155 mm** (incl. 50 mm elevators, 50 × 50 centre gap at the fin); elevator chord 50 → 55 mm | Trim the S1223 pitching moment with tail CL ≤ 0.4; Vh 0.66 |
| E3 | Wing structure: **lattice ribs** (2 mm balsa, laser-cut) at **60 mm** spacing; **LE D-box** of 1.5 mm balsa top and bottom to 15% chord; 3 mm balsa TE strip; Ø8 carbon spar tube at 28% chord (unchanged) | Light, holds the undercamber, stiff in torsion |
| E4 | Covering: **clear laminating/heat-shrink film**, glued to the rib bottoms with contact glue or a film iron | Keeps the concave lower surface. Also lets the judges see the structure |
| E5 | **Design load 16 balls** (bay already holds 16). Fly test loads 6 → 10 → 13 → 16 | Max score once the pilot is confident |
| E6 | **Nylon M4 breakaway bolts** at the rear wing pins (F3) | Crash tolerance, like their rubber bands |
| E7 | Keep: foam-board box fuselage, no gear, belly skid, side ramp doors, raised thrust line | Matches the benchmark and our rules |

## Rejected and why
- **One-piece rubber-banded wing**: it would cover the top loading hatch, which our hands-off loading rule needs.
- **A normal-height nose thrust line**: their nose sits higher off the ground, and our flat belly would put the prop tip in the dirt.
