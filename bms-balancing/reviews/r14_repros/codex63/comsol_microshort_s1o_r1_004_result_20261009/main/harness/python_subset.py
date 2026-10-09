"""One four-input session; exact production AST; no native adapters."""
import sys,os,ast,types,json,hashlib,time,traceback,builtins
from pathlib import Path
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parent))
from inputs import inputs
from input_binding import fingerprint
R=Path(__file__).resolve().parents[1]; S=R.parent
def block(*a,**k):raise RuntimeError('INERT_NATIVE_CONSOLE_JOB_BLOCK')
def audit(event,args):
 if event.startswith(('subprocess.','os.system','os.exec','os.spawn','ctypes.','socket.')):block()
sys.addaudithook(audit);builtins.input=block;os.system=block
def write(o):(R/'results/PYTHON_RESULTS.json').write_text(json.dumps(o,default=str,indent=2),encoding='utf-8')
def main():
 start=time.monotonic();records=[];current=None;reached=[]
 try:
  pins=json.loads((R/'INPUT_SEAL.json').read_text())['positive_inputs']
  path=S/'candidate/consumer.py.inactive.txt';tree=ast.parse(path.read_text(encoding='utf-8-sig'))
  nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.ClassDef,ast.FunctionDef))]
  allowed={'decimal','csv','hashlib','io','copy','json','math'}
  for n in nodes:
   if isinstance(n,ast.Import):assert all(a.name in allowed for a in n.names)
   if isinstance(n,ast.ImportFrom):assert n.module in allowed
  m=types.ModuleType('sealed_consumer');exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),m.__dict__)
  for current,(fn,args) in inputs().items():
   reached=[];assert fingerprint(fn,args,{})==pins[current]['fingerprint']
   def trace(frame,event,arg):
    if event=='call' and frame.f_code.co_filename==str(path):reached.append(frame.f_code.co_name)
   sys.setprofile(trace)
   try: result=getattr(m,fn)(*args)
   finally:sys.setprofile(None)
   if current=='READ_CTRL_CSV':okay=result==[{'time_s':D(0),'value':D(1)},{'time_s':D(1),'value':D(2)}]
   elif current=='READ_CTRL_TIME':okay=result=={D(0):{'time_s':D(0)},D(1):{'time_s':D(1)}}
   elif current=='READ_CTRL_COVERAGE':okay=result[0]==[D(0),D(1)] and result[1]['status']=='PASS' and result[1]['missing_a']==[] and result[1]['missing_b']==[] and result[1]['comparison_times']==['0','1']
   else:okay=list(result)==[D(0)] and result[D(0)]==args[0] and len(result[D(0)])==241
   assert okay and reached.count(fn)==1 and time.monotonic()-start<=120
   rec={'id':current,'status':'PASS','expected':'EXACT_BASELINE_RETURN','observed':'EXACT_BASELINE_RETURN','function':fn,'target_calls':reached.count(fn),'reached_functions':list(dict.fromkeys(reached)),'input':pins[current],'elapsed_s':time.monotonic()-start}
   records.append(rec);write({'status':'RUNNING','count':len(records),'cases':records});print(json.dumps(rec),flush=True)
  write({'status':'PASS','count':4,'cases':records,'elapsed_s':time.monotonic()-start,'engine_sessions':1});return 0
 except Exception as e:
  sys.setprofile(None);failure={'status':'INCOMPLETE','count':len(records),'cases':records,'current_case':current,'first_error':str(e),'traceback':traceback.format_exc(),'current_reach':reached,'elapsed_s':time.monotonic()-start,'retry':0};write(failure);print(json.dumps(failure));return 1
if __name__=='__main__':raise SystemExit(main())
