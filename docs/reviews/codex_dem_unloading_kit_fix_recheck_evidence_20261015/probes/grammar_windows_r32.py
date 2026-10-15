"""Diagnose Windows R32 synthetic-file newline failure, without source edits."""
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
KIT = BASE / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(KIT))
import ul_reader as ur
rd = BASE / 'evidence/grammar_r32_newlines'
rd.mkdir(exist_ok=True)
files = {'in.hist_producer.liggghts': '# 합성 생산자 덱\n', 'in.hist_grammar.liggghts': '# 합성 문법 덱\n', 'plate_hist.stl': 'solid x\nendsolid x\n'}
pins = {n: hashlib.sha256(t.encode()).hexdigest() for n, t in files.items()}
vp = ur._mk_gram(str(rd), 'e' * 64, files)
initial = ur.grammar_prereq(vp, 'e' * 64, inputs=pins)
run = Path(vp).parent
byte_facts = {}
for stage, deck in ur.GRAMMAR_STAGES:
    for filename in (deck, 'plate_hist.stl'):
        path = run / stage / filename
        raw = path.read_bytes()
        byte_facts[f'{stage}/{filename}'] = {
            'actual_sha256': hashlib.sha256(raw).hexdigest(), 'expected_lf_sha256': pins[filename],
            'crlf_count': raw.count(b'\r\n'), 'lf_count': raw.count(b'\n'),
            'equals_lf_text_after_crlf_removal': raw.replace(b'\r\n', b'\n') == files[filename].encode(),
        }
        # Only these new synthetic review files; preserve exact source bytes.
        path.write_bytes(files[filename].encode())
after = ur.grammar_prereq(vp, 'e' * 64, inputs=pins)
out = {'source_modified': False, 'initial': {'allowed': initial[0], 'problems': initial[1]},
       'file_bytes': byte_facts, 'after_synthetic_fixture_lf_bytes_only': {'allowed': after[0], 'problems': after[1]},
       'diagnosis': 'R32 expected SHA hashes LF UTF-8 strings, but _mk_gram/_w text writes translate LF to CRLF on Windows; changing only the review fixture deck/STL bytes back to expected LF makes the production prerequisite pass.'}
(BASE / 'evidence/grammar_windows_r32.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if not initial[0] and after[0] and all(x['equals_lf_text_after_crlf_removal'] for x in byte_facts.values()) else 1)
