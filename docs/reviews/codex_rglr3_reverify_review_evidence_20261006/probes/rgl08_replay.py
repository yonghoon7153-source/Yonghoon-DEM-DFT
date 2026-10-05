"""Original RGL-08 on an actual producer output, at the new pin."""
from pathlib import Path
import sys,json,shutil,tempfile
R=Path(__file__).resolve().parents[1];E=R/'evidence';S=R/'source'
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import pipeline_service as PS
results=json.loads((E/'network_adversarial.json').read_text(encoding='utf8'))
base=R/next(r['path'] for r in results if r['name']=='positive')
rr=Path(tempfile.mkdtemp(prefix='rgl08_replay_',dir=E));rows=[]
for label in ('baseline','missing_tau_inputs','permode_vs_dual_disagree','percolating_power_missing'):
 d=rr/label;shutil.copytree(base,d)
 files=('network_conductivity.json','network_conductivity_hertzian.json','network_conductivity_physics.json','network_conductivity_dual.json','full_metrics.json')
 objs={n:json.loads((d/n).read_text(encoding='utf8')) for n in files}
 if label=='missing_tau_inputs':
  for ob in [objs[n] for n in files[:3]]+list(objs['network_conductivity_dual.json'].values()):
   for k in ('sigma_full','percolating_fraction','temperature_provenance','sigma_grain_S_cm'):ob.pop(k,None)
 if label=='permode_vs_dual_disagree':objs['network_conductivity_physics.json']['sigma_full_mScm']=99.
 if label=='percolating_power_missing':
  for ob in [objs[n] for n in files[:3]]+list(objs['network_conductivity_dual.json'].values())+[objs['full_metrics.json']]:
   for k in list(ob):
    if k.startswith('constriction_power_share_ion_'):ob[k]='internal_solver_exception' if k.endswith('_status') else None
 for n,o in objs.items():(d/n).write_text(json.dumps(o),encoding='utf8')
 ok,why=PS.network_stop_verdict(str(d),objs['full_metrics.json']['network_run_id'])
 rows.append(dict(name=label,accepted=ok,reason=why))
assert rows[0]['accepted'] and not any(x['accepted'] for x in rows[1:])
(E/'rgl08_replay.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
