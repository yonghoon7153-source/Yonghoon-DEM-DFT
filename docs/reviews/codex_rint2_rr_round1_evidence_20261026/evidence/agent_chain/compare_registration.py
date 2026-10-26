import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
here=Path(__file__).parent
m=json.loads((root/'evidence/source_manifest.json').read_text(encoding='utf-8-sig'))
verified=[]
for label,side in [('current','repo'),('baseline','baseline')]:
    j=json.loads((here/('registration_'+label+'.json')).read_text(encoding='utf-8'))
    for path,sha in j['meta']['source_hashes'].items():
        ent=next(x for x in m['files'] if x['side']==side and x['path']==path)
        assert ent['sha256']==sha
        raw=(root/side/path).read_bytes()
        assert hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()==ent['git_blob']
        verified.append(dict(side=side,path=path,sha256=sha,git_blob=ent['git_blob']))
a=json.loads((here/'registration_baseline.json').read_text(encoding='utf-8'))['results']
b=json.loads((here/'registration_current.json').read_text(encoding='utf-8'))['results']
old=json.loads((root/'evidence/prior_artifact/probe_results.json').read_text(encoding='utf-8-sig'))
def compare(a,b,path=''):
    eq,diffs=0,[]
    if type(a)!=type(b): return 0,[(path,a,b)]
    if isinstance(a,dict):
        for k in sorted(a.keys()|b.keys()):
            if k not in a or k not in b: diffs.append((path+'/'+k,a.get(k),b.get(k)))
            else:
                x,y=compare(a[k],b[k],path+'/'+k); eq+=x; diffs+=y
    elif isinstance(a,list):
        if len(a)!=len(b): return 0,[(path,a,b)]
        for i,(aa,bb) in enumerate(zip(a,b)):
            x,y=compare(aa,bb,path+'/'+str(i)); eq+=x; diffs+=y
    elif a==b: eq+=1
    else: diffs.append((path,a,b))
    return eq,diffs
# The original metadata pin is outside numerical/decision comparison.
old.pop('pin',None)
same_baseline=compare(old,a)
ca,cb=dict(a),dict(b); ca.pop('DBE_R_monotonicity'); cb.pop('DBE_R_monotonicity')
same_except=compare(ca,cb)
res={'pin':m['pin'],'baseline':m['baseline'],'verified':verified,
     'baseline_adapted_vs_original':dict(exact_leaves=same_baseline[0],differences=same_baseline[1]),
     'current_vs_baseline_except_DBE_R_monotonicity':dict(exact_leaves=same_except[0],differences=same_except[1]),
     'changed_section':{'before':a['DBE_R_monotonicity'],'after':b['DBE_R_monotonicity']}}
assert not same_baseline[1] and not same_except[1]
(here/'comparison.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in res.items() if k!='verified'},ensure_ascii=False,indent=2))

