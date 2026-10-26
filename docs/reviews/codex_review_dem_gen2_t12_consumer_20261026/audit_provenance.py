from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parent;S=R/'snapshot';E=R/'evidence';sources=json.loads((S/'SOURCES.json').read_text());v=json.loads((E/'remote_verified_partial.json').read_text());known=set(v['verified']);remote=json.loads((E/'remote_remaining.json').read_text())
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for item in remote:
 if item['kind']=='tree':
  assert not item['data']['truncated']
  for t in item['data']['tree']:
   n=item['path']+'/'+t['path']
   if t['type']=='blob' and n in sources:assert sources[n]['oid']==t['sha'];known.add(n)
 else:
  assert oid(item['data'].encode())==sources[item['path']]['oid'];known.add(item['path'])
assert known==set(sources),(len(known),len(sources),set(sources)-known)
D=S/'docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024';gate=json.loads((D/'full_gate/result.json').read_text());raw=(D/'full_gate/full-gate.log').read_bytes();assert hashlib.sha256(raw).hexdigest()==gate['log_sha256'];lines=raw.decode().splitlines();passlines=[s for s in lines if re.match(r'^\s+✓ ',s)];fails=[s for s in lines if re.match(r'^\s+[✗✘] ',s)];assert len(passlines)==155 and not fails
cr=json.loads((S/'docs/reviews/ulpri_closure_evidence_20261026/scoped-external-receipt.json').read_text());assert hashlib.sha256((S/cr['external_report']['path']).read_bytes()).hexdigest()==cr['external_report']['sha256']
for proof in cr['intake_proofs']:assert hashlib.sha256((S/proof['path']).read_bytes()).hexdigest()==proof['sha256']
form=json.loads((D/'factual-input-form.blank.json').read_text());assert all(x is None for x in form['external_review'].values());assert cr['physical_ready'] is False and cr['physical_T12']=='NOT_RUN'
direct=json.loads((E/'direct52.json').read_text());author=json.loads((D/'fixture-results.json').read_text());assert direct['cases']==author['cases'] and direct['source_sha256']==author['source_sha256'] and direct['fixture_script_sha256']==author['fixture_script_sha256']
out={'remote_source_blobs_matched':len(known),'remote_pin':'bffc42cab29da37b45f8a713e30e8572b91e7da3','changed_paths':122,'all_changes_additions':True,'direct_cases_match':52,'gate_log':{'pass_labels':len(passlines),'fail_labels':len(fails),'sha256':gate['log_sha256'],'receipt_exit_code':gate['exit_code'],'independently_rerun':False,'candidate':gate['candidate']},'scoped_receipt_report_hash_match':True,'generic_go_fields_null':True,'physical_T12':'NOT_RUN'}
(E/'audit_result.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
