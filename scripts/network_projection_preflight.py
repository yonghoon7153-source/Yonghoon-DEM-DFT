#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""projection-clear 의 코퍼스 영향을 **재분석 없이·읽기 전용으로** 미리 잰다 (RC6-Q7).

★ 왜 필요한가.  RC5-03 수정으로 merge 전에 network-owned projection 을 **전부 걷어내고**
  새 세대로만 채우게 했다.  옳은 변경이지만 그 결과 **지금 게시된 케이스 중 몇 개가
  어떤 채널을 잃는지 아무도 모른다**.  Codex 6회차 §8:

    "tracked tree 에 full_metrics/per-mode JSON 이 0개다 → 비율을 계산할 근거가 없다.
     현재 코드에도 mutation 전 read-only preflight scanner 가 없다."

  `network_projection_dropped` 는 **mutation 후에만** 생기므로 사전 영향 측정의
  대체물이 아니다.

★★ 이 스크립트는 **아무것도 쓰지 않는다** ★★
  파일을 열되 `'r'` 로만 열고, 시뮬레이션은 전부 **메모리에서** 한다.  결과 리포트조차
  `--out` 을 명시해야 쓴다.  (마이그레이션 영향을 재려고 마이그레이션을 하면 안 된다.)

★ production 과 **같은 정의**를 쓴다.  merge 키 목록은 `pipeline_service.NET_MERGE_KEYS`
  하나뿐이고 app.py 도 그것을 참조한다 — 스캐너가 자기 사본을 들면 스캔 결과가 production
  과 어긋나 오히려 오도한다.

분류 (mode×channel 단위):
  retained          새 세대가 값을 냈다 (유지)
  validly_cleared   상류가 valid_zero/valid_null 등 **정상적으로** 값이 없다
  lost_unknown      옛 값이 있었는데 새 세대가 못 내고, 그 이유도 모른다  ← 위험
  failed            상류 status 가 failed
  contradiction     status 와 값이 어긋난다 (computed 인데 값 없음 등)
  absent            원래도 없었다 (영향 없음)

사용:
  python3 scripts/network_projection_preflight.py --roots results archive
  python3 scripts/network_projection_preflight.py --roots results --out preflight.json
  python3 scripts/network_projection_preflight.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'webapp'))
import pipeline_service as ps          # noqa: E402  (정의를 공유한다 — 사본 금지)

FM = 'full_metrics.json'
LEGACY = 'network_conductivity.json'
DUAL = 'network_conductivity_dual.json'
MODE_FILES = {'hertzian': 'network_conductivity_hertzian.json',
              'physics': 'network_conductivity_physics.json'}

#: 위험 등급 — 이 중 하나라도 있으면 그 케이스는 **재분석/게시를 막아야 한다**.
BLOCKING = ('lost_unknown', 'failed', 'contradiction')


def _read(path):
    """읽기 전용.  없거나 깨졌으면 None (스캐너는 절대 고치지 않는다)."""
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def simulate_merge(case_dir):
    """production 의 projection clear + merge 를 **메모리에서만** 재현한다.

    app.py 의 순서를 그대로 따른다:
      ① `_NET_MERGE_KEYS` 전부 pop  ② legacy JSON 에서 non-None 만 채움
      ③ dual JSON 에서 `NET_PHYSICS_MIRROR_KEYS` 를 `<key>_physics` 로 미러
    """
    fm = _read(os.path.join(case_dir, FM))
    if fm is None:
        return None
    before = {k: fm.get(k) for k in ps.NET_MERGE_KEYS}
    after = {}
    net = _read(os.path.join(case_dir, LEGACY)) or {}
    for k in ps.NET_MERGE_KEYS:
        v = net.get(k)
        if v is not None:
            after[k] = v
    dual = _read(os.path.join(case_dir, DUAL)) or {}
    rP = dual.get('physics') or {}
    for k in ps.NET_PHYSICS_MIRROR_KEYS:
        if rP.get(k) is not None:
            after[f'{k}_physics'] = rP[k]
    return before, after


def classify(case_dir):
    """→ {'case', 'keys': {key: verdict}, 'blocking': [...], 'modes': {...}}"""
    sim = simulate_merge(case_dir)
    if sim is None:
        return {'case': os.path.basename(case_dir), 'error': f'{FM} 없음/깨짐',
                'keys': {}, 'blocking': ['no_full_metrics']}
    before, after = sim
    # 상류 mode 별 상태 (thermal 만 status 가 있다 — 나머지는 아직 무상태다, RC7-02)
    modes = {}
    for mode, fname in MODE_FILES.items():
        d = _read(os.path.join(case_dir, fname))
        if d is None:
            modes[mode] = {'present': False, 'thermal_status': None}
        else:
            modes[mode] = {'present': True, 'thermal_status': d.get('thermal_status')}
    th_fail = any(m['thermal_status'] == 'failed' for m in modes.values())
    th_validnull = any(m['thermal_status'] in ('valid_zero', 'valid_null')
                       for m in modes.values())

    keys = {}
    for k in ps.NET_MERGE_KEYS:
        old, new = before.get(k), after.get(k)
        if new is not None:
            keys[k] = 'retained'
        elif old is None:
            keys[k] = 'absent'
        elif k.startswith('thermal_') and th_fail:
            keys[k] = 'failed'
        elif k.startswith('thermal_') and th_validnull:
            keys[k] = 'validly_cleared'
        else:
            # 옛 값이 있었는데 새 세대가 못 냈고 이유도 없다 — 이것이 위험한 자리다.
            keys[k] = 'lost_unknown'
    # status ↔ 값 모순: thermal 이 computed 인데 값이 안 나온 경우
    for mode, m in modes.items():
        if m['thermal_status'] == 'computed':
            kk = 'thermal_sigma_full_mScm' + ('_physics' if mode == 'physics' else '')
            if after.get(kk) is None:
                keys[kk] = 'contradiction'
    blocking = sorted({v for v in keys.values() if v in BLOCKING})
    prov = _read(os.path.join(case_dir, ps.PROVENANCE_FILE)) or {}
    return {'case': os.path.basename(case_dir), 'keys': keys, 'blocking': blocking,
            'modes': modes, 'network_run_id': prov.get('network_run_id'),
            'lost_keys': sorted(k for k, v in keys.items() if v == 'lost_unknown')}


def find_cases(roots):
    """`full_metrics.json` 이 있는 디렉터리 = 케이스."""
    out = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dn, files in os.walk(root):
            if FM in files:
                out.append(dirpath)
    return sorted(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--roots', nargs='+', default=['results', 'archive'])
    ap.add_argument('--out', help='리포트 JSON 경로 (명시해야만 쓴다 — 기본은 읽기 전용)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    cases = find_cases(a.roots)
    print(f'══ projection-clear 사전영향 (읽기 전용) — 케이스 {len(cases)} ══')
    if not cases:
        print(f'   {a.roots} 아래에 {FM} 이 없다.')
        print('   ⚠ 이 리포에는 tracked corpus 가 없다 — 실제 배포 머신에서 돌려야 뜻이 있다.')
        return 0

    rows = [classify(c) for c in cases]
    tally = {}
    for r in rows:
        for v in r['keys'].values():
            tally[v] = tally.get(v, 0) + 1
    blocked = [r for r in rows if r['blocking']]

    print(f'\n{"판정":<18} {"키 수":>7}')
    for v in ('retained', 'absent', 'validly_cleared', 'failed',
              'contradiction', 'lost_unknown'):
        if tally.get(v):
            print(f'  {v:<16} {tally[v]:>7}')

    print(f'\n── 차단 대상 {len(blocked)}/{len(rows)} 케이스 ──')
    for r in blocked[:20]:
        print(f"  {r['case']:<34} {','.join(r['blocking'])}"
              + (f"  잃는 키 {len(r['lost_keys'])}" if r.get('lost_keys') else ''))
    if len(blocked) > 20:
        print(f'  … 외 {len(blocked) - 20}건')

    if a.out:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump({'roots': a.roots, 'n_cases': len(rows), 'tally': tally,
                       'blocked': [r['case'] for r in blocked], 'cases': rows},
                      f, ensure_ascii=False, indent=1)
        print(f'\n리포트 → {a.out}')

    print('\n⚠ 이 스캐너는 **아무것도 쓰지 않는다** (--out 제외).  차단 대상이 있으면 '
          '그 케이스의\n  재분석·게시를 멈추고 원인을 먼저 규명할 것 — lost_unknown 은 '
          '"옛 값이 있었는데\n  새 세대가 못 내고 이유도 모른다" 는 뜻이다.')
    return 1 if blocked else 0


def _selftest():
    import shutil
    import tempfile
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    d = tempfile.mkdtemp(prefix='pfl_')
    try:
        def case(name, fm, legacy=None, dual=None, hz=None, ph=None):
            c = os.path.join(d, name)
            os.makedirs(c, exist_ok=True)
            json.dump(fm, open(os.path.join(c, FM), 'w'))
            if legacy is not None:
                json.dump(legacy, open(os.path.join(c, LEGACY), 'w'))
            if dual is not None:
                json.dump(dual, open(os.path.join(c, DUAL), 'w'))
            for blob, fn in ((hz, MODE_FILES['hertzian']), (ph, MODE_FILES['physics'])):
                if blob is not None:
                    json.dump(blob, open(os.path.join(c, fn), 'w'))
            return c

        # ① 새 세대가 다 냈다 → retained
        #   ⚠ 실제 both-mode 런은 **dual 파일도** 만든다.  없으면 physics 미러가 안 일어나
        #     physics 가 computed 라고 적힌 것과 모순이 된다 (아래 ①b 가 그것을 시험한다).
        c1 = case('keep', {'sigma_full_mScm': 1.0, 'thermal_sigma_full_mScm': 2.0},
                  legacy={'sigma_full_mScm': 9.0, 'thermal_sigma_full_mScm': 8.0,
                          'thermal_status': 'computed'},
                  dual={'physics': {'sigma_full_mScm': 3.3, 'thermal_sigma_full_mScm': 4.4}},
                  hz={'thermal_status': 'computed'}, ph={'thermal_status': 'computed'})
        r1 = classify(c1)
        ok('1) 새 세대가 낸 키는 retained',
           r1['keys']['sigma_full_mScm'] == 'retained'
           and r1['keys']['thermal_sigma_full_mScm_physics'] == 'retained'
           and not r1['blocking'])

        # ①b ★ physics 가 computed 라는데 dual 이 없어 미러가 안 되면 그것도 모순이다
        c1b = case('nodual', {'thermal_sigma_full_mScm': 2.0},
                   legacy={'sigma_full_mScm': 9.0, 'thermal_sigma_full_mScm': 8.0},
                   hz={'thermal_status': 'computed'}, ph={'thermal_status': 'computed'})
        ok('1b) ★ physics=computed 인데 dual 부재 → contradiction (미러 경로가 끊겼다)',
           classify(c1b)['keys']['thermal_sigma_full_mScm_physics'] == 'contradiction')

        # ② 옛 thermal 이 있는데 새 세대가 못 냈고 이유도 없다 → lost_unknown (위험)
        c2 = case('lost', {'sigma_full_mScm': 1.0, 'thermal_sigma_full_mScm': 111.0},
                  legacy={'sigma_full_mScm': 9.0})
        r2 = classify(c2)
        ok('2) ★ 이유 없이 사라지는 옛 값을 lost_unknown 으로 잡는다',
           r2['keys']['thermal_sigma_full_mScm'] == 'lost_unknown'
           and 'lost_unknown' in r2['blocking'])

        # ③ 상류가 valid_null → 정당한 제거 (위험 아님)
        c3 = case('validnull', {'thermal_sigma_full_mScm': 111.0},
                  legacy={'sigma_full_mScm': 9.0},
                  hz={'thermal_status': 'valid_null'}, ph={'thermal_status': 'valid_null'})
        r3 = classify(c3)
        ok('3) ★ valid_null 상류는 validly_cleared (차단 아님)',
           r3['keys']['thermal_sigma_full_mScm'] == 'validly_cleared'
           and 'lost_unknown' not in r3['blocking'])

        # ④ 상류 failed → failed (차단)
        c4 = case('failed', {'thermal_sigma_full_mScm': 111.0},
                  legacy={'sigma_full_mScm': 9.0}, hz={'thermal_status': 'failed'})
        r4 = classify(c4)
        ok('4) 상류 failed 는 차단 대상',
           r4['keys']['thermal_sigma_full_mScm'] == 'failed' and 'failed' in r4['blocking'])

        # ⑤ status=computed 인데 값이 없다 → contradiction
        c5 = case('contra', {'thermal_sigma_full_mScm': 5.0},
                  legacy={'sigma_full_mScm': 9.0}, hz={'thermal_status': 'computed'})
        r5 = classify(c5)
        ok('5) ★ status=computed 인데 값이 없으면 contradiction',
           r5['keys']['thermal_sigma_full_mScm'] == 'contradiction'
           and 'contradiction' in r5['blocking'])

        # ⑥ physics 는 **dual 파일**에서 온다 (production 과 같은 경로)
        c6 = case('dual', {'sigma_full_mScm_physics': 7.0},
                  legacy={'sigma_full_mScm': 9.0},
                  dual={'physics': {'sigma_full_mScm': 3.3}})
        r6 = classify(c6)
        ok('6) ★ physics 키를 dual 에서 미러한다 (physics.json 이 아니다)',
           r6['keys']['sigma_full_mScm_physics'] == 'retained')

        # ⑦ 원래 없던 키는 영향 없음
        ok('7) 원래 없던 키는 absent', r1['keys'].get('sigma_bruggeman') == 'absent')

        # ⑧ ★ 읽기 전용 — 스캔이 파일을 바꾸지 않는다
        import hashlib
        def snap(root):
            h = {}
            for dp, _dn, fs in os.walk(root):
                for f in fs:
                    p = os.path.join(dp, f)
                    h[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            return h
        b4 = snap(d)
        for c in find_cases([d]):
            classify(c)
        ok('8) ★★ 스캔이 **아무 파일도 바꾸지 않는다** (읽기 전용 계약)', snap(d) == b4)

        ok('9) 케이스 탐색이 full_metrics 로 판별', len(find_cases([d])) == 7)
        # ⑩ production 과 같은 정의를 쓴다 (사본 금지)
        ok('10) ★ merge 키를 pipeline_service 에서 가져온다 (스캐너 사본 없음)',
           ps.NET_MERGE_KEYS is not None and len(ps.NET_MERGE_KEYS) >= 20)
        ok('11) full_metrics 없으면 안전하게 보고', classify(os.path.join(d, 'nope'))['blocking'])
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print(f'\nnetwork_projection_preflight selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
