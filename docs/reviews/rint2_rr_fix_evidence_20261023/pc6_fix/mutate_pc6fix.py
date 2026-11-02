#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 고침 (PC6-01 · 02 · 09 · 11 · 12 · 11-02) — 변이 시험 (가드 하나씩 끄고 그 시험 접두가 잡나) · mutate_pc5.py (10-28) 와 같은 틀.

  python3 mutate_pc6fix.py <원 트리> <사본 트리 (scripts 사본 · docs · webapp 링크)> <결과 json> <로그 폴더> <묶음: moved | pc6 | pc611 | all | <id,…>>

묶음 — moved = 10-28 의 32 중 이번 고침이 옛 글을 옮긴 셋 (P02b · P06b · P07b) 의 같은 가드 · pc6 = 이번 새 가드 (PC6-01 · 02 · 09 · 12) ·
pc611 = PC6-11 (사전 공격 6 회차 마무리 §3-2 의 생존 변이 M2e · M2c · M9 · M8 · M11 · M12 · M15 — 같은 가드 · 옛 글은 지금 사슬 글 (M11 = 이번 고침이 옮김)).
변이마다 사본 트리의 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` (rc ≠ 0 = 잡힘) · 화면 전문 =
<로그 폴더>/<id>.log · 옛 글은 정확히 한 번 (아니면 ERROR) · 끝에 원본으로 되돌린다.  'BASE' = 변이 없음 (모든 접두의 합).  값 · σ 없음 (가짜 러너).
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

#: (id, 끈 가드, 옛 글 (정확히 한 번), 새 글, 시험 접두, 기대 (killed | survived:<까닭>))
MOVED = [
    ('P02b2', 'PC5-02 낱말 규칙 — 잘못된 주소를 자원 낱말 뒤에 봄 (P02b 의 같은 가드 · 이번 고침이 옛 글을 옮김)',
     "    if any(w in txt for w in NOT_RESOURCE_WORDS):\n        return 'runner_rc'\n    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n",
     "    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n    if any(w in txt for w in NOT_RESOURCE_WORDS):\n        return 'runner_rc'\n",
     'PC03', 'killed'),
    ('P06b2', 'PC5-06 요약 있는 길 — 신호 · 시간 초과 · 그룹 미확인의 낱말 규칙 끔 (P06b 의 같은 가드 · 옛 글 옮김)',
     "    return words_keep(txt, base)\n", "    return base\n", 'PC11', 'killed'),
    ('P07b2', 'PC5-07 그룹 원 — environ 못 읽음 = 건너뜀 (P07b 의 같은 가드 · 옛 글 옮김)',
     "                unsure.append(int(e))\n                continue\n        except OSError:\n", "                continue\n        except OSError:\n",
     'PC14', 'killed'),
]
PC6 = [
    # PC6-01 — 그룹 원 찾기 (러너 세션 · 계보)
    ('N01a', 'PC6-01 못 읽는 프로세스의 러너 세션 · 계보 거름 끔 (옛 = 같은 실 uid 면 확인 불가)',
     "                if run is not None and not _run_kin(ps, run, needle, me, ours):\n", "                if False:\n", 'PD01', 'killed'),
    ('N01b', 'PC6-01 _run_kin 늘 False (러너 세션 안도 셈 밖 = 거짓 확인)',
     "    sid = run['pid']\n\n    def inside(st):\n", "    return False\n    sid = run['pid']\n\n    def inside(st):\n", 'PD01', 'killed'),
    ('N01c', 'PC6-01 러너 세션 칸 (세션 번호) 무시 — 그룹 번호만',
     "        return ours and (st[4] == sid or st[3] == sid)\n", "        return ours and (st[3] == sid)\n", 'PD01', 'killed'),
    ('N01d', 'PC6-01 러너 그룹 번호 무시 — 세션 번호만',
     "        return ours and (st[4] == sid or st[3] == sid)\n", "        return ours and (st[4] == sid)\n", 'PD01', 'killed'),
    ('N01e', 'PC6-01 계보 위 표지 env 프로세스 대조 끔',
     "            if needle in Path(PROC_DIR, str(a), 'environ').read_bytes().split(b'\\0'):\n                return True\n",
     "            if False:\n                return True\n", 'PD01', 'killed'),
    ('N01f', 'PC6-01 계보 (ppid) 거슬러 보기 끔 (세션 · 그룹 칸만)',
     "    a, seen = ps[2], set()\n", "    return False\n    a, seen = ps[2], set()\n", 'PD01', 'killed'),
    ('N01g', 'PC6-01 러너 세션 번호 다시 쓰임 대조 끔 (지도자 시작 시각)',
     "    return not (ld is not None and type(st0) is int and ld[1] is not None and ld[1] != st0)\n", "    return True\n", 'PD01', 'killed'),
    ('N01h', 'PC6-01 지도자 없음 = 다른 세션으로 (보수 반대)',
     "    return not (ld is not None and type(st0) is int and ld[1] is not None and ld[1] != st0)\n",
     "    return ld is not None and not (type(st0) is int and ld[1] is not None and ld[1] != st0)\n", 'PD01', 'killed'),
    ('N01i', 'PC6-01 러너 시작 시각 모름 = 다른 세션으로 (보수 반대)',
     "    return not (ld is not None and type(st0) is int and ld[1] is not None and ld[1] != st0)\n",
     "    return not (ld is not None and (type(st0) is not int or ld[1] is None or ld[1] != st0))\n", 'PD01', 'killed'),
    ('N01j', 'PC6-01 계보 고리 = 셈 밖 (보수 반대)',
     "        if a in seen:\n            return True\n", "        if a in seen:\n            return False\n", 'PD01', 'killed'),
    ('N01k', 'PC6-01 계보 깊이 상한 = 셈 밖 (보수 반대)',
     "        a = st[2]\n    return True\n", "        a = st[2]\n    return False\n", 'PD01', 'killed'),
    ('N01l', 'PC6-01 부모 stat 못 읽음 = 셈 밖 (보수 반대)',
     "        except OSError:\n            return True\n        if st is None:\n", "        except OSError:\n            return False\n        if st is None:\n",
     'PD01', 'survived:결정 동등 (주 루프가 같은 프로세스의 stat 못 읽음을 이미 확인 불가로 센다 — 부모는 /proc 의 한 항목이다 · 사이 경합만 다름)'),
    ('N01m', 'PC6-01 확인 불가여도 찾은 표지 프로세스 죽이기 끔 (옛)',
     "            if found:\n                killed.update(found)\n", "            if False:\n                killed.update(found)\n", 'PD01', 'killed'),
    ('N01n', 'PC6-01 run_in_group 이 러너 세션 (GROUP_RUN) 을 넣지 않음',
     "            GROUP_RUN[token] = {'pid': p.pid, 'start': launch.get('runner_start')}\n", "            pass\n", 'PD01r', 'killed'),
    ('N01o', 'PC6-01 recover_group 이 시작 기록의 러너 세션을 넣지 않음',
     "                GROUP_RUN[tok] = {'pid': rp, 'start': rs if type(rs) is int else None}\n", "                pass\n", 'PD01', 'killed'),
    ('N01p', 'PC6-01 시작 기록 runner_start 안 적음',
     "launch.update(pid=p.pid, pgid=pg, runner_start=(rs[1] if rs else None))", "launch.update(pid=p.pid, pgid=pg, runner_start=None)", 'PD01r', 'killed'),
    ('N01q', 'PC6-01 run_in_group 끝 기록 unsure (확인 불가 pid) 안 적음',
     "            unsure = (GROUP_SCAN.get(token) or {}).get('unsure') if left is None else None\n", "            unsure = None\n", 'PD01r', 'killed'),
    ('N01r', 'PC6-01 recover 사유의 확인 불가 pid 뺌',
     "(f' (러너 세션 · 계보 안 pid {unsure[:8]})' if unsure else '')", "''", 'PD01', 'killed'),
    ('N01s', 'PC6-01 proc_stat 부모 · 그룹 칸 바꿔 읽음',
     "    return fl[0], num(19), num(1), num(2), num(3)\n", "    return fl[0], num(19), num(2), num(1), num(3)\n", 'PD01', 'killed'),
    # PC6-02 — 그 밖 CUDA 오류 = 모든 길 runner_rc
    ('N02a', 'PC6-02 그 밖 CUDA 오류 표지 끔 (옛 = 러너 rc 길의 기본값만)',
     "    if any(w in txt for w in CUDA_ERROR_WORDS):\n        return 'runner_rc'\n", "", 'PD02', 'killed'),
    ('N02b', 'PC6-02 CUDA 표지를 자원 낱말 앞에 봄 (OOM 줄의 클래스 이름 = runner_rc · Q2 차례 반대)',
     "    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n    if any(w in txt for w in CUDA_ERROR_WORDS):\n        return 'runner_rc'\n",
     "    if any(w in txt for w in CUDA_ERROR_WORDS):\n        return 'runner_rc'\n    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n",
     'PD02', 'killed'),
    ('N02c', 'PC6-02 words_keep = 늘 그 길 원인 (낱말 규칙 끔)',
     "    return 'runner_rc' if words_cause(txt, None) == 'runner_rc' else base\n", "    return base\n", 'PD02,PC11', 'killed'),
    ('N02d', 'PC6-02 orphan_cause 시간 초과 · 신호 = 잘못된 주소만 (옛)',
     "            c = words_keep(txt, 'timeout' if gc == 'timeout' else 'signal')",
     "            c = 'runner_rc' if any(w in txt for w in NOT_RESOURCE_WORDS) else ('timeout' if gc == 'timeout' else 'signal')", 'PD02', 'killed'),
    ('N02e', 'PC6-02 stop_cause 재실행 자격 원인 = 잘못된 주소만 (옛)',
     "    return words_keep(txt, base)\n", "    return 'runner_rc' if any(w in txt for w in NOT_RESOURCE_WORDS) else base\n", 'PD02', 'killed'),
    ('N02f', 'PC6-02 표지 CUDA_ERROR_ 뺌',
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError')",
     "CUDA_ERROR_WORDS = ('cudaError', 'CUDARuntimeError', 'CUDADriverError')", 'PD02', 'killed'),
    ('N02g', 'PC6-02 표지 cudaError 뺌',
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError')",
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'CUDARuntimeError', 'CUDADriverError')", 'PD02', 'killed'),
    ('N02h', 'PC6-02 표지 CUDARuntimeError 뺌',
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError')",
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDADriverError')", 'PD02', 'killed'),
    ('N02i', 'PC6-02 표지 CUDADriverError 뺌',
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError')",
     "CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError')", 'PD02', 'killed'),
    # PC6-09 — 이 항목 시도 폴더 재진입 = 화면만
    ('N09a', 'PC6-09 이 항목 시도 폴더 = 화면만 끔 (옛 = 옆 거부 기록 + rejected 결과 줄)',
     "        if mine:\n", "        if False:\n", 'PD09', 'killed'),
    ('N09b', 'PC6-09 이 항목 판정에서 시작 커밋 원장 조상 대조 뺌',
     "                    and ledger_is_ancestor(repo, own['ledger_commit'], head))\n", "                    and True)\n", 'PD09', 'killed'),
    ('N09c', 'PC6-09 이 항목 판정에서 대상 · 기계 · 재실행 원 시도 대조 뺌',
     "            mine = (own is not None and own['n'] == n and all(own[k] == e[k] for k in ('target', 'machine', 'resume_of'))\n",
     "            mine = (own is not None and own['n'] == n\n", 'PD09', 'killed'),
    # PC6-12 — 찾은 시도 폴더 attempt.json ↔ 원장 항목
    ('N12a', 'PC6-12 판정 (ledger_verdict_check) 의 찾은 시도 폴더 대조 끔',
     "    why = found_attempts_problem(st, found)                 # ★ 11-02 PC6-12 — 입력 대상 밖 시도 폴더의 attempt.json 도 원장 항목과\n"
     "    if why:\n        raise Stop('ATTEMPT_LEDGER_MISMATCH', why)\n", "", 'PD12', 'killed'),
    ('N12b', 'PC6-12 예측 입력 (ledger_inputs_check) 의 사다리 바탕 대조 끔',
     "    why = found_attempts_problem(st, _attempt_folders([Path(d).resolve().parent for d in dirs]))   # ★ 11-02 PC6-12 — 사다리 바탕의 다른 시도 폴더도\n"
     "    if why:\n        raise Stop('ATTEMPT_LEDGER_MISMATCH', why)\n", "", 'PD12', 'killed'),
    ('N12c', 'PC6-12 합치기 (--merge 경로) 대조 끔',
     "        why = found_attempts_problem(st, found)             # ★ 11-02 PC6-12 — 합칠 시도 폴더의 attempt.json 도 원장 항목과 (원장만 고친 대상 바꿈)\n"
     "        if why:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', why)\n", "", 'PD12m', 'killed'),
    ('N12d', 'PC6-12 합친 예측 판정 (merged_ledger_check · 사본) 대조 끔',
     "    why = found_attempts_problem(st, found)                 # ★ 11-02 PC6-12 — 사본의 attempt.json (대상 · 기계 · 재실행 원 시도) 도 원장 항목과\n"
     "    if why:\n        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{d.name}: {why}')\n", "", 'PD12,UM08',
     'survived:결정 동등에 가까움 (사본 = 결과 줄 요약 sha 로 묶이고 자리 units/<대상> 이 대상을 묶는다 — attempt.json 을 바꾸면 요약 sha 가 먼저 어긋난다 · 미시험)'),
    ('N12e', 'PC6-12 대조 칸에서 대상 뺌', "            diff = [f for f in ('target', 'machine', 'resume_of') if a[f] != e[f]]\n",
     "            diff = [f for f in ('machine', 'resume_of') if a[f] != e[f]]\n", 'PD12', 'killed'),
    ('N12f', 'PC6-12 대조 칸에서 기계 뺌', "            diff = [f for f in ('target', 'machine', 'resume_of') if a[f] != e[f]]\n",
     "            diff = [f for f in ('target', 'resume_of') if a[f] != e[f]]\n", 'PD12', 'killed'),
    ('N12g', 'PC6-12 대조 칸에서 재실행 원 시도 뺌', "            diff = [f for f in ('target', 'machine', 'resume_of') if a[f] != e[f]]\n",
     "            diff = [f for f in ('target', 'machine') if a[f] != e[f]]\n", 'PD12', 'killed'),
    ('N12h', 'PC6-12 대조 늘 통과', "            if a['n'] != k or diff:\n", "            if False:\n", 'PD12', 'killed'),
]
PC611 = [
    ('M2e', 'PC5-01 다시 셈 칸에서 resume_ok 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause')", 'PD11', 'killed'),
    ('M2c', 'PC5-01 다시 셈 칸에서 side 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'stop', 'cause', 'resume_ok')", 'PD11', 'killed'),
    ('M9', 'PC5-01 재실행 풀기 전 다시 셈 = 원 시도만 (앞 재실행 뺌)',
     "and k < n and (k == orig or x['resume_of'] == orig)]:", "and k < n and k == orig]:", 'PD11', 'killed'),
    ('M8', 'PC5-10 다시 판정 keep — 합친 예측의 단위 · 점 대상 뺌',
     "    keep = set(want) | {t for _d, sm in merged for t in (((sm.get('merge') or {}).get('units') or {}) if isinstance(sm.get('merge'), dict) else {})}\n",
     "    keep = set(want)\n", 'PD11m', 'killed'),
    ('M11', 'PC5-07 group_members — stat 못 읽음 = 건너뜀 (이번 고침이 옛 글을 옮김: unsure = True → unsure.append)',
     "        except OSError:\n            unsure.append(int(e))\n            continue\n        if needle in env.split(b'\\0'):",
     "        except OSError:\n            continue\n        if needle in env.split(b'\\0'):", 'PD11s', 'killed'),
    ('M12', 'PC5-03 chain_parent_alive — chain_pid 칸 없음 · 꼴 틀림 = 죽은 것으로',
     "    if type(cp) is not int or cp <= 0:\n        return None\n", "    if type(cp) is not int or cp <= 0:\n        return False\n", 'PD11g', 'killed'),
    ('M15', 'PC5-06 ② 사슬 예외 — 요약 · 결과 줄 없이 다시 올림 (예측 단계)',
     "        chain_exc = chain_exception_record(s, e)\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    sname = 'predict_summary.json'",
     "        raise\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    sname = 'predict_summary.json'", 'PD11p', 'killed'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(\S+)\s+(.*)$')


def run_one(tree, mid, only, env, logd):
    t0 = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                       capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    fails = [{'cid': m.group(1), 'line': m.group(2)[-700:]} for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, tree, outp, logd, group = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5]
    logd.mkdir(parents=True, exist_ok=True)
    groups = {'moved': MOVED, 'pc6': PC6, 'pc611': PC611}
    allm = MOVED + PC6 + PC611
    if group in groups:
        todo = list(groups[group])
    elif group == 'all':
        todo = list(allm)
    else:
        pick = set(group.split(','))
        todo = [m for m in allm if m[0] in pick]
        if 'BASE' in pick:
            todo = [('BASE', '변이 없음', None, None, ','.join(sorted({x for m in allm for x in m[4].split(',')})), 'pass')] + todo
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    res = json.loads(outp.read_text(encoding='utf-8')) if outp.exists() else []
    done = {r['id'] for r in res}
    try:
        for mid, why, old, new, only, expect in todo:
            if mid in done:
                continue
            if old is None:
                dst.write_text(src, encoding='utf-8')
            else:
                n = src.count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'only': only, 'error': f'옛 글 {n} 번'})
                    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                mutated = src.replace(old, new, 1)
                compile(mutated, 'rint_r_chain.py', 'exec')            # 문법 검사 (변이가 문법을 깨면 그 자체가 잘못된 변이)
                dst.write_text(mutated, encoding='utf-8')
            rc, summary, fails, sec = run_one(tree, mid, only, env, logd)
            res.append({'id': mid, 'why': why, 'only': only, 'expect': expect, 'rc': rc, 'killed': (rc != 0) if old is not None else None,
                        'summary': summary, 'fails': fails, 'seconds': sec})
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            state = ('killed' if rc else 'SURVIVED') if old is not None else ('BASE-FAIL' if rc else 'BASE-OK')
            print(mid, only, state, f'(기대 {expect})', summary, 'fails=', [f['cid'] for f in fails], flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
