#!/usr/bin/env python3
"""current-focusing 비교 컬러바 생성 — joint 상한 = 케이스-최대(안 잘림) + 천장 케이스 명시.

문제(사용자 지적 2026-07-23): "joint reference = σ-max case"로 상한을 잡으면 @1C에선 케이스가 뒤바뀌어
(전류가 rate-고정이라 focusing 큰 케이스가 피크 최대) 다른 케이스가 **잘림(clip)**.
  - 전자: @1V은 σ_e 큰 A(σ-max)가 최대, @1C은 focusing 큰 B가 최대 → 프레임별 천장 케이스 다름.
  - 이온: σ_ion 거의 같아 B(focusing-max)가 @1V·@1C 모두 최대.
이 도구는 채널·프레임별로 **max-across-cases**를 천장으로 잡고 어느 케이스인지 라벨한다.

@1C 환산: ⟨J⟩_1C = 면적용량(mAh/cm²) × 1C = mA/cm²;  peak = ⟨J⟩_1C × focusing(p99.8).
@1V(수송, 선형): peak = ⟨J_ch⟩(A/cm²@1V) × focusing.

사용:
  python3 scripts/plot_focusing_colorbar.py            # 내장 A/B(SDCP/baseline) 예시
  python3 scripts/plot_focusing_colorbar.py --json cases.json --out cb   # 사용자 데이터
JSON = [{"name":"A","Je_mean_A_cm2":414,"Jion_mean_A_cm2":0.0296,"focus_e":67.37,
         "focus_ion":32.75,"cap_mAh_cm2":3.07}, {...B...}]
"""
import argparse
import json
import sys

# 내장 예시 = 사용자 표 (A=SDCP σ_e 3.0 / B=baseline σ_e 1.98)
_DEFAULT = [
    {'name': 'A (SDCP)',     'Je_mean_A_cm2': 414.0, 'Jion_mean_A_cm2': 0.0296, 'focus_e': 67.37, 'focus_ion': 32.75, 'cap_mAh_cm2': 3.07},
    {'name': 'B (baseline)', 'Je_mean_A_cm2': 273.0, 'Jion_mean_A_cm2': 0.0281, 'focus_e': 87.70, 'focus_ion': 37.78, 'cap_mAh_cm2': 3.11},
]


def ceilings(cases):
    """채널·프레임별 joint 상한 + 천장 케이스."""
    out = {}
    for ch, mean_key, foc_key in (('e', 'Je_mean_A_cm2', 'focus_e'), ('ion', 'Jion_mean_A_cm2', 'focus_ion')):
        rows = []
        for c in cases:
            foc = float(c[foc_key])
            rows.append({
                'name': c['name'], 'focus': foc,
                'v1_A_cm2': float(c[mean_key]) * foc,                       # @1V absolute (A/cm²)
                'c1_mA_cm2': float(c['cap_mAh_cm2']) * foc,                 # @1C absolute (mA/cm² = cap×1C×focus)
            })
        norm_top = max(rows, key=lambda r: r['focus'])
        v1_top = max(rows, key=lambda r: r['v1_A_cm2'])
        c1_top = max(rows, key=lambda r: r['c1_mA_cm2'])
        out[ch] = {'rows': rows,
                   'norm_top': (norm_top['focus'], norm_top['name']),
                   'v1_top': (v1_top['v1_A_cm2'], v1_top['name']),
                   'c1_top': (c1_top['c1_mA_cm2'], c1_top['name'])}
    return out


def _report(cs):
    print('=' * 92)
    print('current-focusing joint 컬러바 상한 (max-across-cases = 안 잘림) + 천장 케이스')
    print('=' * 92)
    for ch, label in (('e', '전자 |J_e|'), ('ion', '이온 |J_ion|')):
        d = cs[ch]
        print(f'\n── {label} ──')
        print(f"  {'case':>14} {'focus×⟨J⟩':>10} {'@1V (A/cm²)':>14} {'@1C (mA/cm²)':>14}")
        for r in d['rows']:
            print(f"  {r['name']:>14} {r['focus']:>10.2f} {r['v1_A_cm2']:>14.4g} {r['c1_mA_cm2']:>14.1f}")
        nt, nn = d['norm_top']; vt, vn = d['v1_top']; ct, cn = d['c1_top']
        print(f"  ★ joint 상한: 정규화 ×{nt:.1f} ({nn}) · @1V {vt:.4g} A/cm² ({vn}) · "
              f"@1C {ct:.1f} mA/cm² ({cn})")
    print('\n  ⚠ 천장 케이스가 프레임별로 다를 수 있음(전자: @1V=σ-max, @1C=focusing-max).')
    print('    @1C은 전류가 rate-고정이라 focusing 큰 케이스가 피크 최대 → σ-max 아님.')
    print('  ⚠ p99.8 상한 = 상위 0.2% 실질피크(clip); 절대 max는 조금 더 위.  @1V은 선형-외삽(운전점 아님).')


def _render(cs, out_prefix):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print('  (matplotlib 없음 — 표만; PNG 생략)')
        return
    for ch, label in (('e', '|J_e|'), ('ion', '|J_ion|')):
        d = cs[ch]
        nt, nn = d['norm_top']
        ct, cn = d['c1_top']
        vt, vn = d['v1_top']
        fig, ax = plt.subplots(figsize=(10, 1.7))
        grad = np.linspace(0, 1, 256).reshape(1, -1)
        ax.imshow(grad, aspect='auto', cmap='jet', extent=[0, nt, 0, 1])
        ax.set_yticks([])
        ax.set_xlim(0, nt)
        ax.set_title(f'{label} / <J_z> current-focusing (p99.8, sigma-joint = max-across-cases)',
                     fontsize=12, fontweight='bold', loc='left')
        # English labels only (portable font; Korean explanation is in the console table)
        ax.set_xlabel(
            f'joint top = x{nt:.1f} <J>   |   @1V {vt:.3g} A/cm2 ({vn}, sigma-max)   |   '
            f'@1C {ct:.0f} mA/cm2 ({cn}, focusing-max)   '
            f'[ceiling case differs by frame; p99.8 clip]', fontsize=9, color='#444')
        fig.tight_layout()
        fn = f'{out_prefix}_{ch}.png'
        fig.savefig(fn, dpi=130, bbox_inches='tight')
        plt.close(fig)
        print(f'  saved → {fn}')


def main(argv):
    ap = argparse.ArgumentParser(description='current-focusing joint 컬러바 (max-across-cases)')
    ap.add_argument('--json', help='케이스 데이터 JSON (없으면 내장 A/B 예시)')
    ap.add_argument('--out', default='focusing_cb', help='PNG prefix')
    ap.add_argument('--no-plot', action='store_true')
    a = ap.parse_args(argv)
    cases = json.load(open(a.json)) if a.json else _DEFAULT
    cs = ceilings(cases)
    _report(cs)
    if not a.no_plot:
        _render(cs, a.out)


if __name__ == '__main__':
    main(sys.argv[1:])
