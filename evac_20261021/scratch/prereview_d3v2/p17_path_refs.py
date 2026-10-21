#!/usr/bin/env python3
"""PRE-D3V2 탐침 17 — 요청서 · 설계 v2 의 백틱 경로 (docs/ · scripts/ · dem_scripts/ · webapp/) 가 HEAD 작업 트리에 있는가.
재실행: python3 -I p17_path_refs.py"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

docs = ['docs/reviews/codex_mixer_d3_design_request_20261021.md',
        'docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261021.md']
pat = re.compile(r'`((?:docs|scripts|dem_scripts|webapp)/[^`\s]+)`')
res = {}
for d in docs:
    txt = open(os.path.join(pcommon.REPO, d), encoding='utf-8').read()
    paths = sorted(set(pat.findall(txt)))
    miss = [p for p in paths if not os.path.exists(os.path.join(pcommon.REPO, p.rstrip('/')))]
    res[d] = dict(n_paths=len(paths), missing=miss)
pcommon.dump('p17_path_refs.json', res)
for d, v in res.items():
    print(d, '경로', v['n_paths'], '· 없는 것', v['missing'])
