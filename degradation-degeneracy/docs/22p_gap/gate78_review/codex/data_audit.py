"""Gate78 reviewer-owned data/static audit. No subject modules or tests run."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, subprocess, sys, zipfile
O=Path(__file__).resolve().parent
W=Path('C:/Users/Administrator/Documents/Codex/g78_20260927')
D=W/'degradation-degeneracy'
sys.path.insert(0,str(O.parents[1]/'work/gate26-pydeps'))
import yaml
H='720f0a0e466afb595fbd73a50f89416898cc927c'
OLD='ebbcf04ed6cd4f5c2f71b4ebd28031c5fd441002'
C='23c361edbfc92fefcfbf0639b5ac40f61f7ebec7'
def git(*args):
    return subprocess.check_output(['git','-c','http.sslBackend=openssl','-c','credential.interactive=never','-C',str(W),*args])
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2,default=str);f.write('\n')
def obj(p):return yaml.safe_load((D/p).read_bytes())
assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
tracked=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
write('SOURCE_BEFORE.json',{p:ident((W/p).read_bytes()) for p in tracked})
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
sp=[p for p in git('ls-files','-z','--',*scope).decode().split('\0') if p]
hd=hashlib.sha256()
for p in sorted(sp):
    hd.update(p.removeprefix('degradation-degeneracy/').encode());hd.update((W/p).read_bytes())
assert len(sp)==58 and hd.hexdigest()[:16]=='1c67a748598baadb'
diffs={}
for name,a,b,paths in [
 ('CODE_TO_HEAD_SCOPE',C,H,scope),('G77_TO_G78_SCOPE',OLD,H,scope),
 ('G77_CORRECTIONS',OLD,H,['degradation-degeneracy/docs/22p_gap/GATE77_REQUEST.md']),
 ('G77_TO_G78_RESPONSE',OLD,H,['degradation-degeneracy/docs/08_REVIEW_RESPONSE.md']),
 ('G77_TO_G78_NAMES',OLD,H,['degradation-degeneracy'])]:
    args=['diff','--no-ext-diff']+(['--name-status'] if name.endswith('NAMES') else [])
    bts=git(*args,a,b,'--',*paths);(O/(name+'.diff')).write_bytes(bts);diffs[name]=ident(bts)
assert diffs['CODE_TO_HEAD_SCOPE']['bytes']==diffs['G77_TO_G78_SCOPE']['bytes']==0
unchanged={}
for key,paths in {
 'contract_claims_ledger_receipts':['docs/22p_gap/STAGE3_CONTRACT.md','docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/LEG_PRESERVATION.yaml','docs/22p_gap/receipts'],
 'artifacts':['artifacts'],
 'registry_projection_publisher':['docs/22p_gap/_exec_class','docs/22p_gap/proj_g18','docs/22p_gap/row_projection.py'],
 'tests':['tests']}.items():
    got=git('diff','--name-only',OLD,H,'--',*['degradation-degeneracy/'+p for p in paths]).decode().splitlines()
    assert not got,key;unchanged[key]=got
zp=D/'docs/22p_gap/gate77_review/GATE77_REVIEW_20260927.zip'
assert zp.read_bytes()==(O.parent/'gate77_review_20260927'/zp.name).read_bytes()
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))
    m=json.loads(z.read('MANIFEST.json'));files=m['files']
    assert set(names)==set(files)|{'MANIFEST.json'}
    for n,v in files.items():
        p=PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in n
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
        assert ident(z.read(n))==v and z.read(n)==(zp.parent/'codex'/n).read_bytes()
    prior_package={'zip':ident(zp.read_bytes()),'payload':len(files),'manifest':ident(z.read('MANIFEST.json')),
                   'exact_set_SHA_CRC_path_case_link':True,'unpacked_identical':len(files)}
ledger=obj('docs/22p_gap/LEG_PRESERVATION.yaml')
e=next(x for x in ledger['legs'] if x['leg_id']=='grid_fit_v5')
r=obj('docs/22p_gap/receipts/grid_fit_v5.validate.yaml');core=r['core']
csha=hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode()).hexdigest()
assert csha==r['core_sha256']==e['evidence']['verification_receipt_core_sha256']
bundle=D/core['bundle']['uri'];pi=obj(core['bundle']['payload_index'])
members={p.relative_to(bundle).as_posix():ident(p.read_bytes()) for p in bundle.rglob('*') if p.is_file()}
assert set(members)==set(pi)|{'payload_sha256.yaml'}
assert all(members[k]['sha256']==v for k,v in pi.items())
assert len(members)==29 and sum(v['bytes'] for v in members.values())==27313017
assert core['bundle']['payload_index_sha256']==members['payload_sha256.yaml']['sha256']
assert e['inference_role']=='diagnostic' and e['claim_scope']=='no_active_claim'
assert e['evidence']['out']==core['restore']['run_dir_relative']=='results/grid_fit_v5'
primary=next(x for x in obj('docs/22p_gap/CLAIM_STATUS.yaml')['active_claims'] if x['id']=='P22_STAGE3_PRIMARY')
assert primary['requires_leg'] is False
refs=['docs/22p_gap/GATE78_REQUEST.md','docs/22p_gap/GATE77_REQUEST.md','docs/22p_gap/STAGE3_CONTRACT.md',
 'docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/LEG_PRESERVATION.yaml','docs/GATE70_WORKING_STATE.md',
 'docs/22p_gap/receipts/grid_fit_v5.validate.yaml','docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml',
 'src/fitting.py','src/io.py','src/scoring.py','src/grid.py','tools/design_wire.py',
 'docs/22p_gap/make_receipt.py','configs/grid_fine.yaml','scripts/smoke_e2e.sh']
for n in refs:
    dst=O/'reference'/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((D/n).read_bytes())
for n in ['CLAUDE_REPLY.md','DECISION.json','REVIEW_KO.md']:
    dst=O/'prior_gate77'/n;dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes((zp.parent/'codex'/n).read_bytes())
response=(D/'docs/08_REVIEW_RESPONSE.md').read_text(encoding='utf-8')
(O/'reference/RESPONSE_108.txt').write_text(response[response.index('## §108 '):],encoding='utf-8',newline='\n')
out={'head':H,'code':C,'prior_head':OLD,'source_digest':hd.hexdigest()[:16],
 'scope_files':len(sp),'tracked_files':len(tracked),'diffs':diffs,'unchanged':unchanged,
 'prior_review_package':prior_package,'grid_fit_v5':{'members':29,'bytes':27313017,
 'exact_set_SHA':True,'core_sha256':csha,'claim_scope':e['claim_scope'],'inference_role':e['inference_role'],
 'producer_digest':e['evidence']['leg_source_digest'],'validator_digest':core['identity']['validator_source_digest'],
 'restoration_and_validation':'existing records; not rerun by reviewer'},
 'primary_claim':primary,
 'not_present':{p:not (D/p).exists() for p in ['docs/22p_gap/preserve_backend.yaml','docs/22p_gap/preserve_index','docs/22p_gap/sentinel_panel.yaml']},
 'authorization_scope':'User reports/section108 authorize future local stage1+2 after this review; not execution authority for reviewer',
 'limits':{'subject_imports':0,'subject_test_runs':0,'scientific_COMSOL_Java_runs':0,'restore_rescore':0,
           'source_edits':0,'class_or_projection_changes':0,'external_provider_queries':0}}
write('DATA_AUDIT.json',out)
print(json.dumps({'status':'DATA_STATIC_AUDIT_COMPLETE','head':H,'source_digest':out['source_digest'],
 'tracked_files':len(tracked),'scope_files':len(sp),'prior_package_payload':len(files),'source_unchanged':True},ensure_ascii=False))
