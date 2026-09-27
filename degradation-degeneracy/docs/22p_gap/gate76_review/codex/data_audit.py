"""Reviewer-owned data-only audit of the fixed Gate76 tree. No subject imports."""
from pathlib import Path, PurePosixPath
import hashlib, json, subprocess, sys, zipfile, stat, re
O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g76_20260927')
D = W / 'degradation-degeneracy'
sys.path.insert(0, str(O.parents[1] / 'work/gate26-pydeps'))
import yaml
H = 'b5e4eadea7794d157d961170247e49d2761bba26'
C = '23c361edbfc92fefcfbf0639b5ac40f61f7ebec7'
OLD = 'ef6689bbe296e545df57dc481e45ec98c2b9ea3b'
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=False,indent=2,default=str);f.write('\n')
def raw(ref,p): return git('show',ref+':degradation-degeneracy/'+p)
def obj(p): return yaml.safe_load((D/p).read_bytes())
def delta(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return sum((delta(a.get(k),b.get(k),path+'/'+str(k)) for k in sorted(a.keys()|b.keys())),[])
    return [] if a==b else [{'path':path,'before':a,'after':b}]
assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
tracked=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
write('SOURCE_BEFORE.json',{p:ident((W/p).read_bytes()) for p in tracked})
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
sp=[p for p in git('ls-files','-z','--',*scope).decode().split('\0') if p]
hd=hashlib.sha256()
for p in sorted(sp): hd.update(p.removeprefix('degradation-degeneracy/').encode());hd.update((W/p).read_bytes())
assert hd.hexdigest()[:16]=='1c67a748598baadb'
diffs={}
for name,a,b,paths in [
    ('CODE_TO_HEAD_SCOPE',C,H,scope),('G75_TO_G76_SCOPE',OLD,H,scope),
    ('G75_TO_G76_LEDGER',OLD,H,['degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml']),
    ('G75_TO_G76_LINT',OLD,H,['degradation-degeneracy/tests/test_docs_lint.py']),
    ('REVIEW_COPY_SCOPE_FIX','4d8dfc52','5b10a79f',['degradation-degeneracy/tests/test_docs_lint.py']),
    ('G74_TEST_WORDING_FIX',OLD,H,['degradation-degeneracy/tests/test_gate74_defensive.py'])]:
    content=git('diff','--no-ext-diff',a,b,'--',*paths)
    (O/(name+'.diff')).write_bytes(content);diffs[name]=ident(content)
assert diffs['CODE_TO_HEAD_SCOPE']['bytes']==0
unchanged={}
for name,paths in {
    'bundles_and_index':['artifacts/artifact_index.yaml',*[f'artifacts/{k}' for k in obj('artifacts/artifact_index.yaml')['runs']]],
    'class_registry':['docs/22p_gap/_exec_class'],
    'publisher_projection_claims':['docs/22p_gap/row_projection.py','docs/22p_gap/proj_g18','docs/22p_gap/CLAIM_STATUS.yaml'],
    'receipt_producer_and_binding':['tools/preserve.py','docs/22p_gap/make_receipt.py'],
    'test_fix_run_scope':[p.removeprefix('degradation-degeneracy/') for p in scope]}.items():
    a,b=('4d8dfc52','5b10a79f') if name=='test_fix_run_scope' else (OLD,H)
    changed=git('diff','--name-only',a,b,'--',*['degradation-degeneracy/'+p for p in paths]).decode().splitlines()
    unchanged[name]=changed;assert not changed,name
ledger=obj('docs/22p_gap/LEG_PRESERVATION.yaml');prior_ledger=yaml.safe_load(raw(OLD,'docs/22p_gap/LEG_PRESERVATION.yaml'))
ledger_changes=delta(prior_ledger,ledger)
# List-containing document: compare the two specific records and all remaining records separately.
assert ledger.keys()==prior_ledger.keys()
legchanges={};receipts={}
for leg in ('grid_fit_v5','paired_fixed5_v4'):
    p=f'docs/22p_gap/receipts/{leg}.validate.yaml'
    current=obj(p);core=current['core']
    core_sha=hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode()).hexdigest()
    assert core_sha==current['core_sha256']
    e=next(x for x in ledger['legs'] if x['leg_id']==leg)
    olde=next(x for x in prior_ledger['legs'] if x['leg_id']==leg)
    legchanges[leg]=delta(olde,e)
    assert {x['path'] for x in legchanges[leg]}=={'/evidence/verification_receipt_core_sha256','/evidence/validator_identity/source_digest'}
    assert e['evidence']['verification_receipt_core_sha256']==core_sha
    assert e['evidence']['validator_identity']['source_digest']==core['identity']['validator_source_digest']=='1c67a748598baadb'
    histories={}
    for digest,ref in [('c2ef1a811e70bb4c','a49a021833282e0bd04c4565591668dc323e9630'),
                       ('27390883eb132941',OLD),('cd2408354486c148','0f6b8a76')]:
        hb=(D/f'docs/22p_gap/receipts/history/{leg}.validate.{digest}.yaml').read_bytes()
        assert hb==raw(ref,p)
        prev=yaml.safe_load(hb)
        assert prev['core']['identity']['validator_source_digest']==digest
        diff=delta(prev,current)
        assert all(x['path'] in ['/core/identity/validator_source_digest','/core_sha256'] or x['path'].startswith('/stamp/') for x in diff)
        assert prev['core']['validation']==core['validation'] and prev['core']['outputs']==core['outputs']
        histories[digest]={'identity':ident(hb),'byte_identical_to_commit':ref,'changes_to_current':diff}
    bundle=D/core['bundle']['uri'];pi=yaml.safe_load((bundle/'payload_sha256.yaml').read_bytes())
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
    if leg=='grid_fit_v5': assert e['evidence']['out']==core['restore']['run_dir_relative']
    receipts[leg]={'current':ident((D/p).read_bytes()),'core_sha256':core_sha,'histories':histories,
      'producer':e['evidence'].get('leg_source_digest'),'validator':core['identity']['validator_source_digest'],
      'validation_status':e['validation_status'],'ledger_out_present':'out' in e['evidence'],
      'bundle':{'members':len(members),'bytes':sum(x['bytes'] for x in members.values()),'exact_set_SHA':True}}
for key in ledger:
    if key!='legs': assert ledger[key]==prior_ledger[key],key
assert [x for x in ledger['legs'] if x['leg_id'] not in receipts]==[x for x in prior_ledger['legs'] if x['leg_id'] not in receipts]
zp=D/'docs/22p_gap/gate75_review/GATE75_REVIEW_20260927.zip'
assert zp.read_bytes()==(O.parent/'gate75_review_20260927'/zp.name).read_bytes()
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
    m=json.loads(z.read('MANIFEST.json'));files=m['files']
    assert set(names)==set(files)|{'MANIFEST.json'}
    for n,v in files.items():
        q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16) and ident(z.read(n))==v
        assert z.read(n)==(zp.parent/'codex'/n).read_bytes()
    prior_package={'zip':ident(zp.read_bytes()),'payload':len(files),'manifest':ident(z.read('MANIFEST.json')),
                   'CRC_exact_set_SHA':True,'unpacked_members_byte_identical':True}
prefix='degradation-degeneracy/docs/22p_gap/'
gate_paths=[p for p in tracked if p.startswith(prefix+'gate') and p.endswith('.md')]
nonpackage=[p for p in gate_paths if not re.match(r'gate\d+_review/',p[len(prefix):])]
registry=[p for p in tracked if p.startswith(prefix+'_exec_class/')]
disk_registry=[x.relative_to(W).as_posix() for x in (D/'docs/22p_gap/_exec_class').rglob('*') if x.is_file()]
assert set(registry)==set(disk_registry)
refs=['docs/22p_gap/GATE76_REQUEST.md','docs/22p_gap/GATE75_REQUEST.md','docs/22p_gap/LEG_PRESERVATION.yaml',
      'docs/22p_gap/STAGE3_CONTRACT.md','docs/GATE70_WORKING_STATE.md','tools/preserve.py','tools/index_yaml.py',
      'scripts/archive_results.sh','tests/test_gate75_defensive.py','tests/test_gate74_defensive.py','tests/test_docs_lint.py',
      'artifacts/artifact_index.yaml']
refs += [p.relative_to(D).as_posix() for p in (D/'docs/22p_gap/receipts').rglob('*.yaml') if p.name.startswith(('grid_fit_v5.','paired_fixed5_v4.'))]
for n in refs:
    target=O/'reference'/n;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((D/n).read_bytes())
response=(D/'docs/08_REVIEW_RESPONSE.md').read_text(encoding='utf-8')
(O/'reference/RESPONSE_SECTIONS104_105.txt').write_text(response[response.index('## §104 '):],encoding='utf-8')
report={'head':H,'code':C,'previous_head':OLD,'source_digest':hd.hexdigest()[:16],'RUN_SCOPE_files':len(sp),
 'tracked_files':len(tracked),'diffs':diffs,'unchanged':unchanged,'receipts':receipts,'ledger_changes':legchanges,
 'prior_review_package':prior_package,'registry_count':len(registry),'registry_disk_matches':True,
 'claim_scope_new_prefix':{'excluded_markdown_paths':len(gate_paths),'non_gateNN_review_paths':nonpackage},
 'limits':{'subject_imports':0,'full_suite_reruns':0,'scientific_runs_archive_restore_class_changes':0}}
write('DATA_AUDIT.json',report)
print(json.dumps({'status':'DATA_AUDIT_PASS','head':H,'digest':report['source_digest'],'tracked':len(tracked),
 'scope_files':len(sp),'registry_count':len(registry),'nonpackage_excluded':nonpackage,'prior_package':prior_package},ensure_ascii=False))
