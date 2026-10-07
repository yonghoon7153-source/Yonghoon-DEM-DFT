"""Actual audit CLI on a synthetic completed one-case fixture, with translated submitted process receipts.
No production workers or simulation launched. Both helper receipts lost is contrasted with final-only loss.
"""
from pathlib import Path
import sys,json,shutil,subprocess,copy
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn
base=R/'fixtures/seal_baseline'
if not base.exists():
 shutil.copytree(R.parent/'gen2_network_reverify3_20261007/evidence/seal_paths/baseline',base)
saved=json.loads((E/'submitted_evidence.json').read_text(encoding='utf8'))
source=E/'receipt_path_translation/import_obs/log';case='lhs00_000'
receipts=[]
for p in source.glob('*.start.json'):
 j=json.loads(p.read_text(encoding='utf8'))
 if j['identity']['case']=='lhs00_055':receipts.append(p.name.removesuffix('.start.json'))
out=[]
for label in ('all5','helper_final_missing','helper_pair_missing','only_worker_and_solver'):
 root=E/'observation_cli'/label;shutil.copytree(base,root,dirs_exist_ok=True)
 m=json.loads((root/'manifest.json').read_text(encoding='utf8'));m['repo_root']=str(S);m['worker_script']=str(S/'scripts/lhs_webapp_batch.py');m['observe_imports']=True
 m['plan']['cohorts'][0]['harvest_dir']=str(root/'harvest');m['plan']['cohorts'][0]['cohort']=str(root/'cohort.tsv')
 m['import_obs_run_id']='81dc4ccc995152e9f06cfbc45d1cae8e';(root/'manifest.json').write_text(json.dumps(m),encoding='utf8')
 logs=root/'import_obs/log';logs.mkdir(parents=True,exist_ok=True)
 for tok in receipts:
  for suffix in ('.start.json','.txt'):
   p=source/(tok+suffix);(logs/p.name).write_text(p.read_text(encoding='utf8').replace('lhs00_055',case),encoding='utf8')
 obs=rn.import_observation(root/'import_obs',S);other=[p for p in obs['processes'] if p['role']=='other']
 if label=='helper_final_missing':(logs/(other[0]['proc']+'.txt')).unlink()
 if label in ('helper_pair_missing','only_worker_and_solver'):
  targets=other[:1] if label=='helper_pair_missing' else other
  for p in targets:
   for suffix in ('.start.json','.txt'):(logs/(p['proc']+suffix)).unlink()
 p=subprocess.run([sys.executable,'-B',str(S/'scripts/run_network_194_parallel.py'),'audit','--root',str(root),'--json',str(root/'audit.json')],capture_output=True,text=True,encoding='utf8')
 (root/'audit.log').write_text(p.stdout+p.stderr,encoding='utf8');a=json.loads((root/'audit.json').read_text(encoding='utf8'))
 row=dict(label=label,rc=p.returncode,verdicts=a.get('verdicts'),input_problems=a.get('input_problems'),generation_problems=a.get('generation_problems'),import_problems=a.get('import_observation_problems'),
          n_start=(a.get('import_observation') or {}).get('n_started'),n_final=(a.get('import_observation') or {}).get('n_finalized'))
 out.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(E/'observation_cli.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
