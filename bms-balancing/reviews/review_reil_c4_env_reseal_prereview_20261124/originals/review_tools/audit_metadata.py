import pathlib,json,hashlib,csv,io,re,ast,shutil,difflib
R=pathlib.Path(__file__).parent
S=R/'source'/'bms-balancing'
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
out={}
old=S/'evidence/reil_c4_env_20261013'
seal=S/'reil_c6_rebuild_20261013'
man=json.loads((seal/'MANIFEST.json').read_text())
assert sha((seal/'MANIFEST.json').read_bytes())=='4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc'
assert set(p.name for p in seal.iterdir())==set(man)|{'MANIFEST.json'}
assert all(sha((seal/n).read_bytes())==h for n,h in man.items())
out['old_seal']={'manifest_sha256':sha((seal/'MANIFEST.json').read_bytes()),'exact_files':11,'all_payload_hashes_match':True}
recs={}
wraps=[]
for dirname in ['09_records','10_test_tool_records']:
    rr=list((old/dirname).glob('*.RECORD'))
    rows=hashed=unhashed=0
    for p in rr:
        b=p.read_bytes()
        assert b.endswith(b'\r\n') and b.count(b'\n')==b.count(b'\r\n')
        vals=list(csv.reader(io.StringIO(b.decode(),newline='')))
        assert len({v[0] for v in vals})==len(vals)
        rows+=len(vals);hashed+=sum(bool(v[1]) for v in vals);unhashed+=sum(not v[1] for v in vals)
        wraps += [{'record':p.name,'path':v[0],'hash':v[1],'size':v[2]} for v in vals if v[0].startswith(('../../../bin/','../../bin/'))]
    recs[dirname]={'count':len(rr),'rows':rows,'hashed':hashed,'unhashed':unhashed,'all_crlf_final_crlf':True,'duplicate_rows':0}
out['old_records']=recs;out['wrappers']=wraps
lock=(seal/'REIL_C6.lock.txt').read_text()
pairs=re.findall(r'^([^=\s#]+)==([^\s#]+)  # record-sha256 ([0-9a-f]{64})$',lock,re.M)
assert len(pairs)==30
for name,version,h in pairs:
    assert sha((old/'09_records'/f'{name}-{version}.RECORD').read_text(encoding='utf-8').encode())==h
out['old_lock_record_links']=30
for base in ['reil_c4_env_reseal_pre_20261124','reil_c4_env_reseal_selftest_20261124']:
    dd=S/'evidence'/base
    body=b''.join(b'100644 '+p.name.encode()+b'\0'+hashlib.sha1(b'blob '+str(p.stat().st_size).encode()+b'\0'+p.read_bytes()).digest() for p in sorted(dd.iterdir(),key=lambda p:p.name.encode()))
    g=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()
    expected={'reil_c4_env_reseal_pre_20261124':'1e759c6a5d0e38fb7c84f20fe7233f8b15276cc7','reil_c4_env_reseal_selftest_20261124':'6cedd7828d7a0949e70836efacb4b60f1aca3998'}[base]
    assert g==expected,(base,g)
    out[base]={'git_tree_recomputed':g,'files':len(list(dd.iterdir()))}
tests=S/'evidence/reil_c4_env_reseal_selftest_20261124'
for metaname,testname,mutname in [('selftest.meta.txt','selftest.py','mutation_proof.py'),('mutation_proof.meta.txt','selftest.py','mutation_proof.py'),('run1_mutation_proof.meta.txt','run1_selftest.py','run1_mutation_proof.py')]:
    meta=(tests/metaname).read_text()
    for key,p in [('tool_sha256',S/'scripts/reil_c4_env_reseal_check.py'),('selftest_sha256',tests/testname),('mutation_proof_sha256',tests/mutname)]:
        assert re.search(r'^'+key+r': (\w+)$',meta,re.M)[1]==sha(p.read_bytes()),(metaname,key)
out['metadata_source_hash_links']='ALL_MATCHED'
for n in ['selftest','mutation_proof','run1_mutation_proof']:
    lines=(tests/(n+'.stdout.log')).read_text().splitlines()
    out[n+'_submitted_results']={'pass_lines':sum(x.startswith('PASS ') for x in lines),'fail_lines':[x for x in lines if x.startswith('FAIL ')],'last':lines[-1],'stderr_bytes':(tests/(n+'.stderr.log')).stat().st_size}
delta=''.join(difflib.unified_diff((tests/'run1_selftest.py').read_text().splitlines(True),(tests/'selftest.py').read_text().splitlines(True),fromfile='run1_selftest.py',tofile='selftest.py'))
(R/'SELFTEST_STATIC_DIFF.txt').write_text(delta,encoding='utf-8')
tooltext=(S/'scripts/reil_c4_env_reseal_check.py').read_text()
ast.parse(tooltext)
mutast=ast.parse((tests/'mutation_proof.py').read_text())
mut=next(ast.literal_eval(n.value) for n in mutast.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets))
assert len(mut)==12 and all(tooltext.count(m[1])==1 for m in mut)
out['mutation_source_static']={'mutants':12,'control_runs':1,'replacement_targets_each_once':True,'execution_by_reviewer':0}
for f in (R/'official').glob('*.capture.json'):
    x=json.loads(f.read_text());(R/'official'/(f.stem+'.txt')).write_text(x['content'],encoding='utf-8')
prior=R.parents[1]/'reil_c4_env_review_20261013'
# sibling review folders are under outputs
prior=R.parent/'reil_c4_env_review_20261013'
v4=R.parent/'reil_c4a_v4_review_20261124'
basis=R/'basis';basis.mkdir(exist_ok=True)
selected=[]
for src,name in [(prior/'REVIEW_KO.md','OCTOBER_REVIEW_KO.md'),(prior/'DECISION.json','OCTOBER_DECISION.json'),(v4/'REVIEW_DECISION.json','C4A_V4_REVIEW_DECISION.json'),(v4/'input/REIL_C4A_IMPL_REQUEST_v4_20261124.md','C4A_V4_REQUEST.md')]:
    selected.append(ident(src));shutil.copyfile(src,basis/name)
(R/'SELECTED_LOCAL_SOURCES_BEFORE_PACKAGE.json').write_text(json.dumps({'boundary':'After review reads, before review packaging; not start-of-turn or remote audit','files':selected},indent=2)+'\n',encoding='utf-8')
out['scope']={'supplied_program_imports':0,'supplied_program_executions':0,'tests':0,'installs':0,'venv_creation':0,'pip':0,'emit_check':0,'COMSOL':0,'review_only':'Own metadata/hash/CSV/JSON/AST processing. Submitted result logs are historical evidence, not independently observed executions.'}
(R/'STATIC_EVIDENCE_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))

