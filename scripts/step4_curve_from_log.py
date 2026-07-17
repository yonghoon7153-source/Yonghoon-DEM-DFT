#!/usr/bin/env python3
"""step4_dyn 로그의 per-step 요약 라인 → 방전/충전 곡선 (png+svg+csv 동시 산출).

npz는 런 종료 시에만 저장되지만, 신형 로그(0288533+)는 매 스텝
  step  N t=…s [cc] V=… I=… x̄=… ηkin=…mV E-bal … KCL … (ev N, dt Ns)
를 남기므로 **진행 중에도 부분 곡선**을 뽑을 수 있다 (완주 후 정식 판독은 npz로).

사용:  python3 scripts/step4_curve_from_log.py LOG[:LABEL] [LOG2[:LABEL2] …] \
           [--out step4_c1_partial] [--areal 3.07] [--x soc|t]
  LABEL 생략 시 파일명.  --areal(mAh/cm²) 주면 x축을 면적용량으로 (기본 SOC-창 %).

x̄→SOC 창 % 환산 앵커 (step4_dyn/pybamm export와 동일 §F1, Chen2020 기계추출):
  x0=0.2638452245913298, x100=0.853974674630047
"""
import argparse
import csv
import os
import re
import sys

X0, X100 = 0.2638452245913298, 0.853974674630047            # Chen2020 창 (§F1 앵커)
_STEP_RE = re.compile(
    r'step\s+(\d+)\s+t=\s*([\d.]+)s\s+\[(\w+)\]\s+V=([\d.]+)\s+I=([\d.eE+-]+)\s+'
    r'x̄=([\d.]+)\s+ηkin=([\d.]+)mV\s+E-bal\s+(-?[\d.eE+-]+)\s+KCL\s+([\d.eE+-]+)'
    r'(?:\s+\(ev\s+(\d+),\s+dt\s+([\d.]+)s\))?')


def parse_log(path):
    rows = []
    with open(path, errors='replace') as f:
        for ln in f:
            m = _STEP_RE.search(ln)
            if m:
                st, t, ph, V, I, x, eta, eb, kcl, ev, dt = m.groups()
                rows.append(dict(step=int(st), t_s=float(t), phase=ph, V=float(V),
                                 I_A=float(I), x=float(x), eta_kin_mV=float(eta),
                                 ebal=float(eb), kcl=float(kcl),
                                 ev=int(ev) if ev else None, dt_s=float(dt) if dt else None))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('logs', nargs='+', help='LOG[:LABEL] …')
    ap.add_argument('--out', default='step4_curve', help='출력 스템 (.png/.svg/.csv)')
    ap.add_argument('--areal', type=float, default=0.0,
                    help='면적용량 [mAh/cm²] — 주면 x축이 delivered mAh/cm² (기본: SOC-창 %%)')
    ap.add_argument('--x', choices=['soc', 't'], default='soc', help='x축: SOC진행(기본)/시간')
    a = ap.parse_args()

    series = []
    for tok in a.logs:
        path, _, lab = tok.partition(':')
        lab = lab or os.path.basename(path).replace('.log', '')
        rows = parse_log(path)
        if not rows:
            print(f'⚠ {path}: step 라인 없음 (신형 로그인지 확인)', file=sys.stderr)
            continue
        series.append((lab, rows))
        print(f'  {lab}: {len(rows)} steps  t={rows[-1]["t_s"]:.0f}s  '
              f'V {rows[0]["V"]:.4f}→{rows[-1]["V"]:.4f}  x̄→{rows[-1]["x"]:.4f} '
              f'(창 {100*(rows[-1]["x"]-X0)/(X100-X0):.1f}%)')
    if not series:
        raise SystemExit('파싱된 시리즈 없음')

    # CSV (전 시리즈 long-form — Origin 재현용)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['label', 'step', 't_s', 'phase', 'V', 'I_A', 'x_mean',
                    'soc_window_pct', 'delivered_mAh_cm2', 'eta_kin_mV', 'ebal', 'kcl', 'ev', 'dt_s'])
        for lab, rows in series:
            for r in rows:
                soc = 100 * (r['x'] - X0) / (X100 - X0)
                w.writerow([lab, r['step'], r['t_s'], r['phase'], r['V'], r['I_A'], r['x'],
                            f'{soc:.3f}', f'{soc / 100 * a.areal:.4f}' if a.areal else '',
                            r['eta_kin_mV'], r['ebal'], r['kcl'], r['ev'], r['dt_s']])

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print(f'matplotlib 없음 → CSV만 저장: {a.out}.csv')
        return
    fig, ax = plt.subplots(figsize=(4.6, 3.5), dpi=300)
    colors = ['#1f6fb2', '#d1495b', '#2e8b57', '#e0a100']
    for i, (lab, rows) in enumerate(series):
        if a.x == 't':
            xs = [r['t_s'] / 60 for r in rows]
        elif a.areal:
            xs = [(r['x'] - X0) / (X100 - X0) * a.areal for r in rows]
        else:
            xs = [100 * (r['x'] - X0) / (X100 - X0) for r in rows]
        ax.plot(xs, [r['V'] for r in rows], '-', lw=1.6, color=colors[i % len(colors)], label=lab)
    ax.set_xlabel('Time (min)' if a.x == 't'
                  else (f'Delivered capacity (mAh cm$^{{-2}}$)' if a.areal else 'SOC window delivered (%)'))
    ax.set_ylabel('Cell voltage (V vs Li/Li$^+$)')
    ax.legend(frameon=False, fontsize=9)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(a.out + '.png')
    fig.savefig(a.out + '.svg')
    print(f'saved {a.out}.png / .svg / .csv')


if __name__ == '__main__':
    main()
