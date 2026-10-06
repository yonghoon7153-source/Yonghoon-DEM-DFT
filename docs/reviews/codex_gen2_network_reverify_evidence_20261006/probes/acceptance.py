"""Actual producer/publisher/handover; adversarial changes confined to reviewer copies."""
from pathlib import Path
import sys,os,json,copy,contextlib,io,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/acceptance';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
os.environ.update(TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
import app,pipeline_service as ps,tau_flux as tf
import test_pipeline_provenance as TP
import test_gen2_publication_handover as PH
import lhs_design_dataset as LDD,lhs_webapp_batch as LWB
def mutate(d,label):
 for name,key in PH.NET_FILES:
  p=Path(d)/name;obj=json.loads(p.read_text(encoding='utf8'));rh=obj.get('hertzian') if key is None else obj if key=='hertzian' else None
  if rh is not None:
   if label=='missing_full_cert':rh.pop('solve_certificate_full',None)
   if label=='full_cert_from_cf':rh['solve_certificate_full']=copy.deepcopy(rh['solve_certificate_bulk_net'])
   if label=='full_cert_from_h12':rh['solve_certificate_full']=copy.deepcopy(rh['hertz_h12']['solve_certificate_full'])
   if label=='missing_cf_cert':rh.pop('solve_certificate_bulk_net',None)
   if label=='cf_bad_conservation':rh['solve_certificate_bulk_net'].update(I_top=0.,conservation_rel=1.)
   if label=='missing_constr_cert':rh.pop('solve_certificate_constr_net',None)
  p.write_text(json.dumps(obj),encoding='utf8')
def row(d):
 r=tf.case_row(str(d));return {k:v for k,v in r.items() if k.startswith(('ion_net_status_','tau2_ion_')) or k=='ion_net_generation'}
out=[]
for label in ('baseline','missing_full_cert','full_cert_from_cf','full_cert_from_h12','missing_cf_cert','cf_bad_conservation','missing_constr_cert'):
 d=D/label;d.mkdir(exist_ok=True);a,c=TP._write_bed(str(d),'through')
 (d/'full_metrics.json').write_text(json.dumps(TP._bed_ledger('through')),encoding='utf8')
 runner=TP._CLIRunner(mutate=None if label=='baseline' else lambda p,l=label:mutate(p,l))
 log=io.StringIO()
 with contextlib.redirect_stdout(log): stages,rid=app._network_and_stage_e(str(d),str(S/'scripts'),a,c,'1:SE',1,[],runner=runner,stop_before_stage_e=True)
 st,fail=ps.summarize(stages);fm=json.loads((d/'full_metrics.json').read_text());du= json.loads((d/'network_conductivity_dual.json').read_text()) if (d/'network_conductivity_dual.json').exists() else {}
 rh=du.get('hertzian',{});rec=dict(label=label,status=st,stop=ps.network_stop_verdict(str(d),rid),row=row(d),full_q=rh.get('sigma_full'),cf_q=rh.get('sigma_bulk_net'),full_certificate=rh.get('solve_certificate_full'),cf_certificate=rh.get('solve_certificate_bulk_net'))
 (d/'review_run.log').write_text(log.getvalue(),encoding='utf8');out.append(rec)
 print(label,st,rec['row'],flush=True)

base=D/'baseline';prov=ps.read_network_provenance(str(base));rid=prov['network_run_id'];stamp=[]
for label in ('control','all_unknown','all_null','one_null_legacy_shape','g2_declares_legacy','stamp_absent_keys'):
 dst=D/('stamp_'+label);shutil.copytree(base,dst,dirs_exist_ok=True)
 if label=='one_null_legacy_shape':
  PH.mut(dst,'legacy_shape');p=app._network_projection(str(dst),rid);(dst/'full_metrics.json').write_text(json.dumps(p['fm']),encoding='utf8')
 p=copy.deepcopy(prov)
 if label in ('all_unknown','all_null'):
  for k in PH.STAMP_G2_KEYS:p[k]='unrecognized' if label=='all_unknown' else None
 if label in ('stamp_absent_keys','one_null_legacy_shape'):
  for k in PH.STAMP_G2_KEYS:p.pop(k,None)
  if label=='one_null_legacy_shape':p['electrode_model']=None
 if label=='g2_declares_legacy':p.update(electrode_model='virtual_source_legacy',area_rule_physics='physics_g1',psi_placement_physics='legacy_divide',hertz_h12=False)
 (dst/ps.PROVENANCE_FILE).write_text(json.dumps(p),encoding='utf8')
 br=D/('batch_'+label);res=br/'results';res.mkdir(parents=True,exist_ok=True);cd=res/'lhs00_000';shutil.copytree(dst,cd,dirs_exist_ok=True)
 fm=json.loads((cd/'full_metrics.json').read_text());st0=json.loads((S/'docs/data/lhs_webapp_contact_d1ec42fba/status.json').read_text())
 st0.update(stop_after='network',cases={'lhs00_000':dict(case='lhs00_000',stop_after='network',status='done',failed_stages=[],network_run_id=rid)})
 flat={'lhs00_000':dict({k:v for k,v in fm.items() if not isinstance(v,(dict,list))},case='lhs00_000')}
 LWB.write_outputs(br/'batch',st0,flat)
 try:
  result=LDD.load_tau_results(res,LDD.load_webapp(br/'batch'));problem='';cells=result['cases']['lhs00_000']['cells']
 except Exception as ex:problem=type(ex).__name__+': '+str(ex);cells={}
 item=dict(label=label,accepted=not problem,problem=problem,generation=cells.get('ion_net_generation'),stamp={k:p.get(k,'ABSENT') for k in PH.STAMP_G2_KEYS})
 stamp.append(item);print('STAMP',label,item['accepted'],item['generation'],problem[:100],flush=True)
(R/'evidence/acceptance.json').write_text(json.dumps(dict(publication=out,stamp=stamp),indent=2,ensure_ascii=False),encoding='utf8')
