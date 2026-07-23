#!/usr/bin/env python3
"""B-1 화학(CEI) N-전개 → 총 R_int(N) = ledger 접촉 + B-1 화학 (STEP5, 2026-07-23).

접촉-기계 fade(ledger, ~2%)는 작으니 진짜 열화는 화학 계면상(CEI) 성장이 지배(~98%).  이 도구는:
  총 R_int(N) = R_int_0 + ΔR_contact(N)[ledger 실측 shape] + ΔR_chem(N)[CEI 성장법칙]
을 실험 총 R_int 끝점(예: 너 랩 SBE 6.1×/DBE 3.8× @1000cyc)에 **앵커**해 궤적을 낸다.

★ 정직 (적대리뷰 교훈):
  - **끝점(magnitude)은 실험 앵커** (defensible).
  - **모양(shape)은 ASSUMED-FORM**: √N(확산제한 CEI 두께, 기본) or 선형(--shape linear).  검증 =
    실험 R_int(N) **곡선**(≥4 N점) 필요 — 끝점 하나론 √N/선형 구별 불가(--shape 스윕으로 노출).
  - **접촉 몫은 ledger 실측**(fade JSON), 화학 = 나머지(=총−접촉) → 접촉/화학 분해가 정직.
  - 흑연-SEI 계수 이식 금지(N1); √N은 CEI 두께 일반형만.

사용:
  python3 scripts/b1_chem_fade.py --fade fade_real14.json --rint0 18 --rint-exp-x 6.1 \
      --n-exp 1000 --r-contact0 2.0 --shape sqrt --label SBE --out rint_N_SBE
"""
import argparse
import json
import sys


def _shape(N, n_exp, kind):
    """정규화 성장 모양 (N=0→0, N=n_exp→1).  sqrt=확산제한 CEI, linear=일정속도."""
    if kind == 'sqrt':
        return (float(N) / n_exp) ** 0.5
    if kind == 'linear':
        return float(N) / n_exp
    raise ValueError(kind)


def trajectory(fade_json, rint0, rint_exp_x, n_exp, r_contact0, shape, chem_x=None):
    """chem_x=None → 화학=나머지(bare NCM 가정, 옛 방식).  chem_x 지정 → 화학 성장 ×를 명시
    (코팅 NCM = CEI 억제 → 작게) → 나머지 = OTHER(골격재배열·SE분해·Li쪽 = 우리 모델 밖)."""
    d = json.load(open(fade_json))
    tr = d['trajectory']
    ledger_N = [r['cycle'] for r in tr]
    ledger_rct = {r['cycle']: r['rct_holm_rel'] for r in tr}

    def rct_rel_at(N):
        # ledger R_ct rel 보간 (앵커 N점 사이 = ledger 자체 궤적, 최근접-계단은 피하고 선형)
        ks = sorted(ledger_rct)
        if N <= ks[0]:
            return ledger_rct[ks[0]]
        if N >= ks[-1]:
            return ledger_rct[ks[-1]]
        for i in range(len(ks) - 1):
            if ks[i] <= N <= ks[i + 1]:
                t = (N - ks[i]) / (ks[i + 1] - ks[i])
                return ledger_rct[ks[i]] * (1 - t) + ledger_rct[ks[i + 1]] * t
        return ledger_rct[ks[-1]]

    dR_total_exp = rint0 * (rint_exp_x - 1.0)                 # 실험 총 성장 Δ (Ω·cm²) @ n_exp
    dR_contact_exp = r_contact0 * (rct_rel_at(n_exp) - 1.0)   # 접촉 몫 @ n_exp (ledger, ★하한 = frozen-AM)
    if chem_x is None:
        dR_chem_exp = max(0.0, dR_total_exp - dR_contact_exp)  # bare 가정: 화학=나머지
        dR_other_exp = 0.0
    else:                                                     # 코팅 인식: 화학=명시(억제), OTHER=나머지
        dR_chem_exp = rint0 * (chem_x - 1.0)
        dR_other_exp = max(0.0, dR_total_exp - dR_contact_exp - dR_chem_exp)   # 골격재배열·SE분해·Li (모델 밖)

    Ns = sorted(set([0] + ledger_N + [n_exp] + [n_exp // 10, n_exp // 4, n_exp // 2]))
    rows = []
    for N in Ns:
        dR_contact = r_contact0 * (rct_rel_at(N) - 1.0)
        dR_chem = dR_chem_exp * _shape(N, n_exp, shape)      # ★shape ASSUMED, endpoint 앵커
        dR_other = dR_other_exp * _shape(N, n_exp, shape)    # OTHER도 같은 모양(미상)
        R = rint0 + dR_contact + dR_chem + dR_other
        rows.append({'N': N, 'R_int': R, 'dR_contact': dR_contact, 'dR_chem': dR_chem,
                     'dR_other': dR_other, 'R_int_x': R / rint0, 'ledger_rct_rel': rct_rel_at(N)})
    return {'rows': rows, 'rint0': rint0, 'rint_exp_x': rint_exp_x, 'n_exp': n_exp,
            'r_contact0': r_contact0, 'shape': shape, 'chem_x': chem_x,
            'chem_share_pct': 100.0 * dR_chem_exp / max(dR_total_exp, 1e-9),
            'contact_share_pct': 100.0 * dR_contact_exp / max(dR_total_exp, 1e-9),
            'other_share_pct': 100.0 * dR_other_exp / max(dR_total_exp, 1e-9)}


def _report(out, label):
    print('=' * 88)
    print(f'B-1 화학 N-전개 → 총 R_int(N)  [{label}]  ★shape={out["shape"]} ASSUMED · endpoint 실험앵커')
    print('-' * 88)
    print(f"  {'N':>6} {'R_int(Ω·cm²)':>13} {'×pristine':>10} {'ΔR_chem':>9} {'ΔR_contact':>11}")
    for r in out['rows']:
        print(f"  {r['N']:>6} {r['R_int']:>13.1f} {r['R_int_x']:>10.2f} {r['dR_chem']:>9.1f} {r['dR_contact']:>11.2f}")
    print('-' * 88)
    if out['chem_x'] is None:
        print(f"  분해 @N{out['n_exp']}: 화학 {out['chem_share_pct']:.1f}% / 접촉-기계 {out['contact_share_pct']:.1f}% "
              f"(→ 화학 CEI 지배; ★bare NCM 가정 = 화학이 나머지)  ·  R_int0={out['rint0']} → ×{out['rint_exp_x']}")
    else:
        print(f"  분해 @N{out['n_exp']}: 화학 {out['chem_share_pct']:.1f}%(코팅 억제, ×{out['chem_x']}) / "
              f"접촉-기계 {out['contact_share_pct']:.1f}%(ledger 하한) / ★OTHER {out['other_share_pct']:.1f}% "
              f"(골격재배열·SE분해·Li — 우리 모델 밖)  ·  R_int0={out['rint0']} → ×{out['rint_exp_x']}")
        print(f"  ⚠ 코팅 NCM = CEI 억제 → 화학 작음 → 나머지 OTHER가 지배 = 현 모델(화학·frozen-AM 접촉) 미포착 gap.")
    print(f"  ⚠ shape(√N vs 선형)는 끝점 하나론 구별 불가 — 실험 R_int(N) 곡선(≥4점)으로 검증.  --shape 스윕 권장.")
    print('=' * 88)


def _plot(out, label, prefix):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return
    rows = out['rows']
    N = [r['N'] for r in rows]
    Rc = [out['rint0'] for _ in rows]                        # baseline
    Rcon = [out['rint0'] + r['dR_contact'] for r in rows]
    Rchem = [out['rint0'] + r['dR_contact'] + r['dR_chem'] for r in rows]
    Rtot = [r['R_int'] for r in rows]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.fill_between(N, 0, Rc, color='#bdc3c7', label='R_int_0 (pristine)')
    ax.fill_between(N, Rc, Rcon, color='#2980b9', label='+ contact-mech (ledger, ~%.0f%%)' % out['contact_share_pct'])
    ax.fill_between(N, Rcon, Rchem, color='#e67e22', label='+ chemical CEI (~%.0f%%)' % out['chem_share_pct'])
    if out['chem_x'] is not None and out.get('other_share_pct', 0) > 0.5:
        ax.fill_between(N, Rchem, Rtot, color='#c0392b', alpha=0.55,
                        label='+ OTHER unmodeled (~%.0f%%: skeleton/SE/Li)' % out['other_share_pct'])
    ax.plot(N, Rtot, 'k-o', lw=1.5, ms=3, label='total R_int(N)')
    ax.axhline(out['rint0'] * out['rint_exp_x'], color='#c0392b', ls='--', lw=1,
               label='exp anchor x%.1f @N%d' % (out['rint_exp_x'], out['n_exp']))
    ax.set_xlabel('cycle N')
    ax.set_ylabel('R_int (Ohm.cm2)')
    ax.set_title('STEP5 total R_int(N) = contact(ledger) + chemical(B-1, %s) [%s]' % (out['shape'], label),
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')
    ax.text(0.5, -0.16, 'shape=%s ASSUMED-FORM (endpoint anchored to experiment; curve validation pending)'
            % out['shape'], transform=ax.transAxes, ha='center', fontsize=7.5, color='#888')
    fig.tight_layout()
    fn = f'{prefix}.png'
    fig.savefig(fn, dpi=130, bbox_inches='tight')
    print(f'  saved -> {fn}')


def main(argv):
    ap = argparse.ArgumentParser(description='B-1 화학 N-전개 → 총 R_int(N)')
    ap.add_argument('--fade', required=True, help='ledger fade JSON (접촉 R_ct 궤적)')
    ap.add_argument('--rint0', type=float, required=True, help='pristine R_int (Ω·cm²)')
    ap.add_argument('--rint-exp-x', type=float, required=True, help='실험 총 R_int 성장 × @ n-exp')
    ap.add_argument('--n-exp', type=int, default=1000, help='실험 끝점 사이클')
    ap.add_argument('--r-contact0', type=float, default=2.0, help='pristine 접촉 R 성분 (Ω·cm², ledger rel 곱함)')
    ap.add_argument('--shape', default='sqrt', choices=['sqrt', 'linear'], help='CEI 성장 모양(ASSUMED)')
    ap.add_argument('--chem-x', type=float, default=None,
                    help='화학 R 성장 × @n_exp (코팅 NCM = CEI 억제 → 작게, 예 1.3).  미지정 = 화학이 나머지'
                         '(bare 가정).  지정 시 나머지 = OTHER(골격재배열·SE분해·Li = 모델 밖) 노출.')
    ap.add_argument('--label', default='case', help='라벨 (SBE/DBE 등)')
    ap.add_argument('--out', default='rint_N', help='PNG prefix')
    a = ap.parse_args(argv)
    out = trajectory(a.fade, a.rint0, a.rint_exp_x, a.n_exp, a.r_contact0, a.shape, a.chem_x)
    _report(out, a.label)
    _plot(out, a.label, a.out)


if __name__ == '__main__':
    main(sys.argv[1:])
