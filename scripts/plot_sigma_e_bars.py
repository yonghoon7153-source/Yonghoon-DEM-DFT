#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ_e 가로 막대 그림 — 원고 Fig 4b 형식 (SBE 위 · DBE 아래 · 값은 막대 끝).

    python3 scripts/plot_sigma_e_bars.py --dir docs/data/ion8_isd0_20260831
    python3 scripts/plot_sigma_e_bars.py --selftest

★ 값은 **팔 payload 에서 다시 계산한다** — 저장된 요약을 읽지 않는다 (인계 §3-4).
⚠ 이 그림이 대체하는 것: 옛 패널 (b) 의 `1.98 → 3.00 S/cm` 는 vox 0.4 세대의 **철회값**이다.
  단위도 바뀐다 — 현 세대는 **mS/cm** 규모다.
⚠ origin 8팔 산포는 **그리지 않는다** (저자 결정) — 그것은 모델 견고성이지 독자의 값이 아니다.
"""
import argparse
import glob
import json
import os
import sys

YLABEL = r'$\sigma_\mathrm{e}$ (mS cm$^{-1}$)'
BEDS = ('SBE', 'DBE')


def read(dir_):
    """{bed: [σ_e ...]} (mS/cm).  파일명이 아니라 **팔마다 실려 있는 값**을 읽는다."""
    out = {b: [] for b in BEDS}
    for f in sorted(glob.glob(os.path.join(dir_, 'p2_*.json'))):
        s = json.load(open(f, encoding='utf-8')).get('step3') or {}
        v = s.get('sigma_e_eff_S_cm')
        if v is None:
            raise SystemExit(f'{os.path.basename(f)}: sigma_e_eff_S_cm 이 없다')
        bed = 'SBE' if '_SBE_' in os.path.basename(f) else (
              'DBE' if '_DBE_' in os.path.basename(f) else None)
        if bed is None:
            raise SystemExit(f'{os.path.basename(f)}: 침대를 파일명에서 못 읽는다')
        out[bed].append(float(v) * 1000.0)                 # S/cm → mS/cm
    for b in BEDS:
        if not out[b]:
            raise SystemExit(f'{dir_}: {b} 팔이 없다')
    if len(out['SBE']) != len(out['DBE']):
        raise SystemExit(f'팔 수 불일치 SBE {len(out["SBE"])} · DBE {len(out["DBE"])}')
    return out


def summarise(d):
    import statistics as st
    return {b: dict(mean=st.fmean(d[b]), n=len(d[b]),
                    lo=min(d[b]), hi=max(d[b])) for b in BEDS}


def write_csv(path, d, s):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('bed,arm_index,sigma_e_mS_cm\n')
        for b in BEDS:
            for i, v in enumerate(d[b]):
                fh.write(f'{b},{i},{v:.6f}\n')
    with open(path.replace('.csv', '_origin.csv'), 'w', encoding='utf-8') as fh:
        #  Origin wide — 막대는 침대별 평균 한 값이므로 요약을 낸다 (⚠ 주석줄 없음).
        fh.write('bed,sigma_e (mS cm-1)\n')
        for b in BEDS:
            fh.write(f'{b},{s[b]["mean"]:.2f}\n')


def plot(s, out_base):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pos = [2, 1]                                   # SBE 위 · DBE 아래
    vals = [s[b]['mean'] for b in BEDS]
    fig, ax = plt.subplots(figsize=(3.6, 1.6), dpi=300)
    ax.barh(pos, vals, height=0.55, color=('#d97b7b', '#7b93d9'),
            edgecolor=('#b85f5f', '#5f74b8'), linewidth=0.8)
    for p, v in zip(pos, vals):
        ax.annotate(f'{v:.2f}', (v, p), xytext=(6, 0), textcoords='offset points',
                    va='center', ha='left', fontsize=9, color='#11161c')
    ax.set_yticks(pos); ax.set_yticklabels(BEDS, fontsize=9)
    ax.set_xlabel(YLABEL, fontsize=9)
    ax.set_xlim(0, max(vals) * 1.22)
    ax.tick_params(labelsize=8.5)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ('svg', 'png'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight')
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default=os.path.join('docs', 'data', 'ion8_isd0_20260831'))
    ap.add_argument('--out', default=os.path.join('docs', 'figures', 'sigma_e_bars'))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    d = read(a.dir)
    s = summarise(d)
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    write_csv(a.out + '.csv', d, s)
    plot(s, a.out)
    #  ★ 비는 **쌍대응 비의 산술평균**이다 (원장 규약) — mean/mean 이 아니다.
    paired = sum(d['DBE'][i] / d['SBE'][i] for i in range(s['SBE']['n'])) / s['SBE']['n']
    for b in BEDS:
        print(f'  {b}  mean {s[b]["mean"]:.2f} mS/cm  (n={s[b]["n"]} 팔, {s[b]["lo"]:.2f}–{s[b]["hi"]:.2f})')
    print(f'\n  비(쌍대응 산술평균) {paired:.6f}   ⚠ 팔 산포는 그림에 그리지 않는다 (저자 결정)')
    print(f'산출: {a.out}.svg · .png · .csv · _origin.csv')
    return 0


def selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    chk('축 라벨 단위가 mS/cm 다 (옛 패널의 S/cm 아님)', 'mS cm' in YLABEL)
    with tempfile.TemporaryDirectory() as td:
        def mk(bed, i, v):
            json.dump({'step3': {'sigma_e_eff_S_cm': v}},
                      open(os.path.join(td, f'p2_{bed}_sph_a{i}.json'), 'w'))
        for i in range(3):
            mk('SBE', i, 0.05 + i * 1e-3); mk('DBE', i, 0.07 + i * 1e-3)
        d = read(td); s = summarise(d)
        chk('S/cm → mS/cm 환산', abs(s['SBE']['mean'] - 51.0) < 1e-9)
        chk('팔을 전부 읽는다', s['SBE']['n'] == 3 and s['DBE']['n'] == 3)

        #  ★★ 음성 대조 — 팔 수가 어긋나면 거부한다 (한쪽만 완주한 디렉터리를 그리면 안 된다)
        mk('DBE', 3, 0.073)
        try:
            read(td); chk('★★ 팔 수 불일치는 거부', False)
        except SystemExit as ex:
            chk('★★ 팔 수 불일치는 거부', '팔 수 불일치' in str(ex))
        os.remove(os.path.join(td, 'p2_DBE_sph_a3.json'))

        #  σ 가 없는 팔은 조용히 건너뛰지 않는다
        json.dump({'step3': {}}, open(os.path.join(td, 'p2_SBE_sph_a9.json'), 'w'))
        try:
            read(td); chk('σ 없는 팔은 실패시킨다', False)
        except SystemExit as ex:
            chk('σ 없는 팔은 실패시킨다', 'sigma_e_eff_S_cm 이 없다' in str(ex))
        os.remove(os.path.join(td, 'p2_SBE_sph_a9.json'))

        d = read(td); s = summarise(d)
        p = os.path.join(td, 'o.csv'); write_csv(p, d, s)
        rows = open(p, encoding='utf-8').read().strip().split('\n')
        chk('CSV 가 팔별 원값', len(rows) == 7 and rows[0] == 'bed,arm_index,sigma_e_mS_cm')
        ow = open(p.replace('.csv', '_origin.csv'), encoding='utf-8').read().strip().split('\n')
        chk('Origin CSV 는 주석줄 없이 wide', len(ow) == 3 and not ow[0].startswith('#'))
        try:
            plot(s, os.path.join(td, 'f'))
            chk('SVG·PNG 를 낸다', all(os.path.exists(os.path.join(td, 'f.' + e))
                                     for e in ('svg', 'png')))
        except Exception as ex:                                    # noqa: BLE001
            chk(f'SVG·PNG 를 낸다 ({ex})', False)

    print('\n✓ plot_sigma_e_bars selftest PASS' if ok else '\n✗ plot_sigma_e_bars selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
