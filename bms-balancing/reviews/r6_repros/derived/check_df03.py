# DF-03: raw LLI half-width ratios, cylindrical vs pouch, from stored degeneracy JSONs
import json, itertools, statistics as st
def hw(p): j=json.load(open(p)); return j["LLI_percent"]["span"]/2
pouch={s:hw(f"out/degeneracy_{s}_Li{'_v2' if s=='300_0009' else ''}.json") for s in ("100","200","300_0009")}
fix={s:hw(f"out/cells_pouch_fixedhc/degeneracy_{s}_Li.json") for s in ("100","200","300_0009")}
cyl={c:{s:hw(f"out/cells_{c}/degeneracy_{s}_Li.json") for s in ("100","200","300_0009")} for c in ("c168","c171")}
print("pouch",{k:round(v,4) for k,v in pouch.items()}); print("fixedhc",{k:round(v,4) for k,v in fix.items()}); print("cyl",{c:{k:round(v,4) for k,v in d.items()} for c,d in cyl.items()})
P=list(pouch.values())+list(fix.values()); C=[v for d in cyl.values() for v in d.values()]
print(f"pouch(6) [{min(P):.4f},{max(P):.4f}]  cyl(6) [{min(C):.4f},{max(C):.4f}]")
print(f"max/max {max(C)/max(P):.2f}  min/min {min(C)/min(P):.2f}  med/med {st.median(C)/st.median(P):.2f}  min(cyl)/max(pouch) {min(C)/max(P):.2f}  max(cyl)/min(pouch) {max(C)/min(P):.2f}")
pairs=[cyl[c][s]/pouch[s] for c in cyl for s in pouch]; pairs_f=[cyl[c][s]/fix[s] for c in cyl for s in fix]
print(f"same-state pairs vs pouch: {min(pairs):.1f}~{max(pairs):.1f}; vs fixedhc: {min(pairs_f):.1f}~{max(pairs_f):.1f}")
print("all 36 cross ratios: %.1f~%.1f" % (min(c/p for c in C for p in P), max(c/p for c in C for p in P)))
