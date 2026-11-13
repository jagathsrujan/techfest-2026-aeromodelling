# FreeCAD Modelling Plan — rev B

The source of every number is [02_detailed_design.md](02_detailed_design.md). This file says how to model it. Items marked *(interp.)* are modelling choices, not design data.

## Setup
- Work in a **new** FreeCAD document named `TechfestPlane_revB`. **Do not touch** the already-open documents `ElectricPayloadAircraft` or `Cycloidal_Drive___PRINT_READY`.
- Save to `/Users/jagathsrujan/Documents/aeromodelling for iit bombay techfest/design/cad/TechfestPlane_revB.FCStd`. Save after every part.
- The FreeCAD addon is old (no `get_rpc_status`). Use `execute_code` with Part-workbench Python.
- Build each part as one script and store it as one `Part::Feature` with the name given below.
- Units mm. After each part print `isValid()`, the BoundBox and the Volume.

## Frame
- **Origin:** front face of the firewall, on the centreline, at belly level (Z = 0).
- **+X** aft, **+Y** starboard, **+Z** up. FreeCAD's X/Y/Z are the same axes.
- Everything is modelled in assembled position. Mirror port/starboard parts about the XZ plane.

## Airfoil helper (NACA 4412)
- Use m = 0.04, p = 0.4, t = 0.12, with a closed trailing edge (coefficient −0.1036).
- Cosine spacing, about 60 points per surface. Build a closed BSpline wire (upper TE→LE→lower TE) in the local XZ plane, with chord along +X.
- Incidence +2°: rotate the section about its LE so the **LE goes up** (rotate about the Y axis through the LE by −2° in FreeCAD's convention, then check that the TE Z is lower than the LE Z).

## Parts

| # | Object name | Shape / construction | Key coordinates | Colour |
|---|---|---|---|---|
| 1 | `Fuselage_Pod` | Hollow shell, 3 mm walls. **Main box:** X 60–400, Y ±50.5, Z 0–135. **Nose:** loft from an 80×80 square at X 0 (centred Y 0, Z 70) to the full section at X 60. **Tail cone:** loft from the full section at X 400 to a 30×30 square at X 470 (centred Z 110). Cut the bay openings: top hatch opening X 145–329, Y ±47.5; belly opening X 145–329, Y ±47.5. Leave the firewall at X 0–3 solid. | BB ≈ X 0–470, Y ±50.5, Z 0–135 | light grey (Depron) |
| 2 | `Bay_Divider` | Plate X 232–242, Y ±47.5, Z 3–98 | | white |
| 3 | `Bay_Floor_Cradle` *(interp.)* | Skip the dimples. Two thin rails (3 × 3 mm) along X 145–329 at Y ±0, Z 3–6, to show the row split | | white |
| 4 | `Hatch_Lid` | Plate 184 × 95 × 3: X 145–329, Y ±47.5, Z 132–135, **closed** | | balsa tan |
| 5 | `Belly_Door_L` / `Belly_Door_R` | Plates 184 × 46.75 × 3 that fill the belly opening. Hinge lines along X at Y ±47.5 (inner wall), Z 0. Modelled **closed**: X 145–329, Y 0.75–47.5 (and mirror), Z 0–3 | | balsa tan |
| 6 | `Wing_Panel_R` / `Wing_Panel_L` | Loft (ruled) the NACA 4412 section, chord 240, +2° incidence, root LE at (X 170, Y ±50.5, Z 112), tip LE at Y ±595 projected. Apply 3° dihedral by rotating the panel about the X-axis line through (Y ±50.5, Z 112) so the tip goes **up**. Tip at Y = ±595 **projected** (panel length 545/cos 3° = 545.75). Solid is fine; no ribs. | Span check: overall Y extent ≤ ±600 | white / red film |
| 7 | `Aileron_R` / `Aileron_L` | Cut from the panel: the strip of the last 55 mm of chord (TE side), Y 205–585 projected. Store as a separate object coloured differently; the panel keeps the cut-out | | red |
| 8 | `Spar_Tube_R` / `Spar_Tube_L` | Ø8 tubes (Ø6 bore). Starboard panel tube at X 243, port at X 231. Each runs from the opposite fuselage wall (Y ∓50.5) to Y ±500 along its panel's dihedral line, at mid-thickness of the airfoil at that chord station (Z ≈ 119 at the root) | | black (carbon) |
| 9 | `Wing_Pin_R` / `Wing_Pin_L` | Ø4 stubs at X 360, from Y ±40 to ±150 along the dihedral, at mid-thickness | | black |
| 10 | `Tail_Boom` | Tube Ø12 / Ø10, axis X 380–946, Y 0, Z 110 | | black |
| 11 | `H_Stab` | Flat plate 5 mm: X 801–896 (fixed part, 95 mm), Y ±200, Z 116–121 | | white |
| 12 | `Elevator` | Plate X 896–946, Y ±200, Z 116–121 | | red |
| 13 | `V_Fin` | Flat plate 5 mm thick (Y ±2.5). Trapezoid in XZ: root at Z 121 from X 776 to X 886; tip at Z 281 from X 826 to X 886 (fixed part) | | white |
| 14 | `Rudder` | Plate X 886–946 for Z 121–281, Y ±2.5 | | red |
| 15 | `Motor` | Cylinder Ø28, X −32 to 0, axis Y 0, Z 70 | | dark grey |
| 16 | `Spinner` | Cone Ø30 → Ø0, X −50 to −32 | | silver |
| 17 | `Prop_Disc` *(interp.)* | Thin disc Ø254 (10 in, placeholder), 2 mm thick, at X −40, axis on the thrust line. Make it transparent (Transparency 80) | | dark grey |
| 18 | `Battery` | Box X 20–140, Y ±17.5, Z 35–70 (3S 1000–1300 placeholder; raised in verification so it clears the nose taper) | | blue |
| 19 | `Servos` *(interp.)* | Boxes 23 × 12 × 25 at: hatch X 118–141 top right inside; belly X 340–363; ele/rud X 375–398 (two side by side); aileron one in each panel at Y ±150, X 300 (inside the wing outline) | | dark blue |
| 20 | `Nose_Gear` | Leg Ø2.5 from (X 25, Z 0) to the axle (X 25, Z −75); wheel Ø50 × 15, axis Y, centre (X 25, Y 0, Z −75) | | black |
| 21 | `Main_Gear` | Each side: leg Ø2.5 from (X 282, Y ±50.5, Z 60) to the axle (X 282, Y ±150, Z −72.5); wheel Ø55 × 18, centre (X 282, Y ±159, Z −72.5) | | black |
| 22 | `Golf_Balls` | 10 spheres Ø43 (design load): all 8 bottom slots + 2 top inner slots, as in 02 §Payload. **Bottom layer** Z centre 25: X centres 167, 210 (front half) and 264, 307 (rear half); Y centres ±23.75. **Top layer** Z 68: (X 210, Y +23.75) and (X 264, Y −23.75), diagonal so the load is balanced in roll | | white |

## Deliverables (in `design/cad/`)
1. `TechfestPlane_revB.FCStd` with only the named parts above, no temporary objects.
2. `TechfestPlane_revB.step`: whole assembly via `Import.export`.
3. PNGs, 1600 × 1000, white background, `fitAll` first:
   - `iso.png` (isometric)
   - `top.png`, `side.png` (from +Y looking −Y, nose to the left), `front.png`
   - `bay_section.png`: temporary copies of the pod, divider, doors, lid and balls cut by the plane Y = 0, viewed from the side, then deleted before saving
   - `bay_open.png`: temporary copies of the doors rotated 120° outward about their hinge lines and the lid rotated 100° about its port hinge, iso view from below-front, then deleted
4. Print a table of each object's BoundBox and volume at the end.

## Key checks (subagent and verifier)
- Overall Y extent of the wing tips: **≤ ±600, target ±595 (span 1190)**.
- Overall X extent: −50 (spinner) to 946 (elevator/rudder TE).
- Wing root LE at X 170. The TE at the root is ~X 410 and sits *lower* than the LE (positive incidence).
- Wing tip LE Z ≈ 112 + 545·tan 3° ≈ 140.6 (dihedral up).
- The bay interior (X 145–329, Y ±47.5, Z 3–98) holds all 10 balls with no interference with the walls, divider, doors or lid. Check the `common()` volume of balls vs. other parts = 0.
- The spar tubes pass above the bay (bottom of the tube ≥ Z 98) and don't intersect any ball.
- Ground contact: the bottom of every wheel is at Z ≈ −100. The prop disc bottom is at Z 70 − 127 = −57, so prop clearance is ≥ 40 mm.
- Tail: H_Stab + Elevator area 400 × 145 = 58 000 mm². Fin + rudder ≈ 23 200 mm².

---

# Rev C changes (2026-11-03, after design review)

The rev B model is in `TechfestPlane_revB.FCStd`. Rev C fixes the engineering faults listed below. Start from the rev B document, save it as **`TechfestPlane_revC.FCStd`** in `design/cad/` (keep the revB file untouched on disk), and apply the changes. Everything not listed stays as in rev B.

## Faults found in rev B → fix

| # | Fault | Fix |
|---|---|---|
| C1 | One-piece elevator runs under the rudder and lies on the boom end, so it can't deflect, and the rudder sits on it | Split the elevator into 2 halves joined by a wire. Elevator and rudder share the hinge line X 896. The boom ends under the fixed stab |
| C2 | Spar tubes cross the bay/hatch opening, overlap each other and carry the whole wing bending load across an open box | Add a **spar bulkhead** at the CG: a full-height box beam (ply webs, carbon caps). Each panel's spar tube plugs into a socket **inside** the bulkhead. No tube crosses the bay |
| C3 | The bay is an open box with 3 mm foam walls at the most heavily loaded station | Add ply bulkheads F2 (front of bay) and F3 (rear of bay) and carbon longerons along the 4 bay edges |
| C4 | Main gear legs anchored to a foam wall | Add 1.5 mm ply gear doubler plates on the outside of each side wall, X 243–330, spanning between the spar bulkhead and F3 |
| C5 | Boom held only 90 mm deep in the foam tail cone | Run the boom forward into a socket at F3 (two support points ~140 mm apart). Add a ply tail saddle under the stab |
| C6 | Wing roots intersect the pod (dihedral rotated about the LE line) | Trim each panel with the pod outer box so the root face is flush with the side wall (the real root rib is cut at 3°) |
| C7 | Floor cradle floats when the doors open; it clashes with the divider | Delete `Bay_Floor_Cradle`. Any cradle rails belong on the doors |
| C8 | Nose gear leg starts below the nose skin | Extend the leg up to a ply firewall bracket |

## Revised geometry (absolute frame unchanged)

| Object | Action | Geometry |
|---|---|---|
| `Bay_Divider` | **Delete**, replaced by `Spar_Bulkhead` | |
| `Spar_Bulkhead` | New | Box X 231–243, Y ±47.5, Z 3–132 (two 3 mm ply webs + 6 mm balsa core; model it as a solid box). Colour ply tan |
| `Spar_Cap_Top` / `Spar_Cap_Bot` | New | Carbon strips X 231–243, Y ±47.5, Z 129–132 and Z 3–6 (inside the bulkhead box; for visualisation only, so they may overlap the bulkhead; make them black and listed separately) |
| `Bulkhead_F2` | New | Plate X 141–144, Y ±47.5, Z 3–132, ply tan |
| `Bulkhead_F3` | New | Plate X 330–333, Y ±47.5, Z 3–132, ply tan, with a Ø12.2 hole on the boom axis (Y 0, Z 110) |
| `Longerons` | New | Four 3 × 3 carbon strips, X 141–333, along the inside corners of the bay opening: (Y ±44.5..±47.5, Z 129–132) and (Y ±44.5..±47.5, Z 3–6). Black |
| `Fuselage_Pod` | Modify | The bay openings (top and bottom) become X 144–330, Y ±47.5. Bore holes for the boom (Ø12.2 on axis Z 110) through the tail cone end wall. Cut the spar socket holes (see the spar tubes) and the pin holes through the side walls |
| `Hatch_Lid` | Modify | X 144–330, Y ±47.5, Z 132–135 |
| `Belly_Door_R` / `_L` | Modify | X 144–330, Y 0.75..47.5 / −47.5..−0.75, Z 0–3; hinges at Y ±47.5, Z 0 (unchanged) |
| `Spar_Tube_R` / `_L` | Modify | Ø8 tube (Ø6 bore), **both at X 237**. Starboard from Y +2.5 to Y +500, port mirror. Along the 3° dihedral line through the root point (Y ±50.5, Z 118). The inner 48 mm sits inside `Spar_Bulkhead` (the socket). The two tubes must not touch (gap ≥ 5 mm at Y 0) |
| `Wing_Pin_R` / `_L` | Modify | Ø4 stubs at **X 331.5** (inside F3), from Y ±20 to Y ±150 along the dihedral, at mid-thickness of the airfoil at that chord station |
| `Wing_Panel_R` / `_L`, `Aileron_R` / `_L` | Modify | Cut each with the pod outer box (X 0–470, Y ±50.5, Z 0–135) so it no longer intersects the pod. Then cut holes in the panel for its spar tube and pin (so they no longer overlap as solids) and a servo pocket for the aileron servo |
| `Golf_Balls` | Modify | Same 10 balls. Bottom layer X centres **166, 209, 265, 308**, Y ±23.75, Z 25. Top layer Z 68 at (X 209, Y +23.75) and (X 265, Y −23.75). Mean X stays 237 |
| `Tail_Boom` | Modify | Tube Ø12/Ø10, X **333–890**, Y 0, Z 110 (starts at the F3 socket, ends under the fixed stab, short of the hinge at 896) |
| `Tail_Saddle` | New | Ply block X 801–890, Y ±10, Z 110–116 minus the boom cylinder (supports the stab and sets its incidence) |
| `Elevator` | **Delete**, replaced by `Elevator_R` / `Elevator_L` | Plates X 896–946, Y +25..+200 and −200..−25, Z 116–121 |
| `Elevator_Joiner` | New | Ø1.5 wire, X 900, Z 118.5, Y −30..+30 (passes under the rudder) |
| `V_Fin` | Modify | Trapezoid, 5 mm thick: root Z 121, X 776–896; tip Z 281, X 826–896 |
| `Rudder` | Modify | X 896–946, Z **122**–281, Y ±2.5 (1 mm gap above the stab) |
| `Gear_Doubler_R` / `_L` | New | Ply plates X 243–330, Y ±50.5..±52, Z 0–100 (outside the side walls). The main gear legs start on these: leg top at (X 282, Y ±52, Z 60) |
| `Main_Gear` | Modify | Leg from (X 282, Y ±52, Z 60) to the axle (X 282, Y ±150, Z −72.5); wheels as before |
| `Nose_Gear` | Modify | Leg from (X 25, Y 0, Z 40) (through the firewall bracket) to the axle (X 25, Z −75); wheel as before |
| `Nose_Gear_Bracket` | New | Ply block X 3–25, Y ±12, Z 20–45 behind the firewall (clip it to inside the pod shell) |
| `ESC` | New | Box X 25–75, Y ±13, Z 24–34 (under the battery), dark blue |
| `Receiver` | New | Box X 340–380, Y −25..−5, Z 40–52, dark blue |
| `Bay_Floor_Cradle` | **Delete** | |

## Rev C key checks (in addition to the rev B ones that still apply)
- **No clashes:** a pairwise `common()` volume of 0 (< 1 mm³) between all objects, **except** these allowed pairs:
  - pod + boom inside the F3/cone hole region (should now be 0 because the hole is bored)
  - spar caps inside `Spar_Bulkhead`
  - spar tubes inside `Spar_Bulkhead` (the socket), only if you don't bore the socket. Prefer boring it, so 0
  - `Gear_Doubler` + `Main_Gear` leg top < 50 mm³

  Report every pair that remains.
- The elevator halves and the rudder have ≥ 1 mm clearance. The rudder swept ±25° about its hinge line (X 896) does not hit either elevator half or the stab. Check by rotating temporary copies of the rudder and computing `common()`, then delete the copies.
- Each elevator half swept ±20° about the hinge line (Y axis through X 896, Z 118.5) does not hit the boom, the saddle or the rudder (temporary copies, then delete).
- Belly doors swept to 120° do not hit the gear doublers or the main gear legs (temporary copies).
- Hatch lid opened to 100° about (Y −47.5, Z 135) does not hit the port wing panel (temporary copy).
- All 10 balls are inside the bay halves with 0 overlap with any object. The front half is X 144–231 and the rear half X 243–330.
- Span: the wing panel BoundBox Y is still ≤ ±600.

## Rev C deliverables
- `TechfestPlane_revC.FCStd`, `TechfestPlane_revC.step`
- PNGs with the suffix `_revC`: `iso`, `top`, `side` (FreeCAD Front view, nose left), `front` (FreeCAD Left view, looking at the nose), `bay_section` (Y = 0 cut through the pod, bulkheads, balls and doors), `bay_open`, `tail_detail` (iso close-up of the tail with the rudder at +25° and the elevators at −20° on temporary copies).
- Set **every** object visible before taking the screenshots (the pod and lid were hidden in rev B). Delete all temporary objects before saving.

---

# Rev D changes (2026-11-03): no landing gear, side ramp doors, raised motor

Start from `design/cad/TechfestPlane_revC.FCStd`. Save as **`TechfestPlane_revD.FCStd`** with `saveAs`, leaving revC on disk unchanged. The open document may still be internally named `TechfestPlane_revB`; that's fine. Everything not listed stays as in rev C.

## Delete
`Belly_Door_R`, `Belly_Door_L`, `Main_Gear`, `Nose_Gear`, `Nose_Gear_Bracket`, `Gear_Doubler_R`, `Gear_Doubler_L`.

## Modify / add

| Object | Action | Geometry |
|---|---|---|
| `Fuselage_Pod` | Rebuild the nose and openings, keeping the rest (3 mm shell) | **Nose:** loft from a rectangle at X 0 (Y ±35, Z 30–180) to the full section at X 60 (Y ±50.5, Z 0–135); this is the firewall face. **Belly:** closed (no belly opening any more); the 3 mm bottom wall is the bay floor base. **Side door openings:** cut both side walls (and the bottom-wall edge strip Y ±47.5..±50.5) over X 144–330, Z 0–58. Top hatch opening unchanged (X 144–330, Y ±47.5). Keep all existing bores (spar sockets, pins, boom) |
| `Bay_Floor_Ridge` | New | Two prisms (X 144–231 and X 243–330), each with a triangular section: (Y −47.5, Z 3), (Y 0, Z 11), (Y 47.5, Z 3), sitting on the bottom wall (Z 3). Balsa tan |
| `Spar_Bulkhead`, `Spar_Cap_Bot`, `Bulkhead_F2`, `Bulkhead_F3` | Modify | Cut each with `Bay_Floor_Ridge` extended through their X range, so they sit on the ridge and don't overlap it |
| `Side_Door_R` / `_L` | New | Plates X 144–330, Y 47.5..50.5 (and mirror), **Z 0–57** (1 mm gap under the wall so the inner top edge clears on opening; set in verification), closed. Hinge axis along X through (Y ±50.5, Z 0); they open outward 90° to lie flat (Z 0–3, Y ±50.5..±108.5). Balsa tan |
| `Longerons` | Modify | Keep the 4 top segments. Replace the 4 bottom segments with 2 external **door-header** strips, X 144–330, Y ±50.5..±53.5, **Z 59–62** (raised 1 mm in verification) (black carbon) |
| `Golf_Balls` | Modify | 10 spheres Ø43. Bottom layer: X 166, 209, 265, 308 at Y ±25.9, Z 28.5 (resting on the 9.6° ridge slope and against the closed door). Top layer: Z 71.5 at (X 209, Y +25.9) and (X 265, Y −25.9) |
| `Motor`, `Spinner`, `Prop_Disc` | Move | Thrust line through (X 0, Y 0, **Z 155**) with **2° up-thrust**: build them as in rev B on an axis at Z 155, then rotate all three about the point (0, 0, 155) around the Y axis so the front (−X end) rises. Prop_Disc stays Ø254 × 2, transparency 80 |
| `Motor_Mount` | New | Ply plate X 0–3, Y ±30, Z 130–180 (a doubler on the firewall face behind the motor, inside the nose loft), ply tan. Clip it to inside the pod outer envelope if needed |
| `Belly_Skid` | New | Plate X 60–400, Y ±20, Z −1–0 (replaceable polycarbonate), dark grey |
| `Servos` | Check | The box at X 340–363 now drives the side doors. If any servo box clashes with the new nose or floor, move it by the smallest amount and report it |

## Rev D key checks
- **Pairwise clashes:** every pair has `common()` volume < 1 mm³, except the allowed spar caps inside `Spar_Bulkhead` and the `Spinner` + `Prop_Disc` pair. Report every remaining pair.
- **Ground:** the lowest point of the whole model is `Belly_Skid` at Z −1. No other object goes below Z 0.
- **Prop clearance:** the lowest point of `Prop_Disc` is at Z ≥ 25. Report the value.
- **Balls:** all 10 lie fully inside the pod envelope, with 0 overlap with the ridge, doors, walls, bulkheads, lid, longerons and each other. Report the minimum gap to `Bay_Floor_Ridge`.
- **Side doors at 90°:** use temporary copies. Each door lies at Z 0–3 outboard of the pod, clashes with nothing, and its top surface is within 1 mm of the floor edge height (Z 3) so the balls roll straight out. Delete the copies after.
- **Hatch lid at 100°:** still clear of the port wing. Re-check it.
- **Span:** unchanged, wing Y extent ≤ ±600.

## Rev D deliverables (design/cad/)
- `TechfestPlane_revD.FCStd` and `TechfestPlane_revD.step`.
- PNGs with suffix `_revD`, all objects visible, 1600 × 1000, white background:
  - `iso`
  - `top`
  - `side` (FreeCAD Front view, nose left)
  - `front` (FreeCAD Left view, looking at the nose)
  - `bay_section`: a **section at X 209** looking aft, showing the ridge, balls, side doors and wing roots. Make it from temporary cut copies, then delete them
  - `doors_open`: an iso view from front-below-side with temporary copies of both doors at 90° and the hatch at 100°
- Delete all temporary objects before the final save.

---

# Rev E changes (2026-11-03): S1223 wing, bigger tail (benchmark-driven)

Start from `design/cad/TechfestPlane_revD.FCStd` and `saveAs` **`TechfestPlane_revE.FCStd`**, leaving revD on disk unchanged. The open document may still be internally named `TechfestPlane_revB`. Everything not listed stays as in rev D.

## Airfoil
- Use **Selig S1223** from `design/calc/s1223.dat`: UIUC Selig format, 1 header line then x y pairs running TE → upper → LE → lower → TE, closed TE at (1,0).
- Build the section as a closed BSpline through the points, scaled to chord 240.
- S1223 sits higher on its chord line than NACA 4412: upper surface up to 13.5% c, mid-line 7.7% c at 28% chord. So **the root chord line is lowered: root LE at (X 170, Z 100)** instead of Z 112.
- Incidence +2° (LE up) and dihedral 3° are as before, with the dihedral rotation about the X-parallel line through (Y ±50.5, Z 100).
- Expected at the root:
  - upper surface max ≈ Z 132 at 28% chord
  - lower surface ≈ Z 98–99 near the LE
  - TE ≈ Z 91.6

## Modify

| Object | Geometry |
|---|---|
| `Wing_Panel_R` / `_L` | Rebuild with S1223 as above, chord 240, span to Y ±595 projected, root trimmed flush with the pod outer box (Y ±50.5). Cut the bores for the spar tube and pin, and the servo pocket at the new positions below |
| `Aileron_R` / `_L` | Last 55 mm of chord (X 354.9–409.9 at zero incidence), Y 205–585 projected, cut from the new panel (it is thin there, which is fine) |
| `Spar_Tube_R` / `_L` | Ø8, X 237, from Y ±2.5 to ±500 along the dihedral. Root centre at **mid-thickness of the S1223 section at 28% chord ≈ Z 118** (re-measure from the built section: (upper + lower)/2 at X 237 on the root face) |
| `Spar_Bulkhead` | Re-bore the spar sockets at the new tube height. The tube must not touch `Spar_Cap_Top` (Z 129–132). If it does, report the overlap |
| `Wing_Pin_R` / `_L` | Ø4 at X 331.5, Y ±20..±150, at mid-thickness of the section at that station (≈ Z 113.5). Re-bore F3 and the pod |
| `Servos` (the two aileron boxes only) | Move to X 255–280 (inside the thicker forward part of S1223), Y ±150 ± 11.5, centred on mid-thickness. Cut the pocket in the panel |
| `H_Stab` | Flat plate 5 mm: **X 791–891, Y ±250**, Z 116–121 |
| `Elevator_R` / `_L` | **X 891–946**, Y +27..+250 and −250..−27, Z 116–121 (inner edge moved 25 → 27 in verification so the rudder clears at +25° / −20°) |
| `Elevator_Joiner` | Ø1.5 at X 895, Z 118.5, Y ±30. Re-cut the joiner holes in the elevators |
| `V_Fin` | Trapezoid, 5 mm: root Z 121, X 776–891; tip Z 281, X 826–891 |
| `Rudder` | **X 891–946**, Z 122–281, Y ±2.5 |
| `Tail_Saddle` | X 791–885, Y ±10, Z 110–116, minus the boom |
| `Tail_Boom` | X 333–**885** (ends under the fixed stab, short of the 891 hinge) |

## Rev E key checks
- **Pairwise clashes:** every pair has `common()` < 1 mm³ except the allowed spar caps inside `Spar_Bulkhead` and the `Spinner` + `Prop_Disc` pair. Report every remaining pair.
- **Wing section:** report the root-face Z of the upper-surface max, the lowest lower-surface point and the TE. Expect ≈ 132, ≈ 98 and ≈ 91.6.
- The wing panels do not rise above the pod roof by more than the airfoil itself, and the hatch lid at 100° still clears the port wing. Re-check that.
- **Span:** wing Y extent ≤ ±600.
- **Tail:** stab + elevators area = 100 × 500 + 2 × 225 × 55 = 74 750 mm². Report it. Fin + rudder ≈ 23 100 mm².
- **Tail sweeps:** rudder ±25° about X 891 and elevators ±20° about (X 891, Z 118.5), using temporary copies. Report clashes with the boom, saddle, joiner, fin and each other. Hinge-corner overlaps with their own fixed surface are acceptable (bevelled hinges in the build); report them separately.
- **Ground:** the lowest point is `Belly_Skid` at Z −1. The prop disc bottom is ≥ 25.
- **Balls:** all 10 still have 0 overlap.

## Rev E deliverables (design/cad/)
- `TechfestPlane_revE.FCStd` and `TechfestPlane_revE.step`.
- PNGs with suffix `_revE`, all objects visible, 1600 × 1000, white background:
  - `iso`
  - `top`
  - `side`
  - `front`
  - `wing_root_section`: a section through the starboard wing at Y = 300, viewed from +Y (FreeCAD Rear view), showing the S1223 shape, spar and aileron. Use temporary cut copies and delete them after
  - `tail_detail` (rudder at +25° and elevators at −20° on temporary copies)
- No temporary objects left in the saved file.

---

# Rev F changes (2026-11-03): streamlined nose, 13 in folding prop on a centred thrust line

Start from `design/cad/TechfestPlane_revE.FCStd` and `saveAs` **`TechfestPlane_revF.FCStd`** first, leaving revE on disk unchanged. The internal document name may still be `TechfestPlane_revB`. Everything not listed stays as in rev E.

## Delete
`Motor_Mount`, the high Z 130–180 plate.

## Modify / add

| Object | Geometry |
|---|---|
| `Fuselage_Pod` | Replace only the nose (X 0–70); keep everything aft of X 70, including all bores, side-door openings, the hatch opening and the closed belly. New nose:<br>- outer loft from a **50 × 50 square at X 0 (Y ±25, Z 42–92)** to the full outer section at **X 70** (Y ±50.5, Z 0–135), with 3 mm walls<br>- a solid 3 mm firewall at X 0–3 (ply)<br>- the inner cavity must join the existing pod interior smoothly<br>This replaces the tall rev D/E nose (the X 0 rectangle Z 30–180 and the loft to X 60) |
| `Motor` | Cylinder Ø35, X −40 to 0, axis through (Y 0, Z 67), parallel to X (0° down-thrust, 0° side-thrust) |
| `Spinner` | Folding-prop yoke + spinner: cone Ø44 → Ø6 from X −40 to −72, same axis |
| `Prop_Disc` | Disc **Ø330** (13 in), 2 mm thick, centred at X −48 on the axis, transparency 80 (flight pose, blades open) |
| `Battery` | X 20–140, Y ±17.5, **Z 40–75**. It must fit inside the new nose cavity; if it clashes, shorten it from the front (minimum X 30) and report it |
| `ESC` | Move to **X 340–390, Y ±13, Z 60–70** (behind F3). Must not touch the receiver, servos, boom, pins or pod |

## Rev F key checks
- **Pairwise clashes:** every pair has `common()` < 1 mm³ except the allowed spar caps inside `Spar_Bulkhead` and `Spinner` + `Prop_Disc`. Report every remaining pair.
- **Nose:** report the pod outer BoundBox and the cross-section at X 0, 20, 40 and 70: width and Z range of the outer and inner cavity. The battery is inside the inner cavity at every X.
- **Prop:** the disc diameter is 330. Report the disc's lowest Z (it should be ≈ −98; this is expected, since the motor is off at touchdown) and confirm the disc touches nothing but the spinner.
- **Folded-prop pose:** build temporary copies of two blades, each 145 × 25 × 3 mm. Hinge them on the yoke at radius 22 (one up at Z 89, one down at Z 45) at X −45. Fold them back towards +X until each lies at 1 mm off the nose surface or 10° from the axis, whichever comes first.
  - Report the lowest Z of the folded lower blade (must be ≥ 0, so above the belly skid at −1).
  - Report any clash with the pod.
  - Take the screenshot `side_folded_revF.png`, then delete the copies.
- **Ground:** the lowest point of the model (excluding the open `Prop_Disc`) is `Belly_Skid` at Z −1.
- **Span:** unchanged, ≤ ±600.

## Rev F deliverables (design/cad/)
- `TechfestPlane_revF.FCStd` and `TechfestPlane_revF.step`.
- PNGs with the suffix `_revF`, all objects visible, 1600 × 1000, white background:
  - `iso`
  - `top`
  - `side` (FreeCAD Front view, nose left)
  - `front`
  - `side_folded`
  - `nose_detail`: iso close-up of the nose with the prop disc hidden
- No temporary objects left in the saved file.

## Rev F verification changes (applied directly, 2026-11-03)
- **Folded lower blade:** with the agent's 50 × 50 nose, the folded lower blade reached Z −13, under the belly. Any 145 mm blade folded under the nose ends up below the flat belly at X > 70.
  - Fix part 1: the nose firewall became Y ±25, Z 30–92 (loft to the full section at X 70).
  - Fix part 2: a **blade channel** was cut in the belly. Void: XZ polygon (−5,−5)(110,−5)(110,0)(0,40)(−5,40) extruded Y ±15. Liner: polygon (0,−5)(119,−5)(119,0)(0,43) extruded Y ±18 minus the void, clipped to the outer envelope.
- **Result:** the lower blade rests at 17° from the axis, lowest Z +1.17, tip X 94. The upper blade rests at 23°, top Z 147.
- **Belly_Skid** shortened to X 110–400 so it clears the channel.
- The pod is valid (1 solid). Nothing clashes with the pod, and the battery has a 4 mm gap to the shell.
