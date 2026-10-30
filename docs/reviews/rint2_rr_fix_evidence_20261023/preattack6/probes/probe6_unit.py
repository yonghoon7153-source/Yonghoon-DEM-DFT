#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 (10-30 · 대상 4c69070ad = PC5 수정 b9fd47d7b..87a00ef46 포함) — 단위 탐침 (실제 사슬 함수 · 합성 시도 폴더 · GPU 없음).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/probes/probe6_unit.py <임시 폴더> [U1,U2,U3]

U1  1저자 Q2 "그 밖 CUDA 오류 = 자동 재실행 없음 (runner_rc)" ↔ 실제 결과 줄 원인 · 재실행 자격 — 같은 cupy 꼴 오류 한 줄이 런 로그에 있을 때
    (가) 요약 있는 길 RUNNER_RC · 그룹 원인 없음 (러너 rc 1 · 기준) (나) RUNNER_RC + 그룹 원인 timeout · signal (다) GROUP_UNCONFIRMED
    (라) 요약 없는 길 (recover) 끝 기록 by recover · by chain + timeout · signal
U2  요약 있는 길에서 멈춘 런의 로그가 없거나 못 읽을 때 (시간 초과 · 신호) ↔ 요약 없는 길 (못 읽음 = 재실행 자격 False)
U3  사슬 자신의 MemoryError · 디스크 부족 (OSError ENOSPC) = CHAIN_EXCEPTION → 원인 chain_exception · 재실행 자격 False
값 · σ 를 찍지 않는다.
"""
import errno
import hashlib
import json
import sys
import tempfile
from pathlib import Path

WT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'U1', 'U2', 'U3'}
TD = Path(tempfile.mkdtemp(prefix='pa6_unit_', dir=str(BASE)))
MARK = 'L01_floor_arm1/.unchecked/p2_SBE_vgcf100_a0.json.first_result.json'
DEAD = 2 ** 22 + 1
#: 1저자 Q2 의 "그 밖 CUDA 오류" (자원 낱말 다섯 · 잘못된 주소 둘 밖) — cupy 꼴 (시험 PC_MSGS 와 같은 글)
MSGS = {
    'assert_runtime': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorAssert: device-side assert triggered',
    'misaligned': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_MISALIGNED_ADDRESS: misaligned address',
    'illegal_instruction': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_INSTRUCTION: an illegal instruction was encountered',
    'launch_failed': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_LAUNCH_FAILED: unspecified launch failure',
    'launch_failure_rt': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorLaunchFailure: unspecified launch failure',
    'invalid_value': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorInvalidValue: invalid argument',
}


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def folder(tag, files):
    f = TD / tag / 'attempt_1'
    f.mkdir(parents=True)
    for rel, body in files.items():
        (f / rel).parent.mkdir(parents=True, exist_ok=True)
        (f / rel).write_text(body, encoding='utf-8')
    return f


def group(f, name, end, log=None, t='2026-10-30T00:00:00Z'):
    (f / 'groups').mkdir(parents=True, exist_ok=True)
    tok = hashlib.sha256(f'{f}|{name}'.encode()).hexdigest()[:32]
    L = {'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'pid': DEAD, 'pgid': DEAD, 'argv': ['bash'], 'host': RR.host_ident(),
         'started_utc': t, 'by': 'chain', 'chain_pid': DEAD}
    E = dict({'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'rc': None, 'cause': None, 'signal': None, 'confirmed': True, 'left': [],
              'left_after_exit': None, 'killed': 0, 'by': 'chain', 'ended_utc': t}, **end)
    (f / 'groups' / f'{name}.launch.json').write_text(json.dumps(L), encoding='utf-8')
    (f / 'groups' / f'{name}.end.json').write_text(json.dumps(E), encoding='utf-8')
    if log is not None:
        (f / 'logs').mkdir(parents=True, exist_ok=True)
        (f / 'logs' / f'{name}.log').write_text(log, encoding='utf-8')


def summ(code, gc=None, rc=1):
    return {'status': 'STOPPED', 'stop': {'code': code, 'run': 'L01_floor', 'reason': None},
            'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': rc, 'group_cause': gc}]}


def u1():
    rows = {}
    for nm, msg in MSGS.items():
        log = '[p2] run\n' + msg + '\n'
        cases = {
            'A_rc1_no_group_cause': (summ('RUNNER_RC', None, 1), None),
            'B_rc_timeout': (summ('TIME_LIMIT', 'timeout', None), None),
            'B_rc_signal': (summ('RUNNER_RC', 'signal', None), None),
            'C_group_unconfirmed': (summ('GROUP_UNCONFIRMED', None, 0), None),
            'D_orphan_by_recover': (None, {'by': 'recover', 'cause': 'parent_dead'}),
            'D_orphan_chain_timeout': (None, {'cause': 'timeout'}),
            'D_orphan_chain_signal': (None, {'cause': 'signal', 'signal': 'SIGTERM'}),
        }
        for cname, (s, end) in cases.items():
            f = folder(f'U1_{nm}_{cname}', {MARK: '{}\n', 'logs/L01_floor.log': log})
            if end is not None:
                group(f, 'L01_floor', end, log)
            r = RR.attempt_result_line(1, f, s, 'recover' if s is None else 'chain')
            rows[f'{nm}/{cname}'] = (r['cause'], r['side'], r['resume_ok'])
    bypass = sorted(k for k, v in rows.items() if v[2] is True)
    out('U1', rows=rows, n=len(rows), resumable=len(bypass), resumable_cases=bypass,
        verdict=('Q2 의 "그 밖 CUDA 오류 = 자동 재실행 없음" 이 rc 1 길에서만 선다 — 시간 초과 · 신호 · 그룹 미확인 · 사슬 부모 사망 길에서는 '
                 'resume_ok True' if bypass else 'all non-resumable'))


def u2():
    rows = {}
    for cname, s in (('timeout', summ('TIME_LIMIT', 'timeout', None)), ('signal', summ('RUNNER_RC', 'signal', None))):
        f = folder(f'U2_nolog_{cname}', {MARK: '{}\n'})            # 런 로그 없음 (요약 있는 길)
        r = RR.attempt_result_line(1, f, s, 'chain')
        rows[f'summary_nolog/{cname}'] = (r['cause'], r['side'], r['resume_ok'])
    f = folder('U2_orphan_nolog', {MARK: '{}\n'})
    group(f, 'L01_floor', {'by': 'recover', 'cause': 'parent_dead'}, None)
    r = RR.attempt_result_line(1, f, None, 'recover')
    rows['orphan_nolog/by_recover'] = (r['cause'], r['side'], r['resume_ok'])
    out('U2', rows=rows)


def u3():
    rows = {}
    for nm, exc in (('chain_MemoryError', MemoryError('arm json too big (probe)')),
                    ('chain_ENOSPC', OSError(errno.ENOSPC, 'No space left on device', 'ladder_summary.json'))):
        s = {'status': None, 'stop': None, 'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': 0, 'group_cause': None}]}
        RR.chain_exception_record(s, exc)
        f = folder(f'U3_{nm}', {MARK: '{}\n', 'logs/L01_floor.log': '[p2] ok\n'})
        r = RR.attempt_result_line(1, f, s, 'chain')
        rows[nm] = {'stop': s['stop'].get('code'), 'reason': str(s['stop'].get('cause'))[:80], 'cause': r['cause'], 'resume_ok': r['resume_ok']}
    out('U3', rows=rows)


if __name__ == '__main__':
    out('env', python=sys.version.split()[0], RESOURCE_WORDS=list(RR.RESOURCE_WORDS), NOT_RESOURCE_WORDS=list(RR.NOT_RESOURCE_WORDS),
        RESUME_CAUSES=sorted(RR.RESUME_CAUSES))
    for k, fn in (('U1', u1), ('U2', u2), ('U3', u3)):
        if k in ONLY:
            fn()
