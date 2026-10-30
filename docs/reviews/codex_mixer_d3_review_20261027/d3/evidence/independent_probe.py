from pathlib import Path
import sys, importlib.util, itertools, copy, hashlib, json, subprocess
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'snapshot/scripts'
spec=importlib.util.spec_from_file_location('reader',S/'mixer_d3_candidates.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=Path(__file__).resolve().parent; rows=[]; digest=hashlib.sha256();counts={}
ids=['low','middle','high'];raw={'condition.txt':b'independent fixed synthetic condition','observation.txt':b'independent test bytes, not measured data'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def point(code,cat=False):
 if code==2:return None
 if code==3:return {'state':'technical-failure','reason':'independent synthetic failed observation'}
 p={'state':'eligible','value':('flow' if code==0 else 'stop') if cat else (3 if code==0 else 7),'unit':'state' if cat else 'u','source_ids':['data']}
 if not cat:p['uncertainty']={'value':.2,'unit':'u','n':5,'df':4,'method':'synthetic explicit input'}
 return p
def fixture():
 c={'schema':'mixer_d3_decision_contract/1','analysis_id':'independent','condition_sha256':sha(raw['condition.txt']),'grid':[{'id':i,'bo':b} for i,b in zip(ids,[.4,2.75,18])], 'calibration':{t:{'unit':'u','boundary':'inclusive','widths':dict.fromkeys(ids,1)} for t in ['T1','T2']},'validation':{'Vscalar':{'kind':'scalar','unit':'u','boundary':'inclusive','widths':dict.fromkeys(ids,1)},'Vstate':{'kind':'categorical','unit':'state','rule':'exact-match','labels':['flow','stop']}},'seed_policy':{'allowed_role_overlap':[]}}
 o={'schema':'mixer_d3_observations/1','contract_sha256':'b'*64,'condition_artifact':'condition','artifacts':[{'id':i,'path':p,'sha256':sha(raw[p])} for i,p in [('condition','condition.txt'),('data','observation.txt')]],'calibration':{t:{'experiment':point(0),'predictions':{i:point(0) for i in ids}} for t in ['T1','T2']},'validation':{'Vscalar':{'experiment':point(0),'predictions':{i:point(0) for i in ids}},'Vstate':{'experiment':point(0,True),'predictions':{i:point(0,True) for i in ids}}},'seed_manifest':{'C0':[1009],'C1':[1013],'C2':[1019]}}
 return c,o
def ev(c,o):return m.evaluate(c,o,contract_sha256='b'*64,artifact_loader=raw.__getitem__)
def record(name,ok,detail=None):
 rows.append({'name':name,'ok':bool(ok),'detail':detail});assert ok,(name,detail)
for group in ['calibration','validation']:
 count=0
 for codes in itertools.product(range(4),repeat=6):
  c,o=fixture();tests=['T1','T2'] if group=='calibration' else ['Vscalar','Vstate']
  for k,t in enumerate(tests):
   for j,i in enumerate(ids):o[group][t]['predictions'][i]=point(codes[k*3+j],t=='Vstate')
  r=ev(c,o)
  if group=='calibration':
   want=[i for j,i in enumerate(ids) if codes[j]==codes[3+j]==0]
   assert r['S']==want
   assert r['calibration_complete']==all(x<2 for x in codes)
   assert r['S_T1']==[i for j,i in enumerate(ids) if codes[j]==0]
   assert r['S_T2']==[i for j,i in enumerate(ids) if codes[j+3]==0]
   sets=[set(r['S_T1']),set(r['S_T2'])]
   empty='not-empty' if want else 'both-tests-empty' if not any(sets) else 'T1-empty' if not sets[0] else 'T2-empty' if not sets[1] else 'disjoint'
   assert r['empty_case']==empty
   if not want:assert r['validation']['aggregate']=='not-applicable'
  else:
   assert r['S']==ids
   want=['unassessed' if max(codes[j],codes[j+3])>=2 else 'incompatible' if max(codes[j],codes[j+3])==1 else 'compatible' for j in range(3)]
   assert [x['status'] for x in r['validation']['candidates']]==want
   agg='incomplete' if 'unassessed' in want else 'all-compatible' if set(want)=={'compatible'} else 'none-compatible' if set(want)=={'incompatible'} else 'mixed'
   assert r['validation']['aggregate']==agg
   for j,p in enumerate(r['validation']['candidates']):
    for k,t in enumerate(tests):assert p['items'][t]['status']==['compatible','incompatible','unassessed','unassessed'][codes[3*k+j]]
  assert r['execution_ready'] is False
  digest.update(json.dumps(r,sort_keys=True).encode());count+=1
 counts[group]=count
record('exhaustive independent oracle',True,counts)
# Invalid supplied fields must fail even if experiment missing and candidate excluded.
cases=[('bad_numeric',lambda p:p.update(value=True)),('bad_unit',lambda p:p.update(unit='wrong')),('bad_source',lambda p:p.update(source_ids=['missing'])),('bad_uncertainty',lambda p:p.update(uncertainty={'value':0})),('unknown_field',lambda p:p.update(hidden=3))]
for name,change in cases:
 c,o=fixture();o['calibration']['T1']['predictions']['high']=point(1);o['validation']['Vscalar']['experiment']=None;change(o['validation']['Vscalar']['predictions']['high'])
 try:ev(c,o);rejected=False
 except m.ContractError:rejected=True
 record(name,rejected)
# Exact comparison across 601 orders of magnitude.
for x,y,w,want in [('0.4','0.3','0.1','COMPATIBLE'),('1e300','1e-300','1e300','COMPATIBLE'),('1e300','-1e-300','1e300','INCOMPATIBLE')]:
 c,o=fixture();o['calibration']['T1']['predictions']['low']['value']=Decimal(x);o['calibration']['T1']['experiment']['value']=Decimal(y);c['calibration']['T1']['widths']['low']=Decimal(w)
 got=ev(c,o)['calibration']['T1'][0]['status'];record('decimal_'+x+'_'+y,got==want,got)
# Original grid order, separated clusters, readonly inputs, missing seeds.
c,o=fixture();o['calibration']['T1']['predictions']['middle']=point(2);before=copy.deepcopy((c,o));r=ev(c,o)
record('neighbor gap and input preservation',r['neighbor_groups']==[['low'],['high']] and before==(c,o))
for seed in [15485863,86028121,104395301]:
 c,o=fixture();o['seed_manifest']['C2']=[seed]
 try:ev(c,o);ok=False
 except m.ContractError:ok=True
 record('reserved_'+str(seed),ok)
c,o=fixture();del o['seed_manifest'];record('no manifest is not certified',ev(c,o)['seed_check']=={'status':'NOT_PROVIDED','historical_nonuse_verified':False})
# CLI actual source binding, no output on malformed bytes, no overwrite.
import tempfile
cli=Path(tempfile.mkdtemp(prefix='cli-replay-',dir=OUT))
for name in ['positive','none','incomplete','tampered_raw','wrong_digest','duplicate_json','path_escape']:
 d=cli/name;d.mkdir(exist_ok=True);c,o=fixture()
 for p,b in raw.items():(d/p).write_bytes(b)
 if name=='none':
  for i in ids:o['calibration']['T1']['predictions'][i]=point(1)
 if name=='incomplete':o['validation']['Vstate']['predictions']['high']=point(2)
 if name=='path_escape':o['artifacts'][1]['path']='../observation.txt'
 cb=json.dumps(c,ensure_ascii=False).encode();(d/'contract.json').write_bytes(cb);o['contract_sha256']=sha(cb) if name!='wrong_digest' else 'a'*64
 ob=json.dumps(o,ensure_ascii=False).encode()
 if name=='duplicate_json':ob=ob.replace(b'{',b'{"schema":"bad",',1)
 (d/'observations.json').write_bytes(ob)
 if name=='tampered_raw':(d/'observation.txt').write_bytes(b'tampered')
 cmd=[sys.executable,'-I','-X','utf8','-B',str(S/'mixer_d3_candidates.py'),'--contract',str(d/'contract.json'),'--observations',str(d/'observations.json'),'--out',str(d/'result.json')]
 p=subprocess.run(cmd,capture_output=True);(d/'process.log').write_bytes(p.stdout+p.stderr)
 success=name in ['positive','none','incomplete'];record('cli_'+name,p.returncode==(0 if success else 2) and (d/'result.json').exists()==success,{'rc':p.returncode})
 if success:
  result=json.loads((d/'result.json').read_bytes());record('cli_binding_'+name,result['input_sha256']=={'contract':sha(cb),'observations':sha(ob)} and not result['execution_ready'])
  original=(d/'result.json').read_bytes();p=subprocess.run(cmd,capture_output=True);record('cli_no_overwrite_'+name,p.returncode==2 and (d/'result.json').read_bytes()==original)
summary={'source_sha256':sha((S/'mixer_d3_candidates.py').read_bytes()),'python':sys.version,'oracle_combinations':counts,'oracle_output_hash':digest.hexdigest(),'cli_directory':cli.name,'checks':rows,'all_passed':all(x['ok'] for x in rows),'symlink_execution':'NOT_TESTED: Windows privilege unavailable; existing test has WinError1314','physical_runs':0}
(OUT/'independent_results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'oracle_combinations':counts,'checks':len(rows),'all_passed':summary['all_passed']}))
