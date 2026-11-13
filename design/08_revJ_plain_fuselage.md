# Rev J: plain fuselage, no cargo system

Rev J is rev H with the golf-ball load/unload system removed, so the aircraft is a plain flyer. Rev H (`cad/TechfestPlane_revH.FCStd`, `cad/release_revH/`) is kept unchanged as the cargo version.

Built by `cad/scripts/build_revJ.py` from the rev H model. Model: `cad/TechfestPlane_revJ.FCStd`. Build files: `cad/release_revJ/`.

## What was removed

| Removed | Parts |
|---|---|
| Ball bay | `Hopper` (replaced by `Fuselage`), `Gate_L/R`, gate torque rods, horns and pushrods, `ServoBracket_Gate`, gate servo |
| Load port | `Chute`, `PortLid_L/R`, lid torque rods, horns and pushrods, `ServoBracket_Lid`, lid servo |
| Fairings | `Fairing` (nose shell that blended the pod into the 126 mm wide hopper), `FairingTail` |
| Fasteners | 4 inserts, 2 × M3×8, 2 × M3×6, 4 × M2×8 |

35 items, 89.7 g, plus the 43.7 g hopper. The aircraft now has 4 servos (2 aileron, elevator, rudder).

## The new fuselage

One printed LW-PLA shell, 0.6 mm wall, hung under the spine tube in the same place as the hopper. Frame: X aft from the nose datum, Z up, mm.

| Item | Value | Why |
|---|---|---|
| Side profile (X, Z) | (104, 134) → (138.4, 70) → (280, 70) → (424, 128) → (424, 134) | Front edge is the hopper's front wall line, so the nose pod mates and bolts on unchanged. Bottom at Z 70 is flush with the pod bottom |
| Width | 60 mm to X 280, tapering to 20 mm at X 424 | Same width as the nose pod: no step, so no fairing is needed |
| Length | 320 mm | Fits the 325 mm printer bed in one piece |
| Wing saddles | Copied unchanged from the hopper at X 237 and X 338, with half-bores and 8 insert pockets | Wing clamp caps, spine and bolts are the same parts as rev H |
| Ring frames | 3, at X 237, 287.5, 338; 1.2 mm thick, 7 mm deep | Carry wing loads from the saddles round the section, and stiffen the belly for landing |
| Deck doublers | 2.4 mm thick under each saddle | Spread the clamp bolt loads into the 0.6 mm deck |
| Belly skid | Same 98 × 40 × 1 mm polycarbonate strip, now at Z 69 to 70 | Belly landing |

Volume 53,966 mm³ = 29.7 g (the hopper was 43.7 g). The elevator and rudder servo mounts sit on the deck at X 135 to 168 exactly as before. The inside is empty and can take ballast or a second battery position if the CG needs moving.

*(interp.)* The 0.6 mm wall, frame depth and doubler thickness are carried over from the hopper's proven-in-CAD values; none has been printed or load-tested.

## Result

| | Rev H (cargo) | Rev J (plain) |
|---|---|---|
| Empty mass | 807.3 g | **703.1 g** |
| CG X | 233.6 mm | **224.7 mm** |
| Static margin (NP X 273, chord 240) | 16 % | **20 %** |
| Parts in assembly | 155 | 120 |
| Printed part types | 25 | 12 |
| Servos | 6 | 4 |
| Span | 1192 mm | 1192 mm |

## Key checks (from `cad/release_revJ/`)

- All 120 parts touch the structure; none floats.
- Clashes above 2 mm³: only the 3.8 mm³ elevator/stab hinge-line overlap inherited from rev H.
- Fuselage is one valid solid, 320 × 72 × 60 mm.
- Nose pod, both clamp caps, spine, 8 saddle inserts and both servo mounts are in contact with the fuselage.

## Known issues

- **Solver workaround.** With the cargo joints removed, FreeCAD 1.1.1's assembly solver crashed internally ("Solve failed: vector", during its redundant-constraint check). No joint was wrong: the smallest failing set was 13 unrelated joints, and joint order, hinge limits and joint types made no difference. The fix is to ground the nose sub-assembly directly (`Ground NoseAssy`) instead of fixing it to the spine, which is itself grounded, so the result is the same rigid connection. The original joint is kept, suppressed. The solver now returns 0 and no part moved. If the spine's pod station is ever changed, re-enable that joint, solve, and suppress it again.
- Two fixed joints for the pushrod Z-bends are flagged invalid by FreeCAD (also in rev H); the parts sit in place.
- **The fuselage is a script-built solid, not a sketch-driven body.** To change it, edit the numbers at the top of `build_revJ.py` and re-run it on rev H.
- **The CG is 9 mm further forward than rev H.** That is on the safe side for a beginner, but it needs more up-elevator trim; move the battery aft in the pod if it flies nose-heavy.
- **This version carries no payload**, so it cannot score in the Techfest payload rounds. Rev H remains the competition version.
- The two insert bosses at X 88 on the nose pod (for the old fairing) are now unused.
