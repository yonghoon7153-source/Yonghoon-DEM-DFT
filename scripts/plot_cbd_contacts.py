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


def write_origin_csv(path, data, conv=None):
    """Origin 용 **wide** CSV — 열 하나가 침대 하나 (박스/바이올린 그룹 플롯의 표준 입력).

    ⚠ 주석줄(`#`)을 넣지 않는다 — Origin 이 데이터로 읽는다.  대신 규약을 **열 이름**에
    실어 보낸다.  Origin 은 첫 행을 Long Name 으로 가져가므로 규약이 워크시트에 그대로
    남고, CSV 가 혼자 떠돌아도 band 를 잃지 않는다.
    """
    band = (conv or {}).get('band_um')
    tag = f' ({band} um band)' if band is not None else ''
    beds = ('SBE', 'DBE')
    cols = [data[b] for b in beds]
    n = max(len(c) for c in cols)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(','.join(f'{b} contacts per AM{tag}' for b in beds) + '\n')
        for i in range(n):
            fh.write(','.join(str(c[i]) if i < len(c) else '' for c in cols) + '\n')


def plot(data, conv, out_base, horizontal=False, violin=True):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    #  ★ `horizontal` 은 원고 Fig 4b 의 기존 형식(가로 · SBE 위 · 값은 끝에)에 맞춘 판이다.
    #    랩 규약: 그림 요청 시 **기존 figure format 을 재현**한다.
    beds = ('SBE', 'DBE')
    vals = [data[b] for b in beds]
    #  가로판은 위에서부터 SBE·DBE 로 읽히도록 y 를 뒤집는다 (matplotlib 은 아래가 1).
    pos = [2, 1] if horizontal else [1, 2]
    fig, ax = plt.subplots(figsize=(4.0, 2.2) if horizontal else (3.4, 3.2), dpi=300)
    vert = not horizontal
    COLS = ('#d97b7b', '#7b93d9')   # SBE 붉은 · DBE 푸른 (기존 그림 배색)

    #  ⚠ `violin=False` 는 **Origin 대응판**이다 — 사용자 Origin 버전의 Box Chart 에는
    #    바이올린 Type 이 없다 (Box / Data / Bar 계열뿐).  두 그림이 같은 형식이어야 하므로
    #    상자만 그리는 판을 함께 낸다.  상자·수염 규약은 그대로다:
    #    상자 = 사분위(25–75) · 수염 = 1.5×IQR · 그 밖의 점은 **그리지 않는다**
    #    (Origin 에서는 Whisker Range `Outlier`/Coef 1.5 + Outliers 체크 해제와 같다).
    if violin:
        parts = ax.violinplot(vals, positions=pos, widths=0.62, vert=vert,
                              showmeans=False, showmedians=False, showextrema=False)
        for pc, c in zip(parts['bodies'], COLS):
            pc.set_facecolor(c); pc.set_alpha(0.42); pc.set_edgecolor('none')
    bp = ax.boxplot(vals, positions=pos, widths=0.15 if violin else 0.42,
                    showfliers=False, vert=vert, patch_artist=True,
                    medianprops=dict(color='#11161c', lw=1.4),
                    whiskerprops=dict(color='#4a5766'), capprops=dict(color='#4a5766'),
                    boxprops=dict(edgecolor='#4a5766'))
    if not violin:
        for patch, c in zip(bp['boxes'], COLS):
            patch.set_facecolor(c); patch.set_alpha(0.55)
    else:
        for patch in bp['boxes']:
            patch.set_facecolor('white')
    for x, b in zip(pos, beds):
        m = stats(data[b])['median']
        xy = (max(data[b]), x) if horizontal else (x, m)
        off = (8, -3) if horizontal else (16, -3)
        ax.annotate(f'{m:g}', xy, textcoords='offset points', xytext=off,
                    fontsize=9, color='#11161c',
                    va='center', ha='left')

    if horizontal:
        ax.set_yticks(pos); ax.set_yticklabels(beds)
        ax.set_xlabel(YLABEL, fontsize=8.5)
        ax.set_xlim(0, max(max(v) for v in vals) * 1.14)
        ax.grid(axis='x', color='#e3e8ee', lw=0.7)
    else:
        ax.set_xticks(pos); ax.set_xticklabels(beds)
        ax.set_ylabel(YLABEL, fontsize=8.5)
        ax.grid(axis='y', color='#e3e8ee', lw=0.7)
    ax.tick_params(labelsize=9)
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
    ap.add_argument('--data', default=DATA)
    ap.add_argument('--out', default=os.path.join('docs', 'figures', 'cbd_contacts'))
    ap.add_argument('--include-ptfe', action='store_true',
                    help='PTFE 를 도전 도메인에 넣는다 (대조 규약 — 기본은 도전상만)')
    ap.add_argument('--horizontal', action='store_true',
                    help='가로 방향 (원고 Fig 4b 형식 — SBE 위 · 값은 끝에)')
    ap.add_argument('--no-violin', action='store_true',
                    help='상자만 (Origin Box Chart 대응 — 그쪽엔 바이올린 Type 이 없다)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    data, conv = load(a.data, WITH_PTFE if a.include_ptfe else COND)
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    write_csv(a.out + '.csv', data, conv)
    write_origin_csv(a.out + '_origin.csv', data, conv)
    plot(data, conv, a.out, horizontal=a.horizontal, violin=not a.no_violin)
    for b in ('SBE', 'DBE'):
        s = stats(data[b])
        print(f'  {b}  median {s["median"]}  mean {s["mean"]}  p10–p90 {s["p10"]}–{s["p90"]}'
              f'  min–max {s["min"]}–{s["max"]}  접촉 0 인 AM {s["zero"]}/{s["n"]}')
    print(f'\n규약: band {conv["band_um"]} µm · include_ptfe={conv["include_ptfe"]} · '
          f'{conv["representation"]}')
    print(f'산출: {a.out}.svg · .png · .csv · _origin.csv (wide, Origin 용)')
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

        q = os.path.join(td, 'o_origin.csv'); write_origin_csv(q, d, c)
        orows = open(q, encoding='utf-8').read().strip().split('\n')
        chk('Origin CSV = wide (헤더 + 5행, 두 열)',
            len(orows) == 6 and orows[1].count(',') == 1)
        chk('★ Origin CSV 열 이름이 band 를 들고 다닌다 (주석줄 없이)',
            '0.15 um band' in orows[0] and not orows[0].startswith('#'))

        try:
            plot(d, c, os.path.join(td, 'fig'))
            plot(d, c, os.path.join(td, 'figh'), horizontal=True)
            plot(d, c, os.path.join(td, 'figb'), horizontal=True, violin=False)
            chk('SVG·PNG 를 낸다 (세로·가로 둘 다)',
                all(os.path.exists(os.path.join(td, n + '.' + e))
                    for n in ('fig', 'figh', 'figb') for e in ('svg', 'png')))
        except Exception as ex:                                    # noqa: BLE001
            chk(f'SVG·PNG 를 낸다 ({ex})', False)

    print('\n✓ plot_cbd_contacts selftest PASS' if ok else '\n✗ plot_cbd_contacts selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
