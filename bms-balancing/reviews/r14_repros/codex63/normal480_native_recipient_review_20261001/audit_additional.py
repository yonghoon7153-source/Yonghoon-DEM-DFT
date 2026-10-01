"""Recipient-only checks for packaging correction, headers and historical evidence."""
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; R=ROOT/'received'; S=ROOT/'supplement'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def identity(p):
    with p.open('rb') as f: return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
checks=[]
def check(n,ok):
    checks.append({'check':n,'pass':bool(ok)}); assert ok,n
c=read(R/'candidate/CONTRACT.json')
first=(R/'delivery/package_evidence_first_error.py').read_text(encoding='utf-8-sig')
final=(R/'delivery/package_evidence.py').read_text(encoding='utf-8-sig')
bad="for n,e in c['b020_baseline_files'].items():pin(e);add('baseline_b020/'+n,e['path'])\n"
check('packaging correction is exactly removal of absent duplicate baseline lookup',first.count(bad)==1 and first.replace(bad,'')==final and 'b020_baseline_files' not in c)
err=read(R/'delivery/PACKAGING_FIRST_ERROR.json')['return']
check('first packaging error and rc1 retained',err['exit_code']==1 and "KeyError: 'b020_baseline_files'" in err['output'])
check('B020 references already part of baseline_files',sum(n.startswith('B020_') for n in c['baseline_files'])==6 and all((R/'baseline'/n).is_file() for n in c['baseline_files']))
hdr={
 'electrolyte_guard.csv':'time_s ce_min_all_mol_m3 ce_min_d1_mol_m3 ce_min_d2_mol_m3 ce_min_d3_mol_m3 threshold_mol_m3 electrolyte_guard ocp_guard surface_guard',
 'preflight_global.csv':'time_s Li_N_mol_m2 Li_P_mol_m2 Li_electrolyte_mol_m2 xavg_N xavg_P xsurf_N_min xsurf_N_max xsurf_P_min xsurf_P_max ocp_guard reaction_N_A_m2 reaction_P_A_m2 leak_leftward_A_m2'}
for n in ['preflight_boundary1.csv','preflight_boundary4.csv']:
    hdr[n]='time_s phis_V phil_V Eeq_V eta_V etamid_V x_surface x_particle_average cs_surface_mol_m3 reaction_input_mol_m3 csmax_mol_m3 direct_Eeq_surface_V Isx_A_m2'
for n in ['axes_profile_N.csv','axes_profile_P.csv']:
    hdr[n]='time_s coordinate_m x_surface x_particle_average Eeq_V etaMid_V phil_V domain_id'
for n,h in hdr.items():
    with (R/'run/tables'/n).open(encoding='utf-8-sig',newline='') as f: actual=next(csv.reader(f))
    check('raw exact header '+n,actual==h.split())
prior=ROOT.parent/'normal240_native_review_20260930/received/run/tables'
for p in (R/'run/tables').glob('equations_*.csv'):
    check('unchanged sampled particle equation '+p.name,p.read_bytes()==(prior/p.name).read_bytes())
d=read(R/'run/DIAGNOSTIC_RESULT.json'); summary=read(R/'delivery/RESULT_SUMMARY.json')
check('summary binds exact diagnostic bytes',identity(R/'run/DIAGNOSTIC_RESULT.json')=={k:summary['result'][k] for k in ['bytes','sha256']})
check('summary quotes actual numeric result',summary['numeric']==d['numeric'])
user=read(R/'authorization/USER_DECISION.json')
check('approval explicitly excludes960 and includes general limits',any('960' in s for s in user['accepted_observation_limits']) and user['solve_max']==user['compile_max']==user['batch_max']==1 and user['physical_time_max_seconds']==480 and user['code_manifest_sha256']==d['code_manifest_sha256'])
check('no claimed actual core/effective policy verification',read(R/'run/NATIVE_STATE.json')['actual_cores']=='UNVERIFIED' and d['effective_policy']=='UNVERIFIED')
mph=read(R/'run/OUTPUT_MPH_IDENTITY.json')
check('MPH identity record only, no MPH in received package',mph['bytes']==7315279360 and mph['sha256']=='2ada6b402917e31d1dc4c5265bf483d92e6a8e5ef50de57463acbc81f91311ab' and not list(R.rglob('*.mph')))
out={'status':'PASS','checks':checks,'scope':'Static/data checks only; no received code executed. MPH bytes not locally available.', 'output_MPH_sender_identity':mph,
     'packaging_correction':'One erroneous duplicate lookup removed; six B020 CSVs remain included under baseline/.',
     'separate_packaging_budget':'323.703s packaging snapshot is outside completed native parent. No separate packaging budget acceptance inferred.'}
(ROOT/'ADDITIONAL_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks)}))
