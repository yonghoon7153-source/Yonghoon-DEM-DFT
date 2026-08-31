#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AM 입자당 도전재 접점 분포 그림 — SVG · PNG · CSV 동시 산출.

    python3 scripts/plot_cbd_contacts.py --out docs/figures/cbd_contacts
    python3 scripts/plot_cbd_contacts.py --selftest

★ 무엇을 그리나: `cbd_contacts_per_am.py` 가 낸 **AM 별 접점 수** 1,271개의 분포를
  침대별로 나란히.  중앙값 74 → 86 은 이 분포의 중앙선이다 (원장 §18).

⚠ 이 그림이 **뷰어 콜러바와 다른 양**이다.  콜러바는 AM 근접 탄소 **점밀도**(점을 센다,
  섬유 하나 = 점 수십~수백)이고 이쪽은 **개체 수**(섬유 하나 = 1)다.  섞어 읽으면 안 된다.

⚠ 규약 의존이다 — band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.  그래서 규약을
  파일명과 CSV 헤더에 **함께** 싣는다 (숫자만 떠도 규약이 따라간다).
"""
import argparse
import json
import os
import sys

COND = 'conductive only (VGCF+SDCP)'
WITH_PTFE = 'conductive+PTFE'
DATA = os.path.join('docs', 'data', 'cbd_contacts_20260831')
#: 논문 축 라벨.  ⛔ `CBD` 로 부르지 않는다 — CBD 는 carbon-**binder** domain 이라
#  PTFE 포함을 함의하는데 이 값은 도전상만 센다 (포함하면 80 → 88 로 달라진다).
YLABEL = 'Conductive-additive contacts per AM particle'


def load(data_dir=DATA, key=COND):
    """{bed: counts[]} + 규약.  파일이 자기 규약을 들고 있어야 한다."""
    out, conv = {}, None
    for bed in ('SBE', 'DBE'):
        p = os.path.join(data_dir, f'contacts_{bed}_band015.json')
        d = json.load(open(p, encoding='utf-8'))
        if key not in d:
            raise SystemExit(f'{p}: 규약 키 {key!r} 가 없다 (있는 것: {list(d)})')
        out[bed] = list(d[key]['counts'])
        c = d[key]['convention']
        this = (c.get('band_um'), c.get('include_ptfe'), c.get('representation'))
        if conv is None:
            conv = this
        elif conv != this:
            raise SystemExit(f'{p}: 두 침대의 규약이 다르다 {conv} vs {this}')
    return out, dict(band_um=conv[0], include_ptfe=conv[1], representation=conv[2])


def stats(v):
    import statistics as st
    s = sorted(v)
    return dict(n=len(s), median=st.median(s), mean=round(st.fmean(s), 2),
                p10=s[len(s) // 10], p90=s[-max(1, len(s) // 10)],
                min=s[0], max=s[-1], zero=sum(1 for x in s if x == 0))


def write_csv(path, data, conv=None):
    """CSV 는 **AM 별 원값**을 낸다 — 요약만 내면 그림을 재현할 수 없다.

    ⚠ 첫 줄에 **규약을 주석으로 싣는다.**  이 값은 band 폭·개체 정의·PTFE 포함 여부에
    따라 달라지므로(74→86 vs 89→112 vs 80→88), CSV 가 규약 없이 떠돌면 재현 불가다.
    """
    with open(path, 'w', encoding='utf-8') as fh:
        if conv:
            fh.write(f'# convention: band_um={conv.get("band_um")} · '
                     f'contacts = distinct conductive objects outside the AM surface · '
                     f'{conv.get("representation")}\n')
        fh.write('bed,am_index,contacts\n')
        for bed in ('SBE', 'DBE'):
            for i, v in enumerate(data[bed]):
                fh.write(f'{bed},{i},{v}\n')


def plot(data, conv, out_base):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    beds = ('SBE', 'DBE')
    vals = [data[b] for b in beds]
    fig, ax = plt.subplots(figsize=(3.4, 3.2), dpi=300)

    parts = ax.violinplot(vals, positions=[1, 2], widths=0.7,
                          showmeans=False, showmedians=False, showextrema=False)
    for pc, c in zip(parts['bodies'], ('#8aa0b8', '#c9784f')):
        pc.set_facecolor(c); pc.set_alpha(0.45); pc.set_edgecolor('none')
    bp = ax.boxplot(vals, positions=[1, 2], widths=0.16, showfliers=False,
                    patch_artist=True, medianprops=dict(color='#11161c', lw=1.4),
                    whiskerprops=dict(color='#4a5766'), capprops=dict(color='#4a5766'),
                    boxprops=dict(facecolor='white', edgecolor='#4a5766'))
    del bp
    for x, b in zip((1, 2), beds):
        m = stats(data[b])['median']
        ax.annotate(f'{m:g}', (x, m), textcoords='offset points', xytext=(16, -3),
                    fontsize=9, color='#11161c')

    ax.set_xticks([1, 2]); ax.set_xticklabels(beds)
    ax.set_ylabel(YLABEL, fontsize=8.5)
    ax.tick_params(labelsize=9)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.grid(axis='y', color='#e3e8ee', lw=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    for ext in ('svg', 'png'):
        fig.savefig(f'{out_base}.{ext}', bbox_inches='tight')
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--data', default=DATA)
    ap.add_argument('--out', default=os.path.join('docs', 'figures', 'cbd_contacts'))
    ap.add_argument('--include-ptfe', action='store_true',
                    help='PTFE 를 도전 도메인에 넣는다 (대조 규약 — 기본은 도전상만)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    data, conv = load(a.data, WITH_PTFE if a.include_ptfe else COND)
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    write_csv(a.out + '.csv', data, conv)
    plot(data, conv, a.out)
    for b in ('SBE', 'DBE'):
        s = stats(data[b])
        print(f'  {b}  median {s["median"]}  mean {s["mean"]}  p10–p90 {s["p10"]}–{s["p90"]}'
              f'  min–max {s["min"]}–{s["max"]}  접촉 0 인 AM {s["zero"]}/{s["n"]}')
    print(f'\n규약: band {conv["band_um"]} µm · include_ptfe={conv["include_ptfe"]} · '
          f'{conv["representation"]}')
    print(f'산출: {a.out}.svg · .png · .csv')
    print('⚠ 이 값은 규약 의존이다 — band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.')
    return 0


def selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    #  ★ 라벨이 `CBD` 로 되돌아가는 것을 막는다 — CBD 는 바인더 포함을 함의하는데
    #    이 값은 도전상만 센다 (포함하면 80 → 88 로 달라진다).
    chk('축 라벨이 CBD 를 쓰지 않는다', 'CBD' not in YLABEL and 'cbd' not in YLABEL)
    chk('축 라벨이 개체 단위를 말한다', 'contacts per AM particle' in YLABEL)

    with tempfile.TemporaryDirectory() as td:
        def mk(bed, counts, band=0.15, inc=False):
            j = {COND: {'summary': stats(counts), 'counts': counts,
                        'convention': {'band_um': band, 'include_ptfe': inc,
                                       'representation': 'mpm_material_points'}}}
            json.dump(j, open(os.path.join(td, f'contacts_{bed}_band015.json'), 'w'))
        mk('SBE', [1, 2, 3, 4, 5]); mk('DBE', [3, 4, 5, 6, 7])
        d, c = load(td)
        chk('원값을 그대로 읽는다', d['SBE'] == [1, 2, 3, 4, 5] and c['band_um'] == 0.15)

        #  ★★ 음성 대조 — 두 침대의 **규약이 다르면 거부**한다.  band 가 다른 두 파일을
        #    한 그림에 그리면 74→86 과 89→112 를 섞는 것이고, 그림은 멀쩡해 보인다.
        mk('DBE', [3, 4, 5, 6, 7], band=0.30)
        try:
            load(td); chk('★★ 규약이 다른 두 침대는 거부', False)
        except SystemExit as ex:
            chk('★★ 규약이 다른 두 침대는 거부', '규약이 다르다' in str(ex))

        mk('DBE', [3, 4, 5, 6, 7])
        try:
            load(td, '없는규약'); chk('없는 규약 키는 거부', False)
        except SystemExit as ex:
            chk('없는 규약 키는 거부', '규약 키' in str(ex))

        #  CSV 는 AM 별 원값이어야 한다 (요약만 내면 그림 재현 불가)
        p = os.path.join(td, 'o.csv'); write_csv(p, d, c)
        rows = open(p, encoding='utf-8').read().strip().split('\n')
        chk('CSV 가 AM 별 원값 전부 (규약주석 + 헤더 + 10행)',
            len(rows) == 12 and rows[0].startswith('# convention:')
            and rows[1] == 'bed,am_index,contacts')
        chk('★ CSV 주석이 band 를 들고 다닌다', 'band_um=0.15' in rows[0])

        try:
            plot(d, c, os.path.join(td, 'fig'))
            chk('SVG·PNG 를 낸다', all(os.path.exists(os.path.join(td, 'fig.' + e))
                                     for e in ('svg', 'png')))
        except Exception as ex:                                    # noqa: BLE001
            chk(f'SVG·PNG 를 낸다 ({ex})', False)

    print('\n✓ plot_cbd_contacts selftest PASS' if ok else '\n✗ plot_cbd_contacts selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
