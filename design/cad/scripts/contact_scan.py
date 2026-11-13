"""Contact-graph scan of rev H: which parts physically touch which, what floats, what clashes.
Run: freecadcmd design/cad/scripts/contact_scan.py   (writes release_revH/contact_scan.txt)"""
import FreeCAD, Part, os, sys
CAD=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REV=os.environ.get("REV","J")
os.makedirs(os.path.join(CAD,"release_rev"+REV),exist_ok=True)
out=open(os.path.join(CAD,"release_rev"+REV,"contact_scan.txt"),"w")
def P(*a):
    out.write(" ".join(str(x) for x in a)+"\n"); out.flush()
doc=FreeCAD.openDocument(os.path.join(CAD,"TechfestPlane_rev%s.FCStd"%REV))
asm=[o for o in doc.Objects if o.TypeId=="Assembly::AssemblyObject"][0]
leaves=[]
def walk(obj,mat,path):
    for name in obj.getSubObjects():
        r=obj.getSubObject(name,retType=1,matrix=mat)
        if not r or r[0] is None: continue
        sobj,m=r
        lo,lm=sobj.getLinkedObject(True,m,False)
        if lo.TypeId=="PartDesign::Body":
            s=lo.Shape.copy(); s.Placement=FreeCAD.Placement(); s=s.transformed(lm)
            leaves.append((path+name,lo.Label,s,"asm"))
        elif lo.isDerivedFrom("App::Part"): walk(lo,lm,path+name)
walk(asm,FreeCAD.Matrix(),"")
na=len(leaves)
for o in doc.RootObjects:
    if o.TypeId=="App::Link":
        leaves.append((o.Label,o.getLinkedObject(True).Label,Part.getShape(o),"root"))
n=len(leaves); P("asm leaves",na,"root links",n-na)
bbs=[l[2].BoundBox for l in leaves]
adj={i:{} for i in range(n)}; near={}
for i in range(n):
    bi=FreeCAD.BoundBox(bbs[i]); bi.enlarge(5.0)
    for j in range(i+1,n):
        if not bi.intersect(bbs[j]): continue
        try: d=leaves[i][2].distToShape(leaves[j][2])[0]
        except Exception: d=99
        if d<=0.35: adj[i][j]=d; adj[j][i]=d
        elif d<5:
            near.setdefault(i,[]).append((round(d,2),leaves[j][1])); near.setdefault(j,[]).append((round(d,2),leaves[i][1]))
P("distances done")
dups=[]
for i in range(na,n):
    for j in range(na):
        if leaves[i][1]==leaves[j][1] and bbs[i].Center.distanceToPoint(bbs[j].Center)<0.5: dups.append(leaves[i][0]); break
P("root links duplicating an assembly part:",len(dups),dups)
root=[i for i in range(n) if leaves[i][1]=="Spine"][0]
seen={root}; st=[root]
while st:
    a=st.pop()
    for b in adj[a]:
        if b not in seen: seen.add(b); st.append(b)
P("connected:",len(seen),"of",n)
for i in range(n):
    if i not in seen:
        b=bbs[i]; P("FLOATING %-22s (%s,%s) c=(%.0f,%.0f,%.0f) near:%s"%(leaves[i][0][-22:],leaves[i][1],leaves[i][3],b.Center.x,b.Center.y,b.Center.z,sorted(near.get(i,[]))[:3]))
P("--- contacts of every part")
for i in range(n):
    b=bbs[i]
    P("%-22s %-17s %-4s x%.0f y%.0f z%.0f <-> %s"%(leaves[i][0][-22:],leaves[i][1],leaves[i][3],b.Center.x,b.Center.y,b.Center.z,sorted(set(leaves[j][1] for j in adj[i]))))
P("--- overlaps > 2 mm3")
SK={"M3_Insert","M2_Screw_8","M3_SHCS_6","M3_SHCS_8","M3_SHCS_10","M3_SHCS_20","M3_SHCS_40"}
for i in range(n):
    for j,d in adj[i].items():
        if j>i and d<1e-6:
            a,b=leaves[i],leaves[j]
            if {a[1],b[1]}&SK: continue
            try: v=a[2].common(b[2]).Volume
            except Exception: v=-1
            if v>2 or v<0: P("  %-18s %-18s %.1f mm3"%(a[1],b[1],v))
P("END")
