"""Reviewer-owned Gate77 data/static audit; never imports or runs subject code."""
from pathlib import Path, PurePosixPath
import ast, hashlib, json, re, stat, subprocess, sys, zipfile

O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g77_20260927')
D = W / 'degradation-degeneracy'
sys.path.insert(0, str(O.parents[1] / 'work/gate26-pydeps'))
import yaml  # reviewer dependency, not from the subject checkout

H = 'ebbcf04ed6cd4f5c2f71b4ebd28031c5fd441002'
C = '23c361edbfc92fefcfbf0639b5ac40f61f7ebec7'
OLD = 'b5e4eadea7794d157d961170247e49d2761bba26'
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl',
        '-c','credential.interactive=never','-C',str(W),*args])
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,ensure_ascii=False,indent=2,default=str); f.write('\n')
def obj(p): return yaml.safe_load((D/p).read_bytes())
assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
tracked=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
write('SOURCE_BEFORE.json',{p:ident((W/p).read_bytes()) for p in tracked})
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
sp=[p for p in git('ls-files','-z','--',*scope).decode().split('\0') if p]
hd=hashlib.sha256()
for p in sorted(sp):
    hd.update(p.removeprefix('degradation-degeneracy/').encode()); hd.update((W/p).read_bytes())
assert hd.hexdigest()[:16]=='1c67a748598baadb' and len(sp)==58
diffs={}
for name,a,b,paths in [
    ('CODE_TO_HEAD_SCOPE',C,H,scope),('G76_TO_G77_SCOPE',OLD,H,scope),
    ('G76_TO_G77_CONTRACT',OLD,H,['degradation-degeneracy/docs/22p_gap/STAGE3_CONTRACT.md']),
    ('G76_TO_G77_NAMES',OLD,H,['degradation-degeneracy'])]:
    args=['diff','--no-ext-diff']+(['--name-status'] if name.endswith('NAMES') else [])
    bts=git(*args,a,b,'--',*paths); (O/(name+'.diff')).write_bytes(bts); diffs[name]=ident(bts)
assert diffs['CODE_TO_HEAD_SCOPE']['bytes']==diffs['G76_TO_G77_SCOPE']['bytes']==0
unchanged={}
for key,paths in {
    'ledger_claims_receipts':['docs/22p_gap/LEG_PRESERVATION.yaml','docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/receipts'],
    'artifacts':['artifacts'],
    'registry_projection_publisher':['docs/22p_gap/_exec_class','docs/22p_gap/proj_g18','docs/22p_gap/row_projection.py'],
    'tests':['tests']}.items():
    got=git('diff','--name-only',OLD,H,'--',*['degradation-degeneracy/'+p for p in paths]).decode().splitlines()
    assert not got,key; unchanged[key]=got

# Data-only reopening of the prior review package; no archived scripts executed.
zp=D/'docs/22p_gap/gate76_review/GATE76_REVIEW_20260927.zip'
prior=O.parent/'gate76_review_20260927'/zp.name
assert zp.read_bytes()==prior.read_bytes()
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    names=z.namelist(); assert len(names)==len(set(n.casefold() for n in names))
    m=json.loads(z.read('MANIFEST.json')); members=m['files']
    assert set(names)==set(members)|{'MANIFEST.json'}
    for n,v in members.items():
        p=PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in n
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
        assert ident(z.read(n))==v
        assert z.read(n)==(zp.parent/'codex'/n).read_bytes()
    prior_package={'zip':ident(zp.read_bytes()),'payload':len(members),
                   'manifest':ident(z.read('MANIFEST.json')),'unpacked_byte_matches':len(members),
                   'exact_set_SHA_CRC_path_case_link':True}

ledger=obj('docs/22p_gap/LEG_PRESERVATION.yaml')
claims=obj('docs/22p_gap/CLAIM_STATUS.yaml')
e=next(x for x in ledger['legs'] if x['leg_id']=='grid_fit_v5')
receipt=obj('docs/22p_gap/receipts/grid_fit_v5.validate.yaml'); core=receipt['core']
core_sha=hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode()).hexdigest()
assert core_sha==receipt['core_sha256']==e['evidence']['verification_receipt_core_sha256']
bundle=D/core['bundle']['uri']; pi=obj(core['bundle']['payload_index'])
actual={p.relative_to(bundle).as_posix():ident(p.read_bytes()) for p in bundle.rglob('*') if p.is_file()}
assert set(actual)==set(pi)|{'payload_sha256.yaml'}
assert all(actual[k]['sha256']==v for k,v in pi.items())
assert len(actual)==core['bundle']['files']==29
assert sum(v['bytes'] for v in actual.values())==core['bundle']['bytes']==27313017
assert actual['payload_sha256.yaml']['sha256']==core['bundle']['payload_index_sha256']
assert actual['fits.parquet']['sha256']==core['bundle']['fits_sha256']
out={x['role']:x for x in core['outputs']}
assert out['rescored_summary']['source_file_sha256']==core['bundle']['fits_sha256']
assert out['sealed_summary']['file_sha256']==actual['degeneracy_summary.yaml']['sha256']
assert out['sealed_summary']['semantic_sha256']==out['rescored_summary']['semantic_sha256']
assert core['restore']['run_dir_relative']==e['evidence']['out']==obj(core['bundle']['uri']+'/restore_map.yaml')['run_dir']
assert e['claim_scope']=='no_active_claim' and e['inference_role']=='diagnostic' and not e.get('claim_roles')

# Static call inventory is lexical/AST only, not a runtime reachability proof.
targets={'run_transaction','CasBackend','ObjectLockBackend','LockedCasBackend'}
callers=[]; definition_files=[]
for rel in sp:
    if not rel.endswith('.py'): continue
    p=W/rel; tree=ast.parse(p.read_text(encoding='utf-8-sig'),filename=rel)
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in targets:
            definition_files.append({'path':rel,'line':node.lineno,'name':node.name})
        if isinstance(node,ast.Call):
            fn=node.func
            name=fn.id if isinstance(fn,ast.Name) else fn.attr if isinstance(fn,ast.Attribute) else None
            if name in targets: callers.append({'path':rel,'line':node.lineno,'name':name})
external_calls=[x for x in callers if x['path']!='degradation-degeneracy/tools/preserve.py']
missing={p:not (D/p).exists() for p in [
    'docs/22p_gap/preserve_backend.yaml','docs/22p_gap/preserve_index',
    'docs/22p_gap/sentinel_panel.yaml']}
primary=next(x for x in claims['active_claims'] if x['id']=='P22_STAGE3_PRIMARY')
assert primary['requires_leg'] is False and primary['protocol_generation']=='v6'

refs=['docs/22p_gap/GATE77_REQUEST.md','docs/22p_gap/STAGE3_CONTRACT.md',
      'docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/LEG_PRESERVATION.yaml',
      'docs/22p_gap/receipts/grid_fit_v5.validate.yaml','docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml',
      'tools/preserve.py','tools/design_wire.py','src/fitting.py','src/io.py',
      'scripts/archive_results.sh','tools/archive_bundle.py','run.sh','tests/test_docs_lint.py',
      'artifacts/artifact_index.yaml','artifacts/grid_fit_v5/restore_map.yaml',
      'artifacts/grid_fit_v5/payload_sha256.yaml']
for n in refs:
    dst=O/'reference'/n; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes((D/n).read_bytes())
for path,start,dst in [('docs/08_REVIEW_RESPONSE.md','## §106 ','RESPONSE_106_107.txt'),
                       ('docs/09_22P_GAP.md','## 10. 다음','NEXT_SCIENTIFIC_STEP.txt')]:
    txt=(D/path).read_text(encoding='utf-8')
    (O/'reference'/dst).write_text(txt[txt.index(start):],encoding='utf-8',newline='\n')
facts={'head':H,'code':C,'prior_review_head':OLD,'source_digest':hd.hexdigest()[:16],
 'scope_files':len(sp),'tracked_files':len(tracked),'diffs':diffs,'unchanged':unchanged,
 'prior_package':prior_package,'grid_fit_v5':{'ledger':e,'receipt_identity':ident((D/'docs/22p_gap/receipts/grid_fit_v5.validate.yaml').read_bytes()),
   'bundle_members':29,'bundle_bytes':27313017,'member_SHA_matches':True,
   'core_SHA_and_out_binding':True,'receipt_reports_validation_checks':core['validation']['n_checks'],
   'receipt_reports_restore_and_rescore':True,'reviewer_restore_or_rescore':False},
 'primary_claim':primary,'not_present':missing,
 'static_backend_inventory':{'definitions':definition_files,'calls':callers,'calls_outside_preserve_in_RUN_SCOPE':external_calls,
   'limit':'AST named-call inventory; not a dynamic call graph or proof about external deployments'},
 'registered_receipt_claims':[x['leg_id'] for x in ledger['legs'] if (x.get('evidence') or {}).get('registered_receipt')],
 'limits':{'subject_imports':0,'subject_tests':0,'scientific_COMSOL_Java_runs':0,'restore_rescore':0,
           'source_edits':0,'external_provider_queries':0}}
write('DATA_AUDIT.json',facts)
print(json.dumps({'status':'DATA_STATIC_AUDIT_COMPLETE','head':H,'source_digest':facts['source_digest'],
 'scope_files':len(sp),'tracked_files':len(tracked),'prior_payload':len(members),
 'missing':missing,'calls_outside_preserve':external_calls,'bundle_bytes':27313017},ensure_ascii=False))
