#!/usr/bin/env python3
"""Figure 4b 재작도 — 두 PTFE 규약을 **동등하게** 그린다.

    python3 scripts/fig4b_sigma_conventions.py --out docs/figures/fig4b.png
    python3 scripts/fig4b_sigma_conventions.py --selftest

v6 의 Figure 4b 는 철회된 세대(vox 0.4 µm)의 σ 한 쌍을 그린 그림이었다.  교체안은 셋을
지킨다:

  ① **두 규약을 나란히.**  어느 쪽도 먼저 오거나 굵게 그리지 않는다 — R10 재판정 1 이
     `reported` · `resolved` · 굵은 글씨를 전부 금지했다.  색·순서·글자 굵기가 같다.
  ② **origin 산포는 오차막대가 아니다.**  8 origin 은 한 침대의 완전 factorial 이라
     복제 오차 자유도가 0 이다 (R8 Q1).  그래서 막대가 아니라 **관측 범위를 띠로** 그리고
     캡션이 그것을 명시한다.  ⚠ 표준오차·신뢰구간을 암시하는 어떤 표기도 쓰지 않는다.
  ③ **비를 따로 패널로.**  절대값은 규약에 크게 의존하지만 **방향은 공통**이라는 것이
     이 그림이 말해야 하는 것이다.

수치 출처: `docs/reviews/table_s3_data_20260827.md` (정본).  이 파일은 그것을 옮겨 적으며,
`docs/data/w4*/` 축소본에서 판정기로 재도출된 값과 일치한다.
"""
from __future__ import annotations

import argparse
import sys

# --- 정본 수치 (table_s3_data_20260827.md §2 · §3) -----------------------
#  라벨은 원고와 **문자 그대로 같아야** 한다 (selftest 가 대조한다).
LABEL_OFF = 'PTFE omitted from the electronic grid\n(legacy/default convention)'
LABEL_CTR = 'PTFE centerline voxels excluded\n(exact-zero sensitivity convention)'

DATA = {
    'off': dict(label=LABEL_OFF, sbe=72.32, dbe=81.26,
                ratio=1.123672, lo=1.119994, hi=1.126646, spread=0.002700),
    'centerline': dict(label=LABEL_CTR, sbe=53.99, dbe=70.61,
                       ratio=1.307820, lo=1.301726, hi=1.310448, spread=0.002977),
}
ORDER = ['off', 'centerline']          # 등록 순서.  우열이 아니다.

CAPTION = (
    'Effective electronic conductivity of the SBE and DBE microstructures, computed with a '
    'finite-volume solver on a 0.15 um voxel grid. The insulating binder is treated under two '
    'conventions, shown as equivalent sensitivity points rather than one primary result: '
    'omitted from the electronic grid, and with its centerline voxels excluded from conduction. '
    'Neither is established as closer to a real thin coating. Each electrode was solved at all '
    'eight half-voxel grid-origin shifts of a 2x2x2 factorial, the two electrodes sharing the '
    'same origins so that ratios are paired; the shaded band in (b) spans the observed range '
    'over those eight phases. The eight phases form a complete factorial of a single bed rather '
    'than independent replicates, so the band is not a standard error and no confidence interval '
    'is implied. The direction of the change is common to both conventions; its magnitude is not. '
    'The value quoted in the main text uses the centerline convention; that is a reporting choice '
    'and not a determination that either convention is closer to a real coating.'
)


def build(out_path: str, dpi: int = 600):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    #  두 규약에 **같은 시각 비중**을 준다 — 채도만 다르고 명도·선폭은 같다.
    C_SBE, C_DBE = '#8FA9C4', '#C98A6B'
    HATCH = {'off': None, 'centerline': '///'}

    #  ⚠ 축 라벨은 **짧은 형태**로 두 규약에 똑같이 준다.  정식 라벨을 축에 넣으면
    #     서로 겹쳐 읽히지 않는다 (초판이 그랬다) — 정식 라벨은 캡션이 진다.
    SHORT = {'off': 'binder\nomitted', 'centerline': 'centerline\nexcluded'}

    fig, (axa, axb) = plt.subplots(
        1, 2, figsize=(7.0, 3.0), gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.40))

    # ── (a) 절대 전도도
    for i, key in enumerate(ORDER):
        d = DATA[key]
        x0 = i * 1.35
        axa.bar(x0 - 0.26, d['sbe'], 0.46, color=C_SBE, edgecolor='#333',
                linewidth=0.7, hatch=HATCH[key])
        axa.bar(x0 + 0.26, d['dbe'], 0.46, color=C_DBE, edgecolor='#333',
                linewidth=0.7, hatch=HATCH[key])
        for xoff, v in ((-0.26, d['sbe']), (0.26, d['dbe'])):
            axa.text(x0 + xoff, v + 1.8, f'{v:.1f}', ha='center', va='bottom', fontsize=8)
    axa.set_xticks([i * 1.35 for i in range(len(ORDER))])
    axa.set_xticklabels([SHORT[k] for k in ORDER], fontsize=8, linespacing=1.3)
    axa.set_xlim(-0.75, 1.35 * (len(ORDER) - 1) + 0.75)
    axa.set_ylabel('Effective $\\sigma_{ele}$  (mS cm$^{-1}$)', fontsize=9)
    axa.set_ylim(0, 100)
    axa.tick_params(axis='y', labelsize=8)
    axa.legend(handles=[Patch(facecolor=C_SBE, edgecolor='#333', label='SBE'),
                        Patch(facecolor=C_DBE, edgecolor='#333', label='DBE')],
               fontsize=8, frameon=False, loc='upper center', ncol=2,
               bbox_to_anchor=(0.5, 1.02), handlelength=1.3)
    axa.text(-0.20, 1.03, 'a', transform=axa.transAxes, fontsize=11, fontweight='bold')
    for s in ('top', 'right'):
        axa.spines[s].set_visible(False)

    # ── (b) 비.  origin 범위는 이 축척에서 선폭보다 얇다 — 그것 자체가 결과이므로
    #     보이지 않는 띠를 그리는 대신 **범위를 숫자로** 적고 그 사실을 밝힌다.
    for i, key in enumerate(ORDER):
        d = DATA[key]
        x0 = i * 1.0
        axb.bar(x0, d['ratio'] - 1.0, 0.40, bottom=1.0, color='#B9C6B0',
                edgecolor='#333', linewidth=0.7, hatch=HATCH[key])
        axb.fill_between([x0 - 0.20, x0 + 0.20], d['lo'], d['hi'],
                         color='#333', alpha=0.85, linewidth=0, zorder=5)
        axb.text(x0, d['hi'] + 0.010, f"{d['ratio']:.3f}",
                 ha='center', va='bottom', fontsize=9)
        axb.text(x0, d['hi'] + 0.043, f"[{d['lo']:.3f}–{d['hi']:.3f}]",
                 ha='center', va='bottom', fontsize=6.6, color='#444')
    axb.axhline(1.0, color='#666', linewidth=0.8, linestyle=(0, (4, 3)))
    axb.set_xticks([0.0, 1.0])
    axb.set_xticklabels([SHORT[k] for k in ORDER], fontsize=8, linespacing=1.3)
    axb.set_xlim(-0.6, 1.6)
    axb.set_ylabel('DBE / SBE  $\\sigma_{ele}$ ratio', fontsize=9)
    axb.set_ylim(0.98, 1.42)
    axb.tick_params(axis='y', labelsize=8)
    axb.text(-0.32, 1.03, 'b', transform=axb.transAxes, fontsize=11, fontweight='bold')
    #  각주는 **축 아래**로 — 그림 안에 두면 막대와 겹친다
    axb.text(0.5, -0.30, 'brackets: observed range over the eight prescribed\n'
             'grid-origin phases — not a standard error',
             transform=axb.transAxes, ha='center', va='top', fontsize=6.4, color='#444')
    for s in ('top', 'right'):
        axb.spines[s].set_visible(False)

    fig.savefig(out_path, dpi=dpi, bbox_inches='tight', facecolor='white')
    if out_path.endswith('.png'):
        fig.savefig(out_path[:-4] + '.svg', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out_path


# =========================================================================
def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        (print(f'  ok   {name}') if cond
         else (fails.append(name), print(f'  FAIL {name} {detail}')))

    print('fig4b selftest')

    # ① 수치가 정본과 자기일관인가 — 비 = DBE/SBE
    for key, d in DATA.items():
        r = d['dbe'] / d['sbe']
        chk(f'{key}: dbe/sbe = ratio (0.1 % 안)',
            abs(r - d['ratio']) / d['ratio'] < 1e-3, f'{r:.6f} vs {d["ratio"]:.6f}')
        chk(f'{key}: 평균이 관측 범위 안', d['lo'] <= d['ratio'] <= d['hi'])
        chk(f'{key}: 범위가 산포와 정합 (hi-lo ≲ 4·sd)',
            (d['hi'] - d['lo']) <= 4.2 * d['spread'],
            f"{d['hi']-d['lo']:.5f} vs {4.2*d['spread']:.5f}")

    # ② ★ 두 규약이 **동등하게** 취급되는가 (R10 재판정 1)
    chk('두 규약의 라벨 형식이 같다',
        DATA['off']['label'].count('\n') == DATA['centerline']['label'].count('\n'))
    for bad in ('reported', 'resolved', 'primary', 'best', 'correct'):
        chk(f'라벨에 우열 표현 {bad!r} 없음',
            not any(bad in d['label'].lower() for d in DATA.values()))
    chk('등록 순서에 두 규약이 각각 한 번', sorted(ORDER) == sorted(DATA))

    # ③ ★ 캡션이 철회된 통계 표현을 부정형으로만 쓰는가 (R8 Q1)
    for term in ('standard error', 'confidence interval'):
        chk(f'캡션의 {term!r} 는 부정형으로만',
            f'not a {term}' in CAPTION or f'no {term}' in CAPTION,
            CAPTION[CAPTION.find(term) - 40:CAPTION.find(term) + 20])
    chk('캡션이 어느 규약도 primary 로 지정하지 않는다',
        'primary result' in CAPTION and 'rather than one primary result' in CAPTION)
    chk('캡션이 방향/크기 구분을 적는다',
        'direction of the change is common' in CAPTION and 'magnitude is not' in CAPTION)
    chk('캡션이 factorial 임을 적는다',
        'complete factorial of a single bed' in CAPTION)
    #  ★ 본문이 centerline 을 공칭으로 쓰는 것과 캡션이 어긋나면 안 된다 (R15 P2).
    #    ⚠ 이것은 규약 판정의 번복이 **아니다** — 사전등록의 "채택 안 함" 은 그대로이고,
    #    본문 선택이 **편집 결정**임을 캡션이 스스로 밝히게 하는 것뿐이다.
    chk('캡션이 본문의 공칭 선택을 편집 결정으로 밝힌다',
        'quoted in the main text uses the centerline convention' in CAPTION
        and 'a reporting choice' in CAPTION)
    chk('그 문장이 우열 주장으로 새지 않는다',
        'not a determination that either convention is closer' in CAPTION)

    # ④ 철회된 세대의 값이 새지 않는가
    blob = CAPTION + repr(DATA)
    for banned in ('1.98', '3.00', '1.515', '51.5', '1.1232', '12.3', '42.15'):
        chk(f'철회 계열 {banned!r} 없음', banned not in blob)

    # ⑤ 그림이 실제로 그려지는가 (matplotlib 있을 때만)
    try:
        import matplotlib                                    # noqa: F401
    except ImportError:
        print('  skip 렌더 검사 — matplotlib 없음')
    else:
        import tempfile, os
        with tempfile.TemporaryDirectory() as td:
            p = build(os.path.join(td, 'fig4b.png'), dpi=72)
            chk('PNG 가 생성된다', os.path.getsize(p) > 10_000, str(os.path.getsize(p)))
            chk('SVG 도 함께 나온다', os.path.exists(p[:-4] + '.svg'))

    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='docs/figures/fig4b_sigma_conventions.png')
    ap.add_argument('--dpi', type=int, default=600)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    import os
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    p = build(a.out, a.dpi)
    print(f'wrote {p}  +  {p[:-4]}.svg')
    print('\n── 캡션 ──')
    print(CAPTION)
    return 0


if __name__ == '__main__':
    sys.exit(main())
