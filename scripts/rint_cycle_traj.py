#!/usr/bin/env python3
"""경험 R_int(N) 사이클 궤적 — A11-② (R_int 프로젝트, 열화율 축).

두 측정 앵커(pristine R(0), cycled R(N_total) — docs/data/rint_eis_anchors.csv 시나리오 키)를
문헌-앵커 성장-법칙 SHAPE(docs/rint_reference_growthlaw_design.md §3)로 잇는다:

    R(N) = R0 + ΔR_form·1(N≥1) + k·g(N/N_total),   g ∈ {√(N/Nt), N/Nt}
    ΔR_form = j·(R_c − R0),  k = (1−j)·(R_c − R0)   → R(0)=R0, R(Nt)=R_c EXACT (양끝 앵커 고정)

⚠ §F1 정직 (필수 라벨):
  • 양끝 R0/R_c = 측정(user-lab, pristine은 panel_e_approx).  **사이 곡선 = assumed-form** —
    첫-사이클 점프 비율 j 와 g(N)의 √N-vs-선형은 문헌이 SHAPE만 주고 계수는 미확정
    (Koerver "majority in 1st charge" 정성; Conforto per-cycle 테이블 = WSL PDF gap).
  • 그래서 단일 곡선이 아니라 **밴드**로 출력: shape {sqrt, linear} × j {0.3, 0.5, 0.7} = 6곡선의
    min/max envelope.  체크포인트 STEP4 런은 대표(sqrt, j=0.5) + 밴드 폭을 같이 보고.
  • 이것은 접촉저항 축의 "경험 열화"일 뿐 — 진짜 구조 열화(부피변화·CZM)는 A10 소관.

사용:
  python3 scripts/rint_cycle_traj.py --scenario csus            # C-SUS 10→30
  python3 scripts/rint_cycle_traj.py --scenario sbe --checkpoints 0,1,10,100,300,1000
  → CSV(R(N) 밴드) + PNG + STEP4 체크포인트 명령 출력 (MPM_S4_RINT=R(N) step4_only.sh 재사용)

selftest:  python3 scripts/rint_cycle_traj.py --selftest
"""
from __future__ import annotations
import argparse
import csv
import math
import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
ANCHOR_CSV = os.path.join(ROOT, 'docs', 'data', 'rint_eis_anchors.csv')

SHAPES = ('sqrt', 'linear')
JUMPS = (0.3, 0.5, 0.7)          # 첫-사이클 점프 비율 스윕 (미확정 → 밴드)


def load_scenario(name: str):
    """anchors CSV의 scenario_key {name}_pristine / {name}_cycled → (R0, Rc, N_total)."""
    rows = {}
    with open(ANCHOR_CSV) as f:
        for r in csv.DictReader(f):
            if r.get('scenario_key'):
                rows[r['scenario_key']] = r
    kp, kc = f'{name}_pristine', f'{name}_cycled'
    if kp not in rows or kc not in rows:
        raise SystemExit(f'scenario {name}: {kp}/{kc} 키가 {ANCHOR_CSV}에 없음 '
                         f'(있는 키: {sorted(rows)})')
    r0 = float(rows[kp]['value'])
    rc = float(rows[kc]['value'])
    # cycle_n 형식 '1000@2C' → 1000
    ntot = int(str(rows[kc]['cycle_n']).split('@')[0])
    prec = rows[kp]['precision']
    return r0, rc, ntot, prec


def r_of_n(n, r0, rc, ntot, shape, jump):
    """양끝-고정 경험 궤적 (assumed-form)."""
    if n <= 0:
        return r0
    d = rc - r0
    g = math.sqrt(n / ntot) if shape == 'sqrt' else (n / ntot)
    return r0 + jump * d + (1.0 - jump) * d * g if n >= 1 else r0


def grid(ntot):
    g = [0, 1, 2, 5, 10, 20, 50, 100, 200, 300, 500, 700, 1000]
    return [n for n in g if n <= ntot] + ([ntot] if ntot not in g else [])


def build(scenario, checkpoints=None):
    r0, rc, ntot, prec = load_scenario(scenario)
    ns = grid(ntot)
    fam = {(s, j): [r_of_n(n, r0, rc, ntot, s, j) for n in ns]
           for s in SHAPES for j in JUMPS}
    lo = [min(fam[k][i] for k in fam) for i in range(len(ns))]
    hi = [max(fam[k][i] for k in fam) for i in range(len(ns))]
    rep = [r_of_n(n, r0, rc, ntot, 'sqrt', 0.5) for n in ns]   # 대표 곡선 (라벨 필수)
    out = {'scenario': scenario, 'R0': r0, 'Rc': rc, 'N_total': ntot,
           'pristine_precision': prec, 'N': ns,
           'R_rep_sqrt_j05': rep, 'R_band_lo': lo, 'R_band_hi': hi,
           'trust': 'ENDPOINTS measured (pristine=panel_e_approx); curve BETWEEN = assumed-form '
                    '(shape sqrt/linear × jump 0.3-0.7 band) — Conforto per-cycle digitize 전까지. '
                    '접촉저항 축만 (구조 열화 아님 = A10 별도)'}
    if checkpoints:
        out['checkpoints'] = {int(n): round(r_of_n(int(n), r0, rc, ntot, 'sqrt', 0.5), 1)
                              for n in checkpoints}
    return out


def _selftest():
    ok = True
    # 합성 앵커로 양끝 고정 검증 (전 shape×jump)
    r0, rc, nt = 10.0, 30.0, 1000
    for s in SHAPES:
        for j in JUMPS:
            e0 = abs(r_of_n(0, r0, rc, nt, s, j) - r0) < 1e-12
            e1 = abs(r_of_n(nt, r0, rc, nt, s, j) - rc) < 1e-12
            mono = all(r_of_n(a, r0, rc, nt, s, j) <= r_of_n(b, r0, rc, nt, s, j) + 1e-12
                       for a, b in zip([0, 1, 10, 100, 500], [1, 10, 100, 500, 1000]))
            ok &= e0 and e1 and mono
            print(f'  {s:6s} j={j}: R(0)={r_of_n(0,r0,rc,nt,s,j):.1f} '
                  f'R(1000)={r_of_n(1000,r0,rc,nt,s,j):.1f} monotone={mono} '
                  f"{'OK' if (e0 and e1 and mono) else 'FAIL'}")
    # 첫점프: j=0.5면 R(1) ≈ R0 + 0.5·ΔR + (작은 g항)
    r1 = r_of_n(1, r0, rc, nt, 'sqrt', 0.5)
    e = r0 + 0.5 * (rc - r0) <= r1 <= r0 + 0.55 * (rc - r0)
    ok &= e
    print(f'  first-jump: R(1)={r1:.2f} (expect 20.0–21.0)  {"OK" if e else "FAIL"}')
    # CSV 시나리오 로드 (리포 앵커 실측 키)
    try:
        d = build('csus')
        e = d['R0'] == 10.0 and d['Rc'] == 30.0 and d['N_total'] == 1000
        ok &= e
        print(f"  csus anchors: R0={d['R0']} Rc={d['Rc']} Nt={d['N_total']}  {'OK' if e else 'FAIL'}")
    except SystemExit as ex:
        ok = False
        print(f'  csus anchors: FAIL ({ex})')
    print('RINT-TRAJ SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scenario', choices=('sbe', 'dbe', 'csus', 'sus'), default='csus')
    ap.add_argument('--checkpoints', default='0,1,10,100,300,1000',
                    help='STEP4 체크포인트 사이클들 (comma)')
    ap.add_argument('--out-csv', default='', help='R(N) 밴드 CSV 저장 경로 (기본: 출력만)')
    ap.add_argument('--png', default='', help='궤적+밴드 PNG 저장 경로 (matplotlib 있을 때)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    cks = [int(x) for x in a.checkpoints.split(',') if x.strip() != '']
    d = build(a.scenario, cks)
    print(f"scenario {a.scenario}: R(0)={d['R0']} → R({d['N_total']})={d['Rc']} Ω·cm² "
          f"(pristine {d['pristine_precision']})")
    print(f"  trust: {d['trust']}")
    print(f"  {'N':>6} {'R_rep(sqrt,j0.5)':>16} {'band_lo':>8} {'band_hi':>8}")
    for i, n in enumerate(d['N']):
        print(f"  {n:>6} {d['R_rep_sqrt_j05'][i]:>16.2f} {d['R_band_lo'][i]:>8.2f} "
              f"{d['R_band_hi'][i]:>8.2f}")
    print('\n  STEP4 체크포인트 명령 (기존 grid 재사용, 산출물 _rint<값> 태그 자동):')
    for n, r in d['checkpoints'].items():
        print(f'    # cycle N={n}  (R_int={r} — assumed-form 대표곡선, 밴드 병기해 해석)')
        print(f'    MPM_S4_RINT={r} bash step4_only.sh <run_dir>')
    if a.out_csv:
        with open(a.out_csv, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['# ' + d['trust']])
            w.writerow(['N', 'R_rep_sqrt_j05', 'R_band_lo', 'R_band_hi'])
            for i, n in enumerate(d['N']):
                w.writerow([n, f"{d['R_rep_sqrt_j05'][i]:.2f}",
                            f"{d['R_band_lo'][i]:.2f}", f"{d['R_band_hi'][i]:.2f}"])
        print(f'  saved {a.out_csv}')
    if a.png:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        ax.fill_between(d['N'], d['R_band_lo'], d['R_band_hi'], alpha=.25, color='#6c8cff',
                        label='assumed-form band (sqrt/linear × j 0.3–0.7)')
        ax.plot(d['N'], d['R_rep_sqrt_j05'], '-o', ms=3.5, color='#1f4e9c',
                label='representative (√N, j=0.5) — NOT measured')
        ax.plot([0, d['N_total']], [d['R0'], d['Rc']], 's', ms=8, color='#d1495b',
                label='measured endpoints (user-lab)')
        ax.set_xlabel('cycle N')
        ax.set_ylabel('R_int (Ω·cm²)')
        ax.set_title(f"empirical R_int(N) — {a.scenario} ({d['R0']}→{d['Rc']}, "
                     f"pristine {d['pristine_precision']})")
        ax.legend(fontsize=8, frameon=False)
        ax.grid(alpha=.25, lw=.5)
        fig.tight_layout()
        fig.savefig(a.png, dpi=150)
        print(f'  saved {a.png}')


if __name__ == '__main__':
    main()
