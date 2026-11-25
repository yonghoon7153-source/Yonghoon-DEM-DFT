#!/usr/bin/env python3
"""조성별 한 그림 × 3온도 MSD. 실제 t 범위를 제목에 쓴다(헤더를 믿지 않는다)."""
import sys, csv, pathlib
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
sys.path.insert(0, str(R/"tools/figures")); import house_style as H
DB, OUT = R/"db/properties", R/"docs/figures/seminar_2026_09_07"

# ── 잣대 세대 각주 (2026-09-07) ──────────────────────────────────────────
#   그림·CSV 는 슬라이드로 옮겨지면 대화 맥락이 떨어져 나간다 → 각주를 산출물 안에 박는다.
#   문구는 세대 원장이 단일 출처다 (여기 손으로 적으면 갈라진다).
import json as _json
GEN_ID = "gen0_pre_gate"
GEN_NOTE = {g["id"]: g for g in _json.loads(
    (DB/"md_protocol_generations.json").read_text(encoding="utf-8"))["generations"]
}[GEN_ID]["영문_각주"]
assert GEN_NOTE, "세대 원장에 영문 각주가 없다"

rows=[r for r in open(DB/"msd_3sys_200ps_origin.csv") if not r.lstrip().startswith(('#','"#'))]
rd=list(csv.reader(rows)); hdr=rd[0]
dat=np.array([[float(x) for x in r] for r in rd[1:] if r and all(c.strip() for c in r)])
t=dat[:,0]; TMAX=t.max()

SYS=[("LPSCl1.6","LPSCl$_{1.6}$",  "baseline"),
     ("LPSOCl1.6","LPSOCl$_{1.6}$","baseline"),
     ("B2O3@LPSCl1.6","B$_2$O$_3$@LPSCl$_{1.6}$","RETRACTED")]
TC={600:"#2563eb", 800:"#c05621", 1000:"#be123c"}

fig,axes=plt.subplots(1,3,figsize=(14,4.4))
for ax,(key,lab,st) in zip(axes,SYS):
    for T in (600,800,1000):
        y=dat[:,hdr.index(f"{key}_{T}K")]
        ax.plot(t,y,color=TC[T],lw=1.9,label=f"{T} K")
    ax.axvspan(2,50,color="#fef9c3",zorder=0)
    ttl=lab + ("   ⚠ RETRACTED" if st=="RETRACTED" else "")
    H.apply_axes(ax,xlabel="t (ps)",
                 ylabel=r"Li MSD ($\rm\AA^2$)" if key=="LPSCl1.6" else None, title=ttl)
    if st=="RETRACTED":
        ax.title.set_color("#be123c")
        for sp in ("bottom","left"): ax.spines[sp].set_color("#be123c")
    ax.legend(frameon=False,fontsize=9.5,loc="upper left")
    ax.set_xlim(0,TMAX)
for ax in axes:   # 곡선과 안 겹치게 음영 위쪽에
    ax.text(26,ax.get_ylim()[1]*.955,"fit window 2–50 ps",
            ha="center",va="top",fontsize=8,color="#a16207")
# y 축을 계마다 자유롭게 두되 세 계의 최대를 주석으로 (스케일 착시 방지)
fig.suptitle(f"Li MSD per composition — seed-ensemble means · UMA-s-1p1 (omat) · 0–{TMAX:.0f} ps",
             fontsize=12,color=H.INK)
fig.text(.5,.032,"y-axes are independent per panel (see values) · "
         "B2O3@LPSCl1.6: UMA-MD transport axis RETRACTED 2026-08-25 — context only, not citable",
         ha="center",fontsize=8.5,color="#be123c")
fig.text(.5,.004,GEN_NOTE,ha="center",fontsize=7.8,color=H.MUT)
fig.tight_layout(rect=[0,.062,1,.94])
fig.savefig(OUT/"msd_per_composition.png",dpi=300); plt.close(fig)

# ── 같은 y 축 판 (계 간 비교용) ────────────────────────────────────────
fig,axes=plt.subplots(1,3,figsize=(14,4.4),sharey=True)
ymax=max(dat[:,1:].max()*1.05,1)
for ax,(key,lab,st) in zip(axes,SYS):
    for T in (600,800,1000):
        ax.plot(t,dat[:,hdr.index(f"{key}_{T}K")],color=TC[T],lw=1.9,label=f"{T} K")
    ax.axvspan(2,50,color="#fef9c3",zorder=0)
    H.apply_axes(ax,xlabel="t (ps)",
                 ylabel=r"Li MSD ($\rm\AA^2$)" if key=="LPSCl1.6" else None,
                 title=lab + ("   ⚠ RETRACTED" if st=="RETRACTED" else ""))
    if st=="RETRACTED": ax.title.set_color("#be123c")
    ax.set_xlim(0,TMAX); ax.set_ylim(0,ymax)
axes[0].legend(frameon=False,fontsize=9.5,loc="upper left")
fig.suptitle(f"Li MSD per composition — SHARED y-axis · 0–{TMAX:.0f} ps",fontsize=12,color=H.INK)
fig.text(.5,.032,"same y-scale across panels — use this one to compare compositions",
         ha="center",fontsize=8.5,color=H.MUT)
fig.text(.5,.004,GEN_NOTE,ha="center",fontsize=7.8,color=H.MUT)
fig.tight_layout(rect=[0,.062,1,.94])
fig.savefig(OUT/"msd_per_composition_sharedY.png",dpi=300); plt.close(fig)

# ── 조성별 CSV ─────────────────────────────────────────────────────────
NOTE={"LPSCl1.6":"3 seeds; 600 K from modelc_600_reseed (200 ps run), 800/1000 K from highT_reseed (100 ps run)",
      "LPSOCl1.6":"4 seeds; lpsocl_md ladder+reseed_hiT s2/s3/s4 (200 ps runs); licube EXCLUDED (same-seed rerun)",
      "B2O3@LPSCl1.6":"3 seeds; 600 K b2o3_600_reseed (200 ps), 800/1000 K highT_reseed/b2o3 (100 ps). AXIS RETRACTED 2026-08-25"}
for key,lab,st in SYS:
    fn=OUT/f"msd_{key.replace('@','_at_')}.csv"
    with open(fn,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow([f"# Li MSD (A^2) vs t — {key}. Seed-ensemble means, UMA-s-1p1 (omat)."])
        w.writerow([f"# t range 0-{TMAX:.0f} ps @ 1 ps. NOTE: parent file header says '0-200 ps'"])
        w.writerow([ "#   but the data is truncated to the common length across temperatures."])
        w.writerow([f"# {NOTE[key]}"])
        w.writerow([ "# Fit window 2-50 ps, free intercept: MSD = 6Dt + c."])
        w.writerow([f"# PROTOCOL GENERATION: {GEN_ID}. {GEN_NOTE}"])
        w.writerow([ "#   -> db/properties/md_protocol_generations.json (gates G1-G5)"])
        if st=="RETRACTED":
            w.writerow(["# !! UMA-MD transport axis RETRACTED 2026-08-25 (anion-sublattice mobility)."])
            w.writerow(["#    D / Ea / sigma from these curves are NOT citable. Context only."])
        w.writerow(["t_ps","MSD_600K_A2","MSD_800K_A2","MSD_1000K_A2"])
        for i,tt in enumerate(t):
            w.writerow([f"{tt:.1f}"]+[f"{dat[i,hdr.index(f'{key}_{T}K')]:.3f}" for T in (600,800,1000)])
    print("→",fn.name)
print(f"\n실제 t 범위 0–{TMAX:.0f} ps ({len(t)}점) · 최종 MSD (Å²)")
for key,lab,st in SYS:
    print(f"  {key:16s} " + " · ".join(
        f"{T}K {dat[-1,hdr.index(f'{key}_{T}K')]:7.1f}" for T in (600,800,1000)))
