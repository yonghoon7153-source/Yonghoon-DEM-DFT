"""Read-only source review; synthetic receipt fixtures, no preflight/worker/solve.

The real runner builds plans/digests and formats logs; system/raw checks in pf
are synthetic, as in submitted S7. Only separate probe outputs are written.
"""
import contextlib,copy,io,json,sys,types
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'/'receipt_extra';E.mkdir(exist_ok=True)
sys.path.insert(0,str(S/'scripts'))
import supp20_input_receipt as X
N=X.NP
base=X.receipt();reg=base['registration']['values'];dg0=base['recomputed']['input_digest'];plan=X.plan_for()
assert base['rc']==0,base
results={}
def save_result(name,rec):
    results[name]={'rc':rec['rc'],'scope':rec['scope'],'failed':[c['id'] for c in rec['checks'] if not c['ok']],
                   'passed':[c['id'] for c in rec['checks'] if c['ok']]}
    (E/(name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
def log_for(p,stop=(),short='a9422d2e7'):
    pf=dict(cpu=dict(cpu_count=20,cpu_affinity=20),mem=dict(MemTotal_GB=64,MemAvailable_GB=60,SwapFree_GB=0,SwapTotal_GB=0),
      mem_budget_mb=50*1024.0,lanes=20,first_lanes_est_mem_GB=1.0,est_mem_largest_mb=600.0,disk_free_GB=100,disk_need_GB=1,
      est_serial_h=0.5,est_makespan_h=0.1,git=dict(short=short,branch='HEAD',dirty=False,porcelain=[]),
      n_raw_problems=0,generation=dict(generation='g2',problems=[],modes=['hertz','physics','hertz_h12']),
      dependency_closure=dict(files=list(N.CODE_FILES[:5]),errors=[]),lazy_census=dict(n_lazy=3,unclassified=[]),fork_census=[],
      input_digest=N.plan_input_digest(p),warn=[],stop=list(stop))
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):N.print_preflight(pf,p,types.SimpleNamespace(min_free_gb=1.0,network_lock='per-case'),Path('/fixture/root'))
    return buf.getvalue()
def check_log(name,txt):
    path=E/(name+'.log');path.write_text(txt,encoding='utf-8');rec=X.receipt(dry_run_log=str(path));save_result(name,rec);return rec
original=log_for(plan)
check_log('positive_full_log',original)
keep=('코드 ','기대 망 세대','전이 의존','지연 import','fork','입력 지문','원자료 · 메시 문제','⛔')
grep=lambda txt:'\n'.join(ln for ln in txt.splitlines() if any(k in ln for k in keep))+'\n'
check_log('positive_registered_grep',grep(original))
# Actual alternate TSV: change first case's deck_sha256. Same IDs/raw JSON.
ct=Path(plan['cohorts'][0]['cohort']);lines=ct.read_text(encoding='utf-8').splitlines();header=next(ln for ln in lines if ln.startswith('case\t')).split('\t')
ix=header.index('deck_sha256');out=[];changed=False
for ln in lines:
    if ln.startswith('lhss_001\t'):
        fields=ln.split('\t');old=fields[ix];fields[ix]=('0' if old[0]!='0' else '1')+old[1:];ln='\t'.join(fields);changed=True
    out.append(ln)
assert changed
badtsv=E/'alternate_cohort.tsv';badtsv.write_text('\n'.join(out)+'\n',encoding='utf-8')
badplan=X.plan_for(cohort=str(badtsv));baddg=N.plan_input_digest(badplan);badlog=log_for(badplan)
assert baddg['cohort_tsv_sha256']!=dg0['cohort_tsv_sha256']
assert all(baddg[k]==dg0[k] for k in N.INPUT_DIGEST_KEYS if k!='cohort_tsv_sha256')
check_log('wrong_tsv_full_log',badlog)
check_log('wrong_tsv_registered_grep',grep(badlog))
save_result('wrong_tsv_local_positive_rejection',X.receipt(cohort=str(badtsv)))
results['wrong_tsv_comparison']={'correct':dg0['cohort_tsv_sha256'],'wrong':baddg['cohort_tsv_sha256'],
 'registered_grep_byte_identical':grep(original)==grep(badlog),'actual_input_digest_changed':True,'normal_other_digest_fields_equal':True}
# Same producer prints actual observation-off refusal last. Prefix loss hides it.
stop=N.production_observation_problem(dict(plan=plan,observe_imports=False));assert stop
refused=log_for(plan,[stop]);check_log('observation_off_full_log',refused)
prefix=refused.split('  ⚠ Codex 세대 2 재검증 2',1)[0]
check_log('observation_off_truncated_before_stop',prefix)
# Deleting required prerequisite status lines does not fail E5 either.
stripped='\n'.join(ln for ln in original.splitlines() if not any(k in ln for k in X._DRY_TICKS))+'\n'
check_log('missing_three_prerequisite_lines',stripped)
# Correct numerical fingerprint but different launcher checkout identity.
check_log('different_git_short',log_for(plan,short='b429c3c1d'))
def manifest(p,dg,dirname,**over):
    hashes=N.code_hashes();m=dict(schema=N.SCHEMA,launch_format=N.LAUNCH_FORMAT,plan=p,input_digest=dg,code_hashes=hashes,
       code_dependency_closure=list(N.CODE_FILES),handover_code_hashes={rel:N.sha256_file(N.ROOT/rel) for rel in N.HANDOVER_FILES},
       git=dict(sha='a9422d2e772f28417a6e0a5167aaab8d987bf27a',short='a9422d2e7',dirty=False),observe_imports=True,import_obs_run_id='cd'*16,
       generation_probe=dict(generation='g2',problems=[]),**{N.GEN_KEY:'g2'},
       seal=dict(schema=N.LAUNCH_SEAL_SCHEMA,launch_format=N.LAUNCH_FORMAT,code_fp=N.code_fp(hashes),files=len(hashes),**{N.GEN_KEY:'g2'}))
    m.update(over);p_=E/dirname/'manifest.json';p_.parent.mkdir(exist_ok=True);p_.write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8');return str(p_)
p194=N.build_plan(['lhs','lhsx'],N.cohort_specs(types.SimpleNamespace()),(),'cost');dg194=N.plan_input_digest(p194)
ms=manifest(plan,dg0,'supp');mp=manifest(p194,dg194,'primary')
save_result('positive_two_manifests',X.receipt(manifest=ms,primary_manifest=mp))
wronghh={k:'0'*64 for k in N.HANDOVER_FILES}
mpwrong=manifest(p194,dg194,'primary_wrong_handover',handover_code_hashes=wronghh)
save_result('primary_handover_mismatch',X.receipt(manifest=ms,primary_manifest=mpwrong))
mswrong=manifest(plan,dg0,'supp_wrong_handover',handover_code_hashes=wronghh)
save_result('supp_handover_mismatch_control',X.receipt(manifest=mswrong,primary_manifest=mp))
msstale=manifest(badplan,dg0,'supp_plan_tsv_wrong_digest_old')
save_result('manifest_plan_wrong_tsv_digest_stale',X.receipt(manifest=msstale,primary_manifest=mp))
mg=manifest(plan,dg0,'supp_other_git',git=dict(sha='b4'*20,short='b4'*4,dirty=False))
mpg=manifest(p194,dg194,'primary_other_git',git=dict(sha='b4'*20,short='b4'*4,dirty=False))
save_result('both_manifests_other_git',X.receipt(manifest=mg,primary_manifest=mpg))
(E/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
