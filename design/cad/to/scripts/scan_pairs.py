"""Step 2: pairwise overlap volumes using a process pool. usage: scan_pairs.py outdir [min_mm3]"""
import sys, os, json, itertools, time
from multiprocessing import Pool
import FreeCAD as App, Part
outdir = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
idx = json.load(open(os.path.join(outdir, "index.json")))
_cache = {}
def load(n):
    if n not in _cache:
        s = Part.Shape(); s.read(idx[n]["file"]); _cache[n] = s
    return _cache[n]
def work(pair):
    a, b = pair
    try:
        sa, sb = load(a), load(b)
        d = sa.distToShape(sb)[0]
        if d > 1e-6:
            return (a, b, 0.0, d)
        v = sa.common(sb).Volume
        return (a, b, v, 0.0)
    except Exception as e:
        return (a, b, -1.0, str(e)[:60])
def bbo(p, q, tol=0.0):
    return all(p[i] <= q[i + 3] + tol and q[i] <= p[i + 3] + tol for i in range(3))
if __name__ == "__main__":
    names = sorted(idx)
    pairs = [(a, b) for a, b in itertools.combinations(names, 2) if bbo(idx[a]["bb"], idx[b]["bb"])]
    print("parts", len(names), "bbox-overlapping pairs", len(pairs), flush=True)
    t = time.time(); out = []
    with Pool(int(os.environ.get("NPROC", "8"))) as p:
        for k, r in enumerate(p.imap_unordered(work, pairs, chunksize=1)):
            out.append(r)
            if k % 100 == 0: print(k, round(time.time() - t), flush=True)
    json.dump(out, open(os.path.join(outdir, "pairs.json"), "w"))
    hit = sorted([r for r in out if r[2] > thr], key=lambda r: -r[2])
    err = [r for r in out if r[2] < 0]
    print("pairs >%.2f mm3: %d ; errors %d ; total pairs %d ; time %ds" % (thr, len(hit), len(err), len(out), time.time() - t))
    for r in hit: print("%-28s %-28s %8.2f" % (r[0], r[1], r[2]))
    for r in err[:20]: print("ERR", r)
