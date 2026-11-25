#!/usr/bin/env python3
"""세미나용 3계 MSD·아레니우스·σ 세트. 지위 배너를 그림에 박는다."""
import sys, csv, json, pathlib
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
sys.path.insert(0, str(R/"tools/figures")); import house_style as H
DB, OUT = R/"db/properties", R/"docs/figures/seminar_2026_09_07"

KB, Q = 1.380649e-23, 1.602176634e-19
def sigma_mScm(n_cm3, D, T): return 1e3*n_cm3*Q*Q*D/(KB*T)

# ── 잣대 세대 각주 (2026-09-07) ──────────────────────────────────────────
#   왜: 이 세트는 gen0(게이트 이전) 자료다. 그림·CSV 가 슬라이드로 옮겨지면 대화 맥락은
#   떨어져 나가므로 **각주를 산출물 안에 박는다.** 문구는 세대 원장이 단일 출처다 —
#   여기 손으로 적으면 원장과 갈라진다.
GEN_ID = "gen0_pre_gate"
_gens = {g["id"]: g for g in json.loads(
    (DB/"md_protocol_generations.json").read_text(encoding="utf-8"))["generations"]}
GEN_NOTE = _gens[GEN_ID]["영문_각주"]
assert GEN_NOTE, "세대 원장에 영문 각주가 없다"

SYS = {  # label, color, Ea, Ea_err, D(600/800/1000), n_Li, seeds, status
 "LPSCl1.6":       dict(c="#2563eb", Ea=0.197, err=0.032, D=[1.037e-05,2.845e-05,4.728e-05],
                        n=2.220e22, seeds="3 seeds × 3 T", st="baseline"),
 "LPSOCl1.6":      dict(c="#c05621", Ea=0.287, err=0.024, D=[6.2705e-06,2.4162e-05,5.7093e-05],
                        n=2.242e22, seeds="4 seeds × 3 T", st="baseline"),
 "B2O3@LPSCl1.6":  dict(c="#be123c", Ea=0.199, err=0.034, D=[1.041e-05,2.163e-05,5.081e-05],
                        n=2.381e22, seeds="3 seeds × 3 T", st="RETRACTED"),
}
TT = [600, 800, 1000]
for k,v in SYS.items(): v["sig"] = [sigma_mScm(v["n"],d,T) for d,T in zip(v["D"],TT)]

# ── MSD ────────────────────────────────────────────────────────────────
rows=[r for r in open(DB/"msd_3sys_200ps_origin.csv") if not r.lstrip().startswith(('#','"#'))]
rd=list(csv.reader(rows)); hdr=rd[0]; dat=np.array([[float(x) for x in r] for r in rd[1:] if r and all(c.strip() for c in r)])
t=dat[:,0]
fig,axes=plt.subplots(1,3,figsize=(14,4.4),sharex=True)
for ax,T in zip(axes,TT):
    for name,v in SYS.items():
        j=hdr.index(f"{name}_{T}K")
        ax.plot(t,dat[:,j],color=v["c"],lw=1.9,
                ls="--" if v["st"]=="RETRACTED" else "-",label=name)
    ax.axvspan(2,50,color="#fef9c3",zorder=0)
    H.apply_axes(ax,xlabel="t (ps)",ylabel=r"Li MSD ($\rm\AA^2$)" if T==600 else None,
                 title=f"{T} K")
axes[0].legend(frameon=False,fontsize=9,loc="upper left")
axes[0].text(26,axes[0].get_ylim()[1]*.04,"fit window\n2–50 ps",ha="center",fontsize=8,color=H.MUT)
fig.suptitle(f"Li MSD — seed-ensemble means, UMA-s-1p1 (omat), 0–{t.max():.0f} ps",
             fontsize=12,color=H.INK)   # ⛔ 부모 CSV 헤더는 "0-200 ps" 라고 하지만
                                         #   데이터는 온도 공통 길이로 잘려 있다 — 실측을 쓴다
fig.text(.5,.032,"dashed = B2O3@LPSCl1.6: UMA-MD transport axis RETRACTED 2026-08-25 "
         "(anion-sublattice mobility) — shown for context only, not citable",
         ha="center",fontsize=8.5,color="#be123c")
fig.text(.5,.004,GEN_NOTE,ha="center",fontsize=7.8,color=H.MUT)
fig.tight_layout(rect=[0,.062,1,.95]); fig.savefig(OUT/"msd_3sys.png",dpi=300); plt.close(fig)

# ── Arrhenius ──────────────────────────────────────────────────────────
fig,ax=plt.subplots(figsize=(6.6,5.0))
x=np.array([1000/T for T in TT])
for name,v in SYS.items():
    y=np.log(np.array(v["D"]))
    ax.plot(x,y,"o",ms=7,color=v["c"],mfc="none" if v["st"]=="RETRACTED" else v["c"],mew=1.8)
    p=np.polyfit(x,y,1); xf=np.linspace(x.min()-.05,x.max()+.05,50)
    ax.plot(xf,np.polyval(p,xf),color=v["c"],lw=1.6,
            ls="--" if v["st"]=="RETRACTED" else "-",
            label=f"{name}   $E_a$ = {v['Ea']:.3f} ± {v['err']:.3f} eV")
H.apply_axes(ax,xlabel="1000 / T  (K$^{-1}$)",ylabel=r"ln $D$  ($D$ in cm$^2$/s)",
             title="Arrhenius — 3-point (600 / 800 / 1000 K)")
ax.legend(frameon=False,fontsize=9.5,loc="upper right")
sec=ax.secondary_xaxis("top",functions=(lambda v:1000/np.clip(v,1e-9,None),
                                        lambda v:1000/np.clip(v,1e-9,None)))
sec.set_xlabel("T (K)",fontsize=10,color=H.MUT); sec.set_xticks(TT)
ax.text(.02,.03,"open symbols / dashed = RETRACTED axis (b2o3)",transform=ax.transAxes,
        fontsize=8.5,color="#be123c")
fig.text(.5,.006,GEN_NOTE,ha="center",fontsize=7.4,color=H.MUT,wrap=True)
fig.tight_layout(rect=[0,.045,1,1]); fig.savefig(OUT/"arrhenius_3sys.png",dpi=300); plt.close(fig)

# ── sigma ──────────────────────────────────────────────────────────────
fig,ax=plt.subplots(figsize=(7.0,4.6))
w=.26; xs=np.arange(3)
for i,(name,v) in enumerate(SYS.items()):
    ax.bar(xs+(i-1)*w,v["sig"],w,color=v["c"],label=name,
           alpha=.45 if v["st"]=="RETRACTED" else .9,
           hatch="//" if v["st"]=="RETRACTED" else None,edgecolor=v["c"])
    for xx,s in zip(xs+(i-1)*w,v["sig"]):
        ax.text(xx,s*1.02,f"{s:.0f}",ha="center",fontsize=7.5,color=H.MUT)
ax.set_xticks(xs); ax.set_xticklabels([f"{T} K" for T in TT])
H.apply_axes(ax,ylabel=r"$\sigma_{\rm Li}$ (mS/cm)",
             title="Nernst–Einstein conductivity ($H_R$ = 1 assumed) — NOT a bound")
ax.legend(frameon=False,fontsize=9)
fig.text(.5,.042,"[!] absolute sigma NOT citable — H_R<1 makes NE an UNDER-estimate, pellet GB pushes the other way · "
         "no 300 K extrapolation · hatched = retracted axis",
         ha="center",fontsize=8.5,color="#be123c")
fig.text(.5,.006,GEN_NOTE,ha="center",fontsize=7.4,color=H.MUT)
fig.tight_layout(rect=[0,.075,1,1]); fig.savefig(OUT/"sigma_3sys.png",dpi=300); plt.close(fig)

# ── Origin-ready CSV ───────────────────────────────────────────────────
with open(OUT/"seminar_3sys_summary.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["# Seminar set 2026-09-07 — MOST RECENT values per system. NOT a citable table."])
    w.writerow(["# LPSCl1.6/B2O3: b2o3_vs_lpscl16_conductivity.csv (FINAL 2026-07-07, 3seed x 3T)"])
    w.writerow(["# LPSOCl1.6: lpsocl_md_arrhenius.json (4seed x 3T, headline 2026-07-27)"])
    w.writerow(["# sigma = Nernst-Einstein with H_R = 1 assumed. Absolute sigma NOT citable."])
    w.writerow(["#   NOT an upper bound: H_R = D*/D_sigma < 1 (correlated motion) makes NE an UNDER-estimate"])
    w.writerow(["#   (Adeli 2019 measures H_R = 0.23 for Li5.5PS4.5Cl1.5 -> sigma_true ~ 4.3x sigma_NE),"])
    w.writerow(["#   while pellet grain boundaries push measured sigma the other way. Net sign undetermined."])
    w.writerow(["#   Like-for-like our D* is fine: D*(300 K) 1.02e-7 vs Adeli 7Li PFG 1.01e-7 cm^2/s."])
    w.writerow(["# B2O3@LPSCl1.6 UMA-MD transport axis RETRACTED 2026-08-25 (framework creep)."])
    w.writerow([f"# PROTOCOL GENERATION: {GEN_ID}. {GEN_NOTE}"])
    w.writerow(["#   -> db/properties/md_protocol_generations.json (gates G1-G5)"])
    w.writerow(["# sigma(T) is computed PER TEMPERATURE from that row's D:"])
    w.writerow(["#   sigma = n_Li * e^2 * D(T) / (k_B * T)   [Nernst-Einstein, Haven=1]"])
    w.writerow(["#   Ea is a SEPARATE quantity: slope of ln D vs 1000/T across the 3 rows."])
    w.writerow(["system","status","seeds","Ea_eV","Ea_err_eV","T_K","D_cm2_s","n_Li_cm-3","sigma_mScm"])
    for name,v in SYS.items():
        for T,d,s in zip(TT,v["D"],v["sig"]):
            w.writerow([name,v["st"],v["seeds"],v["Ea"],v["err"],T,f"{d:.4e}",f"{v['n']:.3e}",f"{s:.1f}"])
print("saved:", *(p.name for p in sorted(OUT.iterdir())))
for name,v in SYS.items():
    print(f"  {name:16s} Ea {v['Ea']:.3f}±{v['err']:.3f}  σ " +
          " / ".join(f"{s:.0f}" for s in v["sig"]) + " mS/cm  [" + v["st"] + "]")
