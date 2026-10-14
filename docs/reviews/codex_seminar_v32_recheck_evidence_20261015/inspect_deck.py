"""Independent delivered-file inspection; does not execute producer code."""
from pathlib import Path
import hashlib, json, zipfile, posixpath, re, difflib
from lxml import etree as E
from pypdf import PdfReader

R=Path(__file__).resolve().parent
OUT=R/'evidence'; OUT.mkdir(exist_ok=True)
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','mc':'http://schemas.openxmlformats.org/markup-compatibility/2006'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def extract(p):
    slides=[]
    with zipfile.ZipFile(p) as z:
        def rels(path):
            if path not in z.namelist(): return {}
            return {n.get('Id'):dict(target=n.get('Target'),type=n.get('Type'),external=n.get('TargetMode')=='External') for n in E.fromstring(z.read(path))}
        def texts(el): return el.xpath('.//a:t/text() | .//m:t/text()',namespaces=ns)
        pres=E.fromstring(z.read('ppt/presentation.xml')); pr=rels('ppt/_rels/presentation.xml.rels')
        for i,s in enumerate(pres.findall('p:sldIdLst/p:sldId',ns),1):
            path=posixpath.normpath('ppt/'+pr[s.get('{'+ns['r']+'}id')]['target'])
            xml=E.fromstring(z.read(path)); sr=rels(posixpath.dirname(path)+'/_rels/'+posixpath.basename(path)+'.rels')
            notes=[]; media=[]; shapes=[]
            for rel in sr.values():
                if rel['external']: continue
                loc=posixpath.normpath(posixpath.dirname(path)+'/'+rel['target'])
                if rel['type'].endswith('/notesSlide'): notes=texts(E.fromstring(z.read(loc)))
                if rel['type'].endswith('/image'): media.append(dict(path=loc,sha256=sha(z.read(loc)),bytes=len(z.read(loc))))
            for s in xml.xpath('.//p:spTree/*',namespaces=ns):
                t=texts(s)
                if t: shapes.append(dict(text='\n'.join(t),xml=E.tostring(s).decode()))
            eq=[E.tostring(e,method='c14n').decode() for e in xml.xpath('.//m:oMathPara',namespaces=ns)]
            slides.append(dict(slide=i,xml_path=path,texts=texts(xml),notes=notes,media=media,shapes=shapes,equations=eq))
    return {'slides':slides,'size':dict(pres.find('p:sldSz',ns).attrib)}

ppt=R/'input/deck/seminar_20261013_v32.pptx'; pdf=R/'input/deck/seminar_20261013_v32.pdf'
old_path=R/'baseline/seminar_20261013_v3_1.pptx'
if not old_path.exists(): old_path=R.parent/'seminar_closure_v31_20261013/input/deck/seminar_20261013_v3_1.pptx'
obj=extract(ppt); old=extract(old_path)
(OUT/'pptx.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'all_slide_text.txt').write_text('\n\n'.join(f"## Slide {s['slide']}\n"+'\n'.join(s['texts'])+'\nNOTES\n'+'\n'.join(s['notes']) for s in obj['slides']),encoding='utf8')
reader=PdfReader(pdf)
(OUT/'pdf_text.json').write_text(json.dumps([{'page':i,'text':p.extract_text()} for i,p in enumerate(reader.pages,1)],ensure_ascii=False,indent=2),encoding='utf8')
mapping={1:1,2:2,4:5,5:6,6:7,7:3,8:4,9:8,10:9,12:11,13:12,14:13,15:14,16:15,17:16,18:17}
diff=[]; changes=[]
for newnum,oldnum in mapping.items():
    a=old['slides'][oldnum-1]; b=obj['slides'][newnum-1]
    diff+=list(difflib.unified_diff(('\n'.join(a['texts']+['NOTES']+a['notes'])+'\n').splitlines(True),('\n'.join(b['texts']+['NOTES']+b['notes'])+'\n').splitlines(True),fromfile=f'v3.1/{oldnum}',tofile=f'v3.2/{newnum}'))
    changes.append({'new':newnum,'old':oldnum,'body_same':a['texts']==b['texts'],'notes_same':a['notes']==b['notes'],'media_same':sorted(m['sha256'] for m in a['media'])==sorted(m['sha256'] for m in b['media'])})
(OUT/'body_notes.diff').write_text(''.join(diff),encoding='utf8')
(OUT/'change_summary.json').write_text(json.dumps(changes,indent=2),encoding='utf8')
manifest=[]
for line in (R/'input/MANIFEST.sha256').read_text(encoding='utf8').splitlines():
    if not line.strip(): continue
    expected,name=line.split(None,1); path=R/'input'/name.strip().removeprefix('./')
    manifest.append({'path':name,'exists':path.exists(),'match':path.exists() and sha(path.read_bytes())==expected})
filehashes={}
for p in [ppt,pdf,Path('C:/Users/Administrator/Downloads/seminar_20261013_v32.pptx'),Path('C:/Users/Administrator/Downloads/seminar_20261013_v32.pdf'),Path('C:/Users/Administrator/Downloads/codex_seminar_deck_v3_2_recheck_20261014.zip')]:
    if not p.exists(): continue
    filehashes[str(p)]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
refs=[]
for s in obj['slides']:
    if s['slide']==17: continue
    for kind in ('texts','notes'):
        for t in s[kind]:
            for match in re.findall(r'\[([0-9]+(?:\s*,\s*[0-9]+)*)\]',t):
                refs.extend({'slide':s['slide'],'kind':kind,'ref':int(n)} for n in re.findall(r'\d+',match))
eq_escapes=[{'slide':s['slide'],'text':t} for s in obj['slides'] for t in s['texts'] if '\\u' in t]
checks={'hashes':filehashes,'slides':len(obj['slides']),'pdf_pages':len(reader.pages),'manifest':manifest,'reference_uses':refs,'reference_ids':sorted(set(x['ref'] for x in refs)),'literal_unicode_escapes':eq_escapes}
(OUT/'independent_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'slides':len(obj['slides']),'pages':len(reader.pages),'manifest_total':len(manifest),'manifest_bad':[x for x in manifest if not x['match']],'literal_escapes':eq_escapes,'references':checks['reference_ids']},ensure_ascii=False,indent=2))
