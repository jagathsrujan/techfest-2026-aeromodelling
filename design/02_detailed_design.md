# Detailed Design — rev E (2026-11-03)

> Rev E adopts the lessons from the Nitte Aero Club benchmark ([04_benchmark_nitte.md](04_benchmark_nitte.md)): S1223 high-lift wing, a bigger tail, lattice-rib + clear-film construction, and a 16-ball design load. **The CAD model is still rev D** (NACA 4412, small tail) until it is rebuilt.

This builds on [01_requirements_and_concept.md](01_requirements_and_concept.md) (concept approved by the team). The numbers come from [calc/sizing.py](calc/sizing.py): re-run it whenever a weight or dimension changes. Items marked *(interp.)* are assumptions to confirm once parts are weighed or tested.

## Decisions adopted (rev B, structure revised in rev C)

| Topic | Choice | Why |
|---|---|---|
| Layout | Shoulder wing, pod-and-boom fuselage, conventional tail, **no landing gear**: hand launch, belly landing | Stable for a beginner. Dropping the gear saves ~55 g, and the rules allow hand launch and landing anywhere on the ground |
| Wing build | 2 built-up panels: 2 mm balsa **lattice ribs** at 60 mm, 1.5 mm balsa LE D-box to 15% chord, 3 mm TE strip, Ø8 carbon spar; **clear film** glued to the rib tops and bottoms (rev E) | Lightest option that holds an undercambered section (benchmark) |
| Airfoil | **Selig S1223**, root = tip (rev E; was NACA 4412) | Section CLmax ≈ 2.0 at Re ≈ 150k (3D ≈ 1.8), ~40% more lift than NACA 4412 on our span-capped wing. Cost: Cm ≈ −0.25, so the tail is bigger |
| Payload bay | 2 wide × 4 long × 2 layers = **16 slots**; **design load 16 balls** (rev E); test ladder 6 → 10 → 13 → 16 | Rev A's 2 × 6 bay left nowhere for the battery. The shorter two-layer bay frees the nose |
| Payload channels | 2 plain switch channels (top hatch, side ramp doors), no mixing | Clearly legal under the "no programming" rules |
| Gear | **None** (rev D). Replaceable belly skid | Team decision: save weight |
| Prop | **13 in folding prop** on a centred thrust line (rev F; replaces the rev D raised nose pylon) | Team wants a clean nose and a 13 in prop. A rigid 13 in prop would need the hub ~190 mm up to clear the ground on a gearless belly. A folding prop folds flat when the motor stops, so the plane belly-lands. A big, slow prop also gives more thrust per watt at our low speeds |
| Unloading | **Side ramp doors** (rev D): a fixed ridged floor, and one servo drops a door on each side flat onto the ground | Works with the plane resting on its belly. The ridge also self-centres the balls into their rows when loading |

> **Why 16 slots?** The wing spar carry-through is a 12 mm-thick bulkhead at the CG. It splits the bay into front and rear halves (2 × 2 × 2 each). Nothing crosses the hatch opening, and the bay stays centred on the CG, so loading doesn't change the trim.

## Global frame (used by all CAD and drawings)
- **Origin:** front face of the firewall, on the centreline, at belly level.
- **+X** aft along the fuselage datum, **+Y** to starboard, **+Z** up. Belly (bottom of the fixed bay floor) is at Z = 0. Rev D has no gear: the plane rests on a 1 mm belly skid, so the ground is at Z = −1.
- All dimensions are in mm.

## Wing

| Parameter | Value |
|---|---|
| Wingspan (projected) | **1190** (±595), inside the 1200 limit with no tolerance |
| Root / tip chord | 240 / 240 (constant) |
| MAC | 240 |
| Wing area | 285 600 mm² (28.56 dm², incl. fuselage carry-through) |
| Aspect ratio | 4.96 |
| Airfoil (root/tip) | S1223 (12.1% thick, 8.1% camber, undercambered) |
| Sweep | 0° |
| Dihedral | 3° per panel, hinged at the root |
| Incidence | +2° to the fuselage datum |
| Root LE | X 170, **Z 100** (chord line; lowered in rev E because S1223 sits higher on its chord), panel root at Y ±50.5 (fuselage side) |
| Spars | One Ø8 carbon tube per panel at X 237, 3° dihedral. Each plugs 48 mm into a socket inside the **spar bulkhead**. The tubes don't cross the fuselage |
| Rear locating pins | Ø4 carbon at X 331.5 into sockets in bulkhead F3 |

## Fuselage (pod + boom)

| Parameter | Value |
|---|---|
| Length, firewall to tail TE | 946 |
| Overall incl. spinner | ~995 |
| Pod outer width / height | 101 / 135 (X 70–400). **Streamlined nose** (rev F): lofts from a 50 wide × 62 tall firewall (Y ±25, Z 30–92) at X 0 to the full section at X 70. A **prop-blade channel** (30 mm wide, ceiling from Z 40 at X 0 sloping to Z 0 at X 110, 3 mm liner) is recessed into the belly centreline. A folded lower blade nests in it (tip ≈ 1 mm above the belly line) instead of sticking out below the belly |
| Nose length (firewall → wing LE) | 170 |
| Boom | Ø12 carbon tube, X 333–890, axis Z 110. Socketed in bulkhead F3 and the tail-cone end wall (two supports); ply saddle under the stab |
| Battery tray | X 20–140, Z 40–75 (centre X 80, slides for trimming). ESC moved behind F3 (X 340–390) with a motor-side wire extension, to balance the heavier 13 in prop set |
| Payload bay (internal) | Front half X 144–231, rear half X 243–330, W 95, H 129 (Z 3–132) |
| Structure (rev C) | 3 mm ply bulkheads F2 (X 141–144) and F3 (X 330–333). Spar bulkhead X 231–243 (2 × 3 mm ply webs + 6 mm balsa core, carbon caps top and bottom, full depth Z 3–132). 3 × 3 carbon longerons along the 4 bay-opening edges. the lower longerons become external door headers at Z 59–62 (rev D) |
| Thrust line | **Z 67** (centred on the nose, ~at the loaded CG height), 0° down / 0° right *(interp.; shim after the first flights)*. 13 in folding prop on a Ø44 spinner yoke. **Unfolded, the prop reaches ~98 mm below the belly, so the motor must be OFF before touchdown** (the blades then fold back) |

## Empennage

| Parameter | Value |
|---|---|
| Horizontal stabiliser | **Span 500 × chord 155** (incl. 55 mm elevator), area **74 530 mm²** (54 × 55 gap between the elevator halves at the fin), TE X 946, on a ply saddle on the boom (rev E) |
| HT arm (CG → AC) | 600 |
| Tail volume Vh | **0.66** (sized to trim the S1223 moment with tail CL ≤ 0.4) |
| Vertical stabiliser | Height 160, root 170, tip 120, area 23 945 mm² (incl. rudder), TE X 946 |
| VT arm (CG → AC) | ~600 |
| Vv | 0.041 |
| Material | 5 mm Depron or 3 mm balsa sheet, flat plate |

## Control surfaces

| Surface | Length × chord | Area (mm²) |
|---|---|---|
| Aileron (each) | 380 × 55 (Y 205–585) | 20 900 |
| Elevator | 2 halves, each 223 × 55 (Y ±27–250, clears the 55 mm rudder at full throw), joined by a Ø1.5 wire | 24 530 |
| Rudder | 159 × 55 (hinge X 891, same as the elevator; 1 mm above the stab) | 8 745 |

## Stability *(est.)*
- Neutral point: 43.2% MAC (X 274) with the rev E tail.
- Design CG: 28% MAC (X 237). Static margin 15%. The CG may move aft to ~33% MAC (margin ~10%) once the pilot is comfortable, which reduces trim drag.
- Estimated empty CG with the battery at X 80: X 230 (25% MAC, margin ≈ 12%). That is slightly nose-heavy, which is safe for a beginner. Trim it by sliding the battery.
- The balls are centred at X 237, so 10 balls move the CG only ~3 mm aft.

## Weight and performance *(est., replace with measured values)*
- Empty weight is **≈ 739 g** (rev F). The 13 in motor and folding prop set adds ~40 g; dropping the nose pylon saves 10 g.
- Limits: static thrust must be ≤ ~739 g, and a 13 in prop will almost certainly need a throttle endpoint cap.
  - **Check the motor:** a 13 in prop on 3S needs a low-kV motor (~700–900 kV, 28xx/35 mm class). A high-kV motor will overheat.
- Estimated empty CG is X 230 (25% MAC), with the ESC moved aft.
- The thrust line is now on the CG height, so throttle no longer pitches the nose.
- S1223 performance (rev E, 3D CLmax 1.8):

| Balls | AUW (g) | Wing loading (g/dm²) | Stall (m/s) | Cruise (m/s) | Qualifier score | Max loaded T/W |
|---|---|---|---|---|---|---|
| 6 | 1009 | 35.3 | 5.6 | 7.8 | 37 | 0.73 |
| 10 | 1189 | 41.6 | 6.1 | 8.5 | 61 | 0.62 |
| 12 | 1279 | 44.8 | 6.3 | 8.8 | 73 | 0.58 |
| **16** | **1459** | **51.1** | **6.7** | **9.4** | **97** | **0.51** |

- Induced drag at CL ≈ 1.1 roughly doubles the wing drag (~230 g at 9 m/s). There is still ~1.5–2 m/s of climb within the thrust cap. **Launch with 16 balls: full throttle, firm level throw.**

- **Hinges:** the tail surfaces are 5 mm sheet. Bevel the hinge edges (45° V-groove) on the stab/elevator and fin/rudder so they reach ±20° and ±25° without the corners touching. The CAD shows square edges that overlap slightly at full throw.

## Payload mechanism
- **Top hatch (loading)**
  - A 3 mm balsa/printed lid covers the bay top, X 144–330, between the wing roots, hinged along its port edge.
  - One servo at X ~130 flips it open to ~100°.
  - The loader drops balls into the front and rear halves. Dimpled printed liners on the doors keep them in their slots.
- **Side ramp doors (unloading), rev D**
  - The bay floor is now **fixed**: 3 mm ply with a balsa ridge, 8 mm high on the centreline, sloping ~10° down to each side.
  - Each side wall has a door opening X 144–330, Z 3–58. The door (3 mm balsa, 186 × 57, 1 mm gap at the top edge) is hinged along its bottom edge at Y ±50.5, Z 3.
  - One servo (X ~350) drives both doors through two pushrods and torque rods along the hinge lines, opening each door ~90° outward.
  - With the plane on its belly, the open doors lie flat on the ground as ramps. Each row rolls out sideways, and the top layer drops and follows.
  - When loading, the balls roll against the closed doors and sit in two rows automatically.
- **Loading pattern for 10 balls:** all 8 bottom slots, plus 1 top slot in each half on the inner column, so the payload stays symmetric about the CG.

## Landing / ground handling (rev D: no gear)
- **Hand launch:** grip the fuselage under the wing (at the bay sides) and throw level at about 70% throttle. The prop is at the nose, well ahead of the hand. The blades spring open as soon as the motor spins up.
- **Belly landing:** cut the throttle before touchdown so the folding prop stops and folds back. Touch down on the 1 mm replaceable belly skid (polycarbonate or ply under packing tape, X 110–400, aft of the blade channel).
- **At rest:** the plane sits level on its flat belly. The wing roots (Z ≥ 104), the boom (Z ≥ 104) and the tail are all clear of the ground.

## Open items (need team input)
- Real motor, prop, ESC, battery, servo and transmitter specs. These affect the nose length, prop clearance and the T/W cap.
- Confirm with the organisers that two switch-operated payload channels are acceptable.
- Wing retention method (nylon bolt at the rear pins, or a rubber band over the wing roots).
