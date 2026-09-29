#!/usr/bin/env python3
"""두 구의 교차 원판 — **순수 기하** (Physics 피복률 경로와 분리 · 2026-09-30 · Codex `LHSC-05` 계약 (a) · 1저자 비준 "권고대로").

왜 따로인가: `lhs_descriptor_harvest` (item 2 접촉 면적 대조) 는 이 함수 하나만 필요한데 `plastic_coverage` 에서 가져오면
Physics 피복률 경로 (`film_area_from_overlap` · `A_volume = V/H_FILM_MIN` · `DESC-03` · 계약④) 에 의존이 생기고, 그것을 막던 AST 가드는
패키지 경유 (`from scripts import plastic_coverage as pc`) · 별칭 동적 import (`from importlib import import_module as im`) 를 못 봤다.
⇒ 구현을 여기로 옮기고 수확기는 여기서만 가져온다 (의존 자체가 없다).  `plastic_coverage._intersection_disc_area` 는 이 함수의
**별칭** (한 구현 · 규율 ①) — 그쪽 selftest ⑲ 와 수확기 ㉑ 이 같은 객체임을 본다.  값 · 부동소수 결과는 옮기기 전과 같다
(`math.pi == np.pi` · 식 그대로 — `coverage_physics_vs_hertzian --selftest` ① legacy 바이트 핀이 그 증거).

    python3 scripts/lens_geometry.py --selftest
"""
import math
import sys


def intersection_disc_area(r1, r2, delta):
    """두 구의 **교차 원판** 면적 (판정문이 `ligg_area` 로 쓴 규약 · LIGGGHTS `c_cpl[22]` 기하 = `L1-04`).

    중심거리 `d = r₁+r₂−δ` 일 때 교차원 반지름 a 는
        `a² = [4d²r₁² − (d² − r₂² + r₁²)²] / (4d²)`
    ★ 동일 반경 검산: `A = π δ(4r − δ)/4`, 얕은 극한에서 Hertz(`πR*δ`)의 **2배**
      (`A_LIGG/A_Hertz = 2 − δ/(2r)` = `L1-04` 의 형태).
    포함 (`d ≤ |r₁ − r₂|` · 한 구가 다른 구 안) 이면 a² ≤ 0 → 0.  δ ≤ 0 (안 닿음) · d ≤ 0 도 0.
    ⚠ 포함 경계 근처에서는 r₁ − r₂ 에 불연속 · 비단조 — 반올림 전파 허용폭이 서지 않는다 (`lhs_descriptor_harvest._in_domain_rows`).
    """
    d = r1 + r2 - delta
    if d <= 0 or delta <= 0:
        return 0.0
    a2 = (4.0 * d * d * r1 * r1 - (d * d - r2 * r2 + r1 * r1) ** 2) / (4.0 * d * d)
    return float(math.pi * max(a2, 0.0))


def _selftest() -> int:
    fails = []

    def chk(name, cond, extra=''):
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        if not cond:
            fails.append(name)

    r, dlt = 0.5, 0.0125
    a = intersection_disc_area(r, r, dlt)
    chk('① 동일 반경 항등식 A = π δ (4r − δ)/4 (닫힌 식 ↔ 일반식 · 상대 1e-12)', abs(a - math.pi * dlt * (4 * r - dlt) / 4) < 1e-12 * a, f'{a:.12e}')
    chk('② 얕은 극한 A/(π R* δ) = 2 − δ/(2r) (L1-04)', abs(a / (math.pi * (r / 2) * dlt) - (2 - dlt / (2 * r))) < 1e-12)
    chk('③ 포함 (한 구가 다른 구 안 · d ≤ |r1 − r2|) → 0 · 안 닿음 (δ ≤ 0) → 0',
        intersection_disc_area(2.0, 1.0, 2.0) == 0.0 and intersection_disc_area(2.0, 1.0, 2.5) == 0.0
        and intersection_disc_area(1.0, 1.0, 0.0) == 0.0 and intersection_disc_area(1.0, 1.0, -0.1) == 0.0)
    chk('④ 반경 대칭 · δ 에 단조 증가 (경계 밖)',
        intersection_disc_area(2.0, 0.5, 0.05) == intersection_disc_area(0.5, 2.0, 0.05)
        and intersection_disc_area(1.0, 1.0, 0.1) < intersection_disc_area(1.0, 1.0, 0.2) < intersection_disc_area(1.0, 1.0, 0.5))
    try:
        import numpy as _np
        chk('⑤ math.pi == np.pi — 옮기기 전 (np.pi) 과 같은 부동소수 결과', math.pi == _np.pi
            and intersection_disc_area(1.0, 0.5, 0.05) == float(_np.pi * max(
                (4.0 * 1.45 ** 2 * 1.0 - (1.45 ** 2 - 0.25 + 1.0) ** 2) / (4.0 * 1.45 ** 2), 0.0)))
    except ImportError:
        chk('⑤ numpy 없음 — 건너뜀', True)
    print(f'\nlens_geometry SELFTEST {"PASS" if not fails else f"FAIL ({len(fails)})"}')
    return 0 if not fails else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(_selftest())
    print(__doc__)
