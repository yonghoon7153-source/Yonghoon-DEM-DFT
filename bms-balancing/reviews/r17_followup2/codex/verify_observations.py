"""Check that diagnostic observations are complete, not just that the runner returned 0."""
import json, math, pathlib
H=pathlib.Path(__file__).resolve().parent
r=json.loads((H/'REPRO_RESULTS.json').read_text(encoding='utf-8'))['cases']
expected={
 'width_positive':0,'width_seed_negative':2,'width_meta_version_negative':2,
 'width_body_version':2,'width_body_tol':2,'width_body_cell':2,'width_body_run':2,
 'width_body_mixed_version':2,'width_fractional_cycles':2,'width_null_identity':2,'width_null_settings':2,
 'width_row_scale_seed':0,'width_row_n_starts':0,'width_row_scale_mixed':0,
 'width_scale_meta_negative':2,'width_starts_meta_negative':2,
 'width_env_python_only':0,'width_env_null_values':0,'width_env_whitespace':0,
 'width_manifest_whitespace':0,'width_bounds_singleton':0,'width_bounds_nan':0,'width_untyped_width_starts':0,
 'receipt_positive':0,'receipt_null_runtime':3,'receipt_bad_runtime':3,'receipt_bad_materialized':3,
 'receipt_bad_date':3,'receipt_non_digest':3,'receipt_runtime_python_null':0,'receipt_runtime_wrong_keys':0,
 'receipt_materialized_wrong_fields':0,'receipt_missing_runtime_negative':3,
 'gc_control':0,'gc_old_cross_artifact':0,'gc_duplicate':2,'gc_cleanup_escape':2,
 'gc_retained_path_alias':0,'gc_unknown_file':0,'gc_unknown_dir_negative':2}
checks={k:r.get(k,{}).get('rc')==v for k,v in expected.items()}
for k in ['gc_duplicate','gc_cleanup_escape','gc_old_cross_artifact','gc_unknown_dir_negative']:
    checks[k+'_preserved']=r[k]['watched_exists'] is True
for k in ['gc_retained_path_alias','gc_unknown_file']:
    checks[k+'_lost']=r[k]['watched_exists'] is False
for k in ['width_row_scale_seed','width_row_n_starts','width_env_null_values','width_bounds_nan']:
    checks[k+'_identity_claim']='동일 확인' in r[k]['stdout']
for k in ['receipt_runtime_python_null','receipt_runtime_wrong_keys','receipt_materialized_wrong_fields']:
    checks[k+'_verified']=r[k]['verdict']['verified'] is True and r[k]['verdict']['checks']['complete'] is True
checks['infeasible_best_rejected']=r['width_infeasible_best']['exception']=='RuntimeError'
checks['infeasible_best_failed']=r['width_infeasible_best']['published_fields']['width_status']=='failed'
checks['out_of_box_rejected']=r['width_out_of_box_seed']['result']['LAM_PE']['min']>=-16.666667
checks['nan_claim_measured']=r['width_nan_best']['published_fields']['width_status']=='measured'
checks['nan_claim_has_nan']=math.isnan(r['width_nan_best']['published_fields']['LAM_PE_lo'])
checks['content_digest_distinct']=r['package_content_control']['content_distinct'] is True
p=json.loads((H/'PRODUCER_READER_RESULTS.json').read_text(encoding='utf-8'))
checks['real_producer_measured']=p['width_status']==['measured','measured']
checks['real_producer_schema_ok']=p['check_rows']==[]
checks['real_producer_reader_rejects']=p['rc']==2 and '행 0 의 receipt' in p['stderr']
checks['cycle_stripped_control_accepts']=p['control_without_row_cycle']['rc']==0
record={'meaning':'All checks confirm observations, including bugs; NOT product PASS',
        'case_count':len(r),'assertion_count':len(checks),'checks':checks,'all_observations_match':all(checks.values())}
(H/'OBSERVATION_CHECK.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k!='checks'},indent=2))
if not all(checks.values()):
    print([k for k,v in checks.items() if not v]);raise SystemExit(1)
