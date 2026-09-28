#!/usr/bin/env python3
"""믹서 층상 혼합 캠페인 — 발표용 설계·진행 그림 (svg · png · csv 동시 산출).

⛔ **결과를 한 글자도 주장하지 않는다** — 09-28 현재 판정 없음 (Lacey `M` 미판독).
   이 그림은 *무엇을 묻고 · 어떻게 재고 · 얼마나 왔나* 만 말한다.

값의 정본은 `docs/reviews/mixer_layered_prereg_20260921.md` §0 · §1 이다.
★ `--selftest` 가 그 문서를 **실제로 읽어** 이 파일의 Bo 값·런 수와 대조한다 —
  사전등록이 개정되면 그림이 조용히 낡는 것을 막는다 (CLAUDE.md 규율 ④:
  "정본은 밖으로 강제되지 않으면 새어나간다").

⚠ 라벨에 걸린 09-27 Codex 정정 둘 (이 둘을 어기면 사전등록 서술과 충돌한다):
  · HB-03 ⓑ 벽 CED = 대각 ÷ 6.25^(1/3) ⇒ AM–AM 을 올리면 **AM–벽도 함께** 오른다.
    그래서 축은 "AM–AM **명목** 점착" 이고, 사다리는 AM–AM 단독이 아니다.
  · R-3 `LC` 의 AM–AM 점착은 **0 이 아니다** (정적 압축 접촉 0.110 · 0.200).
    그래서 `LC` 는 "사다리 바닥" 으로만 적고 "Bo 0" 이라고 쓰지 않는다.
  · R-4 `LA` 는 **내부 기준점** (Bo_code 3.0 = Bo_po 0.444) — "문헌 앵커" 라벨은 철회됐다.
"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREREG = 'docs/reviews/mixer_layered_prereg_20260921.md'
OUT_FIG = 'docs/figures/mixer_campaign_design_20260928'
OUT_CSV = 'docs/data/mixer_campaign_arms_20260928.csv'

#: 팔 — 사전등록 §1 표.  (이름, Bo_code AM_P–AM_P, 시드=런, 역할)
ARMS = [
    ('LC',  0.00109, 3, '사다리 바닥'),
    ('LB1', 0.1,     1, '사다리'),
    ('LB2', 0.5,     1, '사다리'),
    ('LB3', 1.5,     1, '사다리'),
    ('LA',  3.0,     3, '내부 기준점'),
]
L0_RUNS = 1        # 전 쌍 Bo 0 — 음성 대조, 사다리 **밖**
E0_RUNS = 3        # 무회전 무작위 기준 S_R²
SE_BO_FIXED = 0.212
# 실측 watch (WSL) — L0 82 · LA 76/76/77 · LB1 76 · LB2 77 · LB3 73 · LC 76/77/79
PROGRESS = (0.73, 0.82, '09-28 10:07')

#: ⛔ 그림에 나오면 안 되는 문자열 (사전등록이 철회·정정한 표현)
BANNED_LABELS = ('문헌 앵커', 'hare2026', '코팅하면')

AM, REST, INK, MUTE = '#eb6834', '#2a78d6', '#222222', '#6b6b6b'


def _korean_font() -> str:
    """한글 글꼴을 찾는다.  ⛔ 못 찾으면 **추측하지 않고 멈춘다** (두부가 찍히면
    발표 그림이 조용히 망가진다)."""
    cands = []
    try:
        import koreanize_matplotlib as _km
        cands += sorted(glob.glob(os.path.join(os.path.dirname(_km.__file__),
                                               '**', 'NanumGothic.ttf'), recursive=True))
    except Exception:
        pass
    for pat in ('/usr/share/fonts/**/NanumGothic*.ttf',
                '/usr/share/fonts/**/malgun*.ttf',
                '/usr/share/fonts/**/NotoSansCJK*-Regular.*',
                '/usr/share/fonts/**/NotoSansKR*.*',
                '/mnt/c/Windows/Fonts/malgun.ttf'):
        cands += sorted(glob.glob(pat, recursive=True))
    for c in cands:
        if os.path.exists(c):
            return c
    raise SystemExit(
        '⛔ 한글 글꼴을 못 찾았다 — 이대로 그리면 글자가 두부(□)로 찍힌다.\n'
        '   해결: pip install koreanize-matplotlib  (또는 NanumGothic 설치)')


def build(out_dir: str = ROOT) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import font_manager as fm
    from matplotlib.patches import FancyArrowPatch, Rectangle, RegularPolygon
    from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

    fpath = _korean_font()
    fm.fontManager.addfont(fpath)
    plt.rcParams['font.family'] = fm.FontProperties(fname=fpath).get_name()
    plt.rcParams['axes.unicode_minus'] = False
    # 수식 글꼴은 DejaVu — 한글 글꼴에 U+2212(−) 가 없어 로그축 지수가 깨진다 (실제로 깨졌다)
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

    fig = plt.figure(figsize=(12.2, 4.5), dpi=200)
    gs = fig.add_gridspec(2, 2, width_ratios=[0.86, 1.14], height_ratios=[1.05, 0.95],
                          wspace=0.16, hspace=0.42,
                          left=0.015, right=0.985, top=0.90, bottom=0.075)
    axA, axB, axC = fig.add_subplot(gs[:, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 1])

    # ── A: 무엇을 재나 ────────────────────────────────────────────────────
    axA.set_xlim(-2.45, 3.25); axA.set_ylim(-2.75, 2.35); axA.axis('off')
    axA.set_aspect('equal')          # ← 없으면 39 각형이 타원이 된다 (실제로 됐다)
    rng = np.random.default_rng(20000003)

    def drum(cx, mixed):
        axA.add_patch(RegularPolygon((cx, 0.28), 39, radius=1.02, orientation=0.0,
                                     facecolor='none', edgecolor=INK, lw=1.4, zorder=3))
        n = 1500
        t = rng.random(n) * 2 * np.pi
        r = 0.93 * np.sqrt(rng.random(n))
        x, y = cx + r * np.cos(t), 0.28 + r * np.sin(t)
        is_am = (rng.random(n) < 0.35) if mixed else (y < 0.28 - 0.30)
        axA.scatter(x[is_am], y[is_am], s=2.4, c=AM, lw=0, zorder=2)
        axA.scatter(x[~is_am], y[~is_am], s=2.4, c=REST, lw=0, zorder=2)

    drum(-1.15, False)
    drum(1.75, True)
    axA.add_patch(FancyArrowPatch((0.02, 0.28), (0.60, 0.28), arrowstyle='-|>',
                                  mutation_scale=15, lw=1.5, color=INK))
    axA.text(0.31, 0.50, '8 회전', ha='center', va='bottom', fontsize=10.5, color=INK)
    axA.text(-1.15, 2.12, '층상 장입 (t = 0)', ha='center', fontsize=10.5, color=INK)
    axA.text(1.75, 2.12, '8 회전 후', ha='center', fontsize=10.5, color=INK)
    # ★ 상 라벨은 드럼 위·아래로 **쌓는다** — 옆에 두면 점 구름에 물린다 (두 번 물렸다)
    axA.text(-1.15, 1.52, '위 — SE · 도전재 · 바인더', ha='center', fontsize=9, color=REST)
    axA.text(-1.15, -1.06, '아래 — 활물질', ha='center', fontsize=9, color=AM)
    axA.text(-1.15, -1.52, '39 각형 드럼', ha='center', fontsize=8.4, color=MUTE)
    axA.plot([-2.25, 3.05], [-2.16, -2.16], color=MUTE, lw=1.2)
    for xx, lab in ((-2.25, '0\n미혼합'), (3.05, '1\n무작위 완전혼합')):
        axA.plot([xx, xx], [-2.23, -2.09], color=MUTE, lw=1.2)
        axA.text(xx, -2.32, lab, ha='center', va='top', fontsize=8.6, color=MUTE)
    axA.text(0.40, -2.04, 'Lacey 혼합지수  M', ha='center', va='bottom', fontsize=10, color=INK)
    # ★ 판정이 없다는 것을 그림 안에서 못 박는다
    axA.text(1.75, -0.02, 'M = ?', ha='center', fontsize=12, color=INK,
             bbox=dict(boxstyle='round,pad=0.30', fc='white', ec=MUTE, lw=0.9))

    # ── B: 점착 사다리 ────────────────────────────────────────────────────
    axB.set_xscale('log'); axB.set_xlim(6e-4, 9.0); axB.set_ylim(-0.75, 1.25)
    axB.spines[['left', 'right', 'top']].set_visible(False)
    axB.set_yticks([]); axB.tick_params(axis='x', labelsize=9, colors=MUTE)
    axB.spines['bottom'].set_color(MUTE)
    axB.xaxis.set_major_locator(FixedLocator([0.001, 0.01, 0.1, 1]))
    axB.xaxis.set_major_formatter(FixedFormatter(['0.001', '0.01', '0.1', '1']))
    axB.xaxis.set_minor_locator(NullLocator())
    for name, bo, seeds, _role in ARMS:
        axB.plot([bo], [0.30], 'o', ms=11 if seeds == 3 else 8,
                 mfc=AM if seeds == 3 else 'white', mec=AM, mew=1.8, zorder=3)
        axB.annotate(name, (bo, 0.30), textcoords='offset points', xytext=(0, 14),
                     ha='center', fontsize=10, color=INK)
        axB.annotate(f'{bo:g}' + (f'\n×{seeds} 시드' if seeds == 3 else ''),
                     (bo, 0.30), textcoords='offset points', xytext=(0, -13),
                     ha='center', va='top', fontsize=8.4, color=MUTE)
    axB.plot([ARMS[0][1], ARMS[-1][1]], [0.30, 0.30], color=AM, lw=1.1, alpha=0.35, zorder=1)
    # ⚠ "명목" 이 빠지면 HB-03 ⓑ (AM–벽 동반) 와 충돌한다
    axB.set_xlabel('Bo$_{code}$  —  AM–AM 명목 점착 (점착력 ÷ 무게)', fontsize=9.5,
                   color=INK, labelpad=2)
    axB.set_title(f'점착 사다리 {len(ARMS) + 1} 팔 · {sum(a[2] for a in ARMS) + L0_RUNS} 런',
                  fontsize=11, color=INK, loc='left', pad=16)
    axB.text(0.995, 1.13, f'SE 관련 CED 고정 (Bo {SE_BO_FIXED})', transform=axB.transAxes,
             ha='right', va='top', fontsize=8.6, color=MUTE)

    # ── C: 사다리 밖 + 진행 ───────────────────────────────────────────────
    axC.set_xlim(0, 1); axC.set_ylim(0, 1); axC.axis('off')
    axC.text(0.0, 0.93, 'L0', fontsize=10, color=INK, va='top', fontweight='bold')
    axC.text(0.055, 0.93, f'전 쌍 Bo 0 — 음성 대조 (사다리 밖) · {L0_RUNS} 런',
             fontsize=9.2, color=MUTE, va='top')
    axC.text(0.0, 0.66, 'E0', fontsize=10, color=INK, va='top', fontweight='bold')
    axC.text(0.055, 0.66, f'무회전 무작위 기준 (S$_R^2$) · {E0_RUNS} 런',
             fontsize=9.2, color=MUTE, va='top')
    tot = sum(a[2] for a in ARMS) + L0_RUNS
    axC.text(0.62, 0.93, f'합계  {tot + E0_RUNS} 런', fontsize=10.5, color=INK, va='top')
    axC.text(0.62, 0.70, f'{tot} (사다리) + {E0_RUNS} (E0)', fontsize=8.8, color=MUTE, va='top')
    lo, hi, asof = PROGRESS
    axC.add_patch(Rectangle((0.0, 0.16), 1.0, 0.16, fc='#e9e9e9', ec='none'))
    axC.add_patch(Rectangle((0.0, 0.16), hi, 0.16, fc=REST, ec='none', alpha=0.30))
    axC.add_patch(Rectangle((0.0, 0.16), lo, 0.16, fc=REST, ec='none'))
    axC.text(0.0, 0.055,
             f'측정 {tot} 런  {lo * 100:.0f} – {hi * 100:.0f} % 진행 ({asof})'
             f'   ·   판정 없음 — M 미판독', fontsize=9.4, color=INK, va='top')

    fig.suptitle('믹서 층상 혼합 캠페인 — 설계 및 진행', fontsize=13.5, color=INK,
                 x=0.015, ha='left', y=0.975)

    os.makedirs(os.path.join(out_dir, 'docs/figures'), exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'docs/data'), exist_ok=True)
    for ext in ('svg', 'png'):
        fig.savefig(os.path.join(out_dir, f'{OUT_FIG}.{ext}'),
                    bbox_inches='tight', facecolor='white')
    with open(os.path.join(out_dir, OUT_CSV), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['arm', 'Bo_code_AM_P_AM_P', 'seeds', 'runs', 'role', 'note'])
        w.writerow(['L0', 0.0, L0_RUNS, L0_RUNS, '음성 대조 (사다리 밖)', '전 쌍 Bo 0'])
        for n, b, s, r in ARMS:
            note = ('AM_S 0.00553 · 점착 0 이 아니다 (정적 접촉 0.110 / 0.200) — R-3'
                    if n == 'LC' else
                    'Bo_po 0.444 — 내부 기준점 (문헌 앵커 라벨 철회) — R-4' if n == 'LA' else '')
            w.writerow([n, b, s, s, r, note])
        w.writerow(['E0', 0.0, E0_RUNS, E0_RUNS, '무회전 무작위 기준',
                    '균일 삽입 · 점착 0 · 회전 0'])
    print(f'✅ {OUT_FIG}.svg · .png · {OUT_CSV}')
    print(f'   측정 {tot} 런 + E0 {E0_RUNS} = {tot + E0_RUNS}')


def selftest() -> int:
    fails = []

    def chk(name, cond, extra=''):
        n[0] += 1
        print(('  ok  ' if cond else '  FAIL') + '  ' + name + (('   ' + str(extra)) if extra else ''))
        if not cond:
            fails.append(name)

    print('make_mixer_campaign_fig selftest')
    n = [0]
    src = open(os.path.abspath(__file__), encoding='utf-8').read()
    pp = os.path.join(ROOT, PREREG)
    pre = open(pp, encoding='utf-8').read() if os.path.exists(pp) else ''

    tot = sum(a[2] for a in ARMS) + L0_RUNS
    chk('① 사다리 런 합계 = 10', tot == 10, tot)
    chk('①b 전체 = 13 런', tot + E0_RUNS == 13, tot + E0_RUNS)
    chk('①c 팔 수 = 6 (L0 + 사다리 5)', len(ARMS) + 1 == 6)

    chk('② 사전등록 문서가 실재한다', bool(pre), PREREG)
    # ★ 정본 대조 — 사전등록이 개정되면 그림이 조용히 낡는 것을 막는다 (규율 ④)
    missing = [f'{b:g}' for _n, b, _s, _r in ARMS if f'{b:g}' not in pre]
    chk('③ ★ 모든 Bo 값이 사전등록 본문에 실재한다', not missing, missing)
    chk('③b SE 고정 Bo 도 실재한다', str(SE_BO_FIXED) in pre)

    # ★★ 음성 대조 — ③ 이 무조건 통과하는 검사가 아님을 보인다
    chk('④ ★★ 음성 대조: 가짜 Bo 값은 사전등록에 없다', '0.00777' not in pre)

    # ⛔ 철회된 라벨이 그림에 되살아나지 않게
    live = [w for w in BANNED_LABELS
            if w in src.split('BANNED_LABELS')[-1].split('def selftest')[0]]
    chk('⑤ ⛔ 철회된 라벨(문헌 앵커 등)이 그리기 코드에 없다', not live, live)

    # 결과를 주장하지 않는가 — M 값이 하드코딩돼 있으면 안 된다
    draw = src.split('def build')[1].split('def selftest')[0]
    chk('⑥ ★ 그림에 M 값이 없다 (판정 없음)', "'M = ?'" in draw and 'M = 0.' not in draw)

    chk('⑦ 축 라벨에 "명목" 이 있다 (HB-03 ⓑ: AM–벽 동반)', 'AM–AM 명목 점착' in draw)

    print()
    if fails:
        print(f'⛔ {len(fails)} FAIL: ' + ' · '.join(fails))
        return 1
    print(f'✅ selftest {n[0]}/{n[0]}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description='믹서 캠페인 설계·진행 그림 (svg·png·csv)')
    ap.add_argument('--out', default=ROOT, help='산출 루트 (기본: 리포 루트)')
    ap.add_argument('--selftest', action='store_true', help='정본 대조 포함 자기검사')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    build(a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
