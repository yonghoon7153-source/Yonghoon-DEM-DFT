#!/usr/bin/env python3
"""judge_eprime.py — E′ 파일럿 **판정**. 카드 v5.2 §2 집계식을 코드에 둔다.

    python3 tools/doping/judge_eprime.py --out_root ~/runs/eprime_2026_09_14
    python3 tools/doping/judge_eprime.py --out_root ... --ignore_eligibility   # ⛔ 인용금지
    python3 tools/doping/judge_eprime.py --selftest

무엇을 하나
  ① 런마다 `msd_diffusive_check.aggregation_eligible(t, y, events_per_run)` 로 **자격** 판정
  ② 자격 통과 런만으로 카드 §2 집계식:
       D̄_{p,k} = 시드 2 산술평균 (600 K) · R_k = D̄_P1/D̄_P2 · L_k = ln R_k
       L̄ = (L_A+L_B)/2 · SE = |L_A−L_B|/2 · 95 % 구간 = L̄ ± 12.706·SE (t, df 1)
       판정 = **구간의 위치** 3 갈래 (δ = ln 1.5)
  ③ 2차: (p,k) 마다 600/800/1000 K × 시드 2 = 6 점 겉보기 아레니우스 →
       a_k = Ea(P1_k) − Ea(P2_k) [meV] · ā · SE_a · 구간 ± 12.706·SE_a · δ_Ea = 30 meV

⛔ 이 도구가 **하지 못하는 것**
  · **사건 수를 만들어내지 못한다.** `--save_traj` 없이 돈 라운드에는 궤적이 없고,
    그러면 `events_per_run=None` 이라 카드가 **'검사 불가 = 자격 없음'** 으로 정한다.
    None 을 '통과' 로 바꾸지 않는다 (2026-09-19 실측: 그래서 30 런 전부 자격 미달).
  · 잔류 평균압 P̄ 를 msd.json 에서 못 읽는다 — 카드 §2 가 모든 D·Ea 에 붙이라고 한
    'V = 4066.48 Å³ · P̄ = <실측>' 중 P̄ 를 **결측으로 보고**한다.
  · 결측 (p,k) 를 메우지 않는다. 시드 하나가 빠지면 그 (p,k) 는 결측이다 (카드 §2 결측 규칙).
  · 판정 문턱을 정하지 않는다. δ_lnD = ln 1.5 · δ_Ea = 30 meV 는 **카드가 정했다**.
  · 절대값을 인용 가능하게 만들지 않는다 (1저자 인용정책 2026-09-18 — 상대차만).
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "ionic"))

#: 카드 §2 집계식 — 전부 **카드가 정한 값**이다. 여기서 바꾸면 새 라운드다.
T_DF1 = 12.706          # t(0.975, df=1), NIST
DELTA_LND = math.log(1.5)
DELTA_EA_MEV = 30.0
PRIMARY_T = 600
TEMPS = (600, 800, 1000)
SEEDS = (1, 2)
KB_EV = 8.617333262e-5
V_COMMON_A3 = 4066.479695
PAIRS = {"A": ("P1_Al2O3_A", "P2_Al2S3_A"), "B": ("P1_Al2O3_B", "P2_Al2S3_B")}


def parse_tag(tag: str):
    """md/<tag>/ 에서 (구조, 시드). 속도시험 태그 `X__T600__s1` 도 같은 규칙으로 읽는다."""
    m = re.match(r"^(.*?)(?:__T\d+)?__s(\d+)$", tag)
    return (m.group(1), int(m.group(2))) if m else (None, None)


def scan(out_root):
    """out_root/md/**/T*/msd.json → {(구조, 온도, 시드): 기록}. ⛔ 고르지 않는다 — 전부 담는다."""
    runs = {}
    for f in sorted(glob.glob(os.path.join(out_root, "md", "*", "*", "T*", "msd.json"))):
        tag = Path(f).relative_to(Path(out_root) / "md").parts[0]
        st, sd = parse_tag(tag)
        if st is None:
            continue
        d = json.load(open(f))
        runs[(st, int(d["T_K"]), sd)] = {
            "path": f, "tag": tag, "D": float(d["D_Li_cm2_s"]),
            "t": d["times_ps"], "y": d["msd_Li_A2"],
            "n_Li": d.get("n_Li"), "fit_window_ps": d.get("fit_window_ps"),
            "t_end_ps": (d["times_ps"][-1] if d.get("times_ps") else None)}
    return runs


def count_events(run_dir, d_hop=2.5):
    """궤적에서 **선언한 변위 사건 수**(2.5 Å 카운터). 궤적이 없으면 **None** — 0 이 아니다.

    ⛔ None 과 0 을 섞지 않는다. None = '못 셌다'(자격 없음) · 0 = '세었는데 없었다'.
    """
    for name in ("traj.xyz", "prod.traj", "traj.extxyz"):
        p = Path(run_dir) / name
        if p.exists():
            try:
                from ase.io import read as aread
                import numpy as _np
                fr = aread(str(p), index=":")
                if len(fr) < 2:
                    return None
                sym = _np.array(fr[0].get_chemical_symbols())
                li = _np.where(sym == "Li")[0]
                p0 = fr[0].get_positions()[li]
                n = 0
                for a in fr[1:]:
                    dd = _np.linalg.norm(a.get_positions()[li] - p0, axis=1)
                    hit = dd >= d_hop
                    n += int(hit.sum())
                    p0[hit] = a.get_positions()[li][hit]
                return n
            except Exception:
                return None
    return None


def judge_runs(runs, ignore_eligibility=False):
    """런마다 자격 판정. → {key: {...}}  ⛔ events_per_run=None 은 **통과가 아니다**."""
    from msd_diffusive_check import aggregation_eligible
    out = {}
    for k, r in runs.items():
        ev = count_events(Path(r["path"]).parent)
        ok, why, det = aggregation_eligible(r["t"], r["y"], ev)
        out[k] = {**r, "events_per_run": ev, "eligible": bool(ok),
                  "reasons": why, "detail": det,
                  "used": bool(ok or ignore_eligibility)}
    return out


def dbar(j, struct, T):
    """시드 2 산술평균. **시드 하나라도 빠지면 None** (카드 §2 결측 규칙 — 대체 금지)."""
    vs = []
    for sd in SEEDS:
        r = j.get((struct, T, sd))
        if r is None or not r["used"] or not (r["D"] > 0) or not math.isfinite(r["D"]):
            return None
        vs.append(r["D"])
    return sum(vs) / len(vs)


def ea_mev(j, struct):
    """6 점 겉보기 아레니우스 기울기 → Ea [meV]. 한 점이라도 빠지면 None."""
    xs, ys = [], []
    for T in TEMPS:
        for sd in SEEDS:
            r = j.get((struct, T, sd))
            if r is None or not r["used"] or not (r["D"] > 0):
                return None
            xs.append(1.0 / T); ys.append(math.log(r["D"]))
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0:
        return None
    return -(sxy / sxx) * KB_EV * 1000.0


def verdict_interval(lo, hi, delta):
    """카드 §2-5 — 판정은 **구간의 위치**로 3 갈래."""
    if lo > delta or hi < -delta:
        return "실질_차이_지지"
    if -delta <= lo and hi <= delta:
        return "실질_동등_지지"
    return "미결"


def aggregate(j):
    """카드 §2 집계식. → dict. 유효 부모가 2 미만이면 **구간 판정을 만들지 않는다**."""
    res = {"primary": {"T_K": PRIMARY_T, "delta_lnD": round(DELTA_LND, 6)}, "parents": {}}
    Ls = {}
    for k, (p1, p2) in PAIRS.items():
        d1, d2 = dbar(j, p1, PRIMARY_T), dbar(j, p2, PRIMARY_T)
        row = {"D_bar_P1": d1, "D_bar_P2": d2}
        if d1 and d2:
            row["R"] = d1 / d2; row["lnR"] = math.log(row["R"]); Ls[k] = row["lnR"]
        else:
            row["⛔"] = "결측 — 비율·로그를 만들지 않는다 (카드 §2 결측 규칙)"
        res["parents"][k] = row
    if len(Ls) == 2:
        a, b = Ls["A"], Ls["B"]
        Lb, se = (a + b) / 2, abs(a - b) / 2
        lo, hi = Lb - T_DF1 * se, Lb + T_DF1 * se
        res["primary"].update({
            "L_bar": Lb, "SE": se, "ci_ln": [lo, hi],
            "ratio": math.exp(Lb), "ci_ratio": [math.exp(lo), math.exp(hi)],
            "verdict": verdict_interval(lo, hi, DELTA_LND),
            "⚠_부호": ("두 부모의 부호가 **반대**다" if a * b < 0 else "두 부모 부호 일치")})
    else:
        res["primary"]["⛔"] = (f"유효 부모 {len(Ls)} — A/B 평균·df 1 구간 판정 없음 "
                               f"(카드 §2 실패_전파_규칙 4항)")
    # 2차 ΔEa
    ea, a_k = {}, {}
    for k, (p1, p2) in PAIRS.items():
        e1, e2 = ea_mev(j, p1), ea_mev(j, p2)
        ea[k] = {"Ea_P1_meV": e1, "Ea_P2_meV": e2}
        if e1 is not None and e2 is not None:
            a_k[k] = e1 - e2; ea[k]["a_meV"] = a_k[k]
    res["secondary"] = {"delta_Ea_meV": DELTA_EA_MEV, "per_parent": ea}
    if len(a_k) == 2:
        aa, bb = a_k["A"], a_k["B"]
        ab, sea = (aa + bb) / 2, abs(aa - bb) / 2
        lo, hi = ab - T_DF1 * sea, ab + T_DF1 * sea
        res["secondary"].update({
            "a_bar_meV": ab, "SE_meV": sea, "ci_meV": [lo, hi],
            "verdict": verdict_interval(lo, hi, DELTA_EA_MEV),
            "⚠_부호": ("두 부모의 부호가 **반대**다" if aa * bb < 0 else "두 부모 부호 일치")})
    else:
        res["secondary"]["⛔"] = "두 부모의 ΔEa 가 **모두** 유효해야 한다 (카드 §2 2차)"
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="E′ 파일럿 판정 (카드 v5.2 §2)")
    ap.add_argument("--out_root", default=str(Path.home() / "work/runs/eprime_pilot"))
    ap.add_argument("--out_json", default=None)
    ap.add_argument("--ignore_eligibility", action="store_true",
                    help="⛔ 자격 게이트를 무시하고 집계한다. **인용 금지** — "
                         "'배선을 고쳐 다시 돌리면 결론이 바뀌나' 만 보는 가정 계산이다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    runs = scan(a.out_root)
    print(f"런 {len(runs)} 개 · out_root {a.out_root}")
    if not runs:
        print("⛔ msd.json 을 하나도 못 찾았다 — 경로를 확인할 것"); return 2
    j = judge_runs(runs, ignore_eligibility=a.ignore_eligibility)
    ok = sum(1 for r in j.values() if r["eligible"])
    print(f"자격 통과 {ok}/{len(j)}" + ("  ⛔ **자격 무시 모드**" if a.ignore_eligibility else ""))
    noev = [k for k, r in j.items() if r["events_per_run"] is None]
    if noev:
        print(f"  ⛔ 사건 수를 못 센 런 {len(noev)} 개 — 궤적이 없다 (--save_traj 미사용). "
              f"None 은 통과가 아니라 **검사 불가**다")
    res = aggregate(j)
    res["⚠_부피_조건"] = f"V = {V_COMMON_A3} Å³ · P̄ = **결측** (msd.json 에 없다 — 카드 §2 요구사항 미충족)"
    res["⚠_인용정책"] = "1저자 2026-09-18 — σ·D·Ea 전부 **계 간 상대차로만**. 절대값 인용 금지"
    res["eligibility"] = {"n_runs": len(j), "n_eligible": ok,
                          "ignore_eligibility": bool(a.ignore_eligibility),
                          "n_events_uncountable": len(noev)}
    p = res["primary"]
    if "ratio" in p:
        print(f"\n1차 D_rel(P1/P2; 600 K) — A {res['parents']['A'].get('R'):.3f} · "
              f"B {res['parents']['B'].get('R'):.3f}")
        print(f"  대표 {p['ratio']:.3f} · 95 % 구간 [{p['ci_ratio'][0]:.4f}, {p['ci_ratio'][1]:.1f}]"
              f" · **{p['verdict']}**  ({p['⚠_부호']})")
    else:
        print(f"\n1차: {p['⛔']}")
    s = res["secondary"]
    if "a_bar_meV" in s:
        print(f"2차 ΔEa — A {res['secondary']['per_parent']['A']['a_meV']:+.1f} · "
              f"B {res['secondary']['per_parent']['B']['a_meV']:+.1f} meV")
        print(f"  ā {s['a_bar_meV']:+.1f} · 구간 [{s['ci_meV'][0]:+.0f}, {s['ci_meV'][1]:+.0f}] meV"
              f" · **{s['verdict']}**  ({s['⚠_부호']})")
    else:
        print(f"2차: {s['⛔']}")
    q = a.out_json or os.path.join(a.out_root, "eprime_judgement.json")
    res["rows"] = [{"structure": k[0], "T_K": k[1], "seed": k[2], "D": r["D"],
                    "eligible": r["eligible"], "events_per_run": r["events_per_run"],
                    "t_end_ps": r["t_end_ps"], "reasons": r["reasons"]}
                   for k, r in sorted(j.items())]
    Path(q).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {q}")
    if a.ignore_eligibility:
        print("⛔ 이 산출물은 **인용 금지**다 (자격 게이트를 무시했다)")
    return 0


def _selftest() -> int:
    ok = True
    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m); ok = ok and bool(c)

    chk(parse_tag("P1_Al2O3_A__s1") == ("P1_Al2O3_A", 1), "태그를 (구조, 시드) 로 읽는다")
    chk(parse_tag("H0_host__T600__s1") == ("H0_host", 1),
        "속도시험 태그(__T600__)도 같은 구조·시드로 읽는다")
    chk(parse_tag("garbage") == (None, None), "⛔음성: 모르는 태그는 **None** 이다 (추측하지 않는다)")

    #: 구간 판정 — 위치로만 가른다
    chk(verdict_interval(0.5, 0.9, DELTA_LND) == "실질_차이_지지", "구간 전체가 +δ 위 → 차이 지지")
    chk(verdict_interval(-0.9, -0.5, DELTA_LND) == "실질_차이_지지", "구간 전체가 −δ 아래 → 차이 지지")
    chk(verdict_interval(-0.2, 0.2, DELTA_LND) == "실질_동등_지지", "구간이 등가영역 안 → 동등 지지")
    chk(verdict_interval(-0.2, 0.9, DELTA_LND) == "미결",
        "⛔음성: 걸치면 **미결** — '효과 없음' 으로 읽지 않는다")
    chk(verdict_interval(-5.0, 5.0, DELTA_LND) == "미결", "⛔음성: 아주 넓은 구간도 미결이다")

    def mk(D, used=True):
        return {"D": D, "used": used, "t": [], "y": []}
    base = {}
    for st, d in (("P1_Al2O3_A", 2.5e-6), ("P2_Al2S3_A", 3.6e-6),
                  ("P1_Al2O3_B", 4.2e-6), ("P2_Al2S3_B", 3.0e-6)):
        for T in TEMPS:
            for sd in SEEDS:
                base[(st, T, sd)] = mk(d * (1 + 0.3 * (T - 600) / 200))
    r = aggregate(base)
    chk("ratio" in r["primary"], "[양성] 네 계가 다 있으면 1차 집계가 난다")
    chk(abs(r["parents"]["A"]["R"] - 2.5 / 3.6) < 1e-9,
        f"R_A = D̄_P1/D̄_P2 (기대 {2.5/3.6:.4f}, 실제 {r['parents']['A']['R']:.4f})")
    chk(abs(r["primary"]["ratio"] - math.exp((math.log(2.5/3.6) + math.log(4.2/3.0)) / 2)) < 1e-9,
        "대표 비율은 **기하평균**이다 (산술평균 아님)")
    chk(r["primary"]["⚠_부호"].startswith("두 부모의 부호가 **반대**"),
        f"부모 부호 반대를 집어낸다 ({r['primary']['⚠_부호']})")

    #: ⛔음성 — 시드 하나가 빠지면 그 (p,k) 는 **결측**이고 생존 시드로 대체하지 않는다
    b2 = dict(base); b2[("P1_Al2O3_A", 600, 2)] = mk(2.5e-6, used=False)
    r2 = aggregate(b2)
    chk(r2["parents"]["A"].get("R") is None and "⛔" in r2["parents"]["A"],
        f"⛔음성: 시드 하나 실패 → 그 부모 **결측** ({r2['parents']['A'].get('⛔','')[:30]})")
    chk("ratio" not in r2["primary"] and "⛔" in r2["primary"],
        "⛔음성: 유효 부모가 하나면 **구간 판정을 만들지 않는다**")
    chk("a_bar_meV" not in r2["secondary"],
        "⛔음성: 두 부모의 ΔEa 가 모두 유효해야 2차가 난다")

    #: ⛔음성 — D ≤ 0 은 로그를 만들지 않는다
    b3 = dict(base); b3[("P2_Al2S3_A", 600, 1)] = mk(-1e-9)
    chk(aggregate(b3)["parents"]["A"].get("R") is None,
        "⛔음성: D ≤ 0 이면 비율을 만들지 않는다 (작은 양수로 대체 금지)")

    #: ⛔음성 — 사건 수 None 은 **0 이 아니다**
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        chk(count_events(td) is None,
            "⛔음성: 궤적이 없으면 사건 수가 **None** 이다 (0 이 아니다 — 통과로 읽히면 안 된다)")

    #: Ea 부호 — D 가 T 와 같이 커지면 Ea 는 **양수**다
    flat = {}
    for T in TEMPS:
        for sd in SEEDS:
            flat[("X", T, sd)] = mk(1e-6 * math.exp(-0.25 / (KB_EV * T)) / math.exp(-0.25 / (KB_EV * 600)))
    e = ea_mev(flat, "X")
    chk(e is not None and abs(e - 250.0) < 1.0, f"Ea 를 meV 로 되돌린다 (기대 250, 실제 {e:.1f})")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
