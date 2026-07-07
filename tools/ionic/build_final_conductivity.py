import numpy as np, csv
kB=8.617333e-5; e=1.602176634e-19; kBJ=1.380649e-23
def fit(D,Ts=(600,800,1000)):
    x=1/(kB*np.array(Ts,float)); y=np.log(np.array(D,float)); s,i=np.polyfit(x,y,1); return -s,np.exp(i)
def sig(n,D,T): return 10.0*(n*1e6)*e*e*(D*1e-4)/(kBJ*T)
S={'b2o3':dict(n=2.381e22,D={600:[0.798e-5,1.304e-5,1.021e-5],800:[1.941e-5,2.735e-5,1.814e-5],1000:[4.614e-5,6.367e-5,4.261e-5]}),
   'modelc':dict(n=2.220e22,D={600:[1.1718e-5,1.2037e-5,0.73508e-5],800:[2.832e-5,3.772e-5,1.932e-5],1000:[5.030e-5,4.621e-5,4.533e-5]})}
for k,d in S.items():
    d['m']={T:np.mean(v) for T,v in d['D'].items()}; d['s']={T:np.std(v) for T,v in d['D'].items()}
    d['Ea'],d['D0']=fit([d['m'][600],d['m'][800],d['m'][1000]])
    d['Eaerr']=np.std([fit([d['D'][600][i],d['D'][800][j],d['D'][1000][l]])[0] for i in range(3) for j in range(3) for l in range(3)])
    d['sig']={T:sig(d['n'],d['m'][T],T) for T in (600,800,1000)}
    d['sigerr']={T:sig(d['n'],d['s'][T],T) for T in (600,800,1000)}
b,m=S['b2o3'],S['modelc']
rat={T:b['sig'][T]/m['sig'][T] for T in (600,800,1000)}
raterr={T:rat[T]*np.hypot(b['s'][T]/b['m'][T],m['s'][T]/m['m'][T])/np.sqrt(3) for T in (600,800,1000)}
print(f"b2o3 Ea={b['Ea']:.3f}±{b['Eaerr']:.3f} D0={b['D0']:.3e} | modelc Ea={m['Ea']:.3f}±{m['Eaerr']:.3f} D0={m['D0']:.3e}")
print("sigma:",{T:(round(b['sig'][T]),round(m['sig'][T]),f"{rat[T]:.2f}±{raterr[T]:.2f}") for T in (600,800,1000)})

# ---- FINAL CSV (supersedes the single-seed table in-place) ----
with open("b2o3_vs_lpscl16_conductivity.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["system","Ea_eV","Ea_err","D0_cm2_s","n_Li_cm3","D600_mean","D600_std","D800_mean","D800_std","D1000_mean","D1000_std","sig600_mScm","sig800","sig1000"])
    for k,lab in (("b2o3","b2o3"),("modelc","LPSCl1.6")):
        d=S[k]
        w.writerow([lab,f"{d['Ea']:.3f}",f"{d['Eaerr']:.3f}",f"{d['D0']:.3e}",f"{d['n']:.3e}"]+
                   [x for T in (600,800,1000) for x in (f"{d['m'][T]:.3e}",f"{d['s'][T]:.2e}")]+
                   [f"{d['sig'][T]:.0f}" for T in (600,800,1000)])
    w.writerow(["ratio_b2o3/LPSCl1.6",f"dEa={b['Ea']-m['Ea']:+.3f}+/-{np.hypot(b['Eaerr'],m['Eaerr']):.3f}","","","","","","","","",""]+
               [f"{rat[T]:.2f}+/-{raterr[T]:.2f}" for T in (600,800,1000)])
    w.writerow([])
    w.writerow(["# PER-SEED D (cm2/s): FULLY symmetric 3-seed x 3-T reseed (600K + 800/1000K, kgy 2026-07-06/07)"])
    w.writerow(["system","T_K","s2","s3","s4"])
    for k,lab in (("b2o3","b2o3"),("modelc","LPSCl1.6")):
        for T in (600,800,1000):
            w.writerow([lab,T]+[f"{v:.4e}" for v in S[k]['D'][T]])
    for line in [
      "# ===== FINAL (2026-07-07). SUPERSEDES all single-seed tables (0.2234 Ea, 1.33x sigma, D0-decomposition). =====",
      "# Ea EQUAL: 0.199+/-0.034 vs 0.197+/-0.032 (dEa +0.002+/-0.047).",
      "# sigma ratio per T: 1.08+/-0.18 / 0.82+/-0.15 / 1.15+/-0.12 -> scatter AROUND 1.0 = statistically EQUIVALENT transport.",
      "# The old 1.33x rested on the single-seed 800K pair (b2o3 3.009 high-outlier vs modelc 2.054 low-outlier); reseeded means: 2.163 vs 2.845.",
      "# FRAME for the paper: O-substitution normally LOWERS sigma in oxysulfides; here BVSE channel opening (+45% in-plane) offsets the O-penalty",
      "#   -> conductivity PRESERVED (not boosted). Robust b2o3 gains live in mechanics (+13% bulk) and the covalent B-S network.",
      "# absolute sigma = MLIP Nernst-Einstein upper bound; RT extrapolation NOT reportable (Ea error x ~5 amplification at 300K).",
    ]: w.writerow([line])
print("wrote b2o3_vs_lpscl16_conductivity.csv")

# ---- FINAL Arrhenius figure (all three T reseeded) ----
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
RED,BLUE,INK="#d1352b","#1f6fb4","#222"
fig,(axA,axB)=plt.subplots(1,2,figsize=(12.4,4.8))
Ts=np.array([600,800,1000]); X=1000/Ts
for k,c,mk,lab in (("b2o3",RED,"^","B$_2$O$_3$-doped"),("modelc",BLUE,"s","LPSCl1.6 (undoped)")):
    d=S[k]
    xl=np.linspace(0.95,1.72,50)
    axA.plot(xl, np.log10(d['D0'])-d['Ea']/(kB*np.log(10))*1e-3*xl, "-", color=c, lw=1.5,
             label=f"{lab}:  E$_a$={d['Ea']:.3f}$\\pm${d['Eaerr']:.3f} eV")
    for T in Ts:
        for v in d['D'][T]:
            axA.plot(1000/T, np.log10(v), mk, ms=3.6, mfc="none", mec=c, alpha=0.5)
        dm,ds=d['m'][T],d['s'][T]
        axA.errorbar(1000/T, np.log10(dm), yerr=ds/(dm*np.log(10)), fmt=mk, ms=8.5, color=c,
                     capsize=4, elinewidth=1.3, mec="k", mew=0.5, zorder=5)
axA.set_xlabel("1000 / T  (K$^{-1}$)"); axA.set_ylabel("log$_{10}$ D  (cm$^2$/s)")
axA.set_xlim(0.95,1.72); axA.grid(alpha=0.22,lw=0.6); axA.set_axisbelow(True)
axA.legend(fontsize=9, loc="upper right")
axT=axA.twiny(); axT.set_xlim(axA.get_xlim()); tk=[600,700,800,1000]
axT.set_xticks([1000/t for t in tk]); axT.set_xticklabels(tk); axT.set_xlabel("T (K)", fontsize=10)
axA.set_title("Arrhenius — every T now 3-seed (small = seeds, filled = mean$\\pm$std)", fontsize=10.5, fontweight="bold", pad=26)

w=0.36; xb=np.arange(3)
for j,(k,c,lab) in enumerate((("b2o3",RED,"B$_2$O$_3$-doped"),("modelc",BLUE,"LPSCl1.6"))):
    d=S[k]; off=(-0.5+j)*w
    axB.bar(xb+off,[d['sig'][T] for T in Ts], w, color=c, edgecolor="white", lw=1, label=lab)
    axB.errorbar(xb+off,[d['sig'][T] for T in Ts],[d['sigerr'][T] for T in Ts],fmt="none",ecolor=INK,capsize=4,elinewidth=1.2,zorder=5)
for i,T in enumerate(Ts):
    axB.text(i, max(b['sig'][T],m['sig'][T])+330, f"ratio {rat[T]:.2f}$\\pm${raterr[T]:.2f}", ha="center", fontsize=8.8, color=INK)
axB.set_xticks(xb); axB.set_xticklabels([f"{T} K" for T in Ts])
axB.set_ylabel("$\\sigma$  (mS/cm, MLIP N-E)"); axB.set_ylim(0,3200)
axB.grid(axis="y",alpha=0.22,lw=0.6); axB.set_axisbelow(True); axB.legend(fontsize=9, loc="upper left")
axB.set_title("$\\sigma$ ratio scatters around 1.0  →  equivalent transport", fontsize=10.5, fontweight="bold")
fig.suptitle("FINAL ionic transport — fully symmetric 3-seed $\\times$ 3-T:  equal E$_a$, equivalent $\\sigma$  (O-penalty offset by channel opening)",
             fontsize=11.3, fontweight="bold", y=1.01)
fig.tight_layout(); fig.savefig("b2o3_vs_lpscl16_arrhenius_3seed.png", dpi=200, bbox_inches="tight")
print("wrote b2o3_vs_lpscl16_arrhenius_3seed.png")
