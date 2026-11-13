# Rev G: carbon-spine + V-funnel hopper (team concept, 2026-11-03)

Source: the team sketch (`IMG_1731.HEIC`, Downloads). It shows a single carbon tube from nose to tail, a nose electronics pod with a 13 in prop, a triangular payload hopper under the wing (load on top, unload at the bottom), and the tail + rudder on the tube end.

Decisions agreed with the team:
- symmetric 60° V hopper centred under the CG;
- loading through a port behind the wing that feeds a chute;
- unloading through side gates at the bottom row;
- a printed **bolted** clamp joining the wing spar and the spine;
- a flat wing with one continuous spar.

## Is it better than rev F?

| | Rev F (box pod) | Rev G (spine + hopper) | Why |
|---|---|---|---|
| Empty weight *(est.)* | 739 g | **715 g** | One 16 × 14 carbon spine replaces the pod box, bay bulkheads, longerons and boom |
| Qualifier score, 16 balls | ~97 | **~101** | 720 g payload / empty weight |
| Static thrust cap | ≤ 739 g | ≤ 715 g | T/W ≤ 1 rule. Still ample, since cruise drag ≈ 230 g |
| Fuselage drag | Box 101 × 135 × 470 | Small nose pod + tapered hopper, ~half the wetted area | Modest gain; induced drag dominates at our CL |
| Loading (C1, C2b) | Balls dropped into two halves of a fixed 2-layer bay | **Funnel: drop anywhere, gravity seats them** | Est. −3 to −6 s per load, about +6 to +12 main-round points |
| Unloading (C2a, C3) | 2 side ramp doors | 2 side gates at the bottom row; the upper rows feed down | About the same (~2–3 s) |
| CG with partial loads | Fixed slots, pattern-dependent | **Self-centring**: a symmetric V fills from the bottom up around the centreline | Fewer trim surprises |
| Structure / repair | Many glued foam parts | One spine. Pod, hopper, tail and wing bolt or clamp on, and each can be swapped | Better field repair (same airframe rule) |
| Risks | Known | Ball bridging in the funnel; a long servo pushrod run; the wing clamp must be stiff | All testable on the bench before flying |

**Verdict:** rev G is better overall. It's lighter, should be faster on the ground, and is easier to repair, though the aerodynamic gain is small. Adopted as the new baseline. Rev F stays on disk.

## Frame and key geometry (all mm)
- **Origin:** firewall front face (X 0), centreline (Y 0). **Z 0 = hopper bottom outer surface.** X aft, Y starboard, Z up.
- **Design CG:** X 237 (28% MAC). Estimated empty CG: X 232.
- **Hopper:** bottom centre at **X 225**, 7 mm ahead of the empty CG. This is deliberate, so the parked plane always tips **tail-down** onto its tail skid (about 11°) and the nose and prop stay off the ground.

| Part | Geometry |
|---|---|
| Spine | Carbon tube Ø16 / Ø14, axis Y 0, **Z 142**, X 3–946 |
| Wing | One piece, **flat (0° dihedral)**, S1223, chord 240, span 1190 (Y ±595), **LE X 170, chord line at LE Z 160**, incidence +2° (LE up). Ailerons: last 55 mm chord, Y ±205–585 |
| Wing spars | Front Ø10 carbon at X 237 (28% c), Z ≈ 176.3 (mid-thickness), Y ±560. Rear Ø4 carbon at X 338 (70% c), Z ≈ 172.4, Y ±560 |
| Wing clamps (printed, bolted) | Front: block X 229–245, Y ±15, Z 134–184, wrapping the spine and the front spar. Rear: block X 330–346, Y ±12, Z 134–180, wrapping the spine and the rear spar |
| Hopper | Symmetric trapezoid in side view. **Outer bottom X 176–274 at Z 0; outer top X 104–346 at Z 134** (walls ≈ 61.7°). Outer width Y ±59 (inner ±56, so two balls fit beside the spine at the load port). 3 mm walls. Top plate Z 131–134; the spine sits on it |
| Hopper floor | Fixed. 3 mm plate plus a ridge 8 mm high on the centreline sloping to Y ±56 (as rev F), inner bottom X 179–271 |
| Side gates | Openings in both side walls, X 179–271, Z 0–57. Gates 3 mm, hinged on the bottom outer edge (Y ±59, Z 0), opening 90° outward to lie flat as ramps |
| Load chute + port | Chute inner width 112 (Y ±56), floor plane rising from (X 330, Z 95) at the hopper aft wall to (X 470, Z 131). Side walls up to Z 134. Top cover X 340–415 (under the wing TE). **Load port** open on top at **X 415–470** (behind the TE at X 410), closed by two lids (Y −56..−8 and 8..56, either side of the spine), hinged at the spine |
| Nose pod | Shell 3 mm. Nose taper from 50 × 50 at X 0 (centred Z 110) to 60 × 80 (Y ±30, Z 70–150) at X 40, constant to the hopper. The rear face is the hopper front wall (pod trimmed by the hopper outer solid). The spine runs inside the pod top |
| Motor / prop | Motor Ø35, X −40–0, axis Z 110. Spinner Ø44, X −72 to −40. 13 in folding prop: disc Ø330 at X −48 |
| Electronics (in pod) | Battery X 8–108, Y −25..10, Z 76–106. ESC X 15–65, Y 13..26, Z 76–102. Receiver X 70–100, Y 13..26, Z 76–96 |
| Servos | Ailerons ×2 in the wing at X 225–250, Y ±(138.5..161.5), centred on mid-thickness. Elevator + rudder: two boxes on the hopper top beside the spine, X 140–163, Y ±(9..21), Z 134–158. Gate servo: under the pod, X 85–108, Y ±6, Z 45–70. Port-lid servo: beside the spine, X 475–498, Y 9..21, Z 134–158 |
| Tail | As rev E, raised by 34 (on top of the spine). H_Stab X 791–891, Y ±250, Z 150–155. Elevators X 891–946, Y ±27–250. V_Fin root Z 155, X 776–891; tip Z 315, X 826–891. Rudder X 891–946, Z 156–315. Tail saddle X 791–885, Y ±10, wrapping the spine |
| Skids | Hopper belly skid X 176–274, Y ±20, Z −1–0. Tail skid X 925–946, Y ±6, Z 120–134 (under the spine end) |
| Balls (10 in the CAD) | Layer 1 at Z 28: X 203.25 and 246.75, Y ±34.5 (4 balls). Layer 2 at Z 65.2: X 182, 225 and 268, Y ±34.5 (6 balls). Capacity with layer 3 (Z 102.4, X 160.5 / 203.5 / 246.5 / 289.5) is 18 |

## Key checks (builder and verifier)
1. **Clashes:** no pairwise `common()` > 1 mm³, except a clamp with the tube it clamps (if the bores are not cut) and spinner + prop disc.
2. **Span:** the wing Y extent is ≤ ±600.
3. **Balls:** all 10 lie inside the hopper with 0 overlap. Report the minimum gap to the walls, ridge and gates.
4. **Wing above spine:** the wing lower surface clears the spine top (Z 150) everywhere, including the TE (≈ Z 151.6). Report the minimum gap.
5. **Gates:** gates swept 0–90° clash with nothing, and their open top surface is at floor-edge height.
6. **Port lids:** opened 100° clear the wing TE and the spine. Each side opening is ≥ 46 wide, so a ball passes beside the spine.
7. **Chute:** a Ø43 sphere swept along the chute centreline at Y ±32 from the port down to the hopper clears the chute walls, cover and spine.
8. **Ground:** the hopper skid is the lowest point (Z −1). Report the parked tail-down angle about (X 274, Z −1) onto the tail skid.
9. **Prop disc** Ø330 touches only the spinner.
10. **Tail sweeps:** rudder ±25° and elevators ±20°, with no clash except the own-hinge corners.
