#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""상별 부피 원장 캐시의 **기록 대조** — 파일명이 아니라 안의 설정으로 재사용을 판정한다.

★ 왜 (2026-08-20, Codex CDX-IJ-07): `sdcp_phase_ledger.sh` 의 캐시 키는 사람이 읽는
  태그(`ps_7_3_v015_sph_b030`)인데, 그 태그를 만드는 `${x/./}` 는 **단사가 아니다** —
  `0.3` 과 `03`(=3.0) 이 둘 다 `b03` 이 된다.  서로 다른 설정이 같은 파일을 가리키면
  `[ -s "$OUT" ]` 가 그대로 SKIP 해서 **조용한 오재사용**이 난다.
  ⇒ 태그는 가독성용으로 남기고, **동일성 판정은 저장된 JSON 이 기록한 값**이 한다.

계약: 세 값이 전부 일치해야 exit 0 (= SKIP 허용).  하나라도 다르거나 읽을 수 없으면
  exit 1 (= 재계산).  **fail-closed** — 읽지 못한 것을 "같다" 로 처리하지 않는다.

환경변수 (셸이 넘긴다):
  L_OUT  기존 ledger JSON 경로
  L_VOX  이번 런의 vox (µm)
  L_BR   이번 런의 bridge (µm, awk %g 정규화)
  L_SDD  이번 런의 SDCP 구 직경 (µm) — 점 스탬프면 빈 문자열

  python3 scripts/sdcp_phase_ledger_match.py     # 셸이 env 로 부른다
  python3 scripts/sdcp_phase_ledger_match.py --selftest
"""
from __future__ import annotations

import json
import os
import sys


def same(a, b):
    """수치 동일성.  둘 다 '없음'이면 같다, 하나만 없으면 다르다 (fail-closed)."""
    a_none = a is None or a == ''
    b_none = b is None or b == ''
    if a_none or b_none:
        return a_none and b_none
    try:
        return abs(float(a) - float(b)) < 1e-12
    except (TypeError, ValueError):
        return False


def matches(rec, vox, bridge, sdcp_d):
    """→ (일치?, 다른 항목 목록)."""
    want = (('vox_um', vox), ('bridge_um', bridge), ('sdcp_sphere_d_um', sdcp_d))
    bad = [f'{k}: 기록 {rec.get(k)!r} vs 요청 {v!r}' for k, v in want
           if not same(rec.get(k), v)]
    return (not bad), bad


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        (ok := ok + 1) if cond else fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    rec = {'vox_um': 0.15, 'bridge_um': 0.48, 'sdcp_sphere_d_um': 0.30}
    chk('① 같은 설정은 일치', matches(rec, '0.15', '0.48', '0.30')[0])
    chk('② bridge 가 다르면 불일치', not matches(rec, '0.15', '0.3', '0.30')[0])
    chk('③ 직경이 다르면 불일치', not matches(rec, '0.15', '0.48', '0.45')[0])
    chk('④ vox 가 다르면 불일치', not matches(rec, '0.125', '0.48', '0.30')[0])
    #  ★ 이 도구가 존재하는 이유 — 태그 충돌 쌍이 **기록으로는 갈린다**
    chk('⑤ ★ 태그가 충돌하는 0.3 vs 03 을 기록이 가른다 (b03 ↔ b03)',
        matches({'vox_um': 0.15, 'bridge_um': 0.3}, '0.15', '0.3', '')[0]
        and not matches({'vox_um': 0.15, 'bridge_um': 0.3}, '0.15', '3', '')[0])
    chk('⑥ 점 스탬프(직경 없음) 끼리는 일치',
        matches({'vox_um': 0.15, 'bridge_um': 0.48}, '0.15', '0.48', '')[0])
    chk('⑦ ★ 점 원장을 구 요청에 재사용하지 않는다 (fail-closed)',
        not matches({'vox_um': 0.15, 'bridge_um': 0.48}, '0.15', '0.48', '0.30')[0])
    chk('⑧ ★ 기록이 아예 없는(옛) 원장은 재사용 금지',
        not matches({'vox_um': 0.15}, '0.15', '0.48', '0.30')[0])
    print(f'\nsdcp_phase_ledger_match selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if '--selftest' in argv:
        return _selftest()
    path = os.environ.get('L_OUT', '')
    try:
        with open(path, encoding='utf-8') as f:
            rec = json.load(f)
    except Exception as e:                                     # noqa: BLE001
        print(f'  (원장을 읽을 수 없다 — 재계산: {type(e).__name__})')
        return 1
    ok, bad = matches(rec, os.environ.get('L_VOX'), os.environ.get('L_BR'),
                      os.environ.get('L_SDD'))
    if not ok:
        print('  (기록 대조 불일치 — ' + ' · '.join(bad) + ')')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
