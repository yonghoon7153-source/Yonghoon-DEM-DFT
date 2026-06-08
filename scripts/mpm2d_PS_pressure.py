#!/usr/bin/env python3
"""(가) Resolved-grain 2D MPM — CHAMPION plastic-SE compaction (E=1.53/σ_y=0.15).

The chosen LPSCl-compaction line (vs (나) homogenized cap_compaction_heckel.py).
Real resolved grains (AM_P 12 : AM_S 4 : SE 1) compressed by a servo wall;
SE is softened-J2 plastic + work-hardening, AM rigid.  Reproduces the SEM
morphology (core-preserved + boundary-flattening) and pure-SE 300→~11% porosity.

Material model (3 layers — see CLAUDE.md "MPM cap/champion" timelog):
  • E_SE = 1.53 GPa, σ_y = 0.15 GPa  (champion; softened-J2, HELD/유보).
  • HARD_SE = 10  work-hardening (yield grows with accumulated plastic strain).
  • von-Mises J2 (+0.5·tr in the return map → STILL isochoric, NO cap).
  • over-compression blocked by wall_floor = top_full+0.002 (geometric full-pack
    clamp, NOT a constitutive cap).
Readout: porosity at P_READ pressures where Pcur=mean(prs) crosses the target
  (COMMON Pmean — resolution-biased; for the resolution-INVARIANT dip use the
  self-normalised readout in scripts/mpm2d_jamming.py instead).
  NOTE: out.get default is float('nan') (not 0.0) so an unreached pressure is
  honestly NaN, not a fake 0%.

Run (uma GPU):  python3 mpm2d_PS_pressure.py [n_grid=320] [arch=gpu] [NSEED=3] [AM_STEP=10]
Out: mpm2d_PS_pressure.png / .npy , partial_<p>_<s>.npy

CANONICAL COPY of the uma ~/work/mpm/ script, committed for safety + reference.
"""
import sys
import numpy as np
import taichi as ti

ARCH   = sys.argv[2] if len(sys.argv) > 2 else 'gpu'
n_grid = int(sys.argv[1]) if len(sys.argv) > 1 else 320
NSEED  = int(sys.argv[3]) if len(sys.argv) > 3 else 3
AM_STEP= int(sys.argv[4]) if len(sys.argv) > 4 else 10
ti.init(arch=getattr(ti, ARCH), default_fp=ti.f32)

dx=1.0/n_grid; inv_dx=float(n_grid); dt=8.0e-5*320.0/n_grid; p_vol=(dx*0.5)**2
def lame(E,nu): return E/(2*(1+nu)), E*nu/((1+nu)*(1-2*nu))
MU_SE,LA_SE=lame(1.53,0.30); MU_AM,LA_AM=lame(140.0,0.25)
YIELD_SE=0.15; YIELD_AM=1.0e4; RHO_AM,RHO_SE=4.8,2.0
HARD_SE=10.0
FLOOR=0.08; SW_L,SW_R=0.08,0.92; WIDTH=SW_R-SW_L
WALL0=0.66; WALL_MIN=0.05; WALL_V=0.18
P_READ=[0.30,0.45,0.60]; P_STOP=0.70
R_AMP,R_AMS,R_SE=0.072,0.024,0.006; INIT_SOLID=0.50
PS_LIST=[(7,3)]

MAXP=2_000_000
x=ti.Vector.field(2,ti.f32,MAXP); v=ti.Vector.field(2,ti.f32,MAXP)
C=ti.Matrix.field(2,2,ti.f32,MAXP); F=ti.Matrix.field(2,2,ti.f32,MAXP)
mu_p=ti.field(ti.f32,MAXP); la_p=ti.field(ti.f32,MAXP); yld_p=ti.field(ti.f32,MAXP)
m_p=ti.field(ti.f32,MAXP); prs=ti.field(ti.f32,MAXP); epl=ti.field(ti.f32,MAXP)
grid_v=ti.Vector.field(2,ti.f32,(n_grid,n_grid)); grid_m=ti.field(ti.f32,(n_grid,n_grid))
wall_y=ti.field(ti.f32,()); N=ti.field(ti.i32,()); wimp=ti.field(ti.f32,())

def fracs(am_wt,pp,ss):
    w=am_wt/100.0
    if w<=0: vam=0.0
    elif w>=1: vam=1.0
    else:
        a=w/RHO_AM; b=(1-w)/RHO_SE; vam=a/(a+b)
    tot=pp+ss; fp=(pp/tot)*vam if tot>0 else 0.0; fs=(ss/tot)*vam if tot>0 else 0.0
    return fp,fs,1.0-vam

def build(am,pp,ss,rng):
    fAP,fAS,fSE=fracs(am,pp,ss)
    fill_h=WALL0-0.02; box=WIDTH*(fill_h-FLOOR); target=INIT_SOLID*box
    placed=[]; cell=R_AMP*1.05; H={}
    def clash(cx,cy,r):
        ci,cj=int(cx/cell),int(cy/cell)
        for di in(-2,-1,0,1,2):
            for dj in(-2,-1,0,1,2):
                for(px,py,pr)in H.get((ci+di,cj+dj),[]):
                    if(cx-px)**2+(cy-py)**2<(r+pr+0.0015)**2:return True
        return False
    def add(cx,cy,r,mu,la,yld,rho):
        placed.append((cx,cy,r,mu,la,yld,rho)); H.setdefault((int(cx/cell),int(cy/cell)),[]).append((cx,cy,r))
    plan=[(R_AMP,fAP,MU_AM,LA_AM,YIELD_AM,RHO_AM),(R_AMS,fAS,MU_AM,LA_AM,YIELD_AM,RHO_AM),
          (R_SE,fSE,MU_SE,LA_SE,YIELD_SE,RHO_SE)]
    for(r,frac,mu,la,yld,rho)in plan:
        if frac<=1e-6:continue
        goal=frac*target; acc=0.0; t=0
        while acc<goal and t<800000:
            t+=1; cx=rng.uniform(SW_L+r,SW_R-r); cy=rng.uniform(FLOOR+r,fill_h-r)
            if not clash(cx,cy,r): add(cx,cy,r,mu,la,yld,rho); acc+=np.pi*r*r
    xs=[];mu=[];la=[];yl=[];ms=[]
    for(cx,cy,r,mm,ll,yy,rho)in placed:
        k=int(r/(dx*0.5))+1
        for a in range(-k,k+1):
            for b in range(-k,k+1):
                px,py=cx+a*dx*0.5,cy+b*dx*0.5
                if(px-cx)**2+(py-cy)**2<=r*r:
                    xs.append((px,py)); mu.append(mm); la.append(ll); yl.append(yy); ms.append(p_vol*rho)
    return(np.array(xs,np.float32),np.array(mu,np.float32),np.array(la,np.float32),
           np.array(yl,np.float32),np.array(ms,np.float32))

@ti.kernel
def load(xy:ti.types.ndarray(),mu:ti.types.ndarray(),la:ti.types.ndarray(),
         yl:ti.types.ndarray(),ms:ti.types.ndarray(),n:ti.i32):
    N[None]=n
    for p in range(n):
        x[p]=ti.Vector([xy[p,0],xy[p,1]]); v[p]=ti.Vector([0.0,0.0])
        C[p]=ti.Matrix.zero(ti.f32,2,2); F[p]=ti.Matrix.identity(ti.f32,2)
        mu_p[p]=mu[p]; la_p[p]=la[p]; yld_p[p]=yl[p]; m_p[p]=ms[p]; epl[p]=0.0

@ti.kernel
def substep():
    for I in ti.grouped(grid_m):
        grid_v[I]=ti.Vector.zero(ti.f32,2); grid_m[I]=0.0
    for p in range(N[None]):
        base=(x[p]*inv_dx-0.5).cast(int); fx=x[p]*inv_dx-base.cast(ti.f32)
        w=[0.5*(1.5-fx)**2,0.75-(fx-1.0)**2,0.5*(fx-0.5)**2]
        U,sig,V=ti.svd(F[p]); J=sig[0,0]*sig[1,1]
        st=(2*mu_p[p]*(F[p]-U@V.transpose())@F[p].transpose()
            +ti.Matrix.identity(ti.f32,2)*la_p[p]*J*(J-1))
        prs[p]=-0.5*(st[0,0]+st[1,1])/ti.max(J,1e-4)
        st=(-dt*p_vol*4*inv_dx*inv_dx)*st; aff=st+m_p[p]*C[p]
        for a,b in ti.static(ti.ndrange(3,3)):
            off=ti.Vector([a,b]); dpos=(off.cast(ti.f32)-fx)*dx; wt=w[a][0]*w[b][1]
            grid_v[base+off]+=wt*(m_p[p]*v[p]+aff@dpos); grid_m[base+off]+=wt*m_p[p]
    for I in ti.grouped(grid_m):
        if grid_m[I]>0:
            grid_v[I]/=grid_m[I]; i,j=I[0],I[1]
            if j*dx<FLOOR and grid_v[I][1]<0: grid_v[I][1]=0.0
            if j*dx>wall_y[None]:
                _vb=grid_v[I][1]
                if _vb>-WALL_V: wimp[None]+=grid_m[I]*(_vb+WALL_V)
                grid_v[I][1]=ti.min(grid_v[I][1],-WALL_V)
            if i*dx<SW_L and grid_v[I][0]<0: grid_v[I][0]=0.0
            if i*dx>SW_R and grid_v[I][0]>0: grid_v[I][0]=0.0
    for p in range(N[None]):
        base=(x[p]*inv_dx-0.5).cast(int); fx=x[p]*inv_dx-base.cast(ti.f32)
        w=[0.5*(1.5-fx)**2,0.75-(fx-1.0)**2,0.5*(fx-0.5)**2]
        nv=ti.Vector.zero(ti.f32,2); nc=ti.Matrix.zero(ti.f32,2,2)
        for a,b in ti.static(ti.ndrange(3,3)):
            off=ti.Vector([a,b]); dpos=off.cast(ti.f32)-fx; wt=w[a][0]*w[b][1]; gv=grid_v[base+off]
            nv+=wt*gv; nc+=4*inv_dx*wt*gv.outer_product(dpos)
        v[p]=nv; C[p]=nc; F[p]=(ti.Matrix.identity(ti.f32,2)+dt*nc)@F[p]
        U,sig,V=ti.svd(F[p])
        e0=ti.log(ti.max(sig[0,0],1e-4)); e1=ti.log(ti.max(sig[1,1],1e-4))
        tr=e0+e1; d0=e0-0.5*tr; d1=e1-0.5*tr; dn=ti.sqrt(d0*d0+d1*d1)+1e-9
        dg=dn-(yld_p[p]*(1.0+HARD_SE*epl[p]))/(2*mu_p[p])
        if dg>0:
            epl[p]+=dg
            m0=(d0-dg*d0/dn)+0.5*tr; m1=(d1-dg*d1/dn)+0.5*tr
            F[p]=U@ti.Matrix([[ti.exp(m0),0.0],[0.0,ti.exp(m1)]])@V.transpose()
        x[p]+=dt*v[p]

def run_once(am,pp,ss,seed):
    rng=np.random.default_rng(seed)
    xy,mu,la,yl,ms=build(am,pp,ss,rng); n=len(xy); sa=n*p_vol
    load(xy,mu,la,yl,ms,n); wall_y[None]=WALL0
    top_full=FLOOR+sa/WIDTH                 # POR->0 geometric limit
    wall_floor=top_full+0.002               # never ram below full-pack (over-compression 차단)
    targets=sorted(P_READ); out={}; idx=0
    for fr in range(int(8000*n_grid/320)):
        wimp[None]=0.0
        for _ in range(25): substep()
        Pwall=wimp[None]/(25.0*dt)/WIDTH
        Pcur=float(np.mean(prs.to_numpy()[:n])); top=wall_y[None]
        por=max(0.0,1.0-sa/(WIDTH*(top-FLOOR)))*100
        if am==0 and pp==7 and fr%150==0: print(f'  [dbg n={n_grid}] fr={fr} por={por:5.1f} Pmean={Pcur:.4f} Pwall={Pwall:.4f}',flush=True)
        while idx<len(targets) and Pcur>=targets[idx]:
            out[targets[idx]]=por; idx+=1
        if idx>=len(targets) or Pcur>=P_STOP or top<=wall_floor+1e-4: break
        if Pcur<targets[idx] and top>wall_floor:
            wall_y[None]=max(top-WALL_V*25*dt, wall_floor)
    return [out.get(pt,float("nan")) for pt in P_READ]   # unreached P -> NaN (not fake 0%)

def main():
    comps=list(range(0,101,AM_STEP)); results={}; results_std={}
    for (pp,ss) in PS_LIST:
        arr=np.zeros((len(comps),len(P_READ))); arr_std=np.zeros((len(comps),len(P_READ)))
        for ci,am in enumerate(comps):
            vals=np.array([run_once(am,pp,ss,7000+am*7+s) for s in range(NSEED)])
            arr[ci]=np.nanmean(vals,axis=0); arr_std[ci]=np.nanstd(vals,axis=0)
            print(f"  P:S={pp}:{ss} AM{am:3d}%  300={arr[ci,0]:.1f} 450={arr[ci,1]:.1f} 600={arr[ci,2]:.1f}",flush=True)
        results[(pp,ss)]=arr; results_std[(pp,ss)]=arr_std; np.save(f'partial_{pp}_{ss}.npy',arr); print(f'--- P:S={pp}:{ss} done, saved partial ---',flush=True)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,len(PS_LIST),figsize=(4*len(PS_LIST),4),sharey=True)
    axes=np.atleast_1d(axes)
    cols=['#1f77b4','#2ca02c','#d62728']
    for k,(pp,ss) in enumerate(PS_LIST):
        ax=axes[k]; arr=results[(pp,ss)]
        for pi,pt in enumerate(P_READ):
            ax.errorbar(comps,arr[:,pi],yerr=results_std[(pp,ss)][:,pi],fmt='-o',ms=4,capsize=3,color=cols[pi],label=f'{int(pt*1000)} MPa')
        ax.set_title(f'P:S = {pp}:{ss}',fontsize=10); ax.set_xlabel('AM wt%'); ax.grid(alpha=0.3)
        if k==0: ax.set_ylabel('porosity (%)'); ax.legend(fontsize=8)
    fig.suptitle(f'2D MPM plastic SE — porosity vs AM% by P:S and pressure (n_grid={n_grid}, {NSEED}-seed)',fontsize=11)
    plt.tight_layout(); plt.savefig("mpm2d_PS_pressure.png",dpi=120); print("saved mpm2d_PS_pressure.png")
    np.save("mpm2d_PS_pressure.npy",{'comps':comps,'P_READ':P_READ,'results':{f'{p}:{s}':results[(p,s)] for (p,s) in PS_LIST},'results_std':{f'{p}:{s}':results_std[(p,s)] for (p,s) in PS_LIST}})

if __name__=="__main__": main()
