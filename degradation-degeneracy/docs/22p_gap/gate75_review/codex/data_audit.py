"""Reviewer-owned, data-only inspection. No subject module imports or executions."""
from pathlib import Path, PurePosixPath
import hashlib, json, subprocess, sys, zipfile, stat
O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g75_20260927')
D = W / 'degradation-degeneracy'
sys.path.insert(0, str(O.parents[1] / 'work/gate26-pydeps'))
import yaml
H = 'ef6689bbe296e545df57dc481e45ec98c2b9ea3b'
C = 'ebfb853d1b3dff0678f5f67985003498a3476982'
OLD = 'a49a021833282e0bd04c4565591668dc323e9630'
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    if (O/n).exists():
        assert json.loads((O/n).read_bytes())==v,n
        return
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=False,indent=2,default=str);f.write('\n')
def raw(ref,p):return git('show',ref+':degradation-degeneracy/'+p)
def obj(p):return yaml.safe_load((D/p).read_bytes())
def delta(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return sum((delta(a.get(k),b.get(k),path+'/'+str(k)) for k in sorted(a.keys()|b.keys())),[])
    return [] if a==b else [{'path':path,'before':a,'after':b}]
assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
tracked=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
write('SOURCE_BEFORE.json',{p:ident((W/p).read_bytes()) for p in tracked})
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
sp=git('ls-files','-z','--',*scope).decode().strip('\0').split('\0')
hd=hashlib.sha256()
for p in sorted(sp):hd.update(p.removeprefix('degradation-degeneracy/').encode());hd.update((W/p).read_bytes())
assert hd.hexdigest()[:16]=='27390883eb132941'
diffs={}
for name,a,b,paths in [
    ('CODE_TO_HEAD_SCOPE',C,H,scope),('G74_TO_G75_SCOPE',OLD,H,scope),
    ('G74_TO_G75_LEDGER',OLD,H,['degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml']),
    ('G74_TO_G75_LINT',OLD,H,['degradation-degeneracy/tests/test_docs_lint.py']),
    ('G74_TO_G75_PLAN',OLD,H,['degradation-degeneracy/docs/22p_gap/plan_leg.py']),
    ('TEST_ONLY_FIX', '8765068a','7ec4e234',['degradation-degeneracy/tests/test_grid.py','degradation-degeneracy/tests/test_docs_lint.py'])]:
    content=git('diff','--no-ext-diff',a,b,'--',*paths)
    (O/(name+'.diff')).write_bytes(content);diffs[name]=ident(content)
assert diffs['CODE_TO_HEAD_SCOPE']['bytes']==0
unchanged={}
for name,paths in {
    'bundles_and_index':['artifacts/artifact_index.yaml',*[f'artifacts/{k}' for k in obj('artifacts/artifact_index.yaml')['runs']]], 'class_registry':['docs/22p_gap/_exec_class'],
    'publisher_and_active_projection':['docs/22p_gap/row_projection.py','docs/22p_gap/proj_g18'],
    'claim_status':['docs/22p_gap/CLAIM_STATUS.yaml'],
    'test_fix_run_scope':None}.items():
    if paths is None:result=git('diff','--name-only','8765068a','7ec4e234','--',*scope)
    else:result=git('diff','--name-only',OLD,H,'--',*['degradation-degeneracy/'+p for p in paths])
    unchanged[name]={'changed':result.decode().splitlines()};assert not result.strip(),name
ledger=obj('docs/22p_gap/LEG_PRESERVATION.yaml');receipts={}
for leg in ('grid_fit_v5','paired_fixed5_v4'):
    p=f'docs/22p_gap/receipts/{leg}.validate.yaml'
    old=raw(OLD,p);new=(D/p).read_bytes();old_o=yaml.safe_load(old);new_o=yaml.safe_load(new)
    history=D/f'docs/22p_gap/receipts/history/{leg}.validate.c2ef1a811e70bb4c.yaml'
    assert history.read_bytes()==old
    core=new_o['core']; calculated=hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode()).hexdigest()
    assert calculated==new_o['core_sha256']
    changes=delta(old_o,new_o)
    assert all(x['path'] in ['/core/identity/validator_source_digest','/core_sha256'] or x['path'].startswith('/stamp/') for x in changes),changes
    assert core['validation']==old_o['core']['validation'] and core['outputs']==old_o['core']['outputs']
    e=next(x for x in ledger['legs'] if x['leg_id']==leg)
    assert e['evidence']['verification_receipt_core_sha256']==calculated
    assert e['evidence']['validator_identity']['source_digest']==core['identity']['validator_source_digest']=='27390883eb132941'
    receipts[leg]={'old':ident(old),'new':ident(new),'history_byte_identical':True,'changes':changes,'core_rehash_matches':True,
        'validation_and_outputs_unchanged':True,'producer_and_validator':core['identity'],'ledger_validation_status':e['validation_status']}
    bundle=D/core['bundle']['uri']
    pi=yaml.safe_load((bundle/'payload_sha256.yaml').read_bytes())
    members={x.relative_to(bundle).as_posix():ident(x.read_bytes()) for x in bundle.rglob('*') if x.is_file()}
    assert set(members)==set(pi)|{'payload_sha256.yaml'}
    assert all(members[k]['sha256']==v for k,v in pi.items())
    assert core['bundle']['payload_index_sha256']==members['payload_sha256.yaml']['sha256']
    assert core['bundle']['files']==len(members) and core['bundle']['bytes']==sum(x['bytes'] for x in members.values())
    outs={x['role']:x for x in core['outputs']}
    assert outs['sealed_summary']['file_sha256']==members['degeneracy_summary.yaml']['sha256']
    assert outs['rescored_summary']['source_file_sha256']==members['fits.parquet']['sha256']
    assert outs['sealed_summary']['semantic_sha256']==outs['rescored_summary']['semantic_sha256']
    assert core['restore']['run_dir_relative']==yaml.safe_load((bundle/'restore_map.yaml').read_bytes())['run_dir']
    if leg=='grid_fit_v5':assert e['evidence']['out']==core['restore']['run_dir_relative']
    receipts[leg]['ledger_out_present']='out' in e['evidence']
    receipts[leg]['bundle']={'members':len(members),'exact_set_SHA':True,'bytes':sum(x['bytes'] for x in members.values())}
zroot=D/'docs/22p_gap/gate74_review'
zips=list(zroot.glob('*.zip'))
prior={}
for zp in zips:
    assert zp.read_bytes()==(O.parent/'gate74_review_20260926'/zp.name).read_bytes()
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
        mn=next(n for n in names if n.endswith('MANIFEST.json'))
        m=json.loads(z.read(mn));files=m['files']
        prefix=mn.removesuffix('MANIFEST.json')
        assert set(names)=={prefix+k for k in files}|{mn}
        for n,v in files.items():
            info=z.getinfo(prefix+n);q=PurePosixPath(n)
            assert not q.is_absolute() and '..' not in q.parts and not stat.S_ISLNK(info.external_attr>>16)
            assert ident(z.read(prefix+n))==v
        prior[zp.name]={'zip':ident(zp.read_bytes()),'payload':len(files),'manifest':ident(z.read(mn)),'CRC_exact_set_SHA':True}
report={'head':H,'code':C,'prior_head':OLD,'source_digest':hd.hexdigest()[:16],'RUN_SCOPE_files':len(sp),'tracked_files':len(tracked),
    'diffs':diffs,'unchanged':unchanged,'receipts':receipts,'prior_review_packages':prior,
    'grid_fit_v5_record':next(x for x in ledger['legs'] if x['leg_id']=='grid_fit_v5'),
    'g18':next(x for x in ledger['cohorts'] if x['cohort_id']=='g18_2026_09_15'),
    'limits':{'subject_module_imports':0,'full_suite_reruns':0,'scientific_runs_restore_class_changes':0,'sender_native_execution_independently_observed':False}}
write('DATA_AUDIT.json',report)
refs=['docs/22p_gap/GATE75_REQUEST.md','docs/22p_gap/GATE74_REQUEST.md','docs/22p_gap/LEG_PRESERVATION.yaml',
      'docs/22p_gap/plan_leg.py','docs/22p_gap/row_projection.py','docs/22p_gap/make_receipt.py','docs/22p_gap/proj_g18/CURRENT',
      'tools/preserve.py','scripts/archive_results.sh','tests/test_gate74_defensive.py','tests/test_docs_lint.py',
      'docs/22p_gap/CLAIM_STATUS.yaml','artifacts/artifact_index.yaml']
refs += [p.relative_to(D).as_posix() for p in (D/'docs/22p_gap/receipts').rglob('*.yaml') if p.name.startswith(('grid_fit_v5.','paired_fixed5_v4.'))]
for n in refs:
    to=O/'reference'/n;to.parent.mkdir(parents=True,exist_ok=True);to.write_bytes((D/n).read_bytes())
response=(D/'docs/08_REVIEW_RESPONSE.md').read_text(encoding='utf-8')
(O/'reference/RESPONSE_SECTIONS102_103.txt').write_text(response[response.index('## §102 '):],encoding='utf-8')
print(json.dumps({'status':'DATA_AUDIT_PASS','head':H,'scope_files':len(sp),'tracked':len(tracked),'receipts':list(receipts),'prior_packages':prior},ensure_ascii=False))
