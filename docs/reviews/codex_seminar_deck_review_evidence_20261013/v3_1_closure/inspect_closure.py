"""Inspect and compare delivered files. Never executes delivered code."""
from pathlib import Path, PurePosixPath
import zipfile, json, hashlib, posixpath, difflib
from lxml import etree as E
from pypdf import PdfReader

R = Path(__file__).resolve().parent
for folder in ('input','evidence','renders','notes'):
    (R/folder).mkdir(parents=True, exist_ok=True)
archive = Path('C:/Users/Administrator/Downloads/codex_seminar_deck_v3_1_closure_20261013.zip')
sha = lambda b: hashlib.sha256(b).hexdigest()
inventory=[]
with zipfile.ZipFile(archive) as z:
    assert sum(x.file_size for x in z.infolist()) < 200_000_000
    seen=set()
    for entry in z.infolist():
        p=PurePosixPath(entry.filename.replace('\\','/'))
        assert not p.is_absolute() and '..' not in p.parts and ':' not in str(p)
        assert (entry.external_attr>>16)&0o170000 != 0o120000
        if entry.is_dir(): continue
        p=PurePosixPath(*p.parts[1:])
        assert str(p).casefold() not in seen
        seen.add(str(p).casefold())
        blob=z.read(entry); target=R/'input'/Path(*p.parts)
        target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
        inventory.append(dict(path=p.as_posix(),bytes=len(blob),sha256=sha(blob)))

ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def rels(z,path):
    return {n.get('Id'):dict(target=n.get('Target'),type=n.get('Type'),external=n.get('TargetMode')=='External') for n in E.fromstring(z.read(path))}
def texts(xml): return xml.xpath('.//a:t/text() | .//m:t/text()',namespaces=ns)
slides=[]
ppt=R/'input/deck/seminar_20261013_v3_1.pptx'
with zipfile.ZipFile(ppt) as z:
    pres=E.fromstring(z.read('ppt/presentation.xml')); pr=rels(z,'ppt/_rels/presentation.xml.rels')
    for i,sl in enumerate(pres.findall('p:sldIdLst/p:sldId',ns),1):
        sp=posixpath.normpath('ppt/'+pr[sl.get('{'+ns['r']+'}id')]['target'])
        xml=E.fromstring(z.read(sp)); rp=posixpath.dirname(sp)+'/_rels/'+posixpath.basename(sp)+'.rels'
        sr=rels(z,rp) if rp in z.namelist() else {}; notes=[]; media=[]; shapes=[]
        for rel in sr.values():
            if rel['external']: continue
            loc=posixpath.normpath(posixpath.dirname(sp)+'/'+rel['target'])
            if rel['type'].endswith('/notesSlide'): notes=texts(E.fromstring(z.read(loc)))
            if rel['type'].endswith('/image'): media.append(dict(path=loc,bytes=len(z.read(loc)),sha256=sha(z.read(loc))))
        for sh in xml.xpath('.//p:spTree/*',namespaces=ns):
            t=texts(sh); xf=sh.find('.//a:xfrm',ns); box=None
            if xf is not None:
                off=xf.find('a:off',ns); ext=xf.find('a:ext',ns)
                if off is not None and ext is not None:
                    box={k:round(int(v)/914400,4) for k,v in {**off.attrib,**ext.attrib}.items()}
            if t: shapes.append(dict(text='\n'.join(t),box_inches=box))
        slides.append(dict(slide=i,xml_path=sp,hidden=xml.get('show')=='0',texts=texts(xml),notes=notes,media=media,shapes=shapes))
(R/'evidence/pptx.json').write_text(json.dumps(dict(size=dict(pres.find('p:sldSz',ns).attrib),slides=slides),ensure_ascii=False,indent=2),encoding='utf8')
(R/'evidence/all_slide_text.txt').write_text('\n\n'.join(f"## Slide {s['slide']}\n"+'\n'.join(s['texts'])+'\nNOTES\n'+'\n'.join(s['notes']) for s in slides),encoding='utf8')
pdf=R/'input/deck/seminar_20261013_v3_1.pdf'; reader=PdfReader(pdf)
(R/'evidence/pdf_text.json').write_text(json.dumps([dict(page=i,text=p.extract_text() or '') for i,p in enumerate(reader.pages,1)],ensure_ascii=False,indent=2),encoding='utf8')
old=json.loads((R.parent/'seminar_recheck_v3_20261013/evidence/pptx.json').read_text(encoding='utf8'))['slides']
diff=[]; summary=[]
for a,b in zip(old,slides):
    before='\n'.join(a['texts']+['NOTES']+a['notes']); after='\n'.join(b['texts']+['NOTES']+b['notes'])
    diff.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=f"v3/{a['slide']}",tofile=f"v3.1/{b['slide']}"))
    summary.append(dict(slide=b['slide'],body_changed=a['texts']!=b['texts'],notes_changed=a['notes']!=b['notes'],media_changed=[m['sha256'] for m in a['media']]!=[m['sha256'] for m in b['media']]))
(R/'evidence/body_notes.diff').write_text(''.join(diff),encoding='utf8')
(R/'evidence/change_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
result=dict(archive=dict(path=str(archive),bytes=archive.stat().st_size,sha256=sha(archive.read_bytes())),inventory=inventory,slides=len(slides),pages=len(reader.pages))
(R/'evidence/input_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='inventory'},ensure_ascii=False,indent=2))
