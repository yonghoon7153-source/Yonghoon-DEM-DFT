"""Independent model of pinned Bash lines 2084--2104, NOT a Bash execution.
Actual Bash is unavailable in the Windows session (MSYS NtCreateDirectoryObject
denied). No claim of real sbatch, full CLI, or LIGGGHTS execution is made.
"""
from pathlib import Path
import json, hashlib
R=Path(__file__).resolve().parent;O=R/'independent/gate_model';O.mkdir(parents=True,exist_ok=True)
cases=json.loads((R/'independent/gate_probe/results.json').read_text(encoding='utf-8'))
res=[]
for old in cases:
 kind=old['case'];d=R/'independent/gate_probe'/kind
 rec=d/'attempt/main_inputs.sha256'
 def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 same_files=True
 for line in rec.read_text(encoding='utf-8').splitlines():
  want,n=line.split('  ',1)
  # MSYS /c/... is the Windows C:/... fixture path, not a cluster path.
  p=Path(n[1]+':'+n[2:]) if len(n)>3 and n[0]=='/' and n[2]=='/' else Path(n)
  same_files &= h(p)==want
 # Preconditions correspond to the producer's G0--G3 and same-call checks.
 # Tool/helper equality and no other queued job are held fixed in this test.
 same_call_receipt=h(rec)==old['new_call_receipt']
 gate_allows_submit=same_call_receipt and same_files
 want=kind!='changed_after_trial'
 res.append({'case':kind,'same_call_receipt':same_call_receipt,'same_call_files':same_files,
  'gate_allows_submit_MODEL_ONLY':gate_allows_submit,'reviewed_receipt_matches':old['same_as_reviewed'],
  'manual_ack_recorded':False,'model_expected':want,'pass':gate_allows_submit==want,
  'actual_scheduler_calls':0})
(O/'results.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
raise SystemExit(any(not x['pass'] for x in res))
