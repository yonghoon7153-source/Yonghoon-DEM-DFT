import numpy as np
B=0.529177210903
# --- parse cube ---
f=open("/tmp/ndelf/nd_ELF.cube"); f.readline(); f.readline()
h=f.readline().split(); nat=int(h[0]); origin=np.array([float(x) for x in h[1:4]])
gv=[]; nv=[]
for _ in range(3):
    p=f.readline().split(); nv.append(int(p[0])); gv.append([float(x) for x in p[1:4]])
nv=np.array(nv); gv=np.array(gv); cell=(gv.T*nv).T
Z=[]; xyz=[]
for _ in range(nat):
    p=f.readline().split(); Z.append(int(float(p[0]))); xyz.append([float(x) for x in p[2:5]])
Z=np.array(Z); xyz=np.array(xyz)
data=np.fromstring(f.read(),sep=' ').reshape(nv[0],nv[1],nv[2])
M=gv.T; Minv=np.linalg.inv(M)
def elf_at(r):  # trilinear, PBC
    fijk=Minv@(r-origin); i0=np.floor(fijk).astype(int); d=fijk-i0
    v=0.0
    for dx in (0,1):
        for dy in (0,1):
            for dz in (0,1):
                w=(d[0] if dx else 1-d[0])*(d[1] if dy else 1-d[1])*(d[2] if dz else 1-d[2])
                ii=(i0[0]+dx)%nv[0]; jj=(i0[1]+dy)%nv[1]; kk=(i0[2]+dz)%nv[2]
                v+=w*data[ii,jj,kk]
    return v
shifts=np.array([[i,j,k] for i in(-1,0,1) for j in(-1,0,1) for k in(-1,0,1)])@cell
def mic_image(i,j):  # image of j nearest to i; returns (cart_pos, dist_A)
    cand=xyz[j]+shifts; dd=np.sqrt(((cand-xyz[i])**2).sum(1)); k=dd.argmin()
    return cand[k], dd[k]*B
sym={3:'Li',8:'O',15:'P',16:'S',17:'Cl',60:'Nd'}
idx={e:np.where(Z==z)[0] for z,e in sym.items()}
def line_vals(i,j,n=81,t0=0.0,t1=1.0):
    rj,d=mic_image(i,j); ts=np.linspace(t0,t1,n)
    return np.array([elf_at(xyz[i]+t*(rj-xyz[i])) for t in ts]), d, ts
def bonds(eA,eB,dmax):
    out=[]
    for i in idx[eA]:
        for j in idx[eB]:
            if eA==eB and j<=i: continue
            _,d=mic_image(i,j)
            if 0.3<d<dmax: out.append((i,j,d))
    return out
print("=== COVALENT (midpoint & bonding-max ELF; higher=more shared) ===")
for eA,eB,dmax in [("P","O",2.1),("P","S",2.4)]:
    bs=bonds(eA,eB,dmax); mids=[]; maxs=[]
    for i,j,d in bs:
        vals,dd,ts=line_vals(i,j)
        mids.append(elf_at((xyz[i]+mic_image(i,j)[0])/2))
        m=(ts>=0.3)&(ts<=0.7); maxs.append(vals[m].max())
    if bs:
        print(f"  {eA}-{eB}: n={len(bs)}  d={np.mean([b[2] for b in bs]):.2f}A  "
              f"midpoint ELF={np.mean(mids):.3f}±{np.std(mids):.3f}  "
              f"bonding-max={np.mean(maxs):.3f}±{np.std(maxs):.3f}")
print("=== IONIC (depletion-floor = min ELF along bond; lower=more ionic) ===")
for eA,eB,dmax in [("Li","O",2.6),("Li","Cl",3.0),("Li","S",3.0),("Nd","O",2.8),("Nd","S",3.3)]:
    bs=bonds(eA,eB,dmax); mins=[]
    for i,j,d in bs:
        vals,dd,ts=line_vals(i,j); m=(ts>=0.2)&(ts<=0.8); mins.append(vals[m].min())
    if bs:
        print(f"  {eA}-{eB}: n={len(bs)}  d={np.mean([b[2] for b in bs]):.2f}A  "
              f"min ELF={np.mean(mins):.3f}±{np.std(mins):.3f}")
# profile plot: representative P-O vs P-S
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
po=bonds("P","O",2.1)[0]; ps=bonds("P","S",2.4)[0]
vpo,dpo,ts=line_vals(*po[:2]); vps,dps,_=line_vals(*ps[:2])
fig,ax=plt.subplots(figsize=(7,4.5))
ax.plot(ts*dpo,vpo,'-',color='#d9534f',lw=2,label=f"P-O ({dpo:.2f} Å)")
ax.plot(ts*dps,vps,'-',color='#2ca25f',lw=2,label=f"P-S ({dps:.2f} Å)")
ax.set_xlabel("distance from P (Å)"); ax.set_ylabel("ELF"); ax.set_ylim(0,1.05)
ax.axhline(0.5,ls=':',color='0.6',lw=0.8); ax.legend(); ax.set_title("ELF along P-O vs P-S bond (Nd-doped)")
fig.tight_layout(); fig.savefig("docs/figures/nd_elf/nd_ELF_PO_vs_PS_profile.png",dpi=160)
print("\nwrote docs/figures/nd_elf/nd_ELF_PO_vs_PS_profile.png")
