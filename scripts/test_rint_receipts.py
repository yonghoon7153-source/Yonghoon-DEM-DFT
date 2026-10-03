#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""① 계면 저항 **요청 ↔ 적용 영수증** 통합 시험 — Codex r_int 1단계 `RINT-02` · `13` · `14` · `20` (10-03 · 1저자 비준 G1).

Codex 변이 탐침: 실제 producer 에서 **주 전자 솔브의 `rint=` 만** 지우면 σ_e 는 OFF 와 비트 동일인데 CLI 기록
(model = r1) 은 남아 규칙 J 사후 단언이 PASS 했다.  wetted 호출만 지우면 주 σ · 면 · 표는 그대로라 "주 솔브 ON
시험" 도 통과하는데 wetted σ 0.0009487 → 0.0009606 · R_geom 0 → 0.0544 Ω·cm² 로 바뀐다.  ⇒ 네 솔브 각각의
**실제 적용 영수증**을 독립 보존한 요청 표에 대조하고 (`run_contract.interface_record_ok`), 그 계약을 producer
(발행 전) · `check_arm` · 최종 판정기가 같이 쓴다.  이 시험은 그 배선이 **실물에서** 무는지 본다.

  A  실물 producer — OFF · 전자 ON (집전체 포함) · 이온 ON 이 exit 0 · 계약 통과 · 영수증 상태가 기대대로
  B  AST 변이 — `solve_sigma_z(..., rint=...)` 호출 넷을 AST 로 찾아 **하나씩** `rint=` 를 지우면 producer 가
     게시를 거부한다 (exit 4 · `.failed` · 사유 `STEP3_INTERFACE` 에 그 솔브 이름)
  C  CLI 모순 요청 — 빈 `--step3-rint-e` · 반복 플래그 사이의 같은 쌍 · `--step3-rint-i` + `--no-ion` ·
     `--no-step3` · 이 채널 σ 에서 절연인 상 (`AM_S|SE` 전자) 은 GPU 작업 전에 죽는다
  D  소비자 — 정상 ON 산출물의 영수증을 하나씩 변조하면 `check_arm` 이 거부한다 (원본은 받아들인다)
  E  레지스트리 (RINT-20) — 실물 producer 매니페스트 키가 판정기 레지스트리에 **전부** 분류돼 있다
     (`manifest_unswept_keys` = 빈 목록) · OFF ↔ ON 비교에서 `interface_model` 은 표의 파생이라 HOLD 사유가 아니다

  python3 scripts/test_rint_receipts.py
"""
import ast
import copy
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
PAY = os.path.join(SCRIPTS, 'mpm_webapp_payload.py')
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


def rint_call_sites(src):
    """payload 소스 → `[(대입 대상 이름, 줄)]` — `solve_sigma_z(..., rint=...)` 호출 전수 (AST)."""
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            c = node.value
            f = c.func
            if isinstance(f, ast.Attribute) and f.attr == 'solve_sigma_z' \
                    and any(k.arg == 'rint' for k in c.keywords):
                tgt = node.targets[0]
                out.append((tgt.id if isinstance(tgt, ast.Name) else ast.dump(tgt), c.lineno))
    return sorted(out, key=lambda x: x[1])


def mutant_child(target):
    """`target` 에 대입하는 solve_sigma_z 호출 하나에서만 `rint=` 키워드를 지우고 producer 를 돈다."""
    import mpm_webapp_payload as payload
    with open(PAY, encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=PAY)
    hit = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == target:
            c = node.value
            if isinstance(c.func, ast.Attribute) and c.func.attr == 'solve_sigma_z':
                n0 = len(c.keywords)
                c.keywords = [k for k in c.keywords if k.arg != 'rint']
                hit += (n0 - len(c.keywords))
    assert hit == 1, f'변이 대상 {target} 의 rint 키워드가 정확히 하나가 아니다 ({hit})'
    exec(compile(tree, PAY, 'exec'), payload.__dict__)
    payload.main()


def run_payload(args, cwd, mutant=None, timeout=900):
    if mutant:
        cmd = [sys.executable, os.path.abspath(__file__), '--mutant-child', mutant, '--', *args]
    else:
        cmd = [sys.executable, PAY, *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                       stdin=subprocess.DEVNULL)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def load_manifest(path):
    with open(path, encoding='utf-8') as f:
        p = json.load(f)
    s3 = (p.get('mpm_metrics') or {}).get('step3') or {}
    return p, s3, (s3.get('manifest') or {})


def main():
    import check_method_discipline as cmd_
    import run_contract as RC
    import sdcp_gain_verdict as SGV
    with open(PAY, encoding='utf-8') as f:
        src = f.read()
    sites = rint_call_sites(src)
    names = [s[0] for s in sites]
    print('A0 호출 자리 (AST):', sites)
    chk('A0 rint 를 받는 solve_sigma_z 호출이 정확히 넷 (주 · wetted · bare · 이온)',
        names == ['_res3', '_res3w', '_res3b', '_res3i'], repr(names))

    with tempfile.TemporaryDirectory() as d:
        am, se, ph, fid, dia = cmd_._smoke_fixture(d)
        base = ['--scaffold', am, '--se', se, '--phase', ph, '--fibre', fid, '--fibre-dia', dia,
                '--n-vox', cmd_._SMOKE_NVOX, '--step3-vox', cmd_._SMOKE_VOX,
                '--no-pore', '--no-thermal', '--no-trackb', '--no-field', '--no-step4']
        e_on = ['--step3-rint-e', 'AM_S|AM_S=0.001', 'AM_S|VGCF=0.002']
        i_on = ['--step3-rint-i', 'SDCP|SE=0.001']
        runs = {
            'off':   base + ['--no-ion'],
            'e_on':  base + ['--no-ion'] + e_on,
            'ei_on': base + e_on + i_on,
        }
        res = {}
        print('A  실물 producer (OFF · 전자 ON · 전자+이온 ON)')
        for k, args in runs.items():
            out = os.path.join(d, f'{k}.json')
            rc, log = run_payload(args + ['--out', out], d)
            res[k] = (rc, log, out)
            if not chk(f'A1 {k}: exit 0 · 산출물 있음', rc == 0 and os.path.exists(out),
                       f'rc={rc} {log.strip()[-300:]}'):
                continue
            _, s3, man = load_manifest(out)
            ok, why = RC.interface_record_ok(man)
            chk(f'A2 {k}: 계면 계약 통과', ok, why)
            rcpt = man.get('interface_receipts') or {}
            chk(f'A3 {k}: 네 솔브 영수증', sorted(rcpt) == sorted(RC.INTERFACE_SOLVES), repr(sorted(rcpt)))
            st = {n: (rcpt.get(n) or {}).get('status') for n in RC.INTERFACE_SOLVES}
            if k == 'off':
                chk('A4 off: 전부 not_requested · model None',
                    set(st.values()) == {'not_requested'} and man.get('interface_model') is None, repr(st))
            elif k == 'e_on':
                chk('A4 e_on: 주 · wetted · bare = applied (면 > 0) · 이온 = not_requested',
                    st['electronic_main'] == st['electronic_wetted'] == st['electronic_bare'] == 'applied'
                    and st['ionic'] == 'not_requested', repr(st))
            else:
                chk('A4 ei_on: 이온 영수증이 요청 표를 받았다 (applied · absent_geometry · failed 중 하나)',
                    st['ionic'] in ('applied', 'absent_geometry', 'failed')
                    and (rcpt['ionic'].get('table') == man.get('interface_rint_i_ohm_cm2')), repr(rcpt.get('ionic')))
            print(f'      {k}: σ_e={s3.get("sigma_e_eff_S_cm")} 영수증 {st}')

        print('B  AST 변이 — 호출 하나씩 rint= 삭제 → 게시 거부')
        _mut_args = {'_res3': runs['e_on'], '_res3w': runs['e_on'], '_res3b': runs['e_on'], '_res3i': runs['ei_on']}
        _mut_name = {'_res3': 'electronic_main', '_res3w': 'electronic_wetted',
                     '_res3b': 'electronic_bare', '_res3i': 'ionic'}
        for tgt in names:
            out = os.path.join(d, f'mut{tgt}.json')
            rc, log = run_payload(_mut_args[tgt] + ['--out', out], d, mutant=tgt)
            chk(f'B1 변이 {tgt}: exit 4 · 최종 파일 없음 · .failed 있음',
                rc == 4 and not os.path.exists(out) and os.path.exists(out + '.failed'),
                f'rc={rc} {log.strip()[-240:]}')
            chk(f'B2 변이 {tgt}: 사유 STEP3_INTERFACE · {_mut_name[tgt]}',
                'STEP3_INTERFACE' in log and _mut_name[tgt] in log, log.strip()[-240:])

        print('C  CLI 모순 요청 — GPU 작업 전에 죽는다')
        bad = {
            '빈 --step3-rint-e': base + ['--no-ion', '--step3-rint-e'],
            '반복 플래그 사이 같은 쌍': base + ['--no-ion', '--step3-rint-e', 'AM_S|VGCF=1e-3',
                                      '--step3-rint-e', 'VGCF|AM_S=2e-3'],
            '--step3-rint-i + --no-ion': base + ['--no-ion'] + i_on,
            '--no-step3': base + ['--no-ion', '--no-step3'] + e_on,
            '절연 상 쌍 (AM_S|SE 전자)': base + ['--no-ion', '--step3-rint-e', 'AM_S|SE=1e-3'],
            '절연 상 쌍 (AM_S|SE 이온)': base + ['--step3-rint-i', 'AM_S|SE=1e-3'],
        }
        for lbl, args in bad.items():
            out = os.path.join(d, 'bad.json')
            rc, log = run_payload(args + ['--out', out], d, timeout=300)
            #  'STEP3: voxelizing' = 격자 작업의 첫 표지 — 그 전에 죽어야 GPU · 시간을 안 쓴다
            chk(f'C1 {lbl}: 거부 (exit ≠ 0 · 산출물 없음 · 격자 작업 전)',
                rc != 0 and not os.path.exists(out) and 'STEP3: voxelizing' not in log,
                f'rc={rc} {log.strip()[-200:]}')

        print('D  소비자 — 영수증 변조를 check_arm 이 거부한다')
        good = res.get('e_on', (1, '', ''))[2]
        if os.path.exists(good):
            chk_arm = os.path.join(SCRIPTS, 'sr01_stamp_compare.py')

            _stamp = (load_manifest(good)[2].get('fibre_stamp') or 'point')   # 실물 도장 그대로 (손으로 적지 않는다)

            def arm_rc(path):
                r = subprocess.run([sys.executable, chk_arm, '--check-arm', path, '--stamp', _stamp],
                                   capture_output=True, text=True, timeout=300, cwd=d, stdin=subprocess.DEVNULL)
                return r.returncode, (r.stdout or '') + (r.stderr or '')
            rc0, log0 = arm_rc(good)
            chk('D0 원본 ON 산출물은 check_arm 이 받아들인다', rc0 == 0, log0.strip()[-200:])
            p0, _, _ = load_manifest(good)

            def tamper(fn, lbl):
                p = copy.deepcopy(p0)
                fn(p['mpm_metrics']['step3']['manifest'])
                t = os.path.join(d, 'tamper.json')
                with open(t, 'w', encoding='utf-8') as f:
                    json.dump(p, f)
                rc, log = arm_rc(t)
                chk(f'D1 {lbl}: check_arm 거부', rc != 0 and 'IFACE' in log, f'rc={rc} {log.strip()[-200:]}')
            tamper(lambda m: m['interface_receipts'].__setitem__('electronic_wetted', {'status': 'not_requested'}),
                   'wetted 영수증을 not_requested 로')
            tamper(lambda m: m['interface_receipts']['electronic_bare'].__setitem__('table', {'AM_S|AM_S': 0.001}),
                   'bare 영수증 표를 요청과 다르게')
            tamper(lambda m: m.__setitem__('interface_model', None), 'model 을 None 으로 (표는 그대로)')
            tamper(lambda m: m.pop('interface_receipts'), '영수증 통째로 삭제')
            tamper(lambda m: m['interface_receipts']['electronic_main'].__setitem__('n_faces_rint', 0),
                   '주 영수증 면 수를 0 으로 (쌍별 합과 모순)')
        else:
            chk('D0 e_on 산출물이 있어야 소비자 시험을 돈다', False)

        print('E  레지스트리 — 실물 매니페스트 키 전수 분류 (RINT-20) · 파생 model (RINT-13)')
        for k in ('off', 'e_on', 'ei_on'):
            out = res.get(k, (1, '', ''))[2]
            if out and os.path.exists(out):
                _, _, man = load_manifest(out)
                left = SGV.manifest_unswept_keys(man, man)
                chk(f'E1 {k}: 분류 안 된 매니페스트 키 없음', left == [], repr(left))
        fc = SGV.FIELD_CONTRACT.get('interface_model') or {}
        chk('E2 interface_model 은 계면 표 두 축의 파생 (derived_from)',
            tuple(fc.get('derived_from') or ()) == ('interface_rint_e_ohm_cm2', 'interface_rint_i_ohm_cm2'),
            repr(fc))

    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    if '--mutant-child' in sys.argv:
        i = sys.argv.index('--mutant-child')
        target = sys.argv[i + 1]
        j = sys.argv.index('--')
        sys.argv = [PAY] + sys.argv[j + 1:]
        mutant_child(target)
        raise SystemExit(0)
    main()
