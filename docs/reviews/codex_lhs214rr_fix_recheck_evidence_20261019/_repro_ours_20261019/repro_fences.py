"""읽기 전용 — Codex 10-19 등록 파서 반례 (receipt_fence_matrix.json · 114 문서) 를 우리 트리 코드로 다시 판정.
python3 -B repro_fences.py <우리 트리> <반입 증거 폴더> <out.json>"""
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
M = json.loads((EV / 'evidence/receipt_fence_matrix.json').read_text(encoding='utf-8'))
fp_now = sr.NP.code_fp(sr.NP.code_hashes())
rows, diff = [], []
for c in M['cases']:
    p = EV / 'evidence/receipt_fence_cases' / (c['name'] + '.md')
    txt = p.read_text(encoding='utf-8')
    body, why = sr._md_section(txt, 3)
    cm_active = len(c['commonmark_active_h2']) == 1
    ours = dict(name=c['name'], parser_accept=body is not None, parser_reason=why, commonmark_active=cm_active,
                heading_mismatch=(body is not None) != cm_active)
    if 'receipt_rc' in c:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rec = sr.receipt(reg_doc=str(p))
        ours.update(receipt_rc=rec['rc'], bad=[k['id'] for k in rec['checks'] if not k['ok']], code_fp=rec['registration']['values']['code_fp'])
    for k in ('parser_accept', 'parser_reason', 'heading_mismatch', 'receipt_rc', 'bad', 'code_fp'):
        if k in c and c[k] != ours.get(k):
            diff.append((c['name'], k, c[k], ours.get(k)))
    rows.append(ours)
res = dict(tree=str(TREE), code_fp_now=fp_now, total=len(rows), mismatches=sum(r['heading_mismatch'] for r in rows),
           mismatch_rc0=sum(1 for r in rows if r['heading_mismatch'] and r.get('receipt_rc') == 0),
           codex_total=M['total'], codex_mismatches=M['mismatches'], differences_vs_codex=diff, cases=rows)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in res.items() if k != 'cases'}, ensure_ascii=False)[:1500])
