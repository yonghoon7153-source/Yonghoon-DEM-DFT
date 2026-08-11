#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`--contact-mode both` 산출물 읽기 — Hertzian/Physics 두 모드를 **둘 다** 가져온다.

★ RC5-04 (Codex 5회차 교차검증).  `run_network_full_corrections._run_solver()` 는
자식 솔버를 `--contact-mode both` 로 돌려 놓고 **`network_conductivity.json` 하나만**
읽어 돌려줬다.  그 파일은 `per_mode_results['hertzian']` 의 back-compat 복사본이라
Physics 결과가 들어 있지 않다.  그런데 호출부는

    res.get('sigma_full_mScm_physics')

를 조회했고 — 심지어 "같은 JSON 에 `*_physics` 짝이 있다"는 주석까지 달려 있었다 —
그 값은 **항상 None** 이었다.  결과: Physics Stage E 가 매번 weighted-factor fallback
으로 새고, 실제 재솔브 값이 통째로 버려졌다.

  Codex 실측: 실제 Physics 재솔브 ionic/electronic/thermal = 101 / 202 / 303
              최종 보고값                                  = 500 / 1000 / 1500
              (= 옛 Physics baseline 1000/2000/3000 × 0.5, source 전부 fallback)

**원인은 이름 규약의 오해다**: 접미사는 **키가 아니라 파일명**에 붙는다.
  network_conductivity_hertzian.json → {'sigma_full_mScm': …}
  network_conductivity_physics.json  → {'sigma_full_mScm': …}   ← 같은 키!
  network_conductivity.json          → hertzian 의 복사본 (하위호환)

이 모듈은 **pandas 없이** 돌아간다 — 원래 함수가 있던 파일이 pandas 를 import 해서
회귀 테스트가 그 함수 하나를 검증하지 못했다.  버그를 못 잡은 이유 중 하나가
"테스트할 수 없는 자리에 있었다" 는 것이므로, 검증 가능한 자리로 옮긴다.

  python3 scripts/network_mode_io.py --selftest
"""
from __future__ import annotations

import json
import os
import sys

#: `--contact-mode both` 이 쓰는 per-mode 파일.
MODE_FILES = {'hertzian': 'network_conductivity_hertzian.json',
              'physics':  'network_conductivity_physics.json'}

#: 하위호환 파일 — hertzian 결과의 복사본.
LEGACY_FILE = 'network_conductivity.json'

#: 두 모드에서 다 있어야 하는 채널.  호출부는 `<key>` / `<key>_physics` 로 조회한다.
MODE_CHANNELS = ('sigma_full_mScm', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm')


def _load(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def collect_modes(tmp, warn=None):
    """per-mode JSON 을 읽어 **평평한 한 dict** 로 합친다.  없으면 None.

    반환 규약은 호출부를 그대로 두기 위해 평평하게 유지한다:
      hertzian 채널 → `<key>`          (옛 반환값과 동일)
      physics  채널 → `<key>_physics`  (이제 실제로 존재한다)

    구조화(`{hertzian:…, physics:…}`)가 더 깔끔하지만 호출부 전체를 건드려야 해서,
    **값이 틀리는 문제부터 최소 변경으로** 닫는다.  어느 모드가 실제로 있었는지는
    `_modes_present` 에, 빠진 채널은 `_modes_missing_channels` 에 남긴다 — 조용한
    결손이 이 버그를 4개월 숨겼으므로 결손은 반드시 드러낸다.

    `warn` 은 결손 메시지를 받는 콜러블 (기본 stderr).  값이 없는 것 자체는 물리적으로
    정상일 수 있으므로(퍼콜 실패 등) 예외를 던지지 않고 보고만 한다.
    """
    warn = warn if warn is not None else (lambda m: sys.stderr.write(m + '\n'))
    out, present = {}, []
    for mode, fname in MODE_FILES.items():
        data = _load(os.path.join(str(tmp), fname))
        if data is None:
            continue
        present.append(mode)
        if mode == 'hertzian':
            out.update(data)
        else:
            for k, v in data.items():
                out[f'{k}_physics'] = v
    if not present:
        data = _load(os.path.join(str(tmp), LEGACY_FILE))
        if data is None:
            return None
        out, present = dict(data), ['legacy']
    missing = [f'{m}.{c}' for m in ('hertzian', 'physics') for c in MODE_CHANNELS
               if (c if m == 'hertzian' else f'{c}_physics') not in out]
    out['_modes_present'] = present
    if missing:
        out['_modes_missing_channels'] = missing
        warn(f'[stage-e] per-mode 채널 결손: {", ".join(missing)} '
             f'(있는 모드: {", ".join(present)})')
    return out or None


def _selftest():
    import shutil
    import tempfile
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    d = tempfile.mkdtemp(prefix='nmio_')
    warns = []
    try:
        def put(fname, **kw):
            json.dump(kw, open(os.path.join(d, fname), 'w'))

        # Codex 가 재현한 그 상황: 재솔브 physics 101/202/303 vs hertzian 1/2/3
        put(MODE_FILES['hertzian'], sigma_full_mScm=1.0,
            electronic_sigma_full_mScm=2.0, thermal_sigma_full_mScm=3.0)
        put(MODE_FILES['physics'], sigma_full_mScm=101.0,
            electronic_sigma_full_mScm=202.0, thermal_sigma_full_mScm=303.0)
        put(LEGACY_FILE, sigma_full_mScm=1.0)            # hertzian 복사본
        r = collect_modes(d, warn=warns.append)
        ok('1) ★ Physics 재솔브 값이 살아 돌아온다 (옛 코드는 항상 None)',
           r['sigma_full_mScm_physics'] == 101.0
           and r['electronic_sigma_full_mScm_physics'] == 202.0
           and r['thermal_sigma_full_mScm_physics'] == 303.0)
        ok('2) Hertzian 은 옛 반환값과 같은 자리 그대로 (하위호환)',
           r['sigma_full_mScm'] == 1.0 and r['thermal_sigma_full_mScm'] == 3.0)
        ok('3) 두 모드가 섞이지 않는다 (같은 키인데 파일만 다르다는 것이 이 버그의 원인)',
           r['sigma_full_mScm'] != r['sigma_full_mScm_physics'])
        ok('4) 어느 모드가 있었는지 기록', sorted(r['_modes_present']) == ['hertzian', 'physics'])
        ok('5) 결손이 없으면 경고도 없다',
           '_modes_missing_channels' not in r and not warns)

        os.unlink(os.path.join(d, MODE_FILES['physics']))
        warns.clear()
        r2 = collect_modes(d, warn=warns.append)
        ok('6) ★ physics 부재 → None 이지만 **보고한다** (조용한 결손 금지)',
           r2.get('sigma_full_mScm_physics') is None
           and any('physics' in m for m in r2['_modes_missing_channels'])
           and len(warns) == 1)
        ok('7) 그때도 hertzian 은 정상', r2['sigma_full_mScm'] == 1.0)

        os.unlink(os.path.join(d, MODE_FILES['hertzian']))
        r3 = collect_modes(d, warn=warns.append)
        ok('8) per-mode 가 전무하면 legacy 로 (옛 동작 보존)',
           r3['sigma_full_mScm'] == 1.0 and r3['_modes_present'] == ['legacy'])

        os.unlink(os.path.join(d, LEGACY_FILE))
        ok('9) 아무 파일도 없으면 None', collect_modes(d, warn=warns.append) is None)

        open(os.path.join(d, LEGACY_FILE), 'w').write('{not json')
        ok('10) 깨진 JSON 은 None (예외 아님)', collect_modes(d, warn=warns.append) is None)
        json.dump([1, 2], open(os.path.join(d, LEGACY_FILE), 'w'))
        ok('11) dict 아닌 JSON 도 None', collect_modes(d, warn=warns.append) is None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print(f'\nnetwork_mode_io selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(_selftest() if '--selftest' in sys.argv or len(sys.argv) == 1 else 0)
