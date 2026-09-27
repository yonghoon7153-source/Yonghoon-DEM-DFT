"""Reviewer-owned isolated checks of Gate75 residuals in Gate76.
Allowlisted AST predicates and exact index heredocs only. No subject imports,
pytest, archive/restore/attach/scientific programs or production writes.
"""
from pathlib import Path
import ast, builtins, copy, hashlib, io, json, os, re, secrets, subprocess, sys, types, unicodedata
from contextlib import redirect_stdout, redirect_stderr
O=Path(__file__).resolve().parent
D=Path('C:/Users/Administrator/Documents/Codex/g76_20260927/degradation-degeneracy')
sys.path.insert(0,str(O.parents[1]/'work/gate26-pydeps'))
import yaml
F=O/'fixtures01';F.mkdir(exist_ok=False)
P=D/'tools/preserve.py';L=D/'tests/test_docs_lint.py';S=D/'scripts/archive_results.sh';Y=D/'tools/index_yaml.py'
trace=[];results=[]
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def extract(path,ns,functions=(),constants=()):
    src=path.read_text(encoding='utf-8');tree=ast.parse(src);selected=[]
    for n in tree.body:
        nm=n.name if isinstance(n,(ast.FunctionDef,ast.ClassDef)) else None
        keys=[x.id for x in n.targets if isinstance(x,ast.Name)] if isinstance(n,ast.Assign) else []
        if nm in functions or any(k in constants for k in keys):
            selected.append(n)
            trace.append({'file':path.relative_to(D).as_posix(),'line':n.lineno,'end':n.end_lineno,
                          'name':nm or keys,'source_segment':ident(ast.get_source_segment(src,n).encode())})
    assert set(functions)<={getattr(n,'name',None) for n in selected}
    assert set(constants)<={x.id for n in selected if isinstance(n,ast.Assign) for x in n.targets if isinstance(x,ast.Name)}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(path)+'[allowlisted AST]','exec'),ns)
def outcome(fn):
    try:return {'accepted':True,'result':fn()}
    except Exception as e:return {'accepted':False,'type':type(e).__name__,'message':str(e)}
def record(id,kind,result):results.append({'id':id,'scope':kind,**result})
ns={'Path':Path,'hashlib':hashlib,'json':json,'secrets':secrets,'re':re,'unicodedata':unicodedata,'REPO_ROOT':D}
consts=['VERIFICATION_RECEIPT_KEYS','VERIFICATION_RECEIPT_CORE_KEYS','VERIFICATION_RECEIPT_BUNDLE_KEYS',
 'VERIFICATION_RECEIPT_RESTORE_KEYS','VERIFICATION_RECEIPT_VALIDATION_KEYS','VERIFICATION_RECEIPT_IDENTITY_KEYS',
 'VERIFICATION_RECEIPT_SCHEMA_VERSION','VERIFICATION_RECEIPT_OUTPUT_KEYS','VERIFICATION_RECEIPT_GENERATOR','_HEX16','_HEX64','CLAIM_SCOPE']
extract(P,ns,['PreserveError','_nonempty_str','_is_hex64','_repo_relative_or_refuse','_receipt_core_sha256',
 '_receipt_output_pair','read_verification_receipt','_assert_receipt_bound_to_bundle','_assert_ledger_run_bound'],consts)
audit=json.loads((O/'DATA_AUDIT.json').read_bytes());assert audit['source_digest']=='1c67a748598baadb'
src=types.ModuleType('src');srcio=types.ModuleType('src.io');srcio.source_digest=lambda:audit['source_digest']
src.io=srcio;sys.modules['src']=src;sys.modules['src.io']=srcio
tools=types.ModuleType('tools');pred=types.ModuleType('tools.preserve');pred.__dict__.update(ns)
tools.preserve=pred;sys.modules['tools']=tools;sys.modules['tools.preserve']=pred
ln={'Path':Path,'hashlib':hashlib,'_REPO':D,'_PRESERVE':D/'docs/22p_gap/LEG_PRESERVATION.yaml'}
extract(L,ln,['_no_active_claim_evidence_problems'],['_NO_ACTIVE_CLAIM_EVIDENCE_KEYS'])
ledger=yaml.safe_load(ln['_PRESERVE'].read_bytes())
core=ns['read_verification_receipt']('docs/22p_gap/receipts/grid_fit_v5.validate.yaml','grid_fit_v5',repo_root=D)
bound=ns['_assert_receipt_bound_to_bundle'](core,D/'artifacts/grid_fit_v5','grid_fit_v5')
assert bound=='results/grid_fit_v5'
missing=object()
outcases=[('D00_valid','results/grid_fit_v5'),('D01_other','results/OTHER_RUN'),
 ('D02_old_leg','results/grid_fit_v4'),('D03_artifact','artifacts/grid_fit_v5'),
 ('D04_suffix','results/grid_fit_v5x'),('D05_child','results/grid_fit_v5/sub'),
 ('D06_missing',missing),('D07_empty',''),('D08_blank','   '),('D09_number',17),
 ('D10_list',['results/grid_fit_v5']),('D11_trailing_slash','results/grid_fit_v5/')]
for id,value in outcases:
    data=copy.deepcopy(ledger);leg=next(e for e in data['legs'] if e['leg_id']=='grid_fit_v5')
    if value is missing:leg['evidence'].pop('out')
    else:leg['evidence']['out']=value
    fixture=F/(id+'.yaml');fixture.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
    before=ident(fixture.read_bytes())
    problems=ln['_no_active_claim_evidence_problems'](data)
    producer=outcome(lambda:ns['_assert_ledger_run_bound'](leg['evidence'],bound,'grid_fit_v5',leg['preservation_status']))
    expected=id in ('D00_valid','D11_trailing_slash')
    assert (not problems)==producer['accepted']==expected,(id,problems,producer)
    assert before==ident(fixture.read_bytes())
    record(id,'exact diagnostic consumer + exact producer out predicate; typed real receipt and bundle read only',
           {'accepted':not problems,'expected_acceptance':expected,'problems':problems,'producer':producer,'fixture_unchanged':True})

# Strict loader definitions only: no subject module imported.
yn={'yaml':yaml}
extract(Y,yn,['DuplicateKeyError','IndexShapeError','MergeKeyError','_StrictLoader','load_index_strict'],['_MERGE_TAG'])
ym=types.ModuleType('tools.index_yaml');ym.__dict__.update(yn);sys.modules['tools.index_yaml']=ym
shell=S.read_text(encoding='utf-8')
def heredoc(marker,start=0):
    a=shell.index("<<'"+marker+"'",start);a=shell.index('\n',a)+1
    return shell[a:shell.index('\n'+marker,a)]
pre=heredoc('PYIDX');same=heredoc('PYSAME')
final_start=shell.index('index_ok=1\n')
fin=heredoc('PYEOF',final_start)
for marker,body in [('PYIDX',pre),('PYSAME',same),('FINAL_INDEX',fin)]:
    (F/(marker+'.py.txt')).write_text(body,encoding='utf-8',newline='\n')
    assert body.count('load_index_strict(')==1
class ProbeExit(BaseException):
    def __init__(self,code):self.code=code
def leave(code):raise ProbeExit(code)
def never(*a,**kw):raise AssertionError('scientific/project operation not allowed')
realimport=builtins.__import__
bodies={
 'I00_valid':('runs:\n  preserved: {payload_index_sha256: "'+'a'*64+'"}\n',True),
 'I01_duplicate_runs':('runs:\n  preserved: {}\nruns: {}\n',False),
 'I02_duplicate_run':('runs:\n  x: {}\n  x: {}\n',False),
 'I03_duplicate_identity':('runs:\n  x: {payload_index_sha256: a, payload_index_sha256: b}\n',False),
 'I04_merge_override':('base: &b {payload_index_sha256: a}\nruns:\n  x: {<<: *b, payload_index_sha256: b}\n',False),
 'I05_merge_nonoverlap':('base: &b {payload_index_sha256: a}\nruns:\n  x: {<<: *b}\n',False),
 'I06_wrong_shape':('runs: 5\n',False),
 'I07_empty':('',False),
 'I08_valid_alias':('base: &b {payload_index_sha256: a}\nruns:\n  x: *b\n',True),
}
def run_part(body,argv,folder,mode='normal'):
    output=io.StringIO();errors=io.StringIO()
    fsys=types.SimpleNamespace(argv=argv,stdout=output,stderr=errors)
    def replace(a,b):
        assert Path(a).parent==folder and Path(b)==folder/'artifact_index.yaml'
        if mode=='replace_failure':raise OSError(5,'reviewer injected replace failure')
        os.replace(a,b)
    class FixturePath(type(Path())):
        def write_text(self,*args,**kwargs):
            assert self.parent==folder and self.name.startswith('.artifact_index.')
            if mode=='partial_write_failure':
                super().write_text('partial',encoding='utf-8')
                raise OSError(28,'reviewer injected partial write failure')
            return super().write_text(*args,**kwargs)
    fos=types.SimpleNamespace(_exit=leave,path=os.path,environ={},getpid=lambda:76001,replace=replace)
    def importer(name,*a,**kw):
        if name=='os':return fos
        if name=='sys':return fsys
        if name=='pathlib':return types.SimpleNamespace(Path=FixturePath)
        if name in ('src.io','tools.archive_bundle'):return types.SimpleNamespace(file_digest=never,artifact_kind=never)
        return realimport(name,*a,**kw)
    b=dict(vars(builtins));b['__import__']=importer
    try:
        with redirect_stdout(output),redirect_stderr(errors):exec(compile(body,'[exact index heredoc]','exec'),{'__builtins__':b})
        result={'rc':0,'normal_return':True}
    except ProbeExit as e:result={'rc':e.code}
    except Exception as e:result={'rc':1,'type':type(e).__name__,'message':str(e)}
    return {**result,'stdout':output.getvalue(),'stderr':errors.getvalue()}
for name,(body,expected) in bodies.items():
    direct=outcome(lambda:yn['load_index_strict'](body));assert direct['accepted']==expected,(name,direct)
    for reader,program in [('preflight',pre),('same_name',same),('merge',fin)]:
        folder=F/(name+'_'+reader);folder.mkdir()
        index=folder/'artifact_index.yaml';index.write_text(body,encoding='utf-8');before=ident(index.read_bytes())
        # Different candidate name deliberately avoids same-identity policy; tests only reader rejection.
        argv=['-',str(index)] if reader=='preflight' else (['-',str(index),'unused_new_name','unused_pi'] if reader=='same_name' else ['-',str(folder)])
        result=run_part(program,argv,folder)
        assert (result['rc']==0)==expected,(name,reader,result)
        after=ident(index.read_bytes())
        if not expected or reader!='merge':assert before==after
        else:assert yaml.safe_load(index.read_bytes())['runs']==direct['result']['runs']
        record(name+'_'+reader,'exact shared loader and reader heredoc; merge names=[]; fixture only',
          {'expected_acceptance':expected,'direct_loader':direct,**result,'before':before,'after':after,'index_unchanged':before==after})
for mode in ('normal','replace_failure','partial_write_failure'):
    folder=F/('W_'+mode);folder.mkdir();index=folder/'artifact_index.yaml'
    index.write_text(bodies['I00_valid'][0],encoding='utf-8');before=ident(index.read_bytes())
    result=run_part(fin,['-',str(folder)],folder,mode)
    after=ident(index.read_bytes());temps=list(folder.glob('.artifact_index.*.tmp'))
    assert (result['rc']==0)==(mode=='normal') and not temps
    if mode!='normal':assert before==after
    record('W_'+mode,'exact index finalizer; injected own-fixture filesystem error',
           {**result,'before':before,'after':after,'index_unchanged':before==after,'temporary_files':[]})

# Exact shell wrapper/footer, only the index command replaced by a chosen rc.
end=shell.index('\nPYEOF',shell.index("<<'PYEOF'",final_start))+len('\nPYEOF')
cmd_start=shell.index('if ! "$PY"',final_start)
env=dict(os.environ);env['PATH']='C:/Program Files/Git/usr/bin;C:/Program Files/Git/bin;'+env.get('PATH','')
for code in (0,17):
    body='set -uo pipefail\nDEST="$PWD"\npromoted=(fixture)\nn_want=1\nn_ok=1\nn_bad=0\nn_missing=0\n'
    body+=shell[final_start:cmd_start]+f'if ! (exit {code})\n'+shell[end:]
    path=F/f'shell_index_rc{code}.sh';path.write_text(body,encoding='utf-8',newline='\n')
    cp=subprocess.run(['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc',path.as_posix()],cwd=F,env=env,capture_output=True,timeout=20)
    stdout=cp.stdout.decode('utf-8','replace');stderr=cp.stderr.decode('utf-8','replace')
    assert cp.returncode==(0 if code==0 else 1)
    assert ('git add artifacts' in stdout)==(code==0)
    if code:assert '이미 승격된 묶음: fixture' in stderr and '미완' in stderr
    record('S'+str(code),'exact shell wrapper/footer with index command rc injected; no bundle operation',
           {'index_command_rc':code,'shell_rc':cp.returncode,'stdout':stdout,'stderr':stderr})
report={'head':audit['head'],'source_identities':{str(p.relative_to(D)):ident(p.read_bytes()) for p in (P,L,S,Y)},
 'extracted_source_nodes':trace,'cases':results,'case_count':len(results),
 'counts':{'out_binding':len(outcases),'three_reader_cases':len(bodies)*3,'writer':3,'shell_rc':2},
 'adapters':['independently computed source_digest','AST-only tools.preserve/index_yaml namespaces',
             'os._exit captured, sys streams captured','writer uses names=[] and raising unused scientific imports',
             'partial write/replace errors only on reviewer-owned files','shell index command replaced, exact wrapper/footer retained'],
 'limits':{'whole_subject_module_imports':0,'whole_archive_restore_attach_or_science_runs':0,'full_suite':0,'production_writes':0}}
with (O/'DECISION_PROBES.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'ALL_SCOPED_CHECKS_PASS','case_count':len(results),'counts':report['counts']},ensure_ascii=False))
