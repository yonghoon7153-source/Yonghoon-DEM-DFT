#!/usr/bin/env python3
"""fig_weekly_2026_11_08.py — 주간보고 (2026-11-02 ~ 11-08) 그림 1 장 + Origin CSV 1 벌.

그림: cascade D_rel v7 본 라운드 판정 (11-04 · 마감 `D-2026-11-04-cascade-v7-main-closed`) —
  부모 배치마다 ln[D(P1)/D(P2)] (P1 = Al₂O₃ 처방 · P2 = Al₂S₃ 처방 · T* 1000 K) · 자격을 통과한 부모 6 의
  평균 L̄ 과 95 % 구간 · 카드의 등가영역 ±ln 1.5. 구간이 영역 안에 있어서 판정이 '실질_동등_지지' 다.

    python3 tools/figures/fig_weekly_2026_11_08.py
    python3 tools/figures/fig_weekly_2026_11_08.py --selftest   # 기록 재현 (양성) · 깨기 (음성)

읽는 것 (전부 기록 · 새 계산 없음)
  · db/properties/cascade_d_rel_v7_closed_2026_11_04.json — `1_확정` (부모별 lnR · L̄ · sd · SE · t · 구간 · 비 · 판정)
  · db/raw/cascade_v7_main_2026_10_07/cascade_v7_judgement.json — 판독기 출력 (`parents` 의 lnR · `primary`) — 교차검산 기준

⛔ 이 그림이 못 하는 것
  · 절대 D 를 그리거나 CSV 에 적지 않는다 — 판독 JSON 의 D_bar 칸은 읽지 않는다 (1저자 인용정책 · 마감 §3).
  · 빠진 부모 넷 (A · E · F · H — 한쪽 처방의 시드 하나가 자격 미달) 을 0 으로 그리지 않는다 — 'excluded' 글자만 (대체 금지 · 카드 §3).
  · 판정을 새로 내리지 않는다 — 기록의 판정 글자가 구간 · 영역 관계와 맞는지 검사만 한다.
  · 점이 0 위에 몰려 있어도 'Al₂O₃ 처방이 빠르다' 를 뜻하지 않는다 — 판정은 δ (ln 1.5) 기준 세 갈래이고 결과는 '실질 동등' 이다 (마감 §3).
  · 600 K · 작동 온도 · 실제 재료로 옮기지 않는다 (마감 §2 ① 범위 문장).
"""
from __future__ import annotations

import copy
import csv
import json
import math
import pathlib
import re
import statistics
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

CLOSED = R / "db/properties/cascade_d_rel_v7_closed_2026_11_04.json"
JUDGE = R / "db/raw/cascade_v7_main_2026_10_07/cascade_v7_judgement.json"
OUT = R / "docs/figures/weekly_2026_11_08"
PNG = OUT / "cascade_v7_equivalence.png"
CSV = R / "db/properties/weekly_cascade_v7_equivalence_origin_2026_11_08.csv"
VERDICT = "실질_동등_지지"


class Refuse(RuntimeError):
    """마감 기록과 판독기 출력이 어긋난다 — 그리지 않는다."""


def load():
    return (json.loads(CLOSED.read_text(encoding="utf-8")),
            json.loads(JUDGE.read_text(encoding="utf-8")))


def compute(closed: dict, judge: dict) -> dict:
    """두 기록을 대조해 그림 · CSV 에 쓸 값만 돌려준다 (절대 D 는 꺼내지 않는다)."""
    k = closed["1_확정"]
    parents, prim = judge["parents"], judge["primary"]
    order = sorted(parents)
    rows = []
    for p in order:
        v = parents[p]
        ln = v.get("lnR")                                    # D_bar_* 칸은 읽지 않는다
        rows.append({"parent": p, "lnR": None if ln is None else float(ln)})
    elig = [r for r in rows if r["lnR"] is not None]
    rec = {p: float(x) for p, x in k["부모별_lnR"].items()}
    if set(rec) != {r["parent"] for r in elig}:
        raise Refuse(f"부모 집합이 다르다 — 마감 {sorted(rec)} · 판독기 {[r['parent'] for r in elig]}")
    for r in elig:
        if abs(rec[r["parent"]] - r["lnR"]) > 5e-5:
            raise Refuse(f"부모별 lnR 이 다르다 — {r['parent']}: 마감 {rec[r['parent']]} · 판독기 {r['lnR']:.6f}")
    n = len(elig)
    m = re.match(r"\s*(\d+)\s*/\s*(\d+)", str(k["유효_부모"]))
    if not m or int(m.group(1)) != n or int(m.group(2)) != len(rows) or int(prim["n_valid"]) != n \
            or int(prim["n_parents_declared"]) != len(rows):
        raise Refuse(f"유효 부모 수가 다르다 — 마감 '{k['유효_부모'][:12]}' · 판독기 {prim['n_valid']}/{prim['n_parents_declared']} · 셈 {n}/{len(rows)}")
    xs = [r["lnR"] for r in elig]
    L = statistics.fmean(xs)
    sd = statistics.stdev(xs)
    se = sd / math.sqrt(n)
    t = float(prim["t"])
    if int(prim["df"]) != n - 1 or abs(t - float(k["t_0975_df5"])) > 1e-9:
        raise Refuse("t · 자유도가 기록과 다르다")
    lo, hi = L - t * se, L + t * se
    for name, mine, theirs, tol in (("L̄", L, prim["L_bar"], 1e-9), ("sd", sd, prim["sd"], 1e-9),
                                    ("SE", se, prim["SE"], 1e-9), ("구간 하한", lo, prim["ci_ln"][0], 1e-9),
                                    ("구간 상한", hi, prim["ci_ln"][1], 1e-9), ("비", math.exp(L), prim["ratio"], 1e-9),
                                    ("L̄ (마감)", L, k["L_bar_ln"], 5e-5), ("sd (마감)", sd, k["sd_ln"], 5e-5),
                                    ("SE (마감)", se, k["SE_ln"], 5e-5), ("구간 하한 (마감)", lo, k["ci95_ln"][0], 5e-4),
                                    ("구간 상한 (마감)", hi, k["ci95_ln"][1], 5e-4),
                                    ("비 (마감)", math.exp(L), k["비_D_P1_over_D_P2"], 5e-4),
                                    ("비 구간 하한 (마감)", math.exp(lo), k["ci95_비"][0], 5e-3),
                                    ("비 구간 상한 (마감)", math.exp(hi), k["ci95_비"][1], 5e-4)):
        if abs(mine - float(theirs)) > tol:
            raise Refuse(f"{name} 이 기록과 다르다 — 다시 셈 {mine:.6f} · 기록 {theirs}")
    delta = float(prim["delta_lnD"])
    if abs(delta - math.log(1.5)) > 1e-6:
        raise Refuse(f"등가영역이 ln 1.5 가 아니다 ({delta})")
    inside = -delta < lo and hi < delta
    if not inside or prim["verdict"] != VERDICT or not str(k["판정"]).startswith(VERDICT):
        raise Refuse(f"판정 글자가 구간 · 영역과 안 맞는다 — 구간 [{lo:.4f}, {hi:.4f}] · δ {delta:.4f} · "
                     f"판독기 '{prim['verdict']}' · 마감 '{str(k['판정'])[:12]}'")
    if int(judge["T_star_K"]) != int(k["T_star_K"]) or int(prim["T_K"]) != int(k["T_star_K"]):
        raise Refuse("T* 가 기록끼리 다르다")
    return {"rows": rows, "n": n, "L": L, "lo": lo, "hi": hi, "delta": delta, "T": int(k["T_star_K"])}


def csv_rows(res: dict) -> list[list]:
    """Origin CSV — 부모 한 줄 + 평균 한 줄. 빠진 부모는 빈칸 (0 아님) · 절대 D 칸 없음."""
    out = []
    for r in res["rows"]:
        ln = r["lnR"]
        out.append(["parent", r["parent"], "yes" if ln is not None else "no (one seed not eligible)",
                    "" if ln is None else f"{ln:.6f}", "" if ln is None else f"{math.exp(ln):.6f}",
                    "", "", "", "", f"{res['delta']:.6f}", ""])
    out.append(["pooled_mean", f"{res['n']} eligible parents", "", f"{res['L']:.6f}", f"{math.exp(res['L']):.6f}",
                f"{res['lo']:.6f}", f"{res['hi']:.6f}", f"{math.exp(res['lo']):.6f}", f"{math.exp(res['hi']):.6f}",
                f"{res['delta']:.6f}", VERDICT])
    return out


CSV_HEAD = ["row_type", "parent", "eligible", "ln_ratio_P1_over_P2", "ratio_P1_over_P2",
            "ci95_low_ln", "ci95_high_ln", "ci95_low_ratio", "ci95_high_ratio",
            "equivalence_margin_ln", "verdict"]


def _selftest() -> int:
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ✓ " if c else "  ✗ ") + m)
        ok, bad = ok + bool(c), bad + (not c)

    def refused(fn, needle):
        try:
            fn()
        except Refuse as e:
            return needle in str(e)
        return False

    closed, judge = load()
    res = compute(closed, judge)
    elig = [r["parent"] for r in res["rows"] if r["lnR"] is not None]
    chk(elig == ["B", "C", "D", "G", "I", "J"] and res["n"] == 6, "[양성] 유효 부모 = B · C · D · G · I · J (6/10)")
    chk(abs(res["L"] - 0.0936) < 5e-5 and abs(math.exp(res["L"]) - 1.098) < 5e-4, "[양성] L̄ 0.0936 · 비 1.098 (기록 재현)")
    chk(-res["delta"] < res["lo"] and res["hi"] < res["delta"], "[양성] 구간이 ±ln 1.5 안 → 실질_동등_지지")
    rows = csv_rows(res)
    nums = [float(c) for r in rows for c in r[3:10] if c not in ("",)]
    chk(all(abs(x) > 1e-3 for x in nums), "[양성] CSV 숫자가 전부 비 · ln 비 · 영역뿐 (절대 D 크기 ~1e-5 없음)")
    chk(all(r[3] == "" for r in rows if r[2].startswith("no")), "[양성] 빠진 부모 넷은 빈칸 (0 아님)")

    def mut(f):
        c, j = copy.deepcopy(closed), copy.deepcopy(judge)
        f(c, j)
        return lambda: compute(c, j)

    chk(refused(mut(lambda c, j: c["1_확정"]["부모별_lnR"].__setitem__("C", 0.1001)), "부모별 lnR"),
        "[음성] 마감의 C lnR 을 +0.01 바꾸면 거부")
    chk(refused(mut(lambda c, j: j["parents"]["A"].__setitem__("lnR", 0.05)), "부모 집합"),
        "[음성] 판독기에서 빠진 부모 A 에 lnR 을 넣으면 거부")
    chk(refused(mut(lambda c, j: c["1_확정"].__setitem__("ci95_ln", [0.0292, 0.5])), "구간 상한 (마감)"),
        "[음성] 마감 구간 상한을 0.5 로 바꾸면 거부")
    chk(refused(mut(lambda c, j: j["primary"].__setitem__("verdict", "실질_차이")), "판정 글자"),
        "[음성] 판독기 판정 글자를 바꾸면 거부")
    chk(refused(mut(lambda c, j: c["1_확정"].__setitem__("유효_부모", "7 / 10 (가짜)")), "유효 부모 수"),
        "[음성] 마감의 유효 부모 수를 7 로 바꾸면 거부")
    chk(refused(mut(lambda c, j: j["primary"].__setitem__("delta_lnD", 0.6)), "등가영역"),
        "[음성] 등가영역을 ln 1.5 밖 값으로 바꾸면 거부")
    print(f"fig selftest: ✓ {ok} · ✗ {bad}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    res = compute(*load())
    print(f"교차검산 ✓ 유효 부모 {res['n']} · L̄ {res['L']:.4f} · 비 {math.exp(res['L']):.3f} "
          f"[{math.exp(res['lo']):.3f}, {math.exp(res['hi']):.3f}] · {VERDICT}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.transforms as mtrans
    import numpy as np
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    d = res["delta"]
    ax.axhspan(-d, d, color="#ecfdf5", zorder=0, lw=0)
    for y in (-d, d):
        ax.axhline(y, color="#059669", lw=1.0, ls="--", zorder=1)
    ax.axhline(0, color=H.INK, lw=0.8, zorder=1)
    ax.text(-0.45, d - 0.02, "equivalence margin (ratio 1/1.5 to 1.5, set before the run)", fontsize=8.5,
            color="#047857", va="top")
    xs = np.arange(len(res["rows"]))
    trans = mtrans.blended_transform_factory(ax.transData, ax.transAxes)
    for x, r in zip(xs, res["rows"]):
        if r["lnR"] is None:
            ax.text(x, 0.025, "excluded", ha="center", va="bottom", fontsize=7.5, color=H.MUT, transform=trans)
        else:
            ax.scatter(x, r["lnR"], s=46, color="#0d9488", zorder=3, edgecolor="white", lw=0.6)
    xp = len(res["rows"]) + 0.8
    ax.axvline(len(res["rows"]) - 0.1, color="#d1d5db", lw=0.8)
    ax.errorbar(xp, res["L"], yerr=[[res["L"] - res["lo"]], [res["hi"] - res["L"]]], fmt="o", color=H.INK,
                ms=7, capsize=5, lw=1.6, zorder=4)
    ax.text(xp + 0.35, res["L"], f"{math.exp(res['L']):.2f}\n95% CI {math.exp(res['lo']):.2f}–{math.exp(res['hi']):.2f}",
            fontsize=8.5, color=H.INK, va="center")
    ax.set_xticks(list(xs) + [xp], [r["parent"] for r in res["rows"]] + [f"mean of {res['n']}"])
    ax.set_xlim(-0.6, xp + 2.7)
    ax.set_ylim(-0.5, 0.5)
    H.apply_axes(ax, xlabel="parent configuration (P1 = Al$_2$O$_3$ prescription, P2 = Al$_2$S$_3$ prescription)",
                 ylabel="ln [ D(P1) / D(P2) ]", title=None, fontsize=10.5)
    sec = ax.secondary_yaxis("right", functions=(np.exp, lambda v: np.log(np.clip(v, 1e-9, None))))
    sec.set_yticks([0.67, 0.8, 1.0, 1.25, 1.5])
    sec.set_ylabel("D(P1) / D(P2)", color=H.INK, fontsize=10.5)
    sec.tick_params(colors=H.MUT, labelsize=9)
    ax.set_title(f"cascade v7 main round, T* = {res['T']} K, UMA, common fixed cell: "
                 f"the ratio's 95% CI lies inside the margin (practically equivalent)", fontsize=10, color=H.INK)
    fig.tight_layout()
    fig.savefig(PNG, dpi=300)
    with CSV.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(CSV_HEAD)
        wr.writerows(csv_rows(res))
    print(f"→ {PNG.relative_to(R)} · {CSV.relative_to(R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
