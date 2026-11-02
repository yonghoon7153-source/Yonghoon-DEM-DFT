#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② PC7 고침 (11-02 · author 11-02 approved PC7 fix) — 새 가드마다 그 가드를 끄는 변이 → 시험이 잡나.  사전 공격 7 회차 변이 틀
(preattack7/probes/mutate_pc7.py) 과 같은 꼴 (사본 트리 · 변이마다 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 옛 글 (정확히 한 번) 을 바꾼 뒤
`scripts/test_rint_r_chain.py --only <접두>` · rc ≠ 0 = 잡힘 · 'BASE' = 변이 없음).  값 · σ 없음.

  python3 mutate_pc7fix.py <원 트리> <사본 트리 바탕 (없으면 만든다)> <결과 json> <로그 폴더> [id,…]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

#: (id, 끈 가드, 옛 글 (정확히 한 번), 새 글, 시험 접두)
MUTS = [
    # PC7-01 — 두 번째 입구 · 시작 기록 · 원장 해석 · recover 대조
    ('F01', 'PC7-01 두 번째 입구 거부 끔 (시작 기록이 있어도 들어감)',
     "        s0 = st['starts'].get(n)\n        if s0 is not None:\n",
     "        s0 = st['starts'].get(n)\n        if False:\n", 'PE01'),
    ('F02', 'PC7-01 시작 기록을 커밋하지 않음 (덧붙임 · raw 갱신 둘 다 뺌)',
     "    try:\n        ledger_append(repo, start, f'rint-r attempt {n} start {e[\"target\"]} {e[\"machine\"]}', expect=raw)\n",
     "    try:\n        pass\n", 'PE01,AL01'),
    ('F03', 'PC7-01 두 번째 입구 거부 = 같은 기계 신원일 때만',
     "        s0 = st['starts'].get(n)\n        if s0 is not None:\n",
     "        s0 = st['starts'].get(n)\n        if s0 is not None and s0['host'] == host_ident():\n", 'PE01'),
    ('F04', 'PC7-01 두 번째 입구 거부 = 같은 바탕일 때만',
     "        s0 = st['starts'].get(n)\n        if s0 is not None:\n",
     "        s0 = st['starts'].get(n)\n        if s0 is not None and s0['base'] == str(base.resolve()):\n", 'PE01'),
    ('F05', 'PC7-01 원장 해석 — 같은 번호 시작 기록 둘 받음',
     "            if n in st['starts']:\n                bad(", "            if False:\n                bad(", 'PE01p'),
    ('F06', 'PC7-01 원장 해석 — 결과 줄 뒤 시작 기록 받음',
     "            if n in st['results']:\n                bad(f'항목 {n} 의 시작 기록이 결과 줄 뒤에 있다",
     "            if False:\n                bad(f'항목 {n} 의 시작 기록이 결과 줄 뒤에 있다", 'PE01p'),
    ('F07', 'PC7-01 원장 해석 — 항목 없는 번호의 시작 기록 받음',
     "            if type(n) is not int or n not in st['entries']:\n                bad(f'{i + 1} 째 줄 시작 기록의 항목",
     "            if type(n) is not int:\n                bad(f'{i + 1} 째 줄 시작 기록의 항목", 'PE01p'),
    ('F08', 'PC7-01 시작 기록 꼴 — 폴더 이름 대조 뺌',
     "    if s['folder'] != f'attempt_{s[\"n\"]}':\n", "    if False:\n", 'PE01p'),
    ('F09', 'PC7-01 시작 기록 꼴 — 바탕 절대 경로 대조 뺌',
     "    if not (isinstance(b, str) and b and os.path.isabs(b) and '\\0' not in b):\n", "    if not isinstance(b, str):\n", 'PE01p'),
    ('F10', 'PC7-01 시작 기록 꼴 — 기계 신원 꼴 대조 뺌',
     "    if not (isinstance(h, dict) and set(h) == START_HOST_KEYS and all(v is None or isinstance(v, str) for v in h.values())):\n",
     "    if False:\n", 'PE01p'),
    ('F11', 'PC7-01 recover — 결과 줄 폴더 · 요약 sha 대조 뺌',
     "                if r0['folder'] != f.name or dg != r0['folder_sha256']:\n", "                if False:\n", 'PE01'),
    ('F12', 'PC7-01 recover — 시작 기록 바탕 대조 뺌',
     "            if s0 is not None and s0['base'] != fb:\n", "            if False:\n", 'PE01'),
    ('F13', 'PC7-01 시작 기록 바탕 = resolve 안 함 (str(base))',
     "    start = {'kind': 'start', 'n': n, 'base': str(base.resolve()),", "    start = {'kind': 'start', 'n': n, 'base': str(base),", 'PE01,AL01'),
    ('F14', 'PC7-01 시작 기록을 못 써도 러너로 감 (rc 3 대신 계속)',
     "                                                   f'--ledger {repo} 뒤 다음 시도 (★ 11-02 PC7-01)'))\n        return 3\n"
     "    raw = raw + ledger_line(start)",
     "                                                   f'--ledger {repo} 뒤 다음 시도 (★ 11-02 PC7-01)'))\n        pass\n"
     "    raw = raw + ledger_line(start)", 'PE01'),
    # PC7-02 — 찾은 폴더 엄격 · 예외
    ('G01', 'PC7-02 attempt.json 없는 · 꼴 틀린 · 링크 찾은 폴더 = 건너뜀 (옛 너그러움 · K09 의 반대)',
     "            a = read_attempt(p)\n            if a is None:\n                if r is not None",
     "            a = read_attempt(p)\n            if a is None:\n                continue\n                if r is not None", 'PE02,PD12u'),
    ('G02', 'PC7-02 예외에서 옆 거부 기록 대조 뺌',
     "                if r is not None and r.get('status') == 'rejected' and (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():\n",
     "                if r is not None and r.get('status') == 'rejected':\n", 'PE02,PD12u'),
    ('G03', 'PC7-02 예외에서 결과 줄 rejected 대조 뺌',
     "                if r is not None and r.get('status') == 'rejected' and (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():\n",
     "                if (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():\n", 'PE02,PD12u'),
    ('G04', 'PC7-02 옆 거부 기록 파일 건너뜀 뺌 (파일도 read_attempt)',
     "            if not Path(p).is_dir():\n                continue                                      # 옆 거부 기록 파일",
     "            if False:\n                continue                                      # 옆 거부 기록 파일", 'PE02,PD12u,AL07,AL12'),
    # PC7-03 — recover 길 chain_end 원인 exception
    ('H01', 'PC7-03 recover 길에서 chain_end 원인 표 안 봄 (옛)',
     "            c = chain_end_fixed(er) or words_cause(", "            c = None or words_cause(", 'PE03'),
    ('H02', 'PC7-03 같은 표를 비움 (by chain exception 도 표 밖)',
     "CHAIN_END_FIXED = {'exception': 'chain_exception'}\n", "CHAIN_END_FIXED = {}\n", 'PE03,PC10,PD11p'),
    # PC7-04 — 표지 · 이름 대조
    ('J01', 'PC7-04 표지 대조 뺌',
     "        if prev.get('token') != tok or prev.get('name') != lname:\n", "        if prev.get('name') != lname:\n", 'PE04'),
    ('J02', 'PC7-04 이름 대조 뺌',
     "        if prev.get('token') != tok or prev.get('name') != lname:\n", "        if prev.get('token') != tok:\n", 'PE04'),
    ('J03', 'PC7-04 다르면 chain_end 만 버리고 끝 기록은 씀 (미확인으로 두지 않음)',
     "    if other is not None:                                  # ★ 11-02 PC7-04", "    if False:                                  # ★ 11-02 PC7-04", 'PE04'),
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
