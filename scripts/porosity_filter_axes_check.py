#!/usr/bin/env python3
"""porosity 코퍼스의 **두 필터 축이 붙지 않았는지** 본다 (원장 `GAP3-19` → `GAP3-20`).

왜 이 검사가 있나
───────────────────────────────────────────────────────────────────────────────
`load_pairs()` 는 두 가지를 거른다.  **축이 다르다.**

  · `exclude_particulate` = **레짐 선택**.  particulate / `input_S_` 는 다른 레짐
    (mono-AM_S · separator 류 · SE-rich) 이라 production 폼에서 뺀다.
    넣고 빼는 것이 **정당한 분석 선택**이다.
  · `exclude_broken`      = **무효 데이터 제외**.  `1mAh_100_*` 는 plate_z 메타데이터
    버그로 porosity 자체가 틀렸다 (CLAUDE.md).  선택이 아니라 **영구 필터**다.

⛔ 2026-09-17 이전에는 **한 스위치가 둘 다** 껐다.  그래서 "particulate 레짐을 넣자"
  는 뜻으로 `exclude_particulate=False` 를 주면 broken-sim 9 건이 **조용히 따라
  들어왔다**.  dem·mpm 이 전부 양수라 기존 게이트에 안 걸렸고, `porosity_unified.py`
  의 헤드라인이 전부 틀린 값으로 나왔다:
      n 138 → 129 · gated λ-U LOOCV 0.472 → 0.502 · production RMSE 3.01 → 2.71 %p
      (계수도 움직였다 — `sefill_x_bim` +7.54 → +18.08 = 2.4 배)

⚠⚠ **무엇이 실제로 잡는지** (초판 docstring 을 정정한다, 2026-09-17).
  처음엔 *"핵심은 2×2 분리성"* 이라고 썼는데 **틀렸다** — 결함을 일부러 되살려
  돌려 보니 분리성 세 검사는 **전부 초록**이었다.  결합된 상태에서는 broken 축의
  크기가 그냥 **0** 이 되고, `0 vs 0` · `25 vs 25` 로 합·차 항등식이 **여전히 성립**하기
  때문이다.  ⇒ 항등식은 재결합에 **눈이 멀다**.

★ 실제로 판별하는 것은 셋이다 (결함 복원 시 9 → 6 PASS, rc=1):
    ① `exclude_particulate=False` 하나만 줬을 때 `1mAh_100_*` 이 **새는지**  ← 사고 그 자체
    ② broken 축을 꺼서 **실제로 늘어나는지** (n_broken > 0) = 축이 살아 있는지
    ③ 레짐 축으로 들어온 것이 **전부 particulate/`input_S_`** 인지
  분리성 셋은 *남겨 두되* 보조 지표다 — 다른 종류의 오염(겹치는 필터)을 잡는다.

⚠ 숫자는 코퍼스가 자라면 바뀐다.  그래서 **절대값을 단언하지 않는다** (참고로만 찍는다).
"""
from __future__ import annotations

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ⚠ 이 모듈은 `__main__` 가드가 없어 **import 만으로 분석이 돈다** (기존 구조).
#    출력을 삼켜 검사 결과만 보이게 한다 — 동작은 바꾸지 않는다.
with contextlib.redirect_stdout(io.StringIO()):
    from porosity_plastic_vs_rigid import load_pairs  # noqa: E402

BROKEN_MARK = '1mAh_100'


def cases(**kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return {r['case'] for r in load_pairs(**kw)}


def is_part(c):
    return ('particulate' in c) or c.startswith('input_S_')


def main():
    fail = []

    def chk(name, cond, extra=''):
        print(f'  {"✓" if cond else "✗"} {name}' + (f'   {extra}' if extra else ''))
        if not cond:
            fail.append(name)

    prod = cases(exclude_particulate=True, exclude_broken=True)
    p_br = cases(exclude_particulate=True, exclude_broken=False)
    p_pt = cases(exclude_particulate=False, exclude_broken=True)
    both = cases(exclude_particulate=False, exclude_broken=False)

    n_broken = len(p_br) - len(prod)
    n_part = len(p_pt) - len(prod)
    print(f'  2×2  production={len(prod)}  +broken={len(p_br)}  '
          f'+particulate={len(p_pt)}  둘 다={len(both)}'
          f'   (broken {n_broken} · particulate {n_part})')

    #  ── ★★ 분리성: 한 축을 켜는 효과가 다른 축에 **의존하지 않는다** ──
    chk('★★ broken 축의 크기가 particulate 설정과 무관하다',
        len(both) - len(p_pt) == n_broken,
        f'{len(both) - len(p_pt)} vs {n_broken}')
    chk('★★ particulate 축의 크기가 broken 설정과 무관하다',
        len(both) - len(p_br) == n_part,
        f'{len(both) - len(p_br)} vs {n_part}')
    chk('★ 두 집합이 겹치지 않는다 (합이 정확히 맞는다)',
        len(both) == len(prod) + n_broken + n_part)

    #  ── ★★★ 실사고 재현: 레짐만 넓혔는데 무효 데이터가 따라오면 안 된다 ──
    leaked = sorted(c for c in p_pt if BROKEN_MARK in c)
    chk('★★★ `exclude_particulate=False` 로 레짐만 넓혀도 **무효 9건은 안 따라온다**',
        not leaked, f'샌 케이스 {leaked[:3]}' if leaked else '')

    #  ── 각 축이 실제로 **일을 한다** (검사가 공회전이 아님을 증명) ──
    chk('broken 축이 실제로 거른다 (끄면 들어온다)', n_broken > 0, f'n={n_broken}')
    chk('particulate 축이 실제로 거른다 (끄면 들어온다)', n_part > 0, f'n={n_part}')
    chk('production 에는 무효도 particulate 도 없다',
        not any(BROKEN_MARK in c for c in prod) and not any(is_part(c) for c in prod))
    chk('★ 들어온 broken 은 전부 `1mAh_100_*` 이다 (다른 것이 섞이지 않았다)',
        all(BROKEN_MARK in c for c in (p_br - prod)))
    chk('★ 들어온 particulate 는 전부 particulate/`input_S_` 이다',
        all(is_part(c) for c in (p_pt - prod)))

    print(f'\nporosity_filter_axes SELFTEST {9 - len(fail)} PASS '
          + ('ALL GREEN' if not fail else f'FAIL {fail}'))
    return 1 if fail else 0


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser(description='porosity 필터 두 축의 분리 검사 (GAP3-19/20)')
    ap.add_argument('--selftest', action='store_true',
                    help='검사를 돈다 (인자 없이 돌려도 같다 — 이 파일은 검사가 전부다)')
    ap.parse_args()
    raise SystemExit(main())
