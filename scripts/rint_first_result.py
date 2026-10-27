#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 — 첫 풀이 끝 표지 (payload 프로세스 안 · ★ 10-27 묶음 C2b · Q9 설계 개정 4 Q2 · R4-02 ⓒ · Codex 회차 ① Q-K · author 10-27 approved bundle C).

  python3 scripts/rint_first_result.py <표지 경로> scripts/mpm_webapp_payload.py <payload 인자 …>

러너 (`scripts/sdcp_gain_vox015_8arm.sh` · 사슬이 `P2_ATTEMPT=1` 로 부를 때) 가 킷의 payload 호출을 이 감싸개로 바꾼다.  감싸개는 같은 프로세스에서
payload 를 그대로 돌리되 (`runpy.run_path` · `__main__` · argv 그대로) 그 전에 `step3_sigma` 의 두 자리를 감싼다:
  · `_solve_cg` — 첫 CG 해가 돌아오는 즉시 (σ 를 셈하기 전 · 보수 쪽)
  · `solve_sigma_z` — 조립만 결과 (`graph_only`) 가 아닌 해가 돌아오는 즉시 (조기 반환 해 σ 0 포함 · payload 가 σ 를 화면 · 로그 · 파일에 쓰기 전)
첫 자리에서 표지를 **한 번** 원자적으로 쓴다 (같은 폴더 임시 파일 → fsync → os.replace → 폴더 fsync).  표지에 σ 는 없다 (값 봉인).  표지를 못 쓰면 그 자리에서
멈춘다 (SystemExit 5 · σ 를 내보내지 않는다).

결과 전 · 뒤 판정 (Q9 §3-5) = 시도 폴더 (안 `.unchecked/` 포함) 에 팔 payload (`p2_*.json*`) 또는 이 표지가 하나라도 있으면 결과 뒤.
⚠ 한정 (Q9 §3-5 · Codex Q-K): 남는 틈 = σ 를 얻고 표지를 쓰는 사이에 죽은 꼴 (그 σ 는 어디에도 쓰이지 않았다) · 감싸는 자리 = step3_sigma 의 풀이 길
(LEAN 2 R 런의 전자 솔브 · 다른 솔버 모듈은 감싸지 않는다) · 표지는 그 그룹이 끝난 뒤의 snapshot 으로만 뜻이 있다 (사슬이 그룹 종료를 확인한 뒤 판정).
"""
import functools
import json
import os
import runpy
import sys
import time

SCHEMA = 'rint-first-result-v1'
EXIT_MARK_FAIL = 5


def write_mark(path, kind):
    """표지 → 원자적 쓰기 (임시 → fsync → replace → 폴더 fsync) · σ 없음.  이미 있으면 덮지 않는다 (첫 결과만 · 두 번째는 실패 = 다른 프로세스가 같은 자리를 썼다)."""
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    if os.path.exists(path):
        raise FileExistsError(f'표지가 이미 있다: {path}')
    rec = {'schema': SCHEMA, 'kind': kind, 'pid': os.getpid(), 'token': os.environ.get('RINT_RUN_TOKEN'),
           'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    tmp = f'{path}.tmp.{os.getpid()}'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    try:
        fd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass                                                  # 폴더 fsync 를 못 하는 파일 체계 (기록만 · 표지 파일 자체는 fsync 됨)


def install(mark, s3):
    """step3_sigma 모듈 s3 의 두 자리를 감싼다 → 상태 dict (시험이 읽는다)."""
    state = {'fired': None}

    def fire(kind):
        if state['fired'] is not None:
            return
        try:
            write_mark(mark, kind)
        except Exception as e:                                # noqa: BLE001 — 표지 실패 = σ 를 내보내지 않고 멈춘다
            sys.stderr.write(f'[first-result] ABORT — 첫 풀이 끝 표지를 못 썼다 ({type(e).__name__}: {e}) — σ 를 내보내지 않는다\n')
            sys.stderr.flush()
            os._exit(EXIT_MARK_FAIL)
        state['fired'] = kind

    orig_cg = s3._solve_cg

    @functools.wraps(orig_cg)
    def _solve_cg(*a, **k):
        r = orig_cg(*a, **k)
        fire('cg_solution')
        return r

    orig_solve = s3.solve_sigma_z

    @functools.wraps(orig_solve)
    def solve_sigma_z(*a, **k):
        r = orig_solve(*a, **k)
        if not (isinstance(r, dict) and r.get('graph_only')):
            fire('solve_return')
        return r
    s3._solve_cg = _solve_cg
    s3.solve_sigma_z = solve_sigma_z
    return state


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or not argv[1].endswith('mpm_webapp_payload.py'):
        sys.stderr.write('usage: rint_first_result.py <표지 경로> <…/mpm_webapp_payload.py> <payload 인자 …>\n')
        return 2
    mark, payload = argv[0], argv[1]
    if os.path.exists(mark):
        sys.stderr.write(f'[first-result] ABORT — 표지가 이미 있다 (다른 시도 · 같은 자리): {mark}\n')
        return 2
    scr = os.path.dirname(os.path.abspath(payload))
    if scr not in sys.path:
        sys.path.insert(0, scr)
    import step3_sigma
    install(mark, step3_sigma)
    sys.argv = [payload] + argv[2:]
    runpy.run_path(payload, run_name='__main__')
    return 0


if __name__ == '__main__':
    sys.exit(main())
