from pathlib import Path, PurePosixPath
import zipfile, hashlib, json, stat
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
SRC=Path('C:/Users/Administrator/Downloads')
ZIP=SRC/'COMSOL63_NORMAL480_SAVED_ANALYSIS_20261001.zip'
PDF=SRC/'NORMAL480_ANALYSIS.pdf'
def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'bytes':p.stat().st_size,'sha256':h}
def save(n,d): (ROOT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(ZIP) as z:
    infos=z.infolist(); names=[i.filename for i in infos]
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for i in infos:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
    manifest=json.loads(z.read('DERIVED_MANIFEST.json'))
    assert set(names)=={'DERIVED_MANIFEST.json'}|{x['file'] for x in manifest['files']}
    assert len(manifest['files'])==len(names)-1
    for e in manifest['files']:
        b=z.read(e['file'])
        assert len(b)==e['bytes'] and sha(b)==e['sha256'], e['file']
    assert z.testzip() is None
    assert z.read('NORMAL480_ANALYSIS.pdf')==PDF.read_bytes()
    destination=ROOT/'received'
    assert not destination.exists()
    z.extractall(destination)
    audit={'status':'PASS','zip':identity(ZIP),'pdf':identity(PDF),'payload_count':len(names)-1,'manifest_sha256':sha(z.read('DERIVED_MANIFEST.json')),'exact_set_size_sha_crc_path_case_links':True,'standalone_pdf_equals_zip':True}
    prior=ROOT.parent/'normal480_native_review_20261001'
    audit['prior_review_byte_comparisons']={n:z.read('received/'+n)==(prior/n).read_bytes() for n in ['DECISION.json','NEXT_CODEX_REPLY_KO.md','REVIEW_KO.md','REVIEW_MANIFEST.json']}
    assert all(audit['prior_review_byte_comparisons'].values())
    save('ARCHIVE_AUDIT.json',audit)
reader=PdfReader(PDF)
text='\n\n'.join(f'PAGE {i+1}\n{p.extract_text()}' for i,p in enumerate(reader.pages))
(ROOT/'PDF_EXTRACTED.txt').write_text(text,encoding='utf-8')
audit['pdf_pages']=len(reader.pages)
save('ARCHIVE_AUDIT.json',audit)
print(json.dumps(audit,ensure_ascii=False))
