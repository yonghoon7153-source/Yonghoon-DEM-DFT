#!/usr/bin/env python3
"""plot_cascade3.py — ⛔⛔ **철회 (2026-09-08). 존재하지 않는 농도축으로 그린 그림이다.**

이 스크립트는 `x002/x005/x010` 폴더 키를 dopant fraction x = 0.02/0.05/0.10 으로 읽어
"concentration trends" 3패널을 그렸다. **그런 농도축은 없다.**
47종 캠페인은 슈퍼셀 버그로 **전부 x = 0.25 에서 돌았고**, 세 키는 농도가 아니라
**배치 반복(placement replicate)** 이다.
  근거 · kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:409
         ("의도는 2·5·10%, 슈퍼셀 버그로 0.25 고정") · 같은 파일 350행 · 656행 P0-6
         ("champions csv concentration 전부 0.25")
       · tools/figures/plot_cascade_v23.py:12-14 — 같은 폴더가 이미 적어 놨다
         ("the dir x002/x005/x010 are PLACEMENT REPLICATES at x=0.25,
           NOT a concentration sweep")
즉 세 패널의 x축·눈금·제목이 전부 틀렸다. 기울기·추세·"농도를 올리면 …" 서술은
**어느 것도 인용 금지**다.

무엇이 바뀌었나 (2026-09-08)
  · 산출물 `docs/figures/cascade/cascade_conc_trends.png` 를 **배포 경로에서 내렸다**
    → `docs/figures/_retracted/RETRACTED_cascade_conc_trends_2026_06_15.png`
      (파일은 지우지 않는다 — 틀린 그림도 "무엇이 왜 틀렸나" 의 증거다. docs/figures/_retracted/WHY.md)
  · 이 스크립트는 **남긴다**. 단 그냥 돌면 다시 틀린 그림이 배포 경로에 생기므로,
    ① 기본은 거부하고 ② `--i-know-this-is-retracted` 를 줘야만 `_retracted/` 로 저장한다.
  · 축 라벨을 'placement replicate (all x = 0.25)' 로 고쳤다 — 남은 그림을 누가 열어도
    농도로 안 읽히게. 값 자체는 그대로다 (반복 간 산포로는 읽을 수 있다).

농도 응답이 필요하면
  kb 가 가리키는 `dualx_v23` (actual_x 0.0625 / 0.25 실측) 로 다시 그린다. 이 파일이 아니다.

⛔ 이 도구가 **못 하는 것**
  · 농도 의존성을 못 준다 (그게 이 철회의 전부다).
  · 반복 간 산포조차 통계로 못 준다 — 세 폴더가 같은 x 의 서로 다른 배치라는 것만 알고,
    몇 개가 같은 배치인지·게이트를 통과했는지는 여기서 안 본다.
  · `_FLAG` 가 붙은 항목만 걸러낼 뿐, champions 원장의 인용 지위는 안 본다
    (cascade 47종 랭킹은 archive_only 다).

  python3 tools/figures/plot_cascade3.py --selftest
  python3 tools/figures/plot_cascade3.py --i-know-this-is-retracted   # 철회본 재생성
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, 'db/properties/doping_cascade_trivalent_M3.json')
# ⛔ 배포 경로(docs/figures/cascade/)로는 다시 저장하지 않는다.
OUT = os.path.join(REPO, 'docs/figures/_retracted/RETRACTED_cascade_conc_trends_2026_06_15.png')

#: 폴더 키 → 그 폴더가 **무엇인가**. 값은 x 가 아니라 반복 번호다 (실제 x 는 전부 0.25).
REPLICATES = {'x002': 1, 'x005': 2, 'x010': 3}
ACTUAL_X = 0.25
RETRACTED = ("x002/x005/x010 은 농도가 아니라 x=0.25 의 배치 반복이다 "
             "(kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:409)")


def series(triv, d, key):
    """설계 d 의 축 key 를 (반복번호, 값) 으로. 농도가 아니다."""
    xs, ys = [], []
    for xk, rep in REPLICATES.items():
        e = triv[d].get(xk)
        if isinstance(e, dict) and key in e and not e.get('_FLAG'):
            xs.append(rep)
            ys.append(e[key])
    return xs, ys


def selftest():
    ok = True

    def say(c, m):
        nonlocal ok
        ok &= bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    # 양성: 반복 키를 반복 번호로 읽는다
    triv = {'X2O3': {'r_A': 1.0,
                     'x002': {'k': 1.0}, 'x005': {'k': 2.0}, 'x010': {'k': 3.0}}}
    say(series(triv, 'X2O3', 'k') == ([1, 2, 3], [1.0, 2.0, 3.0]),
        "반복 키를 **반복 번호**로 읽는다 (1/2/3)")
    # ⛔음성 ①: 농도값 0.02/0.05/0.10 이 다시 x축으로 돌아오면 실패
    say(0.02 not in REPLICATES.values() and 0.05 not in REPLICATES.values()
        and 0.10 not in REPLICATES.values(),
        "⛔음성: 삭제된 농도 눈금(0.02/0.05/0.10)이 x축으로 되살아나면 실패")
    say(ACTUAL_X == 0.25, "⛔음성: 실제 x 는 0.25 하나뿐이다")
    # ⛔음성 ②: _FLAG 가 붙은 항목은 빠져야 한다
    triv2 = {'Y2O3': {'r_A': 1.0, 'x002': {'k': 1.0, '_FLAG': 'bad'},
                      'x005': {'k': 2.0}}}
    say(series(triv2, 'Y2O3', 'k') == ([2], [2.0]), "⛔음성: _FLAG 항목은 뺀다")
    # ⛔음성 ③: 배포 경로로 저장하려 하면 실패
    say('docs/figures/cascade/' not in OUT.replace(os.sep, '/'),
        "⛔음성: 배포 경로(docs/figures/cascade/)로 저장하지 않는다")
    say('_retracted' in OUT, "산출물은 _retracted/ 로만 나간다")
    # ⛔음성 ④: 철회 사실이 docstring 에 남아 있어야 한다
    say('철회' in (__doc__ or '') and '0.25' in (__doc__ or ''),
        "⛔음성: 철회 배너가 docstring 에서 사라지면 실패")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    if '--selftest' in sys.argv:
        return selftest()
    if '--i-know-this-is-retracted' not in sys.argv:
        print("⛔ 철회된 그림이다 — 기본으로는 만들지 않는다.")
        print("   " + RETRACTED)
        print("   농도 응답이 필요하면 dualx_v23 (actual_x 0.0625/0.25) 로 다시 그려라.")
        print("   그래도 철회본을 재생성하려면: --i-know-this-is-retracted")
        return 2

    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    triv = json.load(open(SRC))['champions']
    dops = sorted(triv, key=lambda d: triv[d]['r_A'])
    colors = cm.tab10(np.linspace(0, 1, len(dops)))
    fig, ax = plt.subplots(1, 3, figsize=(17, 5))
    panels = [('de_post_anneal_eV_atom', 'formation dE (eV/atom)',
               '(a) stability across placement replicates'),
              ('E_young_GPa', 'E_VRH (GPa)',
               '(b) modulus across placement replicates'),
              ('score_combined', 'combined score',
               '(c) cascade score across placement replicates')]
    for (key, ylab, ttl), a in zip(panels, ax):
        for d, c in zip(dops, colors):
            xs, ys = series(triv, d, key)
            if xs:
                a.plot(xs, ys, 'o-', c=c, ms=6, lw=1.5, label=d.replace('2O3', ''))
        a.set_xlabel('placement replicate (all x = 0.25)')
        a.set_ylabel(ylab)
        a.set_title(ttl)
        a.grid(alpha=.3)
        a.set_xticks([1, 2, 3])
        a.set_xticklabels(['rep 1\n(dir x002)', 'rep 2\n(dir x005)', 'rep 3\n(dir x010)'])
    ax[0].legend(fontsize=7, ncol=2, loc='upper right')
    plt.suptitle('RETRACTED — NOT a concentration sweep: all points are x = 0.25 '
                 '(placement replicates, supercell bug)', fontsize=12, y=1.02, color='#be123c')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches='tight')
    print('saved (retracted, non-distribution path) -> ' + OUT)
    print('⛔ ' + RETRACTED)
    return 0


if __name__ == '__main__':
    sys.exit(main())
