#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q2 (1저자 11-12) — 탄소 접합 원장 저장본 끝-끝: 사슬 (실제 러너 · 실제 payload · 아주 작은 픽스처 킷 · CPU) 에서 저장본 끔 / 켬 결과가
같은가 · 시험 먼저 (고치기 전 = 사슬이 `--cjunc-store` 를 모른다).

틀 = `scripts/test_rint_r_chain_e2e.py` (E18 꼴 · import · 사본 없음): 원장 시도 사다리 P0 · P1 → 예측 (한 기계) → 원장 판정 → 다시 판정 + 사다리 뒤 갈라
낸 원장 사본에서 예측 단위 하나 (`--unit`).  같은 바탕 (킷 · 계획 · 등록 · 코드 체크아웃) 에서 두 번 — 끔 · 켬 (`--cjunc-store <새 폴더>`) — 돌리고
견준다.  그 뒤 켬 폴더 그대로 사다리 P0 을 한 번 더 (원장 없이) = 전부 적중.

  Z1  두 길 다 rc 0 · 사다리 CALIBRATED · 예측 PREDICTED · 판정 이름 (멈춤 아님) · 다시 판정 REVERIFY_SAME · 단위 시도 rc 0
  Z2  팔 JSON 바이트 (요약 arms_read sha256 = 파일 독립 계산) — 사다리 둘 · 예측 · 단위의 모든 런 · 모든 팔이 끔 = 켬
  Z3  판정 공개 칸 (이름 · 상태 · 표지 · 막는 표지 · 문장 · 보정) 같음 · 판정 결과 JSON 바이트 같음 · 사다리 · 예측 요약의 결과 칸 같음
  Z4  봉인 원천 (판정 · 예측의 RunnerGraphSource 조립만 런) 은 저장본을 받지 않는다 — 조립만 payload 인자에 `--step3-cjunc-store` 없음 · 켬 길의
      생산 payload 인자에는 늘 있음 · 예측 · 판정의 원천 런 상태 ok · 판정 표지에 SV_UNCHECKED 없음 (저장본으로 지은 팔의 그래프 = 저장본 없이
      다시 조립한 그래프 — 요약의 팔 공개 칸 ARM_PUBLIC 에는 sv_graph 가 없어 판정 표지로 본다)
  Z5  저장본 폴더 — 켬 길 뒤 파일 ≥ 2 (SBE · DBE 열쇠) · 이름 · 0444 · 임시 파일 없음 · 켬 길 화면 = 지어 씀 / 적중 줄 · 끔 길 = 저장본 줄 없음 ·
      요약 cjunc_store True (끔 = 칸 없음)
  Z6  적중 런 (켬 폴더 · 사다리 P0 · 원장 없이) — 모든 payload = 적중 줄 · 새 파일 없음 · 팔 JSON 바이트 = 끔 길 사다리 P0
  Z5b · Z6b (★ 11-13 RCP-07) 요약 팔별 저장본 상태 `cjunc_store_arms` (런마다 팔마다 상태 · 열쇠 · 저장본 파일 · 파일 sha256 · 기록만) — 켬 = 단계 넷 ·
      적중 런 = 모두 hit · 끔 = 칸 없음
⚠ PASS = 저장본이 생산 사슬 (S0 보고 · 사다리 · 예측 · 단위 · 판정 · 다시 판정) 의 산출 바이트를 바꾸지 않는다는 증거 (픽스처 · CPU) — GPU 길 · 실침대
   (원장 크기 · 읽기 시간) 은 보지 않는다.  합치기 (`--merge`) 는 단위 열두 개가 있어야 해 여기서 돌리지 않는다 — 합치기는 팔 JSON · 요약만 읽으므로
   Z2 의 바이트 같음이 그 입력을 덮는다 (한정).

  python3 scripts/test_cjunc_store_e2e.py            # 전부 (실제 러너 수십 회 · 십수 분)
  python3 scripts/test_cjunc_store_e2e.py --keep
"""
import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
import run_contract as _RCG                                # noqa: E402 — ★ 11-12 2 회차 (재리뷰 RCP2-06) 이 시험 프로세스와 그 자식 (git · payload ·
_RCG.drop_git_env()                                        #   러너) 은 부르는 쪽 환경의 GIT_* 를 물려받지 않는다 (scripts/test_git_env_isolation.py G6)

import test_rint_r_chain_e2e as E                           # noqa: E402 — 끝-끝 틀 (픽스처 · 고정물 체크아웃 · 사슬 부르기) · 사본 없음

RR, TR = E.RR, E.TR
TD = None
_ok, _fail = 0, []
UNIT = RR.unit_name(RR.CS[0], RR.LAWS[0], RR.RJ_ROLES[0])  # 계획 §4-2 표의 첫 단위 (e2e12 UNIT_TABLE[0])


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:900]})' if why != '' else ''))
    return cond


def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def jload(p):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def arm_map(folder, s, tag):
    """요약 런 → {(단계, 런 이름, 팔 파일): (요약 sha256, 파일 독립 sha256)}."""
    out = {}
    for r in (s or {}).get('runs') or []:
        for a in r.get('arms_read') or []:
            p = os.path.join(folder, r['outdir'], a['file'])
            out[(tag, r.get('name'), a['file'])] = (a.get('sha256'), sha(p) if os.path.isfile(p) else None)
    return out


def shim_argv(ws):
    """가짜 python3 가 남긴 payload argv (파일 이름 → 토큰 목록)."""
    out = {}
    for f in glob.glob(os.path.join(ws, '_shim', 'payload_argv.*')):
        toks = open(f, 'rb').read().decode('utf-8', 'replace').split('\0')
        out[f] = toks[:-1] if toks and toks[-1] == '' else toks
    return out


def store_lines(paths):
    lines = []
    for p in paths:
        try:
            lines += [ln for ln in open(p, encoding='utf-8', errors='replace').read().splitlines() if '원장 저장본' in ln]
        except OSError:
            pass
    return lines


def flow(tag, W, store):
    """원장 시도 길 하나 (끔: store None) → 결과 dict."""
    ws, sd, runner, pp, sp, rp = W['ws'], W['sd'], W['runner'], W['pp'], W['sp'], W['rp']
    xs = ['--cjunc-store', store] if store else []
    led = os.path.join(TD, f'ledger_{tag}')
    os.makedirs(led)
    subprocess.run(['git', 'init', '-q', led], check=True, capture_output=True, env=_RCG.git_fixture_env())   # ★ 3 회차 (RCP3-04)
    rcs, sos = [], []

    def call(argv):
        rc_, so_ = E.e2e_call(ws, sd, argv)
        rcs.append(rc_)
        sos.append(so_)
        return rc_, so_

    def add(target, lg):
        _rc, so_ = call(['--stage', 'ledger', '--ledger', lg, '--add', '--ledger-target', target, '--machine', E.E2E_MACH, '--plan', pp,
                         '--runner', runner, '--root', ws])
        m = re.search(r'ATTEMPT_ADDED n=(\d+)', so_)
        return int(m.group(1)) if m else None
    call(['--stage', 'ledger', '--ledger', led, '--init', '--plan', pp])
    before = set(shim_argv(ws))
    dirs, sums = {}, {}
    for law in ('P0', 'P1'):
        n = add(f'ladder:{law}', led)
        base = os.path.join(TD, 'runs', tag, f'lad_{law}')
        call(['--stage', 'ladder', '--law', law, '--target', str(RR.TARGET_SBE_MS), '--runner', runner, '--root', ws, '--plan', pp,
              '--s0-plan', sp, '--registration', rp, '--max-hours', E.E2E_MAXH, '--out', base, '--machine', E.E2E_MACH] + E.s0_args()
             + ['--ledger', led, '--attempt', str(n)] + xs)
        dirs[law] = os.path.join(base, f'attempt_{n}')
        sums[law] = jload(os.path.join(dirs[law], 'ladder_summary.json')) or {}
    led_u = led + '_u'                                       # 단위 길 = 사다리 뒤 갈라 낸 원장 사본 (원장 하나 = 경로 하나 · e2e12 D2)
    shutil.copytree(led, led_u)
    n = add('predict', led)
    pbase = os.path.join(TD, 'runs', tag, 'pred')
    call(['--stage', 'predict', '--ladders', dirs['P0'], dirs['P1'], '--runner', runner, '--root', ws, '--registration', rp,
          '--max-hours', E.E2E_MAXH, '--out', pbase, '--machine', E.E2E_MACH, '--ledger', led, '--attempt', str(n)] + xs)
    dirs['pred'] = os.path.join(pbase, f'attempt_{n}')
    sums['pred'] = jload(os.path.join(dirs['pred'], 'predict_summary.json')) or {}
    nu = add(f'unit:{UNIT}', led_u)
    ubase = os.path.join(TD, 'runs', tag, 'units')
    call(['--stage', 'predict', '--ladders', dirs['P0'], dirs['P1'], '--runner', runner, '--root', ws, '--registration', rp,
          '--max-hours', E.E2E_MAXH, '--out', ubase, '--machine', E.E2E_MACH, '--ledger', led_u, '--attempt', str(nu), '--unit', UNIT] + xs)
    dirs['unit'] = os.path.join(ubase, f'attempt_{nu}')
    sums['unit'] = jload(os.path.join(dirs['unit'], RR.UNIT_SUMMARY['unit'])) or {}
    vdir = os.path.join(TD, 'runs', tag, 'verdict')
    rcv, sov = call(['--stage', 'verdict', '--runs', dirs['P0'], dirs['P1'], dirs['pred'], '--root', ws, '--registration', rp,
                     '--ledger', led, '--out', vdir])
    rvdir = os.path.join(TD, 'runs', tag, 'reverify')
    rcr, sor = call(['--stage', 'verdict', '--reverify', vdir, '--root', ws, '--out', rvdir])
    argv_new = {k: v for k, v in shim_argv(ws).items() if k not in before}
    logs = sorted(glob.glob(os.path.join(TD, 'runs', tag, '**', 'logs', '*.log'), recursive=True))
    return {'rcs': rcs, 'so': sos, 'dirs': dirs, 'sums': sums, 'vdir': vdir, 'rvdir': rvdir, 'rcv': rcv, 'rcr': rcr, 'sov': sov, 'sor': sor,
            'argv': argv_new, 'logs': logs}


def main():
    global TD
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='cjunc_store_e2e_')
    E.TD = TD
    TR.TD = os.path.join(TD, 'tr')
    os.makedirs(TR.TD)
    TR.SHIMDIR = os.path.join(TR.TD, '_bin')
    os.makedirs(TR.SHIMDIR)
    with open(os.path.join(TR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(TR.SHIM.replace('__REAL__', os.path.abspath(sys.executable)))
    os.chmod(os.path.join(TR.SHIMDIR, 'python3'), 0o755)
    t0 = time.time()
    try:
        run_all()
    except Exception as e:                                   # noqa: BLE001 — 시험 안의 예외 = 실패
        import traceback
        chk('예외 없이', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:300]}')
    finally:
        if a.keep:
            print(f'  (임시 폴더 남김: {TD})')
        else:
            for r, ds, fs in os.walk(TD):
                for x in fs:
                    q = os.path.join(r, x)
                    if not os.path.islink(q):
                        try:
                            os.chmod(q, 0o644)
                        except OSError:
                            pass
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_cjunc_store_e2e: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    for n in _fail:
        print(f'  - {n}')
    return 0 if not _fail else 1


def run_all():
    if '--cjunc-store' not in RR.main.__code__.co_consts:
        chk('Z0 사슬에 --cjunc-store 가 있다 (ladder · predict)', False, '고치기 전 판 — 사슬이 저장본 선택지를 모른다 (끔 길도 돌리지 않는다)')
        return
    ws = E.make_root('zs')
    pp, sp, rp = E.make_plan_and_reg(ws)
    sd = E.code_repo()
    W = dict(ws=ws, sd=sd, runner=os.path.join(sd, 'sdcp_gain_vox015_8arm.sh'), pp=pp, sp=sp, rp=rp)
    store = os.path.join(TD, 'cjstore')
    os.makedirs(store)
    os.chmod(store, 0o755)
    t0 = time.time()
    off = flow('off', W, None)
    t1 = time.time()
    on = flow('on', W, store)
    t2 = time.time()
    files_on = sorted(os.listdir(store))
    print(f'    보고 — 끔 길 {t1 - t0:.0f} s · 켬 길 {t2 - t1:.0f} s · rc 끔 {off["rcs"]} · 켬 {on["rcs"]} · 저장본 파일 {len(files_on)}')
    ok_states = all(x['sums'][k].get('status') == 'CALIBRATED' for x in (off, on) for k in ('P0', 'P1')) \
        and all(x['sums']['pred'].get('status') == 'PREDICTED' for x in (off, on))
    vo, vn = jload(os.path.join(off['vdir'], 'verdict.json')) or {}, jload(os.path.join(on['vdir'], 'verdict.json')) or {}
    ro_, rn_ = jload(os.path.join(off['rvdir'], 'reverify_report.json')) or {}, jload(os.path.join(on['rvdir'], 'reverify_report.json')) or {}
    if not chk('Z1 두 길 (끔 · 켬) — rc 전부 0 · 사다리 CALIBRATED · 예측 PREDICTED · 판정 이름 (멈춤 아님) · 다시 판정 REVERIFY_SAME · 단위 시도 rc 0',
               all(r == 0 for r in off['rcs']) and all(r == 0 for r in on['rcs']) and ok_states
               and vo.get('verdict') not in (None, 'NOT_COMPUTED') and vn.get('verdict') not in (None, 'NOT_COMPUTED')
               and ro_.get('result') == 'REVERIFY_SAME' and rn_.get('result') == 'REVERIFY_SAME',
               (off['rcs'], on['rcs'], [off['sums'][k].get('status') for k in ('P0', 'P1', 'pred', 'unit')],
                [on['sums'][k].get('status') for k in ('P0', 'P1', 'pred', 'unit')], vo.get('verdict'), vn.get('verdict'),
                ro_.get('result'), rn_.get('result'), [s[-500:] for s in on['so'] if 'ABORT' in s or 'Stop' in s or 'rc' in s][:2])):
        return
    mo, mn = {}, {}
    for k in ('P0', 'P1', 'pred', 'unit'):
        mo.update(arm_map(off['dirs'][k], off['sums'][k], k))
        mn.update(arm_map(on['dirs'][k], on['sums'][k], k))
    self_ok = all(v[0] == v[1] for v in list(mo.values()) + list(mn.values()))
    diff = sorted(k for k in set(mo) | set(mn) if mo.get(k, (None,))[1] != mn.get(k, (None,))[1])
    n_unit = len([k for k in mo if k[0] == 'unit'])
    chk(f'Z2 팔 JSON 바이트 — 사다리 둘 · 예측 · 단위의 모든 팔 ({len(mo)} · 단위 {n_unit}) 이 끔 = 켬 · 요약 sha256 = 파일 독립 계산',
        mo and n_unit > 0 and set(mo) == set(mn) and not diff and self_ok, (len(mo), len(mn), diff[:5], self_ok))
    pub = ('verdict', 'state', 'flags', 'blocking_flags', 'sentence_allowed', 'calib')
    rbo = open(os.path.join(off['vdir'], 'verdict_results.json'), 'rb').read() if os.path.exists(os.path.join(off['vdir'], 'verdict_results.json')) else None
    rbn = open(os.path.join(on['vdir'], 'verdict_results.json'), 'rb').read() if os.path.exists(os.path.join(on['vdir'], 'verdict_results.json')) else None
    same_sum = all(off['sums'][k].get('ladder') == on['sums'][k].get('ladder') for k in ('P0', 'P1')) \
        and all(off['sums'][k].get(c) == on['sums'][k].get(c) for k in ('pred', 'unit') for c in ('status', 'checks', 'origin'))
    chk('Z3 판정 공개 칸 (이름 · 상태 · 표지 · 막는 표지 · 문장 · 보정) 같음 · 판정 결과 JSON 바이트 같음 · 사다리 결과 칸 · 예측 · 단위 (상태 · 검사 · '
        'origin) 같음', all(vo.get(k) == vn.get(k) for k in pub) and rbo is not None and rbo == rbn and same_sum,
        ([k for k in pub if vo.get(k) != vn.get(k)], rbo == rbn, same_sum))
    go = [t for t in on['argv'].values() if '--step3-cjunc-graph-only' in t]
    prod = [t for t in on['argv'].values() if '--step3-cjunc-graph-only' not in t and '--step3-cjunc' in t]
    gsrc = ((on['sums']['pred'].get('sv_graph_source') or {}).get('runs') or [])
    vg = ((jload(os.path.join(on['vdir'], 'verdict_graph_src.json')) or {}).get('runs') or [])
    chk('Z4 봉인 원천 (조립만 런) 은 저장본을 받지 않는다 — 켬 길의 조립만 payload 인자 (≥ 1) 에 --step3-cjunc-store 없음 · 생산 payload 인자 (≥ 1) '
        '에는 늘 있음 · 예측 · 판정의 원천 런 (≥ 1) 상태 ok · 판정 표지에 SV_UNCHECKED 없음 (저장본으로 지은 팔의 그래프 = 저장본 없이 다시 조립한 그래프)',
        go and prod and not any('--step3-cjunc-store' in t for t in go) and all('--step3-cjunc-store' in t for t in prod)
        and gsrc and all(g.get('status') == 'ok' for g in gsrc) and all(g.get('status') == 'ok' for g in vg)
        and 'SV_UNCHECKED' not in (vn.get('flags') or []),
        (len(go), len(prod), [g.get('status') for g in gsrc], [g.get('status') for g in vg], vn.get('flags')))
    lines_on = store_lines(on['logs'])
    lines_off = store_lines(off['logs'])
    gs_lines = store_lines([p for p in on['logs'] if os.sep + 'graph_src' + os.sep in p or os.path.basename(p).startswith('G')])
    modes = [oct(os.stat(os.path.join(store, f)).st_mode & 0o777) for f in files_on]
    chk('Z5 저장본 폴더 — 파일 ≥ 2 (SBE · DBE 열쇠) · 이름 cjreg_<64 hex>.npz · 0444 · 임시 파일 없음 · 켬 길 화면에 지어 씀 · 적중 줄 · 경고 줄 없음 · '
        '끔 길 · 조립만 런 = 저장본 줄 없음 · 요약 cjunc_store True (끔 = 칸 없음)',
        len(files_on) >= 2 and all(re.fullmatch(r'cjreg_[0-9a-f]{64}\.npz', f) for f in files_on) and set(modes) == {'0o444'}
        and any('새로 지어 저장' in ln for ln in lines_on) and any('읽음' in ln for ln in lines_on)
        and not any('⚠' in ln for ln in lines_on) and not lines_off and not gs_lines
        and all(on['sums'][k].get('cjunc_store') is True for k in ('P0', 'P1', 'pred', 'unit'))
        and all('cjunc_store' not in off['sums'][k] for k in ('P0', 'P1', 'pred', 'unit')),
        (files_on, modes, len(lines_on), lines_off[:2], gs_lines[:2], [on['sums'][k].get('cjunc_store') for k in ('P0', 'P1', 'pred', 'unit')]))
    #  ★ 11-13 RCP-07 — 요약에 팔별 저장본 상태 (런마다 팔마다 · 기록만) · 끔 = 칸 없음

    def arm_states(s):
        rows = s.get('cjunc_store_arms')
        if not isinstance(rows, list):
            return None
        return [(r.get('run'), a.get('arm'), a.get('status'), a.get('problem')) for r in rows for a in (r.get('arms') or [])]
    st_on = {k: arm_states(on['sums'][k]) for k in ('P0', 'P1', 'pred', 'unit')}
    chk('Z5b 요약 팔별 저장본 상태 (RCP-07) — 켬 = 단계 넷 모두 cjunc_store_arms (런 ≥ 1 · 팔마다 built_written | hit | built_peer_same · problem 없음 · 단계 넷의 짓고 쓴 '
        '수 합 = 저장본 파일 수) · 끔 = 칸 없음',
        all(isinstance(v, list) and v and all(x[2] in ('built_written', 'hit', 'built_peer_same') and x[3] is None for x in v) for v in st_on.values())
        and sum(1 for v in st_on.values() for x in v if x[2] == 'built_written') == len(files_on)
        and all('cjunc_store_arms' not in off['sums'][k] for k in ('P0', 'P1', 'pred', 'unit')), st_on)
    # Z6 — 적중 런
    hb = os.path.join(TD, 'runs', 'hit_P0')
    rc, so = E.e2e_call(ws, sd, ['--stage', 'ladder', '--law', 'P0', '--target', str(RR.TARGET_SBE_MS), '--runner', W['runner'], '--root', ws,
                                 '--plan', pp, '--s0-plan', sp, '--registration', rp, '--max-hours', E.E2E_MAXH, '--out', hb,
                                 '--machine', E.E2E_MACH] + E.s0_args() + ['--cjunc-store', store])
    sh = jload(os.path.join(hb, 'ladder_summary.json')) or {}
    mh = {k[1:]: v for k, v in arm_map(hb, sh, 'P0').items()}
    mo0 = {k[1:]: v for k, v in mo.items() if k[0] == 'P0'}
    hl = store_lines(glob.glob(os.path.join(hb, 'logs', '*.log')))
    chk('Z6 적중 런 (켬 폴더 · 사다리 P0 · 원장 없이) — rc 0 · CALIBRATED · 저장본 줄 = 전부 적중 (≥ 1) · 새 파일 없음 · 팔 JSON 바이트 = 끔 길 사다리 P0',
        rc == 0 and sh.get('status') == 'CALIBRATED' and hl and all('읽음' in ln for ln in hl) and sorted(os.listdir(store)) == files_on
        and mh and mh == mo0, (rc, sh.get('status'), hl[:3], sorted(os.listdir(store)) == files_on, sorted(set(mh) ^ set(mo0))[:3],
                               so[-400:]))
    sth = arm_states(sh)
    chk('Z6b 적중 런 요약 팔별 저장본 상태 (RCP-07) — 모든 팔 hit · problem 없음 (원장 없는 꼴 · 러너가 킷 런 폴더의 곁 파일을 OUTDIR 로 옮긴다)',
        isinstance(sth, list) and sth and all(x[2] == 'hit' and x[3] is None for x in sth), sth)


if __name__ == '__main__':
    sys.exit(main())
