import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def slices(npz, out, zs=None, ys=None, xs=None, axes=("z","y","x"), dz=1.0, title=""):
    d=np.load(npz); xyz=d["xyz"]; E=d["E"]; x=d["x"]; des=d["design"]
    c=xyz[E[:,:4]].mean(axis=1)
    sets=[]
    for ax,vals in zip(("z","y","x"),(zs,ys,xs)):
        if vals is None: continue
        for v in vals: sets.append((ax,v))
    n=len(sets); cols=min(n,4); rows=(n+cols-1)//cols
    fig,axs=plt.subplots(rows,cols,figsize=(3.6*cols,3.4*rows),dpi=100); axs=np.atleast_1d(axs).ravel()
    idx={"x":0,"y":1,"z":2}
    for a,(ax,v) in zip(axs,sets):
        m=abs(c[:,idx[ax]]-v)<dz/2
        o=[i for i in (0,1,2) if i!=idx[ax]]
        col=np.where(x[m],np.where(des[m],0,2),1)
        a.scatter(c[m,o[0]],c[m,o[1]],c=col,s=9,cmap=matplotlib.colors.ListedColormap(["#e8821e","#dddddd","#3a4f85"]),vmin=0,vmax=2,marker="s")
        a.set_aspect("equal"); a.set_title("%s = %.1f  (axes %s,%s)"%(ax,v,"xyz"[o[0]],"xyz"[o[1]]),fontsize=8)
    for a in axs[n:]: a.axis("off")
    fig.suptitle(title+"  orange=optimised solid, blue=kept solid, grey=void",fontsize=9)
    fig.tight_layout(); fig.savefig(out,facecolor="white"); plt.close(fig)
if __name__=="__main__":
    W="../work/clamp/"
    slices(W+"clamp_result.npz","../clamp_F_slices.png",zs=[148,152,156,159,164,170,176,181],ys=[0,5,11,14],xs=[229,233,237.8,242],title="WingClampCap_F BESO slices")
