from pathlib import Path
import ast,hashlib,json,sys
R=Path(__file__).resolve().parents[1];S=R/'source';OLD=R/'baseline'
sys.path.insert(0,str(S/'scripts'))
import run_network_194_parallel as N
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={p:sha(S/p) for p in N.CODE_FILES}
oldfiles={p:sha(OLD/p) for p in N.CODE_FILES}
out={'pin':json.loads((R/'source_manifest.json').read_text())['pin'],'sealed_count':len(files),'sealed_changed':[p for p in files if files[p]!=oldfiles[p]],'hashes':files,
 'new_handover':{p:sha(S/p) for p in N.HANDOVER_FILES},'old_handover':{p:sha(OLD/p) for p in N.HANDOVER_FILES},
 'request_matches_pin':(R/'submitted/request.md').read_bytes()==(S/'docs/reviews/codex_supp20_support_review_request_20261012.md').read_bytes(),
 'artifact_missing_as_declared':{p:not(S/p).exists() for p in ['docs/data/lhss_descriptors_cov_1e09f661d','docs/data/lhss_union_1e09f661d/lhss20_union.tsv']}}
for key in ['production194','supp20']:
    try:
        d=N.registered_id_set(key);out[key]={'n':len(d['pairs']),'digest':N.ids_digest(d['pairs'])}
    except N.LaunchError as e:out[key]={'error':str(e)}
def fns(p):
    tree=ast.parse(p.read_text(encoding='utf8'))
    return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
for p in ['scripts/g2_network_reread.py','scripts/run_network_194_parallel.py']:
    a,b=fns(OLD/p),fns(S/p)
    out[p]={'functions_added':sorted(set(b)-set(a)),'functions_changed':sorted(k for k in a.keys()&b.keys() if a[k]!=b[k]),'functions_removed':sorted(set(a)-set(b))}
(R/'evidence/snapshot_contract.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='hashes'},ensure_ascii=False,indent=2))
