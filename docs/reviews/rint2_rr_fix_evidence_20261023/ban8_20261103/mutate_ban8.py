#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② BAN8 (11-03 · 1저자 11-03 밤 Q3 · 분산판 v0 ↔ Banerjee 2019 식 8 · 9) — 생산 분산판 규칙을 하나씩 깨는 변이 → 새 시험 BAN8 이 옳은 이유로
실패하나.  E18 변이 틀 (`docs/reviews/rint2_rr_fix_evidence_20261023/e2e_verdict_20261103/mutate_e18.py`) 과 같은 꼴: 사본 트리 (scripts 복사 · docs ·
webapp = 링크) · 변이마다 대상 파일을 원본에서 다시 쓰고 옛 글 (정확히 한 번) 을 바꾼 뒤 `scripts/test_carbon_junction.py --only BAN8` · rc ≠ 0 = 잡힘 ·
'BASE' = 변이 없음.  끝나면 대상 파일을 원본으로 되돌린다 (원 트리는 건드리지 않는다).

  python3 mutate_ban8.py <원 트리> <사본 트리 바탕 (없으면 만든다)> <결과 json> <로그 폴더> [id,…]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

CJ = 'scripts/carbon_junction.py'
TJ = 'scripts/test_carbon_junction.py'
#: (id, 대상 파일, 깬 규칙, 옛 글 (정확히 한 번), 새 글, 잡아야 할 검사 (기대 · 보고용))
MUTS = [
    ('M1', CJ, 'lumped — 간선 수 k 를 늘 1 (instance 하나에 총 G · 분산판 없음)',
     '    r = float(Lc) / float(L_par)\n    if not (r > 1.0 + CJUNC_LPAR_RTOL):\n        return 1\n',
     '    return 1\n    r = float(Lc) / float(L_par)\n    if not (r > 1.0 + CJUNC_LPAR_RTOL):\n        return 1\n', 'BAN8 ④'),
    ('M2', CJ, '간선 G 를 k 로 나누지 않음 (총 G 가 k 배)',
     '            g[e] = float(junction_g_code(r)) * float(mult[q]) / float(kk[q])',
     '            g[e] = float(junction_g_code(r)) * float(mult[q])', 'BAN8 ④'),
    ('M3', CJ, '등분 칸 가운데 → 칸 시작점 (t = j·L/k)',
     '        t = (j + 0.5) * L / k\n', '        t = j * L / k\n', 'BAN8 ②'),
    ('T1', TJ, '시험 쪽 — 같은 두 섬유에 Eq. 9 (R̄sh2 0) 를 기대값으로 (식 고르기 판별력)',
     '        w8 = _ban8_eq(q, 1.0) * rp * L\n        tol = _ban_tol(m, rj)\n',
     '        w8 = _ban8_eq(q, 0.0) * rp * L\n        tol = _ban_tol(m, rj)\n', 'BAN8 ④'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(BAN8 \S+)\s+(.*)$')


def make_tree(wt, base):
    tree = base / 'tree'
    if tree.exists():
        return tree
    tree.mkdir(parents=True)
    shutil.copytree(wt / 'scripts', tree / 'scripts', symlinks=True, ignore=shutil.ignore_patterns('__pycache__'))
    for nm in ('docs', 'webapp'):
        (tree / nm).symlink_to(wt / nm, target_is_directory=True)
    return tree


def run_one(tree, mid, env, logd):
    t0 = time.time()
    p = subprocess.run([sys.executable, str(tree / TJ), '--only', 'BAN8'], capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('== test_carbon_junction:')]
    fails = [m.group(1) for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, base, outp, logd = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), Path(sys.argv[4])
    pick = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    logd.mkdir(parents=True, exist_ok=True)
    tree = make_tree(wt, base)
    srcs = {f: (wt / f).read_text(encoding='utf-8') for f in (CJ, TJ)}
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    todo = [('BASE', None, '변이 없음', None, None, '')] + MUTS
    if pick:
        todo = [m for m in todo if m[0] in pick]
    res = []
    try:
        for mid, tgt, why, old, new, want in todo:
            for f, s in srcs.items():
                (tree / f).write_text(s, encoding='utf-8')
            if old is not None:
                n = srcs[tgt].count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'error': f'옛 글 {n} 번'})
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                mutated = srcs[tgt].replace(old, new, 1)
                compile(mutated, tgt, 'exec')
                (tree / tgt).write_text(mutated, encoding='utf-8')
            rc, tail, fails, sec = run_one(tree, mid, env, logd)
            hit = sorted({f.split(' ')[1] for f in fails})
            r = {'id': mid, 'target': tgt, 'why': why, 'rc': rc, 'killed': (rc != 0) if old is not None else None, 'want': want or None,
                 'want_hit': (any(f.startswith(want) for f in fails)) if want else None, 'tail': tail, 'failed_checks': hit,
                 'n_fail_lines': len(fails), 'seconds': sec}
            res.append(r)
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            print(mid, 'rc', rc, tail, hit, f'{sec}s', flush=True)
    finally:
        for f, s in srcs.items():
            (tree / f).write_text(s, encoding='utf-8')


if __name__ == '__main__':
    main()
