"""Read-only lineage, pin-scope and byte verification. Not a launch receipt."""
from pathlib import Path
import ast,difflib,hashlib,json,os,urllib.request
R=Path(__file__).resolve().parents[1]; OLD=R.parent/'rint_g2_impl_reverify_20261015'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def long(p):
    s=str(p)
    return Path('\\\\?\\'+s) if os.name=='nt' and not s.startswith('\\\\?\\') else p
def read(p):return long(p).read_bytes()
def save(n,x):(R/'evidence'/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def gitjson(sha):
    p=R/'evidence'/('commit_'+sha+'.json')
    if not p.exists():
        with urllib.request.urlopen(urllib.request.Request(f'https://api.github.com/repos/{REPO}/commits/{sha}',headers={'User-Agent':'Read-only-review'}),timeout=45) as f:p.write_bytes(f.read())
    return json.loads(p.read_text(encoding='utf8'))
def constant(path,name):
    for n in ast.parse(read(path).decode('utf8')).body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):
            return ast.literal_eval(n.value)
    raise KeyError(name)
mf=json.loads(read(R/'source_manifest.json'))
base=json.loads(read(OLD/'source_manifest.json'))
trees=[json.loads(read(R/'evidence'/n)) for n in ('base_tree.json','tree.json')]
maps=[{x['path']:x['sha'] for x in t['tree'] if x['type']=='blob'} for t in trees]
seal=constant(R/'source/scripts/run_network_194_parallel.py','CODE_FILES')
s3=constant(R/'source/scripts/seal_s3_prerun.py','NUMERIC_MODULES')
check=lambda paths:[dict(path=p,old=maps[0].get(p),new=maps[1].get(p),same=maps[0].get(p)==maps[1].get(p)) for p in paths]
diffs={}
for p in ('scripts/rint_iface_join.py','scripts/step3_sigma.py','scripts/test_rint_g2_join.py','scripts/test_rint_g2_am_iface.py','scripts/test_rint_g2_rrm.py'):
    a=read(OLD/'source'/p).decode('utf8').splitlines(True); b=read(R/'source'/p).decode('utf8').splitlines(True)
    diffs[p]=''.join(difflib.unified_diff(a,b,fromfile=base['pin']+'/'+p,tofile=mf['pin']+'/'+p))
(R/'evidence/reviewed_source.diff').write_text(''.join(diffs.values()),encoding='utf8')
save('reviewed_source_diff.json',diffs)
commits=[]
for sha in ('3b9d51789',mf['pin']):
    c=gitjson(sha)
    commits.append(dict(sha=c['sha'],parents=[p['sha'] for p in c['parents']],message=c['commit']['message'],
                        files=[f['filename'] for f in c['files']],sealed_touched=[f['filename'] for f in c['files'] if f['filename'] in seal]))
integrity=[]
for folder,m in ((R,mf),(OLD,base)):
    bad=[]
    for item in m['files']:
        b=read(folder/'source'/item['path'])
        if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256'] or blob(b)!=item['git_blob']:
            bad.append(item['path'])
    integrity.append(dict(folder=folder.name,pin=m['pin'],files=len(m['files']),bad=bad))
out=dict(pin=mf['pin'],base=base['pin'],seal_comparison=check(seal),s3_comparison=check(s3),patch_commits=commits,source_integrity=integrity)
save('root_metadata.json',out)
print(json.dumps(dict(seal_changed=[x['path'] for x in out['seal_comparison'] if not x['same']],
                      s3_changed=[x['path'] for x in out['s3_comparison'] if not x['same']],
                      patch_seal_changes=[dict(sha=c['sha'],paths=c['sealed_touched']) for c in commits],
                      integrity=integrity),ensure_ascii=False))
