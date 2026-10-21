#!/usr/bin/env python3
"""P08 — 가벼운 대조: 묶음 §2 #14–#19 sha256 · 두 등록 문서를 바꾼 커밋 · 비준 전 문서의 영수증 (요청서 Q1 '비준 전 문서는 rc 1 [D1]') ·
환경 판 · 전이 닫힘 · 지연 import · fork (요청서 Q2 · 묶음 §2 #4–#6).  읽기 전용 (등록 사본은 이 탐침 폴더에).
재실행: cd <worktree> && python3 -I p08_light.py <worktree> <out.json>"""
import json, platform, subprocess, sys, tempfile
from pathlib import Path
WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(WT / 'scripts'))
import numpy, scipy, networkx                  # noqa: E402
import run_network_194_parallel as N           # noqa: E402
import supp20_input_receipt as S               # noqa: E402


def git(*a):
    return subprocess.run(['git', *a], cwd=WT, capture_output=True, text=True).stdout


res = dict(env=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__, networkx=networkx.__version__))
pkg = {'scripts/lhs_design_dataset.py': 'd1815155142e909200053c2d8e9de8c0a88c2dc6d3d9462ad18614a42845e1f0',
       'scripts/g2_network_reread.py': '0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8',
       'scripts/lhs_release_build.py': '3096e33fd0f1953363bcde251a77368366a0568c923447111a48a873ad4a1383',
       'scripts/run_network_194_parallel.py': 'f4048aca55b912628278dbdd7b184ac449723736cd3f4f5cdc7eeca31294921a',
       'scripts/wsl_network_smoke.py': 'feb3e84b9c01d2dee28a158fbbd179e57a4c947325181c276d66d2cec1831b11'}
res['pkg_sha256_same'] = {f: N.sha256_file(N.ROOT / f) == h for f, h in pkg.items()}
res['handover_files'] = list(N.HANDOVER_FILES)
res['doc_commits_34713..HEAD'] = {d: git('log', '--format=%h %s', '34713ac96..HEAD', '--', d).strip().split('\n')
                                  for d in ('docs/reviews/lhs_network_batch_registration_20261007_g2.md', 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md')}
res['tool_commits_34713..HEAD'] = git('log', '--format=%h %s', '34713ac96..HEAD', '--', 'scripts/supp20_input_receipt.py').strip().split('\n')
# 비준 전 보충 문서 사본으로 영수증 (컨테이너 범위)
pre = git('show', 'fe23f2b83:docs/reviews/lhs_network_batch_registration_20261012_supp20.md')
with tempfile.TemporaryDirectory(dir=str(OUT.parent)) as td:
    p = Path(td) / 'pre_supp.md'
    p.write_text(pre, encoding='utf-8')
    r = S.receipt(reg_doc=str(p))
    v, probs = S.registration_values(reg_doc=str(p))
res['pre_doc_receipt'] = dict(rc=r['rc'], bad=sorted(c['id'] for c in r['checks'] if not c['ok']), n=len(r['checks']),
                              D1=next(c['detail'] for c in r['checks'] if c['id'] == 'D1'), values=dict(code_fp=v.get('code_fp'), pending=v.get('code_fp_pending')), probs=probs)
c = N.code_dependency_closure(); z = N.lazy_import_census()
res['closure'] = dict(n=len(c['files']), outside=[f for f in c['files'] if f not in N.CODE_FILES], errors=c.get('errors'))
res['lazy'] = dict(n=len(z['lazy']), unclassified=z['unclassified'], stale=z['stale'])
res['fork'] = N.fork_census()
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:6000])
