"""Read only retrieval of pinned review sources; no checkout or execution."""
from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, urllib.parse

R = Path(__file__).resolve().parent
REPO = 'yonghoon7153-source/Yonghoon-DEM-DFT'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Codex-seminar-review'}), timeout=40) as f:
        return f.read()
def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        assert p.read_bytes()==b, str(p)
    else:
        p.write_bytes(b)
commit=json.loads(fetch(f'https://api.github.com/repos/{REPO}/commits/90ca2c8cd'))
PIN=commit['sha']
save(R/'evidence/pin_commit.json', json.dumps(commit,ensure_ascii=False,indent=2).encode())
tree=json.loads(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1'))
assert not tree.get('truncated')
save(R/'evidence/tree.json',json.dumps(tree,ensure_ascii=False,indent=2).encode())
ent={x['path']:x for x in tree['tree'] if x['type']=='blob'}
paths={
 'AGENTS.md','docs/session_20260923_progress.md',
 'docs/dem_governing_equations_background_20261011.md',
 'docs/dem_governing_equations_report_20261009.md',
 'docs/hetero_thesis.md','docs/reviews/findings.json','docs/reviews/claims.json',
 'docs/reviews/codex_review_model_validation_20261008.md',
 'docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md',
 'docs/reviews/lee_abs_sigma_e_prereg_20260923.md',
 'docs/reviews/codex_review_seminar_deck_v3_1_closure_20261013.md',
 'docs/reviews/codex_review_dem_unloading_kit_20261014.md',
 'docs/reviews/dem_unloading_kit_fix_plan_20261014.md',
 'docs/reviews/dem_unloading_history_test_20261014/README.md',
 'docs/data/liggghts_add_pair_pin.json',
 'docs/data/liggghts_3d5c00f_dem_eq_source_20261009/README.md'}
paths|={p for p in ent if p.startswith('docs/data/ps73_damping_branch_20261007/') and ent[p].get('size',0)<10_000_000}
paths|={p for p in ent if p.endswith('/AGENTS.md') and p.startswith('docs/')}
paths|={str(p.relative_to(R/'input/repo')).replace('\\','/') for p in (R/'input/repo').rglob('*') if p.is_file()}
def get(p):
    if p not in ent: return {'path':p,'missing_at_pin':True}
    e=ent[p]; b=None
    for local in [R/'input/repo'/p,R.parent/'dem_unloading_kit_reverify_20261014/source'/p,R.parent/'model_validation_review_20261008/source'/p]:
        if local.exists():
            candidate=local.read_bytes()
            if blob(candidate)==e['sha']: b=candidate; break
    if b is None: b=fetch(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'],p
    save(R/'source'/p,b)
    return {'path':p,'blob_sha':e['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    records=list(pool.map(get,sorted(paths)))
save(R/'evidence/source_manifest.json',json.dumps({'pin':PIN,'files':records},ensure_ascii=False,indent=2).encode())
print(json.dumps({'pin':PIN,'files':len(records),'missing':[x['path'] for x in records if x.get('missing_at_pin')]}))
