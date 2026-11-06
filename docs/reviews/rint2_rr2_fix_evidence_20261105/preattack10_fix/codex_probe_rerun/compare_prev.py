"""Codex 회차 ② 탐침 다시 돌리기 — 이전 기록 (`docs/reviews/rint2_rr2_fix_evidence_20261105/codex_probe_rerun/compare.json` = f5b00a838 판) ↔ 이 고침 뒤 (같은 폴더의
compare.json) 칸마다 대조 (tested_sha256 · probe_tail 의 시각 · 경로 칸은 판이 달라 다르다 = 보고만).
  python3 -I compare_prev.py <이전 compare.json> <이번 compare.json>"""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'))
b = json.load(open(sys.argv[2], encoding='utf-8'))
out = {}
for k in sorted(set(a) | set(b)):
    out[k] = 'same' if a.get(k) == b.get(k) else 'DIFF'
print(json.dumps(out, ensure_ascii=False, indent=1))
print('rows_differ (prev):', [d['name'] for d in a['results']['rows_differ']])
print('rows_differ (now) :', [d['name'] for d in b['results']['rows_differ']])
print('results (prev/now):', a['results']['ours'], a['results']['codex'], '/', b['results']['ours'], b['results']['codex'])
print('tested_sha256 now :', b['tested_sha256'])
