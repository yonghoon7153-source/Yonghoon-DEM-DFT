#!/usr/bin/env python3
"""fig_weekly_2026_10_04.py — 주간보고(2026-09-28 ~ 10-04) 그림 2장 + Origin CSV 2벌.

  (1) li2s_v2_gate.png — li2s 유리 MD v2 판독 (규칙 적용 · 외부 1저자 확인 대기)
      (a) β_MTO(2–50 ps) ± 2σ (σ = 사다리 끝 b · 하한) vs 카드 C2 띠 [0.8, 1.2] — 550 K 800 ps · 600 K 400 ps
      (b) 가까운 문턱까지의 σ 거리 — 끝 b · 앞 b (끝 두 b 규칙 · 개정 CO) vs 2σ 선
      값은 v2 실행 기록 `✅_판독_결과_2026_10_04` 에서만 읽는다. σ 는 기록에 없어서 (β − 0.8)/n_σ 로
      되짚고, 그 범위가 `✅_판독_세부_2026_10_04.σ_대조` 의 문자열(550 K 0.019–0.027)과 맞을 때만 그린다.
  (2) cascade_subwindow.png — cascade 부창 기울기비 (2–18 · 18–34 · 34–50 ps) vs 자격 띠 [0.8, 1.2]
      v6 판정 40 런 (600 K · 200 ps · 원자료 판독 JSON 의 `detail.sub_window_ratios` 만) +
      v6 H0 속도시험 1 런 (라운드 결과 문장) + v7 탐침 끝난 런 (탐침 실행 기록의 판독기 문장).

    python3 tools/figures/fig_weekly_2026_10_04.py            # PNG 2장 + CSV 2벌
    python3 tools/figures/fig_weekly_2026_10_04.py --selftest # 양성 + 음성

이 도구가 **못 하는 것**
  · 값을 판정하지 않는다 — 기록이 적은 판정을 옮기고, 교차검산이 틀리면 **그리지 않는다**.
  · li2s: **외부 1저자 트랙**이다. β·σ 거리는 내부 진단(`citable: false`)이고 갈래 확정은 외부 1저자 몫이다.
    σ 는 **하한**이다 (400 ps 는 b_min 에 못 닿음 · 800 ps 는 닿았으나 여전히 하한 — 개정 CO).
    보조 창(50–200 ps) β 는 그리지 않는다 — 기록 열이고, 편지 CQ 가 그 문장조차 과한지 묻고 있다.
  · cascade: ⛔ **D 를 읽지도 그리지도 않는다** (v7 카드 · 탐침 출력에 D 없음). 판독 JSON 에서
    구조·시드·태그·자격·부창비 다섯 필드만 꺼내고, 꺼낸 묶음에 D 열쇠가 섞이면 **죽는다**.
    부창비는 자격 셋 중 하나일 뿐이다 (D_inc plateau · 사건 수 ≥ 50 은 그림에 없다).
    v6 (200 ps) 와 v7 탐침 (400 ps) 은 생산 길이가 다르다 — 같은 정의의 비지만 잡음 폭이 다르다.
  · 다른 주의 그림을 만들지 않는다 — 날짜가 파일명에 박힌 일회성 산출물이다.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import statistics
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

DB = R / "db/properties"
OUT = R / "docs/figures/weekly_2026_10_04"

LI2S_RUNLOG = DB / "lpscl_smallcell_glass_md_v2_runlog_2026_10_01.json"
V6_JUDGE = R / "db/raw/cascade_v6_2026_10_01/cascade_v6_judgement.json"
V6_ROUND = DB / "cascade_v6_round_result_2026_10_01.json"
V7_RUNLOG = DB / "cascade_v7_probe_runlog_2026_10_03.json"

C2_BAND = (0.8, 1.2)        # 카드 v2 C2 (회신 CD · CL) — 문턱은 기록에서 다시 대조한다
ELIG_BAND = (0.8, 1.2)      # cascade 자격 ② 부창 기울기비 (v6 카드 · v7 승계)
SIGMA_GATE = 2.0            # 회신 CL: 가까운 문턱에서 2σ
PIECES = ("2–18 ps", "18–34 ps", "34–50 ps")

GOOD, WARN, CRIT = "#15803d", "#d97706", "#b91c1c"
VERDICT_EN = {"통과": "pass", "경계 · 구분 불가": "boundary", "미통과": "fail"}
VERDICT_COL = {"pass": GOOD, "boundary": WARN, "fail": CRIT}


class Refuse(RuntimeError):
    """교차검산이 틀렸다 — 그리지 않는다."""


def _rel(p) -> str:
    try:
        return str(pathlib.Path(p).resolve().relative_to(R))
    except ValueError:
        return str(p)


def _load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


# ────────────────────────────────────────────────────────────── li2s v2
def load_li2s(p=LI2S_RUNLOG) -> dict:
    d = _load(p)
    res = d.get("✅_판독_결과_2026_10_04")
    det = d.get("✅_판독_세부_2026_10_04")
    if not res or not det:
        raise Refuse("v2 실행 기록에 판독 결과·세부 절이 없다")
    cols = res.get("열") or []
    want = ["machine", "C1_MSD@50_MTO_Å²", "β_MTO", "n_σ 끝 b", "n_σ 앞 b"]
    if cols[:5] != want or cols[6] != "최종 C2 (끝 두 b)":
        raise Refuse(f"열 이름이 기대와 다르다: {cols[:7]}")
    runs, nrec = [], {}
    for key, sec in res.items():
        m = re.match(r"^(\d+)K_(\d+)ps_끝b(\d+)_앞b(\d+)$", key)
        if not m:
            continue
        T, ps, b_end, b_prev = (int(x) for x in m.groups())
        n_pass = 0
        for s in ("seed1", "seed2", "seed3", "seed4", "seed5"):
            row = sec.get(s)
            if not isinstance(row, list) or len(row) < 7:
                raise Refuse(f"{key} {s} 행이 없다")
            machine, c1, beta, ns_end, ns_prev, _, verdict = row[:7]
            if verdict not in VERDICT_EN:
                raise Refuse(f"{key} {s}: 모르는 판정 {verdict!r}")
            lo, hi = C2_BAND
            near = lo if abs(beta - lo) <= abs(beta - hi) else hi
            if ns_end <= 0:
                raise Refuse(f"{key} {s}: σ 거리 {ns_end} — σ 를 되짚을 수 없다")
            sigma = abs(beta - near) / ns_end
            # 끝 두 b 규칙 (개정 CO): 둘 다 ≥ 2σ 면 통과 · 둘 다 < 2σ 면 경계 · 한쪽만이면 경계
            both = ns_end >= SIGMA_GATE and ns_prev >= SIGMA_GATE
            expect = "통과" if both else "경계 · 구분 불가"
            if not (lo <= beta <= hi):
                expect = None      # 띠 밖 — 이 주의 자료에는 없다. 있으면 판정 재현을 포기하고 죽는다.
            if expect != verdict:
                raise Refuse(f"{key} {s}: 기록 판정 {verdict!r} ≠ 규칙 재현 {expect!r} "
                             f"(n_σ {ns_end} · {ns_prev})")
            n_pass += verdict == "통과"
            runs.append({"T": T, "ps": ps, "seed": int(s[4:]), "machine": machine, "c1": c1,
                         "beta": beta, "ns_end": ns_end, "ns_prev": ns_prev, "b_end": b_end,
                         "b_prev": b_prev, "sigma": sigma, "verdict": VERDICT_EN[verdict]})
        nstr = str(sec.get("N") or "")
        if not nstr.startswith(f"{n_pass}/5"):
            raise Refuse(f"{key}: 기록 N {nstr!r} ≠ 행에서 센 통과 {n_pass}/5")
        nrec[T] = n_pass
    if sorted(nrec) != [550, 600]:
        raise Refuse(f"온도가 550 · 600 둘이 아니다: {sorted(nrec)}")
    # σ 범위 대조 — 세부 절의 문자열 '새 550 K σ 끝(b512) 0.019–0.027'
    m = re.search(r"새 550 K σ 끝\(b512\) ([0-9.]+)–([0-9.]+)", str(det.get("σ_대조") or ""))
    if not m:
        raise Refuse("세부 절 σ_대조 문자열을 못 읽었다")
    s550 = [r["sigma"] for r in runs if r["T"] == 550]
    got = (f"{min(s550):.3f}", f"{max(s550):.3f}")
    if got != m.groups():
        raise Refuse(f"되짚은 550 K σ 범위 {got} ≠ 기록 {m.groups()}")
    branch = str(res.get("갈래_규칙_적용") or "")
    if not branch.startswith("v2-2"):
        raise Refuse(f"기록 갈래가 v2-2 가 아니다: {branch[:30]!r}")
    return {"runs": runs, "N": nrec, "branch": "v2-2", "sigma550": got}


# ────────────────────────────────────────────────────────────── cascade
_KEEP = ("structure", "seed", "tag", "eligible")


def _no_D(obj, where):
    """꺼낸 묶음에 D 열쇠가 섞이면 죽는다 (v7 카드 · D 는 화면·그림에 안 나온다)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if re.match(r"^D($|_)", str(k)):
                raise Refuse(f"{where}: D 열쇠 {k!r} 가 그림 자료에 들어왔다")
            _no_D(v, where)
    elif isinstance(obj, list):
        for v in obj:
            _no_D(v, where)


def _ratios(txt: str, where: str) -> list:
    m = re.search(r"부창비 \[([^\]]+)\]", txt)
    if not m:
        raise Refuse(f"{where}: '부창비 [...]' 를 못 읽었다")
    r = [float(x) for x in m.group(1).split(",")]
    if len(r) != 3:
        raise Refuse(f"{where}: 부창비가 셋이 아니다 {r}")
    return r


def load_cascade(judge=V6_JUDGE, rnd=V6_ROUND, probe=V7_RUNLOG) -> dict:
    j = _load(judge)
    rows = j.get("rows") or []
    v6 = []
    for i, r in enumerate(rows):
        swr = ((r.get("detail") or {}).get("sub_window_ratios"))
        if not isinstance(swr, list) or len(swr) != 3:
            raise Refuse(f"v6 행 {i}: sub_window_ratios 가 셋이 아니다")
        v6.append({k: r.get(k) for k in _KEEP} | {"ratios": [float(x) for x in swr]})
    _no_D(v6, "v6")
    el = j.get("eligibility") or {}
    if len(v6) != el.get("n_runs"):
        raise Refuse(f"v6 행 {len(v6)} ≠ eligibility.n_runs {el.get('n_runs')}")
    n_elig = sum(1 for r in v6 if r["eligible"])
    if n_elig != el.get("n_eligible"):
        raise Refuse(f"v6 자격 {n_elig} ≠ 기록 {el.get('n_eligible')}")
    lo, hi = ELIG_BAND
    n_out = sum(1 for r in v6 if any(not (lo <= x <= hi) for x in r["ratios"]))
    tally = (el.get("reason_tally") or {}).get("②_부창_기울기비")
    if n_out != tally:
        raise Refuse(f"띠 밖 런 {n_out} ≠ 기록 ② 미달 {tally}")
    med = [statistics.median(r["ratios"][k] for r in v6) for k in range(3)]
    rd = _load(rnd)
    diag = rd.get("3_곡선_모양_진단") or {}
    two = diag.get("②_부창_기울기비") or {}
    for k, key in enumerate(("2–18_ps", "18–34_ps", "34–50_ps")):
        m = re.search(r"중앙 ([0-9.]+)", str(two.get(key) or ""))
        if not m or f"{med[k]:.2f}" != m.group(1):
            raise Refuse(f"v6 {key} 중앙 {med[k]:.2f} ≠ 라운드 결과 {m.group(1) if m else None}")
    h0 = _ratios(str(diag.get("H0_속도시험_런") or ""), "v6 H0 속도시험")
    pr = _load(probe)
    v7 = []
    for blk in pr.get("탐침_진행") or []:
        for tag, run in (blk.get("끝난_런") or {}).items():
            txt = str(run.get("판독기") or "")
            m = re.search(r"자격 (통과|미달)", txt)
            if not m:
                raise Refuse(f"v7 {tag}: 자격 문구가 없다")
            rat = _ratios(txt, f"v7 {tag}")
            inband = all(lo <= x <= hi for x in rat)
            if m.group(1) == "통과" and not inband:
                raise Refuse(f"v7 {tag}: 기록은 자격 통과인데 부창비가 띠 밖 {rat}")
            T = re.search(r"__T(\d+)__", tag)
            v7.append({"tag": tag, "T": int(T.group(1)) if T else None,
                       "eligible": m.group(1) == "통과", "ratios": rat})
    _no_D(v7, "v7")
    if not v7:
        raise Refuse("v7 탐침 끝난 런이 없다")
    return {"v6": v6, "v6_median": med, "v6_h0": h0, "v6_n_elig": n_elig, "v7": v7}


# ────────────────────────────────────────────────────────────── 그림
def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def fig_li2s(L: dict, out_png=OUT / "li2s_v2_gate.png") -> str:
    plt = _plt()
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(13.4, 5.2), gridspec_kw={"width_ratios": [1.15, 1]})
    runs = L["runs"]
    xs = {}
    for r in runs:
        xs[(r["T"], r["seed"])] = (r["seed"] - 1) + (0 if r["T"] == 550 else 6)
    lo, hi = C2_BAND
    ax.axhspan(lo, hi, color="#dcfce7", zorder=0)
    ax.axhline(1.0, color=H.MUT, ls=":", lw=1)
    ax.text(10.6, hi - 0.012, f"gate C2: {lo}–{hi}", ha="right", va="top", fontsize=8.8, color=GOOD)
    for r in runs:
        x = xs[(r["T"], r["seed"])]
        col = VERDICT_COL[r["verdict"]]
        ax.errorbar(x, r["beta"], yerr=SIGMA_GATE * r["sigma"], fmt="o", ms=8, color=col,
                    capsize=4, lw=1.4)
    ax.set_xticks([xs[(r["T"], r["seed"])] for r in runs])
    ax.set_xticklabels([f"s{r['seed']}\n{r['machine']}" for r in runs], fontsize=8.6)
    for T, x0, ps in ((550, 2, 800), (600, 8, 400)):
        ax.text(x0, 0.715, f"{T} K · {ps} ps   N = {L['N'][T]}/5", ha="center", fontsize=10,
                color=H.INK, fontweight="bold")
    ax.set_xlim(-0.8, 10.8)
    ax.set_ylim(0.70, 1.22)
    H.apply_axes(ax, ylabel="MSD exponent β_MTO  (2–50 ps)",
                 title="(a)  β ± 2σ vs gate C2  (σ at the last block size = lower bound)")
    ax.plot([], [], "o", color=GOOD, label="pass (both last two b ≥ 2σ)")
    ax.plot([], [], "o", color=WARN, label="boundary (within 2σ of the edge)")
    ax.legend(frameon=False, fontsize=8.6, loc="upper left")

    w = 0.36
    for r in runs:
        x = xs[(r["T"], r["seed"])]
        col = VERDICT_COL[r["verdict"]]
        bx.bar(x - w / 2, r["ns_end"], w * 0.95, color=col)
        bx.bar(x + w / 2, r["ns_prev"], w * 0.95, color=col, alpha=0.45)
    bx.axhline(SIGMA_GATE, color=H.INK, ls="--", lw=1.1)
    bx.text(5.0, SIGMA_GATE + 0.12, "2σ rule", ha="center", fontsize=8.8, color=H.INK)
    near = min((r for r in runs if r["T"] == 550 and r["verdict"] == "boundary"),
               key=lambda r: SIGMA_GATE - r["ns_end"])
    xn = xs[(near["T"], near["seed"])]
    bx.annotate(f"near miss: s{near['seed']} {near['ns_end']:+.2f}σ",
                xy=(xn - w / 2, near["ns_end"]), xytext=(xn + 0.4, 4.6), fontsize=8.6,
                color=H.INK, arrowprops=dict(arrowstyle="->", color=H.MUT, lw=1))
    bx.set_xticks([xs[(r["T"], r["seed"])] for r in runs])
    bx.set_xticklabels([f"s{r['seed']}" for r in runs], fontsize=8.6)
    b550 = next(r for r in runs if r["T"] == 550)
    b600 = next(r for r in runs if r["T"] == 600)
    bx.text(2, -1.25, f"550 K: last b = {b550['b_end']}, {b550['b_prev']}", ha="center",
            fontsize=8.6, color=H.MUT)
    bx.text(8, -1.25, f"600 K: last b = {b600['b_end']}, {b600['b_prev']}", ha="center",
            fontsize=8.6, color=H.MUT)
    bx.set_xlim(-0.8, 10.8)
    bx.set_ylim(0, 8.2)
    H.apply_axes(bx, ylabel="distance to the nearest C2 edge (σ units)",
                 title="(b)  Two-end rule: solid = last b, faded = previous b")
    fig.text(0.01, -0.04,
             "li2s glass MD v2 (120 atoms, UMA). Rules fixed before the results (card v2 + amendment CO). "
             f"Branch by rule = {L['branch']} (600 K ≥ 3/5, 550 K ≤ 2/5) — provisional until the "
             "external first author confirms.\nInternal diagnostic (citable: false). b = time-origin "
             "block size (0.1 ps per origin). No D, σ_Li or Ea values are shown.",
             fontsize=8.2, color=H.MUT, va="top")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return _rel(out_png)


def fig_cascade(C: dict, out_png=OUT / "cascade_subwindow.png") -> str:
    plt = _plt()
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    lo, hi = ELIG_BAND
    ax.axhspan(lo, hi, color="#dcfce7", zorder=0)
    ax.text(2.18, 1.0, f"eligibility band\n{lo}–{hi}", fontsize=8.6, color=GOOD, va="center")
    x = [0, 1, 2]
    for i, r in enumerate(C["v6"]):
        ax.plot(x, r["ratios"], color="#9ca3af", lw=0.8, alpha=0.45, zorder=1,
                label=f"v6 judged runs, 600 K, 200 ps (eligible {C['v6_n_elig']}/{len(C['v6'])})"
                if i == 0 else None)
    ax.plot(x, C["v6_median"], color="#4b5563", lw=2.2, ls="--", zorder=2, label="v6 median")
    ax.plot(x, C["v6_h0"], color="#4b5563", lw=1.4, ls=":", marker="s", ms=5, zorder=2,
            label="v6 H0 speed-test run (600 K)")
    for r in C["v7"]:
        col = GOOD if r["eligible"] else CRIT
        ax.plot(x, r["ratios"], color=col, lw=2.6, marker="o", ms=7, zorder=3,
                label=f"v7 probe H0 s1, {r['T']} K, 400 ps — "
                      f"{'eligible' if r['eligible'] else 'not eligible → T dropped'}")
    ax.set_yscale("log")
    ax.set_yticks([0.1, 0.2, 0.5, 0.8, 1.0, 1.2, 2, 4])
    ax.set_yticklabels(["0.1", "0.2", "0.5", "0.8", "1", "1.2", "2", "4"])
    ax.set_ylim(0.08, 4.5)
    ax.set_xticks(x)
    ax.set_xticklabels(PIECES)
    ax.set_xlim(-0.25, 2.75)
    H.apply_axes(ax, xlabel="sub-window of the 2–50 ps fit window",
                 ylabel="sub-window slope / full-window slope",
                 title="cascade D_rel: MSD shape check — v6 (closed) vs v7 temperature probe")
    ax.legend(frameon=False, fontsize=8.2, loc="lower left")
    ax.text(0.0, -0.17, "A straight MSD gives 1 in every piece. v6 bent downward in all 40 runs "
            "→ closed as method-invalid (10-01).\nv7 raises T only: 800 K failed piece 1 → dropped; "
            "1000 K needs all 6 planned runs to pass. Ratios only — no D values.",
            transform=ax.transAxes, fontsize=8.2, color=H.MUT, va="top")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return _rel(out_png)


# ────────────────────────────────────────────────────────────── CSV
def write_csvs(L: dict, C: dict, d=DB) -> dict:
    out = {}
    p = d / "weekly_li2s_v2_gate_origin_2026_10_04.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["T_K", "prod_ps", "seed", "machine", "C1_MSD50_MTO_A2", "beta_MTO_2_50ps",
                    "n_sigma_last_b", "n_sigma_prev_b", "last_b", "prev_b",
                    "sigma_last_b_lower_bound", "final_C2_by_rule"])
        for r in L["runs"]:
            w.writerow([r["T"], r["ps"], r["seed"], r["machine"], r["c1"], r["beta"], r["ns_end"],
                        r["ns_prev"], r["b_end"], r["b_prev"], f"{r['sigma']:.5f}", r["verdict"]])
    out["li2s"] = _rel(p)
    p = d / "weekly_cascade_subwindow_origin_2026_10_04.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["series", "run", "T_K", "prod_ps", "ratio_2_18ps", "ratio_18_34ps",
                    "ratio_34_50ps", "eligible_recorded"])
        for r in C["v6"]:
            w.writerow(["v6_judged", r["tag"], 600, 200, *r["ratios"], r["eligible"]])
        w.writerow(["v6_median", "median_of_40", 600, 200, *(f"{x:.4f}" for x in C["v6_median"]), ""])
        w.writerow(["v6_H0_speedtest", "H0_host", 600, 200, *C["v6_h0"], False])
        for r in C["v7"]:
            w.writerow(["v7_probe", r["tag"], r["T"], 400, *r["ratios"], r["eligible"]])
    out["cascade"] = _rel(p)
    return out


# ────────────────────────────────────────────────────────────── 시험
def _selftest() -> int:
    import copy
    import tempfile
    bad = []

    def chk(c, m):
        if not c:
            bad.append(m)

    def dies(fn, frag):
        try:
            fn()
        except Refuse as e:
            chk(frag in str(e), f"다른 이유로 죽었다: {e} (기대 {frag!r})")
            return
        bad.append(f"죽어야 하는데 살았다: {frag}")

    # 양성 — 실제 기록
    L = load_li2s()
    chk(len(L["runs"]) == 10, "li2s 런이 10 이 아니다")
    chk(L["N"] == {550: 2, 600: 5}, f"N {L['N']}")
    chk(L["sigma550"] == ("0.019", "0.027"), f"σ 범위 {L['sigma550']}")
    s1 = next(r for r in L["runs"] if r["T"] == 550 and r["seed"] == 1)
    chk(s1["verdict"] == "boundary" and abs(s1["ns_end"] - 1.848) < 1e-9, "near-miss 행")
    C = load_cascade()
    chk(len(C["v6"]) == 40 and C["v6_n_elig"] == 0, "v6 40 런 · 자격 0")
    chk([f"{x:.2f}" for x in C["v6_median"]] == ["2.25", "0.78", "0.49"], f"v6 중앙 {C['v6_median']}")
    chk(C["v6_h0"] == [3.27, 0.65, 0.11], f"H0 {C['v6_h0']}")
    t = {r["T"]: r["eligible"] for r in C["v7"]}
    chk(t.get(800) is False and t.get(1000) is True, f"v7 {t}")
    for r in C["v6"]:
        chk(set(r) == set(_KEEP) | {"ratios"}, f"v6 꺼낸 필드가 다섯이 아니다: {sorted(r)}")

    # 음성 — 임시 파일로 기록을 하나씩 망가뜨린다
    tmp = pathlib.Path(tempfile.mkdtemp())

    def _w(name, obj):
        p = tmp / name
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return p

    li = _load(LI2S_RUNLOG)
    x = copy.deepcopy(li)
    x["✅_판독_결과_2026_10_04"]["550K_800ps_끝b512_앞b384"]["seed1"][6] = "통과"
    dies(lambda: load_li2s(_w("a.json", x)), "≠ 규칙 재현")           # 판정 문자열 위조
    x = copy.deepcopy(li)
    x["✅_판독_결과_2026_10_04"]["600K_400ps_끝b256_앞b192"]["N"] = "4/5"
    dies(lambda: load_li2s(_w("b.json", x)), "기록 N")                 # N 위조
    x = copy.deepcopy(li)
    x["✅_판독_결과_2026_10_04"]["550K_800ps_끝b512_앞b384"]["seed2"][3] = 0.9
    dies(lambda: load_li2s(_w("c.json", x)), "σ 범위")                 # σ 거리 위조 → σ 범위 어긋남
    x = copy.deepcopy(li)
    x["✅_판독_결과_2026_10_04"]["갈래_규칙_적용"] = "v2-3 — …"
    dies(lambda: load_li2s(_w("d.json", x)), "v2-2")                   # 갈래 문자열
    x = copy.deepcopy(li)
    del x["✅_판독_세부_2026_10_04"]
    dies(lambda: load_li2s(_w("e.json", x)), "판독 결과·세부")
    x = copy.deepcopy(li)
    x["✅_판독_결과_2026_10_04"]["열"][2] = "β_STO"
    dies(lambda: load_li2s(_w("f.json", x)), "열 이름")

    jj = _load(V6_JUDGE)
    y = copy.deepcopy(jj)
    y["rows"][0]["detail"]["sub_window_ratios"] = [1.0, 1.0, 1.0]
    dies(lambda: load_cascade(judge=_w("g.json", y)), "띠 밖 런")      # ② 미달 셈이 어긋남
    y = copy.deepcopy(jj)
    y["eligibility"]["n_eligible"] = 3
    dies(lambda: load_cascade(judge=_w("h.json", y)), "v6 자격")
    y = copy.deepcopy(jj)
    _KEEP_SAVE = globals()["_KEEP"]
    globals()["_KEEP"] = _KEEP_SAVE + ("D",)                            # D 를 꺼내려 하면
    try:
        dies(lambda: load_cascade(judge=_w("i.json", y)), "D 열쇠")
    finally:
        globals()["_KEEP"] = _KEEP_SAVE
    pr = _load(V7_RUNLOG)
    z = copy.deepcopy(pr)
    z["탐침_진행"][0]["끝난_런"]["H0_host__T800__s1"]["판독기"] = \
        "자격 통과 · 부창비 [1.72, 0.86, 0.84]"
    dies(lambda: load_cascade(probe=_w("j.json", z)), "띠 밖")           # 통과라 적었는데 띠 밖
    z = copy.deepcopy(pr)
    z["탐침_진행"][1]["끝난_런"]["H0_host__T1000__s1"]["판독기"] = "자격 통과 · 골격 static"
    dies(lambda: load_cascade(probe=_w("k.json", z)), "부창비")
    rd = _load(V6_ROUND)
    q = copy.deepcopy(rd)
    q["3_곡선_모양_진단"]["②_부창_기울기비"]["18–34_ps"] = "중앙 0.81 [0.67, 0.88]"
    dies(lambda: load_cascade(rnd=_w("l.json", q)), "중앙")

    n_pos, n_neg = 9 + len(C["v6"]), 12
    if bad:
        print("SELFTEST FAIL"); [print("  ✗", b) for b in bad]
        return 1
    print(f"SELFTEST PASS — 양성 {n_pos} · 음성 {n_neg}")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return _selftest()
    L, C = load_li2s(), load_cascade()
    pngs = [fig_li2s(L), fig_cascade(C)]
    csvs = write_csvs(L, C)
    for p in pngs:
        print("PNG", p)
    for p in csvs.values():
        print("CSV", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
