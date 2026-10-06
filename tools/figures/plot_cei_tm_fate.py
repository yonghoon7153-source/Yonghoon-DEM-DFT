#!/usr/bin/env python3
"""plot_cei_tm_fate.py — CEI 주장 1 그림: 고전압에서 양극 전이금속(TM)이 인산염으로 끌려간다.

왜 있나 (2026-10-06)
--------------------
CEI 실험 쪽 1저자가 원고를 두 주장으로 닫으려 한다 — ① TM 방출로 인한 인산염 형성·열화
② Nd 함유 CEI (XPS + 임피던스). ①을 받칠 계산 그림이 페이지(`db/properties/cei_figs/index.html`)
에 **한 장으로 없었다**: Fig. 2(P 사다리)는 *P 가 어디로 가나* 를, Fig. 3 은 *Nd 가 얼마나 막나* 를
그린다. *Nd 없는 전해질에서 양극 TM 이 전압별로 어디로 가나* 는 원장
`db/properties/cei_tm_fate_2026_09_17.json` (interface_reactivity_v2.py tm_fate 산출)에만 있었다.
이 스크립트는 그 원장을 **읽기만** 한다 — 새 계산이 없다.

그림
----
양극 넷(LiCoO2 · LiNiO2 · NMC811 · LiMnO2) 패널, 가로 = 인가 전압, 막대 = LPSCl1.6
(Li5.4PS4.4Cl1.6 · 1저자 조성의 x = 0 에 가장 가까운 계) 과의 최소 에너지 계면 반응에서
**반응한 양극 TM 이 가는 곳** 100 % 스택 (TM 인산염 · TM 황화물 · 그 밖 = 염화물·황산염).
검은 표식은 LPSCl(Li6PS5Cl) · LPSOCl1.6 의 TM 인산염 몫 — 전해질을 바꿔도 같은 모양인지 본다.

⛔ 이 그림이 못 하는 것 (캡션·대화에 같이 실을 것)
  · **열화 속도·용량 손실을 말하지 않는다.** 0 K hull 의 산물 조합이다 (CEI 페이지 §9 금지 서술).
  · 분모는 *반응에 들어간* 양극 TM 이다 — "양극의 몇 % 가 녹는다" 가 아니다.
  · **황화물도 양극 소모다** (원장 ⛔). 인산염이 0 인 칸을 "양극이 안전" 으로 읽지 않는다.
  · 최소 꺾임 하나만 본다. 전해질 자체분해 칸(양극이 반응식에 없음)은 **그리지 않는다** (0 이 아니다).
  · 반응에너지 절대값을 다른 논문 옆에 놓지 않는다 (MP 눈금 혼합) — 이 그림은 몫만 그린다.

쓰는 법
  python3 tools/figures/plot_cei_tm_fate.py              # PNG + Origin CSV
  python3 tools/figures/plot_cei_tm_fate.py --nd         # Nd₂O₃@LPSCl1.6 판 + 4.3 V 농도 판 (2026-10-06)
  python3 tools/figures/plot_cei_tm_fate.py --simple     # 한 장 요약 (4.3 V · 양극 셋 · Nd 없음 / x 0.02 / x 0.10)
  python3 tools/figures/plot_cei_tm_fate.py --ncm        # NMC811 만 · 금속별(Ni·Co·Mn) 인산염 % 표 그림
  python3 tools/figures/plot_cei_tm_fate.py --selftest   # 음성 경로 포함

--nd 모드 (2026-10-06 · 사용자 "Nd₂O₃@LPSCl1.6 버전으로도" · "얼마나 줄어드는지")
  · 막대 = Nd₂O₃@LPSCl1.6 = 1저자 조성 `nd_p_002_asused` (Li5.44Nd0.02P0.98S4.37O0.03Cl1.6 · Nd:O = 2:3)
    — x = 0.02 스캔 반응식(`cei_figs/cei_x_scan_panels_x002.csv`)에 **같은 분류 함수**
    (`interface_reactivity_v2.tm_fate`)를 돌린다. 원장 값과 대조: 보호율 원장의 ndP002 와 같아야 한다 (selftest).
  · 비교 표식 = **Li 를 맞춘 무-Nd 대조군** (보호율 원장 `cei_protection_allcells_result_2026_09_21.csv`
    의 tm_phosphate_share_control) — CEI 페이지 §2b 규칙: base(LPSCl1.6) 와 견주면 Li 재고 교란이 들어온다.
    ⇒ 첫 그림(LPSCl1.6 막대)과 숫자가 거의 같지만(≤0.3 %p) **Δ 는 대조군 기준**이다.
  · 비교 게이트(원장 gate_pass)를 못 넘은 칸은 Δ 를 쓰지 않고 'not comparable' 로 둔다 (0 이 아니다).
  · 농도 판: 4.3 V · LiCoO2 · LiNiO2 · NMC811 (LiMnO2 4.3 V 는 전 농도 게이트 탈락 — 그리지 않는다).
    x = 0 점은 같은 계열의 x → 0 끝 `o_only_003` (Li5.4PS4.37O0.03Cl1.6).
  ⛔ "Nd 가 양극을 지킨다 · 열화를 억제한다" 로 읽지 않는다 — 인산염을 면한 TM 은 대부분 황화물로 간다
    (CEI 페이지 §9). 이 그림은 **TM 인산염 몫의 변화**만 그린다.
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "db/properties/cei_tm_fate_2026_09_17.json"
OUT_PNG = REPO / "db/properties/cei_figs/cei_tm_fate_undoped.png"
OUT_CSV = REPO / "db/properties/cei_figs/cei_tm_fate_undoped.csv"

CATHODES = ["LiCoO2", "LiNiO2", "NMC811", "LiMnO2"]
CAT_LABEL = {"LiCoO2": "LiCoO$_2$", "LiNiO2": "LiNiO$_2$", "NMC811": "NMC811", "LiMnO2": "LiMnO$_2$"}
VOLTS = [2.5, 3.0, 3.5, 4.0, 4.3, 4.5]
MAIN = "modelc"                       # LPSCl1.6
OVERLAY = [("comp1", "LPSCl", "o"), ("lpsocl", "LPSOCl1.6", "^")]
SE_LABEL = {"modelc": "LPSCl1.6", "comp1": "LPSCl", "lpsocl": "LPSOCl1.6"}

# ── --nd 모드 ──────────────────────────────────────────────────────────────
X002_CSV = REPO / "db/properties/cei_figs/cei_x_scan_panels_x002.csv"
PROT_CSV = REPO / "db/properties/cei_protection_allcells_result_2026_09_21.csv"
ND = "nd_p_002_asused"                 # Nd₂O₃@LPSCl1.6 (1저자 조성)
ND_X0 = "o_only_003"                   # 같은 계열 x → 0
OUT_ND_PNG = REPO / "db/properties/cei_figs/cei_tm_fate_nd2o3_x002.png"
OUT_ND_CSV = REPO / "db/properties/cei_figs/cei_tm_fate_nd2o3_x002.csv"
OUT_DOSE_PNG = REPO / "db/properties/cei_figs/cei_tm_fate_nd_dose_4p3V.png"
OUT_DOSE_CSV = REPO / "db/properties/cei_figs/cei_tm_fate_nd_dose_4p3V.csv"
DOSE_V = 4.3
DOSE_CATS = ["LiCoO2", "LiNiO2", "NMC811"]
CAT_COLOR = {"LiCoO2": "#2563eb", "LiNiO2": "#059669", "NMC811": "#d97706"}


def x002_fate(csv_path=X002_CSV, electrolytes=(ND, ND_X0)):
    """x = 0.02 스캔 반응식에 첫 그림과 **같은 분류 함수**를 돌린다."""
    sys.path.insert(0, str(REPO / "tools/oxidation"))
    import interface_reactivity_v2 as IR
    d = IR.tm_fate(str(csv_path))
    rows = [r for r in d["rows"] if r["electrolyte"] in electrolytes]
    # 조성 확인 — 라벨이 가리키는 반응식에 Nd 0.02 · O 0.03 이 실제로 있는가
    with open(csv_path) as fh:
        lhs = {r["electrolyte"]: r["reaction"].split("->")[0] for r in csv.DictReader(fh)
               if r["electrolyte"] == ND and r["is_minimum"] in ("1", "True") and "->" in r["reaction"]}
    if ND in electrolytes and not ("Nd0.02" in lhs.get(ND, "") and "O0.03" in lhs.get(ND, "")):
        raise ValueError(f"{ND} 반응식에 Nd0.02 · O0.03 이 없다 — 라벨이 다른 조성을 가리킨다: {lhs.get(ND)!r}")
    return table(rows)


def prot_rows(path=PROT_CSV):
    """(cathode, V, x) -> 보호율 원장 행.  gate_pass 는 bool 로."""
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (r["cathode"], float(r["voltage_V"]), round(float(r["x_Nd"]), 4))
            f = lambda k: None if r[k] in ("", None) else float(r[k])
            out[key] = {"nd": f("tm_phosphate_share"), "ctrl": f("tm_phosphate_share_control"),
                        "gate": r["gate_pass"] == "True", "phase": r["nd_phases"],
                        "why": r["gate_fail_reason"]}
    return out


def delta_pp(nd_share, prot):
    """Δ (%p) = Nd − 대조.  게이트 탈락·값 없음이면 None (0 이 아니다)."""
    if prot is None or not prot["gate"] or prot["ctrl"] is None or nd_share is None:
        return None
    return 100.0 * (nd_share - prot["ctrl"])


def load_rows(path=SRC):
    d = json.loads(Path(path).read_text())
    return d["rows"], set(d.get("self_decomposition_excluded", []))


def table(rows):
    """(electrolyte, cathode, V) -> share dict.  없는 칸은 키가 없다 (0 으로 채우지 않는다)."""
    t = {}
    for r in rows:
        key = (r["electrolyte"], r["cathode"], float(r["voltage_V"]))
        if key in t:
            raise ValueError(f"중복 칸 {key}")
        sh = r["share"]
        tot = sh["phosphate"] + sh["sulfide"] + sh["other"]
        if abs(tot - 1.0) > 0.01:
            raise ValueError(f"몫 합이 1 이 아니다 {key}: {tot:.4f}")
        t[key] = {"phosphate": sh["phosphate"], "sulfide": sh["sulfide"], "other": sh["other"],
                  "phases": r.get("phases", {})}
    return t


def csv_rows(t):
    out = []
    for se in [MAIN] + [o[0] for o in OVERLAY]:
        for cat in CATHODES:
            for v in VOLTS:
                c = t.get((se, cat, v))
                out.append({
                    "electrolyte": SE_LABEL[se], "cathode": cat, "voltage_V": v,
                    "TM_to_phosphate_frac": "" if c is None else round(c["phosphate"], 4),
                    "TM_to_sulfide_frac": "" if c is None else round(c["sulfide"], 4),
                    "TM_to_other_frac": "" if c is None else round(c["other"], 4),
                    "TM_phosphate_phases": "" if c is None else " ".join(c["phases"].get("phosphate", [])),
                    "note": "not drawn: electrolyte self-decomposition / no cathode in min reaction" if c is None else "",
                })
    return out


def _selftest():
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok &= bool(cond)

    rows, _ = load_rows()
    t = table(rows)
    check("실제 원장: LPSCl1.6 칸 23 개 (LiMnO2 4.5 V 자체분해로 없음)",
          sum(1 for k in t if k[0] == MAIN) == 23 and (MAIN, "LiMnO2", 4.5) not in t)
    cr = csv_rows(t)
    miss = [r for r in cr if r["electrolyte"] == "LPSCl1.6" and r["cathode"] == "LiMnO2" and r["voltage_V"] == 4.5][0]
    check("⛔음성: 없는 칸을 CSV 에 0 으로 쓰지 않는다 (빈칸 + note)",
          miss["TM_to_phosphate_frac"] == "" and "self-decomposition" in miss["note"])
    check("실제 원장: LPSCl1.6·LiCoO2 는 3.5 V 까지 인산염 0 · 4.0 V 부터 > 0",
          t[(MAIN, "LiCoO2", 3.5)]["phosphate"] == 0 and t[(MAIN, "LiCoO2", 4.0)]["phosphate"] > 0)
    with tempfile.TemporaryDirectory() as d:
        bad = Path(d) / "bad.json"
        bad.write_text(json.dumps({"rows": [{"electrolyte": "modelc", "cathode": "LiCoO2", "voltage_V": 4.0,
                                             "share": {"phosphate": 0.5, "sulfide": 0.2, "other": 0.0}}]}))
        try:
            table(load_rows(bad)[0]); caught = False
        except ValueError:
            caught = True
        check("⛔음성: 몫 합이 1 이 아닌 칸을 잡는다", caught)
        dup = Path(d) / "dup.json"
        r1 = {"electrolyte": "modelc", "cathode": "LiCoO2", "voltage_V": 4.0,
              "share": {"phosphate": 0.2, "sulfide": 0.8, "other": 0.0}}
        dup.write_text(json.dumps({"rows": [r1, r1]}))
        try:
            table(load_rows(dup)[0]); caught = False
        except ValueError:
            caught = True
        check("⛔음성: 같은 칸이 두 번 나오면 잡는다", caught)
    # ── --nd 모드 ──
    tn = x002_fate()
    pr = prot_rows()
    same = all(abs(tn[(ND, c, v)]["phosphate"] - pr[(c, v, 0.02)]["nd"]) < 1e-4
               for (e, c, v) in tn if e == ND and pr.get((c, v, 0.02), {}).get("nd") is not None)
    check("--nd: tm_fate(x002 스캔) 의 Nd₂O₃@LPSCl1.6 몫 = 보호율 원장 ndP002 (같은 조성 · 다른 경로)", same)
    check("⛔음성 --nd: 게이트 탈락 칸(LiMnO2 4.3 V)은 Δ 를 내지 않는다",
          delta_pp(tn[(ND, "LiMnO2", 4.3)]["phosphate"], pr[("LiMnO2", 4.3, 0.02)]) is None)
    check("--nd: LiCoO2 4.3 V Δ 는 음수 (Nd 가 인산염 몫을 줄인다)",
          delta_pp(tn[(ND, "LiCoO2", 4.3)]["phosphate"], pr[("LiCoO2", 4.3, 0.02)]) < 0)
    with tempfile.TemporaryDirectory() as d:
        fake = Path(d) / "x.csv"
        fake.write_text("cathode,electrolyte,voltage_V,x_atomic_frac,reaction_energy_eV_per_atom,is_minimum,"
                        "forms_Nd_phosphate,reaction\nLiCoO2,nd_p_002_asused,4.3,0.5,-1,1,0,"
                        "0.5 Li5.4P1S4.4Cl1.6 + 0.5 LiCoO2 -> 0.5 CoS2 + 1 Li\n")
        try:
            x002_fate(fake); caught = False
        except ValueError:
            caught = True
        check("⛔음성 --nd: 라벨이 Nd 없는 조성을 가리키면 멈춘다", caught)
    # ── --ncm ──
    nt = ncm_table()
    check("--ncm: Mn 은 모든 전압·두 조성에서 100 % 인산염 · Co 는 0 %",
          all(abs(nt[(sp, v)]["Mn"]["phosphate"] - 1) < 1e-3 and nt[(sp, v)]["Co"]["phosphate"] < 1e-9
              for sp, _ in NCM_CASES for v in VOLTS))
    check("--ncm: 세 금속 합 = TM 전체 몫 (보호율 원장 tm_phosphate_share_control 4.3 V 와 일치)",
          abs(0.8 * nt[("liMatch002", 4.3)]["Ni"]["phosphate"]
              + 0.1 * nt[("liMatch002", 4.3)]["Mn"]["phosphate"] - pr[("NMC811", 4.3, 0.02)]["ctrl"]) < 2e-3)
    try:
        metal_fate("1 LiNi0.8Co0.1Mn0.1O2 -> 0.5 NiS2 + 0.1 CoS2"); caught = False
    except ValueError:
        caught = True
    check("⛔음성 --ncm: 금속 장부가 안 맞는 반응식(Ni 0.3 · Mn 0.1 증발)을 잡는다", caught)
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    sys.path.insert(0, str(REPO / "tools/figures"))
    from house_style import INK, MUT, ELEM, apply_axes

    rows, _ = load_rows()
    t = table(rows)
    cr = csv_rows(t)
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cr[0]))
        w.writeheader(); w.writerows(cr)

    C_PHOS, C_SULF, C_OTH = ELEM["P"], ELEM["S"], "#d1d5db"
    fig, axes = plt.subplots(1, 4, figsize=(13.2, 3.9), sharey=True)
    xs = list(range(len(VOLTS)))
    for ax, cat in zip(axes, CATHODES):
        ax.axvline(2.5, color=MUT, ls=":", lw=1.0, zorder=1)     # 3.5 | 4.0 V 경계
        for i, v in enumerate(VOLTS):
            c = t.get((MAIN, cat, v))
            if c is None:
                ax.text(i, 50, "n/a", ha="center", va="center", fontsize=9, color=MUT, rotation=90)
                continue
            p, s, o = 100 * c["phosphate"], 100 * c["sulfide"], 100 * c["other"]
            ax.bar(i, p, color=C_PHOS, width=0.72, zorder=2)
            ax.bar(i, s, bottom=p, color=C_SULF, width=0.72, alpha=0.55, zorder=2)
            ax.bar(i, o, bottom=p + s, color=C_OTH, width=0.72, zorder=2)
            if p >= 1:      # 인산염 몫 숫자 — 막대 바닥(흰 글씨) · 낮은 막대는 바닥 위 (겹쳐 그린 표식을 피한다)
                inside = p > 12
                ax.text(i, 2.0 if inside else p + 1.5, f"{p:.0f}", ha="center",
                        va="bottom", fontsize=8.5, fontweight="bold",
                        color="white" if inside else C_PHOS, zorder=4)
        for se, lab, mk in OVERLAY:
            ys = [(i, 100 * t[(se, cat, v)]["phosphate"]) for i, v in enumerate(VOLTS) if (se, cat, v) in t]
            ax.plot([a for a, _ in ys], [b for _, b in ys], ls="none", marker=mk, ms=5.5,
                    mfc="white", mec=INK, mew=1.1, zorder=5)
        ax.set_xticks(xs, [f"{v:g}" for v in VOLTS])
        ax.set_ylim(0, 100); ax.set_xlim(-0.6, len(VOLTS) - 0.4)
        apply_axes(ax, xlabel="Applied voltage (V vs. Li/Li$^+$)", title=CAT_LABEL[cat], fontsize=11)
    apply_axes(axes[0], ylabel="Reacted cathode TM (%)", fontsize=11)
    handles = [Patch(color=C_PHOS, label="TM phosphate (LPSCl1.6)"),
               Patch(color=C_SULF, alpha=0.55, label="TM sulfide (LPSCl1.6)"),
               Patch(color=C_OTH, label="TM chloride / sulfate (LPSCl1.6)"),
               Line2D([], [], ls="none", marker="o", mfc="white", mec=INK, label="TM phosphate, LPSCl"),
               Line2D([], [], ls="none", marker="^", mfc="white", mec=INK, label="TM phosphate, LPSOCl1.6")]
    fig.legend(handles=handles, loc="upper center", ncol=5, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, 1.02), labelcolor=INK)
    fig.text(0.5, -0.04,
             "Minimum-energy cathode | electrolyte reaction, 0 K grand-potential hull (MP GGA/GGA+U), Li open at "
             "$\\mu_{Li} = \\mu_{Li}^{metal} - eV$. Bars: where the cathode transition metal that enters the reaction ends up.\n"
             "Dotted line: 3.5 | 4.0 V. This is a product channel, not a degradation rate. n/a: electrolyte self-decomposes (no cathode in the reaction).",
             ha="center", va="top", fontsize=8.3, color=MUT)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight"); plt.close(fig)
    print(f"→ {OUT_PNG.relative_to(REPO)}\n→ {OUT_CSV.relative_to(REPO)}")
    return 0


def main_nd():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    sys.path.insert(0, str(REPO / "tools/figures"))
    from house_style import INK, MUT, ELEM, apply_axes

    tn, pr = x002_fate(), prot_rows()
    # ── CSV (Nd₂O₃ 판) ──
    rows = []
    for cat in CATHODES:
        for v in VOLTS:
            c, p = tn.get((ND, cat, v)), pr.get((cat, v, 0.02))
            dp = None if c is None else delta_pp(c["phosphate"], p)
            rows.append({"electrolyte": "Nd2O3@LPSCl1.6 (Li5.44Nd0.02P0.98S4.37O0.03Cl1.6)", "cathode": cat,
                         "voltage_V": v,
                         "TM_to_phosphate_frac": "" if c is None else round(c["phosphate"], 4),
                         "TM_to_sulfide_frac": "" if c is None else round(c["sulfide"], 4),
                         "TM_to_other_frac": "" if c is None else round(c["other"], 4),
                         "TM_to_phosphate_frac_noNd_Li_matched": "" if (p is None or p["ctrl"] is None) else round(p["ctrl"], 4),
                         "delta_TM_phosphate_pp": "" if dp is None else round(dp, 2),
                         "Nd_phase": "" if (p is None or c is None) else p["phase"],
                         "comparable": "" if p is None else p["gate"],
                         "note": ("not drawn: electrolyte self-decomposition" if c is None else
                                  ("" if dp is not None else f"no delta: comparability gate failed ({p['why'] if p else 'no control'})"))})
    with OUT_ND_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    C_PHOS, C_SULF, C_OTH = ELEM["P"], ELEM["S"], "#d1d5db"
    fig, axes = plt.subplots(1, 4, figsize=(13.2, 4.2), sharey=True)
    for ax, cat in zip(axes, CATHODES):
        ax.axvline(2.5, color=MUT, ls=":", lw=1.0, zorder=1)
        for i, v in enumerate(VOLTS):
            c, p = tn.get((ND, cat, v)), pr.get((cat, v, 0.02))
            if c is None:
                ax.text(i, 50, "n/a", ha="center", va="center", fontsize=9, color=MUT, rotation=90)
                continue
            ph, su, ot = 100 * c["phosphate"], 100 * c["sulfide"], 100 * c["other"]
            ax.bar(i, ph, color=C_PHOS, width=0.72, zorder=2)
            ax.bar(i, su, bottom=ph, color=C_SULF, width=0.72, alpha=0.55, zorder=2)
            ax.bar(i, ot, bottom=ph + su, color=C_OTH, width=0.72, zorder=2)
            if ph >= 1:
                inside = ph > 12
                ax.text(i, 2.0 if inside else ph + 1.5, f"{ph:.0f}", ha="center", va="bottom",
                        fontsize=8.5, fontweight="bold", color="white" if inside else C_PHOS, zorder=4)
            dp = delta_pp(c["phosphate"], p)
            if p is not None and p["ctrl"] is not None and p["gate"]:
                ax.plot(i, 100 * p["ctrl"], ls="none", marker="D", ms=5.5, mfc=INK, mec="white", mew=0.8, zorder=5)
            if dp is not None and abs(dp) >= 0.05:
                ax.text(i, max(ph, 100 * p["ctrl"]) + 4, f"{dp:+.1f}", ha="center", va="bottom",
                        fontsize=8.3, color=INK, fontweight="bold", zorder=6,
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
            elif p is not None and not p["gate"]:
                ax.text(i, 60, "not comparable", ha="center", va="center", fontsize=7.5, color=INK,
                        rotation=90, zorder=6)
            if p is not None and p["phase"]:
                ax.text(i, 98.5, p["phase"].replace("(PO3)", "(PO$_3$)").replace("PO4", "PO$_4$")
                        .replace("P5O14", "P$_5$O$_{14}$").replace("(PO$_3$)4", "(PO$_3$)$_4$")
                        .replace("(PO$_3$)3", "(PO$_3$)$_3$"),
                        ha="center", va="top", rotation=90, fontsize=7.2, color="white", zorder=6)
        ax.set_xticks(range(len(VOLTS)), [f"{v:g}" for v in VOLTS])
        ax.set_ylim(0, 100); ax.set_xlim(-0.6, len(VOLTS) - 0.4)
        apply_axes(ax, xlabel="Applied voltage (V vs. Li/Li$^+$)", title=CAT_LABEL[cat], fontsize=11)
    apply_axes(axes[0], ylabel="Reacted cathode TM (%)", fontsize=11)
    handles = [Patch(color=C_PHOS, label="TM phosphate"),
               Patch(color=C_SULF, alpha=0.55, label="TM sulfide"),
               Patch(color=C_OTH, label="TM chloride / sulfate"),
               Line2D([], [], ls="none", marker="D", mfc=INK, mec="white", label="TM phosphate, no Nd (Li-matched)")]
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.legend(handles=handles, loc="upper center", ncol=4, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, 0.93), labelcolor=INK)
    fig.suptitle("Nd$_2$O$_3$@LPSCl1.6  (Li$_{5.44}$Nd$_{0.02}$P$_{0.98}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$, Nd on the P site)",
                 y=0.99, fontsize=11.5, color=INK)
    fig.text(0.5, -0.05,
             "Bars: where the reacted cathode TM ends up with Nd$_2$O$_3$@LPSCl1.6. Diamond: same quantity for the Li-matched "
             "Nd-free control. Bold number: change in the TM-phosphate share (percentage points, Nd minus control).\n"
             "White text: Nd phase the hull selects. Minimum-energy reaction, 0 K grand-potential hull (MP GGA/GGA+U). "
             "TM kept out of phosphate mostly goes to sulfide; this is a product channel, not a degradation rate.",
             ha="center", va="top", fontsize=8.1, color=MUT)
    fig.savefig(OUT_ND_PNG, dpi=300, bbox_inches="tight"); plt.close(fig)

    # ── 농도 판 (4.3 V) ──
    t0 = tn  # x = 0 끝 = o_only_003 (같은 스캔)
    drows = []
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for cat in DOSE_CATS:
        col = CAT_COLOR[cat]
        x0 = t0.get((ND_X0, cat, DOSE_V))
        xs_nd, ys_nd, xs_c, ys_c = [], [], [], []
        if x0 is not None:
            xs_nd.append(0.0); ys_nd.append(100 * x0["phosphate"]); xs_c.append(0.0); ys_c.append(100 * x0["phosphate"])
        for x in (0.02, 0.05, 0.10, 0.15, 0.20):
            p = pr.get((cat, DOSE_V, x))
            if p is None:
                continue
            if p["gate"] and p["nd"] is not None:
                xs_nd.append(x); ys_nd.append(100 * p["nd"])
            if p["gate"] and p["ctrl"] is not None:
                xs_c.append(x); ys_c.append(100 * p["ctrl"])
            drows.append({"cathode": cat, "voltage_V": DOSE_V, "x_Nd": x,
                          "TM_phosphate_frac_Nd": "" if (p["nd"] is None or not p["gate"]) else round(p["nd"], 4),
                          "TM_phosphate_frac_noNd_Li_matched": "" if (p["ctrl"] is None or not p["gate"]) else round(p["ctrl"], 4),
                          "Nd_phase": p["phase"], "comparable": p["gate"],
                          "note": "" if p["gate"] else f"not drawn: comparability gate failed ({p['why']})"})
        if x0 is not None:
            drows.insert(len(drows) - 5 if len(drows) >= 5 else 0,
                         {"cathode": cat, "voltage_V": DOSE_V, "x_Nd": 0.0,
                          "TM_phosphate_frac_Nd": round(x0["phosphate"], 4),
                          "TM_phosphate_frac_noNd_Li_matched": round(x0["phosphate"], 4),
                          "Nd_phase": "", "comparable": True, "note": "x = 0 end of the family (Li5.4PS4.37O0.03Cl1.6)"})
        ax.plot(xs_c, ys_c, ls="--", lw=1.3, color=col, marker="o", ms=5, mfc="white", mec=col, zorder=2)
        ax.plot(xs_nd, ys_nd, ls="-", lw=2.2, color=col, marker="o", ms=6, mfc=col, mec="white", zorder=3)
        ax.text(xs_nd[-1] + 0.004, ys_nd[-1] + (0.9 if cat == "LiCoO2" else -0.9 if cat == "NMC811" else 0),
                CAT_LABEL[cat], color=col, fontsize=9.5, va="center")
    ax.axvline(0.02, color=MUT, ls=":", lw=1.1)
    ax.text(0.021, 31.5, "target x = 0.02", color=MUT, fontsize=8.5, va="top")
    ax.axhline(10, color=MUT, lw=0.8, ls=(0, (1, 3)))
    ax.text(0.205, 10.8, "NMC811 Mn floor (10 %)", color=MUT, fontsize=8, ha="right", va="bottom")
    ax.set_xlim(-0.005, 0.235); ax.set_ylim(0, 32)
    apply_axes(ax, xlabel="Nd content x  (Li$_{5.4+2x}$Nd$_x$P$_{1-x}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$)",
               ylabel="Reacted cathode TM to phosphate (%)", fontsize=10.5)
    ax.set_title(f"How much Nd lowers the TM-phosphate share ({DOSE_V:g} V)", fontsize=11, color=INK)
    ax.legend(handles=[Line2D([], [], color=INK, lw=2.2, marker="o", mfc=INK, label="with Nd"),
                       Line2D([], [], color=INK, lw=1.3, ls="--", marker="o", mfc="white", label="no Nd, Li-matched")],
              frameon=False, fontsize=8.8, loc="lower left")
    fig.text(0.5, -0.02, "LiNiO$_2$ x = 0.20 failed the comparability gate and is not drawn. LiMnO$_2$ at 4.3 V fails at every x.\n"
             "TM kept out of phosphate mostly goes to sulfide (CoS$_2$, NiS$_2$). 0 K grand-potential hull, minimum-energy reaction.",
             ha="center", va="top", fontsize=7.8, color=MUT)
    fig.tight_layout()
    fig.savefig(OUT_DOSE_PNG, dpi=300, bbox_inches="tight"); plt.close(fig)
    with OUT_DOSE_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(drows[0])); w.writeheader(); w.writerows(drows)
    for pth in (OUT_ND_PNG, OUT_ND_CSV, OUT_DOSE_PNG, OUT_DOSE_CSV):
        print(f"→ {pth.relative_to(REPO)}")
    return 0


OUT_SIMPLE_PNG = REPO / "db/properties/cei_figs/cei_tm_fate_simple_4p3V.png"
OUT_SIMPLE_CSV = REPO / "db/properties/cei_figs/cei_tm_fate_simple_4p3V.csv"


FULL_JSONL = REPO / "db/properties/cei_protection_full.jsonl"
OUT_NCM_PNG = REPO / "db/properties/cei_figs/cei_tm_fate_nmc811_by_metal.png"
OUT_NCM_CSV = REPO / "db/properties/cei_figs/cei_tm_fate_nmc811_by_metal.csv"
NCM_CASES = [("liMatch002", "No Nd"), ("ndP002", "Nd$_2$O$_3$ (x = 0.02)")]
METALS = ["Ni", "Co", "Mn"]


def metal_fate(rxn, metals=METALS):
    """반응식 하나 → 금속별 {phosphate, sulfide, other} 몫 (그 금속의 좌변 양 기준).
    한 산물에 금속이 둘이면(Co(NiS2)2) **각자 따로** 센다. 좌변에 그 금속이 없으면 None."""
    sys.path.insert(0, str(REPO / "tools/oxidation"))
    import re as _re
    import interface_reactivity_v2 as IR
    lhs, rhs = rxn.split("->", 1)
    term = _re.compile(r"^\s*([0-9]*\.?[0-9]+)?\s*([A-Za-z0-9().]+)\s*$")
    tot = {m: 0.0 for m in metals}
    for t in lhs.split("+"):
        mm = term.match(t)
        if mm:
            n = float(mm.group(1)) if mm.group(1) else 1.0
            c = IR.parse_formula(mm.group(2))
            for m in metals:
                tot[m] += n * c.get(m, 0.0)
    bins = {m: {"phosphate": 0.0, "sulfide": 0.0, "other": 0.0} for m in metals}
    phases = {m: [] for m in metals}
    for t in rhs.split("+"):
        mm = term.match(t)
        if not mm:
            continue
        n = float(mm.group(1)) if mm.group(1) else 1.0
        f = mm.group(2); c = IR.parse_formula(f)
        k = "phosphate" if c.get("P", 0) > 0 else "sulfide" if c.get("S", 0) > 0 else "other"
        for m in metals:
            if c.get(m, 0) > 0:
                bins[m][k] += n * c[m]
                if k == "phosphate":
                    phases[m].append(f)
    out = {}
    for m in metals:
        if tot[m] <= 0:
            out[m] = None
            continue
        sh = {k: v / tot[m] for k, v in bins[m].items()}
        if abs(sum(sh.values()) - 1.0) > 0.01:
            raise ValueError(f"{m} 장부가 안 맞는다 ({sum(sh.values()):.4f}): {rxn}")
        out[m] = dict(sh, phases=phases[m])
    return out


def ncm_table(path=FULL_JSONL):
    t = {}
    for l in open(path):
        d = json.loads(l)
        if d["cathode"] != "NMC811" or d["species"] not in dict(NCM_CASES):
            continue
        for V, r in d["by_voltage"].items():
            t[(d["species"], float(V))] = metal_fate(r["reaction"])
    return t


def main_ncm():
    """NMC811 만 (2026-10-06 · 사용자 "ncm만 해봐" · 앞 그림들이 이해가 안 된다는 말 뒤).
    금속별 인산염 % 를 숫자 표로 — Mn 은 늘 인산염 · Co 는 늘 황화물 · Ni 만 갈린다."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    sys.path.insert(0, str(REPO / "tools/figures"))
    from house_style import INK, MUT, ELEM, apply_axes
    t = ncm_table()
    rows_lab, mat, rows_csv = [], [], []
    for m in METALS:
        for sp, lab in NCM_CASES:
            rows_lab.append((m, lab))
            line = []
            for v in VOLTS:
                f = t.get((sp, v), {}).get(m)
                line.append(None if f is None else 100 * f["phosphate"])
                rows_csv.append({"metal": m, "case": "no Nd (Li-matched control)" if sp == "liMatch002" else "Nd2O3@LPSCl1.6 x=0.02",
                                 "voltage_V": v,
                                 "to_phosphate_pct": "" if f is None else round(100 * f["phosphate"], 2),
                                 "to_sulfide_pct": "" if f is None else round(100 * f["sulfide"], 2),
                                 "to_other_pct": "" if f is None else round(100 * f["other"], 2),
                                 "phosphate_phase": "" if f is None else " ".join(f["phases"])})
            mat.append(line)
    cmap = LinearSegmentedColormap.from_list("w2p", ["#ffffff", ELEM["P"]])
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    import numpy as np
    arr = np.array([[np.nan if x is None else x for x in r] for r in mat])
    ax.imshow(arr, cmap=cmap, vmin=0, vmax=100, aspect="auto")
    for i, r in enumerate(mat):
        for j, x in enumerate(r):
            if x is None:
                ax.text(j, i, "n/a", ha="center", va="center", fontsize=9, color=MUT); continue
            ax.text(j, i, f"{x:.0f}%", ha="center", va="center", fontsize=11,
                    fontweight="bold" if rows_lab[i][0] == "Ni" else "normal",
                    color="white" if x > 55 else INK)
    ax.set_xticks(range(len(VOLTS)), [f"{v:g} V" for v in VOLTS], fontsize=10)
    ax.set_yticks(range(len(rows_lab)), [f"{m}  |  {lab}" for m, lab in rows_lab], fontsize=10)
    for y in (1.5, 3.5):
        ax.axhline(y, color=INK, lw=1.2)
    ax.set_xticks(np.arange(-0.5, len(VOLTS)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows_lab)), minor=True)
    ax.grid(which="minor", color="white", lw=1.5); ax.tick_params(which="minor", length=0)
    ax.tick_params(colors=INK, length=0)
    for sp_ in ax.spines.values():
        sp_.set_visible(False)
    ax.set_title("NMC811 | electrolyte: how much of each metal becomes a phosphate",
                 fontsize=11.5, color=INK, pad=10)
    fig.text(0.5, -0.02,
             "Numbers: share of that metal (Ni, Co or Mn from NMC811) that ends up as a metal phosphate in the most favorable "
             "NMC811 | electrolyte reaction.\nThe rest becomes metal sulfide (NiS$_2$, Ni$_3$S$_4$, CoS$_2$); at 3.5 V part of Ni "
             "becomes NiCl$_2$. Mn: LiMnPO$_4$, Mn(PO$_3$)$_2$, MnP$_4$O$_{11}$. Ni: Ni(PO$_3$)$_2$, NiP$_4$O$_{11}$.\n"
             "No Nd = Li-matched Nd-free control (Li$_{5.44}$P$_{0.98}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$). "
             "0 K grand-potential hull (MP GGA/GGA+U); a product channel, not a degradation rate.",
             ha="center", va="top", fontsize=8.0, color=MUT)
    fig.tight_layout()
    fig.savefig(OUT_NCM_PNG, dpi=300, bbox_inches="tight"); plt.close(fig)
    with OUT_NCM_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_csv[0])); w.writeheader(); w.writerows(rows_csv)
    print(f"→ {OUT_NCM_PNG.relative_to(REPO)}\n→ {OUT_NCM_CSV.relative_to(REPO)}")
    return 0


def main_simple():
    """한 장 요약 (2026-10-06 · 사용자 "그림이 전혀 이해가 안돼").
    4.3 V · LiCoO2 · LiNiO2 · NMC811 에서 '양극 금속 중 인산염이 되는 몫' 막대 셋:
      Nd 없음 (같은 계열 x → 0 끝 o_only_003 ≈ LPSCl1.6) · Nd₂O₃ x = 0.02 (1저자 조성) · x = 0.10 (참고 · 만든 적 없음).
    ⚠ Δ 의 정본은 --nd 판(Li 맞춘 대조군 기준)이다. 여기 'Nd 없음' 막대와 Li 맞춘 대조군의 차이는
      x = 0.02 에서 ≤ 0.3 %p · x = 0.10 에서 ≤ 1.6 %p (CSV 에 둘 다 싣는다)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(REPO / "tools/figures"))
    from house_style import INK, MUT, ELEM, apply_axes
    tn, pr = x002_fate(), prot_rows()
    groups = [("No Nd\n(LPSCl1.6)", None, "#9ca3af"),
              ("Nd$_2$O$_3$, x = 0.02\n(target composition)", 0.02, ELEM["P"]),
              ("Nd$_2$O$_3$, x = 0.10\n(reference only)", 0.10, "#c4b5fd")]
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    w = 0.26
    rows = []
    for j, cat in enumerate(DOSE_CATS):
        for k, (lab, x, col) in enumerate(groups):
            if x is None:
                c = tn.get((ND_X0, cat, DOSE_V)); val = None if c is None else 100 * c["phosphate"]; ctrl = val
            else:
                p = pr.get((cat, DOSE_V, x)); ok = p is not None and p["gate"]
                val = 100 * p["nd"] if ok and p["nd"] is not None else None
                ctrl = 100 * p["ctrl"] if ok and p["ctrl"] is not None else None
            xpos = j + (k - 1) * w
            if val is None:
                ax.text(xpos, 1, "n/a", ha="center", va="bottom", fontsize=8, color=MUT)
            else:
                ax.bar(xpos, val, width=w * 0.92, color=col, zorder=2,
                       label=lab if j == 0 else None)
                ax.text(xpos, val + 0.6, f"{val:.0f}%", ha="center", va="bottom", fontsize=9.5,
                        color=INK, fontweight="bold" if x == 0.02 else "normal")
            rows.append({"cathode": cat, "voltage_V": DOSE_V,
                         "case": "no Nd (x->0 end, Li5.4PS4.37O0.03Cl1.6)" if x is None else f"Nd2O3 x={x}",
                         "TM_to_phosphate_pct": "" if val is None else round(val, 2),
                         "Li_matched_noNd_control_pct": "" if ctrl is None else round(ctrl, 2)})
    ax.set_xticks(range(len(DOSE_CATS)), [CAT_LABEL[c] for c in DOSE_CATS], fontsize=11)
    ax.set_ylim(0, 38)
    apply_axes(ax, ylabel="Cathode metal that becomes phosphate (%)", fontsize=11)
    ax.set_title("At 4.3 V: Nd takes phosphorus, so less cathode metal ends up as phosphate",
                 fontsize=11, color=INK)
    ax.legend(frameon=False, fontsize=9, loc="upper right", ncol=1, handlelength=1.2)
    fig.text(0.5, -0.03, "Of the cathode metal (Co, Ni) that reacts with the electrolyte, the share that ends up as a "
             "metal phosphate (CoP$_4$O$_{11}$, Ni(PO$_3$)$_2$).\nThe rest becomes metal sulfide (CoS$_2$, NiS$_2$). "
             "0 K thermodynamics of the most favorable cathode | electrolyte reaction; not a degradation rate.",
             ha="center", va="top", fontsize=8.3, color=MUT)
    fig.tight_layout()
    fig.savefig(OUT_SIMPLE_PNG, dpi=300, bbox_inches="tight"); plt.close(fig)
    with OUT_SIMPLE_CSV.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    print(f"→ {OUT_SIMPLE_PNG.relative_to(REPO)}\n→ {OUT_SIMPLE_CSV.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    if "--ncm" in sys.argv:
        raise SystemExit(main_ncm())
    if "--simple" in sys.argv:
        raise SystemExit(main_simple())
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    raise SystemExit(main_nd() if "--nd" in sys.argv else main())
