#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 마무리 (11-02 · 대상 = PC5 수정 b9fd47d7b..87a00ef46 · 사슬 코드 = 4c69070ad 와 바이트 같음) — 변이 시험 (가드 하나씩 끄고
어느 시험이 · 어떤 이유로 잡나).  mutate_pc5.py (10-28 · 32 변이) 의 옛 글 · 새 글을 그대로 불러 다시 돌리고 (잡힌 이유 = FAIL 줄 전문 기록),
중간 보고 §3 계획 M1–M10 + 이 회차가 더한 가드 (M11–M15) 를 넓은 접두로 돌린다.

  python3 mutate_pc6.py <원 트리> <사본 트리 (scripts 사본 · docs · webapp 링크)> <결과 json> <로그 폴더> <묶음: pc5 | new | <id,…>> [접두 덮어쓰기]

변이마다 사본 트리의 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` (rc ≠ 0 = 잡힘) ·
화면 전문 = <로그 폴더>/<id>.log · FAIL 줄 = (검사 id · 사유 600 자) · 끝에 원본으로 되돌린다.  옛 글은 정확히 한 번 있어야 한다 (아니면 ERROR).
값 · σ 를 찍지 않는다 (가짜 러너 세계).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
PC5 = HERE.parents[3] / 'preattack5' / 'fix_pc5_20261028' / 'mutate_pc5.py'

BROAD = 'PC,AL,RS,UM,GR'

#: 이 회차 변이 — (id, 끈 가드, 옛 글, 새 글, 접두, 의도한 시험 접두 (잡으면 "옳은 이유" 후보))
NEW = [
    ('M1', 'PC5-01 원장 역사 — 숨긴 커밋 셈에서 --full-history 뺌 (기본 역사 단순화 = -s ours 의 둘째 부모를 버린다)',
     "    al = ledger_git(repo, 'rev-list', '--full-history', '--no-merges', commit, '--', LEDGER_FILE, check=False)\n",
     "    al = ledger_git(repo, 'rev-list', '--no-merges', commit, '--', LEDGER_FILE, check=False)\n", BROAD, 'PC02'),
    ('M2a', 'PC5-01 다시 셈 칸에서 status 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('stop', 'side', 'cause', 'resume_ok')", BROAD, 'PC01'),
    ('M2b', 'PC5-01 다시 셈 칸에서 stop 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'side', 'cause', 'resume_ok')", BROAD, 'PC01'),
    ('M2c', 'PC5-01 다시 셈 칸에서 side 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'stop', 'cause', 'resume_ok')", BROAD, 'PC01'),
    ('M2d', 'PC5-01 다시 셈 칸에서 cause 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'stop', 'side', 'resume_ok')", BROAD, 'PC01'),
    ('M2e', 'PC5-01 다시 셈 칸에서 resume_ok 뺌',
     "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause', 'resume_ok')", "RECOUNT_KEYS = ('status', 'stop', 'side', 'cause')", BROAD, 'PC01'),
    ('M3', 'PC5-03 chain_parent_alive — 부른 프로세스 자신 = False → None (산 것으로)',
     "    if cp == os.getpid():\n        return False\n", "    if cp == os.getpid():\n        return None\n", BROAD, 'PC05,GR,AL13,AL14,PC13'),
    ('M4', 'PC5-03 run_in_group 시작 기록 chain_start = None (pid 다시 쓰임을 가를 수 없음)',
     "'chain_start': (me_stat[1] if me_stat else None), 'since_ticks': since}", "'chain_start': None, 'since_ticks': since}", BROAD, 'PC05'),
    ('M5', 'PC5-08 ledger_now 공유 잠금 끔',
     "    with ledger_lock(repo, exclusive=False):\n        return _ledger_now(repo)\n", "    return _ledger_now(repo)\n", BROAD, 'PC15'),
    ('M6', 'PC5-08 ledger_append — 커밋이 됐는데 git 실패면 그 커밋 (→ 늘 되돌림 · 다시 올림)',
     "            if not landed:\n", "            if True:\n", BROAD, 'PC15'),
    ('M7', 'PC5-08 _ledger_rollback — 색인 git reset 뺌',
     "    os.replace(tmp, lp)\n    ledger_git(repo, 'reset', '-q', '--', LEDGER_FILE, check=False)\n", "    os.replace(tmp, lp)\n", BROAD, 'PC15'),
    ('M8', 'PC5-10 다시 판정 keep — 합친 예측의 단위 · 점 대상 뺌',
     "    keep = set(want) | {t for _d, sm in merged for t in (((sm.get('merge') or {}).get('units') or {}) if isinstance(sm.get('merge'), dict) else {})}\n",
     "    keep = set(want)\n", BROAD, 'PC16'),
    ('M9', 'PC5-01 재실행 풀기 전 다시 셈 = 원 시도만 (앞 재실행 뺌)',
     "and k < n and (k == orig or x['resume_of'] == orig)]:", "and k < n and k == orig]:", BROAD, 'PC01,PC07,RS04'),
    ('M10a', 'PC5-07 run_in_group 이 GROUP_SINCE 를 넣지 않음 (since 늘 None)',
     "        GROUP_SINCE[token] = since\n", "        GROUP_SINCE[token] = None\n", BROAD, 'PC14'),
    ('M10b', 'PC5-07 recover_group 이 GROUP_SINCE 를 넣지 않음 (since 늘 None)',
     "            GROUP_SINCE[tok] = since if type(since) is int else None\n", "            GROUP_SINCE[tok] = None\n", BROAD, 'PC05,PC14'),
    ('M11', 'PC5-07 group_members — stat 못 읽음 (OSError) = 확인 불가 → 건너뜀',
     "        except OSError:\n            unsure = True\n            continue\n        if needle in env.split(b'\\0'):",
     "        except OSError:\n            continue\n        if needle in env.split(b'\\0'):", BROAD, 'PC14,GR11'),
    ('M12', 'PC5-03 chain_parent_alive — chain_pid 칸 없음 · 꼴 틀림 = 죽은 것으로 (옛 기록 · 고정물)',
     "    if type(cp) is not int or cp <= 0:\n        return None\n", "    if type(cp) is not int or cp <= 0:\n        return False\n", BROAD, 'PC05'),
    ('M13', 'PC5-06 orphan_cause — 그룹 끝 기록 원인 exception (기다림 중 사슬 예외) → parent_dead',
     "        elif gc == 'exception':\n            c = 'chain_exception'\n", "        elif gc == 'exception':\n            c = 'parent_dead'\n", BROAD, 'PC09'),
    ('M14', 'PC5-06 stop_cause — 멈춤 CHAIN_EXCEPTION 가지 뺌 (→ check · gate)',
     "    if code == CHAIN_EXCEPTION:\n        return 'chain_exception'\n", "", BROAD, 'PC10'),
    ('M15', 'PC5-06 ② 사슬 예외 — 요약 · 결과 줄 없이 다시 올림 (예측 단계 · P06c 의 예측 쪽)',
     "        chain_exc = chain_exception_record(s, e)\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    sname = 'predict_summary.json'",
     "        raise\n    if a.dry_run and not ran:\n        return 3\n    out.mkdir(parents=True, exist_ok=True)\n"
     "    sname = 'predict_summary.json'", BROAD, 'PC10'),
    ('M16', '대조 (C2b 가드) — run_in_group 끝 기록 확인 칸을 늘 True (남은 표지 · 못 읽음 무시 · 잡혀야 정상)',
     "        end = {'schema': GROUP_SCHEMA, 'name': name, 'token': token, 'rc': rc, 'cause': cause, 'signal': (signal_name(sig) if sig else None),\n"
     "               'confirmed': bool(confirmed),",
     "        end = {'schema': GROUP_SCHEMA, 'name': name, 'token': token, 'rc': rc, 'cause': cause, 'signal': (signal_name(sig) if sig else None),\n"
     "               'confirmed': True,", BROAD, 'GR10,GR11,AL13'),
]


def load_pc5():
    spec = importlib.util.spec_from_file_location('mutate_pc5', PC5)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = []
    for mid, why, old, new, only in m.M:
        out.append((mid, why, old, new, only, only))
    return out


FAIL_RE = re.compile(r'^\s*FAIL\s+(\S+)\s+(.*)$')


def run_one(tree, mid, only, env, logd):
    t0 = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                       capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    fails = []
    for ln in p.stdout.splitlines():
        m = FAIL_RE.match(ln)
        if m:
            fails.append({'cid': m.group(1), 'line': m.group(2)[:900]})
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, tree, outp, logd = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    group = sys.argv[5]
    only_override = sys.argv[6] if len(sys.argv) > 6 else None
    logd.mkdir(parents=True, exist_ok=True)
    allm = load_pc5() + NEW
    if group == 'pc5':
        todo = load_pc5()
    elif group == 'new':
        todo = list(NEW)
    else:
        pick = set(group.split(','))
        todo = [m for m in allm if m[0] in pick]
        if 'BASE' in pick:
            todo = [('BASE', '변이 없음', None, None, only_override or BROAD, '')] + todo
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    res = json.loads(outp.read_text(encoding='utf-8')) if outp.exists() else []
    done = {(r['id'], r['only']) for r in res}
    try:
        for mid, why, old, new, only, intended in todo:
            only = only_override or only
            if (mid, only) in done:
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
                dst.write_text(src.replace(old, new, 1), encoding='utf-8')
            rc, summary, fails, sec = run_one(tree, f'{mid}__{only.replace(",", "+")}', only, env, logd)
            inten = [x for x in intended.split(',') if x]
            hit = sorted({f['cid'] for f in fails if any(f['cid'].startswith(x) for x in inten)})
            exc = sorted({f['cid'] for f in fails if re.search(r'\b(NameError|SyntaxError|ImportError|AttributeError|IndentationError)\b', f['line'])})
            res.append({'id': mid, 'why': why, 'only': only, 'intended': intended, 'rc': rc, 'killed': rc != 0 if old is not None else None,
                        'summary': summary, 'fails': fails, 'intended_hit': hit, 'exception_fails': exc, 'seconds': sec})
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            state = ('killed' if rc else 'SURVIVED') if old is not None else ('BASE-FAIL' if rc else 'BASE-OK')
            print(mid, only, state, summary, 'fails=', [f['cid'] for f in fails], flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
