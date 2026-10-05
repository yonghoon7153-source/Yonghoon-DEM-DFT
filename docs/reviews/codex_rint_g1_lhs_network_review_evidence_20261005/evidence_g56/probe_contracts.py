"""Actual app/pipeline/tau functions. Only solver writes are fixture-injected.
No simulation, no source modification; each case is an isolated temporary dir.
"""
import copy, json, os, subprocess, sys, tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'source'
sys.path[:0]=[str(S/'webapp'),str(S/'scripts')]
import app, pipeline_service as ps, tau_flux, grade_engine as ge

def record(mode):
 tail='hertz' if mode=='hertzian' else 'physics'
 return dict(sigma_full=0.05, sigma_full_mScm=0.15, sigma_full_status='computed',
   sigma_bulk_net=0.1,sigma_bulk_net_mScm=0.3,percolating_fraction=1.0,
   sigma_grain_S_cm=0.003,temperature_provenance={'sigma_ion_T_factor':1.0,'T_C':None,'T_ref_C':25.0},
   phi_se=0.3,boundary_rule='L0',boundary_band_frac=0.08,
   ionic_status='computed',electronic_status='computed',thermal_status='computed',
   **{f'constriction_power_share_ion_{tail}':0.5,f'constriction_power_share_ion_{tail}_status':'computed'})

def pipeline_case(label, modify=None, seed=None):
 with tempfile.TemporaryDirectory(prefix='g56_') as t:
  d=Path(t); atoms=d/'atoms.csv'; contacts=d/'contacts.csv'
  atoms.write_text('id\n1\n'); contacts.write_text('id1,id2\n1,2\n')
  fm={'phi_se':0.3,'thickness_um':100.0,'thickness_mass_conserving_um':100.0,'phi_se_mass_conserving':0.3,'percolation_pct':100.0}
  if seed: fm.update(seed)
  (d/'full_metrics.json').write_text(json.dumps(fm))
  # A healthy previous active generation, to verify rollback on failed retry.
  for n in ('network_conductivity.json','network_conductivity_hertzian.json','network_conductivity_physics.json'):
   (d/n).write_text(json.dumps(dict(record('hertzian'),old_marker=True)))
  (d/'network_conductivity_dual.json').write_text(json.dumps({'hertzian':record('hertzian'),'physics':record('physics'),'old_marker':True}))
  ps.stamp_network_provenance(str(d),'OLD_RUN',{},'success')
  H,P=record('hertzian'),record('physics')
  dual={'hertzian':copy.deepcopy(H),'physics':copy.deepcopy(P)}
  artifacts={'network_conductivity.json':copy.deepcopy(H),'network_conductivity_hertzian.json':H,
    'network_conductivity_physics.json':P,'network_conductivity_dual.json':dual}
  if modify: modify(artifacts)
  def runner(cmd,**kw):
   assert Path(cmd[1]).name=='network_conductivity.py',cmd
   for name,data in artifacts.items(): (d/name).write_text(json.dumps(data))
   return subprocess.CompletedProcess(cmd,0,'synthetic solver fixture','')
  logs=[]
  stages,rid=app._network_and_stage_e(str(d),str(S/'scripts'),str(atoms),str(contacts),'1:AM,3:SE',1000,logs,
     runner=runner,stop_before_stage_e=True)
  fm2=json.loads((d/'full_metrics.json').read_text())
  tau=tau_flux.case_row(str(d)); prov=ps.read_network_provenance(str(d))
  return {'label':label,'summary':ps.summarize(stages),'stages':stages,'stop_gate':ps.network_stop_verdict(str(d),rid),
    'active_provenance':prov,'old_generation_survived':json.loads((d/'network_conductivity.json').read_text()).get('old_marker',False),
    'full_metrics':fm2,'tau':tau,'grade_tau':ge._derived_value('__tau_lap_eff',fm2),'paired_sigma0':tau_flux.tau2_from_metrics(fm2)[1]}

def records(a):
 return [a['network_conductivity.json'],a['network_conductivity_hertzian.json'],a['network_conductivity_physics.json'],*a['network_conductivity_dual.json'].values()]
def missing_handover(a):
 for rec in records(a):
  for key in ('sigma_full','percolating_fraction','temperature_provenance','sigma_grain_S_cm'):
   rec.pop(key,None)
def inconsistent_mode(a):
 a['network_conductivity_physics.json']['sigma_full_mScm']=99.0
def invalid_stop(a):
 a['network_conductivity_dual.json']['physics']['boundary_rule']='L9'
def missing_power_with_excuse(a):
 for rec in records(a):
  for key in list(rec):
   if key.startswith('constriction_power_share_ion_'):
    rec[key]='internal_solver_exception' if key.endswith('_status') else None

if __name__=='__main__':
 out=[pipeline_case('healthy'),pipeline_case('missing_tau_inputs',missing_handover),
  pipeline_case('permode_vs_dual_disagree',inconsistent_mode),pipeline_case('stop_gate_failure_after_publication',invalid_stop),
  pipeline_case('percolating_power_missing',missing_power_with_excuse),
  pipeline_case('stale_temperature_factor4',seed={'temperature_provenance':{'sigma_ion_T_factor':4.0,'T_C':60.0}})]
 for row in out:
  print(json.dumps({k:row[k] for k in ('label','summary','stop_gate','old_generation_survived','grade_tau','paired_sigma0')},ensure_ascii=False))
 (Path(__file__).parent/'contract_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
