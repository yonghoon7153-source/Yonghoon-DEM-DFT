#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""압력 단위 규약 — **필드 이름이 단위를 정한다.  값 크기로 추정하지 않는다.**

코드리뷰 F-11 대응.  옛 구현은 세 곳(`webapp/app.py`, `scripts/grade_engine.py`,
`scripts/rank_all_cases.py`)에 **같은 heuristic 을 복제**해 두고 있었다:

    tp = ip.get('target_press_sim') or ip.get('target_pressure_MPa')
    MPa = float(tp) * 1000 if float(tp) < 10 else float(tp)

두 가지가 틀렸다.

① **이름이 다른 두 필드를 한 변수로 합쳤다.**  `target_press_sim` 은 덱 단위(×1000 → MPa),
   `target_pressure_MPa` 는 **이미 MPa** 다.  단위가 다른 값을 같은 변수에 담으면 그 뒤
   어떤 변환도 추측이 된다.
② **값 크기로 단위를 판정했다** (`< 10` 이면 덱 단위로 간주).  그래서
   `target_pressure_MPa` 에 10 미만을 넣으면 **1000 배**가 된다:

       0.3 MPa → 300 MPa       2 MPa → 2000 MPa       5 MPa → 5000 MPa

   ★ 하필 그 구간이 **ASSB 운전 스택압**이다 (우리 앵커 CSV 에도 "비대칭압 2.5/0.2 MPa"
   가 있다).  가상의 입력이 아니라 이 프로젝트가 실제로 쓰는 값이 파손된다.

⇒ 여기서는 **필드 이름으로만** 판정하고, 크기 heuristic 을 쓰지 않는다.  또 falsy 검사
   (`a or b`) 대신 `is not None` 을 써서 **0 이 유효한 값**일 때 다음 필드로 새지 않게 한다.

⚠ 이 함수는 **제작(소결) 목표압** 하나만 돌려준다.  리뷰 F-11 이 요구한 네 축 분리
   (제작압 / 운전압 / MPM wallP 실측 / DEM 접촉압 분포)는 각 소비처가 서로 다른 키를
   써야 하는 별도 작업이다 — 여기서 한 값으로 합치지 않는다.
"""
from __future__ import annotations

#: 덱(sim) 압력 → MPa.  규약: Scale r×1000 · E×0.001 · P×0.001 → 압력은 ×1000 이 역변환.
SIM_TO_MPA = 1000.0

#: 필드 이름 → MPa 로 가는 배수.  **이 표가 단위의 정본**이다.
_FIELD_TO_MPA = {
    'target_press_sim': SIM_TO_MPA,     # 덱 단위
    'target_pressure_MPa': 1.0,         # 이미 MPa
}


def target_pressure_mpa(input_params, default=None):
    """제작 목표압을 MPa 로 돌려준다.  없으면 `default`.

    필드 이름이 단위를 정한다 (F-11).  `target_press_sim` 이 우선이고, 없을 때만
    `target_pressure_MPa` 를 본다 — 둘 다 있으면 덱 값이 원본에 가깝기 때문.
    """
    if not isinstance(input_params, dict):
        return default
    for field, mult in _FIELD_TO_MPA.items():
        v = input_params.get(field)
        if v is None or v == '':
            continue                    # ★ falsy 가 아니라 None/'' 만 건너뛴다 (0 은 유효)
        try:
            return float(v) * mult
        except (TypeError, ValueError):
            continue
    return default


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    def old(sim, mpa):
        """옛 heuristic — 무엇이 달라졌는지 대조용."""
        tp = sim or mpa
        return None if tp is None else (float(tp) * 1000 if float(tp) < 10 else float(tp))

    # ── 정상 동작 (옛 코드와 같아야 하는 것) ──
    ok('1) 덱 단위 0.30 → 300 MPa',
       target_pressure_mpa({'target_press_sim': 0.30}) == 300.0)
    ok('2) 덱 단위 0.10 → 100 MPa',
       target_pressure_mpa({'target_press_sim': 0.10}) == 100.0)
    ok('3) 이미 MPa 인 300 → 300', target_pressure_mpa({'target_pressure_MPa': 300}) == 300.0)

    # ── ★ 옛 heuristic 이 1000배로 파손하던 것 (ASSB 운전 스택압 구간) ──
    for v in (0.2, 0.3, 2.0, 2.5, 5.0):
        got, was = target_pressure_mpa({'target_pressure_MPa': v}), old(None, v)
        ok(f'4) ★ target_pressure_MPa={v} → {v} (옛: {was:g} = {was / v:.0f}배 파손)',
           got == v and was == v * 1000)

    # ── falsy 새어나감 ──
    ok('5) ★ sim=0 이 유효값으로 처리된다 (옛 `a or b` 는 MPa 로 샜다)',
       target_pressure_mpa({'target_press_sim': 0, 'target_pressure_MPa': 7}) == 0.0
       and old(0, 7) == 7000.0)
    ok('6) 없으면 default', target_pressure_mpa({}, default=-1) == -1
       and target_pressure_mpa({'target_press_sim': None}) is None)
    ok('7) 빈 문자열은 건너뛰고 다음 필드를 본다',
       target_pressure_mpa({'target_press_sim': '', 'target_pressure_MPa': 4.0}) == 4.0)
    ok('8) 문자열 숫자도 받는다', target_pressure_mpa({'target_press_sim': '0.30'}) == 300.0)
    ok('9) 파싱 불가는 default', target_pressure_mpa({'target_press_sim': 'abc'}) is None)
    ok('10) dict 아니면 default', target_pressure_mpa(None, default=0) == 0)

    print(f'\npress_units selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(_selftest())
