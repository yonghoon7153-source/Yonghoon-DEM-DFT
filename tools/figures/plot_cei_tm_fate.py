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
  python3 tools/figures/plot_cei_tm_fate.py --selftest   # 음성 경로 포함
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


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
