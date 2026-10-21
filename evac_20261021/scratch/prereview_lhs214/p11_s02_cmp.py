#!/usr/bin/env python3
"""P11 — S02 탐침 HEAD 재실행 출력 ↔ 10-20 우리 재현 기록 (같은 탐침 사본 · 34713ac96 트리) 항목별 비교 (seconds 키 제외).
재실행: python3 -I p11_s02_cmp.py <worktree> <s02_dir>"""
import json, sys
from pathlib import Path
WT, D = Path(sys.argv[1]), Path(sys.argv[2])
REC = WT / 'docs/reviews/codex_lhs214cx_fix_recheck_evidence_20261020/_repro_ours_20261020/s02_probe'


def items(p):
    out = []
    for ln in p.read_text(encoding='utf-8').splitlines():
        if not ln.strip():
            continue
        o = json.loads(ln)
        o.pop('seconds', None)
        out.append(o)
    return out


res = {}
for m in ('core', 'axis', 'mutants', 'failclosed'):
    a, b = items(D / f'{m}.stdout'), items(REC / f'{m}.stdout')
    res[m] = dict(n_now=len(a), n_rec=len(b), identical=a == b,
                  differing=[(x.get('name'), y.get('name')) for x, y in zip(a, b) if x != y][:5])
print(json.dumps(res, ensure_ascii=False, indent=1))
(D / 'p11_cmp.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
