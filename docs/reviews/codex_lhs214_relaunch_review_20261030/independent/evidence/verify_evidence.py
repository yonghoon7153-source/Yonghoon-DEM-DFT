"""Portable, read-only source/evidence checks; writes only under --out.

No simulator, runner command, WSL, scheduler, or selftest is launched.
The only executed project functions are read-only registration/receipt validators.
The verification tree is a byte copy of supplied source plus Git-verified cached inputs.
"""
from pathlib import Path, PurePosixPath
import argparse, ast, copy, hashlib, json, platform, re, shutil, sys, tarfile

def sha(b): return hashlib.sha256(b).hexdigest()
def gitblob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def readj(p): return json.loads(Path(p).read_bytes())
def dump(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--s1',type=Path,required=True)
ap.add_argument('--identity-metadata',type=Path,required=True)
ap.add_argument('--tgz',type=Path,required=True)
ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
a=ap.parse_args()
repo,s1,meta,out=(x.resolve() for x in (a.repo,a.s1,a.identity_metadata,a.out))
out.mkdir(parents=True,exist_ok=True)
PIN='35f0327377a4213774010a090df4d224e50d29e1'
bundle=repo/'docs/reviews/lhs214_wsl_preflight_35f032737_1028/bundle'
evidence=bundle.parent
result={'scope':'Archived WSL bytes and CPU-only read-only validation; no new WSL execution or launch',
        'python':platform.python_version(),'executable':sys.executable,'launch_pin':PIN}

# Check original archive directly, without extraction.
tar_rows=[]
with tarfile.open(a.tgz,'r:gz') as tf:
    members=tf.getmembers(); names=[m.name for m in members]
    assert len(names)==len(set(names))
    assert len({n.casefold() for n in names})==len(names)
    for m in members:
        p=PurePosixPath(m.name)
        assert not p.is_absolute() and '..' not in p.parts and not m.issym() and not m.islnk()
        assert m.isdir() or m.isfile()
        if m.isfile():
            b=tf.extractfile(m).read(); local=bundle/p.name
            assert local.read_bytes()==b
            tar_rows.append({'member':m.name,'file':p.name,'bytes':len(b),'sha256':sha(b),'same_as_bundle':True})
assert len(tar_rows)==18
manifest={ln.split(None,1)[1].strip():ln.split(None,1)[0] for ln in (evidence/'MANIFEST.sha256').read_text().splitlines()}
assert set(manifest)=={p.name for p in bundle.iterdir() if p.is_file()}
assert set(manifest)=={r['file'] for r in tar_rows}
assert all(manifest[r['file']]==r['sha256'] for r in tar_rows)
result['archive']={'bytes':a.tgz.stat().st_size,'sha256':sha(a.tgz.read_bytes()),'files':tar_rows,
                   'manifest_all_18_match':True,'ordinary_files':len(tar_rows),'directories':sum(m.isdir() for m in members)}
assert result['archive']['sha256']=='9c05aef7591ad10af70af52c01508b494ddc71855322b0ce367f42f67a5be0b8'

# Complete a separate verification copy; never add data to the supplied repository.
vr=out/'verification_tree'; vr.mkdir(exist_ok=True)
copied=[]
for part in ('scripts','webapp'):
    for p in (repo/part).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            rel=p.relative_to(repo); dst=vr/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
            copied.append({'path':rel.as_posix(),'sha256':sha(p.read_bytes()),'source':'review ZIP'})
for name in ('lhs_network_batch_registration_20261007_g2.md','lhs_network_batch_registration_20261012_supp20.md'):
    rel=Path('docs/reviews')/name; dst=vr/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(repo/rel,dst)
    copied.append({'path':rel.as_posix(),'sha256':sha((repo/rel).read_bytes()),'source':'review ZIP'})
b7=readj(meta/'B7_docs_data.json');rev=readj(meta/'review_docs_data.json')
assert b7.get('truncated') is False and rev.get('truncated') is False
bm={x['path']:x for x in b7['tree']};rm={x['path']:x for x in rev['tree']}
cached_trees={}
inputs=[]
for p in (s1/'repo/docs/data').rglob('*'):
    if not p.is_file():continue
    local=p.relative_to(s1/'repo/docs/data');top=local.parts[0]
    assert bm[top]['sha']==rm[top]['sha'],top
    if len(local.parts)==1:
        expected=bm[top]['sha'];tree_sha=None
    else:
        if top not in cached_trees:
            t=readj(s1/'trees'/('data_'+top+'.json'))
            assert t['sha']==bm[top]['sha'] and t.get('truncated') is False,top
            cached_trees[top]=t
        t=cached_trees[top];inner=PurePosixPath(*local.parts[1:]).as_posix()
        entry=next(x for x in t['tree'] if x['path']==inner)
        assert entry['type']=='blob';expected=entry['sha'];tree_sha=t['sha']
    b=p.read_bytes();assert gitblob(b)==expected,str(local)
    rel=Path('docs/data')/local;dst=vr/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    inputs.append({'path':rel.as_posix(),'bytes':len(b),'sha256':sha(b),'git_blob':expected,'top_tree':tree_sha,'B7_and_review_blob_verified':True})
result['verification_tree']={'source_files':copied,'cached_inputs':inputs,'cached_input_count':len(inputs),
    'note':'Cache blobs checked against current B7/review docs/data entries and linked nontruncated S1 subtree responses; no product-code or expected-value changes.'}
dump(out/'verified_input_inventory.json',inputs)

sys.path.insert(0,str(vr/'scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S
# Fingerprint independently from file bytes and documented sorted JSON format.
hashes={rel:sha((vr/rel).read_bytes()) for rel in N.CODE_FILES}
fp=sha(json.dumps(sorted(hashes.items()),separators=(',',':')).encode())
assert len(hashes)==32 and hashes==N.code_hashes() and fp==N.code_fp(hashes)
regs={}
for name in ('lhs_network_batch_registration_20261007_g2.md','lhs_network_batch_registration_20261012_supp20.md'):
    text=(vr/'docs/reviews'/name).read_text(encoding='utf-8')
    section=text.split('\n## 3.',1)[1].split('\n## ',1)[0]
    tokens=set(re.findall(r'\bcode_fp ([0-9a-f]{64})\b',section))
    assert tokens=={fp};assert not re.findall(r'\bcode_fp_pending [0-9a-f]{64}\b',text)
    regs[name]={'active_code_fp':list(tokens),'active_pending_tokens':0}
result['code']={'code_fp':fp,'code_files':hashes,'registrations':regs,
  'tool_sha256':{rel:sha((vr/rel).read_bytes()) for rel in S.TOOL_PINS}}

# Input fingerprints calculated independently by enumerating raw descriptor files.
def independent_digest(cohorts):
    ids=[];rows=[];missing=[];tsvs={};count=0
    for cohort in sorted(cohorts):
        spec=N.COHORT_SPECS[cohort];hdir=vr/spec['harvest']
        tsvs[cohort]=sha((vr/spec['cohort']).read_bytes())
        for p in sorted(hdir.glob('*.json')):
            if p.name.startswith('_'):continue
            raw=readj(p).get('raw') or {};vals=[str((raw.get(k) or {}).get('sha256') or '') for k in ('atom','contact','mesh','deck')]
            ids.append(p.stem+'\t'+cohort);rows.append('\t'.join([p.stem,cohort,*vals]));count+=1
            if '' in vals:missing.append(p.stem)
    return dict(n=count,ids_sha256=sha(('\n'.join(ids)+'\n').encode()),raw_sha256_table_sha256=sha(('\n'.join(rows)+'\n').encode()),
                missing_raw_sha=missing,cohort_tsv_sha256=tsvs)

result['receipts']={}
for prefix,kind,cohorts in [('net194','production194',['lhs','lhsx']),('netsupp20','supp20',['lhss'])]:
    p=next(p for p in bundle.glob(prefix+'*.json') if not p.stem.endswith(('_receipt','_verify')))
    rec=readj(p);log=bundle/PurePosixPath(rec['log']['path']).name;lb=log.read_bytes()
    assert rec['git']['sha']==PIN and len(rec['git']['sha'])==40 and rec['git']['dirty'] is False
    assert len(lb)==rec['log']['bytes'] and sha(lb)==rec['log']['sha256']
    v=N.preflight_receipt_checks(p,expect_set=kind,approved_sha=PIN)
    assert len(v['checks'])==11 and all(c['ok'] for c in v['checks']),[(c['id'],c['detail']) for c in v['checks'] if not c['ok']]
    independent=independent_digest(cohorts)
    assert independent==rec['input_digest']==v['recomputed']['input_digest']
    reg=(vr/'docs/reviews'/('lhs_network_batch_registration_20261007_g2.md' if prefix=='net194' else 'lhs_network_batch_registration_20261012_supp20.md')).read_text(encoding='utf-8')
    for value in [independent['ids_sha256'],independent['raw_sha256_table_sha256'],*independent['cohort_tsv_sha256'].values()]:assert value in reg
    dump(out/(kind+'_reverified.json'),v)
    result['receipts'][kind]={'file':p.name,'sha256':sha(p.read_bytes()),'log_sha256':sha(lb),'log_bytes':len(lb),
       'direct_unmodified_receipt':True,'passed':[c['id'] for c in v['checks']],'input_digest':independent,
       'raw_dump_files_reopened':False,'generation':rec['generation'],'root':rec['args']['root'],
       'runner_sha256':rec['runner']['sha256'],'exit_code':rec['exit_code'],'completed':rec['completed']}
    assert rec['runner']['sha256']==result['code']['tool_sha256']['scripts/run_network_194_parallel.py']
    if prefix=='netsupp20':
        s=S.receipt(preflight_receipt=str(p),approved_sha=PIN)
        dump(out/'supp20_full_reverified.json',s)
        assert s['rc']==0 and len(s['checks'])==24 and all(c['ok'] for c in s['checks']),[(c['id'],c['detail']) for c in s['checks'] if not c['ok']]
        result['supp20']={'rc':s['rc'],'scope':s['scope'],'passed':[c['id'] for c in s['checks']], 'manual':s['manual'],
                         'manifest':s['inputs']['manifest'],'primary_manifest':s['inputs']['primary_manifest']}

receipt_sha_lines=[]
for ln in (bundle/'receipts_sha256.txt').read_text().splitlines():
    expected,old=ln.split(None,1);p=bundle/PurePosixPath(old.strip()).name
    assert sha(p.read_bytes())==expected;receipt_sha_lines.append(p.name)
result['receipt_sha_lines']=receipt_sha_lines
saved194=readj(next(bundle.glob('net194*_verify.json')))
savedsupp=readj(next(bundle.glob('netsupp20*_receipt.json')))
assert saved194['rc']==0 and len(saved194['checks'])==11 and all(c['ok'] for c in saved194['checks'])
assert savedsupp['rc']==0 and len(savedsupp['checks'])==24 and all(c['ok'] for c in savedsupp['checks'])
assert saved194['approved_sha']==PIN and savedsupp['inputs']['approved_sha']==PIN
assert savedsupp['inputs']['manifest'] is None and savedsupp['inputs']['primary_manifest'] is None
result['saved_verifiers']={'194_rc':saved194['rc'],'194_checks':len(saved194['checks']),'supp20_rc':savedsupp['rc'],'supp20_checks':len(savedsupp['checks']),
                         'supp20_recorded_tools_match':savedsupp['recorded']['tool_sha256']==result['code']['tool_sha256']}
assert result['saved_verifiers']['supp20_recorded_tools_match']

hand=(bundle/'handcheck_194_lines.txt').read_text(encoding='utf-8').splitlines()
full=(bundle/result['receipts']['production194']['file']).with_suffix('.log').read_text(encoding='utf-8')
assert len(hand)==2 and all(line in full.splitlines() for line in hand)
logs={}
for name in ('fast16.log','real4.log','reread_selftest.log','runner_selftest.log','receipt_selftest.log'):
    txt=(bundle/name).read_text(encoding='utf-8')
    logs[name]={'sha256':sha((bundle/name).read_bytes()),'last_nonempty_line':[l for l in txt.splitlines() if l.strip()][-1],
                'tick_count':txt.count('✓'),'cross_count':txt.count('✗'),'PASS_lines':len(re.findall(r'^\s*PASS\s',txt,re.M)),
                'separate_shell_rc_lines':re.findall(r'^(?:fast16|real4|reread|runner|receipt) rc=\d+$',txt,re.M),
                'internal_rc_mention_count':len(re.findall(r'\brc=\d+',txt))}
screen=evidence/'step2_screen_paste_1028_1736.txt';st=screen.read_text(encoding='utf-8')
rcs=dict(re.findall(r'^(fast16|real4|reread|runner|receipt) rc=(\d+)$',st,re.M));assert rcs=={k:'0' for k in ('fast16','real4','reread','runner','receipt')}
env=(bundle/'env.txt').read_text(encoding='utf-8').splitlines();assert env[0].split()[1:]==env[1].split()[1:]
assert (bundle/'head.txt').read_text().strip()==PIN and (bundle/'dirty.txt').stat().st_size==0
result['operator_evidence']={'selftest_logs':logs,'screen':{'sha256':sha(screen.read_bytes()),'in_original_tgz':False,'in_manifest':False,'reported_shell_rcs':rcs,
       'post_selftest_dirty_zero_reported':'dirty 줄 수 (자체 시험 뒤) = 0' in st,'classification':'operator-pasted terminal transcript; no independently authenticated capture timestamp'},
       'env_normal_isolated_equal':True,'reported_env':env,'end_dirty_file_bytes':0,
       'step0_original':(bundle/'step0.txt').read_text(encoding='utf-8'),
       'step0_name_absence_and_initial_dirty_not_in_raw_file':True,'old_root_names_listed_does_not_prove_old_contents_unchanged':True}

# Targeted S0b guard test, extracting original nested helpers without running full selftest.
source=(vr/'scripts/supp20_input_receipt.py').read_text(encoding='utf-8');tree=ast.parse(source)
selftest=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_selftest')
nodes=[next(n for n in selftest.body if isinstance(n,ast.FunctionDef) and n.name==name) for name in ('fp_state','s0b_fp')]
space={'fp_now':fp};exec(compile(ast.Module(body=nodes,type_ignores=[]),'unmodified_S0b_helpers','exec'),space)
different=fp[:-1]+('0' if fp[-1]!='0' else '1');wrong='1'*64;other='2'*64
def r(active,pending=None):return {'code_fp':active,'code_fp_pending':pending}
cases={
 'registered':(r(fp),r(fp),[],True),
 'pending':(r(wrong,fp),r(wrong,fp),[],True),
 'supp_only_ratified':(r(fp),r(wrong,fp),[],False),
 'pending_base_differs':(r(wrong,fp),r(other,fp),[],False),
 'ratified_pending_left':(r(fp,wrong),r(fp,wrong),[],False),
 'base_pending_conflict':(r(fp),r(fp),['등록 문서 code_fp_pending — 값이 둘'],False),
 'undeclared':(r(wrong),r(wrong),[],False),
 'both_same_wrong_last_digit':(r(different),r(different),[],False),
 'pending_same_wrong_last_digit':(r(wrong,different),r(wrong,different),[],False),
 '194_missing_active':(r(fp),r(None),[],False),
 'both_missing_active':(r(None),r(None),[],False),
 'both_registered_missing_checkout':(r(fp),r(fp),[],False),
}
s0=[]
for name,(supp,primary,probs,want) in cases.items():
    space['fp_now']=None if name=='both_registered_missing_checkout' else fp
    got,reason=space['s0b_fp'](supp,primary,probs);assert got is want,(name,got,want)
    s0.append({'name':name,'expected':want,'got':got,'reason':reason})
space['fp_now']=fp
variant_dir=out/'registration_variants';variant_dir.mkdir(exist_ok=True)
sources={k:(vr/'docs/reviews'/n).read_text(encoding='utf-8') for k,n in (
    ('supp','lhs_network_batch_registration_20261012_supp20.md'),('primary','lhs_network_batch_registration_20261007_g2.md'))}
def parsed_variant(tag,kind,active,pending=()):
    text=sources[kind];start=text.index('\n## 3.');end=text.index('\n## ',start+1)
    changed,n=re.subn(r'`code_fp [0-9a-f]{64}`','`code_fp '+active+'`',text[start:end])
    assert n==1
    text=text[:start]+changed+text[end:]+'\n'+''.join('`code_fp_pending '+v+'`\n' for v in pending)
    p=variant_dir/(tag+'_'+kind+'.md');p.write_text(text,encoding='utf-8')
    return S.registration_values(reg_doc=str(p))
seven=[('registered',fp,(),fp,(),True),('pending',wrong,(fp,),wrong,(fp,),True),
       ('supp_only_ratified',fp,(),wrong,(fp,),False),('pending_base_differs',wrong,(fp,),other,(fp,),False),
       ('ratified_pending_left',fp,(wrong,),fp,(wrong,),False),('base_pending_conflict',fp,(),fp,(wrong,other),False),
       ('undeclared',wrong,(),wrong,(),False)]
parsed_seven=[]
for name,sr,sp,pr,pp,want in seven:
    supp,sprobs=parsed_variant(name,'supp',sr,sp);primary,pprobs=parsed_variant(name,'primary',pr,pp)
    got,reason=space['s0b_fp'](supp,primary,pprobs);assert got is want,(name,got,want)
    parsed_seven.append({'name':name,'expected':want,'got':got,'reason':reason,
        'supp_parsed':{k:supp[k] for k in ('code_fp','code_fp_pending')},
        'primary_parsed':{k:primary[k] for k in ('code_fp','code_fp_pending')},
        'primary_fp_problems':[x for x in pprobs if x.startswith('등록 문서 code_fp')]})
mutants=[]
for index,label in enumerate(('undeclared_guard','registered_pending_guard','primary_parse_problem_guard','cross_registration_equality_guard')):
    mutated=copy.deepcopy(nodes);fn=mutated[1];ifs=[n for n in fn.body if isinstance(n,ast.If)]
    assert len(ifs)==4
    fn.body.remove(ifs[index]);ns={'fp_now':fp}
    exec(compile(ast.Module(body=mutated,type_ignores=[]),'S0b_guard_mutant','exec'),ns)
    caught=[]
    for name,(supp,primary,probs,want) in cases.items():
        ns['fp_now']=None if name=='both_registered_missing_checkout' else fp
        if ns['s0b_fp'](supp,primary,probs)[0] is not want:caught.append(name)
    assert caught,label;mutants.append({'removed_guard':label,'caught_by':caught})
result['S0b']={'method':'Unmodified AST-extracted nested helper functions; no full selftest, no launch simulation. In-memory guard removals for sensitivity only.',
               'original_helper_line_ranges':[[n.lineno,n.end_lineno] for n in nodes], 'cases':s0,'mutants':mutants,'original_seven_via_real_parser':parsed_seven,
               'production_receipt_source_matches_S1':sha((repo/'scripts/supp20_input_receipt.py').read_bytes())==sha((s1/'repo/scripts/supp20_input_receipt.py').read_bytes())}
assert result['S0b']['production_receipt_source_matches_S1']
dump(out/'evidence_results.json',result)
print(json.dumps({'archive_files':len(tar_rows),'verified_cache_inputs':len(inputs),'code_fp':fp,'preflight_checks':[len(v['passed']) for v in result['receipts'].values()],
 'supp20_checks':len(result['supp20']['passed']),'S0b_cases':len(s0),'S0b_parser_cases':len(parsed_seven),'S0b_mutants_caught':len(mutants),'saved_results':str(out/'evidence_results.json')},ensure_ascii=False,indent=2))
