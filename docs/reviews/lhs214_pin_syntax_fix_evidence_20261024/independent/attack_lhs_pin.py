from pathlib import Path
import sys,subprocess,ast,hashlib,json,contextlib
sys.dont_write_bytecode=True
ROOT=Path('/workspace/.cloud-setup/nonrint-20261024/lhs-readiness/snapshot');OUT=Path('/workspace/.cloud-setup/nonrint-20261024/audit/lhs-pin');OUT.mkdir(parents=True,exist_ok=False)
PIN='ffbd438e7522d58eb069561fe58020f4086707ac';REPO='/workspace/Yonghoon-DEM-DFT';REL='scripts/run_network_194_parallel.py';sha=lambda b:hashlib.sha256(b).hexdigest()
base=subprocess.check_output(['git','-C',REPO,'show',PIN+':'+REL]);current=(ROOT/REL).read_bytes();scope={}
assert base.count(b'_HEX40.match(gsha)')==2
scope['exact_two_call_changes']=current==base.replace(b'_HEX40.match(gsha)',b'_HEX40.fullmatch(gsha)')
sys.path.insert(0,str(ROOT/'scripts'))
import run_network_194_parallel as runner
import supp20_input_receipt as receipt
scope['runner_not_sealed']=REL not in runner.CODE_FILES
scope['sealed32_unchanged']=len(runner.CODE_FILES)==32 and all((ROOT/p).read_bytes()==subprocess.check_output(['git','-C',REPO,'show',PIN+':'+p]) for p in runner.CODE_FILES)
scope['receipt_unchanged']=(ROOT/'scripts/supp20_input_receipt.py').read_bytes()==subprocess.check_output(['git','-C',REPO,'show',PIN+':scripts/supp20_input_receipt.py'])
scope['deliverable_equals_test_source']=(Path('/workspace/.cloud-setup/nonrint-20261024/lhs-readiness/deliverables')/REL).read_bytes()==current
oldtree=ast.parse(base);newtree=ast.parse(current)
def functions(t):return {x.name:ast.dump(x,include_attributes=False) for x in t.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
f0,f1=functions(oldtree),functions(newtree);scope['only_preflight_AST_changed']={k for k in f0 if f0[k]!=f1[k]}=={'preflight_receipt_checks'}
oldnode=next(x for x in oldtree.body if isinstance(x,ast.FunctionDef) and x.name=='preflight_receipt_checks');ns=dict(runner.__dict__);exec(compile(ast.Module(body=[oldnode],type_ignores=[]),'pinned_baseline_preflight_receipt_checks','exec'),ns);oldfn=ns['preflight_receipt_checks'];fn=runner.preflight_receipt_checks
cases=[];triggered=False

def hook(path,*a,**kw):
 global triggered
 initial=fn(path,*a,**kw)
 if triggered or not initial.get('checks') or not all(c['ok'] for c in initial['checks']):return initial
 triggered=True;p=Path(path);before=p.read_bytes();rec=json.loads(before);pin=rec['git']['sha'];assert len(pin)==40
 (OUT/'fixture.original.json').write_bytes(before);(OUT/'fixture.log').write_bytes(Path(initial['log']['path']).read_bytes())
 variants={'normal':pin,'LF':pin+'\n','CRLF':pin+'\r\n','double_LF':pin+'\n\n','space':pin+' ','tab':pin+'\t','NUL':pin+'\0','leading_LF':'\n'+pin,'middle_LF':pin[:20]+'\n'+pin[20:],'zero_width':pin+'\u200b','unicode_digit':'１'+pin[1:],'uppercase':pin.upper(),'short39':pin[:-1],'long41_hex':pin+'0','null':None,'bool':True,'integer':123,'list':[pin],'dict':{'sha':pin},'wrong_last_hex':pin[:-1]+('0' if pin[-1]!='0' else '1')}
 try:
  for label,value in variants.items():
   for approval in [pin,pin[:7],None]:
    rec['git']['sha']=value;p.write_text(json.dumps(rec),encoding='utf-8');actual=fn(p,expect_set='supp20',approved_sha=approval);bad=[c['id'] for c in actual['checks'] if not c['ok']]
    if label=='normal':expected=[]
    elif label=='wrong_last_hex':expected=['P10'] if approval==pin else []
    else:expected=['P7']+(['P10'] if approval else [])
    cases.append({'case':label,'approval':'full40' if approval==pin else 'prefix7' if approval else 'omitted','actual_bad':bad,'expected_bad':expected,'pass':bad==expected})
  rec['git']['sha']=pin+'\n';p.write_text(json.dumps(rec),encoding='utf-8');old=oldfn(p,expect_set='supp20',approved_sha=pin);oldbad=[c['id'] for c in old['checks'] if not c['ok']];scope['old_LF_counterexample_reproduced']=oldbad==[]
 finally:p.write_bytes(before)
 return initial
runner.preflight_receipt_checks=hook
try:
 with (OUT/'canonical_receipt_selftest.log').open('w') as log:
  with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):rc=receipt._selftest()
finally:runner.preflight_receipt_checks=fn
scope['canonical_selftest_rc0']=rc==0;scope['fixture_observed']=triggered;scope['source_unchanged_during_attack']=(ROOT/REL).read_bytes()==current
lines=(OUT/'canonical_receipt_selftest.log').read_text().splitlines();scope['canonical123_summary']='supp20_input_receipt selftest: 123/123 PASS' in lines[-1]
failed=[k for k,v in scope.items() if not v]+[f"{c['case']}:{c['approval']}" for c in cases if not c['pass']]
result={'status':'PASS' if not failed else 'FAIL','base_pin':PIN,'runner_before_sha256':sha(base),'runner_after_sha256':sha(current),'scope_checks':scope,'attack_cases':cases,'case_count':len(cases),'canonical_selftest_rc':rc,'canonical_last_line':lines[-1],'canonical_log_sha256':sha((OUT/'canonical_receipt_selftest.log').read_bytes()),'failures':failed,'scope':'Direct canonical preflight function attacks on synthetic existing selftest receipt; no WSL/B7 real approval, production launch or fullgate.'}
(OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='attack_cases'},ensure_ascii=False,indent=2));raise SystemExit(bool(failed))
