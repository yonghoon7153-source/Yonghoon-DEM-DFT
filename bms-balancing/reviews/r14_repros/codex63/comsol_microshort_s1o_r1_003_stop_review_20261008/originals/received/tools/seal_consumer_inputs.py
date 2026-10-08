"""Data-only input materialization. No candidate imports, function calls, or test results."""
import sys,ast,json,hashlib,copy,csv,io,time
from pathlib import Path
from decimal import Decimal as D,localcontext
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'harness'))
import shared_fixture as f
from input_binding import fingerprint
class Captured(Exception):pass
class CaptureOnly:
 def __init__(self,cid):self.cid=cid;self.calls=[]
 def __getattr__(self,name):
  def capture(*args,**kwargs):
   self.calls.append(fingerprint(name,args,kwargs))
   if self.cid=='READ01':
    if name=='read_csv_bytes':
     raw=args[0];e='N' if args[2]['path'].endswith('N.csv') else 'P'
     (ROOT/'fixture_inputs'/('shared_profile_'+e+'.csv')).write_bytes(raw)
     # Own data normalization only, never the received reader under test.
     return [{k:D(v) for k,v in row.items()} for row in csv.DictReader(io.StringIO(raw.decode()))]
    if name=='timed_rows':return {r['time_s']:r for r in args[0]}
    if name=='coverage':return None
    if name=='profile_rows':
     grouped={}
     for row in args[0]:grouped.setdefault(row['time_s'],[]).append(row)
     return grouped
   raise Captured()
  return capture
tree=ast.parse((ROOT/'harness/python_harness.py').read_text())
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('compare_args','charge_case','consumer_case')]
scope={'D':D,'f':f,'copy':copy,'localcontext':localcontext}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'owned_data_constructor','exec'),scope)
plan=json.loads((ROOT/'VALIDATION_PLAN_CORRECTED.json').read_text(encoding='utf-8-sig'))
dest=ROOT/'fixture_inputs';dest.mkdir(exist_ok=True)
if (ROOT/'CONSUMER_INPUT_IDENTITIES.json').exists():raise RuntimeError('NO_OVERWRITE')
started=time.monotonic();records=[]
for case in plan['cases']:
 if case['engine']!='Python' or case['id'].startswith(('AUTH','RESOURCE')):continue
 capture=CaptureOnly(case['id'])
 try:scope['consumer_case'](case['id'],capture,case)
 except Captured:pass
 if not capture.calls:raise RuntimeError('NO_CAPTURE:'+case['id'])
 record={'id':case['id'],'input_id':case['input_id'],'calls':capture.calls,'recipe':case['fixture_mutation'],
  'expected':case['expected'],'scope':'actual derived input canonical hashes; full expanded replicas not persisted; exact own generator and shared seeds sealed'}
 raw=json.dumps(record,separators=(',',':'),ensure_ascii=False).encode();path=dest/(case['id']+'.recipe.json');path.write_bytes(raw)
 record['recipe_identity']={'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};records.append(record)
 print(json.dumps({'constructed_input':case['id'],'call_count':len(capture.calls),'elapsed_s':time.monotonic()-started}),flush=True)
(ROOT/'CONSUMER_INPUT_IDENTITIES.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
seeds={'requests':f.REQUESTS,'coordinates':{k:[str(x) for x in v] for k,v in f.COORDS.items()},'precision':50,'F_C_mol':str(f.F),'current_A_m2':'.25001','Li_initial_N_P_E_mol_m2':['1','1','1'],'x_N':'.445','x_P':'.581','base_voltage_V':'3','extra_actual_times_s':['.00015','100.001'],'shared_profiles_sha256':{e:hashlib.sha256((dest/('shared_profile_'+e+'.csv')).read_bytes()).hexdigest() for e in ('N','P')}}
(dest/'SHARED_SEED.json').write_text(json.dumps(seeds,indent=2),encoding='utf-8')
print(json.dumps({'candidate_calls':0,'functional_tests':0,'consumer_inputs':len(records),'elapsed_s':time.monotonic()-started}))
