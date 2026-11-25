#!/usr/bin/env python3
"""Clean publication ELF map — pure field, NO axes/text/markers/colorbar.
High-res, blue->red ELF colormap. Plane = P + 2 bonded atoms (motif auto-detect).
Usage:
  python3 plot_elf_clean.py --cube nd_ELF.cube --motif PS4 --out a.png
  python3 plot_elf_clean.py --cube nd_ELF.cube --motif PS2O2 --out b.png
  python3 plot_elf_clean.py --cube X.cube --atoms 24 29 34 --out c.png  # P A B (1-based)
"""
import argparse, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.colors as mcolors
from scipy.ndimage import map_coordinates
BOHR=0.5291772108
PT={3:"Li",7:"N",8:"O",15:"P",16:"S",17:"Cl",60:"Nd"}
def read_cube(path):
    L=open(path).read().splitlines(); nat=int(L[2].split()[0])
    origin=np.array([float(x) for x in L[2].split()[1:4]])*BOHR
    gn,vox=[],[]
    for i in range(3):
        p=L[3+i].split(); gn.append(int(p[0])); vox.append([float(x) for x in p[1:4]])
    gn=np.array(gn); cell=np.array(vox)*BOHR*gn[:,None]
    atoms=[]
    for i in range(nat):
        p=L[6+i].split(); atoms.append((PT.get(int(p[0]),str(p[0])),np.array([float(x) for x in p[2:5]])*BOHR))
    data=np.array(" ".join(L[6+nat:]).split(),float).reshape(*gn)
    return data,origin,cell,gn,atoms
def elf_cmap():
    return mcolors.LinearSegmentedColormap.from_list("ELF",
        ["#08306b","#08519c","#2171b5","#6baed6","#41ab5d","#fee08b","#fdae61","#d73027","#a50026"])
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cube",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--motif",choices=["PS4","PS2O2","PS3O"],default=None)
    ap.add_argument("--atoms",type=int,nargs=3,default=None)
    ap.add_argument("--half",type=float,default=4.0); ap.add_argument("--n",type=int,default=600)
    ap.add_argument("--dpi",type=int,default=600)
    a=ap.parse_args()
    data,origin,cell,gn,atoms=read_cube(a.cube)
    cinv=np.linalg.inv(cell); syms=[x[0] for x in atoms]; pos=np.array([x[1] for x in atoms])
    cell_invT=np.linalg.inv(cell.T)
    def mic(d): f=cell_invT@d; f-=np.round(f); return cell.T@f
    # choose plane
    if a.atoms:
        iP,iA,iB=[k-1 for k in a.atoms]
    else:
        # neighbor composition of each P
        chosen=None
        for k in [i for i in range(len(atoms)) if syms[i]=="P"]:
            nO=[j for j in range(len(atoms)) if syms[j]=="O" and np.linalg.norm(mic(pos[j]-pos[k]))<1.9]
            nS=[j for j in range(len(atoms)) if syms[j]=="S" and np.linalg.norm(mic(pos[j]-pos[k]))<2.3]
            if a.motif=="PS4" and len(nO)==0 and len(nS)>=2: chosen=(k,nS[0],nS[1]); break
            if a.motif=="PS2O2" and len(nO)==2: chosen=(k,nO[0],nO[1]); break
            if a.motif=="PS3O" and len(nO)==1 and len(nS)>=1: chosen=(k,nO[0],nS[0]); break
        if not chosen: raise SystemExit(f"no {a.motif} P found")
        iP,iA,iB=chosen
    p0=pos[iP]; A=p0+mic(pos[iA]-p0); B=p0+mic(pos[iB]-p0)
    print(f"plane: P=atom{iP+1}({syms[iP]}) A=atom{iA+1}({syms[iA]},{np.linalg.norm(A-p0):.2f}A) B=atom{iB+1}({syms[iB]},{np.linalg.norm(B-p0):.2f}A)")
    e1=(A-p0)/np.linalg.norm(A-p0); nrm=np.cross(e1,B-p0); nrm/=np.linalg.norm(nrm); e2=np.cross(nrm,e1)
    H,N=a.half,a.n; us=np.linspace(-H,H,N)
    U,V=np.meshgrid(us,us); R=p0[None,:]+U.ravel()[:,None]*e1+V.ravel()[:,None]*e2
    F=((R-origin)@cinv)%1.0; G=(F*gn).T   # 3 x Npts
    img=map_coordinates(data,G,order=1,mode="grid-wrap").reshape(N,N)
    fig=plt.figure(figsize=(6,6)); ax=fig.add_axes([0,0,1,1]); ax.axis("off")
    ax.imshow(img,origin="lower",extent=[-H,H,-H,H],cmap=elf_cmap(),vmin=0,vmax=1,
              aspect="equal",interpolation="bilinear")
    fig.savefig(a.out,dpi=a.dpi); print(f"-> {a.out} ({6*a.dpi}px)")
if __name__=="__main__": main()
