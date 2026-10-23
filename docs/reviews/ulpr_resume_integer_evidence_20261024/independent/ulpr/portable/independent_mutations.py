from pathlib import Path
import sys,json,hashlib,contextlib,argparse
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser(description='Independent ULPR mutations; --repo is the frozen candidate repository/export.');ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);args=ap.parse_args()
K=Path(args.repo)/'docs/data/ps45_unload_20261009';O=Path(args.out);O.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(K))
p=K/'ul_reader.py';b=p.read_bytes();h=hashlib.sha256(b).hexdigest();assert h=='7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b';s=b.decode();results=[]
for label,old,new in [('event_rounding_restored',"index = _resume_integer if r['event'] == 'RESUME' else _i","index = _i"),('event_csv_structure_guard_removed','auth, apr = ([], []) if pr else _resume_auth(d, events)','auth, apr = _resume_auth(d, events)')]:
 assert s.count(old)==1
 mutant=s.replace(old,new);ns={'__file__':str(p),'__name__':'independent_mutant_'+label};exec(compile(mutant,label,'exec'),ns);cases=[];uncaught=None
 def chk(name,condition,detail=''):
  exception=None
  try:ok=bool(condition() if callable(condition) else condition)
  except Exception as e:ok=False;exception=type(e).__name__+': '+str(e)
  cases.append({'name':name,'pass':ok,'assertion_exception':exception,'detail':str(detail) if not ok else ''})
 with (O/(label+'.log')).open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  try:ns['_resume_integer_tests'](chk,ns['ul_lib'].load_params())
  except Exception as e:uncaught=type(e).__name__+': '+str(e)
  print(json.dumps(cases,ensure_ascii=False,indent=2))
 failures=[x for x in cases if not x['pass']];ok=bool(failures) and uncaught is None and not any(x['assertion_exception'] for x in cases)
 results.append({'mutation':label,'replacement':{'old':old,'new':new},'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'detected_by_behavior_assertions':ok,'pass_count':len(cases)-len(failures),'fail_count':len(failures),'uncaught_exception':uncaught,'failures':failures})
result={'status':'PASS' if all(x['detected_by_behavior_assertions'] for x in results) and p.read_bytes()==b else 'FAIL','source_sha256':h,'source_unchanged':p.read_bytes()==b,'mutation_count':len(results),'results':results,'scope':'Two independently chosen in-memory mutations; canonical R39 assertions only. Distinct from author 11-mutant evidence; no source writes or fullgate.'}
(O/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='PASS' else 1)
