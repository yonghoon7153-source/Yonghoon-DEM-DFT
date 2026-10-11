from pathlib import Path
import json,hashlib,urllib.request,urllib.parse,concurrent.futures
R=Path(__file__).resolve().parent;S=R/'source';PIN='a20fc1875951bead5fad4a4d387e77b4979b84c6'
T=json.loads((R/'tree.json').read_text())
paths=[e for e in T['tree'] if e['type']=='blob' and (e['path'].startswith(('docs/data/real14_reference_20260928/','docs/data/case15_corner_20261001/','docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_observation_run2/')) or e['path'] in ('.github/workflows/discipline.yml','docs/reviews/lhs_release_v13_plan_20261007.md','docs/reviews/findings.json','docs/reviews/codex_review_gen2_network_reverify4_20261007.md')) and not (S/e['path']).is_file()]
def get(e):
    p=e['path'];b=urllib.request.urlopen('https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+urllib.parse.quote(p),timeout=90).read()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
    d=S/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=False)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: rows=list(ex.map(get,paths))
m=json.loads((R/'source_manifest.json').read_text());m['files'].extend(rows)
(R/'source_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
print('ADDED',len(rows),[x['path'] for x in rows])
