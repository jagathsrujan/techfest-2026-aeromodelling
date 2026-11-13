# Rev H: aerodynamics and DFM/fit review (2026-11-04)

The team asked to stop refining the load/unload mechanisms (gates and lids stay as built in phase 4) and to put the effort into flight performance, design for manufacture, and how the parts fit together.

Scripts: `calc/planform_study.py` (lifting line, S1223 CLmax vs Re), `calc/drag_buildup.py` (parasitic build-up). Section and component data are approximate *(interp.)*; use them to rank options, not as absolute numbers.

## 1. What limits performance
- **Payload is set by wing CLmax** (stall speed at hand launch and landing), because the span is capped at 1.2 m.
- **Thrust is capped by the rules:** static thrust ≤ empty weight (T/W ≤ 1). At ~770 g empty the thrust is ≤ 770 gf, but AUW with 16 balls is ~1490 g, so T/W is only ≈ 0.5 loaded. **Climb and launch margin therefore depend on drag.** Every lightening step also lowers the allowed thrust, which makes drag matter even more.

## 2. Drag build-up at cruise (16 balls, 9.8 m/s, CL 0.87)

| Item | ΔCD | Share |
|---|---|---|
| Box hopper exposed face (sharp edges, flat front shoulders) | 0.029 | **21%** |
| Wing profile | 0.018 | 13% |
| Spine tube aft of wing (Ø16 cylinder, Re 10k) | 0.015 | 11% |
| Stab + fin | 0.007 | 5% |
| Tail mount, horns, rod exits | 0.005 | 4% |
| Pod | 0.004 | 3% |
| Induced | 0.051 | 36% |

**Current: L/D ≈ 6.2, 239 gf drag, 23 W.** With a faired fuselage: **L/D ≈ 7.7, 193 gf, 18.6 W (−19%).**

## 3. Planform study (span 1190, same area 28.6 dm²)

| Option | e | 3D CLmax | Vs at 1490 g | Cruise L/D | Build cost |
|---|---|---|---|---|---|
| A: rect 240 (current) | 0.96 | 1.66 | 7.10 | 10.9* | baseline |
| B: A + 2° washout | 0.97 | 1.64 | 7.14 | 11.0 | twist jig |
| C: rect centre ±300, outer taper 0.6 (266 → 160) | 0.99 | **1.78** | **6.85** | 10.9 | unique ribs (free on laser), angled rear spar, kinked aileron |
| E: B + 50 mm tip plates | 1.05 eff | 1.64 | 7.14 | 11.5 | +6 g |
| F: C + washout + tip plates | 1.07 eff | 1.76 | 6.89 | 11.5 | most complex |

\* Planform L/D uses the wing-alone parasitic (+0.012); the full aircraft is in §2.

Findings:
- All options stall at the root first (benign for a beginner). Washout buys nothing, so **build the wing flat on the board**.
- Tip plates give **+5% L/D for 6 g**: adopt.
- The taper (C) gives +7% CLmax, about +100 g payload at the same stall speed (~2 balls). That rests on the S1223 CLmax-vs-Re trend *(interp.)* and adds build complexity: the rear spar no longer sits at constant chord %, and the aileron crosses the panel break. **Team decision: rejected, keep rectangular.**

## 4. Trim, incidence, thrust line
- **Cruise pitch balance:**
  - Wing Cm −0.25 gives −1.03 N·m; lift 7 mm ahead of the CG adds +0.11 N·m.
  - The tail must provide ~1.5 N down, CLt ≈ −0.34.
  - Downwash ≈ 6°; fuselage attitude ≈ −0.2° (wing +2°). So **stab incidence ≈ +1° relative to the spine**, i.e. decalage +1°.
  - Build it into the TailMount stab saddle (+1°). Flight trimming handles the remaining uncertainty.
- **Thrust line:**
  - Thrust is at Z 110 and the CG at Z ~129, so the thrust line is 19 mm below the CG; the drag centre (wing at Z 160+) is above the CG. The aircraft will pitch up with power.
  - A 13 in prop gives strong torque and P-factor.
  - **Build 2° down and 2° right thrust into the MotorMount face** (free on a printed part). Re-check the folded-blade and pod clearances.

## 5. Aero changes for phase 4c
1. **Fuselage fairing (biggest win):**
   - Grow the nose pod into one faired shell covering the hopper front: elliptic nose from the firewall (Ø50 at X 0) to the full hopper section (Y ±59 + skin, Z 0–134) by X ≈ 150.
   - R12 rounds on the front vertical edges and the front belly edge. Gates and lids stay flush and untouched.
   - Add a tapering tail cone where the chute meets the spine (X 470 → ~560).
   - LW-PLA, 0.6 mm skin + 3 hoop ribs, target ≤ 14 g. Bolted with 2 × M3 into existing inserts; removable for battery access (or the battery hatch stays on top).
2. **Tip plates:** 2 mm balsa or 0.6 mm printed, 50 high (Z −15/+35 about the chord line), following the S1223 tip rib outline extended. The wing panel is shortened so that **total span including plates ≤ 1192**.
3. **Stab incidence +1°** in the TailMount saddle.
4. **MotorMount 2° down, 2° right.**
5. **Spine aft of the wing:** keep 14/12 from phase 4b. Optional: a 0.3 mm clear-film teardrop wrap. Not adopted; it gives about −0.005 CD for 4 g, so re-assess after flight testing.
6. Planform: **team decision 2026-11-04: keep the rectangular 240 chord** (option E: flat wing + tip plates). The taper is dropped.

## 6. DFM and fit rules (all parts)

**Fits**
| Joint | Fit |
|---|---|
| Carbon tube/rod in printed bore | OD + 0.15 |
| Carbon tube/rod in laser bore | OD + 0.10 |
| Printed clamp halves | 0.5 mm split gap, so bolts preload the tube |
| Heat-set M3 insert | Ø4.0 × 6 hole in an Ø8 boss (≥ 2 mm wall), insert axis normal to the print layers where possible |
| M3 pass hole | Ø3.4 |
| Hinge pins | Ø + 0.2 in printed knuckles |

**Anti-rotation**
- The round spine in round clamps can roll the wing relative to the tail.
- Index it with one M3 cross-bolt through the spine at the front wing clamp, plus a printed key at the TailMount.
- Glue is not relied on for indexing.

**Print orientation (Bambu H2D)**
- Every printed part gets a stated build orientation: load paths along the layers; bores vertical where tolerance matters; no support inside insert bosses.
- PA-CF for structural nodes (clamps, motor mount, tail mount); LW-PLA for shells (hopper, pod, fairing, chute); PETG for brackets.
- The H2D's dual nozzle can print PVA/PETG support interface for PA-CF.

**Laser parts**
- Kerf 0.12 mm balsa, 0.15 mm lite-ply. Nest on 600 × 400 sheets; export DXFs per sheet.
- Ribs get tab-and-slot feet into a laser-cut building jig (flat wing on the board).
- LE sheets are split at Y 0 with a 30 mm doubler.
- Rib, spar and TE slots are sized for the actual stock thickness, with a measure-then-adjust alias in Params.

**Assembly**
- Every fastener reachable with a 2.5 mm ball driver once the neighbouring parts are installed.
- Assembly order: spine → pod/hopper → wing clamps → wing → tail. Documented in an exploded drawing.

**Field repair**
- Wing, tail, pod and motor mount each come off with ≤ 4 bolts.

## 7. Key checks (phase 4c)
- Span including plates ≤ 1192.
- Fairing mass ≤ 14 g; no clash with the gates at 0–90° or the lids at 0–90°.
- The folded prop blades clear the fairing.
- MotorMount angles of 2°/2° measured from the face normal.
- Stab +1° measured on the stab chord line.
- All carbon bores at the fit table values.
- Every printed part has an orientation note and fits the H2D bed (325 × 320 × 325).
- Laser DXFs exported and nested.
- BOM: empty mass ≤ 800 g, CG X 225–240.
