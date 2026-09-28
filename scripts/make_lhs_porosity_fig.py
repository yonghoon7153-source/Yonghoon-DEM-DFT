#!/usr/bin/env python3
"""LHS 인계 — 공극률 계산 재수립 그림 (svg · png 동시 산출).

정본: 결함 원장 `docs/reviews/findings.json` 의 `LHS-10` ~ `LHS-13` ·
      진행 문서 `docs/session_20260923_progress.md` ⑩ · ⑲.

★ `--selftest` 가 원장을 **실제로 읽어** 이 파일의 건수·상태와 대조한다.
  건수를 산문으로 옮겨 적으면 원장이 갱신돼도 그림만 낡는다 (규율 ④).

⚠ 그림이 반드시 구분해야 하는 것 둘:
  · `LHS-13` 만 **`open`** 이다 (나머지 셋은 `claimed_fixed`).  "결함 4 건" 으로만
    그리면 *셋은 고쳤고 하나는 미해결* 이라는 정보가 사라진다.
  · `claimed_fixed` 는 **`fixed` 가 아니다** — 재수확 검증 전이므로 결과표는 배포 보류.
  · `LHS-12` 는 방향이 반대다 (결과를 망친 것이 아니라 **정상** 침대를 거부) → 색을 가른다.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = 'docs/reviews/findings.json'
OUT = 'docs/figures/lhs_porosity_rebuild_20260928'
N_TOTAL = 130

#: (id, 영향 건수 | None, 한 줄, 방향)  — 건수는 selftest 가 원장 본문에서 확인한다
ITEMS = [
    ('LHS-11', 97,   '압착판 위치를 원자 덤프보다\n이른 시점 파일에서 읽음', 'bad'),
    ('LHS-12', 58,   '안전장치가 **정상** 침대를 거부', 'guard'),
    ('LHS-13', 4,    '벽 관통 의심 — 원인 미확정', 'bad'),
    ('LHS-10', None, '공극률 분모를 벽이 아니라\n상자 바닥에서 잼 (계산 규약)', 'bad'),
]
OPEN_IDS = ('LHS-13',)          # 원장 status == 'open'
AM, REST, INK, MUTE, RED, AMB = '#eb6834', '#2a78d6', '#222222', '#6b6b6b', '#c0392b', '#e8a33d'


def _ledger(root: str) -> dict:
    p = os.path.join(root, LEDGER)
    if not os.path.exists(p):
        return {}
    d = json.load(open(p, encoding='utf-8'))
    rows = d if isinstance(d, list) else d.get('findings', d)
    if isinstance(rows, dict):
        rows = list(rows.values())
    return {str(r.get('id')): r for r in rows if isinstance(r, dict)}


def _korean_font() -> str:
    c = []
    try:
        import koreanize_matplotlib as _km
        c += sorted(glob.glob(os.path.join(os.path.dirname(_km.__file__), '**',
                                           'NanumGothic.ttf'), recursive=True))
    except Exception:
        pass
    for pat in ('/usr/share/fonts/**/NanumGothic*.ttf', '/usr/share/fonts/**/malgun*.ttf',
                '/usr/share/fonts/**/NotoSansCJK*-Regular.*', '/mnt/c/Windows/Fonts/malgun.ttf'):
        c += sorted(glob.glob(pat, recursive=True))
    for x in c:
        if os.path.exists(x):
            return x
    raise SystemExit('⛔ 한글 글꼴을 못 찾았다 — 이대로 그리면 글자가 두부(□)로 찍힌다.\n'
                     '   해결: pip install koreanize-matplotlib')


def build(out_dir: str = ROOT) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import font_manager as fm
    from matplotlib.patches import Circle

    f = _korean_font()
    fm.fontManager.addfont(f)
    plt.rcParams['font.family'] = fm.FontProperties(fname=f).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

    fig = plt.figure(figsize=(12.6, 4.6), dpi=200)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.06, 0.94], wspace=0.22,
                          left=0.055, right=0.985, top=0.82, bottom=0.11)
    axA, axB = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    y = np.arange(len(ITEMS))[::-1]
    axA.barh(y, [N_TOTAL] * len(ITEMS), color='#ededed', height=0.50)
    for i, (tag, n, desc, kind) in enumerate(ITEMS):
        if n is not None:
            axA.barh(y[i], n, color=AMB if kind == 'guard' else RED, height=0.50)
            axA.text(n + 3, y[i], f'{n} / {N_TOTAL}', va='center', fontsize=9.5, color=INK)
        else:
            axA.text(4, y[i], '건수 미집계 — 규약 자체의 결함',
                     va='center', fontsize=9, color=MUTE)
        # ★ 상태를 같이 찍는다 — 넷을 뭉뚱그리면 "셋은 고쳤고 하나는 미해결" 이 사라진다
        openq = tag in OPEN_IDS
        axA.text(N_TOTAL + 21, y[i], '미해결' if openq else '수정 주장',
                 va='center', ha='left', fontsize=8.6,
                 color='white' if openq else MUTE,
                 bbox=dict(boxstyle='round,pad=0.26', lw=0,
                           fc=RED if openq else '#e4e4e4'))
        axA.text(-6, y[i] + 0.40, tag, ha='right', va='center', fontsize=10,
                 color=INK, fontweight='bold')
        axA.text(-6, y[i] - 0.15, desc.replace('**', ''), ha='right', va='center',
                 fontsize=8.3, color=MUTE, linespacing=1.35)
    axA.set_xlim(0, 178); axA.set_ylim(-0.7, 3.7); axA.axis('off')
    axA.set_title(f'① 결함 4 건 (LHS 침대 {N_TOTAL} 개 수확 중, 09-24)',
                  fontsize=11.5, color=INK, loc='left', pad=10)
    axA.text(0, -0.62, '⚠ "수정 주장" = 재수확 검증 **전** — 아직 검증된 것이 아니다',
             fontsize=8.6, color=MUTE)

    axB.set_xlim(0, 10); axB.set_ylim(0, 6.2); axB.axis('off'); axB.set_aspect('equal')
    for x0, dup, lab, sub in ((1.0, True, '구 부피 단순 합 (sphere-sum)', '겹침을 두 번 센다'),
                              (5.9, False, '겹침 한 번만 (union)', '정확한 계산')):
        for dx in (0, 1.45):
            axB.add_patch(Circle((x0 + 0.95 + dx, 4.15), 1.05, fc=REST, ec=INK,
                                 lw=1.1, alpha=0.42))
        if dup:
            axB.add_patch(Circle((x0 + 1.675, 4.15), 0.33, fc=RED, ec='none', alpha=0.85))
            axB.text(x0 + 1.675, 2.72, '중복 계상', ha='center', fontsize=8.6, color=RED)
        axB.text(x0 + 1.675, 5.55, lab, ha='center', fontsize=9.8, color=INK)
        axB.text(x0 + 1.675, 2.26, sub, ha='center', fontsize=8.6, color=MUTE)
    axB.text(2.675, 1.32, '고체 부피 과대\n⇒ 공극률 음수', ha='center', fontsize=9.6,
             color=RED, linespacing=1.4)
    axB.text(7.575, 1.32, f'다시 재니\n{N_TOTAL} 개 전부 양수', ha='center', fontsize=9.6,
             color=INK, linespacing=1.4)
    axB.annotate('', xy=(5.55, 4.15), xytext=(4.75, 4.15),
                 arrowprops=dict(arrowstyle='-|>', lw=1.5, color=INK))
    axB.text(0.0, 0.22, '⇒ 수확 · 덱의 결함이 아니다 (계산 방식의 문제) · 이 결과가 순수 SE 시험으로 이어짐',
             fontsize=9, color=MUTE, ha='left')
    axB.set_title('② 음수 공극률의 원인 (09-27)', fontsize=11.5, color=INK, loc='left', pad=10)

    fig.suptitle('LHS 인계 — 공극률 계산을 다시 세웠다', fontsize=13.5, color=INK,
                 x=0.012, ha='left', y=0.965)
    fig.text(0.012, 0.012,
             '상태 — 수확기 · 생성기 v2 (HND-01~06) 재수확 검증 전 · 결과표 배포 보류',
             fontsize=9.4, color=INK)

    os.makedirs(os.path.join(out_dir, 'docs/figures'), exist_ok=True)
    for e in ('svg', 'png'):
        fig.savefig(os.path.join(out_dir, f'{OUT}.{e}'), bbox_inches='tight', facecolor='white')
    print(f'✅ {OUT}.svg · .png')


def selftest() -> int:
    fails, n = [], [0]

    def chk(name, cond, extra=''):
        n[0] += 1
        print(('  ok  ' if cond else '  FAIL') + '  ' + name + (('   ' + str(extra)) if extra else ''))
        if not cond:
            fails.append(name)

    print('make_lhs_porosity_fig selftest')
    led = _ledger(ROOT)
    chk('① 결함 원장을 읽었다', bool(led), f'{len(led)} 항목')
    for tag, cnt, _d, _k in ITEMS:
        chk(f'② {tag} 이 원장에 실재한다', tag in led)
        if cnt is not None and tag in led:
            body = json.dumps(led[tag], ensure_ascii=False)
            # ★ 정본 대조 — 건수를 산문으로 옮겨 적은 것이 맞는지 원장 본문에서 찾는다
            chk(f'③ {tag} 의 건수 {cnt} 가 원장 본문에 있다', str(cnt) in body)
    opens = [t for t in led if t.startswith('LHS-1') and led[t].get('status') == 'open']
    chk('④ ★ 원장의 open 인 LHS-1x 가 그림의 OPEN_IDS 와 같다',
        set(opens) & {i[0] for i in ITEMS} == set(OPEN_IDS), f'원장 open={opens}')
    # ★★ 음성 대조 — ③ 이 무조건 통과하는 검사가 아님을 보인다
    body11 = json.dumps(led.get('LHS-11', {}), ensure_ascii=False)
    chk('⑤ ★★ 음성 대조: 가짜 건수 4242 는 원장에 없다', '4242' not in body11)
    src = open(os.path.abspath(__file__), encoding='utf-8').read()
    draw = src.split('def build')[1].split('def selftest')[0]
    chk('⑥ 그림이 "수정 주장" 과 "미해결" 을 구분해 찍는다',
        "'미해결'" in draw and "'수정 주장'" in draw)
    chk('⑦ claimed_fixed 를 "검증됨" 으로 적지 않는다', '검증됨' not in draw)
    print()
    if fails:
        print(f'⛔ {len(fails)} FAIL: ' + ' · '.join(fails))
        return 1
    print(f'✅ selftest {n[0]}/{n[0]}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description='LHS 공극률 재수립 그림 (svg·png)')
    ap.add_argument('--out', default=ROOT, help='산출 루트 (기본: 리포 루트)')
    ap.add_argument('--selftest', action='store_true', help='원장 대조 포함 자기검사')
    a = ap.parse_args()
    return selftest() if a.selftest else (build(a.out) or 0)


if __name__ == '__main__':
    sys.exit(main())
