import ast, hashlib, json
from pathlib import Path

R = Path(__file__).resolve().parent
S = R / 'codekey_sources/scripts'
tree = json.loads((R / 'remote_scripts_tree.json').read_text(encoding='utf-8'))
assert not tree['truncated']
remote = {x['path']: x for x in tree['tree']}
source = S / 'rint_r_chain.py'
module = ast.parse(source.read_text(encoding='utf-8'))
names = None
for n in module.body:
    if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'CODE_FILES' for t in n.targets):
        names = ast.literal_eval(n.value)
assert names and len(names) == 19
rows=[]
for name in names:
    b=(S/name).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    rows.append({'file':name,'sha256':hashlib.sha256(b).hexdigest(),'git_blob':blob,
                 'remote_git_blob':remote[name]['sha'],'match':blob==remote[name]['sha']})
old = R/'remote_toolpin_README.md'
b=old.read_bytes()
expected='6401d4f9a2850946588e4929326c13ff319827720f47f55165f69c748f7859f2'
# apply_patch added an LF to the remote tool response. Restore exactly the verified historical bytes in this evidence copy.
if hashlib.sha256(b).hexdigest()!=expected:
    assert b.endswith(b'\n') and hashlib.sha256(b[:-1]).hexdigest()==expected
    old.write_bytes(b[:-1])
result={'files':len(rows),'matched':sum(x['match'] for x in rows),'rows':rows,
        'scripts_tree':tree['sha'],'historical_README_sha256':hashlib.sha256(old.read_bytes()).hexdigest()}
(R/'codekey_sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
assert all(x['match'] for x in rows)
