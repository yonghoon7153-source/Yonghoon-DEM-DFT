"""Reviewer-owned text/hash/AST inspection only. Never imports or executes submitted modules."""
import ast, difflib, fnmatch, hashlib, json, re
from pathlib import Path

HERE=Path(__file__).resolve().parent
P='degradation-degeneracy/'
HEAD='43056f78d845741b43357181fcfd64fc78a8ef0c'
records=json.loads((HERE/'REFERENCE_TEXT.json').read_text(encoding='utf-8'))['records']
prior=json.loads((HERE/'prior_review_data/GATE90_REFERENCE_TEXT.json').read_text(encoding='utf-8'))['records']
prior += json.loads((HERE/'prior_review_data/GATE90_MUTATION_REFERENCE.json').read_text(encoding='utf-8'))['records']
oldhead='24f499ba6a5e45a75613e9842ce99a679b5ce863'
by={r['path']:r for r in records}
old={r['path']:r for r in prior if r['ref']==oldhead}
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def get(p): return by[P+p]['content']
def prev(p): return old[P+p]['content']
def scope(p):
    if not p.startswith(P): return False
    x=p[len(P):]
    return x.startswith(('src/','tools/','configs/','scripts/')) or x=='run.sh' or ('/' not in x and fnmatch.fnmatchcase(x,'requirements*.txt'))
out={'scope':'Read-only source text/hash/AST and submitted logs; no received code invocation, tests, smoke, mutation, restore, solver or installation.'}
out['files']=[{'path':r['path'],'ref':r['ref'],'bytes':len(r['content'].encode()),'sha256':sha(r['content'].encode()),'git_blob_match':blob(r['content'].encode())==r['sha']} for r in records]
assert all(r['git_blob_match'] for r in out['files'])
expected=json.loads((HERE/'EXPECTED_LOG_HASHES.json').read_text())
out['logs']=[]
for r in expected:
    raw=get('docs/22p_gap/gate91_evidence/'+r['file']).encode()
    got={'file':r['file'],'bytes':len(raw),'sha256':sha(raw),'matches':len(raw)==r['bytes'] and sha(raw)==r['sha256']}
    assert got['matches'],r['file']
    out['logs'].append(got)
comparisons=json.loads((HERE/'GIT_COMPARISONS.json').read_text())
out['scope_changes']={k:[r['filename'] for r in v['files'] if scope(r['filename'])] for k,v in comparisons.items()}
assert out['scope_changes']=={'production_diff':[P+'tools/env_profile.py'],'post_code_diff':[],'supplement_diff':[]}
tree=json.loads((HERE/'REQUEST_TREE.json').read_text());assert tree['truncated'] is False
tree_by={r['path']:r for r in tree['tree']}
oldtree=json.loads((HERE/'prior_review_data/GATE90_REQUEST_TREE.json').read_text())
while 'content' in oldtree: oldtree=json.loads(oldtree['content'])
assert oldtree['truncated'] is False
oldtree_by={r['path']:r for r in oldtree['tree']}
available={}
for n in ['PRIOR_RUN_SCOPE_SNAPSHOT.json','RECEIVED_SNAPSHOT.json']:
    available.update(json.loads((HERE/'prior_review_data'/n).read_text())['files'])
available.update(old);available.update(by)
digest=hashlib.sha256();scope_files=[]
for e in sorted(tree['tree'],key=lambda r:r['path']):
    if not scope(e['path']) or any(x in e['path'].split('/') for x in ['__pycache__','.ipynb_checkpoints']) or e['path'].endswith(('.pyc','.pyo')): continue
    b=available[e['path']]['content'].encode();assert blob(b)==e['sha'],e['path']
    digest.update(e['path'][len(P):].encode());digest.update(b)
    scope_files.append({'path':e['path'],'blob':e['sha'],'sha256':sha(b)})
assert digest.hexdigest()[:16]=='f0175fff71132003'
out['source_digest']={'files':scope_files,'count':len(scope_files),'recomputed':digest.hexdigest()[:16]}
preserve=['requirements-validation-C.lock.txt','requirements.txt','scripts/smoke_e2e.sh','docs/22p_gap/make_receipt.py','docs/22p_gap/env_profile_B_v4.yaml','src/io.py','src/fitting.py','run.sh','tests/conftest.py']
out['unchanged']={p:oldtree_by[P+p]['sha']==tree_by[P+p]['sha'] for p in preserve}
assert all(out['unchanged'].values())
ep=get('tools/env_profile.py');was=prev('tools/env_profile.py')
diff='\n'.join(difflib.unified_diff(was.splitlines(),ep.splitlines(),fromfile='gate90/tools/env_profile.py',tofile='gate91/tools/env_profile.py',lineterm=''))+'\n'
(HERE/'SOURCE_DIFF.txt').write_text(diff,encoding='utf-8')
# For changed runtime functions: compare syntax trees after only declared key/string renames and docstring removal.
renames={'in_record':'verified','path_origins':'origins','path_origin':'origin','path_origins_in_record':'origins_verified','경로 검색 origin 이 RECORD 가 있는 유효 배포판 하나의 파일':'RECORD 가 있는 설치 배포판 하나의 파일'}
class Normalize(ast.NodeTransformer):
    def visit_Constant(self,n):
        if isinstance(n.value,str) and n.value in renames: n.value=renames[n.value]
        return n
    def visit_FunctionDef(self,n):
        if n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str): n.body=n.body[1:]
        return self.generic_visit(n)
    def visit_Dict(self,n):
        pairs=[(k,v) for k,v in zip(n.keys,n.values) if not (isinstance(k,ast.Constant) and k.value=='not_measured')]
        n.keys=[x[0] for x in pairs];n.values=[x[1] for x in pairs]
        return self.generic_visit(n)
def funcs(s): return {n.name:n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
newf,oldf=funcs(ep),funcs(was)
assert set(newf)==set(oldf)
out['functions_same_after_declared_normalization']={k:ast.dump(Normalize().visit(newf[k]))==ast.dump(Normalize().visit(oldf[k])) for k in newf if k!='_summary'}
assert all(out['functions_same_after_declared_normalization'].values())
out['summary_review']='Source diff inspected manually: path-search wording, field renames and loaded-origin-unmeasured suffix; no branch/rc change.'
assert 'NOT_MEASURED = ("loaded_module_origin",)' in ep
assert '"not_measured": list(NOT_MEASURED)' in ep
out['scope_declaration']={'constant':['loaded_module_origin'],'result_initialized_before_lock_read':ep.index('"not_measured": list(NOT_MEASURED)')<ep.index('raw = lp.read_bytes()'),'summary_narrowed':'경로 검색 origin 의 RECORD 소속' in ep and '(로드된 module origin 미측정)' in ep,'C1_sentence': '측정 기능을 요구하는 회귀의 지원 환경에서는 측정 불가를 시험 실패로 본다' in ep}
# Test changes and mutation registry are inspected as text/AST only; never collected by pytest.
for path,name in [('tests/test_gate90_env_profile.py','TEST90_DIFF.txt'),('docs/22p_gap/mutation_replay.py','MUTATION_DIFF.txt')]:
    d='\n'.join(difflib.unified_diff(prev(path).splitlines(),get(path).splitlines(),fromfile='gate90/'+path,tofile='gate91/'+path,lineterm=''))+'\n'
    (HERE/name).write_text(d,encoding='utf-8')
oldnodes=set(re.findall(r'^def (test_\w+)\(',prev('tests/test_gate90_env_profile.py'),re.M))
newnodes=set(re.findall(r'^def (test_\w+)\(',get('tests/test_gate90_env_profile.py'),re.M))
out['test90_nodes_unchanged']=oldnodes==newnodes;assert out['test90_nodes_unchanged']
out['receipts']=[]
for leg in ['paired_fixed5_v4','grid_fit_v5']:
    path=f'docs/22p_gap/receipts/{leg}.validate.yaml';a=prev(path);b=get(path)
    history=get(f'docs/22p_gap/receipts/history/{leg}.validate.3f84c0db52d2b9ac.yaml')
    assert a==history
    ac=a.split('\ncore:\n')[1].split('\nstamp:\n')[0];bc=b.split('\ncore:\n')[1].split('\nstamp:\n')[0]
    norm=lambda x:re.sub(r'(?m)^(    validator_source_digest: ).*',r'\1<generation>',x)
    assert norm(ac)==norm(bc)
    ch=re.search(r'^core_sha256: ([0-9a-f]{64})$',b,re.M)[1]
    assert ch in get('docs/22p_gap/LEG_PRESERVATION.yaml')
    assert '    not_measured:\n    - loaded_module_origin' in b and '      path_origins_in_record: 9' in b
    out['receipts'].append({'leg':leg,'history_exact_previous':True,'core_content_changes_only':['validator_source_digest'],'core_sha_recorded_not_reserialized':ch,'anchor_present':True,'stamp_has_unmeasured_declaration':True,'validator_tree_dirty':re.search(r'  validator_tree_dirty: (.+)',b)[1]})
    (HERE/(leg+'_RECEIPT_DIFF.txt')).write_text('\n'.join(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile='gate90/'+leg,tofile='gate91/'+leg,lineterm=''))+'\n',encoding='utf-8')
full=get('docs/22p_gap/gate91_evidence/12_full_replay_f27006370_412_of_412_rc0.log')
counts={'killed':len(re.findall(r'^물었다',full,re.M)),'survived':len(re.findall(r'^★ 안 물었다',full,re.M)),'errors':len(re.findall(r'^★ 실행오류',full,re.M)),'declared':len(re.findall(r'^신고',full,re.M))}
assert counts=={'killed':412,'survived':0,'errors':0,'declared':11}
out['replay_log_counts']=counts
profile_log=get('docs/22p_gap/gate91_evidence/08_env_profile_json_f27006370_match.log')
profile=json.loads(next(l for l in profile_log.splitlines() if l.startswith('{')))
assert profile['not_measured']==['loaded_module_origin'] and profile['counts']['path_origins_in_record']==9 and profile['status']=='MATCH'
out['submitted_profile_json']=profile
out['raw_log_claim_checks']={
 'pytest_2182': '2182 passed, 1 xfailed' in get('docs/22p_gap/gate91_evidence/10_full_pytest_f27006370_2182passed.log'),
 'smoke_rc0': 'smoke rc=0' in get('docs/22p_gap/gate91_evidence/11_smoke_f27006370_rc0.log'),
 'docs_lint_358': '358 passed' in get('docs/22p_gap/gate91_evidence/14_docs_lint_send_43056f78d_358passed.log')}
assert all(out['raw_log_claim_checks'].values())
out['limitations']=['No submitted code executed. No remote live measurement. Log counts are submitted evidence, not reviewer reruns.','Receipt core hashes checked as recorded scalars and anchors; no YAML reserialization or restore.','Git comparisons are fixed endpoint comparisons, not a full intermediate commit execution audit.']
(HERE/'STATIC_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_digest':out['source_digest']['recomputed'],'scope_files':len(scope_files),'log_hashes_verified':len(out['logs']),'unchanged':out['unchanged'],'normalized_functions':out['functions_same_after_declared_normalization'],'receipts':out['receipts'],'replay':counts},ensure_ascii=False))
