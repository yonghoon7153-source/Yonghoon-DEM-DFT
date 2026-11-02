#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이 결과 JSON (mutate_pc6.py) + 변이마다 화면 로그 → 요약 JSON (리포에 남길 작은 판) — 변이 · 접두 · 잡힘 · 실패 검사 · 사유 (검사 제목 뒤 글 앞
400 자) · 초.

  python3 mut_summary.py <원 트리> <로그 폴더> <출력 json> <결과 json …>
"""
import json
import sys
from pathlib import Path

wt, logd, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(wt / 'scripts'))
import test_rint_r_chain as TM  # noqa: E402

titles = {cid: title for cid, title, _fn in TM.CHECKS}
rows = []
for jp in sys.argv[4:]:
    for r in json.load(open(jp, encoding='utf-8')):
        log = logd / f"{r['id']}__{r['only'].replace(',', '+')}.log"
        txt = log.read_text(encoding='utf-8') if log.exists() else ''
        fails = []
        for ln in txt.splitlines():
            s = ln.strip()
            if not s.startswith('FAIL '):
                continue
            cid = s.split()[1]
            t = titles.get(cid, '')
            rest = s[len('FAIL  ' + cid + ' '):] if s.startswith('FAIL  ' + cid + ' ') else s
            why = rest[len(t):].strip() if t and rest.startswith(t) else rest[-400:]
            fails.append({'cid': cid, 'why': why[:400]})
        rows.append({'id': r['id'], 'guard': r.get('why'), 'only': r['only'], 'killed': r.get('killed'), 'summary': r.get('summary'),
                     'fails': fails, 'seconds': r.get('seconds')})
outp.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(rows), 'rows →', outp)
