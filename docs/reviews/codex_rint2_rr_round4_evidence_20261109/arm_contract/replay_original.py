"""Replay original RR3 probe, then invert only its two bug-existence asserts."""
from pathlib import Path
import difflib, hashlib, json, os, subprocess, sys
HERE=Path(__file__).resolve().parent
REPO=Path(os.environ.get('RINT_REVIEW_REPO',str(HERE.parent/'package'/'repo'))).resolve()
SOURCE=REPO/'docs/reviews/codex_rint2_rr_round3_evidence_20261108/pc12_attack/probe_pc12_independent.py'
raw=SOURCE.read_bytes(); txt=raw.decode('utf-8'); new=txt
replacements={
    "assert ledger_rows[1]['attempt_order_problem'] is None":
    "assert ledger_rows[1]['attempt_order_problem'][0] == 'RESUME_NOT_ALLOWED'",
    "assert before['resume_ok'] is False and after['resume_ok'] is True and problem is None":
    "assert before['resume_ok'] is False and after['resume_ok'] is False and 'file_ids' in problem",
}
for old,replacement in replacements.items():
    assert new.count(old)==1
    new=new.replace(old,replacement)
(HERE/'closure_oracle.diff').write_text(''.join(difflib.unified_diff(txt.splitlines(True),new.splitlines(True),fromfile='original',tofile='closure_oracle')),encoding='utf-8')
rows=[]
for name,content in [('original_replay',raw),('closure_replay',new.encode('utf-8'))]:
    out=HERE/name; out.mkdir(exist_ok=True)
    script=out/'probe.py';script.write_bytes(content)
    r=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(script)],env=dict(os.environ,RINT_REVIEW_REPO=str(REPO)),capture_output=True)
    (out/'stdout.log').write_bytes(r.stdout);(out/'stderr.log').write_bytes(r.stderr)
    rows.append({'name':name,'rc':r.returncode,'sha256':hashlib.sha256(content).hexdigest()})
(HERE/'replay_results.json').write_text(json.dumps({'original_source_sha256':hashlib.sha256(raw).hexdigest(),
      'target_pin':'1f9f3607eb2f0118d322eeff780bba6eb17b85a2',
      'note':'The original result pin labels round3; source_sha256 is the actual round4 source.',
      'runs':rows},indent=2),encoding='utf-8')
print(json.dumps(rows))
assert rows[0]['rc']==1 and rows[1]['rc']==0
