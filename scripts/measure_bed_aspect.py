"""침대 종횡비 지표 — 실린더 축(0,0) 기준.  §6 사전등록 정의 그대로."""
import numpy as np, sys, glob, re
def load(p):
    L=open(p).read().split('\n')
    i=[k for k,l in enumerate(L) if l.startswith('ITEM: ATOMS')][0]
    cols=L[i].split()[2:]
    A=np.array([[float(v) for v in l.split()] for l in L[i+1:] if l.strip()])
    return {n:A[:,j] for j,n in enumerate(cols)}, len(A)
def last_frame(d, pref):
    fs=glob.glob(f'{d}/{pref}_*.liggghts')
    key=lambda f:int(re.search(r'_(\d+)\.liggghts$',f).group(1))
    return max(fs,key=key), key(max(fs,key=key))
def metric(d,pref,label):
    f,step=last_frame(d,pref); D,n=load(f)
    x,y,z,r=D['x'],D['y'],D['z'],D['radius']
    rad=np.hypot(x,y)                      # ★ 실린더 축 기준
    R99=np.percentile(rad,99); H=z.max()-z.min()
    Vp=n*(4/3)*np.pi*r.mean()**3
    phi=Vp/(np.pi*R99**2*H)
    print(f'{label:12s} step {step:6d} · n {n:5d}')
    print(f'   R(99%) {R99*1e3:6.2f} mm  ·  H {H*1e3:6.2f} mm  ·  ★ H/R {H/R99:6.3f}')
    print(f'   R/R_통 {R99/0.05:5.3f}  ·  φ(포락) {phi:5.3f}  ·  z [{z.min()*1e3:.2f}, {z.max()*1e3:.2f}]')
    return dict(R=R99,H=H,HR=H/R99,phi=phi,n=n)
S='/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad'
a=metric(f'{S}/run_nocoh/post','noCohesion','noCohesion')
print()
b=metric(f'{S}/run_coh/post','cohesion','cohesion')
print(f'\n★★ 대조  H/R  {a["HR"]:.3f} → {b["HR"]:.3f}  =  ×{b["HR"]/a["HR"]:.2f}')
print(f'         R    {a["R"]*1e3:.2f} → {b["R"]*1e3:.2f} mm  =  ×{b["R"]/a["R"]:.2f}')
print(f'         H    {a["H"]*1e3:.2f} → {b["H"]*1e3:.2f} mm  =  ×{b["H"]/a["H"]:.2f}')
print(f'         φ    {a["phi"]:.3f} → {b["phi"]:.3f}  =  ×{b["phi"]/a["phi"]:.2f}')
