"""Record immutable snapshot comparisons and review-time pin lookup evidence."""
from pathlib import Path
import datetime,hashlib,json,os,urllib.request
R=Path(__file__).resolve().parents[1]
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def get(path):
    u='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'+path
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'read-only-review'}),timeout=60))
path='docs/reviews/codex_lhs214r_fix_recheck_request_20261016.md'
lookup=get('commits?sha=claude%2Fstoic-knuth-NObVQ&path='+path+'&per_page=10')
head=get('commits/claude%2Fstoic-knuth-NObVQ')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_evidence_path':path,'request_history':lookup,'branch_head_observed':head['sha'],'code_pin':'60ba39e224aff48a030dccfe750342f3bf9db61f','base_pin':'6cb2569569ec74b7f5a96e0ef19494e872da5272'}
trees={f:json.loads((R/'evidence'/f'tree_{p}.json').read_text(encoding='utf8')) for f,p in [('source','60ba39e22'),('base','6cb256956')]}
out['request_and_evidence_at_code_pin']=[e['path'] for e in trees['source']['tree'] if 'lhs214r' in e['path']]
maps={f:{e['path']:e['sha'] for e in t['tree'] if e['type']=='blob'} for f,t in trees.items()}
out['script_web_changes']=[p for p in sorted(maps['source'].keys()|maps['base'].keys()) if p.startswith(('scripts/','webapp/')) and maps['source'].get(p)!=maps['base'].get(p)]
old=json.loads((R.parent/'lhs214_fix_reverify_20261015/evidence/tree_9e3ef54ca.json').read_text(encoding='utf8'))
om={e['path']:e['sha'] for e in old['tree'] if e['type']=='blob'}
out['previous_pin_to_base_script_web_changes']=[p for p in sorted(om.keys()|maps['base'].keys()) if p.startswith(('scripts/','webapp/')) and om.get(p)!=maps['base'].get(p)]
(R/'evidence/pin_resolution.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
integrity={}
for label in ('source','base'):
    m=json.loads((R/f'{label}_manifest.json').read_text(encoding='utf8'));bad=[]
    for row in m['files']:
        b=long(R/label/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['git_blob']:bad.append(row['path'])
    integrity[label]={'files':len(m['files']),'mismatches':bad,'pin':m['pin']}
(R/'integrity.json').write_text(json.dumps(integrity,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'request_history_count':len(lookup),'script_web_changes':len(out['script_web_changes']),'prev_to_base':out['previous_pin_to_base_script_web_changes'],'integrity':integrity},ensure_ascii=False,indent=2))
