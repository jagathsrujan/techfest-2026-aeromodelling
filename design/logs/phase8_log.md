# Phase 8 notebook: rev J model clean-up

Plan: `design/09_revJ_cleanup_plan.md`. Model: `design/cad/TechfestPlane_revJ.FCStd` (edited in place). No part geometry is changed; the only things that change are how parts are grouped, which joints exist, labels, and leftover objects.

Reference for "nothing moved": `design/cad/to/work/snap_before.json` (121 leaves: 120 parts plus the wing Covering film). After every merge step the leaf snapshot is re-run on the saved file and compared with it.

## Step 0: backup and baseline (2026-11-13)
- Backup `design/cad/to/work/TechfestPlane_revJ_pre_cleanup.FCStd` already existed and is byte-identical (same md5 as the live file) to the file before any edit.
- The GUI had the file open under the internal name `TechfestPlane_revH`. Closed it without saving and reopened the file; the internal name is now `TechfestPlane_revJ` and `doc.FileName` ends in `revJ.FCStd`.
- Baseline check on the untouched file: `SNAP=after leaf_snapshot.py` gave 121 leaves, 1354 objects, solve 0, 0 differences, PASS.
- Findings that shaped the method: no link inside any sub-assembly has a placement expression (nothing bound to `Params`), so converting placements loses no parametric link. Bodies themselves are not inside any group (they are only reached through links). `Params` is not inside a group either.
- Convention used when moving a link from sub-assembly S (top link TS) to D (top link TD): new local placement = inverse(TD.Placement) * TS.Placement * old local placement.

Method for every merge step: record the global placement of every child link, move the links with the conversion above, check by script that every moved link's global placement is unchanged (it was, to 1e-9 mm, every time), delete the joints that became internal, delete the emptied top-level link and its App::Part (the Part's origin goes with it), run `Assembly.solve()`, save, then run `leaf_snapshot.py SNAP=after` on the saved file. Every step below ended with 121 leaves, 0 differences, PASS, solve 0, unless stated.

## Step 1: Fuselage (2026-11-13)
- Merged `A_EleServoAssy`, `A_RudServoAssy`, `A_ZBend_EleAssy`, `A_ZBend_RudAssy` into `A_HopperAssy` (22 links moved; all top-level placements were identity, so no conversion was needed). Deleted joints `Joint014`, `Joint015`, `Joint_ZBend_Ele`, `Joint_ZBend_Rud` (now internal).
- Alternative considered: keep servo mounts as separate sub-assemblies fixed to the spine. Rejected: the plan wants one rigid Fuselage item.
- Objects 1354 -> 1310. Snapshot 0 differences PASS, solve 0.

## Step 2: Nose (2026-11-13)
- Merged `A_MotorMountAssy`, `A_MotorAssy`, `A_PropAssy` into `A_NoseAssy` (27 links). `A_MotorAssy` and `A_PropAssy` were rotated 2 degrees and offset (3.8, -0.27, 0.21) mm by the solver, so their children got converted placements (the real test of the conversion). Global placements unchanged. Deleted joints `Joint005`, `Joint006`, `Joint007`.
- Solver: with the old workaround in place the solve returned 0. Then un-suppressed `Fix NoseAssy-Spine` (`Joint004`) and deleted `Ground_NoseAssy`: the plain Fixed joint solves (0) in the GUI and headless. So **no grounding fallback is needed** any more; the solver bug did not appear with the merged Nose.
- Objects 1310 -> 1276 (the 34 removed include the grounded joint and the 3 sub-assembly Parts with origins). PASS.

## Step 3: Wing (2026-11-13)
- Merged `A_CapAssy_F`, `A_CapAssy_R` into `A_WingAssy` (12 links; 54 global placements checked incl. the wing's own). Retargeted `Joint002` (spine clamp front to cap F) so its second reference is the Wing link (`A_WingAssy`, `L_WingClampCap_F.LCS_saddle_F.`), relabelled `Fix Wing-Spine`. Deleted `Joint001` (cap R to spine) and `Joint003` (wing to cap F).
- Alternative: keep `Joint001` as well, mating cap R to the spine. Rejected: it would over-constrain the now rigid wing.
- Objects 1276 -> 1254. PASS, solve 0.

## Step 4: Tail (2026-11-13)
- `A_Stab` and `A_Fin` pointed straight at bodies, so new child links `L_Stab` and `L_Fin` were created inside the Tail part, with placement = inverse(Tail) * old top-level placement (stab pitched 1 degree, fin rolled 90 degrees). The old top-level links were deleted. Deleted `Joint010`, `Joint011`. Retargeted the elevator joints and rudder joint first reference to `A_TailMountAssy` with sub names `L_Stab.LCS_hinge_R.` etc.
- Objects 1254 -> 1252. PASS.

## Step 5: Elevator (2026-11-13)
- Merged `A_ElevUnit_L` into `A_ElevUnit_R` (the left half, joiner and horn are one physical part). Deleted the redundant left hinge `Joint022`; `Joint021` (right hinge, limits -20..+20) now drives the whole elevator.
- Objects 1252 -> 1241. PASS.

## Step 6: Labels (2026-11-13)
- Labels set on the 9 top-level links and the 8 App::Parts: Spine, Fuselage, Nose, Wing, Aileron_R, Aileron_L, Tail, Elevator, Rudder. Relabelled `L_Hopper` -> `L_Fuselage`, `L_B_PodHopper_*` -> `L_B_PodFuselage_*`, `L_I_PodHopper_*` -> `L_I_PodFuselage_*`, joints to `Ground Spine`, `Fix Fuselage-Spine`, `Fix Wing-Spine`, `Fix Nose-Spine`, `Fix Tail-Spine`, `Rev Aileron_R`, `Rev Aileron_L`, `Rev Elevator`, `Rev Rudder`. Internal names unchanged.
- **Problem:** FreeCAD makes labels unique, so "Fuselage" became "Fuselage001" because a body is already labelled Fuselage (same for Spine, Aileron_R/L, Rudder). The bodies cannot be renamed because the leaf snapshot check compares labels. **Fix:** temporarily switched on the FreeCAD preference "allow duplicate labels" (User parameter Document/DuplicateLabels), set the nine labels, and restored the preference to its old value (False). The nine top-level links now carry exactly the plan names; five of those labels are shared with a body of the same name (the body is what the link shows). Search by internal name (`A_HopperAssy` etc.) if a script needs to tell them apart. `LCS_hopperwall` (label of an LCS inside the nose pod) still says hopper; left alone because it is not in the plan list and it is not a link or joint label.
- Grounded joint view object still hidden (`ViewObject.Visibility = False`); all joint markers hidden. PASS.

## Step 7: Removals (2026-11-13)
- `RibLinks`: its 22 links were referenced only by the group itself; the wing's own 22 `L_Rib*`/`L_RootRib*` links point straight at the `Rib`/`RootRib` bodies. Removed the group and the 22 links; wing rib links intact (22).
- LCS: 104 at start, 22 remain. Deleted 82 LCS that no joint uses, that nothing depends on (checked InList, expressions, scripts) and are not hinge or the three kept fuselage LCS. Kept 22: the 15 used by the 9 joints, `LCS_saddle_r`, `LCS_pod`, and the hinge LCS (`LCS_hinge006/007/008` in ribs/TE strip, `LCS_hinge_L` stab, `LCS_hinge014` elevator left). Note: LCS_ele, LCS_rud, LCS_clamp_r, LCS_stab, LCS_fin, and all bolt/tray/servo LCS are gone; if later work needs those positions they must be re-created. Many of the deleted LCS had Params expressions on their own placement; those expressions went with them, and nothing else referenced them.
- Params: 31 aliases matched the plan's cargo patterns (plan said 39; the other 8 do not exist under those names). Searched all 660 expressions and every sheet formula for the alias and for the bare cell address: no use anywhere. Rows cleared (alias and contents, columns A to G). Aliases 266 -> 235. `hop_*` aliases: `hop_w`, `hop_wall`, `hop_x0`, `hop_x1` are also unused, `hop_xc`, `hop_bot_half`, `hop_top_half`, `hop_h` are used. The unused `hop_*` ones were **kept** (plan rule: only the listed patterns). In total 96 aliases were found unused by alias or cell address; 31 were cleared, the other 65 (including the 4 `hop_*`) were kept as out of scope.
- `Fuselage_src`, `ZBend_Ele_Shape`, `ZBend_Rud_Shape` moved into a hidden group `Sources` (label `Sources (do not delete)`). `Covering` stays (it is a leaf).
- Checked: no empty App::Part, no unlinked body, no orphan Origin, no object in error state, no hidden link.
- Objects 1241 -> 1137 (incl. the 1 new group). Recompute clean. PASS.

## Step 8: Final checks on the saved file (2026-11-13)
- Check 1: snapshot 121 leaves (120 parts + Covering), 0 differences: PASS.
- Check 2: contact scan `connected: 120 of 120`, overlaps only Stab/Elevator_R 3.8 mm3 and Stab/Elevator_L 3.8 mm3 (the same overlap, listed per half): PASS.
- Check 3: headless `Assembly.solve()` on a fresh open = 0: PASS.
- Check 4: envelope from leaf bounding boxes X -72.2..946.0, Y -596.0..596.0, Z 69.0..315.0: PASS.
- Checks 5-8: 9 top-level links named as planned; 9 joints, none suppressed; roots are `Assembly` and `Sources`; `Params` is not a root object in FreeCAD's sense because it is referenced by sketches (it does not appear in `RootObjects`); no hidden links; no error states.
- Check 9 (hinges): **the Angle property of a Revolute joint does nothing in the solver of this FreeCAD (also on the pre-cleanup file)**, so it cannot be used to deflect. Instead each control surface's top-level link was rotated about its hinge axis by +10 and -10 degrees and the assembly solved (solve 0 each time): only the aileron + its horn, the elevator (both halves + joiner + horn), or rudder + horn moved; everything else stayed within 0.05 mm. Reset gave drift below 2e-12 mm. Angle properties are 0 in the saved file.
- Check 10: `export_release.py` ran: `EMPTY MASS 703.1 g`, `DONE`. (It rewrote the BOM, printed folder and report files with the same contents; the model file is not changed by it.)
- Renders re-saved at 2400 x 1400, white background: `release_revJ/renders/iso_revJ.png` (from above) and `iso_below_revJ.png` (from below). Both show all parts. Tree: `release_revJ/tree_revJ.txt`.

## Open points
- Duplicate labels (see step 6) are deliberate. If the team prefers unique labels, rename the five bodies and the snapshot label list together.
- Final object count 1137 (from 1354).
