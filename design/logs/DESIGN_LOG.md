# Design log: rev H (fully constrained, fit-for-build model)

This is the running record of what was done, why, what was tried and what went wrong. Each phase links to its detailed log. From phase 4c on, the CAD agents write `logs/phaseX_log.md` live, step by step. Phases 1–4b below were backfilled from the agents' reports and my verification notes.

How the work is split:
- **Planner (Opus):** reads the requirements, does the calculations, and writes the plan docs (`06_revH_build_plan.md`, `07_aero_dfm_review.md`).
- **CAD agent (Sonnet):** builds in FreeCAD from that plan.
- **Planner:** checks the images, masses and clearances before anything is reported as done.

---

## Phase 1: core structure (2026-11-03)
**Goal:** replace the loose rev G solids with parametric, fully constrained bodies driven by one `Params` spreadsheet, so a single number change (e.g. tube diameter) updates every part that depends on it.

- **Built:** 13 bodies from 94 sketches, all at 0 degrees of freedom: spine, hopper, chute, nose pod, wing clamps and motor mount.
- **Why bodies plus a spreadsheet:** the team can change a fit or a stock size without remodelling, and every part already sits in its flight position, so the assembly is just mating.
- **Result:** no clashes and the balls fit. But the structure came out at 195 g against the ~150 g estimate. That was the **first warning that the paper weight estimate was optimistic.**

## Phase 2: wing (2026-11-03)
**Goal:** a buildable wing: laser-cut balsa ribs, carbon spars, balsa LE sheeting (D-box), TE strip, ailerons, film covering.

- **Result:** the wing is about 203 g.
- **Limitation:** the S1223 rib outline is a fixed spline, so the chord is not parametric. Changing the chord means regenerating the rib.
- **Problem hit:** the agent overwrote existing spreadsheet aliases and broke ~340 expressions.
  - Fix: the aliases were rebuilt. Volumes were re-checked against phase 1 (within 0.3%).
  - New rule: **only add aliases in empty rows.**

## Phase 3: tail, systems, fasteners (2026-11-04)
**Goal:** tail surfaces, TailMount, servos, pushrods, battery tray, and every M3 bolt with its heat-set insert.

- **Result:** 18 bolt/insert pairs, all coaxial (checked).
- **Problem found:** the gate pushrod ran fore-aft, but the gates hinge about the X axis, so a fore-aft rod cannot turn them. It also passed through the hopper wall.
  - Decision: a **torque-rod drive**. The hinge pins run forward as torque rods, each with a horn; one servo with its shaft pointing forward pushes both horns sideways through short rods. This is the standard way to drive a hinge from a servo that sits off-axis.

## Phase 4: assembly + BOM (2026-11-04)
**Goal:** a real FreeCAD assembly (spine grounded, everything mated through named attachment points), hinge joints with limits, a full clash check, and a BOM with real masses.

- **Result:**
  - 29 joints, solved; parts land within 1e-13 mm of their design positions.
  - Gates drive 0–90° from one servo.
  - All printed parts fit the H2D bed.
- **Problems found by measuring the real model:**
  1. **Mass 903 g** (estimate 715).
  2. **CG X 267**, only 6 mm ahead of the neutral point (X 273), so **~2.5% static margin**. That is nearly unflyable for a beginner.
     - Cause: the tail group (~76 g at X ~870) acts on a long lever arm.
     - Key insight: removing 1 g at the tail moves the CG as much as adding ~2.5 g of nose ballast. So the fix was **lightening the tail, not adding ballast**.
  3. A single servo couldn't drive both lids (one lid only reached 63°).
  4. The elevator and rudder pushrods crossed the load port.

## Phase 4b: weight / CG recovery (2026-11-04)
**Decision basis:** a quick moment calculation predicted ~770 g and CG X ~231 after the changes below, with no ballast.

| Change | Mass before → after (g) |
|---|---|
| Stab: framed 3 mm balsa | 23.8 → 5.9 |
| Elevators, rudder, fin: −39% via lightening windows | — |
| Spine 16/14 → 14/12 | 71.0 → 61.3 |
| Front spar 10/8 → 8/6 (root stress ~170 MPa at 3 g, SF ~5) | 52.9 → 41.2 |
| Hopper: 0.6 mm walls | 54.7 → 42.3 (target was 38) |
| TailMount: lightened | 26.2 → 13.4 |
| Glue allowance: realistic | 25.0 → 10.3 |
| Root ribs: lightening holes (kept ≥ 5 mm webs) | −6 total |

- **Bolts:** aluminium, except the 4 steel bolts at the front wing clamp.
- **Pushrods:** moved inside the spine tube.
- **Fits now parametric:** `clr_print` 0.15 and `clr_laser` 0.10.
- **Result: 790 g, CG X 233 (~17% static margin).**
- **Scope change from the team:** the load/unload mechanisms are frozen. Focus moves to aerodynamics, DFM and fit.
- **Open item found in verification:** a 2 mm carbon rod cannot make the sharp 90° exit bends drawn in the model. The ends become steel-wire Z-bends (in phase 4c).

## Aero + DFM review (planner, 2026-11-04)
Full reasoning: `07_aero_dfm_review.md`; scripts: `calc/drag_buildup.py`, `calc/planform_study.py`.

- **Rule coupling:** the rules cap thrust at the empty weight, so loaded T/W is ~0.5. Drag therefore decides climb and launch.
- **Drag build-up:** the box hopper is ~21% of cruise drag and the bare spine ~11%. A faired fuselage gives −19% drag, the biggest win.
- **Planform:** taper gave +7% CLmax, but on uncertain data and with harder build. **Team chose: keep rectangular.**
  - Tip plates: +5% L/D for 6 g.
  - Washout: useless here, since the wing stalls at the root first.
- **Trim:** stab +1° and motor 2° down / 2° right, both from the moment balance.

## Phase 4c: fairing, tip plates, angles, DFM files (2026-11-04, done)
Full notebook: `logs/phase4c_log.md`. This phase ran as a visible session.

- **Fairing:**
  - Nose shell + tail cone weigh 13.1 g. That needed a 0.4 mm skin and a straight taper, because 0.6 mm and an elliptic nose would be ~25 g.
  - Gates still have 0.78 mm clearance and lids 0.64 mm.
  - The folded prop blades rest on the nose at 20–32° fold.
  - Test-print the nose first, because a 0.4 mm skin relies on its hoops.
- **Span:** 1192.0 mm with the tip plates.
- **Stab +1°:** rotated about the TE so the hinge and pushrods don't move. Measured 1.000°.
- **Motor 2° down / 2° right:** the angles are built into the printed mount face. Measured 2.00 / 2.00.
- **Spine anti-rotation:** an M3 × 40 cross-bolt from the top at X 231.5, beside the spar, plus a flat and key at the TailMount. The cap wall around the bolt is only ~0.7 mm; phase 5 must fix it.
- **Pushrod ends:** Ø1 steel Z-bends, R3.
- **DFM files:** print-orientation CSV (25 parts, all fit the bed), 4 nested laser DXF sheets with a rib jig, and the assembly order.
- **BOM: 814 g, CG X 232.9.** That is 14 g over the 800 g target; the fairing and tip plates were the trade.
- **Found:** the two front clamp bolts sit under the front spar, so they can't be reached with the wing on, and the wing can't be removed. Phase 5 has to fix this when it redesigns the front clamp cap.
- **Tooling fix (planner):**
  - The FreeCAD add-on (Aug 2026) was older than the auto-updating Claude-side connector (0.1.28). That is why timeout/async calls failed and FreeCAD hung or restarted.
  - Updated the add-on to 0.1.28 (backup kept) and pinned the connector version with the `freecadcmd` path.
  - Async jobs and `timeout` were tested and work. Headless runs need the Claude app restarted.
- **Open:**
  - full-aircraft clash scan (run headless);
  - elevator/stab 3.8 mm³ overlap check;
  - STEP export with the assembly tree;
  - exploded PNG shows a duplicate wing.

## Phase 5: topology optimisation + clamp fixes (2026-11-05, stopped early)
Full notebook: `logs/phase5_log.md`.

- **Front wing clamp cap:** bolts moved to X 227 and 247 so a driver reaches all four with the wing on; cross-bolt wall grown from 0.7 to 2.8 mm. Optimised and redrawn: 13.6 → 7.6 g, peak stress 6.4 MPa (limit 17.5).
- **Motor mount:** plate replaced by a hub with four spokes: 6.9 → 4.4 g. Stress is 12.4 MPa away from the bolt seats; the raw peak at a seat edge is 19.1 MPa, which is a support artefact but is flagged.
- **Tail mount and rear clamp: not optimised.** The team stopped the optimisation because it was taking too long. Both keep their phase 4b hand-lightened shapes (15.2 g and 13.0 g).

## Phase 6: model clean-up and manufacturing release (2026-11-13)
**Trigger:** the team opened the model and saw loose parts that made no physical sense.

**What was actually wrong (found with a contact scan of every part, `cad/scripts/contact_scan.py`):**

| Problem | Cause | Fix |
|---|---|---|
| Gates, belly skid and wing clamps appeared to hang in mid-air | The hopper body had no visible feature, so the main fuselage shell was not drawn although it was in the assembly | Tip feature made visible (same for the spine, which was showing a pre-flat feature) |
| Doubled bolts, inserts, servos and prop blades, some in old positions | 80 links left at the document root outside the assembly; 15 of them still sat at pre-phase-5 positions | Deleted (nothing referenced them) |
| Hopper cut into the spine by 282 mm³ | Phase 5 lengthened the front saddle to 31 mm but the spine half-bore pocket stayed 17 mm long | `HalfBore_0` length now follows `sad_len_f` |

- **Result:** 155 parts, all touching the structure; the only overlap left is 3.8 mm³ per elevator at the stab hinge line.
- **Release:** `cad/release_revH/` holds per-part STL/STEP for printing, STEP for laser parts, the carbon cut list, an assembly STEP, renders and a refreshed BOM.
- **BOM: 807.3 g, CG X 233.6.**
- **Not done:** 4 fixed joints (fairing, tail cone, two Z-bends) are flagged invalid by FreeCAD although the solver returns 0 and the parts sit in place; the laser DXF sheets were not regenerated (no laser part changed).
- A backup of the model before this phase is `cad/to/work/TechfestPlane_revH_pre_release.FCStd` (not in git).

## Phase 7: rev J, plain fuselage without the cargo system (2026-11-13)
Full description: `08_revJ_plain_fuselage.md`. Script: `cad/scripts/build_revJ.py`.

- **Request from the team:** remove the competition-specific ball loading and unloading, and make a normal fuselage for plain flying.
- **Decision:** a new revision file (rev J); rev H stays as the cargo version.
- **Fuselage shape:** a 60 mm wide box shell with the same front wall plane and the same two spine saddles as the hopper. Alternative considered: a fresh shape with new mounts. Rejected, because keeping the hopper's interfaces means the nose pod, wing clamps, spine and servo mounts are reused without change.
- **Removed:** hopper, gates, chute, lids, both fairings, 2 servos and their linkages: 35 items.
- **Result: 703.1 g (−104 g), CG X 224.7, static margin 20 %.** 120 parts, all attached, no new clashes.
- **Problems:** (1) the tail cone's source shape was left visible after its body was deleted; removed. (2) An unused M3×40 body and BOM row were left from phase 5; the BOM row is now the M3×20 cross-bolt. (3) The assembly solver returns −1 on rev J; positions are correct, cause not found.
