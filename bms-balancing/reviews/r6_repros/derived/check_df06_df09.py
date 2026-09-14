import csv, json
def rows(p): return list(csv.DictReader(l for l in open(p) if not l.startswith("#")))
v1=rows("out/matrix_300_0009.csv"); v2=rows("out/matrix_300_0009_v2.csv")
objcol=[c for c in v1[0] if "obj" in c.lower()]; print("obj cols v1:",objcol,"| v2:",[c for c in v2[0] if "obj" in c.lower()])
key=lambda r:(r["half_cell"],r["si"],float(r["w_dqdv"]))
d1={key(r):r for r in v1}; d2={key(r):r for r in v2}; print("rows v1/v2:",len(d1),len(d2),"common:",len(set(d1)&set(d2)))
oc=objcol[0]
for tol in (0.0,1e-12,1e-10,1e-9,1e-8,1e-6):
    worse=better=same=0; worse_w=[]
    for k in d1:
        a,b=float(d1[k][oc]),float(d2[k][oc]); rel=(b-a)/abs(a)
        if rel>tol: worse+=1; worse_w.append(k[2])
        elif rel<-tol: better+=1
        else: same+=1
    print(f"tol {tol:g}: worse {worse} better {better} same {same}; worse all w=1? {all(w==1.0 for w in worse_w)} (w values {sorted(set(worse_w))})")
# max worsening
mx=max(((float(d2[k][oc])-float(d1[k][oc]))/abs(float(d1[k][oc])),k) for k in d1); print("max rel worsening",mx)
# DF-09: best_p modes vs GITT/Li/w0 rows
j=json.load(open("out/degeneracy_300_0009_Li_v2.json")); bm=j["best_modes_percent"]
cols=[c for c in v2[0] if c.startswith(("LAM","LLI"))]; print("mode cols:",cols)
for name,d in (("v1",d1),("v2",d2)):
    r=d[("GITT","Li",0.0)]
    print(name, {c:(float(r[c]), float(r[c])-bm[c.split('_percent')[0].replace('_pct','')] if c.split('_percent')[0].replace('_pct','') in bm else None) for c in cols})
