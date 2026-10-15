"""Byte identity, submitted Linux log consistency and immutable metadata audit."""
from pathlib import Path
import hashlib,json,re,urllib.request,urllib.parse
R=Path(__file__).resolve().parents[1];OLD=R.parent/'dem_unloading_kit_reverify_20261014'
K=R/'source/docs/data/ps45_unload_20261009';repo='yonghoon7153-source/Yonghoon-DEM-DFT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get(path):
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/'+repo+'/'+path,headers={'User-Agent':'Codex-readonly-review'}),timeout=30) as f:return json.load(f)
cur=json.loads((R/'source_manifest.json').read_text());old=json.loads((OLD/'source_manifest.json').read_text())
om={x['path']:x for x in old['files']};cm={x['path']:x for x in cur['files']}
out={'pin':cur['pin'],'source_byte_violations':[p for p,x in cm.items() if sha(R/'source'/p)!=x['sha256']],
     'changed_kit_vs_previous':[p for p in cm if p.startswith('docs/data/ps45_unload_20261009/') and p in om and cm[p]['sha256']!=om[p]['sha256']],
     'params_equal':(K/'unload_params.json').read_bytes()==(OLD/'source/docs/data/ps45_unload_20261009/unload_params.json').read_bytes(),
     'production_decks_equal':all(p.read_bytes()==(OLD/'source/docs/data/ps45_unload_20261009'/p.relative_to(K)).read_bytes() for p in (K/'decks').rglob('*.liggghts')),
     'seals':{str(p.relative_to(K)):sha(p) for p in [K/'SHA256SUMS',K/'history_test/SHA256SUMS']},'linux_suites':{}}
E=R/'source/docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014'
for folder in E.iterdir():
    if not (folder/'summary.json').is_file():continue
    s=json.loads((folder/'summary.json').read_text(encoding='utf-8'));rows=[]
    for x in s.get('results',[]):
        txt=(folder/(x['name']+'.log')).read_text(encoding='utf-8')
        ok=sum(ln.lstrip().startswith('✓') for ln in txt.splitlines());fail=sum(ln.lstrip().startswith('✗') for ln in txt.splitlines())
        rows.append({'name':x['name'],'rc':x['rc'],'ok':ok,'fail':fail,'summary_matches':ok==x['n_check_lines_ok'] and fail==x['n_check_lines_fail'],
                     'footer_rc_matches':txt.rstrip().endswith(f'# ── rc = {x["rc"]} ──')})
    out['linux_suites'][folder.name]={'git_head':s.get('git_head'),'seal_match':s.get('kit_SHA256SUMS_sha256')==sha(K/'SHA256SUMS'),'rows':rows}
# Exact tree identities avoid treating unavailable agent worktree commits as
# remotely verified. Original Linux stdout remains author-supplied evidence.
out['commit_metadata']={}
for ref in [cur['pin'],'039abb141','70b3fefed','4a8b55013','b1121b6b6','e271bdd48']:
    c=get('commits/'+ref);tr=get('git/trees/'+c['sha']+'?recursive=1');assert not tr.get('truncated')
    kit=next(x for x in tr['tree'] if x['path']=='docs/data/ps45_unload_20261009')
    out['commit_metadata'][ref]={'sha':c['sha'],'kit_tree':kit['sha'],'message':c['commit']['message'],'parents':[p['sha'] for p in c['parents']]}
request='docs/reviews/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md'
cs=get('commits?sha='+urllib.parse.quote('claude/stoic-knuth-NObVQ',safe='')+'&path='+urllib.parse.quote(request)+'&per_page=5')
out['request_history']=[{'sha':c['sha'],'message':c['commit']['message']} for c in cs]
for c in cs:
    details=get('commits/'+c['sha'])
    if any('SELF-116' in (f.get('patch') or '') for f in details.get('files',[])):
        out['self116_correction']={'sha':c['sha'],'files':details.get('files',[])}
        changed=[]
        for f in details.get('files',[]):
            if f['filename'] in (request,'docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/README.md'):
                url=f'https://raw.githubusercontent.com/{repo}/{c["sha"]}/'+urllib.parse.quote(f['filename'])
                with urllib.request.urlopen(url,timeout=30) as response: data=response.read()
                dest=R/'submitted'/('corrected_'+Path(f['filename']).name)
                dest.write_bytes(data)
                changed.append({'file':f['filename'],'sha256':hashlib.sha256(data).hexdigest()})
        out['corrected_submitted_files']=changed
        out['attached_request_equals_corrected']=(R/'submitted/request.md').read_text(encoding='utf-8').strip()==(R/'submitted'/('corrected_'+Path(request).name)).read_text(encoding='utf-8').strip()
        break
(R/'evidence/source_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:out[k] for k in ['pin','source_byte_violations','params_equal','production_decks_equal','seals','request_history']},ensure_ascii=False,indent=2))
