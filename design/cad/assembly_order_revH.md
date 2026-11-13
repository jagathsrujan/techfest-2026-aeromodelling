# Rev H assembly order (phase 4c)

Model: `design/cad/TechfestPlane_revH.FCStd`. Tool for every M3 socket-head bolt: **2.5 mm hex ball-end driver**. M2 x 8 servo screws: 1.5 mm hex or small Phillips as supplied with the servo mount.
Order follows doc 07: spine, then pod and hopper, then wing clamps, wing, tail, with the fairing last.

**How access was checked.** In the assembled CAD model, from each bolt head a straight 60 mm line (the driver) along the bolt axis, plus six lines tilted 25 degrees around it (what a ball driver can do), were tested against every other part. "Axis free" means the straight line is clear; "cone x/6" is how many of the six tilted lines are clear. This is stricter than reality for steps done before neighbouring parts are installed, so the step column says when a bolt must be done early.

## Step 0: preparation (bench)
| What | Detail |
|---|---|
| Heat-set inserts (21 x M3 x 5.7, Ø4.0 x 6 holes) | hopper saddles 8 (`I_Saddle_1..8`), hopper/chute 2, pod/hopper 2, pod front (motor mount) 4, pod/fairing 2, TailMount pinch 2, front cap cross-bolt 1 (pressed from the spine-bore side of `WingClampCap_F`, before the cap goes on the spine) |
| Fits | carbon in printed bore OD + 0.15, carbon in laser bore OD + 0.10, hinge pins Ø + 0.2, M3 pass holes Ø3.4 |
| Spine | cut to 943 mm; flat 0.4 mm deep, 42 mm long at X 814 to 856 (top); cross-holes Ø3.4 at X 231.5, 338, 805, 865 |
| Wing parts | cut from `laser_dxf/sheet01..04`; ribs have jig feet, built flat on the jig base plates (sheet 04) |

## Step 1: spine and tail-end servos
1. Fit `ServoMount_Spine` x 2 (elevator and rudder servo mounts, X 138 to 165) and servos: **4 x M2 x 8**. Access: axis free, cone 6/6 (open from the top).
2. Thread the elevator and rudder pushrods (Ø2 carbon, inside the spine, exits at X ~883). No fasteners. The two rods lie at Y +-3; keep them clear of the front-clamp cross-bolt (0.5 mm measured).

## Step 2: hopper and chute
3. Lay the spine in the two hopper saddles (X 237, 338): nothing is fastened yet (the clamp caps do that, step 7).
4. Chute to hopper aft flange: **2 x M3 x 8** (`B_ChuteHopper_0/1`, into inserts). Access: axis free, cone 6/6.

## Step 3: nose pod
5. Pod to hopper front wall: **2 x M3 x 6** (`B_PodHopper_0/1`). Access: axis free, cone 4/6 (hopper blocks the rest).
6. Motor mount to pod front: **1 x M3 x 8 and 3 x M3 x 10** (`B_MMPod_1..4`, 4 inserts on a Ø44 circle; heads sit on the tilted 2 degree face, 0.1 mm off it, use a washer). **Do this before the motor and prop go on**: with the motor installed 3 to 4 of 6 cone lines are free, but `B_MMPod_1` is blocked on axis by the prop hub.
7. Motor to mount: **4 x M3 x 8** (`B_Motor_1..4`), heads face the pod interior. **Do this before the battery, battery tray and hatch go in**: access in the finished aircraft is 0/6 (battery and pod block it); through the open hatch/pod rear before the battery it is free.
8. Folding prop onto the motor shaft (no bolt). Folded blades rest at 20 to 32 degrees from the nose.

## Step 4: pod fit-out
9. Battery tray, battery (Velcro strap), ESC, receiver; battery hatch (magnets, no bolts).

## Step 5: wing clamps (front and rear)
10. Cap bolts: **front cap 4 x M3 x 20 steel** (`B_Saddle_5..8`, X 233 and 241, Y +-11) and **rear cap 4 x M3 x 20 aluminium** (`B_Saddle_1..4`, X 334 and 342) into the hopper saddle inserts.
    **Access findings (open items):**
    - `B_Saddle_5` and `_7` (X 233): axis free but cone only 2/6, tight.
    - **`B_Saddle_6` and `_8` (front cap, X 241) are blocked on axis by the front spar** (Z 172 to 180), directly above them. They can only be tightened if the cap is bolted down before the spar is threaded through it. Because the wing is one piece, that does not work with the model as built. *This predates phase 4c; I did not change it.* Options for the team: move the two bolts to X 230 and X 246 by widening the cap to 20 mm (the hopper saddle inserts must move too), or split the cap so the bolts sit on the open side.
    - Rear cap bolts: axis free, cone 2/6.
11. **Cross-bolt (new, anti-rotation): 1 x M3 x 40 (7075 aluminium)** from the top at X 231.5, Y 0, beside the front spar: through the cap, into the insert pressed from the bore side, tip 4 mm inside the spine bore (locks the tube). Access: axis free, cone **6/6**. It clears the spar by 0.81 mm, the spine by 0.2 mm and the two pushrods by 0.5 mm each. The wing film needs a small window over the cap top.

## Step 6: wing
12. Build on the jig: ribs (18 balsa, 4 lite-ply root ribs) stand on their feet in the slots of the two jig base plates; thread the carbon spars (front Ø8/6, rear Ø4); glue LE sheets (top and bottom, split at Y 0 with 30 mm doublers), TE strip halves, ailerons, tip plates (2 mm balsa, span 1190 + 2 x 2 = 1192).
13. Aileron servo trays (PETG) and servos: **4 x M2 x 8** (2 per servo), axis free, cone 6/6.
14. Wing onto the spine: spars in the cap bores (step 5). Cover with film, then cut the film window for the cap screws.

## Step 7: tail
15. Slide `TailMount` onto the spine end (X 780 to 946) with the 40 mm key over the spine flat. **Pinch bolts: 2 x M3 x 20** (`B_Pinch_1/2`, X 805 and 865, vertical). **Access is blocked by the fin and stab directly above the heads (0/6).** Tighten them before the stab and fin are fitted; they cannot be re-tightened without removing the fin. *Pre-existing: the TailMount was not changed in this respect.*
16. Stab on the saddle wedge (incidence +1 degree, leading edge up), then the fin (its bottom edge is trimmed to follow the inclined stab top); glue.
17. Elevators (hinge X 891), joiner, rudder; control horns (PETG); pushrod ends: Ø1 steel Z-bend wire through each horn hole (0.3 mm clearance), lashed and CA-bonded to the carbon rod over 12 mm.

## Step 8: payload hardware (frozen mechanisms)
18. Gate servo bracket, gates, hinge pins, lid servos and lids as in phase 4. Their M2 screws: gate servo screws are behind the nose fairing (axis blocked by the fairing; remove the fairing to reach them), lid servo bracket screws face forward into the chute and are blocked on axis (0/6, chute); do these before the chute is fitted.

## Step 9: fairing (last)
19. Nose fairing: **2 x M3 x 6** through the bridge strap at X 88, Y +-18 into the pod inserts. Access: axis free, cone **6/6**.
20. Tail cone: slide onto the spine from the tail end, bond to the chute rim and the spine collar (no bolts).
21. Final: check gate sweep 0 to 90 degrees and lid sweep 0 to 90 degrees by hand, check prop folds, check the CG at X 225 to 240 with the battery moved if needed.

## Fastener summary (this model)
| Fastener | Qty | Where |
|---|---|---|
| M3 x 40 (aluminium) | 1 | cross-bolt, front cap |
| M3 x 20 (4 steel front cap, 6 aluminium: 4 rear cap + 2 tail pinch) | 10 | clamps, tail |
| M3 x 10 | 3 | motor mount to pod |
| M3 x 8 | 7 | 1 motor mount, 4 motor, 2 chute |
| M3 x 6 | 4 | 2 pod/hopper, 2 fairing |
| M2 x 8 | 12 | servo mounts |
| M3 heat-set inserts | 21 | see step 0 |

*The fully assembled access scan is in `design/logs/phase4c_log.md`, entry 6.*
