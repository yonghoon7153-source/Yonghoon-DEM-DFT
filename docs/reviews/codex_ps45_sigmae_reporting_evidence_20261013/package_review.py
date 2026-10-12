"""Package review evidence; exclude full external papers and transient renders."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
urls={
 'ketter2025_si.pdf':'https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-56514-5/MediaObjects/41467_2025_56514_MOESM1_ESM.pdf',
 'ketter2025_source_data.zip':'https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-56514-5/MediaObjects/41467_2025_56514_MOESM3_ESM.zip',
 'ketter2025.html':'https://www.nature.com/articles/s41467-025-56514-5',
 'minnmann_thesis.pdf':'https://jlupub.ub.uni-giessen.de/server/api/core/bitstreams/62b7b618-5ae3-423e-98cd-28d39c4b0749/content',
 'trevisanello2021.pdf':'https://d-nb.info/1372186662/34',
 'minnmann2021.html':'https://iopscience.iop.org/article/10.1149/1945-7111/abf8d7/meta'}
lit=[]
for name,url in urls.items():
    p=R/'literature'/name
    if not p.exists():continue
    usable=name!='minnmann2021.html'
    if name.endswith('.pdf'):assert p.read_bytes().startswith(b'%PDF')
    lit.append({'file':name,'url':url,'bytes':p.stat().st_size,'sha256':h(p),
                'source_status':'primary document/author reprint accessed' if usable else 'bot-check HTML, NOT article, NOT used',
                'included_in_delivery_zip':False})
(R/'evidence/literature_access_final.json').write_text(json.dumps(lit,ensure_ascii=False,indent=2),encoding='utf8')
excluded={'literature','tmp','__pycache__'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(R).parts) and p.name not in {'DELIVERY_MANIFEST.json','DELIVERY_RECEIPT.json'}]
manifest={'scope':'ps45 report-only review; no production edits or real-bed reruns','files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)} for p in sorted(files)]}
mp=R/'DELIVERY_MANIFEST.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
files.append(mp)
dest=R.parent/'codex_ps45_sigmae_reporting_review_20261013.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,R.name+'/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for item in manifest['files']:
        assert hashlib.sha256(z.read(R.name+'/'+item['path'])).hexdigest()==item['sha256']
receipt={'zip':str(dest),'bytes':dest.stat().st_size,'sha256':h(dest),'entries':len(files),'manifest_sha256':h(mp),'zip_recheck':'PASS'}
(R/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
