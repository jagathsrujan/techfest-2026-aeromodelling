# Phase 9 notebook: rev J tree clean-up (fasteners, nose fairing features)

Model: `design/cad/TechfestPlane_revJ.FCStd`, edited in place. Start state is commit 1ea244c (1138 objects).
Scratch copies (not in the project): `revJ_start.FCStd`, `revJ_stageA.FCStd`, `revJ_stageB.FCStd` in the session scratchpad `phase9/` folder.
Check scripts: `leaf_snapshot.py` (SNAP=phase9), `contact_scan.py` (REV=J), and a scratch script `p9check.py` (top links, joints, error states, NosePod data) on a fresh headless open.

## Orientation (2026-11-15)
- 46 fastener links found by linked body label (M3_/M2_): 17 M3_Insert, 11 M3_SHCS_20, 8 M2_Screw_8, 5 M3_SHCS_8, 3 M3_SHCS_10, 2 M3_SHCS_6.
- By group: Fuselage 12, Wing 14, Nose 16, Tail 4. Each link sits directly in its sub-assembly App::Part.
- Dependencies: no joint, no expression and no object outside the links and the `PartDefinitions` folder refers to a fastener link or body.
- Contact scan before the change: no structural part had only fasteners as neighbours. So no part could become FLOATING.
- `export_release.py` keeps BOM rows whose body is missing. The fastener BOM rows stay unchanged. Not run (inference from the code).

## Task 1: fastener positions recorded, fasteners removed
- Decision (planner): remove all fastener links and bodies from the model; keep them in `revJ_BOM.csv` as bought items.
- Reason: more design changes are coming, the fastener links would go out of date, and they were about one third of the assembly tree.
- Alternatives not chosen: keep them in the model (they go stale and fill the tree); hide them (still in the tree, still stale).
- Positions written first to `design/cad/release_revJ/hardware_positions_revJ.csv` (46 rows). Global placement = Assembly x top link x child link. Cross-check with `getSubObject` gave 0 mm difference.
- Local frame of each fastener body (for reading the CSV): the link origin is at the head seat (bolts) or the bottom face (inserts); local +Z points to the head.
  - M3_Insert: Z 0..5.7, OD 4.0
  - M3_SHCS_6/8/10/20: shank Z -L..0, head Z 0..3.0, head OD 5.5
  - M2_Screw_8: Z -8.0..1.6
- Data notes for the planner (not changed): motor-mount bolts `L_B_MMPod_1` is M3_SHCS_8 at x -3.014; `_2`, `_3` are M3_SHCS_10 at x -4.100; `_4` is M3_SHCS_10 at x -5.186. The motor bolts are tilted about 2 degrees (direction 0.999, -0.035, 0.035).
- Done: deleted the 46 links by object, then each body with `removeObjectsFromDocument()` and `removeObject()` (body, 4 features and sketches, Origin with 7 children).
- Objects 1138 -> 1014. This matches the count of 124 calculated before the delete.
- No visibility changed (diff of all objects before and after). `PartDefinitions` 53 -> 47 items.
- Checks on the saved file:
  - Snapshot: 75 leaves, 46 MISSING (all M3_/M2_), 0 MOVED/CHANGED, 0 EXTRA, solve 0.
  - Contact scan: connected 74 of 74, no FLOATING, overlaps only Stab/Elevator_R and Stab/Elevator_L 3.8 mm3.
  - 9 top links, 9 joints, none suppressed, all "Up-to-date", no error objects.
- Picture: `phase9/A_below.png` in the scratchpad. Complete aircraft, same as the committed reference. PASS.

## Task 2: NosePod fairing features (tested, NOT landed)
- Feature order: `... RearTrim2, Sk_motor_screw_access, MotorScrewAccess, Sk_FairBoss_P, FairBoss_P, Sk_FairBoss_N, FairBoss_N, Sk_FairInsert_P, FairInsert_P, Sk_FairInsert_N, FairInsert_N`. New Tip = MotorScrewAccess.
- Done on a trial: Tip set, 4 features and 4 sketches deleted from the end backwards, MotorScrewAccess made the only visible feature, recompute. Saved, all checks run.
- Results:
  - One valid solid. Volume 39695.412 -> 38901.210 mm3 (-794.2 mm3, -2.0 %).
  - Bounding box X 0..138.388, Y -30..30 unchanged, but Z max 151.0 -> 150.6.
  - Centre of mass (55.015, 3.215, 110.224) -> (54.342, 3.281, 109.508): shift 0.985 mm.
  - Contacts unchanged (74 of 74), solve 0, no error objects, 1006 objects. Picture correct (`phase9/B_below.png`).
- Two of the planner's pass values fail: the bounding box must be unchanged, and the centre-of-mass shift must be less than 0.5 mm.
- Cause (measured with a boolean difference, `fairdiff.py`): the fairing features are not only internal.
  - FairBoss_P/N: Ø8 pads from Z 141 to 151 at (88, ±18). Inside the pod they add 389.6 mm3 each (Z 141..150). Above the pod top (Z 150.6) they make two Ø8 x 0.4 mm bumps (15.1 mm3 each).
  - FairInsert_P/N: Ø4 x 6 mm pockets from Z 151 down. They cut two Ø4 holes through the top wall at Z 150.0..150.6 (7.5 mm3 each).
  - Removal therefore takes away 809.3 mm3 and fills 15.1 mm3. Net -794.2 mm3 near (88, 0, 145). This exactly explains the centre-of-mass shift.
- Decision: the brief says to stop the task and leave the last passing saved state when a pass value fails. The live file was restored to the Task 1 state (`revJ_stageA.FCStd`, md5 844b9bae...). The trial is kept as `phase9/revJ_stageB.FCStd` (md5 860927ad...).
- Options for the planner:
  1. Land the trial file (copy it over the live file). It removes the bumps, closes the holes, and the pod loses 794 mm3 (about 1 g in PLA).
  2. Keep the features as now.
- Params aliases not touched.

## Task 3: part history kept
- Decision (planner): no action. Every body stays parametric.
- Reason: the parts must stay editable through their sketches and the Params sheet for the coming changes.
- Alternative not chosen: convert bodies to simple solids (shorter tree, but no editing).

## Final checks on the saved file (Task 1 state, 1014 objects)
- Snapshot: 75 leaves, 46 MISSING (all M3_/M2_), 0 MOVED/CHANGED, 0 EXTRA, solve 0.
- Contact scan: connected 74 of 74, no FLOATING, overlaps only Stab/Elevator 3.8 mm3 (each half).
- Fresh headless open: solve 0, 9 top links, 9 joints, none suppressed, none Invalid or Error, no error objects after recompute, no broken links.
- Roots: Assembly, PartDefinitions. Grounded joint view hidden. Spine, ZBend_Ele and ZBend_Rud visible. PartDefinitions hidden, 47 items.
- Renders re-saved from this file: `release_revJ/renders/iso_revJ.png` and `iso_below_revJ.png`, 2400 x 1400, white.

## Problems and fixes
- `fitAll` plus `saveImage` gives a wide white margin. A change of the camera height after `fitAll` clipped the model or gave an empty image. Fix: save at 4800 x 2800, then trim the margin and scale to 2400 x 1400 with PIL (`crop.py`).
- When two images are saved in one script, the second `setCameraOrientation` was not finished before `saveImage` (camera animation). The first `iso_below` render came out from above. Fix: update the GUI and wait about 1 s after each orientation change.
- The check scripts rewrite `release_revJ/contact_scan.txt` and `to/work/snap_phase9.json`. Both are from the final file.
