"""Read-only validators on archived receipts; only the archived log path is relocated.
No run/launch command, raw DEM simulation, or production batch is executed.
"""
from pathlib import Path
import sys,json,hashlib,importlib.util,copy
R=Path(__file__).resolve().parent
repo=R/'repo';sys.path.insert(0,str(repo/'scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S
W=R/'wsl/lhs_preflight_35f032737_1028_173239'
O=R/'independent';O.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('before_runner',R/'before/scripts/run_network_194_parallel.py')
B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B);B.ROOT=N.ROOT
def bad(v):return sorted(x['id'] for x in v['checks'] if not x['ok'])
results={'scope':'archived receipts, path-relocated log only; not independent access to WSL raw dumps','code_fp':N.code_fp(N.code_hashes()),'normal':{},'cases':[],'before':[],'integrity':[]}
for prefix,kind in [('net194','production194'),('netsupp20','supp20')]:
 orig=next(p for p in W.glob(prefix+'*.json') if not p.stem.endswith(('_verify','_receipt')))
 raw=json.loads(orig.read_bytes());lp=W/Path(raw['log']['path']).name;lb=lp.read_bytes()
 results['integrity'].append({'receipt':orig.name,'receipt_sha256':hashlib.sha256(orig.read_bytes()).hexdigest(),'log':lp.name,'log_sha256_match':hashlib.sha256(lb).hexdigest()==raw['log']['sha256'],'log_bytes_match':len(lb)==raw['log']['bytes'],'sha_raw':raw['git']['sha']})
 rec=copy.deepcopy(raw);rec['log']['path']=str(lp)
 path=O/(prefix+'_relocated.json');path.write_text(json.dumps(rec,ensure_ascii=False),encoding='utf8');pin=rec['git']['sha']
 normal=N.preflight_receipt_checks(path,kind,pin);results['normal'][kind]=normal
 assert not bad(normal),(kind,bad(normal),normal)
 variants={'normal':pin,'LF':pin+'\n','CRLF':pin+'\r\n','two_LF':pin+'\n\n','space':pin+' ','tab':pin+'\t','NUL':pin+'\0','leading_LF':'\n'+pin,'middle_LF':pin[:20]+'\n'+pin[20:],'zero_width':pin+'\u200b','uppercase':pin.upper(),'short39':pin[:-1],'long41':pin+'a','wrong_last':pin[:-1]+('0' if pin[-1]!='0' else '1'),'null':None,'bool':True,'int':0,'list':[pin],'dict':{'sha':pin},'fullwidth_digit':'３'+pin[1:]}
 for name,value in variants.items():
  rec['git']['sha']=value;path.write_text(json.dumps(rec,ensure_ascii=False),encoding='utf8')
  for approval,ap in [('full',pin),('prefix7',pin[:7]),('omitted',None)]:
   v=N.preflight_receipt_checks(path,kind,ap)
   expect=[] if name=='normal' or (name=='wrong_last' and approval!='full') else ['P10'] if name=='wrong_last' else ['P7'] if ap is None else ['P10','P7']
   row={'set':kind,'name':name,'approval':approval,'expected':sorted(expect),'bad':bad(v),'pass':bad(v)==sorted(expect)};results['cases'].append(row)
   assert row['pass'],row
 for name,value in [('normal',pin),('LF',pin+'\n'),('wrong_last',pin[:-1]+('0' if pin[-1]!='0' else '1'))]:
  rec['git']['sha']=value;path.write_text(json.dumps(rec),encoding='utf8');v=B.preflight_receipt_checks(path,kind,pin);results['before'].append({'set':kind,'name':name,'bad':bad(v)})
 rec['git']['sha']=pin;path.write_text(json.dumps(rec,ensure_ascii=False),encoding='utf8')
 for name,ap in [('uppercase',pin.upper()),('spaced',' '+pin+'\n'),('bad_inner',pin[:9]+'\n'+pin[9:]),('different_review_pin','b7a979032160dc1d9514c612aa36ff0d6c28bf54')]:
  v=N.preflight_receipt_checks(path,kind,ap);results.setdefault('approval',[]).append({'set':kind,'name':name,'bad':bad(v)})
(O/'receipt_probe.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'normal':{k:bad(v) for k,v in results['normal'].items()},'boundary_cases':len(results['cases']),'boundary_failures':sum(not x['pass'] for x in results['cases']),'before':results['before'],'approval':results['approval'],'code_fp':results['code_fp'],'integrity':results['integrity']},ensure_ascii=False,indent=2))
