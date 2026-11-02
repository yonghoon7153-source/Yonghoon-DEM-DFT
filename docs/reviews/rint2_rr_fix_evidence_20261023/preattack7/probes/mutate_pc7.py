#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 7 회차 (11-02 · 대상 0658c0ac6) — 독립 변이 시험.  고친 사람의 변이 틀 (pc6_fix/mutate_pc6fix.py · pc6_13_fix/mutate_pc6_13.py) 을 불러 쓰지 않는다.

  python3 mutate_pc7.py <원 트리> <사본 트리 바탕 (없으면 만든다)> <결과 json> <로그 폴더> [id,…]

사본 트리 = <바탕>/tree (scripts 사본 · docs · webapp 링크 · .gitignore) · 변이마다 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 옛 글 (정확히 한 번)
을 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` (rc ≠ 0 = 잡힘) · 'BASE' = 변이 없음.  값 · σ 없음.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

#: (id, 끈 · 바꾼 가드, 옛 글 (정확히 한 번), 새 글, 시험 접두)
MUTS = [
    # PC6-01 _run_kin · group_members — 이전 회차 변이 틀에 없던 가지 · 보수 쪽 · 결정 동등 후보
    ('K01', 'PC6-01 _run_kin 부모 없음 (st None · hidepid=2 · 사라짐) = 확인 불가로 (보수 쪽 · 지금 = 셈 밖)',
     "        if st is None:\n            return False\n", "        if st is None:\n            return True\n", 'PD01'),
    ('K02', 'PC6-01 _run_kin 부모 칸 못 읽음 (a None) = 확인 불가로 (보수 쪽 · 지금 = 셈 밖)',
     "        if a is None or a <= 1 or a == me:\n            return False\n",
     "        if a is None:\n            return True\n        if a <= 1 or a == me:\n            return False\n", 'PD01'),
    ('K03', 'PC6-01 _run_kin 계보 고리 대조 뺌 (깊이 상한이 같은 답 = 결정 동등 후보)',
     "        if a in seen:\n            return True\n", "", 'PD01'),
    ('K04', 'PC6-01 _run_kin a == me (부른 사슬 자신) = 확인 불가로',
     "        if a is None or a <= 1 or a == me:\n            return False\n",
     "        if a == me:\n            return True\n        if a is None or a <= 1:\n            return False\n", 'PD01'),
    ('K05', 'PC6-01 recover_group 러너 시작 틱 무시 (start None · 세션 번호 다시 쓰임 대조 끔)',
     "                GROUP_RUN[tok] = {'pid': rp, 'start': rs if type(rs) is int else None}\n",
     "                GROUP_RUN[tok] = {'pid': rp, 'start': None}\n", 'PD01'),
    ('K06', 'PC6-01 group_settle scan 이 이번 셈 기록을 지우지 않음 (옛 셈의 표지 프로세스를 죽일 수 있음)',
     "        GROUP_SCAN.pop(token, None)                            # 이번 셈 결과만 (바꿔 끼운 group_members = 기록 없음 → 죽이지 않음)\n", "", 'PD01,PD13'),
    # PC6-09 — 이 항목 판정 칸 하나씩
    ('K07', 'PC6-09 이 항목 판정에서 기계만 뺌',
     "all(own[k] == e[k] for k in ('target', 'machine', 'resume_of'))", "all(own[k] == e[k] for k in ('target', 'resume_of'))", 'PD09'),
    ('K08', 'PC6-09 이 항목 판정에서 재실행 원 시도만 뺌',
     "all(own[k] == e[k] for k in ('target', 'machine', 'resume_of'))", "all(own[k] == e[k] for k in ('target', 'machine'))", 'PD09'),
    # PC6-12 — 고침 방향 확인 (정보 변이: attempt.json 없는 · 꼴 틀린 찾은 폴더 = 사유 → 어느 시험이 지금 너그러움에 기대나)
    ('K09', 'PC6-12 (정보 · 고침 방향) attempt.json 없는 · 꼴 틀린 찾은 시도 폴더 = 사유 (지금 = 건너뜀)',
     "            a = read_attempt(p) if Path(p).is_dir() else None\n            if a is None:\n                continue\n",
     "            a = read_attempt(p) if Path(p).is_dir() else None\n            if a is None:\n                if Path(p).is_dir():\n"
     "                    return f'{Path(p).name}: attempt.json 없음 · 꼴 틀림 (원장 항목 {k} 있음)'\n                continue\n",
     'PD12,PC01,PC12,PC13,AL07,AL12,UM,GR'),
    # PC6-13 — 이전 변이 틀과 다른 자리
    ('K10', 'PC6-13 recover_group chain_end = 옛 끝 기록 by chain 이어도 표지 (token) 대조 없이 — (정보: 지금도 대조 없음) · 대신 rc 칸 뺌',
     "        chain_end = {k: prev.get(k) for k in ('rc', 'cause', 'confirmed', 'ended_utc')}\n",
     "        chain_end = {k: prev.get(k) for k in ('cause', 'confirmed', 'ended_utc')}\n", 'PD13'),
    ('K11', 'PC6-13 stop_cause 그룹 미확인 + 실패 rc = words_keep (자원 낱말도 runner_rc 로)',
     "            return words_cause(txt, 'runner_rc')\n        base = 'group_unconfirmed'\n",
     "            return words_keep(txt, 'runner_rc')\n        base = 'group_unconfirmed'\n", 'PD13'),
    ('K12', 'PC6-13 runner_rc_failed — bool · 실수 = 0 이면 성공으로 (꼴 틀린 값 보수 끔)',
     "    return rc is not None and not (type(rc) is int and rc == 0)\n", "    return rc is not None and rc != 0\n", 'PD13'),
    ('K13', 'PC6-13 _execute 멈춤 문장의 러너 rc 뺌 (화면만)',
     " · 러너 rc {rec[\"rc\"]}) — 그 런의 '", ") — 그 런의 '", 'PD13'),
    # PC6-02 — 라이브러리 표지 하나씩 (표 동등 검사 말고 실경로 · 길 표가 잡나)
    ('K14', 'PC6-02 표지 CUDA error: 뺌',
     "'CUFFT_',\n                    'CUDA error:')", "'CUFFT_')", 'PD02c'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(\S+)\s+(.*)$')


def make_tree(wt, base):
    tree = base / 'tree'
    if tree.exists():
        return tree
    tree.mkdir(parents=True)
    shutil.copytree(wt / 'scripts', tree / 'scripts', symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
    for nm in ('docs', 'webapp'):
        (tree / nm).symlink_to(wt / nm, target_is_directory=True)
    if (wt / '.gitignore').exists():
        shutil.copy2(wt / '.gitignore', tree / '.gitignore')
    return tree


def run_one(tree, mid, only, env, logd):
    t0 = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                       capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    fails = [{'cid': m.group(1), 'line': m.group(2)[-500:]} for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, base, outp, logd = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), Path(sys.argv[4])
    pick = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    logd.mkdir(parents=True, exist_ok=True)
    tree = make_tree(wt, base)
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    todo = [('BASE', '변이 없음', None, None, ','.join(sorted({x for m in MUTS for x in m[4].split(',')})))] + MUTS
    if pick:
        todo = [m for m in todo if m[0] in pick]
    res = json.loads(outp.read_text(encoding='utf-8')) if outp.exists() else []
    done = {r['id'] for r in res}
    try:
        for mid, why, old, new, only in todo:
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
                compile(mutated, 'rint_r_chain.py', 'exec')
                dst.write_text(mutated, encoding='utf-8')
            rc, tail, fails, sec = run_one(tree, mid, only, env, logd)
            r = {'id': mid, 'why': why, 'only': only, 'rc': rc, 'killed': (rc != 0) if old is not None else None, 'tail': tail,
                 'fails': fails, 'seconds': sec}
            res.append(r)
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            print(mid, 'rc', rc, tail, [f['cid'] for f in fails], f'{sec}s', flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
