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

X0, X100 = 0.2638452245913298, 0.853974674630047            # Chen2020 창 (§F1 앵커 — 폴백값;
#   각 로그의 OCP 헤더에서 자기 앵커를 파싱해 우선 사용.  수치리뷰 F1/F5(2026-07-17):
#   공유 앵커/공유 areal은 두 전극의 실용량 1.3% 차 때문에 knee 근방에서 최대 4~10 mV
#   가짜 갭을 만들 수 있음 → 앵커·용량은 per-로그가 정본.
_STEP_RE = re.compile(
    r'step\s+(\d+)\s+t=\s*([\d.]+)s\s+\[(\w+)\]\s+V=([\d.]+)\s+I=([\d.eE+-]+)\s+'
    r'x̄=([\d.]+)\s+ηkin=([\d.]+)mV\s+E-bal\s+(-?[\d.eE+-]+)\s+KCL\s+([\d.eE+-]+)'
    r'(?:\s+\(ev\s+(-?\d+),\s+dt\s+([\d.]+)s\))?')       # ev -1 sentinel도 허용 (아니면 dt까지 통째로 유실)
_CAND_RE = re.compile(r'step\s+\d+\s+t=')                    # 후보 라인 (파싱 실패 감지용)
_ANCH_RE = re.compile(r'x0=([\d.]+)\s+x100=([\d.]+)')        # OCP 헤더의 per-런 앵커


_NANINF_RE = re.compile(r'nan|inf', re.I)                   # 발산 스텝 감지 (V=nan 등)


def parse_log(path):
    rows, anch, n_cand, n_div = [], None, 0, 0
    with open(path, errors='replace') as f:
        for ln in f:
            if anch is None:
                ma = _ANCH_RE.search(ln)
                if ma:
                    anch = (float(ma.group(1)), float(ma.group(2)))
            m = _STEP_RE.search(ln)
            if _CAND_RE.search(ln):
                n_cand += 1
                if m is None and _NANINF_RE.search(ln):      # 후보인데 미파싱 + nan/inf = 발산(인코딩 아님)
                    n_div += 1
            if m:
                st, t, ph, V, I, x, eta, eb, kcl, ev, dt = m.groups()
                rows.append(dict(step=int(st), t_s=float(t), phase=ph, V=float(V),
                                 I_A=float(I), x=float(x), eta_kin_mV=float(eta),
                                 ebal=float(eb), kcl=float(kcl),
                                 ev=(int(ev) if ev and int(ev) >= 0 else None),   # -1 sentinel → None
                                 dt_s=float(dt) if dt else None))
    n_miss = n_cand - len(rows)
    if n_div:                                                # 발산 = 솔버 HARD-FAIL, 인코딩 문제 아님 (오진 방지)
        print(f'⚠ {path}: 발산 스텝(nan/inf) {n_div}줄 — 런이 여기서 수렴 실패(HARD-FAIL)해 '
              f'곡선에서 제외됨(정상).  솔버 로그의 HARD-FAIL 메시지를 확인하세요.', file=sys.stderr)
    if n_miss - n_div > 0:                                   # nan/inf 아닌 진짜 미상만 인코딩/줄바꿈 의심
        print(f'⚠ {path}: step-후보 {n_cand}줄 중 {len(rows)}줄만 파싱 '
              f'(발산 {n_div} 제외 {n_miss - n_div}줄 미상) — 로그 인코딩(UTF-8)/줄바꿈 손상 여부 확인',
              file=sys.stderr)
    return rows, anch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('logs', nargs='+', help='LOG[:LABEL[:AREAL_mAh_cm2]] …')
    ap.add_argument('--out', default='step4_curve', help='출력 스템 (.png/.svg/.csv)')
    ap.add_argument('--areal', type=float, default=0.0,
                    help='공통 면적용량 [mAh/cm²] 폴백 — per-시리즈 값(LOG:LABEL:AREAL)이 '
                         '있으면 그쪽 우선.  ⚠ 두 전극 실용량이 다르면(예 3.107 vs 3.066) '
                         '공통값은 knee 근방 비교를 오염시킴 (수치리뷰 F1) — 원고 figure는 '
                         'per-시리즈 필수.')
    ap.add_argument('--x', choices=['soc', 't'], default='soc', help='x축: SOC진행(기본)/시간')
    a = ap.parse_args()

    series = []
    for tok in a.logs:
        parts = tok.split(':')
        path = parts[0]
        lab = parts[1] if len(parts) > 1 and parts[1] else os.path.basename(path).replace('.log', '')
        ar = float(parts[2]) if len(parts) > 2 and parts[2] else a.areal
        rows, anch = parse_log(path)
        if not rows:
            print(f'⚠ {path}: step 라인 없음 (신형 로그인지 확인)', file=sys.stderr)
            continue
        x0, x100 = anch if anch else (X0, X100)              # per-런 앵커 우선 (F1)
        series.append((lab, rows, x0, x100, ar))
        print(f'  {lab}: {len(rows)} steps  t={rows[-1]["t_s"]:.0f}s  '
              f'V {rows[0]["V"]:.4f}→{rows[-1]["V"]:.4f}  x̄→{rows[-1]["x"]:.4f} '
              f'(창 {100*(rows[-1]["x"]-x0)/(x100-x0):.1f}%)'
              + ('' if anch else '  [헤더 앵커 없음 → Chen2020 폴백]')
              + (f'  areal={ar:g}' if ar else ''))
    if not series:
        raise SystemExit('파싱된 시리즈 없음')

    # CSV (전 시리즈 long-form — Origin 재현용).  ⚠ dt_s 열 = 클램프/재시도 前 제안값 (F5) —
    # 적용 스텝폭이 아님; 시간축은 t_s가 정확.
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['label', 'step', 't_s', 'phase', 'V', 'I_A', 'x_mean',
                    'soc_window_pct', 'delivered_mAh_cm2', 'eta_kin_mV', 'ebal', 'kcl', 'ev',
                    'dt_proposed_s'])
        for lab, rows, x0, x100, ar in series:
            for r in rows:
                soc = 100 * (r['x'] - x0) / (x100 - x0)
                w.writerow([lab, r['step'], r['t_s'], r['phase'], r['V'], r['I_A'], r['x'],
                            f'{soc:.3f}', f'{soc / 100 * ar:.4f}' if ar else '',
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
    any_ar = any(s[4] for s in series)
    for i, (lab, rows, x0, x100, ar) in enumerate(series):
        if a.x == 't':
            xs = [r['t_s'] / 60 for r in rows]
        elif ar:
            xs = [(r['x'] - x0) / (x100 - x0) * ar for r in rows]
        else:
            xs = [100 * (r['x'] - x0) / (x100 - x0) for r in rows]
        ax.plot(xs, [r['V'] for r in rows], '-', lw=1.6, color=colors[i % len(colors)], label=lab)
    ax.set_xlabel('Time (min)' if a.x == 't'
                  else (f'Delivered capacity (mAh cm$^{{-2}}$)' if any_ar else 'SOC window delivered (%)'))
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
