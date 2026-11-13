# Rev H — build-ready, parametric, assembled model (plan)

Rev G ([05_revG_spine_hopper.md](05_revG_spine_hopper.md), `cad/TechfestPlane_revG.FCStd`) fixed the layout. All its envelope numbers (frame, positions, sizes) carry over unchanged. Rev H turns that layout into **parts you can actually make and bolt together**:
- every part is a fully constrained, spreadsheet-driven PartDesign body;
- each part is drawn in its own manufacturing frame;
- a FreeCAD **Assembly** (built-in Assembly workbench, FreeCAD 1.1) places the parts with joints. Control surfaces, gates and lids hinge on revolute joints.
- fasteners, inserts, hinges and linkages are modelled;
- the BOM and weight come from the real volumes.

Team inputs:
- **Fabrication:** laser cutter and Bambu Lab **H2D** printer (single-nozzle volume ≈ 325 × 320 × 325 mm).
- **Material priority:** maximum strength-to-weight. Print as much as is sensible, with FEM-driven organic shapes on the loaded nodes.
- **Fasteners:** M3 bolts + brass heat-set inserts.

## 1. Construction philosophy (strength-to-weight)
- **Long members are carbon:** spine, wing spars, pushrods, elevator joiner.
- **Wide flat structure is laser-cut balsa / lite-ply:** wing ribs, sheeting, tail surfaces. Per gram it beats printing for thin flat parts.
- **Nodes are printed.** Wherever loads change direction (wing–spine clamps, motor mount, tail mount, hinges, servo trays) the part is printed in **PETG-CF or PA-CF** (stiff, tough). The three most loaded nodes then get **topology optimisation** (FreeCAD FEM + CalculiX BESO loop, phase 5) to get organic, minimum-mass shapes.
- **Shells are printed thin in LW-PLA** (foamed, ~0.55 g/cm³): nose pod, hopper, chute, gates, lids. They use single walls of 0.6–0.8 mm with integral grid stiffeners. Each fits the H2D bed in one piece.
- Every bolted joint uses **M3 SHCS into M3 × 5.7 brass heat-set inserts**: insert hole Ø4.0 × 6 deep, boss OD ≥ 8. Pass-through holes are Ø3.4.

## 2. Modelling rules (for the builder)
- **Master spreadsheet `Params`** holds every driving dimension with an alias (list in §5). No magic numbers in sketches: every sketch dimension is either an expression on `Params` or a local construction value written in the sketch name.
- **One PartDesign Body per manufactured part.**
  - Sketches must be **fully constrained (DoF = 0)**. Check `sketch.solve() == 0` and `len(sketch.MalformedConstraints) == 0`, and print the DoF each time.
  - Use Pad, Pocket, Revolution, Loft, Fillet and Chamfer.
  - Select fillet and chamfer edges geometrically, never by index. Fillets are allowed only on printed parts.
- **Each body is drawn in its own manufacturing frame:**
  - laser-cut parts flat in XY with Z thickness;
  - printed parts on the print bed with Z up;
  - tubes along Z from 0.

  Each body carries an **LCS (`PartDesign::CoordinateSystem`) at every mating point**, named `LCS_<mate>` (e.g. `LCS_spine` on a clamp sits on the spine bore axis).
- **Assembly:** create `Assembly` (Assembly workbench) holding App::Links to the bodies.
  - **Ground the Spine.**
  - Place parts with **Fixed joints between LCS pairs**.
  - Use **Revolute joints** for the ailerons, elevators, rudder, side gates and port lids.
  - If the scripted joint API refuses a reference, fall back to setting the Link `Placement` by expression from `Params`. Keep the revolute joints if at all possible, and report every fallback.
- Repeated parts (ribs, inserts, bolts, servos) are **one body + App::Link copies** (or Link arrays), not duplicated geometry.
- **Do not touch** the rev G and rev B documents. Rev H goes in its own file.

## 3. Part list (manufacturing breakdown)

### A. Fuselage / payload structure

| Body | Make | Material | Description |
|---|---|---|---|
| `Spine` | Cut | CF tube 16/14 | L 943; drill Ø3.4 cross-holes at the clamp stations |
| `NosePod` | Print | LW-PLA, 0.6 mm wall | Rev G nose shape (X 0–~138). Hollow, with 3 internal frames at X 3, 50 and 100, each with a Ø16.2 spine bore (the spine passes along the pod top). Starboard **battery hatch** opening X 10–110, Z 80–125 with a 3 mm lip. Rear face mates the hopper front wall: 2 insert bosses, so the pod bolts to the hopper. Front face carries the `MotorMount` (4 insert bosses on a Ø44 bolt circle) |
| `BatteryHatch` | Print | LW-PLA | Hatch for the opening above; 2 Ø6 × 2 magnet pockets plus matching pockets in the pod lip |
| `MotorMount` | Print (TO in phase 5) | PA-CF / PETG-CF | Cross plate for the 35 mm motor (16 × 19 M3 pattern), 4 bolts to the pod. Thrust axis Z 110 in aircraft frame |
| `Hopper` | Print | LW-PLA 0.8 mm + 1.2 mm grid ribs | Rev G V-hopper (outer bottom X 176–274 at Z 0, top X 104–346 at Z 134, Y ±59), integral ridge floor, side-gate openings, and an aft wall opening to the chute. The top flange carries **two spine saddles** at X 237 and X 338. These are the lower halves of the wing clamps: they wrap the bottom half of the spine with 4 insert bosses each. A Ø16.2 half-bore runs along the top centreline |
| `Chute` | Print | LW-PLA 0.8 mm | Rev G chute (X 302–470), separate print, bolted to the hopper aft flange (2 × M3). The load port is open on top; 2 lid hinge knuckle rows sit along the spine sides (Y ±10) |
| `Gate_L` / `Gate_R` | Print | LW-PLA + PETG hinge knuckles | Rev G gate panels (92 × 57) with ribs, 3 knuckles on the bottom edge, and a torque horn on the front knuckle |
| `PortLid_L` / `PortLid_R` | Print | LW-PLA | Rev G lids, 2 knuckles each on the spine-side edge plus a horn |
| `HingePin` ×4 | Cut | Ø1.5 steel / CF rod | Gate and lid hinge pins |
| `BellySkid` | Cut | 1 mm polycarbonate | Rev G skid under the hopper bottom, held with tape (not modelled as a fastener) |

### B. Wing (one piece, flat, S1223, chord 240, span 1190)

| Body | Make | Material | Description |
|---|---|---|---|
| `Rib` | Laser | 2 mm balsa | S1223 at chord 240, **minus** the LE sheeting (1.5 mm) up to 15% c and the TE strip. Ø10.2 front-spar hole at 28% c, Ø4.2 rear-spar hole at 70% c. 3–4 triangular lightening holes, ≥ 5 mm web. Aileron cut line at 77% c. **Qty 20**, at Y = ±(42, 100, 160 … 580); the spacing is ~60 mm, and the two root ribs straddle the clamps |
| `RootRib` | Laser | 3 mm lite-ply | As `Rib` but solid near the spars, with 2 bolt holes. Qty 4, at Y ±20 and ±42 (either side of each clamp bay) |
| `Spar_Front` | Cut | CF tube 10/8 | L 1170, Y ±585 |
| `Spar_Rear` | Cut | CF rod/tube Ø4 | L 1170 |
| `LE_Sheet_Top` / `LE_Sheet_Bot` | Laser | 1.5 mm balsa | D-box skins following the S1223 contour from the LE to 15% c (modelled as thin lofted shells), full span |
| `TE_Strip` | Cut | 3 × 10 mm balsa, shaped | At 77% c, the rear of the fixed wing / the aileron hinge line |
| `Aileron_L` / `Aileron_R` | Laser + sheet | 3 mm balsa | 55 mm chord tapered sheet section, Y 205–585 |
| `WingClampCap_F` | Print (TO in phase 5) | PA-CF | Upper half of the front clamp. It wraps the top half of the spine and the whole front spar, sits between the root ribs, and has 4 M3 bolts down into the hopper saddle inserts |
| `WingClampCap_R` | Print (TO in phase 5) | PA-CF | The same for the rear spar at X 338 |
| `ServoTray_Ail` ×2 | Print | PETG | Tray glued between the ribs at Y ±150; 9 g servo pocket plus 2 screw bosses; balsa cover hatch |
| `Covering` | — | Clear film | **Visual only:** a 0.05 mm transparent skin, or skip it. Not part of the BOM mass (BOM adds 25 g/m² × area) |

### C. Tail

| Body | Make | Material | Description |
|---|---|---|---|
| `TailMount` | Print (TO in phase 5) | PA-CF | Sleeve over the spine end (X 780–946) with 2 M3 pinch bolts. Flat saddle for the stab at Z 150, a slot for the fin root, and an integral tail skid underneath |
| `Stab` | Laser | 3 mm balsa (or 5 mm Depron) | Rev G stab, X 791–891, Y ±250 |
| `Elevator_L` / `_R` | Laser | 3 mm balsa | Rev G elevators, Y ±27–250 |
| `ElevatorJoiner` | Bend | Ø1.5 steel | U-wire |
| `Fin` / `Rudder` | Laser | 3 mm balsa | Rev G fin and rudder |
| `ControlHorn` ×4 | Print | PETG | Elevator, rudder and 2 ailerons |

### D. Systems

| Body | Qty | Notes |
|---|---|---|
| `Servo9g` | 7 | 23 × 12.5 × 22 mm + tabs; one body, linked. Locations: 2 aileron, elevator, rudder, gate, lid, plus a spare slot if needed |
| `Pushrod` | 6 | Ø2 CF rod + printed or metal clevis ends: ele and rud (from servos at X 140–163 along the spine, in 3 printed `PushrodGuide` clips), 2 ailerons, gate, lid |
| `PushrodGuide` | 3 | Printed clip on the spine at X 450, 600, 750 |
| `Motor35` | 1 | Ø35 × 40 plus shaft |
| `FoldingProp13` | 1 | Spinner yoke Ø44 plus 2 blades (165 mm each from the axis) as real blade shapes, open (flight) pose |
| `Battery3S` | 1 | 100 × 35 × 30 on a printed tray in the pod, with a Velcro strap (visual) |
| `ESC`, `Receiver` | 1 each | Rev G positions |
| `M3_SHCS_<L>` | per joint | Lengths 8 / 10 / 12 / 16 / 20, simple head + shank, linked |
| `M3_Insert` | per boss | Ø4.0 × 5.7 knurl-free cylinder, linked |

## 4. Assembly joints
- **Ground:** `Spine`.
- **Fixed joints:**

| Part | Mates to | Station |
|---|---|---|
| `Hopper` saddles | `Spine` | X 237 and X 338 |
| `WingClampCap_F` / `_R` | `Spine` | same stations |
| Wing group (ribs, spars, sheeting, strip) | `WingClampCap` | via the spar axes |
| `NosePod` | `Spine` | frames |
| `NosePod` | `Hopper` | front wall |
| `MotorMount` | `NosePod` | |
| `Motor` | `MotorMount` | |
| `Prop` | `Motor` | |
| `Chute` | `Hopper` | |
| `TailMount` | `Spine` | X 780–946 |
| `Stab`, `Fin` | `TailMount` | |
| Servos | their trays/mounts | |
| Bolts and inserts | their bosses | |

- **Revolute joints:**

| Part | Hinge axis | Range |
|---|---|---|
| `Aileron_L` / `_R` | X 355 | ±20° |
| `Elevator_L` / `_R` | X 891 | ±20° |
| `Rudder` | X 891 | ±25° |
| `Gate_L` / `_R` | Bottom edge | 0–90° |
| `PortLid_L` / `_R` | Y ±10 | 0–100° |

## 5. `Params` spreadsheet (aliases → value, mm)
Wing:
- `span 1190`, `chord 240`, `x_le 170`, `z_le 160`, `incidence 2`
- `spar_f_x 0.28`, `spar_f_d 10`, `spar_r_x 0.70`, `spar_r_d 4`
- `rib_t 2`, `rib_pitch 60`, `le_sheet_t 1.5`, `le_sheet_x 0.15`, `ail_chord 55`, `ail_y0 205`, `ail_y1 585`

Spine:
- `spine_od 16`, `spine_id 14`, `spine_z 142`, `spine_x0 3`, `spine_x1 946`

Hopper and payload:
- `hop_xc 225`, `hop_bot_half 49`, `hop_top_half 121`, `hop_h 134`, `hop_w 118`, `hop_wall 0.8`, `ridge_h 8`
- `gate_len 92`, `gate_h 57`, `chute_x1 470`, `port_x0 415`, `port_w 46`
- `ball_d 43`

Nose and motor:
- `pod_x1 138`, `thrust_z 110`, `motor_d 35`, `prop_d 330`

Tail:
- `stab_x0 791`, `stab_x1 891`, `stab_span 500`, `elev_chord 55`, `elev_gap 27`, `fin_h 160`
- `tail_t 3`, `tailmount_x0 780`

Fasteners:
- `m3_clear 3.4`, `insert_d 4.0`, `insert_depth 6`, `boss_d 8`

## 6. Phases (one Sonnet agent each, run in sequence, each saving the same file)
1. **Params + fuselage structure (§3A)** with LCSs. Check the sketches' DoF and validity, and that the hopper still holds the 10 balls (temporary spheres).
2. **Wing (§3B):** the rib body plus the Link array, spars, sheeting, TE, ailerons, clamp caps and servo trays.
3. **Tail + systems + fasteners (§3C, §3D).**
4. **Assembly + joints** (§4), exploded view, BOM CSV and checks (§7).
5. **Topology optimisation** of `WingClampCap_F`, `MotorMount` and `TailMount`: BESO with CalculiX on a gmsh tet mesh, using the design load cases below. Turn the result into a smoothed solid, check it with FEM (stress < 0.5 × material strength, i.e. a safety factor ≥ 2), then swap it into the assembly.

Design load cases for phase 5 (AUW 1.46 kg, 16 balls):
- **Wing clamps:** 4 g manoeuvre, so wing lift = 57 N on the front clamp (≈ 80 %) plus the wing pitching moment Cm −0.25 at 12 m/s (≈ 1.8 N·m), carried as a couple between the two clamps.
- **Motor mount:** 7.5 N thrust plus 0.3 N·m torque, and a 30 N side load for hard-landing shock.
- **Tail mount:** 8 N tail down-load, ±3 N rudder side load, 15 N skid strike.

## 7. Checks (verifier)
- Every sketch DoF = 0, and every body `Shape.isValid()`.
- The assembly solves, and every joint is reported (no fallback if possible).
- Pairwise clashes between distinct parts < 1 mm³ in the assembled state. These are allowed:
  - bolts or inserts with the part they sit in, **only** if the hole/insert pocket was cut (it should be cut, giving 0);
  - prop blades with nothing.
- Revolute sweeps: ailerons ±20°, elevators ±20°, rudder ±25°, gates 0–90°, lids 0–100°, with no clash beyond the bevelled hinge corners (report any).
- Ten balls fit; the ball-in-chute sweep from rev G still passes.
- Span ≤ 1200. Printed parts each fit the 325 × 320 × 325 bed (report each bounding box in its print frame). Laser parts fit a 600 × 400 sheet.
- **BOM CSV** (`design/cad/revH_BOM.csv`) columns: part, qty, make, material, density, volume, mass. Total mass compared with the `sizing.py` estimate (715 g).

## 8. Deliverables (`design/cad/`)
- `TechfestPlane_revH.FCStd`, `TechfestPlane_revH.step`, `revH_BOM.csv`.
- PNGs:
  - iso, side, top, front;
  - `exploded_revH` (subassemblies pulled apart along their joint axes);
  - `wing_structure_revH` (covering hidden: ribs, spars, D-box);
  - `hopper_section_revH`;
  - `nose_section_revH`;
  - `tail_detail_revH`.

## 9. Phase 4b — weight/CG recovery + mechanism fixes (after phase 4 verification, 2026-11-04)

Phase 4 BOM: **903 g, empty CG X 267.3** vs NP X 273 → static margin 2.5% (near-neutral, unflyable for a beginner) and qualifier 16 balls = 80 (vs 101 target). Root cause: tail group ~76 g at X ~870 and overweight structure. Fix by lightening (no ballast). Target ≈ 770 g, CG ≈ X 231 (estimate in this section's table).

| # | Change | Δ g | X |
|---|---|---|---|
| 1 | Stab: 3 mm balsa solid → built-up: 3×6 balsa LE/TE spars + 3 mm balsa ribs at ~70 pitch with lightening, film covered (or 3 mm depron + 1×3 carbon strip at 30% chord) — ≤ 9 g | −15 | 840 |
| 2 | Elevators, rudder, fin: lightening cut-outs (truss/triangle, 6 mm webs) ≤ 40% of current mass removed | −12 | 900 |
| 3 | Spine 16/14 → **14/12** carbon (aliases for OD/ID; all clamp bores, saddles, TailMount sleeve, pod follow) | −10 | 475 |
| 4 | Spar_Front Ø10/8 → **Ø8/6** (clamp bores, rib holes follow). Root bending at 3 g/1.6 kg ≈ 5.9 N·m → σ ≈ 170 MPa, SF ≈ 5 on pultruded CF | −12 | 237 |
| 5 | Hopper: walls 0.8 mm skin + existing rib grid (ribs 1.2 × 6), floor 1.2 mm — target ≤ 38 g LW-PLA | −17 | 225 |
| 6 | M3 SHCS steel → 7075 aluminium (BOM material change; bolts in clamps stay steel only where SF needs it — keep steel for the 4 wing clamp bolts) | −15..−19 | ~250 |
| 7 | Glue allowance 5 % → 2.5 % of structure (CA/epoxy, realistic) | −13 | — |
| 8 | Lid drive: delete single double-arm servo + `ServoBracket_Lid` + pushrods. **Two 5 g micro servos**, one per lid, mounted mirror-image beside the spine directly on each lid torque rod line (servo horn → 15 mm pushrod → LidHorn, or coaxial direct drive); same channel (mirror mount gives opposite rotation). Lid range 0–90° (vertical is enough; 92° clears the spine) | −8 | 480 |
| 9 | RootRib (lite-ply): lightening holes leaving ≥ 5 mm webs around spar bores and clamp bolt holes | −12 | 300 |
| 10 | **Elevator + rudder pushrods inside the spine tube**: Ø2 carbon rods (or 0.8 mm steel in 2/1 PTFE tube) enter the spine through 3 × 12 slots just aft of the ele/rud servos (X ~170, on the ±Y sides, top half of tube), run inside the 12 mm bore, exit through slots at X ~880 to the horns. No rod may lie in the load port / chute / lid sweep. Re-run chute ball sweep (Y ±34, lids at 90°) — must pass | 0 | — |
| 11 | ElevatorJoiner X 895 → 892 (clears TailMount + Spine at +20°) | 0 | — |
| 12 | TailMount: interim lighten (shell 1.6 mm, sleeve wall 2 mm, pocket the saddle) — final shape comes from phase 5 TO | −10..−16 | 860 |

Checks after 4b: assembly solves 0; clashes as phase 4; gate sweep 0–90; lid sweep 0–90 **both lids** with their own servos; chute ball sweep passes; BOM rerun → empty mass ≤ 790 g and **CG X 225–240** (if > 240, move battery/ESC forward within the pod before anything else); span 1190; bed fit.

## 10. Engineering notebook rule (team request, 2026-11-04)
Every CAD phase keeps `design/logs/phaseX_log.md`, written as the work goes. Each entry records: the item, the design choice, the alternatives with numbers, the checks run with measured results, problems and fixes, and screenshot paths. The planner adds a summary of each phase plus the verification results to `design/logs/DESIGN_LOG.md`.

## 11. Phase 5 — topology optimisation + clamp fixes (planner, 2026-11-04)

**Updated loads.** Empty mass is now 814 g, so AUW with 16 balls is 1.534 kg. The rules cap thrust at the empty weight, so T ≤ 8.0 N.

| Part | Load cases (each run separately; size to the worst) |
|---|---|
| `WingClampCap_F` | (a) 4 g pull-up: total lift 60 N, front clamp carries 80 % = 48 N upward on the spar bore, reacted at the spine bore + bolts. (b) the same plus the wing pitching couple 1.8 N·m as ±18 N between the front and rear clamps (lever 101 mm). (c) a crash/landing 3 g down-load: −36 N |
| `MotorMount` | thrust 8 N along the shaft + 0.3 N·m torque; side load 30 N at the prop hub (49 mm ahead of the face); reacted at the 4 pod bolts |
| `TailMount` | 8 N stab down-load at the stab saddle; ±3 N fin side load at the fin root (lever ~80 mm); 15 N skid strike upward at the aft end; reacted at the spine sleeve |

**Material (PA-CF, conservative).**
- E 4 GPa, ν 0.35.
- Strength 35 MPa, which is the interlayer value. Allowable = strength / 2 = **17.5 MPa von Mises**.
- Minimum feature 1.6 mm (4 perimeters); minimum wall around an insert 2 mm; no unsupported overhang above 50° in the stated print orientation.

**Method (robust, so it stays parametric).**
1. Set up the design space: the part's current envelope, enlarged where it doesn't clash with neighbours. Non-design regions are the bores, bolt and insert bosses (Ø8) and the mating faces.
2. Mesh with gmsh tets and run a **BESO loop with CalculiX** in a headless/async process, not on the GUI thread. Target volume fraction ~30–35 %, using a sensitivity filter.
3. Save density-field images (iso + 3 views) to `design/cad/to/`.
4. **Reinterpret the result as a parametric PartDesign body**: ribs and trusses along the load paths, fillets R ≥ 1. Do not use the raw tet mesh as the part, because it is unprintable and unparametric.
5. **Check it with FEM** using the same load cases: σ_vM max ≤ 17.5 MPa and deflection reasonable. Report the stress plots.
6. Replace the part in the assembly so it still solves and nothing clashes.

**Fixes that go into the redesigned `WingClampCap_F`.**
- The 2 front clamp bolts (currently at X 241, under the front spar) must be **reachable with the wing installed**, so the wing can come off with ≤ 4 bolts. Move them clear of the spar footprint (e.g. fore/aft of the spar, X ≤ 228 or ≥ 246) with a straight 2.5 mm ball-driver line from above through film windows, or from below through the hopper/gate opening (≤ 25° off-axis).
- The wall around the M3 × 40 cross-bolt must be ≥ 1.6 mm everywhere (it is ~0.7 mm now).

**Phase 4c leftovers.**
- Run the full pairwise clash scan headless on the saved file.
- Check the 3.8 mm³ elevator/stab overlap against `stab_inc` = 0.
- Export the STEP with the assembly tree.
- Regenerate the exploded PNG without the duplicate wing.

**Deliverables.**
- Updated FCStd/STEP/BOM (target ≤ 800 g).
- `design/cad/to/` with density images and stress plots for each part.
- Before/after mass table.
- `design/logs/phase5_log.md` notebook.
