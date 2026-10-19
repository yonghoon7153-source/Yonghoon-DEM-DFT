"""읽기 전용 — Codex 10-19 (핀 685c2bbdb) 빈 ATX 제목 반례 19 (s01_heading_boundary_cases.json) 를 우리 트리 코드로 다시 판정.
python3 -B repro_headings.py <우리 트리> <묶음 lhs214s_recheck_20261019 폴더> <out.json>"""
import contextlib
import io
import json
import os
import sys
from pathlib import Path
TREE, EV, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
os.chdir(TREE)
sys.path[:0] = [str(TREE / 'scripts'), str(TREE / 'webapp')]
sys.dont_write_bytecode = True
import supp20_input_receipt as sr  # noqa: E402
M = json.loads((EV / 'evidence/s01_heading_boundary_cases.json').read_text(encoding='utf-8'))
rows, diff = [], []
for c in M['rows']:
    p = EV / Path(*c['input'].replace('\\', '/').split('/'))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rec = sr.receipt(reg_doc=str(p))
    ours = dict(rc=rec['rc'], bad=[k['id'] for k in rec['checks'] if not k['ok']], code_fp=rec['registration']['values']['code_fp'])
    ok_oracle = (ours['code_fp'] == c['oracle']['code_fp'])
    rows.append(dict(name=c['name'], ours=ours, codex_actual=c['actual'], oracle_code_fp=c['oracle']['code_fp'], ours_matches_oracle=ok_oracle))
    for k in ('rc', 'bad', 'code_fp'):
        if c['actual'].get(k) != ours.get(k):
            diff.append((c['name'], k, c['actual'].get(k), ours.get(k)))
res = dict(tree=str(TREE), total=len(rows), ours_vs_oracle_mismatch=sum(not r['ours_matches_oracle'] for r in rows),
           codex=dict(total=M['total'], mismatches=M['mismatches'], fail_open=M['fail_open'], false_rejections=M['false_rejections']),
           differences_vs_codex_actual=diff, rows=rows)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, ensure_ascii=False))
