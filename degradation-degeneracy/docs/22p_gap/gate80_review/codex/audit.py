"""Reviewer-owned static/data audit. No subject module imports or execution."""
from pathlib import Path, PurePosixPath
import ast, copy, hashlib, json, stat, subprocess, sys, zipfile
O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g80_20260928')
D = W / 'degradation-degeneracy'
sys.path.insert(0, str(O.parents[1] / 'work/gate26-pydeps'))
import yaml
H = '9a26dd5f31ca6fae45d5a55f5c59e33408371984'
C = '6ffa98d4df542aa42abde2f94685beffec33312c'
P = 'b0203d1090b2659c31f8eb6f55e5a144657e9052'
PC = '3dc269d80a7441b294d475b625b096baf3d1a459'
def git(*args):
    return subprocess.check_output(['git', '-c', 'http.sslBackend=openssl', '-c', 'credential.interactive=never', '-C', str(W), *args])
def ident(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def save(name, obj):
    p = O/name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def original(ref, p): return git('show', ref+':degradation-degeneracy/'+p)
def y(p): return yaml.safe_load((D/p).read_bytes())
def diffs(a,b,p=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [r for k in sorted(a.keys()|b.keys()) for r in diffs(a.get(k),b.get(k),p+'/'+str(k))]
    return [] if a==b else [{'path':p,'before':a,'after':b}]
assert git('rev-parse','HEAD').decode().strip()==H
assert not git('status','--porcelain=v1','-uall').strip()
scope=['degradation-degeneracy/'+x for x in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
sp=[p for p in git('ls-files','-z','--',*scope).decode().split('\0') if p]
refs=['src/fitting.py','tests/test_gate79_stage3_logging.py','tests/test_fitting.py',
      'docs/22p_gap/GATE80_REQUEST.md','docs/22p_gap/GATE79_REQUEST.md',
      'docs/22p_gap/STAGE3_CONTRACT.md','docs/22p_gap/LEG_PRESERVATION.yaml',
      'docs/22p_gap/CLAIM_STATUS.yaml','docs/22p_gap/mutation_replay.py']
selected=sorted(set(sp)|{'degradation-degeneracy/'+p for p in refs})
before={p:ident((W/p).read_bytes()) for p in selected}
save('SOURCE_BEFORE.json',before)
hd=hashlib.sha256()
for p in sorted(sp): hd.update(p.removeprefix('degradation-degeneracy/').encode()); hd.update((W/p).read_bytes())
assert hd.hexdigest()[:16]=='eda3feb8f4536511'
assert not git('diff','--no-ext-diff',C,H,'--',*scope)
changed=git('diff','--name-only',PC,H,'--',*scope).decode().splitlines()
assert changed==['degradation-degeneracy/src/fitting.py']
for name,a,b,paths in [('SCOPE_CHANGE',PC,H,scope),('CODE_TO_HEAD',C,H,scope),
 ('TEST_DOC_RECEIPT_CHANGE',P,H,['degradation-degeneracy/tests','degradation-degeneracy/docs/22p_gap/GATE79_REQUEST.md',
 'degradation-degeneracy/docs/22p_gap/STAGE3_CONTRACT.md','degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml',
 'degradation-degeneracy/docs/22p_gap/mutation_replay.py'])]:
    (O/(name+'.diff')).write_bytes(git('diff','--no-ext-diff',a,b,'--',*paths))

class StripDocs(ast.NodeTransformer):
    def generic_visit(self,node):
        node=super().generic_visit(node)
        if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
                node.body=node.body[1:]
        return node
old=ast.parse(original(PC,'src/fitting.py')); new=ast.parse((D/'src/fitting.py').read_bytes())
assert ast.dump(StripDocs().visit(copy.deepcopy(old)))==ast.dump(StripDocs().visit(copy.deepcopy(new)))
fn=next(n for n in new.body if isinstance(n,ast.FunctionDef) and n.name=='_minimize_until_stable')
loop=next(n for n in fn.body if isinstance(n,ast.For))
nf=next(n for n in loop.body if isinstance(n,ast.If) and ast.unparse(n.test)=='not np.isfinite(res.fun)')
oa=next(n for n in loop.body if isinstance(n,ast.Assign) and any(isinstance(q,ast.Name) and q.id=='ok' for t in n.targets for q in ast.walk(t)))
assert loop.body.index(nf)<loop.body.index(oa) and any(isinstance(q,ast.Break) for q in nf.body)
test=ast.parse((D/'tests/test_gate79_stage3_logging.py').read_bytes())
newtests={n.name: {'line': n.lineno, 'assertions':[ast.unparse(q.test) for q in ast.walk(n) if isinstance(q,ast.Assert)]}
          for n in test.body if isinstance(n,ast.FunctionDef) and ('g79_03c_' in n.name or 'g79_03d_' in n.name)}
assert len(newtests)==2
mt=ast.parse((D/'docs/22p_gap/mutation_replay.py').read_bytes())
mutants=next(n.value for n in mt.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets))
m=next(n for n in mutants.elts if isinstance(n,ast.Tuple) and isinstance(n.elts[0],ast.Constant) and n.elts[0].value=='legacy-ok-is-the-last-finite-round-g79')
pre,post,selector=[ast.literal_eval(m.elts[i]) for i in (2,3,4)]
assert (D/'src/fitting.py').read_text(encoding='utf-8').count(pre)==1 and selector=='g79_03c'
save('STATIC_CHECKS.json',{'executable_AST_identical_excluding_docstrings':True,
  'nonfinite_break_line':nf.lineno,'ok_assignment_line':oa.lineno,'nonfinite_break_before_ok':True,
  'tests_read_not_run':newtests,'mutation':{'preimage_count':1,'before':pre,'after':post,'selector':selector},
  'subject_imports':0,'subject_calls':0,'docstrings_are_intentionally_changed':True})

zp=D/'docs/22p_gap/gate79_review/GATE79_REVIEW_20260928.zip'
assert zp.read_bytes()==(O.parent/'gate79_review_20260928'/zp.name).read_bytes()
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    names=z.namelist(); assert len(names)==len(set(n.casefold() for n in names))
    raw=z.read('MANIFEST.json'); files=json.loads(raw)['files']
    assert set(names)==set(files)|{'MANIFEST.json'}
    for n,v in files.items():
        pp=PurePosixPath(n)
        assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in n and ':' not in n
        assert not stat.S_ISLNK(z.getinfo(n).external_attr>>16)
        assert ident(z.read(n))==v and z.read(n)==(zp.parent/'codex'/n).read_bytes()
    package={'zip':ident(zp.read_bytes()),'manifest':ident(raw),'payload':len(files),'checks':'exact set/size/SHA/CRC/path/case/link; prior and unpacked byte identity'}
ledger=y('docs/22p_gap/LEG_PRESERVATION.yaml')
oldledger=yaml.safe_load(original(P,'docs/22p_gap/LEG_PRESERVATION.yaml'))
assert len(diffs(oldledger,ledger))==1 and diffs(oldledger,ledger)[0]['path']=='/legs'
legdiff={n['leg_id']:diffs(o,n) for o,n in zip(oldledger['legs'],ledger['legs']) if o!=n}
assert set(legdiff)=={'paired_fixed5_v4','grid_fit_v5'}
assert all({d['path'] for d in ds}=={'/evidence/verification_receipt_core_sha256','/evidence/validator_identity/source_digest'} for ds in legdiff.values())
receipts={}
for leg in ['paired_fixed5_v4','grid_fit_v5']:
    p='docs/22p_gap/receipts/'+leg+'.validate.yaml'
    oldraw=original(P,p); hist='docs/22p_gap/receipts/history/'+leg+'.validate.c78d7969ef49fd07.yaml'
    assert oldraw==(D/hist).read_bytes()
    r=y(p); oldr=yaml.safe_load(oldraw); core=r['core']; e=next(x for x in ledger['legs'] if x['leg_id']==leg)
    ch=hashlib.sha256(yaml.safe_dump(core,allow_unicode=True,sort_keys=False,width=100).encode()).hexdigest()
    assert ch==r['core_sha256']==e['evidence']['verification_receipt_core_sha256']
    assert core['identity']['validator_source_digest']=='eda3feb8f4536511'
    assert core['identity']['src_io_sha256']==oldr['core']['identity']['src_io_sha256']==ident((D/'src/io.py').read_bytes())['sha256'][:16]
    ds=diffs(oldr,r)
    assert all(x['path'] in ['/core/identity/validator_source_digest','/core_sha256','/stamp/generated_at_utc','/stamp/validator_commit'] for x in ds)
    assert core['validation']==oldr['core']['validation'] and core['outputs']==oldr['core']['outputs']
    pi=y(core['bundle']['payload_index']); bundle=D/core['bundle']['uri']
    members={p.relative_to(bundle).as_posix():ident(p.read_bytes()) for p in bundle.rglob('*') if p.is_file()}
    assert set(members)==set(pi)|{'payload_sha256.yaml'}
    assert all(members[k]['sha256']==v for k,v in pi.items())
    assert members['payload_sha256.yaml']['sha256']==core['bundle']['payload_index_sha256']
    assert len(members)==core['bundle']['files'] and sum(x['bytes'] for x in members.values())==core['bundle']['bytes']
    if leg=='grid_fit_v5': assert e['evidence']['out']==core['restore']['run_dir_relative']
    else: assert 'out' not in e['evidence']
    receipts[leg]={'history_equals_prior':True,'history':ident(oldraw),'current':ident((D/p).read_bytes()),
        'diff':ds,'core_sha256':ch,'bundle_members':len(members),'bundle_bytes':sum(x['bytes'] for x in members.values()),
        'stamp':r['stamp'],'validation_and_outputs_unchanged':True,'validation_checks':core['validation']['n_checks'],
        'producer_digest':e['evidence']['leg_source_digest']}
    for name, b in [('prior/'+leg+'.validate.yaml',oldraw),('reference/'+p,(D/p).read_bytes())]:
        dst=O/name; dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
unchanged={}
for key,paths in {'artifacts':['artifacts'],'claims':['docs/22p_gap/CLAIM_STATUS.yaml'],
 'class_projection':['docs/22p_gap/_exec_class','docs/22p_gap/proj_g18','docs/22p_gap/row_projection.py']}.items():
    assert not git('diff','--name-only',P,H,'--',*['degradation-degeneracy/'+x for x in paths]);unchanged[key]=True
g=next(x for x in ledger['legs'] if x['leg_id']=='grid_fit_v5')
assert g['inference_role']=='diagnostic' and g['claim_scope']=='no_active_claim'
for p in refs:
    dest=O/'reference'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((D/p).read_bytes())
for n in ['REVIEW_KO.md','DECISION.json']:
    dest=O/'prior_gate79'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((zp.parent/'codex'/n).read_bytes())
response=(D/'docs/08_REVIEW_RESPONSE.md').read_text(encoding='utf-8')
(O/'reference/RESPONSE_111.txt').write_text(response[response.index('## §111 '):],encoding='utf-8')
after={p:ident((W/p).read_bytes()) for p in selected}
assert before==after and not git('status','--porcelain=v1','-uall').strip()
save('SOURCE_AFTER_CHECK.json',{'selected_files':len(selected),'all_unchanged':True,'head':H,'clean':True})
save('DATA_AUDIT.json',{'head':H,'code':C,'prior_head':P,'source_digest':hd.hexdigest()[:16],
 'scope_files':len(sp),'scope_changed':changed,'code_to_head_scope_diff_bytes':0,'selected_files':len(selected),
 'prior_review':package,'receipts':receipts,'ledger_diff':legdiff,'unchanged':unchanged,
 'subject_execution':0,'full_tests_rerun':False,'review_scope':'static source/AST and data identity, not replay/restore/COMSOL'})
print(json.dumps({'status':'PASS','scope_files':len(sp),'selected_files':len(selected),'prior_payload':len(files),
 'source_digest':hd.hexdigest()[:16],'executable_AST_unchanged':True,'receipts_checked':2,'bundle_members':sum(r['bundle_members'] for r in receipts.values())}))
