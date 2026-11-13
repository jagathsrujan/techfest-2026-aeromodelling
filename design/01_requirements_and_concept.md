# Techfest 2026-27 Aeromodelling — Requirements & Concept (rev A, 2026-11-03)

Status: **draft concept for team review.** Numbers marked *(est.)* are first-pass estimates and get replaced by measured weights and thrust as parts arrive.

## 1. Requirements (from the rulebook)

| # | Requirement | Value | Design consequence |
|---|---|---|---|
| R1 | Empty weight | ≤ 1000 g | Target **≤ 650 g**: it divides the qualifier score |
| R2 | Wingspan | ≤ 1200 mm, zero tolerance | Design **1190 mm** tip to tip, measured over the tips |
| R3 | Propeller | ≤ 13 in, not metal | 9–11 in is plenty |
| R4 | Static thrust / empty weight | ≤ 1 | Thrust ≤ ~650 g. Cap it with a transmitter endpoint if the motor makes more |
| R5 | Payload | 45 g, Ø43 mm golf balls, fully internal | Enclosed bay, no exposed balls |
| R6 | Loading / unloading | Hands-off, doors on the transmitter, plane on the ground | Servo hatches plus ground clearance under the bay |
| R7 | Launch | Hand launch allowed | Landing gear is for landing and ground unloading only |
| R8 | Flight | ≥ 30 s per leg, 3 min for the whole mission | Endurance is trivial; ground time is what costs points |
| R9 | Banned | Gyros, receiver programming, programmed mission steps, FPV, RTF/ARF/BNF | Plain receiver, manual switches, our own airframe |
| R10 | Landing | Inside the inner boundary (−20%); touching the outer boundary disqualifies | Slow, docile, short landing |
| R11 | Same aircraft in both rounds, repairs only | Must be robust and field-repairable | Carry spare props, servos and foam |

**Scoring logic**
- Qualifier = 45 × balls × 100 / empty weight. Main = Σ(10 × balls) − ground seconds.
- Each extra ball earns about 10 points per trip and costs about 1–2 s of loading time, so we want as many balls as the airframe flies safely.
- The empty weight is both the qualifier denominator and the thrust cap, so **light and efficient beats powerful**.

## 2. Team resources
- **Materials:** XPS foam, Depron, balsa, film covering, 3D printers, carbon rods/tubes (COTS).
- **Electronics already owned:** transmitter + receiver, motor + ESC + props, LiPos + charger, servos. **Specs still needed** (see §8).
- **Pilot:** beginner / some sim time. The plane must be very stable and slow, and forgive mistakes.
- **CAD:** FreeCAD, driven by Claude.

## 3. Concept: high-wing, conventional-tail "payload trainer"
- **High wing with dihedral** (~3–4°): sits on top of a box fuselage, self-levelling and beginner-friendly.
- **Constant-chord wing**, 1190 × 240 mm: easy to build, docile at the stall.
  - Balsa spars and ribs with film covering, or an XPS core with a carbon spar. The choice is in §6.
  - **2 piece** plugged into a carbon tube joiner, for transport and repair.
- **Box fuselage** from Depron/balsa with an internal payload bay **centred on the CG**, so the CG doesn't move when balls go in or out.
- **Tractor motor in the nose** to balance the bay and the tail.
- **Conventional tail** on a carbon tail boom or a tapered foam boom; elevator and rudder.
- **Controls:** ailerons (2 servos or 1 centre servo), elevator, rudder, throttle, plus 2 payload channels.
- **Fixed landing gear** (carbon/printed): gives belly clearance for balls to drop out and survives grass landings.
  - A tricycle layout is easiest for a beginner to land.

## 4. First-pass sizing *(est.)*

Wing: span 1190 mm, chord 240 mm, area **28.6 dm²**, AR **5.0**. CLmax ≈ 1.3 is assumed (Clark-Y / NACA 4412 class).

| Balls | AUW (g) | Wing loading (g/dm²) | Stall (m/s) | Cruise ~1.4 Vs (m/s) | Qualifier score | Loaded T/W (thrust = 655 g) |
|---|---|---|---|---|---|---|
| 6 | 925 | 32.4 | 6.3 | 8.8 | 41 | 0.71 |
| 8 | 1015 | 35.5 | 6.6 | 9.3 | 55 | 0.65 |
| **10** | **1105** | **38.7** | **6.9** | **9.7** | **69** | **0.59** |
| 12 | 1195 | 41.8 | 7.2 | 10.1 | 82 | 0.55 |

**Proposed design point: 10 balls (450 g) with a bay sized for 12.**
- Fly 6–8 first, then work up as the pilot gains confidence.
- Everything up to 12 stays slow (stall < 7.5 m/s) with T/W > 0.5, which is enough for a hand launch and climb.

**Tail (volume coefficients Vh 0.5, Vv 0.04, tail arm ~600 mm)**
- Horizontal: ~5.7 dm², e.g. 400 × 145 mm.
- Vertical: ~2.3 dm², e.g. 160 tall × 145 mm average chord.

**Fuselage** *(est.)*
- About 900 mm long, ~100 mm wide (two balls side by side), ~90 mm tall at the bay.
- Nose about 200 mm.

### Weight budget *(est., target 655 g)*

| Item | g |
|---|---|
| Motor + prop | 70 |
| ESC | 25 |
| Battery (3S ~1000–1300 mAh) | 95 |
| Receiver + 6 servos | 65 |
| Wing (incl. joiner) | 170 |
| Fuselage + bay | 110 |
| Tail + boom | 35 |
| Payload doors + linkages | 25 |
| Landing gear | 40 |
| Wiring, glue, misc | 20 |
| **Total** | **655** |

## 5. Payload mechanism concept
- **Bay:** 2 rows × 6 = 12 balls, about 270 L × 95 W × 50 H mm, centred on the CG between the wing spars.
- **Loading: top hatch.**
  - A servo flips open a hatch in the fuselage top, behind the wing leading edge or between the two wing halves.
  - A printed funnel guides the balls into the two rows, and the loader drops them in.
  - The hatch closes, which stops the C1/C2b clock.
- **Unloading: bottom bomb-bay doors.**
  - One servo drives two belly doors that open downward. The bay floor is the doors themselves.
  - The balls fall and roll clear, which ends C2a/C3.
  - The gear must give **≥ 70 mm belly clearance** so the open doors and the falling balls clear the ground.
- **Channels:** two separate transmitter switches (hatch, belly doors), with no mixing.
  - The rules ban "programming" for mission steps, so we stay clearly legal by using plain switch channels. **Confirm with the organisers before the competition.**
- **Ground-time targets:**
  - Loading 10 balls takes about 8–10 s (they go in two at a time).
  - Unloading takes about 2 s.

## 6. Open decisions
1. **Wing construction.** Choose one:
   - Balsa ribs + spar + film: lightest, ~140–170 g.
   - XPS hot-wire core + carbon spar + tape/film: tougher and faster to build, ~180–220 g.
   - *Suggestion:* balsa built-up wing for weight, with a carbon tube spar.
2. **Airfoil.** Choose one:
   - Clark Y: flat bottom, easy on a building board.
   - NACA 4412: CLmax ~1.5.
   - High-lift undercambered (E423 / S1223): harder to build and cover.
   - *Suggestion:* NACA 4412 or Clark Y.
3. **Gear layout:** tricycle (easiest landings) or taildragger (lighter).
4. **Number of balls to commit to in the abstract** (form asks "Maximum number of golf balls").

## 7. Next steps
1. Team fills in the electronics specs (§8) and weighs each part.
2. Freeze the concept: wing build, airfoil, gear, bay size.
3. Detailed sizing: CG/neutral point, static margin, control surfaces, motor/prop thrust check.
4. Write the FreeCAD modelling plan, then build the model. Outputs: three-view, isometric, STEP.
5. Build, flight test, measure thrust and weights.
6. Fill in the abstract before **25 Nov 2026**, with 5–10 build photos.

## 8. Electronics data needed from the team
- Motor: model, kV, weight.
- ESC: amp rating, weight.
- Props available (diameter × pitch).
- Battery: cells, mAh, C rating, weight.
- Servos: model, weight, torque.
- Transmitter: model, number of channels.
- Receiver: model, number of channels.
