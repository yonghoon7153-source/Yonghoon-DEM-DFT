"""New static AST/bytes/text/JSON inspector; does NOT import/call candidate code."""
from pathlib import Path
import ast, json, hashlib, difflib, re, sys, time, datetime
OUT=Path(__file__).resolve().parents[1];BASE=OUT.parent/'microshort_s1o_20261007_133011'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,x): (OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def check(name,ok,detail=None):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok: raise ValueError('STATIC_CHECK_FAILED:'+name)
def funcs(p):
    raw=p.read_bytes();src=raw.decode('utf-8');lines=src.splitlines(True);tree=ast.parse(src,filename=str(p))
    found={}
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
            first=min([n.lineno]+[d.lineno for d in getattr(n,'decorator_list',[])])
            span=''.join(lines[first-1:n.end_lineno]).encode()
            found[n.name]={'start_line':first,'end_line':n.end_lineno,'bytes':len(span),'sha256':sha(span),'span':span}
    return tree,found
def ps_funcs(raw):
    marks=list(re.finditer(rb'^function ([A-Za-z0-9_]+)\(',raw,re.M));result={}
    for i,m in enumerate(marks):
        end=marks[i+1].start() if i+1<len(marks) else raw.index(b"throw 'S1O_OFFLINE_ONLY",m.start())
        result[m.group(1).decode()]=raw[m.start():end]
    return result

try:
    original=read(BASE/'CODE_MANIFEST.json')
    allowed={'candidate/consumer.py.inactive.txt','candidate/Parent.ps1.inactive.txt','candidate/variants/P0.java.inactive.txt','candidate/variants/P0.diff.txt','contracts/CHARGE_BALANCE.json','contracts/EXECUTION_BINDING.json','SOURCE_CONTRACT_LINKS.json'}
    changes=[];diffs=[]
    for f in original['files']:
        if f['path']=='VALIDATION_PLAN.json': continue # historical plan moves under reference; R1 plan sealed separately
        p=OUT/f['path'];old=(BASE/f['path']).read_bytes();new=p.read_bytes()
        check('original_pin:'+f['path'],len(old)==f['bytes'] and sha(old)==f['sha256'])
        if old!=new:
            check('authorized_changed_file:'+f['path'],f['path'] in allowed)
            changes.append({'path':f['path'],'old_bytes':len(old),'old_sha256':sha(old),'new_bytes':len(new),'new_sha256':sha(new)})
            diffs.extend(difflib.unified_diff(old.decode('utf-8').splitlines(True),new.decode('utf-8').splitlines(True),fromfile='original/'+f['path'],tofile='R1/'+f['path']))
        else: check('unchanged:'+f['path'],True)
    index={}
    for rel in ('candidate/consumer.py.inactive.txt','candidate/control.py.inactive.txt'):
        tree,now=funcs(OUT/rel);oldtree,old=funcs(BASE/rel)
        check('python_static_parse:'+rel,True)
        permitted={'charge_balance','analyze'} if 'consumer' in rel else set()
        check('python_no_unexpected_function_set:'+rel,set(now)==set(old))
        for name in old:
            if name not in permitted: check('unchanged_function:'+name,now[name]['span']==old[name]['span'])
        index[rel]={k:{a:v for a,v in spec.items() if a!='span'} for k,spec in now.items()}
        if 'consumer' in rel:
            literals=lambda t:{n.args[0].value for n in ast.walk(t) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Decimal' and n.args and isinstance(n.args[0],ast.Constant)}
            check('Decimal_literal_set_unchanged',literals(tree)==literals(oldtree),sorted(str(x) for x in literals(tree)))
            text=(OUT/rel).read_text(encoding='utf-8')
            for s in ('safe==native_times[-2]',"list(global_rows)==native_times", "'CHARGE_GLOBAL_LI_MISMATCH'", "value < -q_abs", "error.details={'first_violation':first}","source_binding=charge_proof"):
                check('N1_N2_required_text:'+s,s in text)
    pold=ps_funcs((BASE/'candidate/Parent.ps1.inactive.txt').read_bytes());pnew=ps_funcs((OUT/'candidate/Parent.ps1.inactive.txt').read_bytes())
    for name in ('S1Has','S1Struct','S1Number','S1Sha','S1Failure','S1FinalReturn'):
        check('unchanged_parent_function:'+name,pold[name]==pnew[name])
    parse=read(OUT/'PARENT_STATIC_PARSE.json')
    check('parent_parser_no_errors',not parse['errors'])
    check('parent_parser_bound_to_current',parse['source_sha256']==sha((OUT/'candidate/Parent.ps1.inactive.txt').read_bytes()))
    index['candidate/Parent.ps1.inactive.txt']=parse['functions']
    p0=(OUT/'candidate/variants/P0.java.inactive.txt').read_bytes();p0old=(BASE/'candidate/variants/P0.java.inactive.txt').read_bytes()
    check('P0_only_log_literal_reverse',p0.replace(b'|strict|accepted tsteps storage|eventout|',b'|strict|requested tlist storage|eventout|')==p0old)
    check('P0_tout_setting_unchanged',b'.set("tout","tsteps")' in p0)
    for n in ('INITIALIZATION','COEFFICIENT_READBACK','COST_MODEL','K_DESIGN','POLICY_VARIANTS','RESOURCE_CONTRACT'):
        check('untouched_contract:'+n,(OUT/f'contracts/{n}.json').read_bytes()==(BASE/f'contracts/{n}.json').read_bytes())
    charge=read(OUT/'contracts/CHARGE_BALANCE.json');oldcharge=read(BASE/'contracts/CHARGE_BALANCE.json')
    for key in ('F_C_mol','A_c_m2','L_sep_m','current_balance','charge_definitions','charge_balance','total_li','sign_deadbands','threshold_change_policy'):
        check('unchanged_charge_physics_or_limits:'+key,charge[key]==oldcharge[key])
    for p in (OUT/'contracts').glob('*.json'):
        data=read(p)
        check('contract_json_parse:'+p.name,True)
        check('contract_not_activated:'+p.name,all(data.get(k,False) is False for k in ('approved','usable','native_ready')))
    binding=read(OUT/'contracts/EXECUTION_BINDING.json');oldbinding=read(BASE/'contracts/EXECUTION_BINDING.json')
    for key in ('phase_limits_s','overall_limit_s','counts','resource_contract_sha256'):
        check('native_proposal_unchanged:'+key,binding['unit'][key]==oldbinding['unit'][key])
    check('native_adapters_still_open',binding['adapter_status']=='UNIMPLEMENTED_OPEN' and binding['unit']['commands']['native_compile_argv'] is None)
    check('no_runtime_dirs',not any((OUT/n).exists() for n in ('future_run','future_run_001','future_parent','future_parent_001','future_authorizations','future_validation_fixture_R1_001')))
    origins=read(OUT/'ORIGINALS_BEFORE.json')
    for row in origins:
        p=Path(row['path']);raw=p.read_bytes()
        check('original_preserved:'+str(p.relative_to(BASE)),len(raw)==row['bytes'] and sha(raw)==row['sha256'])
    save('SOURCE_INDEX_R1.json',index);save('CHANGED_FILES.json',changes)
    (OUT/'MINIMAL_DIFF.txt').write_text(''.join(diffs),encoding='utf-8',newline='')
    save('STATIC_AUDIT_R1.json',{'status':'PASS_STATIC_ONLY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'count':len(checks),'functional_validation':'NOT_RUN','candidate_imports':0,'candidate_function_calls':0,'COMSOL':0,'JVM':0,'original_files_checked':len(origins),'static_scope':'AST parse, raw byte equality, text and JSON checks only; no execution of fixtures or candidate functions','python_executable':{'path':sys.executable,'sha256':sha(Path(sys.executable).read_bytes())}})
    print(json.dumps({'kind':'R1_STATIC_AUDIT','checks':len(checks),'status':'PASS_STATIC_ONLY','changed_files':len(changes),'original_files':len(origins),'functional_validation':'NOT_RUN'}))
except Exception as exc:
    save('STATIC_FIRST_ERROR.json',{'error':str(exc),'checks_completed':checks,'candidate_executed':False})
    raise
