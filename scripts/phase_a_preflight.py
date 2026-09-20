#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase A 96팔 **사전 점검** — 어댑터를 돌리기 전에 봉인 3축을 초 단위로 확인한다.

    python3 scripts/phase_a_preflight.py --pa ~/pa
    python3 scripts/phase_a_preflight.py --dir <payload 디렉터리> [--dir ...]
    python3 scripts/phase_a_preflight.py --selftest

━━ 왜 어댑터만으로 부족한가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
어댑터(`phase_a_arms_from_payload.py`)가 **정본 게이트**이고 이 도구는 그것을 대체하지
않는다.  다만 어댑터는 팔당 150 MB × 96 = **약 4.8 GB** 를 읽고서야 거부한다.
2026-09-18 의 봉인 이탈이 정확히 그렇게 발견됐다 (판정 직전).
⇒ **영수증만 읽어** 같은 3축을 먼저 본다.  영수증은 수 KB 다.

━━ 무엇을 보나 — 2026-09-18 에 실제로 어긋났던 **그 셋** ━━━━━━━━━━━━━━━━━━
  ① `ptfe_stamp`   봉인 `centerline` ↔ 실제 `off` 였다
  ② LEAN = 2       `--no-ion --no-pore …` 가 안 켜져 6 성분이 돌았다
  ③ `code_sha`     전 계층 `null` 이었다 (CL-75 = 인용 금지)
정본 = `docs/reviews/phase_a_6mah_order_prereg_20260907.md` §5 ·
       `docs/reviews/phase_a_seal_breach_20260918.md`

★ 봉인 축은 **어댑터의 `SEAL` 을 그대로 가져온다** — 여기에 다시 타이핑하면 두 벌이
  되고, 두 벌은 반드시 어긋난다.  (이 세션에서 `--expect-physics` 선언이 봉인 목록과
  갈라져 사고가 났다.  같은 실수를 검사기 층에서 되풀이하지 않는다.)

⚠⚠ **통과가 "판정해도 된다" 는 뜻이 아니다.**  이 도구는 영수증과 표본 1팔만 본다.
  전수 대조·origin 색인·수렴 표지·조성 교차확인은 **어댑터가** 한다.
  ⇒ 초록이면 어댑터로 넘어가라는 뜻이고, 빨강이면 어댑터를 돌릴 필요가 없다는 뜻이다.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def _adapter():
    """어댑터 모듈 — `SEAL` 의 **단일 출처**."""
    p = os.path.join(_HERE, 'phase_a_arms_from_payload.py')
    spec = importlib.util.spec_from_file_location('_pa_adapter', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


#: LEAN = 2 (σ_e 전용) 의 `component_plan` — 사전등록 §5 `--no-ion --no-pore`
LEAN2_PLAN = {'electronic': True, 'ionic': False, 'thermal': False,
              'pore': False, 'collector': False}

_CHUNK = 1 << 20


def scan_payload(path, keys=('component_plan', 'code_sha')):
    """150 MB JSON 을 **통째로 파싱하지 않고** 작은 조각만 뽑는다.

    ⚠ `json.load` 는 팔당 수 GB 메모리를 쓴다.  사전 점검이 본 런보다 비싸면 안 된다.
    ⚠ 경계에 걸친 문자열을 놓치지 않도록 청크를 **겹쳐서** 읽는다.
    """
    want = {k: None for k in keys}
    tail = ''
    pats = {'component_plan': re.compile(r'"component_plan"\s*:\s*(\{[^{}]*\})'),
            'code_sha': re.compile(r'"code_sha"\s*:\s*("(?:[^"\\]|\\.)*"|null)')}
    with open(path, encoding='utf-8', errors='replace') as fh:
        while True:
            buf = fh.read(_CHUNK)
            if not buf:
                break
            hay = tail + buf
            for k in keys:
                if want[k] is None:
                    m = pats[k].search(hay)
                    if m:
                        want[k] = m.group(1)
            if all(v is not None for v in want.values()):
                break
            tail = hay[-4096:]
    return want


def discover(root, max_depth=4):
    """`root` 아래에서 payload 배치를 찾는다 — **이름이 아니라 내용으로**.

    ⚠⚠ 초판은 `phaseA_h*_*` 이름 글롭이었다.  2026-09-20 실측으로 두 군데서 틀렸다:
      ⓐ **너무 좁다** — 재실행이 다른 이름/자리에 쓰면 못 찾고, 찾은 것이 하필
         **옛 깨진 배치**(`phaseA_h*_20260914`)라 "이탈" 을 보고했다.  사람이 그것을
         재실행 결과로 읽으면 정확히 거꾸로 판단한다.
      ⓑ **너무 넓다** — `phaseA_h015_20260914.log` 같은 **파일**까지 집어
         "디렉터리가 없다" 를 세 번 찍었다.
    ⇒ 배치의 정의는 이름이 아니라 **`run_receipt.json` 을 가진 디렉터리**다.
    ★ 배치를 찾으면 그 아래로는 더 내려가지 않는다 (팔 하위 디렉터리를 배치로 오인 금지).
    """
    root = os.path.expanduser(root)
    if not os.path.isdir(root):
        return []
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == '.' else rel.count(os.sep) + 1
        if 'run_receipt.json' in filenames:
            hits.append(dirpath)
            dirnames[:] = []                      # 배치 안으로는 안 들어간다
            continue
        if depth >= max_depth:
            dirnames[:] = []
    return sorted(hits)


def check_dir(d, seal):
    """디렉터리 하나 → 결과 dict.  ⚠ 없는 것은 **통과가 아니다**."""
    out = dict(dir=d, problems=[], n_arms=0, receipt_sha=None,
               ptfe=None, lean=None, sample=None, sample_sha=None, when='—')
    rp = os.path.join(d, 'run_receipt.json')
    if not os.path.isdir(d):
        out['problems'].append('디렉터리가 없다')
        return out
    if not os.path.exists(rp):
        out['problems'].append('run_receipt.json 이 없다 — 봉인을 확인할 수 없다')
        return out
    try:
        r = json.load(open(rp, encoding='utf-8'))
    except Exception as e:                                   # noqa: BLE001
        out['problems'].append(f'영수증을 읽을 수 없다: {e}')
        return out
    #  ① 봉인 축 (어댑터의 SEAL 을 그대로 쓴다)
    for k, v in seal.items():
        got = r.get(k)
        if k == 'ptfe_stamp':
            out['ptfe'] = got
        if got != v:
            out['problems'].append(f'봉인 이탈 {k}={got!r} (봉인 {v!r})')
    #  ③ code_sha
    out['receipt_sha'] = r.get('code_sha')
    if not out['receipt_sha']:
        out['problems'].append('영수증에 code_sha 가 없다 (CL-75 = 인용 금지)')
    #  origins
    org = r.get('origins')
    if not isinstance(org, list) or not org:
        out['problems'].append('영수증에 origins 배열이 없다')
    else:
        out['n_origins'] = len(org)
    #  팔 개수
    arms = sorted(glob.glob(os.path.join(d, 'p2_*_a*.json')))
    out['n_arms'] = len(arms)
    if not arms:
        out['problems'].append('팔 payload 가 하나도 없다')
        return out
    #  ★ 배치가 **언제** 돌았나 — 2026-09-20 에 옛 배치(09-14)를 재실행으로 읽을 뻔했다.
    #    이름은 믿지 않는다 (재실행이 옛 이름을 쓸 수도, 새 이름을 쓸 수도 있다).
    try:
        import datetime as _dt
        _t = max(os.path.getmtime(x) for x in arms)
        out['when'] = _dt.datetime.fromtimestamp(_t).strftime('%m-%d %H:%M')
    except Exception:                                        # noqa: BLE001
        pass
    #  ② LEAN = 2 — 표본 1팔 (전수는 어댑터가 본다)
    out['sample'] = os.path.basename(arms[0])
    got = scan_payload(arms[0])
    cp_raw = got.get('component_plan')
    if cp_raw is None:
        out['problems'].append(f'표본 팔에 component_plan 이 없다 ({out["sample"]})')
    else:
        try:
            cp = json.loads(cp_raw)
        except Exception:                                    # noqa: BLE001
            out['problems'].append(f'component_plan 을 파싱할 수 없다: {cp_raw[:80]}')
        else:
            out['lean'] = cp
            off = [k for k, v in LEAN2_PLAN.items() if bool(cp.get(k)) != v]
            if off:
                out['problems'].append(
                    'LEAN=2 가 아니다 — ' + ', '.join(f'{k}={cp.get(k)}' for k in off))
    sha_raw = got.get('code_sha')
    if sha_raw is not None and sha_raw != 'null':
        out['sample_sha'] = sha_raw.strip('"')
    if not out['sample_sha']:
        out['problems'].append(f'표본 팔에 code_sha 가 없다 ({out["sample"]})')
    return out


def report(rows, expect_arms=32):
    seal_ok = True
    print(f'{"디렉터리":36s} {"팔":>4s} {"마지막팔":>12s} {"ptfe_stamp":>11s} '
          f'{"LEAN2":>6s} {"code_sha":>11s}')
    for m in rows:
        lean = '—' if m['lean'] is None else ('✓' if not any(
            bool(m['lean'].get(k)) != v for k, v in LEAN2_PLAN.items()) else '⛔')
        sha = (m['receipt_sha'] or '—')
        print(f'{os.path.basename(m["dir"])[:36]:36s} {m["n_arms"]:4d} '
              f'{m["when"]:>12s} {str(m["ptfe"]):>11s} {lean:>6s} {str(sha)[:11]:>11s}')
        for p in m['problems']:
            print(f'    ⛔ {p}')
            seal_ok = False
        if m['n_arms'] and m['n_arms'] != expect_arms:
            print(f'    ⚠ 팔이 {m["n_arms"]} 개 — 기대 {expect_arms}')
    print()
    if not rows:
        print('⛔ 볼 디렉터리가 없다 — `--pa` 경로나 `--dir` 을 확인할 것')
        return 1
    if seal_ok:
        print('✓ 봉인 3축 통과 (영수증 + 표본 1팔) — **어댑터로 넘어가도 된다**')
        print('  ⚠ 이것은 전수 검사가 아니다.  origin 색인·수렴 표지·조성 교차확인은')
        print('    `phase_a_arms_from_payload.py` 가 한다 — 그쪽이 정본 게이트다.')
        return 0
    print('⛔ 봉인 이탈이 있다 — 어댑터를 돌릴 필요가 없다.')
    print('  정본: docs/reviews/phase_a_6mah_order_prereg_20260907.md §5')
    print('       docs/reviews/phase_a_seal_breach_20260918.md')
    return 1


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    seal = _adapter().SEAL
    chk('① 봉인 축을 어댑터에서 가져온다 (두 벌을 만들지 않는다)',
        seal.get('ptfe_stamp') == 'centerline' and 'fibre_stamp' in seal)

    def mk(td, ptfe='centerline', sha='be0ae9568', plan=None, n=2, arm_sha='be0ae9568'):
        os.makedirs(td, exist_ok=True)
        rc = {'origins': [[0, 0, 0], [1, 0, 0]], 'code_sha': sha,
              'fibre_stamp': 'segment', 'ptfe_stamp': ptfe, 'bridge_um': 0.24}
        if sha is None:
            rc.pop('code_sha')
        json.dump(rc, open(os.path.join(td, 'run_receipt.json'), 'w'))
        plan = LEAN2_PLAN if plan is None else plan
        for i in range(n):
            body = {'pad': 'x' * 3000, 'mpm_metrics': {'step3': {'manifest': {
                'component_plan': plan, 'code_sha': arm_sha}}}}
            json.dump(body, open(os.path.join(td, f'p2_K_a{i}.json'), 'w'))
        return td

    with tempfile.TemporaryDirectory() as t:
        good = mk(os.path.join(t, 'ok'))
        m = check_dir(good, seal)
        chk('② 정상 배치는 문제 0', not m['problems'] and m['n_arms'] == 2)
        chk('②b 표본에서 LEAN=2 를 읽는다', m['lean'] == LEAN2_PLAN)

        #  ★ ① 재현 — 2026-09-18 의 ptfe_stamp=off
        bad = mk(os.path.join(t, 'ptfe'), ptfe='off')
        chk('③ ptfe_stamp=off 를 잡는다 (2026-09-18 재현)',
            any('ptfe_stamp' in p for p in check_dir(bad, seal)['problems']))

        #  ★ ② 재현 — LEAN 미적용 (6 성분)
        full = mk(os.path.join(t, 'lean'),
                  plan={'electronic': True, 'ionic': True, 'thermal': True,
                        'pore': True, 'collector': True})
        chk('④ LEAN=2 미적용을 잡는다 (2026-09-18 재현)',
            any('LEAN=2' in p for p in check_dir(full, seal)['problems']))

        #  ★ ③ 재현 — code_sha 전 계층 null
        nosha = mk(os.path.join(t, 'sha'), sha=None, arm_sha=None)
        pr = check_dir(nosha, seal)['problems']
        chk('⑤ code_sha 부재를 잡는다 — 영수증과 팔 **둘 다** (2026-09-18 재현)',
            sum('code_sha' in p for p in pr) == 2)

        #  ★ 변이 — 없는 것은 통과가 아니다
        empty = os.path.join(t, 'empty'); os.makedirs(empty)
        chk('⑥ 변이: 영수증이 없으면 **거부** (없는 것은 통과가 아니다)',
            bool(check_dir(empty, seal)['problems']))
        chk('⑥b 변이: 디렉터리 자체가 없으면 거부',
            bool(check_dir(os.path.join(t, '없다'), seal)['problems']))
        noarm = os.path.join(t, 'noarm')
        mk(noarm, n=0)
        chk('⑥c 변이: 팔이 0 개면 거부',
            any('하나도 없다' in p for p in check_dir(noarm, seal)['problems']))

        #  ★ 청크 경계 — 겹쳐 읽지 않으면 놓친다
        big = os.path.join(t, 'big'); os.makedirs(big)
        json.dump({'origins': [[0, 0, 0]], 'code_sha': 'abc', 'fibre_stamp': 'segment',
                   'ptfe_stamp': 'centerline', 'bridge_um': 0.24},
                  open(os.path.join(big, 'run_receipt.json'), 'w'))
        pad = 'y' * (_CHUNK + 512)
        with open(os.path.join(big, 'p2_K_a0.json'), 'w') as fh:
            fh.write('{"pad": "' + pad + '", "component_plan": '
                     + json.dumps(LEAN2_PLAN) + ', "code_sha": "abc"}')
        chk('⑦ 1 MB 청크 경계 너머의 component_plan 도 읽는다',
            check_dir(big, seal)['lean'] == LEAN2_PLAN)

        #  ★★ ⑧ 탐색 — **이름이 아니라 내용으로** (2026-09-20 실측 재현)
        #     초판 이름 글롭은 ⓐ 재실행 배치를 못 찾고 하필 **옛 깨진 배치**를 집었고
        #     ⓑ `*.log` **파일**까지 집어 "디렉터리가 없다" 를 찍었다.
        root = os.path.join(t, 'root')
        mk(os.path.join(root, 'phaseA_h015_20260914'))          # 옛 이름
        mk(os.path.join(root, '재실행', 'h015_rerun'))            # 다른 이름·한 단계 깊이
        open(os.path.join(root, 'phaseA_h015_20260914.log'), 'w').write('x')
        os.makedirs(os.path.join(root, 'empty_dir'), exist_ok=True)
        got = discover(root)
        chk(f'⑧ 이름이 달라도 배치를 찾는다 ({len(got)} 개)', len(got) == 2)
        chk('⑧b 변이: `.log` **파일**은 배치가 아니다',
            not any(g.endswith('.log') for g in got))
        chk('⑧c 변이: 영수증 없는 디렉터리는 배치가 아니다',
            not any(g.endswith('empty_dir') for g in got))
        #  배치 안에 또 배치처럼 보이는 것이 있어도 내려가지 않는다
        inner = os.path.join(root, 'phaseA_h015_20260914', 'sub')
        mk(inner)
        chk('⑧d 배치를 찾으면 그 아래로 안 내려간다 (팔 하위를 배치로 오인 금지)',
            inner not in discover(root))
        chk('⑧e 없는 뿌리는 빈 목록 (죽지 않는다)', discover(os.path.join(t, '없다')) == [])

    print(f'\nphase_a_preflight selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pa', default='',
                    help='~/pa 같은 상위 경로 — `run_receipt.json` 을 가진 배치를 '
                         '**내용으로** 찾는다 (이름 글롭이 아니다)')
    ap.add_argument('--dir', action='append', default=[], help='payload 디렉터리 (여러 번)')
    ap.add_argument('--expect-arms', type=int, default=32)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    dirs = [d for d in a.dir]
    if a.pa:
        found = discover(a.pa)
        if not found:
            print(f'⛔ {a.pa} 아래에서 `run_receipt.json` 을 가진 배치를 못 찾았다.')
            print('   재실행 산출물이 다른 자리에 있으면 `--dir <경로>` 로 직접 줄 것.')
            raise SystemExit(1)
        print(f'탐색 {os.path.expanduser(a.pa)} → 배치 {len(found)} 개 '
              f'(`run_receipt.json` 보유 기준)\n')
        dirs += found
    if not dirs:
        ap.error('--pa 나 --dir 중 하나는 필요하다')
    dirs = [d for d in dict.fromkeys(dirs) if os.path.isdir(d) or True]
    seal = _adapter().SEAL
    raise SystemExit(report([check_dir(d, seal) for d in dirs],
                            expect_arms=a.expect_arms))
