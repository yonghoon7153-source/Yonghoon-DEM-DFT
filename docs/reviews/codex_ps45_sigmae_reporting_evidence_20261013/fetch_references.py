from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request
R=Path(__file__).resolve().parent
urls={
 'ketter2025_main.pdf':'https://juser.fz-juelich.de/record/1040442/files/s41467-025-56514-5.pdf?version=1',
 'ketter2025_si.pdf':'https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-56514-5/MediaObjects/41467_2025_56514_MOESM1_ESM.pdf',
 'ketter2025.html':'https://www.nature.com/articles/s41467-025-56514-5',
 'minnmann_thesis.pdf':'https://jlupub.ub.uni-giessen.de/server/api/core/bitstreams/62b7b618-5ae3-423e-98cd-28d39c4b0749/content',
 'minnmann2021.html':'https://iopscience.iop.org/article/10.1149/1945-7111/abf8d7/meta',
 'trevisanello2021.pdf':'https://d-nb.info/1372186662/34',
}
def get(item):
    name,url=item
    out={'name':name,'url':url}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as f:
            raw=f.read();out['content_type']=f.headers.get('Content-Type');out['final_url']=f.url
        if name.endswith('.pdf') and not raw.startswith(b'%PDF'):raise ValueError('Not a PDF')
        (R/'literature'/name).write_bytes(raw)
        out.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),status='downloaded')
    except Exception as e:out.update(status='unavailable',error=str(e))
    print(json.dumps(out),flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,urls.items()))
(R/'evidence/literature_downloads.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
