import sys, json, numpy as np
import verify, motor_beso
brep = sys.argv[1]; tag = sys.argv[2]
gj = json.load(open("../work/motor_geom.json"))
geom = dict(dir_pod=np.array(gj["dir_pod"]), dir_mot=np.array(gj["dir_mot"]), pod=[np.array(p) for p in gj["pod"]],
            mot=[np.array(p) for p in gj["mot"]], face_c=np.array(gj["face_c"]), hub=np.array(gj["hub"]))
def bc(mesh, tol=0.05, use_surf=False, which=None):
    return motor_beso.build_cases(mesh, tol=tol, use_surf=use_surf, geom=geom)
r = verify.verify("motor_mount", brep, bc, h=float(sys.argv[3]) if len(sys.argv) > 3 else 0.9, hmin=0.35, tag=tag)
print(json.dumps(r, indent=1))
