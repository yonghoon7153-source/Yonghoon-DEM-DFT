#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PC5 수정 (10-28 밤) — 새 가드 변이 시험 (가드 하나씩 끄고 그 시험 접두가 잡나) · 사전 공격 5 회차 mutate_pa5.py 와 같은 틀.

  python3 mutate_pc5.py <원 트리> <사본 트리 (scripts 사본 · docs 링크)> <결과 json> [변이 id …]

사본 트리의 scripts/rint_r_chain.py 를 변이마다 원본에서 다시 쓰고 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` 를 돌린다 (rc ≠ 0 = 잡힘).
끝에 원본으로 되돌린다.  변이 = (id, 설명, 옛 글 (정확히 한 번), 새 글, 시험 접두).  'BASE' = 변이 없음 (사본 트리 기준선 · 모든 접두).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

M = [
    ('P01a', 'PC5-01 판정 · 합치기 — 결과 줄 다시 셈 (target_ledger_problem) 끔',
     "        why = result_line_problem(k, p, r)                      # ★ 10-28 밤 PC5-01 — status · stop · cause · 재실행 자격도 폴더 증거에서 다시 센다\n"
     "        if why:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)\n",
     "", 'PC01,PC02'),
    ('P01b', 'PC5-01 재실행 풀기 전 — 사슬 다시 셈 (resume_chain_problem) 끔',
     "        return resume_chain_problem(st, e, n, a.out)\n", "        return None\n", 'PC01'),
    ('P01c', 'PC5-01 입력 시도 — 결과 줄 다시 셈 (ledger_inputs_check) 끔',
     "        why = result_line_problem(n, d, r)                      # ★ 10-28 밤 PC5-01 — 입력 시도의 결과 줄 = 폴더 증거에서 다시 센 값\n"
     "        if why:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)\n",
     "", 'PC0,PC1,UM,AL,RS'),
    ('P01d', 'PC5-01 원장 역사 — 첫 부모 밖 원장 커밋 (merge -s ours) 검사 끔',
     "    if hidden:\n", "    if False:\n", 'PC02'),
    ('P02a', 'PC5-02 자원 낱말 — cupy 클래스 이름 둘 되살림',
     "RESOURCE_WORDS = ('OutOfMemoryError', 'CUDA_ERROR_OUT_OF_MEMORY', 'cudaErrorMemoryAllocation', 'MemoryError', 'No space left on device')",
     "RESOURCE_WORDS = ('OutOfMemoryError', 'CUDA_ERROR_OUT_OF_MEMORY', 'cudaErrorMemoryAllocation', 'MemoryError', 'No space left on device', "
     "'CUDARuntimeError', 'CUDADriverError')",
     'PC03,PC04'),
    ('P02b', 'PC5-02 낱말 규칙 — 잘못된 주소 (NOT_RESOURCE) 를 자원 낱말 뒤에 봄',
     "    if any(w in txt for w in NOT_RESOURCE_WORDS):\n        return 'runner_rc'\n    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n"
     "    return default\n",
     "    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n    if any(w in txt for w in NOT_RESOURCE_WORDS):\n        return 'runner_rc'\n"
     "    return default\n",
     'PC03'),
    ('P03a', 'PC5-03 recover — 산 사슬 부모 검사 끔',
     "            if alive is not False:\n", "            if False:\n", 'PC05'),
    ('P03b', 'PC5-03 사슬 부모 — 시작 시각 대조 끔 (pid 다시 쓰임 = 산 사슬)',
     "    return type(cs) is int and ps[1] == cs\n", "    return True\n", 'PC05'),
    ('P03c', 'PC5-03 사슬 부모 — 시작 시각 칸 없음 = 죽은 사슬',
     "        return True                                            # 시작 시각 칸 없음",
     "        return False                                           # 시작 시각 칸 없음", 'PC05'),
    ('P04a', 'PC5-04 recover — 다른 부팅을 볼 수 있는 쪽으로 (옛 재부팅 확인 꼴)',
     "        if same_boot and same_ns and same_mid:\n", "        if same_ns and same_mid:\n", 'PC06,GR08'),
    ('P04b', 'PC5-04 recover — machine_id 다름 검사 끔',
     "        if same_boot and same_ns and same_mid:\n", "        if same_boot and same_ns:\n", 'GR08'),
    ('P04c', 'PC5-04 운영자 표지 — 시도 폴더 범위 끔 (바탕의 모든 그룹)',
     "        opx = op if (op is not None and _attempt_of(lp, root) == fo) else None\n", "        opx = op\n", 'PC06'),
    ('P04d', 'PC5-04 운영자 표지 — 쓰이지 않은 표지 = rc 3 끔',
     "    if op is not None and n_used == 0:\n", "    if False:\n", 'PC06'),
    ('P04e', 'PC5-04 운영자 표지 — 번호 · 사유 꼴 검사 끔',
     r"        if a.operator_confirm < 1 or not why.strip() or '\n' in why or '\r' in why or len(why) > 300:",
     "        if False:", 'PC06'),
    ('P05a', 'PC5-05 채택 — 결과 전 멈춘 재실행 건너뜀 끔',
     "        if e['resume_of'] is not None and side == 'pre':\n", "        if False:\n", 'PC07'),
    ('P06a', 'PC5-06 요약 없는 시도 — 원인 = 늘 parent_dead · 읽음 (옛)',
     "        cause, readable = orphan_cause(folder)", "        cause, readable = 'parent_dead', True", 'PC08,PC09'),
    ('P06b', 'PC5-06 요약 있는 길 — 신호 · 시간 초과 · 그룹 미확인의 잘못된 주소 낱말 끔',
     "    return 'runner_rc' if any(w in txt for w in NOT_RESOURCE_WORDS) else base\n", "    return base\n", 'PC11'),
    ('P06c', 'PC5-06 ② 사슬 예외 — 요약 · 결과 줄 없이 다시 올림 (사다리)',
     "        chain_exc = chain_exception_record(s, e)\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    write_json(out / 'ladder_summary.json', s)",
     "        raise\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    write_json(out / 'ladder_summary.json', s)", 'PC10'),
    ('P06d', 'PC5-06 요약 없는 시도 — 런 로그 못 읽음 = 읽음으로',
     "            txt, ok = '', False\n", "            txt = ''\n", 'PC09'),
    ('P06e', 'PC5-06 결과 칸 — 못 읽음을 재실행 자격에서 뺌',
     " and not trace and readable\n", " and not trace\n", 'PC09'),
    ('P07a', 'PC5-07 그룹 원 — Z 지도자의 산 스레드 끔 (Z = 끝남 · 옛)',
     "            if ps[0] in _DEAD_STATES:\n                live = None\n", "            if ps[0] in _DEAD_STATES:\n                continue\n", 'PC14'),
    ('P07b', 'PC5-07 그룹 원 — environ 못 읽음 = 건너뜀 (옛)',
     "                unsure = True\n                continue\n        except OSError:\n", "                continue\n        except OSError:\n", 'PC14'),
    ('P07c', 'PC5-07 그룹 원 — 그룹 시작 전 프로세스 거름 끔',
     "\n                        or (since is not None and ps[1] is not None and ps[1] < since)):", "):", 'PC14'),
    ('P07d', 'PC5-07 그룹 원 — 다른 실 uid 거름 끔',
     "(uid != 0 and ru is not None and ru != uid)", "False", 'PC14'),
    ('P07e', 'PC5-07 그룹 원 — pid 1 셈 밖 끔',
     "if (int(e) == 1 or (uid", "if ((uid", 'PC14,PC05,GR'),
    ('P08a', 'PC5-08 덧붙임 — 실패 뒤 되돌림 끔',
     "                try:\n                    _ledger_rollback(repo, raw)\n                except (OSError, Stop):\n                    pass\n", "", 'PC15'),
    ('P08b', 'PC5-08 덧붙임 — 배타 잠금 끔',
     "    with ledger_lock(repo, exclusive=True):\n        _head, raw = _ledger_now(repo)",
     "    with contextlib.nullcontext():\n        _head, raw = _ledger_now(repo)", 'PC15'),
    ('P08c', 'PC5-08 --init — git 실패 뒤 되돌림 끔',
     "                            if not _ledger_committed(repo, hb):\n                                _ledger_rollback(repo, None)\n",
     "                            pass\n", 'PC15'),
    ('P10a', 'PC5-10 다시 판정 — 다른 대상 시도 폴더 너그러움 끔 (옛)',
     "        if commit != head and en is not None and en['target'] not in keep:\n            continue\n", "", 'PC16'),
    ('P10b', 'PC5-10 다시 판정 — 같은 대상 뒤 시도도 너그럽게',
     "        if commit != head and en is not None and en['target'] not in keep:\n", "        if commit != head and en is not None:\n", 'PC16'),
    #  사전 공격 5 회차 변이 구멍 둘 (mutate_pa5.py 의 X09 · X18 · 같은 옛 글 · 새 상주 시험 접두)
    ('X09', '결과 줄 꼴 — rejected 인데 결과 뒤 · 재실행 자격 검사 끔',
     "    if r['status'] == 'rejected' and (r['side'] != 'pre' or r['resume_ok']):\n        return '거부인데 결과 뒤 · 재실행 자격'\n", "", 'PC12'),
    ('X18', 'recover --ledger — 거부 기록 (rejected.json) 폴더 = rejected 결과 줄 끔',
     "            rj = f / REJECTED_FILE\n            if rj.is_file():", "            rj = f / REJECTED_FILE\n            if False:", 'PC13'),
]


def main():
    wt, tree, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pick = set(sys.argv[4:])
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', OMPI_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
               PYTHONDONTWRITEBYTECODE='1')
    res = json.loads(outp.read_text()) if outp.exists() else []
    done = {r['id'] for r in res}
    todo = list(M)
    if 'BASE' in pick:
        todo = [('BASE', '변이 없음 (사본 트리 기준선)', None, None, ','.join(sorted({p for m in M for p in m[4].split(',')})))] + todo
    try:
        for mid, why, old, new, only in todo:
            if (pick and mid not in pick) or mid in done:
                continue
            if old is None:
                dst.write_text(src, encoding='utf-8')
            else:
                n = src.count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'error': f'옛 글 {n} 번'})
                    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                dst.write_text(src.replace(old, new, 1), encoding='utf-8')
            t0 = time.time()
            p = subprocess.run(['nice', '-n', '19', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                               capture_output=True, text=True, env=env, cwd=str(tree))
            tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
            fails = [ln.strip()[:60] for ln in p.stdout.splitlines() if ln.lstrip().startswith('FAIL ')]
            res.append({'id': mid, 'why': why, 'only': only, 'rc': p.returncode, 'killed': p.returncode != 0,
                        'summary': tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:]), 'fails': fails, 'seconds': round(time.time() - t0, 1)})
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
            print(mid, ('killed' if p.returncode else 'SURVIVED') if old is not None else ('BASE-FAIL' if p.returncode else 'BASE-OK'),
                  tail[-1] if tail else '', flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
