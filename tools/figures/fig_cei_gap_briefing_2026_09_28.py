#!/usr/bin/env python3
"""fig_cei_gap_briefing_2026_09_28.py — 판별종 밴드갭 10/10 브리핑 1장 (슬라이드용).

  (a) Ours vs MP — 10 종. 9 종은 ±0.12 eV 띠 안, NdP₅O₁₄ 한 종만 −0.943 eV.
  (b) 부피 가설 반증 — ΔV(%) vs Δgap(eV). P₂O₅ 가 +9.42 % 팽창하고도 −0.016 eV 로 맞는다.
  (c) 결론 — 10 종 전부 넓은 갭. §C 가 묻는 것은 "전자를 흘리나" 이다.

  값은 전부 `db/properties/cei_gap_results_2026_09_19.json` 에서 읽는다.

    python3 tools/figures/fig_cei_gap_briefing_2026_09_28.py
    python3 tools/figures/fig_cei_gap_briefing_2026_09_28.py --selftest

이 도구가 **못 하는 것**
  · 갭을 계산하지 않는다 — 기록을 읽어 그린다. 행 수가 10 이 아니면 **죽는다**.
  · PBE 갭이다. 실험값이 아니고 MP 도 PBE(+U) 다 — 절대값 주장에 쓰지 않는다.
  · 미재현 1 종의 **원인을 말하지 않는다** (미확정). 인용위험 CONDITIONAL 로 묶여 있다.
  · "절연체" 는 **갭이 열려 있다**는 뜻이고, 실제 계면층의 연속성·두께·전자수송은 안 쟀다.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from house_style import INK, MUT, apply_axes  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "db/properties/cei_gap_results_2026_09_19.json"
OUT = REPO / "db/properties/cei_figs"

OKC, BADC = "#0d9488", "#be123c"
TEX = {"NdPS4": "NdPS$_4$", "Nd2O3": "Nd$_2$O$_3$", "Nd3PO7": "Nd$_3$PO$_7$",
       "NdCl3": "NdCl$_3$", "P2O5": "P$_2$O$_5$", "Nd2(SO4)3": "Nd$_2$(SO$_4$)$_3$",
       "Nd(PO3)3": "Nd(PO$_3$)$_3$", "NdPO4": "NdPO$_4$",
       "LiNd(PO3)4": "LiNd(PO$_3$)$_4$", "NdP5O14": "NdP$_5$O$_{14}$"}


def load():
    d = json.loads(SRC.read_text("utf-8"))
    rows = d["rows"]
    if len(rows) != 10:
        raise SystemExit(f"⛔ 기록 행이 {len(rows)} 개다 — 10/10 그림을 그릴 수 없다")
    agg = d["집계"]
    miss = d["⛔_NdP5O14_미재현"]
    vol = miss["⛔_반증된_가설_부피"]["ΔV_대_Δ갭"]   # 부피 절은 미재현 절 **안**에 있다
    if len(vol) != len(rows):
        raise SystemExit(f"⛔ ΔV 표가 {len(vol)} 행 · 갭 표가 {len(rows)} 행 — 짝이 안 맞는다")
    return rows, agg, vol, miss


def _tex(p):
    if p not in TEX:
        raise SystemExit(f"⛔ 라벨을 모르는 상: {p!r} — TEX 에 추가해라")
    return TEX[p]


def panel_a(ax, rows, agg):
    band = agg["재현_9종"]["max_abs_diff_eV"]
    lo, hi = 1.8, 6.7
    ax.plot([lo, hi], [lo, hi], "-", color=MUT, lw=1.0, zorder=1)
    ax.fill_between([lo, hi], [lo - band, hi - band], [lo + band, hi + band],
                    color=OKC, alpha=.12, zorder=0)
    for r in rows:
        bad = abs(r["diff_eV"]) > band + 1e-9
        ax.plot(r["mp_ref_eV"], r["gap_eV"], "o", ms=7,
                color=BADC if bad else OKC, mec="white", mew=1.0, zorder=3)
        if bad:
            ax.annotate(f"{_tex(r['phase'])}\n{r['diff_eV']:+.2f} eV",
                        xy=(r["mp_ref_eV"], r["gap_eV"]), xytext=(-14, -44),
                        textcoords="offset points", fontsize=9, color=BADC,
                        ha="center", linespacing=1.3,
                        arrowprops=dict(arrowstyle="->", color=BADC, lw=1.0))
    ax.text(2.1, 6.2, f"9 of 10 within $\\pm${band:.2f} eV", fontsize=9.2, color=OKC)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    apply_axes(ax, "Materials Project reference (eV)", "This work, PBE (eV)",
               "(a)  10 discriminating phases, gaps reproduced")


def panel_b(ax, vol):
    for v in vol:
        bad = abs(v["dgap_eV"]) > 0.5
        ax.plot(v["dV_pct"], v["dgap_eV"], "o", ms=7,
                color=BADC if bad else OKC, mec="white", mew=1.0, zorder=3)
    big = max(vol, key=lambda v: v["dV_pct"])
    ax.annotate(f"{_tex(big['phase'])}: +{big['dV_pct']:.1f} % volume,\n"
                f"gap off by {big['dgap_eV']:+.3f} eV",
                xy=(big["dV_pct"], big["dgap_eV"]), xytext=(-12, -62),
                textcoords="offset points", fontsize=9, color=OKC, ha="right",
                linespacing=1.3, arrowprops=dict(arrowstyle="->", color=OKC, lw=1.0))
    out = min(vol, key=lambda v: v["dgap_eV"])
    ax.annotate(_tex(out["phase"]), xy=(out["dV_pct"], out["dgap_eV"]),
                xytext=(26, 8), textcoords="offset points", fontsize=9, color=BADC,
                arrowprops=dict(arrowstyle="->", color=BADC, lw=1.0))
    ax.axhline(0, color=MUT, lw=.8, ls=":", zorder=0)
    apply_axes(ax, "Cell volume vs MP (%)", "Gap difference (eV)",
               "(b)  The volume explanation is refuted")


def panel_c(ax, rows):
    rs = sorted(rows, key=lambda r: r["gap_eV"])
    ys = range(len(rs))
    ax.barh(list(ys), [r["gap_eV"] for r in rs],
            color=[BADC if abs(r["diff_eV"]) > .5 else OKC for r in rs], height=.62)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([_tex(r["phase"]) for r in rs], fontsize=8.8)
    lo = min(r["gap_eV"] for r in rs)
    ax.set_xlim(0, max(r["gap_eV"] for r in rs) * 1.18)
    ax.text(max(r["gap_eV"] for r in rs) * .52, 0.55,
            f"all 10 gaps $\\geq$ {lo:.2f} eV", fontsize=9.6, color=INK)
    apply_axes(ax, "Band gap, PBE (eV)", None,
               "(c)  Every product phase is a wide-gap insulator")


def build(out=None):
    rows, agg, vol, _ = load()
    fig, axs = plt.subplots(1, 3, figsize=(14.4, 4.2),
                            gridspec_kw={"width_ratios": [1.05, 1.0, 1.05]})
    panel_a(axs[0], rows, agg); panel_b(axs[1], vol); panel_c(axs[2], rows)
    fig.tight_layout()
    p = pathlib.Path(out) if out else OUT / "cei_gap_briefing_2026_09_28.png"
    fig.savefig(p, dpi=300, bbox_inches="tight"); plt.close(fig)
    return p


def write_csv(out=None):
    rows, _, vol, _ = load()
    dv = {v["phase"]: v["dV_pct"] for v in vol}
    p = pathlib.Path(out) if out else OUT / "cei_gap_briefing_origin_2026_09_28.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["phase", "spacegroup", "gap_ours_eV", "gap_mp_eV",
                    "diff_eV", "diff_pct", "dV_vs_mp_pct"])
        for r in sorted(rows, key=lambda r: r["gap_eV"]):
            w.writerow([r["phase"], r["spacegroup"], r["gap_eV"], r["mp_ref_eV"],
                        r["diff_eV"], r["diff_pct"], dv.get(r["phase"], "")])
    return p


def _selftest():
    import shutil, tempfile
    ok = True
    td = tempfile.mkdtemp(prefix="gapbrief_")

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    try:
        rows, agg, vol, miss = load()
        chk(len(rows) == 10, "[양성] 10 종")
        bad = [r for r in rows if abs(r["diff_eV"]) > agg["재현_9종"]["max_abs_diff_eV"]]
        chk(len(bad) == 1 and bad[0]["phase"] == "NdP5O14",
            f"[양성] 띠 밖은 {len(bad)} 종 · {bad[0]['phase'] if bad else '—'}")
        chk(abs(bad[0]["diff_eV"] - agg["미재현_1종"]["diff_eV"]) < 1e-9,
            "[양성] 미재현 값이 집계와 같다")
        chk(min(r["gap_eV"] for r in rows) > 2.0,
            "[양성] 최소 갭이 2 eV 를 넘는다 (전부 절연체)")
        p2 = [v for v in vol if v["phase"] == "P2O5"][0]
        chk(p2["dV_pct"] > 9 and abs(p2["dgap_eV"]) < .05,
            "[양성] P2O5 가 +9 % 팽창에도 갭이 맞는다 — 부피 가설 반증의 핵심")
        f = pathlib.Path(build(out=f"{td}/g.png"))
        chk(f.exists() and f.stat().st_size > 40000, "[양성] 그림이 그려진다")
        c = pathlib.Path(write_csv(out=f"{td}/g.csv"))
        chk(len(c.read_text("utf-8").splitlines()) == 11, "[양성] CSV 머리 1 + 10 행")
        # ⛔음성 — 모르는 상 라벨은 빈칸으로 그리지 않고 죽는다
        died = False
        try:
            _tex("NdXyz9")
        except SystemExit as e:
            died = "라벨을 모르는" in str(e)
        chk(died, "[⛔음성] 모르는 상은 빈 라벨로 그리지 않고 죽는다")
        # ⛔음성 — 행 수가 10 이 아니면 죽는다 (9/10 을 10/10 으로 안 그린다)
        import unittest.mock as _m
        short = json.loads(SRC.read_text("utf-8")); short["rows"] = short["rows"][:9]
        died2 = False
        with _m.patch.object(pathlib.Path, "read_text",
                             lambda self, *a, **k: json.dumps(short)):
            try:
                load()
            except SystemExit as e:
                died2 = "10/10" in str(e)
        chk(died2, "[⛔음성] 9 행이면 10/10 그림을 그리지 않는다")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    print(f"✓ {build().relative_to(REPO)}")
    print(f"✓ {write_csv().relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
