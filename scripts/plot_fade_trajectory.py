#!/usr/bin/env python3
"""ledger fade(N) 정직-분해 그림 — 접촉-기계 몫(ledger) vs 실험 총 R_int(N).

cycle_contact_ledger.py --recontact forbid 출력(fade JSON)을 받아 fade(N) 궤적 + 실험 총 R_int 끝점과의
정직한 분해를 그린다.  ★핵심 메시지(적대리뷰 확증): 접촉-기계 fade(R_ct~1.1×)는 총 fade(실험 3.8~6.1×)의
작은 몫 → 화학(B-1 CEI)이 지배.  frame[5] 분업: MPM/ledger=방향·기전, 크기=화학+실험.

정직 라벨(그림에 박음): N-스케일 ASSUMED(δcr/gap) · 포화 모양=Miner+상수구동(검증된 법칙 아님) ·
접촉-기계 채널만(화학=B-1, 취성=FEM 별개) · 실험 곡선(≥4 N) 앵커 대기.

사용:
  python3 scripts/plot_fade_trajectory.py --fade fade_real14.json --out fade_real14
  (실험 총 끝점 override: --exp-total-x SBE:6.1,DBE:3.8 --exp-cycle 1000)
"""
import argparse
import json
import sys


def main(argv):
    ap = argparse.ArgumentParser(description='ledger fade(N) 정직-분해 그림')
    ap.add_argument('--fade', required=True, help='cycle_contact_ledger --out 의 fade JSON')
    ap.add_argument('--out', default='fade_traj', help='PNG prefix')
    ap.add_argument('--exp-total-x', default='SBE:6.1,DBE:3.8',
                    help='실험 총 R_int 배수 끝점 (라벨:배수, 쉼표) — 기본 = user lab Fig6e @1000cyc')
    ap.add_argument('--exp-cycle', type=int, default=1000, help='실험 끝점 사이클 N')
    a = ap.parse_args(argv)

    d = json.load(open(a.fade))
    tr = d['trajectory']
    N = [r['cycle'] for r in tr]
    fbrk = [100.0 * r['f_broken_amse'] for r in tr]
    rct_holm = [r['rct_holm_rel'] for r in tr]
    rct_ct = [r['rct_ct_area_rel'] for r in tr]
    exp = {}
    for kv in a.exp_total_x.split(','):
        k, v = kv.split(':')
        exp[k] = float(v)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('  matplotlib 없음 — 표만:')
        for r in tr:
            print(f"    N={r['cycle']:4d}  f_broken={100*r['f_broken_amse']:5.1f}%  "
                  f"R_ct(Holm)={r['rct_holm_rel']:.3f}× (CT {r['rct_ct_area_rel']:.3f}×)")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))

    # Panel 1: fade(N) trajectory (contact-mechanical)
    ax1b = ax1.twinx()
    ln1 = ax1.plot(N, fbrk, 'o-', color='#c0392b', label='f_broken (AM-SE), %')
    ln2 = ax1b.plot(N, rct_holm, 's--', color='#2980b9', label='R_ct rel (Holm)')
    ln3 = ax1b.plot(N, rct_ct, '^:', color='#8e44ad', label='R_ct rel (CT area)')
    ax1.set_xscale('log')
    ax1.set_xlabel('cycle N (log)')
    ax1.set_ylabel('f_broken (AM-SE contacts), %', color='#c0392b')
    ax1b.set_ylabel('R_ct relative (x)', color='#2980b9')
    ax1.set_title('ledger contact-mechanical fade(N)  [recontact=forbid]', fontsize=11, fontweight='bold')
    lns = ln1 + ln2 + ln3
    ax1.legend(lns, [l.get_label() for l in lns], fontsize=8, loc='upper left')
    ax1.text(0.5, -0.30,
             'ASSUMED N-scale (delta_cr/gap) . saturating shape = Miner+const-driver (NOT a validated law) . '
             'contact-mechanical channel only',
             transform=ax1.transAxes, ha='center', fontsize=7.5, color='#888', wrap=True)

    # Panel 2: honest decomposition — contact-mechanical vs experimental total
    rct_end = rct_holm[-1]
    labels = ['ledger\ncontact-mech\n(R_ct, N=%d)' % N[-1]] + [f'exp TOTAL\nR_int\n({k}, N={a.exp_cycle})' for k in exp]
    vals = [rct_end] + [exp[k] for k in exp]
    colors = ['#2980b9'] + ['#e67e22'] * len(exp)
    bars = ax2.bar(range(len(vals)), vals, color=colors)
    ax2.set_xticks(range(len(vals)))
    ax2.set_xticklabels(labels, fontsize=8)
    ax2.set_ylabel('R growth (x pristine)')
    ax2.set_title('Honest decomposition: contact-mechanical is a SMALL share', fontsize=11, fontweight='bold')
    for b, v in zip(bars, vals):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.05, f'{v:.2f}x', ha='center', fontsize=9, fontweight='bold')
    ax2.axhline(1.0, color='#aaa', lw=0.8, ls=':')
    ax2.text(0.5, -0.22,
             'contact-mechanical (%.2fx) << experimental total (%.1f-%.1fx) => CHEMICAL (B-1 CEI) DOMINATES. '
             'frame[5]: MPM/ledger=direction, magnitude=chemistry+experiment.'
             % (rct_end, min(exp.values()), max(exp.values())),
             transform=ax2.transAxes, ha='center', fontsize=7.5, color='#888', wrap=True)

    fig.suptitle('Real degrading electrode — HONEST fade(N) decomposition (A-1/A-3, 2026-07-23)',
                 fontsize=12, fontweight='bold')
    fig.tight_layout(rect=[0, 0.05, 1, 0.96])
    fn = f'{a.out}.png'
    fig.savefig(fn, dpi=130, bbox_inches='tight')
    print(f'  saved -> {fn}')
    print(f'  ledger R_ct(N={N[-1]}) = {rct_end:.3f}x (Holm) . exp total = {exp} @N{a.exp_cycle} '
          f'=> contact-mechanical share ~ {100*(rct_end-1)/(max(exp.values())-1):.0f}% of total')


if __name__ == '__main__':
    main(sys.argv[1:])
