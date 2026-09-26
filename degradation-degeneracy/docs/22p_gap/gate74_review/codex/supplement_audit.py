"""Additional read-only evidence collation; no target-module execution."""
from pathlib import Path
import json,hashlib,sys
O=Path(__file__).resolve().parent;D=Path('C:/Users/Administrator/Documents/Codex/g74_20260926/degradation-degeneracy')
sys.path.insert(0,str(O.parents[1]/'work/gate26-pydeps'))
import yaml
sha=lambda b:hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
B=D/'artifacts/grid_fit_v5'
r=yaml.safe_load((D/'docs/22p_gap/receipts/grid_fit_v5.validate.yaml').read_bytes())
s=yaml.safe_load((B/'degeneracy_summary.yaml').read_bytes())
semantic=sha(canon({k:v for k,v in s.items() if k!='_채점원본'}))
assert semantic==next(x for x in r['core']['outputs'] if x['role']=='sealed_summary')['semantic_sha256']
ids={k:sha((D/v).read_bytes())[:16] for k,v in {
 'src_io_sha256':'src/io.py','src_scoring_sha256':'src/scoring.py','archive_bundle_sha256':'tools/archive_bundle.py',
 'make_receipt_sha256':'docs/22p_gap/make_receipt.py','row_projection_sha256':'docs/22p_gap/row_projection.py'}.items()}
assert all(r['core']['identity'][k]==v for k,v in ids.items())
raw=(D/'docs/08_REVIEW_RESPONSE.md').read_bytes();text=raw.decode('utf-8');lines=text.splitlines()
start=next(i for i,x in enumerate(lines) if x.startswith('## §99 '))
dest=O/'reference/docs/08_REVIEW_RESPONSE_sections99_101.txt'
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text('\n'.join(f'{i+1}: {x}' for i,x in enumerate(lines) if i>=start)+'\n',encoding='utf-8')
prior=O.parent/'gate73_review_20260925/GATE73_REVIEW_KO.md'
(O/'reference/GATE73_REVIEW_KO.md').write_bytes(prior.read_bytes())
ledger=yaml.safe_load((D/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes())
c=next(x for x in ledger['cohorts'] if x['cohort_id']=='g18_2026_09_15')
ptr=json.loads((D/'docs/22p_gap/proj_g18/CURRENT').read_bytes())
(O/'reference/docs/22p_gap/proj_g18').mkdir(parents=True,exist_ok=True)
(O/'reference/docs/22p_gap/proj_g18/CURRENT').write_bytes((D/'docs/22p_gap/proj_g18/CURRENT').read_bytes())
out={'sealed_summary_semantic_sha':semantic,'independent_sealed_summary_rehash':True,'rescored_output_rerun':False,
 'receipt_source_file_identities':ids,'source_docs08_sha':sha(raw),'source_docs08_first_line':start+1,
 'prior_gate73_review_sha':sha(prior.read_bytes()),'projection_roster':{'ledger_legs':c['legs'],'policy':c['cross_leg_comparison'],
 'CURRENT_projection_yaml_members':[n for n in ptr['files'] if n.endswith('.projection.yaml')],
 'CURRENT_sha':sha((D/'docs/22p_gap/proj_g18/CURRENT').read_bytes())},
 'authorization_gap':'Same attempt 591c0939: explicit resume refused at 18:18, cache moved then resume started at 18:20. Prior user authorization for the second call not in supplied evidence.',
 'wsl_cause_limit':'VM reboot time reported, not independently measured. OOM/idle/tmux attribution remains report or inference; zero completed feasible conditions is not zero started computations.',
 'suite_results':'20 failed/1859 passed/2 xfailed and smoke rc0 are sender reports, no receiver rerun.'}
with (O/'SUPPLEMENT_AUDIT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(out,ensure_ascii=False))
