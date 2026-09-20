#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 드럼 **배플(lifter)** STL 생성기 — `D10(b)` 전단 축.

    python3 scripts/make_mixer_baffles.py --n 6 --height 0.10 --out Baffles.stl
    python3 scripts/make_mixer_baffles.py --selftest

━━ 왜 별도 메시인가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`Drum.stl` 은 1저자가 준 튜토리얼 원본이다.  **한 장도 건드리지 않는다** — 원본을
고치면 배플 없는 팔과 있는 팔이 *"같은 드럼"* 이라는 근거가 사라진다.
⇒ 배플은 **네 번째 메시**로 얹고, 드럼과 **같은 `move/mesh` 회전**을 준다.
⇒ `--n 0` 이면 이 파일을 아예 만들지 않고 덱도 메시 줄을 안 쓴다
  = 배플 없는 팔의 덱이 **기존 런과 글자 그대로 같다** (재실행 불요).

━━ 좌표계 — 드럼 원본을 따른다 (실측) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`Drum.stl` 실측: x ∈ [−0.1, 0.1] (축·길이) · y, z ∈ [−0.5, 0.5] (단면, 반경 0.5).
덱이 `scale` 로 줄이므로 **여기서도 같은 단위**로 쓴다 (R = 0.5).

배플 하나 = 반경 방향 평판.  안쪽으로 `height·R` 만큼 들어온다.
  바깥 모서리 r = R,  안쪽 모서리 r = R·(1 − height)
  길이는 드럼 전장 (x ∈ [−0.1, 0.1])
⚠ 두께 0 평판이다 — LIGGGHTS 삼각 벽은 양면을 다 본다.
"""
from __future__ import annotations

import argparse
import math

R_DRUM = 0.5
X_HALF = 0.1


def baffle_tris(n, height, r=R_DRUM, x_half=X_HALF, phase=0.0):
    """배플 `n` 개 → 삼각형 리스트.  각 삼각형은 (법선, v0, v1, v2)."""
    if n <= 0:
        return []
    if not (0.0 < height < 1.0):
        raise SystemExit(f'⛔ height 는 0 < h < 1 이어야 한다 (받은 값 {height})')
    r_in = r * (1.0 - height)
    tris = []
    for k in range(n):
        th = phase + 2.0 * math.pi * k / n
        c, s = math.cos(th), math.sin(th)
        #  평판은 반경 방향 — 법선은 **접선 방향**
        nrm = (0.0, -s, c)
        out = (r * c, r * s)                       # (y, z) 바깥 모서리
        inn = (r_in * c, r_in * s)                 # (y, z) 안쪽 모서리
        a = (-x_half, out[0], out[1])
        b = (+x_half, out[0], out[1])
        cc = (+x_half, inn[0], inn[1])
        dd = (-x_half, inn[0], inn[1])
        tris.append((nrm, a, b, cc))
        tris.append((nrm, a, cc, dd))
    return tris


def to_stl(tris, name='LIGGGHTS_STL_EXPORT'):
    L = [f'solid {name}']
    for nrm, *vs in tris:
        L.append('  facet normal %g %g %g' % nrm)
        L.append('    outer loop')
        for v in vs:
            L.append('      vertex %g %g %g' % v)
        L.append('    endloop')
        L.append('  endfacet')
    L.append(f'endsolid {name}')
    return '\n'.join(L) + '\n'


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    t = baffle_tris(6, 0.10)
    chk('① 배플 하나당 삼각형 2개 (6개 → 12)', len(t) == 12)
    chk('② n=0 이면 빈 목록 (배플 없는 팔의 덱이 기존과 같아진다)',
        baffle_tris(0, 0.10) == [])
    vs = [v for tri in t for v in tri[1:]]
    chk('③ 모든 꼭짓점이 드럼 안 (r ≤ R, |x| ≤ 0.1)',
        all(math.hypot(v[1], v[2]) <= R_DRUM + 1e-12 and abs(v[0]) <= X_HALF + 1e-12
            for v in vs))
    #  ★ 높이가 요청대로인가 — 바깥/안쪽 반경의 차
    radii = sorted({round(math.hypot(v[1], v[2]), 9) for v in vs})
    chk(f'④ 안쪽 반경이 R(1−h) = 0.45 (실제 {radii[0]})',
        abs(radii[0] - R_DRUM * 0.9) < 1e-9 and abs(radii[-1] - R_DRUM) < 1e-9)
    #  ★ 변이 — 높이를 바꾸면 안쪽 반경이 따라 움직인다 (상수를 내는 것이 아니다)
    r2 = sorted({round(math.hypot(v[1], v[2]), 9)
                 for tri in baffle_tris(6, 0.20) for v in tri[1:]})
    chk(f'④b 변이: h=0.20 → 안쪽 반경 0.40 (실제 {r2[0]})',
        abs(r2[0] - R_DRUM * 0.8) < 1e-9)
    #  ★ 각도가 고르게 나뉘는가
    angs = sorted({round(math.atan2(v[2], v[1]), 6) for v in vs
                   if abs(math.hypot(v[1], v[2]) - R_DRUM) < 1e-12})
    chk(f'⑤ 6개가 고르게 (각 {len(angs)}개, 간격 60°)',
        len(angs) == 6 and abs((angs[1] - angs[0]) - math.pi / 3) < 1e-6)
    #  ★ 법선이 단위이고 평판에 수직인가
    def dot(a, b):
        return sum(p * q for p, q in zip(a, b))
    good = True
    for nrm, a, b, c in t:
        if abs(math.sqrt(dot(nrm, nrm)) - 1.0) > 1e-9:
            good = False
        e1 = tuple(q - p for p, q in zip(a, b))
        e2 = tuple(q - p for p, q in zip(a, c))
        if abs(dot(nrm, e1)) > 1e-9 or abs(dot(nrm, e2)) > 1e-9:
            good = False
    chk('⑥ 법선이 단위이고 평판 두 변에 수직', good)
    #  ★ 변이 — 퇴화 높이는 거부
    def raises(h):
        try:
            baffle_tris(4, h)
            return False
        except SystemExit:
            return True
    chk('⑦ 변이: h=0 · h=1 · h<0 은 거부 (퇴화 평판을 조용히 만들지 않는다)',
        raises(0.0) and raises(1.0) and raises(-0.1))
    #  ★ STL 을 실제로 파싱해 개수가 맞는가 (문자열이 STL 인지)
    txt = to_stl(t)
    chk('⑧ STL 문자열이 facet 12개 · solid/endsolid 로 감싼다',
        txt.count('facet normal') == 12 and txt.startswith('solid ')
        and txt.rstrip().endswith('endsolid LIGGGHTS_STL_EXPORT'))
    print(f'\nmake_mixer_baffles selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=6, help='배플 개수 (0 이면 안 만든다)')
    ap.add_argument('--height', type=float, default=0.10,
                    help='드럼 반경 대비 배플 높이 (0 < h < 1).  기본 0.10')
    ap.add_argument('--out', default='', help='쓸 파일 (없으면 표준출력)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    tris = baffle_tris(a.n, a.height)
    if not tris:
        raise SystemExit('⛔ --n 0 — 배플을 만들지 않는다 (덱에서도 메시 줄을 빼라)')
    txt = to_stl(tris)
    if a.out:
        open(a.out, 'w').write(txt)
        print(f'배플 {a.n}개 · 높이 {a.height:.2f}·R → {a.out} '
              f'(삼각형 {len(tris)})')
    else:
        print(txt, end='')
