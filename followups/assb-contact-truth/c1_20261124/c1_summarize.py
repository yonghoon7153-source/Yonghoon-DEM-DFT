"""C1 보고용 요약 — c1_analyze 가 쓴 표 · JSON 을 읽어 README · 보고 표를 만든다 (읽기만 · 판정 계산 없음 · 4 차 규칙 고정 뒤 작성).

사용: python -I c1_summarize.py --csv <run4_tables> --grid <out4/grid>
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def rd(p):
    p = Path(p)
    if not p.exists() or p.stat().st_size == 0:
        return []
    return list(csv.DictReader(open(p)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--grid", required=True)
    a = ap.parse_args()
    c = Path(a.csv)
    g = Path(a.grid)
    gen = rd(c / "c1a_general.csv")
    if gen:
        print("## C1a 일반 문장 표 (f = 0.5 · 48 칸)")
        print("| Δt | σ_V | ΔR0 | 가른다 | 경계 | 못 가른다 | 비율 | 일반 문장 | 정칙화 조건 |")
        print("|---|---|---|---|---|---|---|---|---|")
        for r in gen:
            print(f"| {r['dt_s']} s | {r['sigma_V']} V | {r['dR0']} | {r['n_separate']} | {r['n_boundary']} | {r['n_cannot']} | "
                  f"{float(r['frac_separate']):.3f} | {'허용' if r['sentence_allowed'] == 'True' else '불가'} | {r['reg_condition']} |")
    fs = rd(c / "c1a_fstar.csv")
    if fs:
        print("\n## C1a f* 분포 (칸 48 · 대표 f 셋 안 최대 '가른다' f)")
        cnt = defaultdict(Counter)
        for r in fs:
            cnt[(r["dt_s"], r["sigma_V"], r["dR0"])][r["f_star"] or "—"] += 1
        print("| Δt | σ_V | ΔR0 | 0.7071 | 0.5 | 0.25 | 없음 |")
        print("|---|---|---|---|---|---|---|")
        for k, v in cnt.items():
            print(f"| {k[0]} s | {k[1]} V | {k[2]} | {v.get('0.707107', 0)} | {v.get('0.5', 0)} | {v.get('0.25', 0)} | {v.get('—', 0)} |")
    vd = rd(c / "c1a_verdicts.csv")
    if vd:
        print("\n## C1a f = 0.5 판정 (ΔR0 none) — Wa × 모양 별 '가른다' 칸 수 (각 12 칸)")
        cnt = defaultdict(Counter)
        for r in vd:
            if r["k"] == "4" and r["dR0"] == "none":
                cnt[(r["dt_s"], r["sigma_V"])][(r["Wa"], r["shape"], r["verdict"])] += 1
        cols = [(w, s) for w in ("10", "0.1") for s in ("G05", "G2")]
        print("| Δt | σ_V | " + " | ".join(f"Wa{w} {s}" for w, s in cols) + " |")
        print("|---|---|" + "---|" * len(cols))
        for k, v in cnt.items():
            print(f"| {k[0]} s | {k[1]} V | " + " | ".join(str(v.get((w, s, "가른다"), 0)) for w, s in cols) + " |")
        nan = Counter((r["dt_s"], r["n_nan"] != "0") for r in vd if r["k"] == "4" and r["dR0"] == "none")
        print("\n미해상 (MC τ̂ NaN ≥ 1) 칸 수 (f = 0.5 · σ 두 판 합):",
              {k[0]: n for k, n in nan.items() if k[1]})
    ex = rd(c / "c1a_expectation.csv")
    if ex:
        print("\n## §5-4 예상 대조 (관측 배율 ÷ 예측 배율 − 1 · |최대| · 중앙값) — Wa 10 · 선형")
        print("| 팔 | 특징 | n | max |dev| | median dev |")
        print("|---|---|---|---|---|")
        for r in ex:
            if r["Wa"] == "10" and r["amp"] == "lin":
                print(f"| {r['arm']} | {r['feature']} | {r['n']} | {float(r['max_abs_rel_dev_from_prediction']):.3g} | {float(r['median_rel_dev']):.3g} |")
    sig = rd(c / "c1a_signature.csv")
    if sig:
        print("\n## 서명 (f = 0.5 · 잡음 0 · truth Δt) — A ÷ K 의 τ · C 중앙값 (Wa × 진폭)")
        acc = defaultdict(list)
        for r in sig:
            if r["k"] == "4":
                for nm in ("tau", "C", "Rp", "R0"):
                    v = r.get(f"AoverK_{nm}", "")
                    if v not in ("", "nan"):
                        acc[(r["Wa"], r["amp"], nm)].append(float(v))
        import statistics as st
        print("| Wa | 진폭 | A/K τ | A/K C | A/K R_p | A/K R0 |")
        print("|---|---|---|---|---|---|")
        for w in ("10", "0.1"):
            for amp in ("lin", "taf"):
                vals = [st.median(acc[(w, amp, nm)]) if acc[(w, amp, nm)] else float("nan") for nm in ("tau", "C", "Rp", "R0")]
                print(f"| {w} | {amp} | " + " | ".join(f"{v:.3f}" for v in vals) + " |")
    dz = g / "dc" / "dc_z.json"
    if dz.exists():
        d = json.loads(dz.read_text())
        print("\n## DC 영 채널")
        print(f"보정 (Q_F 축 · 판정) z_max = {d['z_max_qf']:.4g} · 시간 축 (진단) z_max = {d['z_max_time_diag']:.4g} · 중단 {d['stop_rule3a']} · 문제 {d['problems']}")
        for r in d["z_rows_qf_decision"]:
            if r["dR0"] == "none":
                print(f"  Q_F Wa{r['Wa']} {r['rate']} f{r['f']:.3f}: z {r['z']:.4g} (같은 f 직접 {r['z_direct_same_f']:.4g}) · n {r['n_samples']}")
        for r in d["z_rows_time_diagnostic"]:
            if r["dR0"] == "none":
                print(f"  time Wa{r['Wa']} {r['rate']} f{r['f']:.3f}: z {r['z']:.4g}")
    for tag in ("c1b", "ad_c1b"):
        p = c / f"{tag}_summary.json"
        if p.exists():
            s = json.loads(p.read_text())
            print(f"\n## {tag}")
            for w, v in s.items():
                print(f"- Wa {w}: 실행 {v['n_runs_ok']} · |S| {v['S_size']} · 막힌 표적 {v['blocked_targets']} · 읽기: {v['reading']}")
                print(f"  O 범위 {v['O_ranges']}")
                print(f"  첫 충전 상한 — θ = 1 실행의 상한 값 범위 {v['bound_theta1_range']} · θ = 0.96: 위반 {v['bound_violations_theta096']} · "
                      f"느슨함 {v['looseness_theta096_range']} · 참 θ 몫 {v['true_share_theta096_range']}")
    ad = rd(c / "ad_c1a_zmap.csv")
    if ad:
        print("\n## AD ↔ K z (f = 0.5 · ΔR0 none · σ 1 mV) 최댓값 / 최솟값 (48 칸)")
        acc = defaultdict(list)
        for r in ad:
            if r["k"] == "4" and r["dR0"] == "none" and r["sigma_V"] == "0.001":
                acc[r["dt_s"]].append(float(r["z"]))
        for k, v in acc.items():
            print(f"  Δt {k}: max {max(v):.3g} · min {min(v):.3g} · z ≥ 5 칸 {sum(x >= 5 for x in v)}")
    adz = rd(c / "ad_dc_z_qf.csv")
    if adz:
        print("AD DC (Q_F) z_max:", max(float(r["z"]) for r in adz))


if __name__ == "__main__":
    main()
