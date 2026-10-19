"""읽기 전용 — 이 트리의 실제 등록 영수증 · 등록 값 · §3 글을 JSON 으로 (트리 경로는 <TREE> 로 바꿈).  argv = 트리 · 출력."""
import contextlib, io, json, os, sys
from pathlib import Path
TREE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
os.chdir(TREE); sys.path[:0] = [str(TREE / 'scripts'), str(TREE / 'webapp')]; sys.dont_write_bytecode = True
import supp20_input_receipt as sr  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    r = sr.receipt()
v, p = sr.registration_values()
s3 = sr._md_section(Path(sr.REG_DOC).read_text(encoding='utf-8'), 3)[0]
txt = json.dumps({'receipt': r, 'values': v, 'probs': p, 's3': s3}, ensure_ascii=False, indent=1, sort_keys=True, default=str).replace(str(TREE), '<TREE>')
OUT.write_text(txt, encoding='utf-8')
print(r['rc'], [c['id'] for c in r['checks'] if not c['ok']])
