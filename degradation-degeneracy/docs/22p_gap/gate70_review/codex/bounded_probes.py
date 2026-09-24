"""Bounded receiver checks; records limitations instead of claiming full regression."""
import ast, copy, hashlib, json, os, pathlib, subprocess, sys, time
OUT=pathlib.Path(__file__).resolve().parent
TREE=pathlib.Path('C:/Users/Administrator/Documents/Codex/g70_synthetic_checks/degradation-degeneracy')
sys.path.insert(0,str(TREE))
def save(n,o): (OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,argv,env=None):
    t=time.monotonic();r=subprocess.run(argv,cwd=TREE,env=env,capture_output=True,timeout=90)
    (OUT/(n+'.stdout.bin')).write_bytes(r.stdout);(OUT/(n+'.stderr.bin')).write_bytes(r.stderr)
    row={'argv':list(map(str,argv)),'cwd':str(TREE),'rc':r.returncode,'seconds':time.monotonic()-t}
    save(n+'.json',row);print(json.dumps(row),flush=True);return r
if sys.argv[1]=='branch':
    raw=(TREE/'src/io.py').read_bytes();tree=ast.parse(raw)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_provenance')
    assignment=next(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sdiff' for t in n.targets))
    check=next(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.slice,ast.Constant) and t.slice.value=='start_파일_일치' for t in n.targets))
    module=ast.Module(body=[assignment,check],type_ignores=[])
    code=compile(ast.fix_missing_locations(module),str(TREE/'src/io.py'),'exec')
    base={'source_digest':'5e660a8c73d5663a','git_commit':'0'*40,'git_dirty':False,
          'env':{'python':'3.12'},'input_sha256':{'x':'a'*64},'halfcell_recipe':{'method':'ocp'}}
    cases={}
    alterations={'same':{},'git_commit_only':{'git_commit':'1'*40},
       'source_changed':{'source_digest':'0'*16},'dirty_changed':{'git_dirty':True},
       'dirty_null':{'git_dirty':None},'environment_changed':{'env':{'python':'other'}},
       'input_changed':{'input_sha256':{'x':'b'*64}},'recipe_changed':{'halfcell_recipe':{'method':'ocpbias'}}}
    for name,delta in alterations.items():
        ns={'disk':{**base,**delta},'sp':base.copy(),'checks':{}};exec(code,ns)
        verdict=ns['checks']['start_파일_일치'];cases[name]={'accepted':verdict[0],'different_fields':ns['sdiff']}
        assert verdict[0]==(name in {'same','git_commit_only'})
    reversed_module=copy.deepcopy(module)
    tuples=[n for n in ast.walk(reversed_module) if isinstance(n,ast.Tuple) and any(isinstance(v,ast.Constant) and v.value=='source_digest' for v in n.elts)]
    assert len(tuples)==1
    tuples[0].elts.insert(1,ast.Constant(value='git_commit'))
    ns={'disk':{**base,'git_commit':'1'*40},'sp':base.copy(),'checks':{}}
    exec(compile(ast.fix_missing_locations(reversed_module),'reviewer_tuple_reversal','exec'),ns)
    assert ns['checks']['start_파일_일치'][0] is False
    save('F50B_BRANCH_CASES.json',{'source_sha256':hashlib.sha256(raw).hexdigest(),
      'source_lines':[assignment.lineno,check.end_lineno], 'method':'Unchanged comparison AST nodes only; not complete validate_provenance or original pytest F50b test',
      'cases':cases,'old_tuple_commit_only_rejected':True,'whole_validator_pass_claimed':False})
    # Exact original test bodies, no unrelated matplotlib import.
    test_raw=(TREE/'tests/test_compare.py').read_bytes();parsed=ast.parse(test_raw)
    wanted={'test_dirty_scope_ignores_unrelated_subproject','test_dirty_scope_bypasses_are_closed'}
    nodes=[n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'unchanged_extracted_dirty_tests','exec'),ns)
    rows={}
    for name in sorted(wanted):
        p=TREE.parent/('receiver_'+name);p.mkdir(exist_ok=False)
        ns[name](p);rows[name]={'status':'PASS','original_function_body_unchanged':True,'fixture':str(p)}
    save('DIRTY_EXTRACTED_TESTS.json',{'tests':rows,'scope':'Two original function bodies; not full pytest module collection'})
elif sys.argv[1] in {'io','io-owned-temp'}:
    e=os.environ.copy();e.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for key in ['PYTEST_ADDOPTS','PYTEST_PLUGINS','PYTEST_CURRENT_TEST']:e.pop(key,None)
    nodes=['test_source_digest_covers_full_run_scope','test_run_scope_matcher_shared_with_digest','test_scope_exclusion_helper_is_shared','test_tracked_dirty_is_conservative_for_excluded_paths','test_untracked_requirements_counts_as_critical','test_digest_path_key_is_platform_independent']
    # Select exact existing first five; the path-key test name is inspected separately.
    name='io_scope_tests'; extra=[]
    if sys.argv[1]=='io-owned-temp':
        temp=TREE.parent/'receiver_pytest_temp_02';temp.mkdir(exist_ok=False)
        e['TEMP']=e['TMP']=str(temp)
        name='io_scope_tests_owned_temp'
        extra=['--basetemp='+str(temp/'base')]
    run(name,[sys.executable,'-X','utf8','-B','-m','pytest',*[f'tests/test_io_bookkeeping.py::{n}' for n in nodes[:5]],'--noconftest','-q','-p','no:cacheprovider','--json-report','--json-report-file='+str(OUT/(name+'.pytest.json')),*extra],e)
elif sys.argv[1]=='shell':
    bash='C:/Program Files/Git/bin/bash.exe'
    e=os.environ.copy();e.pop('BASH_ENV',None);e.pop('ENV',None)
    r=run('shell_no_mode',[bash,'--noprofile','--norc','run.sh'],e)
    if b'--mode' not in r.stderr:
        save('SHELL_PROBE_LIMIT.json',{'status':'SHELL_START_FAILED','no_parser_conclusion':True});sys.exit(0)
    assert r.returncode==1
    e['RUN_SH_DRY']='1'
    r=run('shell_all_dry',[bash,'--noprofile','--norc','run.sh','--mode','all','--out','results/receiver_unused','--nproc','1'],e)
    assert r.returncode==0
    lines=r.stdout.decode().splitlines();grid=next(s for s in lines if s.startswith('--mode grid'));fit=next(s for s in lines if s.startswith('--mode fit'))
    import shlex
    for n,line in [('grid_child_parser',grid),('fit_child_parser',fit)]:
        assert '--may-open' in line
        r=run(n,[bash,'--noprofile','--norc','run.sh',*shlex.split(line)],e)
        assert r.returncode==1 and b'--may-open' in r.stderr
    save('ALL_CHILD_PARSER_RESULT.json',{'status':'REPRODUCED_UNSUPPORTED_MAY_OPEN','grid':grid,'fit':fit,
        'scope':'Dry argv construction + actual child parser rejection. No grid/fit/precheck/claim executed.',
        'science_calls':0})
