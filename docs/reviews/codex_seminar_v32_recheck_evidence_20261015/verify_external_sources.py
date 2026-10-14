from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request
R=Path(__file__).resolve().parent
litpin=json.loads((R/'evidence/lit_branch_commit.json').read_text(encoding='utf8'))['sha']
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-review'}),timeout=40) as f: return f.read()
def record(p,url):
    b=fetch(url); match=p.exists() and p.read_bytes()==b
    normalized_equal=p.exists() and p.read_bytes().rstrip(b'\r\n')==b.rstrip(b'\r\n')
    if not p.exists(): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
    raw=R/'external_fetched'/p.name; raw.parent.mkdir(parents=True,exist_ok=True); raw.write_bytes(b)
    return {'path':str(p.relative_to(R)),'raw_path':str(raw.relative_to(R)),'url':url,'bytes':len(b),'local_equal':match,'equal_ignoring_final_newline':normalized_equal,'sha256':hashlib.sha256(b).hexdigest(),'blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
jobs=[(p,f'https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/{litpin}/litdb/papers/{p.name}') for p in (R/'agents/lit').glob('*.md')]
up='3d5c00f20519e6bb6eb6756f51f1ad36564e649d'
jobs += [(R/'source_upstream'/name,f'https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/{up}/src/{name}') for name in ['surface_model_default.h','tangential_model_history.h','normal_model_hooke_hysteresis.h','rolling_model_cdt.h']]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    rows=list(pool.map(lambda a:record(*a),jobs))
(R/'evidence/external_sources.json').write_text(json.dumps({'lit_pin':litpin,'liggghts_pin':up,'files':rows},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'lit_pin':litpin,'card_matches':[(x['path'],x['equal_ignoring_final_newline']) for x in rows if '/lit/' in x['path'].replace('\\','/')],'files':len(rows)},ensure_ascii=True))
