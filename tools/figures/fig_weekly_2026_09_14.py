#!/usr/bin/env python3
"""fig_weekly_2026_09_14.py — 주간 정리(2026-09-08~14) 그림 2장 + Origin-ready CSV.

  ① LPSOCl 3×3×1 400 ps 아레니우스 — 자격 시드별 D + 온도별 평균 + 3점 무가중 ln D 적합.
     출처: db/properties/lpsocl_box331_c3_input_d_2026_09_11.json (시드 D) ·
           db/properties/lpsocl_box331_closed_2026_09_11.json (Ea · CI95 · 정의 · 세대).
  ② cascade §4b EOS 이력현상 — W3_f02 다섯 구조의 상승/하강 E(V) 두 갈래와 자격.
     출처: db/properties/cascade_pilot_diag10_raw/W3_f02__<구조>.postproc.json.

    python3 tools/figures/fig_weekly_2026_09_14.py            # 그림 2장 + CSV 2벌
    python3 tools/figures/fig_weekly_2026_09_14.py --selftest # 양성 + 음성

이 도구가 **못 하는 것**
  · 값을 다시 판정하지 않는다 — Ea·CI95·자격·차단 사유는 원장에서 읽어 그대로 적는다.
    Ea 는 D 평균으로 재계산해 원장과 1 meV 안에서 맞는지 **확인만** 한다(틀리면 시작하지 않는다).
  · ② 는 citable 이 아니다 — 원장(cascade_pilot_4b_closed_2026_09_13.json)이 "물성값이 아니라
    준비 상태에 대한 사실" 이라 했다. 그림에도 그렇게 박는다.
  · 잣대 각주를 손으로 적지 않는다 — md_protocol_generations.json 의 `영문_각주` 가 단일 출처다.
  · 다른 주의 그림을 만들지 않는다 — 날짜가 파일명에 박힌 일회성 산출물이다 (seminar 세트와 같은 부류).
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

DB = R / "db/properties"
OUT = R / "docs/figures/weekly_2026_09_14"
RAW = DB / "cascade_pilot_diag10_raw"
KB_EV = 8.617333262e-5          # eV/K
TT = (600, 800, 1000)
STRUCTS = ("H0_host", "P1_Al2O3_A", "P1_Al2O3_B", "P2_Al2S3_A", "P2_Al2S3_B")
RUN_TAG = "W3_f02"


# ── ① 아레니우스 ─────────────────────────────────────────────────────────
def load_arrhenius(seed_path=DB / "lpsocl_box331_c3_input_d_2026_09_11.json",
                   closed_path=DB / "lpsocl_box331_closed_2026_09_11.json") -> dict:
    """원장 두 개 → {T: {seed: D}} · 평균 · Ea(원장) · CI95 · 세대 각주.

    ⛔ 시드 D 가 null 이면 **빼고** 평균한다(원장 규칙: no_value 시드는 자격 없음).
       세 온도 중 하나라도 자격 시드가 없으면 ValueError — 3점 적합이 정의되지 않는다.
    """
    seeds = json.loads(pathlib.Path(seed_path).read_text(encoding="utf-8"))
    closed = json.loads(pathlib.Path(closed_path).read_text(encoding="utf-8"))
    per_t = {}
    for T in TT:
        row = seeds.get(str(T))
        if not isinstance(row, dict):
            raise ValueError(f"시드 D 원장에 {T} K 가 없다")
        ok = {s: float(v) for s, v in row.items() if v is not None}
        if not ok:
            raise ValueError(f"{T} K 에 자격 시드가 하나도 없다 — 3점 적합 불가")
        per_t[T] = ok
    v = closed["확정값"]
    gens = json.loads((DB / "md_protocol_generations.json").read_text(encoding="utf-8"))["generations"]
    # ⚠ 원장의 `세대` 는 "gen2_400ps_4window — **이 세대의 첫 등록값**" 처럼 설명이 딸린다.
    #   id 토큰(첫 공백 전)만 대조한다 — 설명까지 같아야 한다고 읽으면 늘 못 찾는다.
    gen_id = str(v.get("세대") or "gen2_400ps_4window").split()[0]
    gen = next((g for g in gens if g["id"] == gen_id), None)
    if gen is None or not gen.get("영문_각주"):
        raise ValueError(f"세대 원장에 {gen_id} 의 영문 각주가 없다 — 손으로 적지 않는다")
    return {"per_t": per_t,
            "mean": {T: float(np.mean(list(per_t[T].values()))) for T in TT},
            "Ea_ledger": float(v["값_eV"]),
            "CI95": [float(x) for x in v["CI95_eV"]],
            "halfwidth": float(v["반폭_eV"]),
            "name": v["이름"], "gen_id": gen_id, "gen_note": gen["영문_각주"],
            "source": [str(pathlib.Path(seed_path).relative_to(R)),
                       str(pathlib.Path(closed_path).relative_to(R))]}


def ea_from_means(mean: dict) -> tuple[float, np.ndarray]:
    """온도별 평균 D 의 3점 무가중 ln D 적합 → (Ea eV, polyfit 계수 on x=1000/T)."""
    if set(mean) != set(TT):
        raise ValueError(f"세 온도가 전부 있어야 한다: {sorted(mean)}")
    x = np.array([1000.0 / T for T in TT])
    y = np.log(np.array([mean[T] for T in TT]))
    p = np.polyfit(x, y, 1)
    return float(-p[0] * KB_EV * 1000.0), p


def fig_arrhenius(a: dict, out_png=OUT / "lpsocl_box331_arrhenius.png",
                  out_csv=DB / "lpsocl_box331_arrhenius_origin_2026_09_14.csv") -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ea, p = ea_from_means(a["mean"])
    if abs(ea - a["Ea_ledger"]) > 1e-3:
        raise ValueError(f"재계산 Ea {ea:.4f} 가 원장 {a['Ea_ledger']:.4f} 와 1 meV 넘게 다르다 — 그리지 않는다")
    c = H.SYS["lpsocl"]
    x = np.array([1000.0 / T for T in TT])
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    for T in TT:
        xs = [1000.0 / T] * len(a["per_t"][T])
        ax.plot(xs, np.log(list(a["per_t"][T].values())), "o", ms=6, mfc="none", mec=c, mew=1.4,
                label="seed D (MTO, 2–50 ps, free intercept)" if T == TT[0] else None)
    ax.plot(x, np.log([a["mean"][T] for T in TT]), "o", ms=9, color=c,
            label="T-mean of eligible seeds (n = %s)" % "/".join(str(len(a["per_t"][T])) for T in TT))
    xf = np.linspace(x.min() - .05, x.max() + .05, 50)
    ax.plot(xf, np.polyval(p, xf), color=c, lw=1.7,
            label=f"3-point fit   $E_a$ = {a['Ea_ledger']:.3f} ± {a['halfwidth']:.3f} eV (cell-conditioned)")
    H.apply_axes(ax, xlabel="1000 / T  (K$^{-1}$)", ylabel=r"ln $D_{\rm Li}$  ($D$ in cm$^2$/s)")
    ax.set_title("Arrhenius — LPSOCl1.6 3×3×1, 400 ps (closed 2026-09-11)", fontsize=11.5, color=H.INK)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    sec = ax.secondary_xaxis("top", functions=(lambda v: 1000 / np.clip(v, 1e-9, None),
                                               lambda v: 1000 / np.clip(v, 1e-9, None)))
    sec.set_xlabel("T (K)", fontsize=10, color=H.MUT)
    sec.set_xticks(list(TT))
    ax.text(.02, .05, "± = CI95 half-width from seed resampling (2·3·3)\n"
                      "segment slopes 600–800 / 800–1000 K compatible within pre-sealed ±0.05 eV",
            transform=ax.transAxes, fontsize=8.5, color=H.MUT, va="bottom")
    fig.text(.5, .006, a["gen_note"], ha="center", fontsize=7.2, color=H.MUT, wrap=True)
    fig.tight_layout(rect=[0, .05, 1, 1])
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"# {a['name']} = {a['Ea_ledger']:.4f} eV, CI95 [{a['CI95'][0]:.4f}, {a['CI95'][1]:.4f}] (seed resampling)"])
        w.writerow(["# sources: " + " ; ".join(a["source"])])
        w.writerow(["# D per eligible seed (cm^2/s): MTO, window 2-50 ps, free intercept. null seed = no_value (excluded)."])
        w.writerow(["# fit_lnD = 3-point unweighted fit through ln(D_mean) vs 1000/T; Ea = -slope*kB*1000"])
        w.writerow([f"# PROTOCOL GENERATION: {a['gen_id']}. {a['gen_note']}"])
        seeds = sorted({s for T in TT for s in a["per_t"][T]})
        w.writerow(["T_K", "x_1000_over_T"] + [f"D_{s}_cm2_s" for s in seeds] + ["D_mean_cm2_s", "lnD_mean", "fit_lnD"])
        for T in TT:
            xx = 1000.0 / T
            w.writerow([T, f"{xx:.6f}"] + [a["per_t"][T].get(s, "") for s in seeds]
                       + [f"{a['mean'][T]:.4e}", f"{np.log(a['mean'][T]):.5f}", f"{np.polyval(p, xx):.5f}"])
    return {"png": str(out_png.relative_to(R)), "csv": str(out_csv.relative_to(R)), "Ea_recomputed": ea}


# ── ② EOS 이력현상 ──────────────────────────────────────────────────────
def load_branches(raw_dir=RAW, run_tag=RUN_TAG, structs=STRUCTS) -> list[dict]:
    """postproc → [{name, V, E_up, E_down, eligible, shape, span, pct, V0_up, V0_down, reason}].

    ⛔ 상승·하강·부피점 길이가 다르면 ValueError — 짝이 안 맞는 두 갈래는 이력현상이 아니다.
    """
    rows = []
    for s in structs:
        p = pathlib.Path(raw_dir) / f"{run_tag}__{s}.postproc.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        e, h = d["eos"], d["eos"]["hysteresis"]
        V, up, dn = e["V_points"], h["E_up"], h["E_down"]
        if not (len(V) == len(up) == len(dn)) or len(V) < 3:
            raise ValueError(f"{s}: 부피점 {len(V)} · 상승 {len(up)} · 하강 {len(dn)} — 짝이 안 맞는다")
        rows.append({"name": d["name"], "n_atoms": d["n_atoms"], "V": V, "E_up": up, "E_down": dn,
                     "eligible": bool(e["downstream_eligible"]),
                     "shape": float(h["shape_max_abs_dE_eV"]), "span": float(h["E_span_eV"]),
                     "pct": 100.0 * float(h["shape_over_span"]),
                     "V0_up": h.get("V0_up"), "V0_down": h.get("V0_down"),
                     "run_id": d["run_id"], "code_id": d["code_id"],
                     "reason": (e.get("fit_quality_reason") or "").split("·")[0].strip()})
    return rows


def fig_hysteresis(rows: list[dict], out_png=OUT / "cascade_4b_eos_hysteresis.png",
                   out_csv=DB / "cascade_pilot_4b_eos_hysteresis_origin_2026_09_14.csv") -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(rows), figsize=(3.3 * len(rows), 4.3), sharex=True)
    for ax, r in zip(np.atleast_1d(axes), rows):
        V = np.array(r["V"]); up = np.array(r["E_up"]); dn = np.array(r["E_down"])
        ref = up.min()
        ax.plot(V, up - ref, "o-", color=H.INK, ms=5, lw=1.5, label="up branch (increasing V)")
        ax.plot(V, dn - ref, "s--", color="#c05621", ms=5, lw=1.4, mfc="none", label="down branch (decreasing V)")
        ok = r["eligible"]
        verdict = "eligible" if ok else "blocked"
        H.apply_axes(ax, xlabel="V (Å$^3$)", ylabel="E − min E$_{up}$ (eV)" if r is rows[0] else None,
                     title=f"{r['name']}  [{verdict}]", fontsize=10)
        ax.title.set_color("#0d9488" if ok else "#be123c")
        ax.text(.03, .97, f"shape Δ {r['shape']:.3f} eV / span {r['span']:.2f} eV\n= {r['pct']:.0f} % (limit 10 %)",
                transform=ax.transAxes, fontsize=8, va="top", color=H.INK,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=.85))
    hnd, lab = np.atleast_1d(axes)[0].get_legend_handles_labels()
    fig.legend(hnd, lab, loc="upper center", bbox_to_anchor=(.5, .915), ncol=2, frameon=False, fontsize=8.5)
    fig.suptitle(f"EOS hysteresis check — {RUN_TAG} (7 points ±3 %, fixed shape, fmax 0.02 eV/Å): "
                 "ordered host passes, disordered doped structures fail", fontsize=11, color=H.INK)
    fig.text(.5, .01, "Diagnostic only (citable: false). Eligibility = postproc downstream_eligible; "
                      "reasons in db/properties/cascade_pilot_4b_closed_2026_09_13.json. "
                      "UMA-s-1p1 (omat), 204/208-atom 2×2×1 supercells.",
             ha="center", fontsize=7.6, color=H.MUT)
    fig.tight_layout(rect=[0, .04, 1, .90])
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"# cascade pilot section 4b — EOS up/down branches, run_tag {RUN_TAG}. DIAGNOSTIC ONLY, citable: false."])
        w.writerow(["# source: db/properties/cascade_pilot_diag10_raw/W3_f02__<structure>.postproc.json (V100, 2026-09-13)"])
        w.writerow(["# E_rel = E - min(E_up) per structure. eligible = downstream_eligible (fit quality + hysteresis gates)."])
        w.writerow(["# run_ids: " + " ; ".join(f"{r['name']}={r['run_id']}" for r in rows)])
        w.writerow(["structure", "n_atoms", "V_A3", "E_up_eV", "E_down_eV", "E_up_rel_eV", "E_down_rel_eV",
                    "shape_dE_eV", "E_span_eV", "shape_over_span_pct", "eligible"])
        for r in rows:
            ref = min(r["E_up"])
            for V, up, dn in zip(r["V"], r["E_up"], r["E_down"]):
                w.writerow([r["name"], r["n_atoms"], f"{V:.4f}", f"{up:.6f}", f"{dn:.6f}",
                            f"{up - ref:.6f}", f"{dn - ref:.6f}", f"{r['shape']:.4f}", f"{r['span']:.4f}",
                            f"{r['pct']:.1f}", int(r["eligible"])])
    return {"png": str(out_png.relative_to(R)), "csv": str(out_csv.relative_to(R)),
            "eligible": [r["name"] for r in rows if r["eligible"]]}


# ── selftest ────────────────────────────────────────────────────────────
def _selftest() -> int:
    import tempfile
    n = 0
    a = load_arrhenius()
    ea, _ = ea_from_means(a["mean"])
    assert abs(ea - a["Ea_ledger"]) < 1e-3, (ea, a["Ea_ledger"]); n += 1
    assert all(len(a["per_t"][T]) >= 2 for T in TT), a["per_t"]; n += 1
    rows = load_branches()
    assert [r["name"] for r in rows] == list(STRUCTS) and all(len(r["V"]) == 7 for r in rows); n += 1
    assert [r["name"] for r in rows if r["eligible"]] == ["H0_host"], "W3_f02 자격은 H0 하나여야 한다 (원장 1/5)"; n += 1
    # 음성 ① 온도 하나가 통째로 no_value 면 3점 적합이 정의되지 않는다
    with tempfile.TemporaryDirectory() as td:
        bad = json.loads((DB / "lpsocl_box331_c3_input_d_2026_09_11.json").read_text(encoding="utf-8"))
        bad["600"] = {"s2": None, "s3": None, "s4": None}
        pth = pathlib.Path(td) / "bad.json"; pth.write_text(json.dumps(bad), encoding="utf-8")
        try:
            load_arrhenius(seed_path=pth); raise AssertionError("자격 시드 0 인 온도를 통과시켰다")
        except ValueError:
            n += 1
        # 음성 ② 평균 D 를 살짝 바꾸면 원장 Ea 와 안 맞아 그리지 않는다
        b = dict(a); b["mean"] = dict(a["mean"]); b["mean"][1000] *= 1.5
        try:
            fig_arrhenius(b, out_png=pathlib.Path(td) / "x.png", out_csv=pathlib.Path(td) / "x.csv")
            raise AssertionError("원장과 어긋난 Ea 로 그림을 그렸다")
        except ValueError:
            n += 1
        # 음성 ③ 두 갈래 길이가 다르면 이력현상 그림을 만들지 않는다
        src = json.loads((RAW / f"{RUN_TAG}__H0_host.postproc.json").read_text(encoding="utf-8"))
        src["eos"]["hysteresis"]["E_down"] = src["eos"]["hysteresis"]["E_down"][:-1]
        (pathlib.Path(td) / f"{RUN_TAG}__H0_host.postproc.json").write_text(json.dumps(src), encoding="utf-8")
        try:
            load_branches(raw_dir=td, structs=("H0_host",)); raise AssertionError("짝 안 맞는 갈래를 통과시켰다")
        except ValueError:
            n += 1
        # 음성 ④ 세대 각주가 비어 있으면 손으로 메우지 않고 멈춘다
        cl = json.loads((DB / "lpsocl_box331_closed_2026_09_11.json").read_text(encoding="utf-8"))
        cl["확정값"]["세대"] = "gen1_traj_mto_200ps"      # 각주가 비어 있는 세대
        pc = pathlib.Path(td) / "closed.json"; pc.write_text(json.dumps(cl, ensure_ascii=False), encoding="utf-8")
        try:
            load_arrhenius(closed_path=pc); raise AssertionError("각주 없는 세대를 통과시켰다")
        except ValueError:
            n += 1
    print(f"selftest ok — {n} checks (양성 4 · 음성 4)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_selftest())
    a = load_arrhenius()
    r1 = fig_arrhenius(a)
    r2 = fig_hysteresis(load_branches())
    print(json.dumps({"arrhenius": r1, "hysteresis": r2}, ensure_ascii=False, indent=1))
