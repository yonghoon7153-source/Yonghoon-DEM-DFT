"""동치 변이 기록 (사전 공격 14 고침) — 목록 밖으로 뺀 변이를 같은 뿌리 · 같은 시험 (`--only PA14,PA13`) 으로 돌려 놓침을 기록한다 (뜻이 같아 어떤 입력도 못 가름).
  X01 = conv_ok 사유의 cg_resid `_show` → repr — 그 자리 cg_resid 는 바로 위 `_num` 을 이미 지난 값 (float 로 바뀌는 유한 수) 이라 `_show` = repr.
쓰임: python3 mutate_pa14_equiv.py <작업 트리> <결과 폴더>"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mktree import make_tree  # noqa: E402

WT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
ORIG = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
TEST = WT / 'scripts' / 'test_rint_r_chain.py'
EQUIV = [('X01_show_resid_conv_repr', "· cg_resid {_show(r)} (positive = 수렴 계약 · {why})'", "· cg_resid {r!r} (positive = 수렴 계약 · {why})'")]
res = {}
for nm, old, new in EQUIV:
    n = ORIG.count(old)
    if n != 1:
        res[nm] = ('SKIP', f'old occurs {n}', [])
        print(nm, res[nm], flush=True)
        continue
    src = OUT / 'srcs' / f'{nm}.py'
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(ORIG.replace(old, new), encoding='utf-8')
    root, tmp = OUT / 'roots' / nm, OUT / 'tmp' / nm
    make_tree(WT, root, src, TEST)
    tmp.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(root / 'scripts' / 'test_rint_r_chain.py'), '--only', 'PA14,PA13'], cwd=str(tmp),
                       env=dict(os.environ, TMPDIR=str(tmp)), capture_output=True, text=True, timeout=1800)
    fails = re.findall(r'^  FAIL  (\S+)', r.stdout, re.M)
    summ = [ln for ln in r.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    shutil.rmtree(root, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    res[nm] = ('CAUGHT' if fails else 'MISSED (동치)', summ[-1] if summ else r.stdout[-300:], fails)
    print(nm, *res[nm], flush=True)
(OUT / 'mutation_equiv_results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
