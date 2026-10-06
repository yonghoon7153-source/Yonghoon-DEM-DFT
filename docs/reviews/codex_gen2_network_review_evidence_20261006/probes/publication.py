"""Actual producer -> candidate checks -> publication -> tau reader; mutations on review fixtures only."""
from pathlib import Path
import sys,json,copy,contextlib,io
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'source/scripts'),str(R/'source/webapp')]
import app
import pipeline_service as ps
import test_pipeline_provenance as tp
import tau_flux as tf
ROOT=R/'evidence/publication';ROOT.mkdir(exist_ok=True)
def change(du,label):
 for k,r in du.items():
  if not isinstance(r,dict):continue
  if label=='h12_as_primary' and k=='hertzian':
   h12=copy.deepcopy(r['hertz_h12']);r.update(h12)
  elif label=='bad_psi' and k=='physics':r['psi_placement']='multiply_TYPO'
  elif label=='bad_electrode':
   r['electrode_model']='DIRICHLET_TYPO'
   if 'hertz_h12' in r:r['hertz_h12']['electrode_model']='DIRICHLET_TYPO'
  elif label=='partial_missing_g2' and k=='physics':
   for key in ('area_rule','psi_placement'):r.pop(key,None)
def mut(d,label):
 for name,key in [('network_conductivity_dual.json',None),('network_conductivity.json','hertzian'),('network_conductivity_hertzian.json','hertzian'),('network_conductivity_physics.json','physics')]:
  p=Path(d)/name;obj=json.loads(p.read_text());change(obj if key is None else {key:obj},label);p.write_text(json.dumps(obj),encoding='utf8')
results=[]
for label in ('baseline','h12_as_primary','bad_psi','bad_electrode','partial_missing_g2'):
 d=ROOT/label;d.mkdir(exist_ok=True)
 atom,contact=tp._write_bed(str(d),'through')
 (d/'full_metrics.json').write_text(json.dumps(tp._bed_ledger('through')),encoding='utf8')
 runner=tp._CLIRunner(mutate=(lambda p,l=label:mut(p,l)) if label!='baseline' else None)
 log=io.StringIO()
 with contextlib.redirect_stdout(log):
  stages,rid=app._network_and_stage_e(str(d),str(R/'source/scripts'),atom,contact,'1:SE',1,[],runner=runner,stop_before_stage_e=True)
 status,failed=ps.summarize(stages)
 (d/'run.log').write_text(log.getvalue(),encoding='utf8')
 row=tf.case_row(str(d));fm=json.loads((d/'full_metrics.json').read_text())
 item=dict(label=label,status=status,failed=failed,stop=ps.network_stop_verdict(str(d),rid),row=row,projected={k:fm.get(k) for k in ('sigma_full','bulk_model','resistance_model','electrode_model','area_rule_physics','psi_placement_physics')})
 results.append(item)
 print(label,status,item['stop'],item['projected'],flush=True)
base=results[0]['row']
for item in results:item['mixed_with_baseline']=tf.generation_mixing_problem([base,item['row']])
(R/'evidence/publication.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
