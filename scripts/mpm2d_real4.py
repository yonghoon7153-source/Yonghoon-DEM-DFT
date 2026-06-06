#!/usr/bin/env python3
"""2D MPM mirror of input_real_4.liggghts (6mAh, SE=0.5um, 12:4:1) — true plastic.

Mirrors the LIGGGHTS real_9 setup as closely as MPM allows:
  • 3 phases AM_P:AM_S:SE = 6:2:0.5 um (size ratio 12:4:1, needs fine grid/GPU)
  • composition AM:SE = 81.6:18.4, P:S = 7:3  → area fractions (rho 4.8/2.0):
        AM_P 45.4% / AM_S 19.5% / SE 35.1% of solid
  • AM rigid (E=140 GPa, nu 0.25); SE TRUE-PLASTIC (E=24 GPa, nu 0.30, sigma_y
    0.30 GPa, von Mises J2).  [the script's E_SE=1.35 is the elastic-softened
    DEM proxy; here we use real LPSCl modulus + yield so SE actually flows]
  • densities rho_AM=4.8, rho_SE=2.0  (per-particle mass)
  • process: random initial packing (~settled state) → rigid wall compresses
    (oedometer) → porosity measured.  Snapshots + porosity curve saved.

GPU:  python3 mpm2d_real4.py 320 gpu   (CPU fallback: ... 96 cpu)
"""
import sys
import numpy as np
import taichi as ti

ARCH = sys.argv[2] if len(sys.argv) > 2 else 'gpu'
ti.init(arch=getattr(ti, ARCH), default_fp=ti.f32, random_seed=9)

n_grid = int(sys.argv[1]) if len(sys.argv) > 1 else 512
dx = 1.0/n_grid; inv_dx = float(n_grid)
dt = 8.0e-5
p_vol = (dx*0.5)**2

# ── materials (real LPSCl plastic, NCM rigid) ──
def lame(E, nu): return E/(2*(1+nu)), E*nu/((1+nu)*(1-2*nu))
MU_AM, LA_AM = lame(140.0, 0.25)
MU_SE, LA_SE = lame(24.0, 0.30)       # real LPSCl modulus (NOT softened 1.35)
YIELD_SE = 0.30                        # sigma_y ~ 0.30 GPa → yields ~1.3% strain
YIELD_AM = 1.0e4                       # NCM ~rigid
RHO_AM, RHO_SE = 4.8, 2.0

# ── geometry (50um RVE → box; 1um = SCALE) ──
SCALE = 0.0083
R_AMP, R_AMS, R_SE = 6*SCALE, 2*SCALE, 0.5*SCALE     # 12:4:1 (real_4, SE=0.5um)
# composition: AM:SE 81.6:18.4 wt, P:S 7:3, rho 4.8/2.0 → area fractions
_vam = (0.816/RHO_AM)/((0.816/RHO_AM)+(0.184/RHO_SE))
fAP, fAS, fSE = 0.7*_vam, 0.3*_vam, 1-_vam            # ~0.454 / 0.195 / 0.351
FLOOR = 0.08; SW_L, SW_R = 0.10, 0.90; WIDTH = SW_R-SW_L
WALL0 = 0.70; WALL_MIN = 0.16; WALL_V = 0.30
INIT_SOLID = 0.46                                     # random-packed (settled) state

MAXP = 4_000_000
x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
C = ti.Matrix.field(2,2, ti.f32, MAXP); F = ti.Matrix.field(2,2, ti.f32, MAXP)
mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP)
yld_p = ti.field(ti.f32, MAXP); m_p = ti.field(ti.f32, MAXP); ph_p = ti.field(ti.i32, MAXP)
grid_v = ti.Vector.field(2, ti.f32, (n_grid,n_grid)); grid_m = ti.field(ti.f32, (n_grid,n_grid))
wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())


def build(rng):
    fill_h = WALL0-0.02; box = WIDTH*(fill_h-FLOOR); target = INIT_SOLID*box
    placed = []; cell = R_AMP*1.05; H = {}
    def clash(cx, cy, r):
        ci, cj = int(cx/cell), int(cy/cell)
        for di in (-2,-1,0,1,2):
            for dj in (-2,-1,0,1,2):
                for (px,py,pr) in H.get((ci+di,cj+dj),[]):
                    if (cx-px)**2+(cy-py)**2 < (r+pr+0.0015)**2: return True
        return False
    def add(cx, cy, r, ph):
        placed.append((cx,cy,r,ph)); H.setdefault((int(cx/cell),int(cy/cell)),[]).append((cx,cy,r))
    plan = [(R_AMP,fAP,0),(R_AMS,fAS,1),(R_SE,fSE,2)]   # ph 0=AM_P 1=AM_S 2=SE
    for (r,frac,ph) in plan:
        goal = frac*target; acc = 0.0; t = 0
        while acc < goal and t < 500000:
            t += 1
            cx = rng.uniform(SW_L+r, SW_R-r); cy = rng.uniform(FLOOR+r, fill_h-r)
            if not clash(cx,cy,r): add(cx,cy,r,ph); acc += np.pi*r*r
    xs=[]; mu=[]; la=[]; yl=[]; ms=[]; ph=[]
    PARM = {0:(MU_AM,LA_AM,YIELD_AM,RHO_AM), 1:(MU_AM,LA_AM,YIELD_AM,RHO_AM),
            2:(MU_SE,LA_SE,YIELD_SE,RHO_SE)}
    for (cx,cy,r,phase) in placed:
        mm,ll,yy,rho = PARM[phase]; k = int(r/(dx*0.5))+1
        for a in range(-k,k+1):
            for b in range(-k,k+1):
                px,py = cx+a*dx*0.5, cy+b*dx*0.5
                if (px-cx)**2+(py-cy)**2 <= r*r:
                    xs.append((px,py)); mu.append(mm); la.append(ll); yl.append(yy)
                    ms.append(p_vol*rho); ph.append(phase)
    return (np.array(xs,np.float32), np.array(mu,np.float32), np.array(la,np.float32),
            np.array(yl,np.float32), np.array(ms,np.float32), np.array(ph,np.int32))


@ti.kernel
def load(xy: ti.types.ndarray(), mu: ti.types.ndarray(), la: ti.types.ndarray(),
         yl: ti.types.ndarray(), ms: ti.types.ndarray(), ph: ti.types.ndarray(), n: ti.i32):
    N[None] = n
    for p in range(n):
        x[p]=ti.Vector([xy[p,0],xy[p,1]]); v[p]=ti.Vector([0.0,0.0])
        C[p]=ti.Matrix.zero(ti.f32,2,2); F[p]=ti.Matrix.identity(ti.f32,2)
        mu_p[p]=mu[p]; la_p[p]=la[p]; yld_p[p]=yl[p]; m_p[p]=ms[p]; ph_p[p]=ph[p]


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
        st=(-dt*p_vol*4*inv_dx*inv_dx)*st; aff=st+m_p[p]*C[p]
        for a,b in ti.static(ti.ndrange(3,3)):
            off=ti.Vector([a,b]); dpos=(off.cast(ti.f32)-fx)*dx; wt=w[a][0]*w[b][1]
            grid_v[base+off]+=wt*(m_p[p]*v[p]+aff@dpos); grid_m[base+off]+=wt*m_p[p]
    for I in ti.grouped(grid_m):
        if grid_m[I]>0:
            grid_v[I]/=grid_m[I]; i,j=I[0],I[1]
            if j*dx<FLOOR and grid_v[I][1]<0: grid_v[I][1]=0.0
            if j*dx>wall_y[None]: grid_v[I][1]=ti.min(grid_v[I][1],-WALL_V)
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
        dg=dn-yld_p[p]/(2*mu_p[p])
        if dg>0:
            m0=(d0-dg*d0/dn)+0.5*tr; m1=(d1-dg*d1/dn)+0.5*tr
            F[p]=U@ti.Matrix([[ti.exp(m0),0.0],[0.0,ti.exp(m1)]])@V.transpose()
        x[p]+=dt*v[p]


def main():
    rng = np.random.default_rng(9)
    xy,mu,la,yl,ms,ph = build(rng); n = len(xy)
    nap=int((ph==0).sum()); nas=int((ph==1).sum()); nse=int((ph==2).sum())
    print(f"n_grid={n_grid} arch={ARCH}  material_pts={n}  "
          f"area: AM_P {fAP*100:.1f}% AM_S {fAS*100:.1f}% SE {fSE*100:.1f}%")
    load(xy,mu,la,yl,ms,ph,n)
    solid = n*p_vol; area = WIDTH
    wall_y[None] = WALL0; H0 = WALL0-FLOOR
    snaps=[]; series=[]
    nf=120; sub=45
    for frame in range(nf):
        for _ in range(sub): substep()
        wall_y[None]=max(WALL0-WALL_V*(frame+1)*sub*dt, WALL_MIN); top=wall_y[None]
        por=max(0.0,1.0-solid/(area*(top-FLOOR)))*100
        strain=(H0-(top-FLOOR))/H0*100
        series.append((strain,por))
        if frame in (0, nf//2, nf-1):
            snaps.append((top, x.to_numpy()[:n].copy(), ph))
        if frame%15==0 or frame==nf-1:
            print(f"  frame {frame:3d}  strain={strain:5.1f}%  porosity={por:5.2f}%", flush=True)

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    s=np.array(series)
    fig,ax=plt.subplots(1,4,figsize=(16,4))
    col={0:'#555555',1:'#9a9a9a',2:'#f6c623'}
    for k,(top,xyp,php) in enumerate(snaps):
        for phase,cc in col.items():
            m=php==phase
            ax[k].scatter(xyp[m,0],xyp[m,1],s=0.4,c=cc)
        ax[k].axhline(FLOOR,color='k',lw=1); ax[k].axhline(top,color='r',lw=1.5)
        ax[k].set_xlim(0.05,0.95); ax[k].set_ylim(0,0.75); ax[k].set_aspect('equal')
        ax[k].set_title(['initial','mid','final'][k],fontsize=10); ax[k].axis('off')
    ax[3].plot(s[:,0],s[:,1],'-o',ms=2.5,color='#2e8b57')
    ax[3].set_xlabel('wall strain (%)'); ax[3].set_ylabel('porosity (%)')
    ax[3].set_title('real_9 2D MPM (true plastic SE)',fontsize=10); ax[3].grid(alpha=0.3)
    plt.tight_layout(); plt.savefig("mpm2d_real4.png",dpi=130)
    print(f"final porosity = {series[-1][1]:.2f}%   saved mpm2d_real4.png")


if __name__=="__main__": main()
