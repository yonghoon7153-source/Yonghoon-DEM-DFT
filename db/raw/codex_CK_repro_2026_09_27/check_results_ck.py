"""Assert the recorded CK review outcomes; no scientific calculation."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
read=lambda n:json.loads((p/n).read_text(encoding='utf-8'))
r=read('pack_cj_results.json')
skip={'positive','recovery','empty_run','windows_bsdtar','post_promotion_cleanup_error','unchanged_source'}
cases={k:v for k,v in r.items() if k not in skip}
assert len(cases)==17
for k,v in cases.items():
    assert v['rc']==4 and not v['success_message'] and not v['parts_present'],k
    if k=='second_mv_error': assert v['sha_check_rc']!=0 and not v['old_pair_preserved'],k
    else: assert v['old_pair_preserved'],k
for k in ('positive','recovery'):
    assert r[k]['rc']==0 and r[k]['sha_check_rc']==0 and len(r[k]['members'])==25,k
assert r['empty_run']['rc']==0 and len(r['empty_run']['members'])==2
v=r['post_promotion_cleanup_error']
assert v['rc']==0 and v['sha_check_rc']==0 and '⚠' in v['log']
meta=read('metadata_ci.json')
assert len(meta['declared_hashes'])==17 and all(meta['declared_hashes'].values())
assert meta['generated_runner_matches'] and meta['tool_hash_matches']
assert meta['cg_comparison']=={'inputs':90,'changed_inputs':[],'d3_changed':[]}
assert len(meta['geometry'])==18
assert all(x['source_sha_ok'] and x['order_ok'] and x['max_pos_diff_A']<1e-8 and x['max_cell_diff_A']<1e-8 for x in meta['geometry'])
c=read('results_ci.json')
assert c['positive_cli']['rc']==0 and c['positive_sealed']['rc']==0
for k in ('pilot_replaced_id','pilot_same_id_changed_output'):
    assert c[k]['status']=='PILOT_NOT_SEALED' and c[k]['cli']['rc']==3,k
assert c['runner_positive']['rc']==0 and c['runner_sha_check']['rc']==0
assert c['runner_partial_pp_failure']['result']['rc']==1
s=read('semantic_cj_results.json')
assert s['noentropy_missing_nonpilot']['E_noentropy_eV'] is None
assert s['noentropy_missing_nonpilot']['samples']['③']['mTS_term_J_m2'] is None
assert s['noentropy_zero_nonpilot']['E_noentropy_eV']==0.0
print('CK result assertions PASS (native 194 and mutation 12 are NOT claimed reproduced)')
