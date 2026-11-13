# Rev J model clean-up plan (phase 8)

Goal: make `design/cad/TechfestPlane_revJ.FCStd` simple to open, read and change. More design changes are coming, so this phase does **not** produce print or laser files. No part geometry changes.

Frame: X aft from the nose datum, Y to starboard, Z up, mm. The assembly frame is the aircraft frame.

## 1. Starting point (measured 2026-11-13)

| Item | Now |
|---|---|
| Objects in the document | 1354 |
| Top-level items in `Assembly` | 21 links (18 sub-assemblies + Spine, Stab, Fin) |
| Joints | 22 (2 grounded, 1 suppressed, 2 flagged invalid) |
| Coordinate systems (LCS) | 104, of which 38 are used by joints |
| `Params` aliases | 266, of which 39 belong to the removed cargo system |
| Hidden root objects | `RibLinks` group with 22 links |
| Leaf parts in the assembly | 120 |

## 2. Target assembly tree

Nine top-level items instead of 21. Each rigid group is one sub-assembly; only real hinges stay as joints.

| Top-level item | Built from (existing) | Contains |
|---|---|---|
| `Spine` (grounded) | `A_Spine` | spine tube |
| `Fuselage` | `A_HopperAssy` + `A_EleServoAssy` + `A_RudServoAssy` + `A_ZBend_EleAssy` + `A_ZBend_RudAssy` | fuselage shell, belly skid, 8 saddle inserts, 2 servo mounts, 2 servos, 4 screws, 2 pushrods, 2 Z-bends |
| `Nose` | `A_NoseAssy` + `A_MotorMountAssy` + `A_MotorAssy` + `A_PropAssy` | pod, hatch, tray, battery, ESC, receiver, motor mount, motor, prop and blades, bolts, inserts |
| `Wing` | `A_WingAssy` + `A_CapAssy_F` + `A_CapAssy_R` | spars, ribs, sheeting, TE, covering, tip plates, aileron servos and trays, pushrods, both clamp caps and their bolts |
| `Aileron_R`, `Aileron_L` | `A_AilUnit_R`, `A_AilUnit_L` (unchanged) | aileron + horn |
| `Tail` | `A_TailMountAssy` + `A_Stab` + `A_Fin` | tail mount, pinch bolts, inserts, stab, fin |
| `Elevator` | `A_ElevUnit_R` + `A_ElevUnit_L` | both elevator halves, joiner, horn (they are one physical part) |
| `Rudder` | `A_RudUnit` (unchanged) | rudder + horn |

Target joints (9): ground on Spine; Fixed Fuselage–Spine, Wing–Spine, Nose–Spine, Tail–Spine; Revolute Aileron_R, Aileron_L, Elevator, Rudder (keep the existing angle limits).

## 3. Method rules

1. **Back up first**: copy the model to `design/cad/to/work/TechfestPlane_revJ_pre_cleanup.FCStd`.
2. **Take the reference snapshot before touching anything**: `freecadcmd design/cad/scripts/leaf_snapshot.py` with `SNAP=before`. It records every leaf part's name, volume and global centre of mass.
3. **Merge by moving links, not by rebuilding.** To merge sub-assembly B into A: for each child link in B's `App::Part`, compute its global placement (through B's top-level link), move it into A's `App::Part`, and set its local placement so the global placement is unchanged. Then delete B's joints, B's top-level link and B's empty `App::Part`.
4. **Reuse existing joints.** Do not create joints from scratch. Retarget the `Reference1`/`Reference2` of an existing joint when its part moved into another group (for example the elevator hinge must point at `Tail` → `L_Stab.LCS_hinge_R.` after Stab moves into `Tail`). Delete joints that become internal to a rigid group.
5. **Solver.** After each merge run `Assembly.solve()`; it must return 0 and no leaf may move. FreeCAD 1.1.1's solver has a known internal crash on some joint sets ("Solve failed: vector", see `08_revJ_plain_fuselage.md`). If it appears, the accepted fallback is to ground that rigid group directly instead of fixing it to the spine; record it. The current `Ground NoseAssy` + suppressed `Fix NoseAssy-Spine` pair is such a fallback: try the plain Fixed joint again at the end and keep whichever solves, never both.
6. **Labels**: give the eight groups the names in section 2 (set `Label` on the top-level link and on its `App::Part`). Relabel the body `Fuselage` items that still say Hopper (`A_HopperAssy`, `L_Hopper`, `L_B_PodHopper_*`, `L_I_PodHopper_*`, joint labels). Internal object names cannot change and need not.
7. **Delete only what nothing depends on.** Before deleting any object check its `InList` and search every `ExpressionEngine` and the `Params` sheet for references. If in doubt, keep it and list it in the notebook.
8. Work in small steps and save after each one that passes its checks. Hidden grounded-joint markers stay hidden (`ViewObject.Visibility = False`).

## 4. What to remove

| Item | Rule |
|---|---|
| `RibLinks` group and its 22 links | Remove if the `L_Rib*`/`L_RootRib*` links in the wing do not depend on them. If they do, retarget those links to the `Rib`/`RootRib` bodies with the same global placement first |
| Suppressed, invalid or now-internal joints | Remove (see rule 4) |
| LCS not used by any remaining joint | Remove if nothing else references it. Keep every LCS in section 2's joints, plus `LCS_saddle_f`, `LCS_saddle_r`, `LCS_pod` on the fuselage and all hinge LCS |
| Cargo `Params` aliases (`gate_*`, `lid_*`, `chute_*`, `port_*`, `ball_d`, `ridge_h`, `pin_len_*`, `srv_gate_z`, `lid_srv_z`, `fair_*`) | Clear the row only if no expression anywhere uses the alias. Never change or reuse an alias that is in use. `hop_*` aliases are probably still used: check, do not assume |
| `Fuselage_src`, `ZBend_Ele_Shape`, `ZBend_Rud_Shape` | **Keep** (they define those bodies). Move them into one hidden group labelled `Sources (do not delete)` |
| Empty `App::Part`s, unlinked bodies, objects in error state | Remove |

Not in scope: fasteners stay (they mark bolt positions for later changes); `Covering` stays; no geometry edits (the unused fairing bosses on the nose pod stay); no renaming of the many `L_*` child links; no re-export of print or laser files.

## 5. Deliverables

- `design/cad/TechfestPlane_revJ.FCStd`, cleaned, saved, all views showing every part.
- `design/logs/phase8_log.md`: engineering notebook, one entry per step: what was done, the alternatives considered, the checks run with their numbers, problems and fixes.
- `design/cad/release_revJ/tree_revJ.txt`: the final tree (top-level items, their children, joints).
- `design/cad/release_revJ/renders/iso_revJ.png` and `iso_below_revJ.png` re-saved (2400 × 1400, white background).
- Do not commit.

## 6. Key checks

| # | Check | Pass value |
|---|---|---|
| 1 | `SNAP=after` snapshot compared with `before` (`leaf_snapshot.py` prints the diff) | 120 leaves, same labels, volumes within 0.1 mm³, global centres within 0.01 mm |
| 2 | `REV=J freecadcmd design/cad/scripts/contact_scan.py` | `connected: 120 of 120`; overlaps only Elevator/Stab 3.8 mm³ |
| 3 | `Assembly.solve()` on a fresh headless open of the saved file | 0 |
| 4 | Envelope | X −72.2…946.0, Y −596…596, Z 69…315 |
| 5 | Top-level links in `Assembly` | 9, named as in section 2 |
| 6 | Joints | 9 as in section 2, or the documented grounding fallback; none suppressed, none invalid |
| 7 | Root objects | `Assembly`, `Params` (wherever it lives now), the `Sources` group; nothing else |
| 8 | Hidden links / objects in error state | none |
| 9 | Hinges | setting each revolute to ±10° moves only that control surface; reset to 0 before saving |
| 10 | `REV=J freecadcmd design/cad/scripts/export_release.py` still runs | prints `EMPTY MASS 703.1 g` and `DONE` (then discard its file changes are fine to keep) |
| 11 | Object count | reported before and after |
