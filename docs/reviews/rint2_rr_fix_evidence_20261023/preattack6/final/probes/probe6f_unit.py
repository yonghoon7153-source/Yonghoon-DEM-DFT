#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 마무리 (11-02) — 단위 탐침 (실제 사슬 함수 · 합성 시도 폴더 · GPU 없음).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/final/probes/probe6f_unit.py <임시 폴더> [U4,U5,U6]

U4  PC6-01 × PC6-02 겹침 — 요약 있는 길 · 멈춤 GROUP_UNCONFIRMED (구경꾼 · 러너는 rc 1 로 끝남 · 런 기록 rc 1) · 로그 = 1저자 Q2 의 "그 밖 CUDA 오류" →
    원인 · 재실행 자격 (Runner._execute 는 확인 실패를 rc 보다 먼저 본다)
U5  --operator-why 꼴 검사 (사슬 main 인자 해석) — 줄바꿈 \\n · \\r 은 거부 · 그 밖 줄 경계 (U+2028 · U+0085 · \\v · \\f · \\x1c) · 터미널 제어 (\\x1b) ·
    --operator-confirm 유니코드 숫자 · 밑줄 숫자
U6  RECOUNT_KEYS 의 결정 몫 — 결과 줄 칸 하나씩 (status · stop) 만 바꾼 꼴이 채택 (adoption) 결과를 바꾸나 (변이 M2a · M2b 생존의 뜻 · 손 원장)
값 · σ 를 찍지 않는다.
"""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

WT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'U4', 'U5', 'U6'}
TD = Path(tempfile.mkdtemp(prefix='pa6f_unit_', dir=str(BASE)))
MARK = 'L01_floor_arm1/.unchecked/p2_SBE_vgcf100_a0.json.first_result.json'
MSGS = {
    'launch_failed': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_LAUNCH_FAILED: unspecified launch failure',
    'assert_runtime': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorAssert: device-side assert triggered',
    'illegal_address': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_ILLEGAL_ADDRESS: an illegal memory access was encountered',
    'python_bug': "Traceback (most recent call last):\nKeyError: 'sigma'",
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


def u4():
    rows = {}
    for nm, msg in MSGS.items():
        for rc in (1, 0):
            f = folder(f'U4_{nm}_rc{rc}', {MARK: '{}\n', 'logs/L01_floor.log': '[p2] run\n' + msg + '\n'})
            s = {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor', 'reason': None},
                 'runs': [{'name': 'L01_floor', 'outdir': 'L01_floor_arm1', 'rc': rc, 'group_cause': None}]}
            r = RR.attempt_result_line(1, f, s, 'recover')
            rows[f'{nm}/rc{rc}'] = (r['cause'], r['side'], r['resume_ok'])
    out('U4', rows=rows)


def _main_rc(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            rc = RR.main(argv)
        except SystemExit as e:
            rc = ('SystemExit', e.code)
    return rc, buf.getvalue().strip().splitlines()[-1:] if buf.getvalue().strip() else []


def u5():
    d = TD / 'U5_ledger'
    d.mkdir()
    o = TD / 'U5_out'
    o.mkdir()
    rows = {}
    for tag, why in (('newline', 'a\nb'), ('cr', 'a\rb'), ('u2028', 'a b'), ('u0085', 'a\u0085b'), ('vt', 'a\x0bb'), ('ff', 'a\x0cb'),
                     ('fs', 'a\x1cb'), ('esc', 'a\x1b[2Jb'), ('nul_free_ok', 'ok reason')):
        rc, tail = _main_rc(['--stage', 'recover', '--out', str(o), '--ledger', str(d), '--operator-confirm', '1', '--operator-why', why])
        rows[f'why_{tag}'] = {'rc': rc, 'splitlines_parts': len(why.splitlines()), 'tail': tail}
    for tag, n in (('fullwidth_1', '１'), ('underscore_1_0', '1_0'), ('plus', '+1'), ('space', ' 1 ')):
        rc, tail = _main_rc(['--stage', 'recover', '--out', str(o), '--ledger', str(d), '--operator-confirm', n, '--operator-why', 'ok'])
        rows[f'confirm_{tag}'] = {'rc': rc, 'tail': tail}
    out('U5', rows=rows)


def u6():
    """손 원장 상태 둘 (사슬 함수 adoption 만) — 칸 하나만 바꾼 결과 줄이 채택을 바꾸나."""
    hdr = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': 'a' * 64, 'utc': 'x'}

    def ent(n, resume_of=None):
        return {'kind': 'entry', 'n': n, 'target': 'ladder:P0', 'machine': 'kgy', 'resume_of': resume_of, 'plan_sha256': 'a' * 64,
                'code_key_sha256': 'c' * 64, 'env': {}, 'bed': {}, 'utc': 'x'}

    def res(n, status, stop, side, cause, ok):
        return {'kind': 'result', 'n': n, 'status': status, 'stop': stop, 'side': side, 'cause': cause, 'resume_ok': ok, 'folder': f'attempt_{n}',
                'folder_sha256': hashlib.sha256(str(n).encode()).hexdigest(), 'by': 'chain', 'utc': 'x'}
    stop_g = {'code': 'NOT_REGISTERED', 'run': None, 'reason': None}
    stop_rc = {'code': 'RUNNER_RC', 'run': 'L01_floor', 'reason': None}
    cases = {
        # 원 시도 1 = 결과 뒤 OOM (자격) · 재실행 2 = 결과 전 관문 멈춤 → status 를 rejected 로 (같은 stop · side · cause · ok)
        'resume_pre_stopped': [ent(1), res(1, 'stopped', stop_rc, 'post', 'resource', True), ent(2, 1), res(2, 'stopped', stop_g, 'pre', 'gate', False)],
        'resume_pre_as_rejected': [ent(1), res(1, 'stopped', stop_rc, 'post', 'resource', True), ent(2, 1), res(2, 'rejected', stop_g, 'pre', 'gate', False)],
        # 원 시도 1 = 결과 뒤 멈춤 · stop 만 다른 꼴 (원인 · 자격 같음)
        'post_stop_rc': [ent(1), res(1, 'stopped', stop_rc, 'post', 'runner_rc', False)],
        'post_stop_time': [ent(1), res(1, 'stopped', {'code': 'TIME_LIMIT', 'run': 'L01_floor', 'reason': None}, 'post', 'runner_rc', False)],
        # interrupted ↔ stopped (같은 stop dict · 원인 · 자격)
        'post_interrupted': [ent(1), res(1, 'interrupted', stop_rc, 'post', 'resource', True)],
    }
    rows = {}
    for k, lines in cases.items():
        raw = ''.join(RR.ledger_line(x) for x in [hdr] + lines).encode('utf-8')
        try:
            st = RR.ledger_parse(raw)
            ad = RR.adoption(st, 'ladder:P0')
            rows[k] = {'chain': ad['chain'], 'effective': ad['effective'], 'problems': [p[0] for p in ad['problems']],
                       'resume_allowed_next': (lambda last: last is not None and last['status'] != 'completed' and last['resume_ok'])(
                           st['results'].get(ad['effective']) if ad['effective'] else None)}
        except RR.Stop as e:
            rows[k] = {'parse': f'{e.code}: {e.cause[:120]}'}
    out('U6', rows=rows)


if __name__ == '__main__':
    out('env', python=sys.version.split()[0])
    for k, fn in (('U4', u4), ('U5', u5), ('U6', u6)):
        if k in ONLY:
            fn()
