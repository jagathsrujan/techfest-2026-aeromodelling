# Phase 4c engineering notebook: fairing, tip plates, thrust/incidence angles, DFM files

Written as the work goes, for the student team. Model: `design/cad/TechfestPlane_revH.FCStd`.
Spec: `design/07_aero_dfm_review.md` (sections 5, 6, 7) and `design/06_revH_build_plan.md`.

## Entry 0: State found at start (a previous run stopped partway)

I opened the saved file and looked at what is already there before changing anything.

| Item | What I found | Verdict |
|---|---|---|
| 1 Fairing | `Fairing` body exists (nose shell only, X 3 to 177, Y +-66, Z -2 to 152), volume 36.9 cm3, so about 20.3 g at 0.55 g/cm3. Two M3 bolts + inserts in the assembly (`FairingAssy`), Fixed joint to the NosePod. No tail cone. No check of prop or gate clearance logged. | Partly done. Too heavy (20 g vs 14 g target) and no tail cone |
| 2 Tip plates | `TipPlate` body (2 mm, outline from -15 to +35 about the chord line), two links inside `WingAssy` at Y +-595. Overall wing group Y -596 to +596 = 1192 mm. Parameters in `Params` rows 230-236. | Looks done. I will re-measure |
| 3 Stab +1 deg | Stab placement is zero rotation, Stab bounding box is flat (Z 150 to 153). Params has the alias, nothing is built. | Not done |
| 4 Motor 2 deg down / 2 deg right | MotorMount placement is a plain -90 deg pitch. No angles built. | Not done |
| 5 Anti-rotation | No cross-bolt, no key at the TailMount, no steel Z-bend pushrod ends. | Not done |
| 6 DFM files | `design/cad/laser_dxf/` does not exist, no `print_orientation_revH.csv`, no `assembly_order_revH.md`. | Not done |

Assembly check: `Assembly.solve()` returns 0 (solves). Note for the team: calling `solve()` from a script throws a harmless GUI error
(the joint view objects were created by script and have no view proxy). I patch the redraw call to a no-op first, then it returns 0.

Current numbers carried over: empty mass 789.75 g, CG X 232.9, Z 127.4 (from `revH_BOM.csv`, before this phase).


## Entry 1: Item 1, the fairing (nose shell + tail cone)

**What I built.** The old fairing (36.9 cm3, about 20 g) was one imported lump with no tail cone. I replaced it with two printed LW-PLA pieces, both generated from the same section function so they stay consistent:
- `Fairing` (nose shell, X 4 to 176): a rounded-square section that grows in a straight taper from about 54 x 60 mm at the pod nose to the full hopper width (Y +-59.6 = hopper 59 + skin) and Z 0 to 134. Corner radius goes from R7 at the nose to R12 at X 150. The aft end is cut flush to the slanted hopper front face (plane X = 176 - 0.5373 Z) with a 0.3 mm gap. Two hoop ribs (X 35 and X 130, 0.8 wide x 2.4 deep) plus a third hoop that is also the bolt bridge (below).
- `FairingTail` (new body, X 470.3 to 560): starts at the chute end section (Y +-59.6, Z 96 to 134) and tapers to a collar on the spine (inner bore 14.4, spine is 13.9 OD at Z 142). It is a separate print because 560 mm does not fit the 325 mm bed. New Params rows 237-243 (`fair_skin`, `fair_x_full`, `fair_rib_w`, `fair_rib_d`, `fair_tail_x0`, `fair_tail_x1`, `fair_gap`).

**Mass: the brief's 14 g cannot be reached the literal way.** I computed real volumes (LW-PLA 0.55 g/cm3):

| Option | Nose | Tail cone | Total (before ribs) |
|---|---|---|---|
| elliptic nose, 0.6 skin (as written in doc 07) | 19.1 g | 5.4 g | 24.5 g |
| straight taper, 0.6 skin | 14.4 g | 5.4 g | 19.8 g |
| straight taper, 0.45 skin | 10.8 g | 4.1 g | 14.9 g |
| **straight taper, 0.4 skin (chosen)** | 9.6 g | 3.6 g | 13.2 g |

The surface area of a shell that grows from a 54 mm nose to a 119 mm wide x 134 mm tall section in 150 mm is about 58,000 mm2; no choice of shape makes that 0.6 mm thick and 14 g. So **deviation: skin 0.4 mm (one 0.4 mm print line in vase mode) instead of 0.6, and a straight taper instead of an elliptic nose.** Final measured: nose 18.5 cm3 = **10.2 g**, tail cone 5.3 cm3 = **2.9 g**, total **13.1 g** including ribs and the bolt bridge (target 14 g, was 20 g). Risk: a 0.4 mm skin is only stiff because of the three hoops; test-print the nose before committing.

**Things I had to change because they clashed (all measured, not guessed):**
1. *Nose section.* The brief says a circle of diameter 50 at X 0. The pod nose is a 50.8 x 52 rounded square (corners R7), so a circle cuts its corners (measured contact 0.0 mm at X 10 to 14). I used a rounded square that starts 27 mm half-width and 7 mm corners. Deviation: not a true circle.
2. *Pod hump.* The pod top is a flat hump at Z 151, Y +-30 (X 40 to 106), 17 mm above the 134 roof. The roof has a slot that follows the pod outline (0.5 mm margin). The two M3 bolts (X 88, Y +-18) go through a small bridge hoop over the hump (8 mm wide, 0.8 thick, 0.02 mm clear of the pod boss) into the existing pod inserts.
3. *Fairing start at X 4.* The pod's own nose face already is the firewall ring; starting the shell at X 4 removes the overlap. The motor mount is 4.7 mm clear.
4. *Belly.* A belly that reaches Z 0 only at X 150 crossed the gate servo and gate pushrods (which sit at Z 3 to 10, X 132 to 136). The belly now reaches Z 0 at X 125 and the sides at X 150.
5. *Gate horn windows.* The gate horns live inside the nose (X 133 to 137) and swing through the side skin. I cut a round window per horn (R12.6 on the right, R10.6 on the left, X 131 to 138.1) about the hinge line Y +-61, Z 2.
6. *Tail cone vs lid drive.* The lid servo, bracket (X 482 to 516, Z 104 to 155), pushrods and horns sit inside the cone volume. The cone has notches around each (0.6 mm margin) and a clear cylinder R13.8 around each horn swing (X 472 to 484). The spine tunnel wall only starts at X 486 so it never meets a horn.
7. Object names are unique across the whole document: my first `LCS_chute` was auto-renamed `LCS_chute001` and the joint silently grabbed the Hopper's LCS and flung the cone to X 940. I renamed it `LCS_tailcone`, and the new chute-side LCS is `LCS_fairtail`.

**Checks (assembled model, measured):**
- Assembly solves (`solve()` = 0). New joint `Joint_FairTail` (Fixed, chute LCS_fairtail to LCS_tailcone). Nose keeps `Joint028` (Fixed to the pod).
- Clearance to the nose shell: pod 0.02, hopper 0.29, belly skid 0.34, inserts 0.32, spine 2.0, battery 4.7, ESC 3.8, hatch 2.5, motor mount 4.7 mm; gate pushrods 0.85 and 1.04. Tail cone: spine 0.2, chute 0.3, lid servo 1.1, bracket 0.6, torque rods 0.64.
- Gates swept 0 to 90 degrees about the hinge (rotated copies, outward sign), vs the Fairing only: minimum **0.78 mm** left, **0.83 mm** right. Lids swept 0 to 90: minimum **0.64 mm** to the tail cone; distance to the nose over 250 mm.
- Folded prop. The folding blades rest on the nose. I rotated both blades back about their hinge and found, for each stop angle, the smallest fold angle that clears the fairing (inflated by 1 mm), pod, spine: horizontal 20 degrees, 15 degrees 20, 45 degrees 32, 60 degrees 32, 75 degrees 29, vertical (one up one down) 29, 135 degrees 32. So the blades hang 20 to 32 degrees off the axis instead of lying flat; the lowest blade tip stays at **Z 15.9** (above the ground) and tips reach X 70 to 83, far from the gates (X 179+). The method samples the blade edges (about 290 points each) against the fairing envelope, so it is a sampled check, not a full solid-to-solid proof.

**Problem notes for the team.** (a) Boolean volume checks on lofted shells gave false overlaps; using ruled lofts and distance tests fixed that. (b) The saved GUI state had 243 links and 65 body tips hidden, so the model looked empty; I made them visible and hid the LCS triads. (c) Heavy sampling scripts exceed the 90 s FreeCAD call limit; I split them.

Screenshot: `design/cad/nose_fairing_revH.png` (low front-side view, fairing in grey, gate-horn windows at the bottom).


## Entry 2: Item 2, tip plates (re-measured)

Nothing needed changing. I measured the assembled shapes instead of trusting the earlier note:
- Wing panels alone (ribs, spars, LE/TE): Y -595 to +595 = **1190**.
- Tip plates (`TipPlate`, 2 mm balsa, 240 long, Z 137.3 to 194.4 in the assembly, i.e. -15 / +35 about the chord line): Y 594 to 596 each side.
- **Total span including plates = 1192.0 mm**, same value as the Assembly bounding box (Y -596 to +596), and equal to the limit `span_max` = 1192 in `Params` (rule: span <= 1.2 m; this leaves 8 mm margin).
- Overlap of the right plate with the spars, LE sheets, TE strip and covering: **0.0 mm3** for all of them (the plate has the spar bores cut). Plate volume 23.3 cm3 each in the printed/laser frame.

Alternative considered: 0.6 mm printed plate (doc 07 allows it). I kept the 2 mm balsa plate because it glues to the rib ends and is already modelled and checked.

## Entry 3: Item 3, stab incidence +1 degree

**Design choice.** The stab is fixed to the TailMount at `LCS_stab`, and the elevators hinge off the stab, so the incidence belongs in the TailMount. I rotate the stab about its **trailing edge** (the elevator hinge line, X 891, Z 150), not about its leading edge:

| Pivot | LE move | TE / hinge move | Consequence |
|---|---|---|---|
| leading edge (X 791) | 0 | TE drops 1.75 mm | hinge line, joiner and pushrod exits all move and the TE cuts into the saddle |
| **trailing edge (chosen)** | **LE up 1.75 mm** | **0 (hinge shifts 0.03 mm)** | pushrod exits, joiner and elevator hinge stay where they were |

What changed:
1. `TailMount`: new `Sk_stabwedge` (fully constrained, DoF 0) plus `StabWedge` Pad: a wedge on top of the saddle plate (X 791 to 885, Y +-10), 1.745 mm high at the LE falling to 0.1 mm at X 885, so the saddle face is physically inclined. Driven by `Params.stab_inc`.
2. `TailMount.LCS_stab` now has an `AttachmentOffset` expression: position (891 - 100 cos 1 deg, 0, 150 + 100 sin 1 deg) = (791.015, 0, 151.745) and rotation 1 deg about Y. (It is an attached LCS, so the `Placement` property is ignored; the offset is what counts.) The stab, elevators, horn and joiner follow through the existing Fixed and Revolute joints.
3. `Fin`: the fin sits on top of the stab and its flat bottom edge (Z 153) clashed with the raised stab (160 mm3). Added `Sk_stabincl_trim` (DoF 0) and `StabIncTrim`, a through-cut that shaves 200 mm3 off the fin's bottom edge along the incline, leaving the tab that goes through the stab notch. (First attempt cut nothing: the Fin body is drawn flat in its own XY frame, so my sketch was on the wrong plane. Fixed by attaching it to the Fin's XY plane.)

**Measured (assembled).** Stab chord line **1.000 degrees LE-up** (stab bottom-face normal tilt 1.000 degrees); stab LE bottom at Z 151.64, TE bottom Z 150.0; the assembly still solves (0). Overlaps: stab/TailMount 0.0 mm3, stab/fin **0.24 mm3** (a sliver at the TE, under the 0.5 limit), TailMount/fin 1.18 mm3 (this existed before: it is identical with incidence set to 0, so it is a known sliver, not caused by this change). Setting `stab_inc` = 0 gives a stab/wedge overlap of 1418 mm3 because the wedge is then in the way, so the incidence must stay driven from `Params`.


## Entry 4: Item 4, motor thrust angle (2 degrees down, 2 degrees right)

**Design choice.** The mount is a 4 mm thick disc (Ø50) bolted to the pod on a Ø44 circle. Two ways to get the angle:

| Option | Result |
|---|---|
| shim washers under the motor | loose parts, angle depends on assembly |
| **tilt the motor face of the printed mount (chosen)** | angle is fixed by the print, nothing to lose; thickness at the face centre stays 4.0 (pivot on the face centre), ranges 2.8 to 5.2 mm across the disc |

How it is built (all in `MotorMount`, driven by `Params.mm_down` and `Params.mm_right`, both = 2):
1. `Plate` thickened from `mm_t` (4) to 6 mm by a new expression (`Params.mm_t + Params.mm_wedge`, new row 244 `mm_wedge` = 2) to give wedge stock.
2. Datum plane `Plane_motorface` through the face centre, tilted by an expression (first about the local x = global Z axis by `-mm_right`, then about y by `-mm_down`).
3. `Sk_motorface_cut` (70 x 70, DoF 0) on that plane and pocket `MotorFaceCut` remove everything in front of the plane. The motor face is now inclined, the pod face stays flat (X = 0).
4. `LCS_motor001` is attached to the datum plane, so the motor, its 4 bolts and the prop follow through the existing Fixed joints (`Joint006`, `Joint007`). The assembly solves (0).
5. `Sk_motorholes_tilt` (DoF 0) and pocket `MotorHolesTilt`: motor bolt holes cut along the tilted axis (the plate's X-aligned holes alone gave a 9 mm3 bolt overlap).

**Measured.**
- Mount face normal = (-0.9988, +0.0349, -0.0349): **down 2.00 degrees, right 2.00 degrees** (right = +Y, the starboard wing side).
- Motor shaft direction and prop axis in the assembly: same vector, down 2.0, right 2.0 (right = 1.999).
- Motor/mount overlap 0.0; mount/pod 0.0; motor to fairing 12.4 mm; motor to pod 3.1 mm; mount to fairing 4.7 mm.

**Fasteners had to be re-seated (problems and fixes).**
- *Pod bolts (4 x M3, heads on the tilted face).* The face is at x = -4 + 0.035 (y - (z-110)), so the four seats are at x = -2.91, -4.00, -4.00, -5.09. I moved each bolt to its seat, and set bolt 1 to M3x8 so no shank goes past the 6 mm insert depth (shank into pod 5.0 / 5.9 / 5.9 / 4.8 mm). Heads sit 0.1 mm off the tilted face (about 0.19 mm of tilt across a head, so use a washer). Overlap with the mount: 0.03 mm3 each (was 0.52).
- *Motor bolts (4 x M3x8, heads on the pod side).* They tilt with the motor, so their heads sank 0.75 mm into the flat rear face (9 mm3). Moved 0.9 mm along their axis: overlap now 0.0 with mount, motor and pod. (They bite 3.2 mm into the motor instead of 4.)

**Prop clearance (re-run with the tilted prop).** The folded blades rest on the fairing at a fold angle of 20 (horizontal), 32 (45 deg), 32 (60 deg), 29 (vertical), 32 (135 deg) degrees: unchanged from before the tilt. Lowest blade tip Z 18.5 (was 15.9), blade tips reach X 71 to 85. Same sampled method as Entry 1.

**Effect on position.** The prop hub (X -53, Y 0, Z 110 before) moves to (-52.94, +1.71, 108.29): 1.7 mm lower and 1.7 mm to starboard, because the pivot is the mount face (X -4) and the hub is 49 mm ahead of it. The motor body is no longer co-axial with the fairing nose by 2 degrees; the nose is a smooth taper, and the motor stays 12 mm from it.


## Entry 5: Item 5, spine anti-rotation and pushrod ends

### 5a. Vertical M3 cross-bolt at the front wing clamp
**What is in the way (measured).** The front spar (Z 172 to 180) crosses the cap right above the spine, so a bolt at the clamp centre (X 237) would go through the spar tube. The hopper under the spine is only a 1.58 mm ceiling plate, and the bay under it is closed except the side gate openings.

**First attempt (built, then rejected).** Bolt from below at X 237, head under the hopper ceiling, into an insert in the cap. It was clash-free (0.2 mm to the spine, 0.5 mm to both pushrods) but **fails the rule that every fastener is reachable with a 2.5 mm ball driver**: from the nearest opening (the gate cut-out, Z 57, 59 mm to the side) the driver would have to come in about 40 degrees off the bolt axis (a ball driver manages roughly 25). I removed it (hopper hole deleted, hopper volume back to the original).

**Options compared.**

| Option | Verdict |
|---|---|
| bolt from below at X 237 | clash-free, driver cannot reach (40 degrees) |
| bolt from the top at X 237 | hits the spar |
| **bolt from the top at X 231.5, beside the spar (chosen)** | straight vertical access from above (wing film window only); needs a thin cap wall |

**Built.** New `Params.xbolt_dx` = -5.5 (row 249) drives all four items:
- `Spine` cross-hole (the existing Ø3.4 `CrossHoles` hole moved from X 237 to **X 231.5**; it goes through both walls, so the bottom wall also has a 3.4 hole, harmless);
- `WingClampCap_F`: `XBoltInsert_Cap` (Ø4 x 6.2 pocket from the spine-bore side at Z 148.9, for a heat-set insert pressed in before the cap goes on the spine) and `XBoltClear_Cap` (Ø3.4 clearance hole, 29 mm, from the cap top at Z 183.8 down to the insert), both sketches DoF 0;
- new body `M3_SHCS_40` (copy of the M3 bolt with a 40 mm shank): the bolt goes in from the top, head on the cap top (Z 183.8 to 186.8, still inside the wing section), threads through the insert and ends 4 mm inside the spine bore (tip Z 143.8), locking the tube against rotation;
- links `L_B_XBolt_F` and `L_I_XBolt_F` inside `CapAssy_F` (they follow the existing Fixed joints).
Assembly solves (0). Measured: bolt to spine **0.2 mm**, to the front spar **0.81 mm**, to both internal pushrods (Y +-3) **0.5 mm each**, to the hopper 5.9 mm; overlaps with cap, spine and insert **0.0 mm3**.
**Risks to know.** (1) The clearance hole leaves a cap wall of about 0.8 mm on the outer side and 0.7 mm between the hole and the spar bore (PA-CF, printed with the layers vertical): if the first print is weak there, widen the cap by 2 mm. (2) The head overhangs the cap edge by 0.25 mm. (3) The bolt is 7075 aluminium M3x40 (the BOM uses 1.0 g).

### 5b. Key / flat at the TailMount
The TailMount already has two vertical pinch bolts through the spine (X 805 and 865), which index the tail. I still added the requested flat and key as a second, redundant lock:
- `Spine`: `Sk_spine_flat` (DoF 0) and pocket `SpineFlat`: a 0.4 mm deep flat on the top of the tube, X 814 to 856 (the 42 mm is `key_len` + 2), width 4.4 mm. Removes 50 mm3 of carbon.
- `TailMount`: `Sk_key` (DoF 0) and pad `SpineKey`: a 40 x 4 mm printed rib in the bore ceiling (X 815 to 855), sitting 0.1 mm above the flat (clearance measured **0.1 mm**). It sits between the two pinch bolts, so it never meets their holes.
New `Params` rows 245 to 248: `flat_depth` 0.4, `key_len` 40, `key_x0` 815, `key_gap` 0.1.
Two things to know: (1) the underside of the sleeve is windowed, so the key had to go on top; (2) with a 0.35 mm flat on a 1 mm wall tube the wall is 0.65 mm there, only 42 mm long and clamped by the sleeve; if you would rather not grind the carbon, drop the flat and rely on the two pinch bolts.

### 5c. Pushrod exits: 1 mm steel Z-bend ends
**Before:** each Ø2 carbon rod ran out of the spine slot (lateral at X 883) and aft to X 905 at Y +-25, ending in a Ø1.6 vertical pin into the horn.
**Now:** the carbon rods end at X 889 (`Pushrod_*_OutB` shortened from 22 to 6 mm, old `PinB` features deleted). Two new bodies `ZBend_Ele` and `ZBend_Rud`: Ø1 steel wire laid alongside the rod end from X 877 (12 mm lashed and bonded with CA), then along +X, **R3 bend** up, a vertical leg through the horn hole, and a second **R3 bend** forming a hook over the horn (leg ends 4 mm long). Wire lengths: 44.9 mm (Ele) and 57.2 mm (Rud), 0.28 g and 0.35 g. (Option compared: a Ø1.6 pin glued into the carbon needs a hole in the carbon; the wire keeps the Ø2 rod solid.)
Fixed joints to the rod's `LCS_B` (`Joint_ZBend_Ele`, `Joint_ZBend_Rud`), solves 0. Measured: wire through the horn hole with **0.31 mm (Ele) and 0.35 mm (Rud)** radial clearance, to the elevators 1.5 mm, to the stab 3.5 mm, overlap with every part 0.0; contact with its carbon rod (0.0) is the lashed joint.
Not modelled: the lashing/CA and the 5 mm extra wire clearance for a clevis. The wires are generated shapes (Part pipe), not sketch-driven features: stated deviation from the "fully constrained sketch" rule.


## Entry 6: Item 6, manufacturing files

**Files written (all in `design/cad/`).**
- `print_orientation_revH.csv`: 25 rows (one per printed part: material, orientation, bed size, supports, notes). **All 25 fit the 325 x 320 x 325 bed**; the largest are the hopper 242 x 126 x 142, the nose fairing 176 x 119 x 152 and the TailMount standing on its end (33 x 20 x 166). The orientations are my proposals from the geometry (bores vertical where tolerance matters, insert bosses normal to the layers, thin shells nose-down); confirm them in the slicer.
- `laser_dxf/`: 4 sheets, 600 x 400, shelf-nested with 4 mm spacing and 2 mm margin, DXF (AC1009 polylines; layers `CUT`, `SHEET`, `LABELS`; units mm). The material, thickness and kerf are in each file name:

| File | Contents | Sheet used |
|---|---|---|
| `sheet01_balsa_2.0mm_kerf0.12.dxf` | 18 ribs with jig feet, 2 tip plates | 73 % |
| `sheet02_balsa_3.0mm_kerf0.12.dxf` | stab, 2 elevators, fin, rudder, 2 TE strip halves (595 x 10) | 48 % |
| `sheet03_balsa_1.5mm_kerf0.12.dxf` | LE sheet top halves (2 x 595 x 46.3) and bottom halves (2 x 595 x 37.5), 4 splice doublers 30 mm | 44 % |
| `sheet04_liteply_3.0mm_kerf0.15.dxf` | 4 root ribs with feet, 2 jig base plates (594 x 110) | 68 % |

- `laser_nest_preview.png` (1600 x 1000), `assembly_order_revH.md`.

**Design choices and numbers.**
- *Rib jig feet.* Two tabs, 8 mm wide, at chord positions X 45 and X 105 (local rib frame), reaching down to Y -13 (the jig plate top is at -10, so each tab passes 3 mm through the 3 mm plate). The lower surface is at Y 0.6 (X 45) and 10.7 (X 105), so the tabs are 15 and 25 mm long. I first tried X 140 (surface 13.8 mm up, too tall) and moved it. The jig plate slots are 8.2 mm long and rib thickness + 0.1 mm wide (2.1 for balsa, 3.1 for the ply root ribs); 11 stations per half-wing (Y 20, 42, 100 to 580 in 60 mm steps) in two rows of slots.
- *LE sheet.* It is a bent 1.5 mm skin, so the flat width is taken from the real skin cross-section: perimeter 95.7 / 78.0 mm minus 2 x 1.5 thickness, halved: 46.3 mm (top) and 37.5 mm (bottom). Halves are 595 long (split at Y 0) with a 30 mm doubler each, two of each cut (one spare).
- *Count correction.* The model has **18** balsa ribs (Y +-100 to +-580) plus 4 root ribs (+-20, +-42); the old BOM had 20 "Rib". I cut 18 and corrected the BOM.
- *Not nested:* the ailerons, TE_Fixed panels, spars (carbon, bought), `BellySkid` (1 mm polycarbonate): they are 3D shapes in the model or non-laser parts; list for a later pass.

**Problems.** The 595 mm strips did not fit a 5 mm margin on a 600 mm sheet, so the margin is 2 mm (595 + 4 = 599; check your cutter's usable area); the stab (500 long) needed a 90 degree turn in the nest. No DXF library was available, so the DXFs are written by a small script (polylines approximating arcs at 0.05 mm); open one in your CAM software before the first cut.

**Access check (assembled model, 60 mm ball-driver line + six lines at 25 degrees).** Results: free on axis and 6/6 cone: cross-bolt, fairing bolts, chute bolts, the 12 M2 servo-mount screws on top. Blocked in the finished aircraft but fine if done in order: motor bolts (battery and pod block them), the pod/motor-mount bolt `MMPod_1` (prop hub), gate servo screws (now behind the removable fairing), lid servo screws (chute). **Genuinely unreachable with the wing/tail on, both pre-existing and not changed this phase:** (1) the two front clamp bolts at X 241 (`B_Saddle_6`, `_8`) have the front spar directly above them; (2) the two tail pinch bolts (X 805, 865) are under the fin and stab. Both are listed in `assembly_order_revH.md` with options (widen the front cap to move the bolts beside the spar; fit the pinch bolts before the fin and stab).


## Entry 7: closing checks, BOM and exports

**Checks (section 7 of doc 07).**
| Check | Result |
|---|---|
| Span incl. tip plates <= 1192 | **1192.0 mm** (panels 1190 + 2 x 2 mm) |
| Fairing mass <= 14 g | **13.1 g** (nose 10.2 + tail cone 2.9; at 0.4 mm skin, not 0.6, see entry 1) |
| Fairing clash with gates 0 to 90 degrees / lids 0 to 90 degrees | min **0.78 mm** (gates), **0.64 mm** (lids to the tail cone); rotated-copy sweeps against the fairing only |
| Prop clearance (folded) | blades rest at 20 to 32 degrees fold angle; lowest tip Z 15.9 to 18.5 |
| Thrust angles | **2.00 down, 2.00 right** measured on the mount face normal and on the motor shaft |
| Stab incidence | **1.000 degree** LE-up measured on the chord and bottom face |
| Clashes < 0.5 mm3 | pairs touching a part changed this phase (212 pairs, bbox-filtered): all clear except the items below |
| Every printed part fits the bed | **25 of 25 fit** (`print_orientation_revH.csv`) |
| Assembly solves | **0** |

Remaining overlaps above 0.5 mm3 (from the clash scan): `TailMount` with `Fin` 1.18 mm3 (known sliver, identical with incidence 0), and each elevator with the stab 3.8 mm3 (its own hinge; **I did not compare with incidence 0** because that call hung FreeCAD, so I cannot say if the 1 degree changed it). Two overlaps that my wedge had created (pinch bolts with the TailMount, 35.7 and 10.8 mm3) were fixed by cutting the bolt holes and head clearance through the wedge (pockets `PinchHoleWedge`, `PinchHeadWedge`): now 0.0.
**Not done:** a full pairwise clash scan of the whole aircraft (492 candidate pairs) took too long (34 pairs in 7 minutes) and was stopped; the wing-to-wing parts (ribs, spars, sheets) were not rescanned. The earlier phases' results for those still stand.

**BOM (`revH_BOM.csv`, same columns).** Empty mass **814.4 g** (was 789.75), **CG X 232.9, Z 127.0** (X window 225 to 240 met). **The 800 g target is missed by 14.4 g.** Where the +24.7 g went: fairing 13.1, tip plates 7.5 (2 x 3.73), TailMount wedge and key 1.9, extra bolts/inserts/wires about 3, glue +0.5; ribs corrected 20 to 18 (-1.8). To reach 800 g, options with numbers: drop the tail cone (-2.9 g, loses the drag benefit behind the chute), tip plates 2 mm to 1.5 mm balsa (-1.9 g) or lightened (-1.5 g), cap lightening, or accept 815 g (empty weight sets the allowed static thrust, so every gram also lowers the thrust limit). The glue, film and wiring masses are not measured: wiring was placed at X 223, Z 134 so that the old model reproduces the old CG (X 232.9, Z 127.4); the new CG uses the same assumption.

**Exports (`design/cad/`).** `TechfestPlane_revH.FCStd` (saved), `TechfestPlane_revH.step` (155 parts as one compound in assembled position, no assembly tree or colours: the background assembly exporter did not finish), PNGs 1600 x 1000 on white: `iso_revH`, `side_revH`, `top_revH`, `front_revH`, `exploded_revH` (a second copy of the wing is still drawn in place), `nose_fairing_revH`, `tail_detail_revH`, `laser_nest_preview`. Visibility fixed in the saved file: 243 hidden links and 65 hidden body tips switched on, coordinate triads hidden.

**New `Params` rows (all >= 237):** 237 to 243 fairing, 244 `mm_wedge`, 245 to 248 flat/key, 249 `xbolt_dx`. Existing rows 230 to 236 untouched.
**Stated deviations:** (1) fairing skin 0.4 mm, linear nose, rounded-square nose section, shell starts at X 4; (2) fairing in two printed bodies (`Fairing`, `FairingTail`); (3) the fairing and the Z-bend wires are generated shapes, not sketch-driven features; (4) BOM 814.4 g > 800 g; (5) cross-bolt at X 231.5 from the top instead of at the clamp centre; (6) two clamp bolts and two tail pinch bolts are unreachable on the finished aircraft (pre-existing, flagged in `assembly_order_revH.md`).


## Entry 8: pause for FreeCAD add-on update (planner request)

**State at pause.** Nothing is mid-rebuild. The last save of `TechfestPlane_revH.FCStd` was made after the final changes (assembly solved 0, no objects in error state, span 1192.0). The fairing (`Fairing`, `FairingTail`) is in its final good version, so nothing needed rolling back. I made no FreeCAD calls after that save.

**Done:** items 1 to 6 as logged in entries 1 to 7; BOM, print CSV, 4 laser DXFs, assembly doc, STEP and PNGs written.

**Not finished / in progress:**
- Full pairwise clash scan of the whole aircraft (stopped: too slow on the GUI thread; the async attempt crawled). Once the add-on is updated, run it headless or async on the saved file.
- Elevator/stab overlap of 3.8 mm3 each: compare with `stab_inc` = 0 (that call hung FreeCAD) to confirm it is the own-hinge.
- STEP is a plain compound of 155 parts; the background export of the full assembly (with tree) never finished. Retry after the update.
- The exploded PNG still shows a second wing copy in place.

**Fairing build steps that failed along the way, and why (all resolved):** (1) smooth multi-section BSpline lofts gave false boolean overlaps and a failed cut, fixed with ruled lofts and distance tests; (2) a rib slab intersected with the curved outer solid failed (`Null shape`), fixed by building the rib slightly inside the skin; (3) the pod outer-shell solid came out inverted, so the pod cut was replaced by a roof slot following the pod outline; (4) the pod offset (`makeOffsetShape`) returned a null shape; (5) the tail-cone LCS name clashed with an existing object, so the joint dragged the cone to X 940 until I renamed it. A sampled prop-clearance script and the full clash scan exceeded the 90 s GUI limit and hung FreeCAD twice; it recovered both times.
