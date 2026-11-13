# Phase 5 notebook: topology optimisation + clamp fixes

Plain-language engineering notebook. One entry per step: what we chose, what we compared, what we measured, what went wrong, where the pictures are.

## Entry 1: set-up and how we will do the optimisation

**What the job is.** Three printed nodes carry the real loads: the front wing clamp cap (`WingClampCap_F`), the motor mount (`MotorMount`) and the tail mount (`TailMount`). We let a computer decide where material is needed (topology optimisation, "TO"), then redraw the result as an ordinary parametric FreeCAD body that we can print.

**Tools found.** FreeCAD 1.1 bundled CalculiX 2.23 (`ccx`) and gmsh 4.15 (command line). The bundled Python has numpy, scipy, matplotlib and PIL, but no gmsh module and no meshio. So: gmsh is called as a program, meshes are read by our own small reader, and our own BESO loop writes CalculiX input files.

**Method (same for all three parts).**
1. Design space = current envelope, enlarged where neighbours allow; bores, bolt bosses and mating faces are "non-design" (kept solid).
2. Tetrahedral mesh (gmsh), CalculiX linear static solve of all load cases in one run, BESO: remove the least-strained elements step by step (2 % volume per step) until 33 % of the volume is left.
3. Density pictures (iso, front, top, side) go to `design/cad/to/`.
4. Rebuild as PartDesign ribs/webs along the visible load paths, fillets R >= 1 mm.
5. Verify that rebuilt solid with quadratic tets (C3D10) and the same loads: von Mises <= 17.5 MPa (PA-CF 35 MPa interlayer / 2).
6. Swap into the assembly, solve, clash scan.

**Why our own BESO and not FreeCAD's FEM workbench.** The FEM workbench can set up one solve, not an iterating topology loop; a loop needs to rewrite the material every iteration. Writing the CalculiX deck directly lets the loop run in a separate process (crash-safe, never blocks the GUI).

**Load model simplifications (stated so nobody is surprised).** Forces are spread over the bore/hub surface nodes as equal nodal forces (plus a moment by a rigid-body-consistent distribution). Bolts are modelled as fixed seats (head bearing area). These give sensible peak stresses away from the supports; the very edge of a support is a numerical hot spot and is reported separately where it matters.

## Entry 2: WingClampCap_F (front wing clamp cap): optimise, rebuild, verify, swap in

**Starting point.** 11,356 mm3 = 13.6 g (PA-CF, 1.2 g/cm3). Two known faults: (1) the four bolts sat at X 233 and 241, right under the front spar (it covers X 233.8 to 241.8), so a driver could not reach them with the wing on; (2) the M3 cross-bolt hole was 0.5 to 0.8 mm from the cap's edge and from the spar bore.

**Design choices made before optimising (the fixes).**
| Item | Old | New | Why |
|---|---|---|---|
| Clamp bolts | X 237 +/- 4, Y +/- 11 | **X 227 and 247** (station +/- 10), Y +/- 11 | Both rows are clear of the spar footprint (233.8 to 241.8). A straight vertical line from above reaches every bolt head. Hopper saddle grown from 15 to 31 mm and its four inserts moved with it (new Params `sad_len_f`, `sad_dx_f`). |
| Cross-bolt | X 231.5 (5.5 ahead of centre), M3x40 head on the tower top | **X 228.8** (8.2 ahead), M3x20, head on a short boss | At X 231.5 the driver line grazed the spar ring. At 228.8 the line is 0.5 mm clear of the ring and passes beside the cap. A short M3x20 replaces the M3x40 (saves 1.0 g of steel too). `xbolt_dx` -5.5 -> -8.2; the hole in the Spine follows by its own expression. |
| Cross-bolt wall | about 0.7 mm | boss OD 9.0 around a 3.4 hole = **2.8 mm**; 4.0 insert pocket = **2.5 mm** wall | Needs >= 1.6 (>= 2.0 round an insert). |

**Design space and non-design regions (all in the aircraft frame).** Envelope X 222.5 to 251.5, Y +/- 16.5, Z 142 to 160 at the sides and up to 183.8 over the spar. (Y limit 16.5 leaves 2 mm to the root ribs at 18.5.) Kept solid: a 1.6 mm shell round the spar bore (|Y| <= 14) and round the spine bore (|X-237| <= 10), the pad under each bolt head, the cross-bolt boss. Voids: both bores, the bolt holes, the insert pocket, the driver channel. Mesh: 51,700 tets (1.5 mm, finer at holes).

**Loads (spec section 11).** (a) 4 g pull-up 48 N up on the upper half of the spar bore; (b) the same plus the 1.8 N.m pitching couple as +18 N on the front clamp = 66 N; (c) 3 g crash, 36 N down on the lower half of the bore. Supports: head seats of the 4 bolts (all directions); in (c) the spine-bore crown carries the vertical load instead (bolts only held sideways).

**Alternatives compared (BESO runs).**
| Run | Target (designable volume) | Result | Verdict |
|---|---|---|---|
| 1. plain sorted threshold | 33 % | did not settle: 30 % of elements flipped every iteration | method fault: the optimiser flip-flops without a limit on how many elements may be added per step. Fixed with an addition limit (1 % of the volume per step, the usual BESO "admission ratio") |
| 2. with limit, 33 % | 33 % | steady, but total 11,158 mm3, i.e. no saving | my "kept" regions were too generous (full-height columns round each bolt) |
| 3. with limit, tighter kept regions | **15 %** | steady, 7,750 mm3 total, compliance flat over the last 25 iterations | used. Pictures: `design/cad/to/clamp_F_density.png`, `clamp_F_slices.png` |

**What the optimiser showed.** (1) material gathers in a column between the spar ring and the spine ring, strongest at the two ends of the spar bore (Y = +/- 13 to 16); the middle of the column is nearly empty; (2) thin struts run from the spine ring out to the four bolt pads; (3) the whole flange between bolts is removed. All stresses in the solid design space were only about 1 MPa, so the stress limit is far from governing: shape is decided by minimum wall (1.6 mm) and by printability.

**Rebuild as a parametric body (what we read from the pictures).** Spar ring (OD 12, 28 long) + **two end plates** (1.8 thick at Y = +/- 13.1) running down from the ring to **two flange bars** (3.8 thick, 27 x 9.4, one per Y side, carrying the bolts) + **two ribs** from the spine ring up to the bars + spine half-ring (OD 17.8 over the 14.15 bore) + cross-bolt boss. All sketches have DoF 0 (checked with FullyConstrained), key sizes are tied to new Params rows 250 to 268.

**Measured.**
| Check | Result |
|---|---|
| Volume / mass | **6,260 mm3 = 7.5 g** (was 11,356 = 13.6 g): **-6.1 g, -45 %** |
| Valid single solid | yes, 1 solid |
| FEM, C3D10 mesh, max von Mises (limit 17.5) | (a) 4.67, **(b) 6.42**, (c) 3.37 MPa. Worst point is at a bolt-seat edge (X 244, Y -12.5, Z 156.6), which is a constraint edge, so real stress is lower. Safety factor on 35 MPa: **5.5** |
| Peak deflection | 0.025 mm (very stiff) |
| Assembly solve | 0 |
| Clash of the new cap with hopper, spar, spine, 8 bolts/inserts, pushrods | 0.000 mm3 each. Only the 0.05 mm clear film overlaps (4.9 mm3, the film must be cut where the end plates pass: a window, as the spec expects) |
| Driver reach, straight 3 mm line above each head | all 4 clamp bolts and the cross-bolt: **0 hits** on any part (film aside) |

**Problems and fixes.** (1) gmsh opened its GUI and hung until we gave it the batch flag; (2) BESO flip-flop (above); (3) recomputing the whole 1,983-object document takes minutes: the add-on timed out twice, we waited and re-checked.

**Pictures.** `design/cad/to/clamp_F_density.png`, `clamp_F_slices.png`, `clamp_F_stress_a_4g_lift_48N_v2.png`, `clamp_F_stress_b_lift_plus_couple_66N_v2.png`, `clamp_F_stress_c_3g_down_36N_v2.png`.

## Entry 3: MotorMount

**Starting point.** Round plate OD 50 x 4 with four OD 12 lightening holes, 5,748 mm3 = 6.9 g. Loads (spec section 11): thrust 8 N + 0.3 N.m torque; side load 30 N at the prop hub, 49 mm ahead of the face (that is a 1.47 N.m bending moment on the plate); supports are the four pod bolts.

**Design space.** The 50 mm disc, 4 mm thick (rear face on the pod, front face = motor face), plus a standoff ring (R 18.5 to 25, up to 8 mm in front of the face) outside the 35 mm motor can. Nothing may go behind the plate (pod wall) and nothing inside R 18.5 in front (motor). Kept solid: pads round the 4 pod-bolt heads (R 4.7) and the 4 motor-bolt holes (R 3.3). Mesh 53,000 tets. Cases: thrust, side load along Y, side load along Z.

**BESO.** 25 % of the designable volume (plate + ring). 89 iterations, steady; total solid 4,344 mm3 (of 13,673). Pictures: `design/cad/to/motor_mount_density.png`, `motor_mount_slices.png`.
Reading: (1) the thin standoff ring is almost all removed: only tiny bits at the four poles, so a deep standoff is not worth its mass; (2) the rear half of the plate stays nearly solid, the front half is sparse; (3) material runs from the motor-bolt pads out towards the four pod-bolt pads (the diagonals).

**Rebuild (parametric).** Hub disc R 14 x 3.2 (holds the motor pattern) + **four diagonal spokes** 10 wide x 4 high out to the four pod pads (OD 9.4) + four motor-bolt pads (OD 8). Pads are built 6.5 high and then trimmed by the existing 2 degree-down / 2 degree-right motor-face cut, so the motor face and bolt-head seats are exactly where they were (joints and LCS unchanged). All sketches DoF 0; new Params rows 269 to 274.

**Alternatives compared (FEM, quadratic tets, same loads).**
| Hub thickness | Mass | Peak vM raw (side load Y / Z) | Away from supports |
|---|---|---|---|
| 2.4 mm | 3,325 mm3 = 4.0 g | 17.7 / 18.5 MPa | not computed |
| **3.2 mm (chosen)** | **3,670 mm3 = 4.4 g** | 18.2 / 19.1 MPa | **12.4 / 11.3 MPa** |
| old plate | 5,748 mm3 = 6.9 g | not run | |

**Honest note on the stress numbers.** The raw peak sits on the edge of the fixed bolt-head seat (an ideal rigid support: the stress there grows as the mesh is refined). So the check reports two numbers: raw max, and max outside a 1.5 mm zone around every support/load node. Thrust case: 2.3 raw / 1.3 away. Side-load cases: raw 18.2 and 19.1 MPa (**1.1 x the 17.5 limit, so the raw check fails by a hair**), but 12.4 and 11.3 MPa away from the supports, and the 99.5th percentile is about 8 MPa. Making the hub thicker did not lower the raw peak because it is a support artefact, not a thin-section problem. We call it verified on the "away from supports" value (limit 17.5, safety factor on 35 MPa about 2.8) and flag it for the team.
Deflection at the loaded holes: <= 0.045 mm.

**Assembly.** Solve 0. Zero clash with the nose pod and the four inserts; the pod bolts touch it by 0.03 mm3 (tolerance noise in the tilted bolt holes). Note: the first clash test I ran compared parts without their parent placement and showed a false 29.6 mm3 overlap with the motor; the headless scan (which applies parent placements) is the one to trust and is run at the end.

**Pictures.** `design/cad/to/motor_mount_stress_*_v2.png`.
