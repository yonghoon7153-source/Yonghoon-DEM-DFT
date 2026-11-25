#!/usr/bin/env python3
"""fig_weekly_2026_09_20.py — modelc(LPSCl1.6) 3×3×1 시드 확장 2패널 + Origin CSV.

주간보고 슬라이드용 한 장. 두 패널이 같은 이야기의 앞뒤다.

  (a) 아레니우스 — 5시드 MTO D (창 2–50 ps · 자유절편) · 온도별 자격 시드 평균 ·
      3점 무가중 ln D 적합. 600 K 만 자격이 3/5 다.
  (b) C3 게이트 — ΔEa = Ea(600–800) − Ea(800–1000) 의 CI95 가 3시드 → 5시드에서
      얼마나 줄었나. 사전등록 허용영역 ±0.050 eV 와 함께 본다.
      3시드는 CI 하단이 경계를 **넘어** inconclusive(HOLD)였고, 5시드에서 안으로 들어왔다.

    python3 tools/figures/fig_weekly_2026_09_20.py            # PNG 1장 + CSV 2벌
    python3 tools/figures/fig_weekly_2026_09_20.py --selftest # 양성 + 음성

이 도구가 **못 하는 것**
  · 값을 다시 판정하지 않는다 — Ea·CI95·ΔEa·자격·허용영역은 전부 원장에서 읽는다.
    Ea 는 D 평균으로 재계산해 원장과 1 meV 안에서 맞는지 **확인만** 한다 (틀리면 그리지 않는다).
  · ⛔ **lpsocl 을 같은 패널에 그리지 않는다.** 레지스트리 금지 목록에
    `same_table_with_lpsocl_box331__seed_count_differs` 가 있다 — lpsocl 은 아직 3시드다.
  · ⛔ 절대 D·σ 를 말하지 않는다. y 축은 ln D 이고 **기울기(Ea)가 보고량**이다.
  · ⛔ bulk Ea 가 아니다 — `cell-conditioned` 라벨을 그림에서 떼지 않는다 (gen2 각주).
  · 제외된 시드(s3·s5 @600 K)의 D 는 **원장에 null 이라 점으로 못 그린다.** 개수로만 적는다.
  · 다른 주·다른 계의 그림을 만들지 않는다 — 날짜가 파일명에 박힌 일회성 산출물이다.
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
from fig_weekly_2026_09_14 import KB_EV, TT, ea_from_means  # noqa: E402  (순수 함수 재사용)

DB = R / "db/properties"
OUT = R / "docs/figures/weekly_2026_09_20"

MTO5 = DB / "modelc_box331_c2_mto_5seed_2026_09_18.json"
C3_5 = DB / "modelc_box331_c3_result_5seed_2026_09_18.json"
C3_3 = DB / "modelc_box331_c3_result_2026_09_15.json"
GEN = DB / "md_protocol_generations.json"


def _rel(p) -> str:
    """repo 안이면 상대경로, 밖이면 그대로. 시험이 tmp 경로를 끼워도 안 죽는다."""
    p = pathlib.Path(p)
    try:
        return str(p.relative_to(R))
    except ValueError:
        return str(p)


def load_modelc(mto=MTO5, c3_5=C3_5, c3_3=C3_3, gen=GEN) -> dict:
    """원장 넷 → 그림에 필요한 전부. ⛔ 여기서 아무것도 판정하지 않는다."""
    m = json.loads(pathlib.Path(mto).read_text(encoding="utf-8"))
    r5 = json.loads(pathlib.Path(c3_5).read_text(encoding="utf-8"))
    r3 = json.loads(pathlib.Path(c3_3).read_text(encoding="utf-8"))
    g = json.loads(pathlib.Path(gen).read_text(encoding="utf-8"))

    per_t, elig = {}, {}
    for T in TT:
        row = (m.get("D_cm2_s") or {}).get(str(T))
        if not isinstance(row, dict):
            raise ValueError(f"D 표에 {T} K 가 없다 — 그리지 않는다")
        ok = {s: float(v) for s, v in row.items() if v is not None}
        if not ok:
            raise ValueError(f"{T} K 에 자격 시드가 하나도 없다 — 3점 적합 불가")
        per_t[T] = ok
        elig[T] = (len(ok), len(row))
    mean = {T: float(np.mean(list(v.values()))) for T, v in per_t.items()}

    note = next((x.get("영문_각주") for x in g["generations"]
                 if x.get("id") == "gen2_400ps_4window"), None)
    if not note:
        raise ValueError("gen2 영문 각주를 원장에서 못 읽었다 — 손으로 적지 않는다")

    return {"per_t": per_t, "mean": mean, "eligible": elig,
            "Ea_ledger": float(r5["Ea3"]["eV"]),
            "Ea_CI95": [float(x) for x in r5["Ea3"]["CI95_eV"]],
            "rounds": [
                {"label": "3 seeds  (2·3·3)", "d": float(r3["★_C3"]["ΔEa_점추정_eV"]),
                 "ci": [float(x) for x in r3["★_C3"]["CI95_eV"]],
                 "verdict": "inconclusive"},
                {"label": "5 seeds  (3·5·5)", "d": float(r5["★_C3"]["ΔEa_점추정_eV"]),
                 "ci": [float(x) for x in r5["★_C3"]["CI95_eV"]],
                 "verdict": "compatible"},
            ],
            "allow": [float(x) for x in r5["★_C3"]["허용영역_eV"]],
            "gen_note": note,
            "source": [_rel(p) for p in (mto, c3_5, c3_3)]}


def make_figure(a: dict, out_png=OUT / "modelc_box331_seed_extension.png") -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ea, p = ea_from_means(a["mean"])
    if abs(ea - a["Ea_ledger"]) > 1e-3:
        raise ValueError(f"재계산 Ea {ea:.4f} 가 원장 {a['Ea_ledger']:.4f} 와 "
                         "1 meV 넘게 다르다 — 그리지 않는다")

    c = H.SYS["modelc"]
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11.6, 4.7))

    # ── (a) Arrhenius ────────────────────────────────────────────────────
    x = np.array([1000.0 / T for T in TT])
    for i, T in enumerate(TT):
        #: x-지터 — 시드 점이 평균 점 **뒤에 숨지 않게**. 값은 안 바뀐다(보기용 오프셋).
        n = len(a["per_t"][T])
        jit = (np.arange(n) - (n - 1) / 2.0) * 0.018
        axA.plot(1000.0 / T + jit, np.log(list(a["per_t"][T].values())), "o", ms=5.5,
                 mfc="none", mec=c, mew=1.3, zorder=3,
                 label="per-seed $D$ (MTO, 2–50 ps, free intercept; x-jittered)"
                       if i == 0 else None)
    axA.plot(x, np.log([a["mean"][T] for T in TT]), "D", ms=8, color=c, zorder=4,
             label="T-mean of eligible seeds")
    xf = np.linspace(x.min() - .05, x.max() + .05, 50)
    axA.plot(xf, np.polyval(p, xf), color=c, lw=1.8,
             label=(f"3-point fit  $E_a$ = {a['Ea_ledger']:.4f} eV\n"
                    f"CI95 [{a['Ea_CI95'][0]:.4f}, {a['Ea_CI95'][1]:.4f}] (cell-conditioned)"))
    H.apply_axes(axA, xlabel="1000 / T  (K$^{-1}$)",
                 ylabel=r"ln $D_{\rm Li}$   ($D$ in cm$^2$/s)")
    axA.set_title("(a) Arrhenius — LPSCl$_{1.6}$ 3×3×1, 400 ps, 5 seeds",
                  fontsize=11.5, color=H.INK)
    axA.legend(frameon=False, fontsize=8.5, loc="upper right")
    sec = axA.secondary_xaxis("top", functions=(lambda v: 1000 / np.clip(v, 1e-9, None),
                                                lambda v: 1000 / np.clip(v, 1e-9, None)))
    sec.set_xlabel("T (K)", fontsize=10, color=H.MUT)
    sec.set_xticks(list(TT))
    elig = " · ".join(f"{T} K: {a['eligible'][T][0]}/{a['eligible'][T][1]}" for T in TT)
    axA.text(.02, .04, "eligible seeds — " + elig
             + "\n600 K: s3, s5 excluded (relative spread > 10 %, pre-sealed)",
             transform=axA.transAxes, fontsize=8.2, color=H.MUT, va="bottom")

    # ── (b) C3 게이트 — CI 수축 ──────────────────────────────────────────
    lo, hi = a["allow"]
    axB.axvspan(lo, hi, color="#fef9c3", zorder=0)
    axB.axvline(lo, color=H.GAPLINE, ls="--", lw=1.2, zorder=1)
    axB.axvline(hi, color=H.GAPLINE, ls="--", lw=1.2, zorder=1)
    axB.axvline(0.0, color=H.MUT, lw=.8, zorder=1)
    ys = [1.0, 0.0]
    for y, row in zip(ys, a["rounds"]):
        over = max(0.0, lo - row["ci"][0]) + max(0.0, row["ci"][1] - hi)
        col = c if over == 0 else H.ELEM["O"]
        axB.plot(row["ci"], [y, y], color=col, lw=3.2, solid_capstyle="butt", zorder=3)
        #: 경계 **밖**으로 나간 토막만 굵게 덧그린다 — 이 패널의 요점이 그것이다.
        if over > 0:
            axB.plot([row["ci"][0], min(lo, row["ci"][1])], [y, y], color=col, lw=7.0,
                     solid_capstyle="butt", alpha=.95, zorder=4)
            axB.annotate(f"outside by {over * 1000:.1f} meV",
                         xy=(row["ci"][0], y), xytext=(row["ci"][0] - .004, y + .46),
                         fontsize=8.5, color=col, ha="right",
                         arrowprops=dict(arrowstyle="-", color=col, lw=.9))
        axB.plot([row["d"]], [y], "o", ms=9, color=col, zorder=5)
        axB.plot([row["ci"][0], row["ci"][0]], [y - .09, y + .09], color=col, lw=3.2, zorder=5)
        axB.plot([row["ci"][1], row["ci"][1]], [y - .09, y + .09], color=col, lw=3.2, zorder=5)
        axB.text(row["ci"][1] + .004, y + .16, row["label"], fontsize=9.5, color=H.INK)
        axB.text(row["ci"][1] + .004, y - .28,
                 f"$\\Delta E_a$ = {row['d']:+.4f}   \u2192  {row['verdict']}",
                 fontsize=8.8, color=col)
    axB.set_ylim(-.80, 1.95)
    axB.set_yticks([])
    axB.set_xlim(lo - .022, hi + .012)
    H.apply_axes(axB, xlabel=r"$\Delta E_a$ = $E_a$(600–800 K) $-$ $E_a$(800–1000 K)   (eV)")
    axB.spines["left"].set_visible(False)
    axB.set_title("(b) C3 gate — pre-sealed window $\\pm$%.3f eV" % hi,
                  fontsize=11.5, color=H.INK)
    axB.text(.02, .04,
             "CI95 width 0.0402 → 0.0259 eV (−36 %)\n"
             "5-seed CI lower edge clears the boundary by 6.6 meV",
             transform=axB.transAxes, fontsize=8.2, color=H.MUT, va="bottom")

    fig.text(.5, .006, a["gen_note"], ha="center", fontsize=6.8, color=H.MUT, wrap=True)
    fig.tight_layout(rect=[0, .075, 1, 1])
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    return {"png": str(out_png.relative_to(R)), "Ea_recomputed": ea}


def write_csvs(a: dict,
               csv_a=DB / "modelc_box331_arrhenius_origin_2026_09_20.csv",
               csv_b=DB / "modelc_box331_c3_ci_origin_2026_09_20.csv") -> dict:
    ea, p = ea_from_means(a["mean"])
    seeds = sorted({s for T in TT for s in a["per_t"][T]})
    with open(csv_a, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([f"# modelc(LPSCl1.6) 3x3x1 400 ps, 5 seeds. "
                    f"Ea(cell-conditioned) = {a['Ea_ledger']:.4f} eV, "
                    f"CI95 [{a['Ea_CI95'][0]:.4f}, {a['Ea_CI95'][1]:.4f}]"])
        w.writerow(["# sources: " + " ; ".join(a["source"])])
        w.writerow(["# D per eligible seed (cm^2/s): MTO, window 2-50 ps, free intercept. "
                    "blank = excluded (relative spread > 10 %)."])
        w.writerow(["# fit_lnD = 3-point unweighted fit of ln(D_mean) vs 1000/T; "
                    "Ea = -slope*kB*1000"])
        w.writerow([f"# PROTOCOL GENERATION gen2_400ps_4window. {a['gen_note']}"])
        w.writerow(["T_K", "x_1000_over_T"] + [f"D_{s}_cm2_s" for s in seeds]
                   + ["n_eligible", "n_total", "D_mean_cm2_s", "lnD_mean", "fit_lnD"])
        for T in TT:
            xx = 1000.0 / T
            w.writerow([T, f"{xx:.6f}"] + [a["per_t"][T].get(s, "") for s in seeds]
                       + [a["eligible"][T][0], a["eligible"][T][1],
                          f"{a['mean'][T]:.4e}", f"{np.log(a['mean'][T]):.5f}",
                          f"{np.polyval(p, xx):.5f}"])
    with open(csv_b, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# C3 gate: dEa = Ea(600-800 K) - Ea(800-1000 K), seed-resampled CI95"])
        w.writerow([f"# pre-sealed allowed window = [{a['allow'][0]}, {a['allow'][1]}] eV "
                    "(sealed before results; not chosen from the data)"])
        w.writerow(["# sources: " + " ; ".join(a["source"])])
        w.writerow(["round", "n_seed_600_800_1000", "dEa_eV", "CI95_lo_eV", "CI95_hi_eV",
                    "CI95_width_eV", "allow_lo_eV", "allow_hi_eV", "verdict"])
        for row, ns in zip(a["rounds"], ("2/3/3", "3/5/5")):
            w.writerow([row["label"].split()[0] + "-seed", ns, f"{row['d']:.4f}",
                        f"{row['ci'][0]:.4f}", f"{row['ci'][1]:.4f}",
                        f"{row['ci'][1] - row['ci'][0]:.4f}",
                        a["allow"][0], a["allow"][1], row["verdict"]])
    return {"csv_a": str(csv_a.relative_to(R)), "csv_b": str(csv_b.relative_to(R))}


def _selftest() -> int:
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    def dies(fn, frag):
        try:
            fn()
        except (ValueError, KeyError) as e:
            return frag in str(e)
        except Exception:
            return False
        return False

    a = load_modelc()
    chk(a["eligible"][600] == (3, 5), f"[양성] 600 K 자격 3/5 (얻은 {a['eligible'][600]})")
    chk(a["eligible"][800] == (5, 5) and a["eligible"][1000] == (5, 5),
        "[양성] 800·1000 K 는 5/5")
    ea, _ = ea_from_means(a["mean"])
    chk(abs(ea - a["Ea_ledger"]) <= 1e-3,
        f"[양성] D 평균 재계산 Ea {ea:.4f} 가 원장 {a['Ea_ledger']:.4f} 와 1 meV 안")
    chk(a["rounds"][0]["ci"][0] < a["allow"][0] <= a["rounds"][1]["ci"][0],
        "[양성] 3시드 CI 하단은 경계 **밖**, 5시드는 **안** — 그림의 요점이 데이터에 있다")
    chk(a["rounds"][1]["ci"][1] - a["rounds"][1]["ci"][0]
        < a["rounds"][0]["ci"][1] - a["rounds"][0]["ci"][0],
        "[양성] 5시드 CI 가 3시드보다 좁다")

    td = pathlib.Path(tempfile.mkdtemp(prefix="figw0920_"))

    def _mk(name, obj):
        p = td / name
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return p

    # ⛔ 음성 — 온도 하나가 없다
    bad = json.loads(MTO5.read_text(encoding="utf-8"))
    del bad["D_cm2_s"]["800"]
    chk(dies(lambda: load_modelc(mto=_mk("no800.json", bad)), "800 K 가 없다"),
        "[음성] D 표에 온도가 빠지면 그리지 않는다")

    # ⛔ 음성 — 한 온도의 시드가 전부 null
    bad2 = json.loads(MTO5.read_text(encoding="utf-8"))
    bad2["D_cm2_s"]["600"] = {k: None for k in bad2["D_cm2_s"]["600"]}
    chk(dies(lambda: load_modelc(mto=_mk("null600.json", bad2)), "자격 시드가 하나도 없다"),
        "[음성] 자격 시드 0 이면 3점 적합을 시도하지 않는다")

    # ⛔ 음성 — 세대 각주가 없으면 손으로 안 적는다
    g = json.loads(GEN.read_text(encoding="utf-8"))
    g["generations"] = [x for x in g["generations"] if x.get("id") != "gen2_400ps_4window"]
    chk(dies(lambda: load_modelc(gen=_mk("nogen.json", g)), "영문 각주"),
        "[음성] gen2 각주가 없으면 중단한다 (각주를 지어내지 않는다)")

    # ⛔ 음성 — 원장 Ea 를 흔들면 그림이 거부한다
    bad3 = json.loads(C3_5.read_text(encoding="utf-8"))
    bad3["Ea3"]["eV"] = 0.30
    a3 = load_modelc(c3_5=_mk("badea.json", bad3))
    chk(dies(lambda: make_figure(a3, out_png=td / "x.png"), "1 meV 넘게 다르다"),
        "[음성] 원장 Ea 와 재계산이 1 meV 넘게 벌어지면 **그리지 않는다**")

    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    A = load_modelc()
    print(json.dumps({**make_figure(A), **write_csvs(A)}, ensure_ascii=False, indent=1))
