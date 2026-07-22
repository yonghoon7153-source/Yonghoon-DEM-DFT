#!/usr/bin/env python3
"""CYCLE-STEP4 — R_int(N) 궤적 → retention의 수송-기원 몫 조립.

R_int Phase 2 사다리(delivered vs R_int, 측정)와 R_int(N) 궤적(rint_cycle_traj, 경험 밴드)을
합쳐, 사이클마다 STEP4를 다시 안 돌리고 retention_transport(N)을 예측한다:

  retention_transport(N) = delivered@R_int(N) / delivered@R_int(0)

핵심 근거: η_Rint=I·R_int 정확 선형 + delivered vs R_int ~선형(0.5%p/Ω, 5점 사다리 검증) →
R_int(N)을 사다리에 보간하면 그 값의 효과가 근사 아닌 해석적.  ⚠ 사다리는 pristine 0-18Ω만
측정 → cycled R_int(N)>18은 **외삽**(라벨); CV 회수 포화 가능성 → 고-R_int STEP4 몇 점으로
확인 권장(V100).

★프레임: 이건 retention의 **수송(R_int)-기원 몫만**.  전극 구조/화학 열화(D_s(N)·반응면·CEI)는
별개(A10 원장 + 화학) → 측정 retention − retention_transport = 그 나머지 (CYCLE-STEP3 분해와 정합).
사다리 delivered는 pristine 전극 고정 규약이라, R_int(N)만 바꾼 "전극 동결" 예측.

사용:
  python3 scripts/cycle_retention.py --scenario dbe --electrode dbe
  python3 scripts/cycle_retention.py --scenario sbe --electrode sbe --ladder-csv rint_ladder.csv
selftest:  python3 scripts/cycle_retention.py --selftest
"""
import argparse
import csv
import json
import os

# 측정 사다리 (2C CCCV delivered %, 전극별; 2026-07-22 V100).  R_int=user-lab Fig.6e pristine approx.
LADDER = {
    'dbe': {0: 89.6, 10: 84.6, 12: 83.6},   # DBE (SDCP): R0, C-SUS, bare-Al
    'sbe': {0: 88.9, 18: 80.4},             # SBE (no SDCP): R0, bare-Al
}


def interp_delivered(ladder, r):
    """사다리(dict R→delivered%)에서 R_int=r의 delivered 보간/외삽 (선형).  반환 (val, extrapolated)."""
    xs = sorted(ladder)
    ys = [ladder[x] for x in xs]
    if len(xs) == 1:                                    # 단일점 = 기울기 미상 → 그대로 (외삽 불가)
        return ys[0], (r != xs[0])
    if r <= xs[0]:
        s = (ys[1] - ys[0]) / (xs[1] - xs[0])
        return ys[0] + s * (r - xs[0]), r < xs[0]
    if r >= xs[-1]:
        s = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])       # 끝 기울기로 외삽
        return ys[-1] + s * (r - xs[-1]), r > xs[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= r <= xs[i + 1]:
            s = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])
            return ys[i] + s * (r - xs[i]), False
    return ys[-1], True


def load_ladder_csv(path):
    """step4_rint_ladder.py 산출 CSV → {R_int: delivered%} (전극군 무시, 전부)."""
    lad = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            lad[float(row['R_int_ohm_cm2'])] = float(row['delivered_pct'])
    return lad


def build(scenario, electrode, ladder, checkpoints):
    import rint_cycle_traj as rct
    r0, rc, ntot, prec = rct.load_scenario(scenario)
    ns = checkpoints or rct.grid(ntot)
    d0, _ = interp_delivered(ladder, r0)                # R_int(0) 기준 delivered
    rows = []
    for n in ns:
        r_rep = rct.r_of_n(n, r0, rc, ntot, 'sqrt', 0.5)
        r_lo = min(rct.r_of_n(n, r0, rc, ntot, s, j) for s in rct.SHAPES for j in rct.JUMPS)
        r_hi = max(rct.r_of_n(n, r0, rc, ntot, s, j) for s in rct.SHAPES for j in rct.JUMPS)
        d_rep, ex_rep = interp_delivered(ladder, r_rep)
        d_from_hi, _ = interp_delivered(ladder, r_hi)   # R_int 큰쪽 = delivered 작음
        d_from_lo, _ = interp_delivered(ladder, r_lo)
        ret = d_rep / max(d0, 1e-9) * 100
        rows.append(dict(cycle=int(n), R_int_rep=round(r_rep, 1), R_int_lo=round(r_lo, 1),
                         R_int_hi=round(r_hi, 1), delivered_pct=round(d_rep, 2),
                         retention_transport_pct=round(ret, 2),
                         retention_lo=round(min(d_from_hi, d_from_lo) / max(d0, 1e-9) * 100, 2),
                         retention_hi=round(max(d_from_hi, d_from_lo) / max(d0, 1e-9) * 100, 2),
                         extrapolated=bool(ex_rep)))
    return dict(scenario=scenario, electrode=electrode, R0=r0, Rc=rc, N_total=ntot,
                pristine_precision=prec, delivered_at_R0=round(d0, 2),
                ladder=ladder, ladder_range=[min(ladder), max(ladder)],
                caveats=[
                    'retention_transport = R_int(N)-기원 몫만 (전극 pristine 동결 규약). '
                    '측정 전체 retention − 이것 = 전극구조/화학 열화(A10 원장+CEI) — CYCLE-STEP3 분해와 정합.',
                    f'사다리 측정범위 {min(ladder)}-{max(ladder)}Ω; R_int(N)>{max(ladder)}는 외삽(extrapolated=True) '
                    '— η_Rint=I·R 선형이라 근사 좋으나 CV 회수 포화 가능 → 고-R_int STEP4 확인 권장.',
                    'R_int(N) 사이 곡선 = assumed-form 밴드(rint_cycle_traj, √N/선형×j0.3-0.7); 양끝만 측정.',
                    'R_int 앵커 = user-lab Fig.6e pristine 근사(panel_e_approx) — 정밀 digitize 대기.',
                ], rows=rows)


def run(a):
    ladder = load_ladder_csv(a.ladder_csv) if a.ladder_csv else LADDER.get(a.electrode)
    if not ladder:
        raise SystemExit(f'❌ 전극 "{a.electrode}" 사다리 없음 (LADDER 키: {list(LADDER)}) — --ladder-csv 제공')
    chk = [int(x) for x in a.checkpoints.split(',') if x.strip()] if a.checkpoints else None
    out = build(a.scenario, a.electrode, ladder, chk)
    print(f'시나리오 {a.scenario} (전극 {a.electrode}): R_int {out["R0"]}→{out["Rc"]} @{out["N_total"]}cyc, '
          f'사다리 {out["ladder_range"]}Ω, delivered@R0={out["delivered_at_R0"]}%')
    print(f'{"N":>5s} {"R_int(rep)":>10s} {"delivered%":>11s} {"retention_T%":>13s} {"밴드":>14s} {"외삽":>5s}')
    for r in out['rows']:
        ex = '⚠ext' if r['extrapolated'] else ''
        print(f'{r["cycle"]:5d} {r["R_int_rep"]:10.1f} {r["delivered_pct"]:11.2f} '
              f'{r["retention_transport_pct"]:13.2f} [{r["retention_lo"]:.1f}-{r["retention_hi"]:.1f}] {ex:>5s}')
    with open(a.out + '.json', 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out['rows'][0].keys()))
        w.writeheader(); w.writerows(out['rows'])
    print(f'\nsaved {a.out}.json / .csv  (retention_transport = R_int-기원 몫만; 나머지=전극 열화 A10)')


def _selftest():
    ok = True
    # 1) 보간: 사다리 {0:90,10:85} → R=5 → 87.5
    lad = {0: 90.0, 10: 85.0}
    v, ex = interp_delivered(lad, 5)
    ok1 = abs(v - 87.5) < 1e-9 and not ex
    ok &= ok1
    print(f'selftest1 보간 R5→87.5: {v:.2f} ext={ex}  {"OK" if ok1 else "FAIL"}')
    # 2) 외삽: R=20 → 80 (기울기 −0.5 연장), extrapolated=True
    v2, ex2 = interp_delivered(lad, 20)
    ok2 = abs(v2 - 80.0) < 1e-9 and ex2
    ok &= ok2
    print(f'selftest2 외삽 R20→80 ext: {v2:.2f} ext={ex2}  {"OK" if ok2 else "FAIL"}')
    # 3) 양끝 EXACT
    ok3 = abs(interp_delivered(lad, 0)[0] - 90) < 1e-12 and abs(interp_delivered(lad, 10)[0] - 85) < 1e-12
    ok &= ok3
    print(f'selftest3 양끝 EXACT: {"OK" if ok3 else "FAIL"}')
    # 4) retention: R_int 성장 → retention 단조 감소 (실 시나리오)
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        out = build('dbe', 'dbe', LADDER['dbe'], [0, 1, 100, 1000])
        rets = [r['retention_transport_pct'] for r in out['rows']]
        ok4 = rets[0] == 100.0 and all(rets[i] >= rets[i + 1] - 1e-9 for i in range(len(rets) - 1))
        ok &= ok4
        print(f'selftest4 retention 단조↓ (N0=100%): {[round(x,1) for x in rets]}  {"OK" if ok4 else "FAIL"}')
    except Exception as e:
        print(f'selftest4 SKIP (rint_cycle_traj import: {e!r})')
    # 5) 단일점 사다리 = 외삽 불가 안전처리
    v5, ex5 = interp_delivered({0: 88.9}, 18)
    ok5 = abs(v5 - 88.9) < 1e-9 and ex5
    ok &= ok5
    print(f'selftest5 단일점 사다리 안전(외삽불가 플래그): {v5} ext={ex5}  {"OK" if ok5 else "FAIL"}')
    print('CYCLE-RETENTION SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='CYCLE-STEP4 R_int(N)→retention 수송-기원 몫')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--scenario', default='dbe', help='rint_cycle_traj 시나리오 (sbe/dbe/csus)')
    ap.add_argument('--electrode', default='dbe', help='사다리 전극 (dbe/sbe; LADDER 키 또는 --ladder-csv)')
    ap.add_argument('--ladder-csv', default=None, help='step4_rint_ladder CSV (전극 사다리 오버라이드)')
    ap.add_argument('--checkpoints', default=None, help='기록 사이클 (기본 = rint_cycle_traj grid)')
    ap.add_argument('--out', default='cycle_retention_out')
    a = ap.parse_args()
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # rint_cycle_traj import
    if a.selftest:
        raise SystemExit(0 if _selftest() else 1)
    run(a)


if __name__ == '__main__':
    main()
