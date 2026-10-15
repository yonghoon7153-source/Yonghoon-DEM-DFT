"""Copy immutable prior probes/old sources; audit current/previous content hashes."""
from pathlib import Path
import ast,hashlib,json,shutil,difflib,re
R=Path(__file__).resolve().parent
O=R.parent/'rint_g2_impl_review_20261014'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy_exact(a,b):
    b.parent.mkdir(parents=True,exist_ok=True)
    if b.exists():assert a.read_bytes()==b.read_bytes(),str(b)
    else:shutil.copyfile(a,b)
    return {'source':str(a.relative_to(R.parent)),'copy':str(b.relative_to(R)), 'sha256':sha(b)}
copied=[]
for name in ('owner_vox_mismatch.py','off_compatibility.py','owner_independent.py'):
    copied.append(copy_exact(O/'probes'/name,R/'probes'/name))
copied.append(copy_exact(O/'source_prior/step3_sigma.py',R/'source_prior/step3_sigma.py'))
copied.append(copy_exact(O/'source/scripts/step3_sigma.py',R/'source_prior/step3_sigma_before_fix.py'))
files=['rint_t2_dev.py','rint_iface_join.py','rint_rrm_reference.py','step3_sigma.py']
diff=[]
for f in files:
    a=(O/'source/scripts'/f).read_text(encoding='utf8').splitlines(True)
    b=(R/'source/scripts'/f).read_text(encoding='utf8').splitlines(True)
    diff.extend(difflib.unified_diff(a,b,fromfile='1087a9b2f/scripts/'+f,tofile='dcb97f1ed/scripts/'+f))
(R/'evidence/reviewed_source.diff').write_text(''.join(diff),encoding='utf8')
old={x['path']:x for x in json.loads((O/'source_manifest.json').read_text(encoding='utf8'))['files']}
new={x['path']:x for x in json.loads((R/'source_manifest.json').read_text(encoding='utf8'))['files']}
def literal_constant(path,name):
    for n in ast.parse(path.read_text(encoding='utf8')).body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
code=literal_constant(R/'source/scripts/run_network_194_parallel.py','CODE_FILES')
mods=['scripts/'+p for p in literal_constant(R/'source/scripts/seal_s3_prerun.py','NUMERIC_MODULES')]
# Verify full trees, not just the locally downloaded subset.
oldtrees=list((O/'evidence').glob('*tree*.json'))
oldtree=None
for p in oldtrees:
    obj=json.loads(p.read_text(encoding='utf8'))
    if 'tree' in obj:oldtree={x['path']:x['sha'] for x in obj['tree'] if x['type']=='blob'};break
newtree={x['path']:x['sha'] for x in json.loads((R/'evidence/tree.json').read_text(encoding='utf8'))['tree'] if x['type']=='blob'}
def compare(ps):
    return [{'path':p,'old_blob':oldtree.get(p) if oldtree else old.get(p,{}).get('git_blob'),
             'new_blob':newtree.get(p),
             'same':(oldtree.get(p) if oldtree else old.get(p,{}).get('git_blob'))==newtree.get(p)} for p in ps]
hashes=[]
for phase in ('tests_first','final'):
    path=R/'source/docs/reviews/rint_g2_impl_fix_evidence_20261015'/phase/'HASHES.txt'
    for line in path.read_text(encoding='utf8').splitlines():
        m=re.match(r'^([0-9a-f]{40})\s+([0-9a-f]{64})\s+(\S+)',line)
        if not m:continue
        blob,hs,p=m.groups();q=R/'source'/p
        hashes.append({'phase':phase,'path':p,'declared_sha256':hs,
            'matches_final_pin':q.exists() and sha(q)==hs,
            'matches_prior_pin':(O/'source'/p).exists() and sha(O/'source'/p)==hs})
out={'copies':copied,'fixed_source_changes':compare(['scripts/'+x for x in files]),
     'sealed_32':compare(code),'s3_numeric_6':compare(mods),'submitted_hash_checks':hashes,
     'old_full_tree_available':oldtree is not None}
(R/'evidence/integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'sealed32':len(code),'unchanged32':sum(x['same'] for x in out['sealed_32']),
    's3modules':len(mods),'unchanged6':sum(x['same'] for x in out['s3_numeric_6']),
    'copies':len(copied),'oldtree':oldtree is not None},indent=2))
