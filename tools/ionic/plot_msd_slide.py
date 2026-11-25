import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d=np.genfromtxt('/home/user/Yonghoon-DEM-DFT/docs/figures/msd_compare/msd_compare_comp1_modelc.csv',delimiter=',',names=True)
t=d['t_ps']
reds={600:'#f4a3a3',800:'#e74c3c',1000:'#a01818'}
blues={600:'#9dc3e6',800:'#2e86de',1000:'#16335c'}
fig,ax=plt.subplots(figsize=(7.6,5.6))
fitmask=(t>=20)&(t<=90)
def D_from(slope): return slope/6*1e-4  # Å²/ps -> cm²/s
for T in (600,800,1000):
    for tag,col,lab in [('comp1',reds[T],'LPSCl'),('modelc',blues[T],'LPSCl$_{1.6}$')]:
        y=d[f'{tag}_{T}K']
        ax.plot(t,y,color=col,lw=1.6,label=f'{lab} {T}K')
        p=np.polyfit(t[fitmask],y[fitmask],1)
        ax.plot(t,np.polyval(p,t),color=col,lw=0.9,ls='--',alpha=0.7)
ax.set_xlim(0,100); ax.set_ylim(0,None)
ax.set_xlabel('time (ps)',fontsize=12); ax.set_ylabel('Li MSD  ⟨|r(t)−r(0)|²⟩  (Å²)',fontsize=12)
ax.set_title('Li mean-squared displacement (AIMD-MLIP, NVT)\nlinear (diffusive) slope = 6D  →  Arrhenius (next slide)',fontsize=12)
ax.axvspan(20,90,color='0.93',zorder=0)
ax.text(0.97,0.40,'$\\langle r^2\\rangle = 6Dt$\n(Einstein)\n\nLPSCl$_{1.6}$ (blue)\nsteeper → higher D\nat every T',transform=ax.transAxes,ha='right',va='center',fontsize=9.5,
        bbox=dict(fc='#fff8e1',ec='#ccc'))
ax.legend(fontsize=8,ncol=3,loc='upper left')
plt.tight_layout(); plt.savefig('/tmp/msd_slide.png',dpi=200,bbox_inches='tight'); print('ok')
