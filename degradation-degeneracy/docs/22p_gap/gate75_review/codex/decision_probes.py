"""Isolated reviewer probes: allowlisted AST predicates, index heredocs, shell rc boundary.
Never import subject modules; never run archive/restore/fit/publisher or pytest.
Writes are confined to this review's fresh fixture directory.
"""
from pathlib import Path
import ast, copy, hashlib, io, json, os, re, secrets, stat, subprocess, sys, types, unicodedata
from contextlib import redirect_stdout, redirect_stderr
O=Path(__file__).resolve().parent
D=Path('C:/Users/Administrator/Documents/Codex/g75_20260927/degradation-degeneracy')
sys.path.insert(0,str(O.parents[1]/'work/gate26-pydeps'))
import yaml
F=O/'fixtures02';F.mkdir(exist_ok=False)
P=D/'tools/preserve.py';L=D/'tests/test_docs_lint.py';S=D/'scripts/archive_results.sh'
trace=[];results=[]
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def extract(path,ns,functions=(),constants=()):
    src=path.read_text(encoding='utf-8');tree=ast.parse(src);selected=[]
    for node in tree.body:
        nm=node.name if isinstance(node,(ast.FunctionDef,ast.ClassDef)) else None
        keys=[x.id for x in node.targets if isinstance(x,ast.Name)] if isinstance(node,ast.Assign) else []
        if nm in functions or any(k in constants for k in keys):
            selected.append(node)
            trace.append({'file':path.relative_to(D).as_posix(),'line':node.lineno,'end':node.end_lineno,
                'name':nm or keys,'source_segment':ident(ast.get_source_segment(src,node).encode())})
    assert set(functions)<={getattr(n,'name',None) for n in selected}
    assert set(constants)<={x.id for n in selected if isinstance(n,ast.Assign) for x in n.targets if isinstance(x,ast.Name)}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path)+'[allowlisted AST]', 'exec'),ns)
def outcome(fn):
    try:return {'accepted':True,'result':fn()}
    except Exception as e:return {'accepted':False,'type':type(e).__name__,'message':str(e)}
def record(id,kind,result):results.append({'id':id,'scope':kind,**result})
ns={'Path':Path,'hashlib':hashlib,'json':json,'secrets':secrets,'re':re,'unicodedata':unicodedata,'stat':stat,'REPO_ROOT':D}
consts=['VERIFICATION_RECEIPT_KEYS','VERIFICATION_RECEIPT_CORE_KEYS','VERIFICATION_RECEIPT_BUNDLE_KEYS',
 'VERIFICATION_RECEIPT_RESTORE_KEYS','VERIFICATION_RECEIPT_VALIDATION_KEYS','VERIFICATION_RECEIPT_IDENTITY_KEYS',
 'VERIFICATION_RECEIPT_SCHEMA_VERSION','VERIFICATION_RECEIPT_OUTPUT_KEYS','VERIFICATION_RECEIPT_GENERATOR','_HEX16','_HEX64','CLAIM_SCOPE']
funcs=['PreserveError','_nonempty_str','_is_hex64','_repo_relative_or_refuse','_receipt_core_sha256','_receipt_output_pair',
       'read_verification_receipt','_assert_receipt_bound_to_bundle','_assert_ledger_run_bound','_assert_prospective_plan_is_startable']
extract(P,ns,funcs,consts)
# Source digest adapter is independently calculated from fixed checkout, not a subject module.
audit=json.loads((O/'DATA_AUDIT.json').read_bytes());assert audit['source_digest']=='27390883eb132941'
src=types.ModuleType('src');srcio=types.ModuleType('src.io');srcio.source_digest=lambda:audit['source_digest']
src.io=srcio;sys.modules['src']=src;sys.modules['src.io']=srcio
tools=types.ModuleType('tools');pred=types.ModuleType('tools.preserve');pred.__dict__.update(ns)
tools.preserve=pred;sys.modules['tools']=tools;sys.modules['tools.preserve']=pred
ln={'Path':Path,'hashlib':hashlib,'_REPO':D,'_PRESERVE':D/'docs/22p_gap/LEG_PRESERVATION.yaml'}
extract(L,ln,['_scope_problems','_no_active_claim_evidence_problems','test_full_bundle_claims_are_backed_by_a_real_bundle'],
        ['_CLAIM_SCOPES','_NO_ACTIVE_CLAIM_EVIDENCE_KEYS'])
ledger=yaml.safe_load(ln['_PRESERVE'].read_bytes())
core=ns['read_verification_receipt']('docs/22p_gap/receipts/grid_fit_v5.validate.yaml','grid_fit_v5',repo_root=D)
bound=ns['_assert_receipt_bound_to_bundle'](core,D/'artifacts/grid_fit_v5','grid_fit_v5')
assert bound=='results/grid_fit_v5'
for id,change in [('D00_valid',None),('D01_wrong_out',('out','results/OTHER_RUN')),
                  ('D02_missing_out',('out',None)),('D03_wrong_receipt_core',('verification_receipt_core_sha256','0'*64)),
                  ('D04_unknown_scope',('claim_scope','diagnostic'))]:
    data=copy.deepcopy(ledger);leg=next(e for e in data['legs'] if e['leg_id']=='grid_fit_v5')
    if change:
        k,v=change
        if k=='claim_scope':leg[k]=v
        elif v is None:leg['evidence'].pop(k)
        else:leg['evidence'][k]=v
    fixture=F/(id+'.yaml');fixture.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
    before=ident(fixture.read_bytes());ln['_PRESERVE']=fixture
    problems=ln['_scope_problems'](data)+ln['_no_active_claim_evidence_problems'](data)
    generic=outcome(ln['test_full_bundle_claims_are_backed_by_a_real_bundle'])
    runtime=outcome(lambda:ns['_assert_ledger_run_bound'](leg['evidence'],bound,'grid_fit_v5',leg['preservation_status']))
    record(id,'exact AST predicates + typed receipt reader, no attach/write',{'lint_problems':problems,
      'generic_full_bundle_lint':generic,'existing_runtime_out_predicate':runtime,'fixture_unchanged':before==ident(fixture.read_bytes())})
    if id=='D00_valid':assert problems==[] and generic['accepted'] and runtime['accepted']
    if id=='D01_wrong_out':assert problems==[] and generic['accepted'] and not runtime['accepted']
    if id in ('D02_missing_out','D03_wrong_receipt_core','D04_unknown_scope'):assert problems
for id,value in [('C00_fixed','ab'*32),('C01_null',None),('C02_short','ab'*8),('C03_nonhex','zz'*32),('C04_upper','AB'*32),('C05_number',17)]:
    e={'leg_id':'review_fixture','claim_scope':'no_active_claim','run_spec':{'grid':{'discharged_cache_sha256':value}}}
    result=outcome(lambda:ns['_assert_prospective_plan_is_startable'](e))
    record(id,'exact AST startability predicate',result);assert result['accepted']==(id=='C00_fixed')
for id,e in [('C06_missing_grid',{'leg_id':'L','claim_scope':'no_active_claim','run_spec':{}}),
             ('C07_missing_scope',{'leg_id':'L','run_spec':{'grid':{'discharged_cache_sha256':'ab'*32}}})]:
    result=outcome(lambda:ns['_assert_prospective_plan_is_startable'](e));record(id,'exact AST startability predicate',result);assert not result['accepted']

shell=S.read_text(encoding='utf-8')
def heredoc(marker):
    start=shell.index("<<'"+marker+"'")+len(marker)+4
    return shell[start:shell.index('\n'+marker,start)].lstrip('\n')
pre=heredoc('PYIDX');(F/'index_preflight_exact.py.txt').write_text(pre,encoding='utf-8')
class ProbeExit(BaseException):
    def __init__(self,code):self.code=code
def leave(code):raise ProbeExit(code)
realimport=__import__
def precheck(path):
    fakeos=types.SimpleNamespace(_exit=leave)
    fake_sys=types.SimpleNamespace(argv=['-',str(path)],stdout=io.StringIO(),stderr=io.StringIO())
    def importer(name,*a,**kw):
        if name=='os':return fakeos
        if name=='sys':return fake_sys
        return realimport(name,*a,**kw)
    b=dict(vars(__import__('builtins')));b['__import__']=importer
    try:exec(compile(pre,str(S)+'[PYIDX]','exec'),{'__builtins__':b})
    except ProbeExit as e:return {'rc':e.code,'stdout':fake_sys.stdout.getvalue(),'stderr':fake_sys.stderr.getvalue()}
    raise AssertionError('No preflight exit')
bodies={
 'I00_valid':'runs:\n  preserved: {payload_index_sha256: "'+('a'*64)+'"}\n',
 'I01_bad_shape':'runs: 5\n',
 'I02_duplicate_runs':'runs:\n  preserved: {payload_index_sha256: "'+('a'*64)+'"}\nruns: {}\n',
 'I03_duplicate_run_name':'runs:\n  same: {payload_index_sha256: "'+('a'*64)+'"}\n  same: {payload_index_sha256: "'+('b'*64)+'"}\n',
 'I04_duplicate_identity':'runs:\n  same:\n    payload_index_sha256: "'+('a'*64)+'"\n    payload_index_sha256: "'+('b'*64)+'"\n'}
for id,body in bodies.items():
    path=F/(id+'.yaml');path.write_text(body,encoding='utf-8');before=ident(path.read_bytes())
    result=precheck(path);parsed=yaml.safe_load(body)
    record(id,'exact PYIDX heredoc with only os._exit and sys streams adapted',{
       **result,'parsed':parsed,'fixture_unchanged':ident(path.read_bytes())==before})
    assert result['rc']==(1 if id=='I01_bad_shape' else 0)

# Index finalizer heredoc. names=[] avoids all bundle source/validator operations.
# Project imports provide inert, unused adapters; no module is loaded.
fstart=shell.index("<<'PYEOF'",shell.index('if [[ "${#promoted[@]}" -gt 0 ]]'))
fin=shell[shell.index('\n',fstart)+1:];fin=fin[:fin.index('\nPYEOF')]
(F/'index_finalizer_exact.py.txt').write_text(fin,encoding='utf-8')
for id,body,fail in [('W00_atomic_control',bodies['I00_valid'],False),('W01_replace_failure',bodies['I00_valid'],True),
                     ('W02_duplicate_input_rewrite',bodies['I02_duplicate_runs'],False)]:
    folder=F/id;folder.mkdir();index=folder/'artifact_index.yaml';index.write_text(body,encoding='utf-8');before=ident(index.read_bytes())
    def replace(a,b):
        assert Path(a).parent==folder and Path(b)==index
        if fail:raise OSError(5,'reviewer injected index replace failure')
        os.replace(a,b)
    fakeos=types.SimpleNamespace(getpid=lambda:75001,replace=replace)
    fake_sys=types.SimpleNamespace(argv=['-',str(folder)],stdout=io.StringIO(),stderr=io.StringIO())
    unused=types.SimpleNamespace(file_digest=lambda *a,**kw:(_ for _ in ()).throw(AssertionError('not allowed')),
                                artifact_kind=lambda *a,**kw:(_ for _ in ()).throw(AssertionError('not allowed')))
    def importer(name,*a,**kw):
        if name=='os':return fakeos
        if name=='sys':return fake_sys
        if name in ('src.io','tools.archive_bundle'):return unused
        return realimport(name,*a,**kw)
    b=dict(vars(__import__('builtins')));b['__import__']=importer
    out=io.StringIO()
    with redirect_stdout(out),redirect_stderr(out):result=outcome(lambda:exec(compile(fin,str(S)+'[index heredoc]','exec'),{'__builtins__':b}))
    record(id,'exact index heredoc; no promoted bundle, fixture files only',{
      **result,'before':before,'after':ident(index.read_bytes()),'index_unchanged':before==ident(index.read_bytes()),
      'parsed_after':yaml.safe_load(index.read_bytes()),'output':out.getvalue()})
    assert result['accepted']==(not fail)
    if fail:assert before==ident(index.read_bytes())

# Exact shell control-flow boundary after the index command, replacing only that
# command's body with an injected exit status. No archive command is executed.
start=shell.index('if [[ "${#promoted[@]}" -gt 0 ]]')
end=shell.index('\nPYEOF',start)+len('\nPYEOF')
tail=shell[end:]
assert tail.startswith('\nfi\n')
for code in (0,17):
    script='set -uo pipefail\nDEST="$PWD"\npromoted=(fixture)\nn_want=1\nn_ok=1\nn_bad=0\nn_missing=0\n'
    script+=shell[start:shell.index('\n',start)+1]+f'  (exit {code})\n'+tail
    path=F/f'boundary_rc{code}.sh';path.write_text(script,encoding='utf-8',newline='\n')
    cp=subprocess.run(['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc',path.as_posix()],cwd=F,
       capture_output=True,timeout=20)
    record('S'+str(code),'exact shell finalizer wrapper/footer with injected index-command status',{
      'injected_index_rc':code,'shell_returncode':cp.returncode,'stdout':cp.stdout.decode('utf-8','replace'),
      'stderr':cp.stderr.decode('utf-8','replace'),'script':path.relative_to(O).as_posix()})
    assert cp.returncode==0
report={'scope':'Isolated data/predicate/return-code review; not subject suite or archive execution',
 'head':audit['head'],'source_identities':{str(p.relative_to(D)):ident(p.read_bytes()) for p in (P,L,S)},
 'extracted_functions_constants':trace,'cases':results,'case_count':len(results),
 'adapters':['src.io.source_digest uses independently computed fixed source digest',
   'tools.preserve is allowlisted AST-only namespace', 'PYIDX os._exit -> BaseException; streams captured',
   'index writer uses names=[]; two unused scientific imports replaced by raising adapters',
   'index replace failure injected only in reviewer fixture','shell archive/index command replaced with exit 0 or 17; exact footer retained'],
 'limits':{'whole_subject_module_imports':0,'whole_subject_program_executions':0,'full_suite_runs':0,
 'grid_fit_solve_archive_restore_class_changes':0,'production_file_writes':0,'source_test_fixture_writes_only':True}}
with (O/'DECISION_PROBES.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'PROBES_COMPLETED','cases':len(results),
 'confirmed':['wrong out accepted by new/generic lint but refused by existing runtime predicate',
 'duplicate YAML keys accepted','injected index command rc17 masked to shell rc0']},ensure_ascii=False))
