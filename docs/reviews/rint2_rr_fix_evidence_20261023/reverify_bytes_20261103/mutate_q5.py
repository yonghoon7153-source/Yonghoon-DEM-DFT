#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 다시 판정 보고 바이트 칸 (11-03 밤 · 1저자 Q5 · 원장 RINT2-E01) — 새 가드를 하나씩 끄는 변이 → RV05 · RV06 (가짜 러너 세계 · 빠름) 이 옳은 이유로
실패하나.  E18 · BAN8 변이 틀 (`docs/reviews/rint2_rr_fix_evidence_20261023/e2e_verdict_20261103/mutate_e18.py`) 과 같은 꼴: 사본 트리 (scripts 복사 · docs ·
webapp = 링크) · 변이마다 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 옛 글 (정확히 한 번) 을 바꾼 뒤 `scripts/test_rint_r_chain.py --only RV05,RV06` ·
rc ≠ 0 = 잡힘 · 'BASE' = 변이 없음 · 끝나면 원본으로 되돌린다 (원 트리는 건드리지 않는다).  끝-끝 E18j 는 이 틀 밖 (한 판 ≈ 10 분 · 시험 먼저 기록만).

  python3 mutate_q5.py <원 트리> <사본 트리 바탕 (없으면 만든다)> <결과 json> <로그 폴더> [id,…]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

RR = 'scripts/rint_r_chain.py'
#: (id, 끈 가드, 옛 글 (정확히 한 번), 새 글, 잡아야 할 검사)
MUTS = [
    ('Q1', '까닭을 늘 빈 목록 (다름만 적음)',
     "    view['kinds'] = [x for x in BYTE_DIFF_KINDS if x in k]\n    return view\n", "    view['kinds'] = []\n    return view\n", 'RV05'),
    ('Q2', '보고에 결과 바이트 칸 없음 (옛 v1 꼴)',
     "            'results_bytes': byte_diff_view(old_res, new_res if new_res is not None else (canon_bytes(res) if res is not None else None)),\n",
     '', 'RV06'),
    ('Q3', '칸 순서 대조 끔',
     '    if _key_seq(v0) != _key_seq(v1):\n        k.add(\'key_order\')\n', '', 'RV05'),
    ('Q4', '끝 공백을 줄바꿈으로 (끝 꼴 가르기 하나로)',
     "        if tail.replace(b'\\n', b'') != tail_r.replace(b'\\n', b''):\n            k.add('trailing_whitespace')\n",
     "        if tail.replace(b'\\n', b'') != tail_r.replace(b'\\n', b''):\n            k.add('newline')\n", 'RV05'),
    ('Q5', '화면 까닭 줄 없음',
     "    print(f'  바이트 까닭 — 판정 JSON", "    0 and print(f'  바이트 까닭 — 판정 JSON", 'RV06'),
    ('Q6', '값 다름 먼저 가르기 끔 (값이 달라도 꼴 까닭으로)',
     "    if v0 != v1:                                             # NaN", "    if False:                                                # NaN", 'RV05'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(RV0[56])\b')


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


def run_one(tree, mid, env, logd):
    t0 = time.time()
    p = subprocess.run([sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', 'RV05,RV06'], capture_output=True, text=True,
                       env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    fails = [m.group(1) for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, base, outp, logd = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), Path(sys.argv[4])
    pick = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    logd.mkdir(parents=True, exist_ok=True)
    tree = make_tree(wt, base)
    src = (wt / RR).read_text(encoding='utf-8')
    dst = tree / RR
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    todo = [('BASE', '변이 없음', None, None, '')] + MUTS
    if pick:
        todo = [m for m in todo if m[0] in pick]
    res = []
    try:
        for mid, why, old, new, want in todo:
            if old is None:
                dst.write_text(src, encoding='utf-8')
            else:
                n = src.count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'error': f'옛 글 {n} 번'})
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                mutated = src.replace(old, new, 1)
                compile(mutated, RR, 'exec')
                dst.write_text(mutated, encoding='utf-8')
            rc, tail, fails, sec = run_one(tree, mid, env, logd)
            r = {'id': mid, 'why': why, 'rc': rc, 'killed': (rc != 0) if old is not None else None, 'want': want or None,
                 'want_hit': (want in fails) if want else None, 'tail': tail, 'fails': fails, 'seconds': sec}
            res.append(r)
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            print(mid, 'rc', rc, tail, fails, f'{sec}s', flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
