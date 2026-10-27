#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""첫 풀이 끝 표지 감싸개 (`scripts/rint_first_result.py`) 단위 시험 — ★ 10-27 묶음 C2b (Q9 설계 개정 4 Q2 · R4-02 ⓒ · Codex 회차 ① Q-K ·
author 10-27 approved bundle C).

  python3 scripts/test_rint_first_result.py

가짜 `step3_sigma` (임시 폴더 · `_solve_cg` · `solve_sigma_z` 두 자리) 와 가짜 payload 로 감싸개를 **따로 프로세스**로 돌린다 (실제 러너 · payload 실경로 =
`scripts/test_ca_ext_runner.py` N12 · `scripts/test_rint_r_chain_e2e.py` E1u · E13):
  F01 CG 해 → 표지 한 번 (kind cg_solution · σ 없음 · 원자적 · payload 가 σ 를 찍기 전에 표지가 있다)
  F02 CG 없는 조기 반환 해 (σ 0) → 표지 한 번 (kind solve_return)
  F03 조립만 결과 (graph_only) → 표지 없음
  F04 표지 자리에 쓸 수 없음 → 감싸개 rc 5 · payload 가 σ 를 찍지 않는다 · 표지 없음
  F05 표지가 이미 있음 → 감싸개 rc 2 (payload 를 돌리지 않는다)
  F06 인자 꼴 (모자람 · 둘째가 payload 아님) → rc 2
  F07 payload 의 종료 코드 · argv · __name__ 그대로 (SystemExit 3 → rc 3)
  F08 두 번째 풀이 (같은 프로세스) = 표지를 다시 쓰지 않는다 (첫 결과만)
  F09 (구현과 함께 · 변이로 검증) 입구 검사 뒤 다른 프로세스가 같은 자리를 먼저 씀 → 덮지 않는다 · rc 5 · σ 없음
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WRAP = HERE / 'rint_first_result.py'
FAKE_S3 = r'''
def _solve_cg(L, b, x0=None, rtol=None):
    return [0.0], 0


def solve_sigma_z(mode='cg'):
    if mode == 'graph':
        return {'graph_only': True, 'cjunc_graphs': None}
    if mode == 'early':
        return {'sigma_eff': 0.0, 'reason': 'no_through_component'}
    _solve_cg(None, None)
    return {'sigma_eff': 1.25}
'''
FAKE_PAYLOAD = r'''
import os, sys
import step3_sigma as S3
mode = sys.argv[1]
mark = os.environ['T_MARK']
if mode == 'exit3':
    raise SystemExit(3)
if mode == 'race':                                  # 다른 프로세스가 같은 표지 자리를 먼저 쓴 꼴 (감싸개 입구 검사 뒤 · 풀이 전)
    open(mark, 'w').write('OTHER')
r = S3.solve_sigma_z('cg' if mode in ('cg', 'twice', 'race') else mode)
print('mark_before_sigma', os.path.exists(mark))
print('SIGMA', r.get('sigma_eff'))
if mode == 'twice':
    r2 = S3.solve_sigma_z('cg')
    print('SIGMA2', r2.get('sigma_eff'))
print('NAME', __name__, 'ARGV', sys.argv[1:])
'''

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:600]})' if why != '' else ''))


def run(td, mode, mark, extra=None):
    """가짜 scripts 폴더 (감싸개 사본 · 가짜 step3_sigma · 가짜 payload) 에서 감싸개 → (rc, 화면)."""
    sd = Path(td) / 'scripts'
    if not sd.exists():
        sd.mkdir()
        (sd / 'rint_first_result.py').write_bytes(WRAP.read_bytes())
        (sd / 'step3_sigma.py').write_text(FAKE_S3, encoding='utf-8')
        (sd / 'mpm_webapp_payload.py').write_text(FAKE_PAYLOAD, encoding='utf-8')
    argv = [sys.executable, '-I', str(sd / 'rint_first_result.py')] + (extra if extra is not None else [str(mark), str(sd / 'mpm_webapp_payload.py'), mode])
    env = dict(os.environ, T_MARK=str(mark), RINT_RUN_TOKEN='ab' * 16)
    p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=60)
    return p.returncode, p.stdout + p.stderr


def main():
    with tempfile.TemporaryDirectory(prefix='rint_first_result_t_') as td:
        unc = Path(td) / 'out' / '.unchecked'
        m1 = unc / 'p2_a0.json.first_result.json'
        rc, so = run(td, 'cg', m1)
        rec = json.loads(m1.read_text(encoding='utf-8')) if m1.exists() else {}
        chk('F01 CG 해 → 표지 한 번 · kind cg_solution · σ 칸 없음 · 그룹 표지 실림 · payload 가 σ 를 찍기 전에 표지가 있다 · 임시 파일 남지 않음',
            rc == 0 and rec.get('kind') == 'cg_solution' and rec.get('schema') == 'rint-first-result-v1' and not any('sigma' in k for k in rec)
            and rec.get('token') == 'ab' * 16 and 'mark_before_sigma True' in so and 'SIGMA 1.25' in so
            and sorted(x.name for x in unc.iterdir()) == [m1.name], (rc, rec, so[-300:]))
        m2 = unc / 'p2_a1.json.first_result.json'
        rc, so = run(td, 'early', m2)
        rec = json.loads(m2.read_text(encoding='utf-8')) if m2.exists() else {}
        chk('F02 CG 없는 조기 반환 해 (σ 0) → 표지 (kind solve_return) · σ 를 찍기 전', rc == 0 and rec.get('kind') == 'solve_return'
            and 'mark_before_sigma True' in so, (rc, rec, so[-300:]))
        m3 = unc / 'p2_a2.json.first_result.json'
        rc, so = run(td, 'graph', m3)
        chk('F03 조립만 결과 (graph_only) → 표지 없음', rc == 0 and not m3.exists() and 'mark_before_sigma False' in so, (rc, so[-300:]))
        blocker = Path(td) / 'afile'                    # 폴더 자리에 파일 (root 로 돌아도 막힌다 — 권한 비트는 root 를 못 막는다)
        blocker.write_text('x', encoding='utf-8')
        m4 = blocker / 'sub' / 'x.first_result.json'
        rc, so = run(td, 'cg', m4)
        chk('F04 표지 자리에 쓸 수 없음 (부모 자리가 파일) → 감싸개 rc 5 · payload 가 σ 를 찍지 않는다 · 표지 없음',
            rc == 5 and 'SIGMA' not in so and not m4.exists() and 'ABORT' in so, (rc, so[-300:]))
        rc, so = run(td, 'cg', m1)
        chk('F05 표지가 이미 있다 → rc 2 · payload 를 돌리지 않는다 (σ 없음)', rc == 2 and 'SIGMA' not in so, (rc, so[-200:]))
        sd = Path(td) / 'scripts'
        rc_a, so_a = run(td, 'cg', unc / 'q.json', extra=[str(unc / 'q.json')])
        rc_b, so_b = run(td, 'cg', unc / 'r.json', extra=[str(unc / 'r.json'), str(sd / 'step3_sigma.py'), 'cg'])
        chk('F06 인자 꼴 — 모자람 · 둘째가 mpm_webapp_payload.py 아님 → rc 2', rc_a == 2 and rc_b == 2, (rc_a, so_a[-120:], rc_b, so_b[-120:]))
        m7 = unc / 'p2_a7.json.first_result.json'
        rc, so = run(td, 'exit3', m7)
        chk('F07 payload 의 SystemExit 3 → 감싸개 rc 3 (종료 코드 그대로) · 표지 없음 (풀이 전)', rc == 3 and not m7.exists(), (rc, so[-200:]))
        m8 = unc / 'p2_a8.json.first_result.json'
        rc, so = run(td, 'twice', m8)
        rec = json.loads(m8.read_text(encoding='utf-8')) if m8.exists() else {}
        chk('F08 같은 프로세스의 두 번째 풀이 = 표지를 다시 쓰지 않는다 (첫 결과만 · 같은 이름 · __main__ · argv 그대로)',
            rc == 0 and rec.get('kind') == 'cg_solution' and 'SIGMA2 1.25' in so and "NAME __main__ ARGV ['twice']" in so, (rc, rec, so[-300:]))
        m9 = unc / 'p2_a9.json.first_result.json'
        rc, so = run(td, 'race', m9)
        body = m9.read_text(encoding='utf-8') if m9.exists() else None
        chk('F09 (구현과 함께 · 변이로 검증) 입구 검사 뒤 다른 프로세스가 같은 표지 자리를 먼저 씀 → 덮지 않는다 (그 내용 그대로) · 감싸개 rc 5 · σ 를 찍지 않는다',
            rc == 5 and body == 'OTHER' and 'SIGMA' not in so, (rc, body, so[-300:]))
    n = _ok + len(_fail)
    print(f'\ntest_rint_first_result: {_ok}/{n} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
