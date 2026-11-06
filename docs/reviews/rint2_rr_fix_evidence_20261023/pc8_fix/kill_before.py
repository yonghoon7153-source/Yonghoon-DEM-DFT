"""PC8-06 — 사전 공격 8 회차의 생존 변이 M26 · B01 (mutate8.py 의 바로 그 글자) 를 고치기 전 사슬 · 접합 코드 (74150affc) + 새 시험 (PC8 시험 먼저) 사본
트리에 하나씩 넣고 새 시험이 잡는지 → JSON (변이 없는 판 = BASE · 끝나면 원 바이트로 되돌림).

  python3 -I kill_before.py <고치기 전 사본 트리> <출력.json>
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
CASES = [
    ('BASE_RV07', None, None, None, ['scripts/test_rint_r_chain.py', '--only', 'RV05,RV06,RV07']),
    ('M26', 'scripts/rint_r_chain.py', "    if canon_bytes(v0) != new:                               # 값은 같은데",
     "    if False:                               # 값은 같은데", ['scripts/test_rint_r_chain.py', '--only', 'RV05,RV06,RV07']),
    ('BASE_BAN8', None, None, None, ['scripts/test_carbon_junction.py', '--only', 'BAN8']),
    ('B01', 'scripts/carbon_junction.py', "        t = (j + 0.5) * L / k", "        t = (j + 0.25) * L / k", ['scripts/test_carbon_junction.py', '--only', 'BAN8']),
]
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
res = {}
for name, f, old, new, argv in CASES:
    orig = None
    if f is not None:
        orig = (MT / f).read_bytes()
        txt = orig.decode('utf-8')
        if txt.count(old) != 1:
            res[name] = {'error': f'옛 글 {txt.count(old)} 번'}
            continue
        (MT / f).write_bytes(txt.replace(old, new).encode('utf-8'))
    try:
        p = subprocess.run([sys.executable] + argv, cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    finally:
        if orig is not None:
            (MT / f).write_bytes(orig)
    out = p.stdout + p.stderr
    res[name] = {'rc': p.returncode, 'killed': (p.returncode != 0) if f is not None else None,
                 'failed': sorted(set(re.findall(r'^\s*FAIL\s+(\S+(?: \S+)?)', out, re.M)))[:20],
                 'summary': [ln for ln in out.splitlines() if re.search(r'test_rint_r_chain:|== test_carbon_junction', ln)][-1:]}
    print(name, res[name], flush=True)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
