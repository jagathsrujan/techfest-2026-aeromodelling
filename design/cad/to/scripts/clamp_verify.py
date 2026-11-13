import sys, json
import verify, clamp_beso
brep = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else ""
r = verify.verify("clamp_F", brep, clamp_beso.build_cases, h=float(sys.argv[3]) if len(sys.argv) > 3 else 1.2, hmin=0.4, tag=tag)
print(json.dumps(r, indent=1))
