"""Sweep repo structure files for the broken canonical arrangement:
halide (Cl/Br/I) within 2.8 A of S (physical S–X >= ~3.3 A). First frame only, files <= 20 MB."""
import os, sys, warnings, json, time
warnings.filterwarnings("ignore")
import numpy as np
from ase.io import read
root = sys.argv[1]; out = sys.argv[2]
EXT = (".cif", ".vasp", ".xyz", ".extxyz", ".cube", ".xsf")
files = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if not (os.path.join(dp, d).endswith(("/.git", "/litdb/figures", "/node_modules")))]
    for f in fn:
        if f.endswith(EXT) or f.startswith(("POSCAR", "CONTCAR")):
            p = os.path.join(dp, f)
            if os.path.getsize(p) <= 20e6: files.append(p)
res = []; t0 = time.time()
for p in sorted(files):
    rec = {"path": os.path.relpath(p, root)}
    try:
        kw = {}
        if p.endswith((".xyz", ".extxyz")): kw["index"] = 0
        at = read(p, **kw)
        s = np.array(at.get_chemical_symbols())
        hal = np.isin(s, ["Cl", "Br", "I"]); sul = s == "S"
        if not hal.any() or not sul.any(): continue
        pbc = at.cell.rank == 3 and at.pbc.any()
        if not pbc: at.pbc = False
        iS = np.where(sul)[0]; iX = np.where(hal)[0]
        D = at.get_distances(iS[0], iX, mic=pbc)  # warm
        dmin = 9e9; nshort = 0
        for i in iS:
            d = at.get_distances(i, iX, mic=pbc)
            dmin = min(dmin, d.min()); nshort += int((d < 2.8).sum())
        rec.update(n=len(at), pbc=bool(pbc), SX_min=round(float(dmin), 3), n_SX_lt_2p8=nshort)
        if dmin < 2.8: res.append(rec)
    except Exception as e:
        pass
json.dump({"n_files": len(files), "flagged": res, "secs": round(time.time() - t0, 1)}, open(out, "w"), indent=1)
print("files", len(files), "flagged", len(res), "secs", round(time.time() - t0, 1))
