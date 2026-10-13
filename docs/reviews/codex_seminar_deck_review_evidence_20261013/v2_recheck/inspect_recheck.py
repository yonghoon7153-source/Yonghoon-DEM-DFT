"""Inspect delivered deck and archive without editing originals or running simulations."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile, posixpath, difflib
from lxml import etree as E
from pypdf import PdfReader

R=Path(__file__).resolve().parent
D=Path('C:/Users/Administrator/Downloads')
for sub in ['input','evidence','notes','renders']:(R/sub).mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def rels(z,path):
    return {x.get('Id'):{'target':x.get('Target'),'type':x.get('Type'),'external':x.get('TargetMode')=='External'} for x in E.fromstring(z.read(path))}
def texts(root):return root.xpath('.//a:t/text() | .//m:t/text()',namespaces=ns)
archive=D/'seminar_20261013_v2_codex_recheck.zip';inv=[]
with zipfile.ZipFile(archive) as z:
    assert sum(x.file_size for x in z.infolist())<150_000_000
    names=set()
    for x in z.infolist():
        path=PurePosixPath(x.filename.replace('\\','/'))
        assert not path.is_absolute() and '..' not in path.parts and ':' not in x.filename
        assert (x.external_attr>>16)&0o170000!=0o120000
        if x.is_dir():continue
        assert str(path).casefold() not in names
        names.add(str(path).casefold());b=z.read(x)
        p=R/'input'/Path(*path.parts);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        inv.append({'path':path.as_posix(),'bytes':len(b),'sha256':sha(b)})
originals=[]
for name in ['seminar_20261013_v2_codex_recheck.zip','seminar_20261013_v2.pptx','seminar_20261013_v2.pdf']:
    b=(D/name).read_bytes();originals.append({'name':name,'bytes':len(b),'sha256':sha(b)})
    if name.endswith(('.pptx','.pdf')):assert b==(R/'input'/name).read_bytes()

slides=[]
with zipfile.ZipFile(D/'seminar_20261013_v2.pptx') as z:
    pres=E.fromstring(z.read('ppt/presentation.xml'));pr=rels(z,'ppt/_rels/presentation.xml.rels')
    for i,entry in enumerate(pres.findall('p:sldIdLst/p:sldId',ns),1):
        sp=posixpath.normpath('ppt/'+pr[entry.get('{'+ns['r']+'}id')]['target']);root=E.fromstring(z.read(sp))
        rp=posixpath.dirname(sp)+'/_rels/'+posixpath.basename(sp)+'.rels';sr=rels(z,rp) if rp in z.namelist() else {}
        notes=[];media=[];shapes=[]
        for rel in sr.values():
            if rel['external']:continue
            loc=posixpath.normpath(posixpath.dirname(sp)+'/'+rel['target'])
            if rel['type'].endswith('/notesSlide'):notes=texts(E.fromstring(z.read(loc)))
            if rel['type'].endswith('/image'):media.append({'path':loc,'bytes':len(z.read(loc)),'sha256':sha(z.read(loc))})
        for sh in root.xpath('.//p:spTree/*',namespaces=ns):
            t=texts(sh);xf=sh.find('.//a:xfrm',ns);box=None
            if xf is not None:
                off=xf.find('a:off',ns);ex=xf.find('a:ext',ns)
                if off is not None and ex is not None:box={k:round(int(v)/914400,4) for k,v in {**off.attrib,**ex.attrib}.items()}
            if t:shapes.append({'text':'\n'.join(t),'box_inches':box,'font_sizes_pt':sorted({int(x)/100 for x in sh.xpath('.//a:rPr/@sz | .//a:defRPr/@sz | .//a:endParaRPr/@sz',namespaces=ns)})})
        slides.append({'slide':i,'xml_path':sp,'hidden':root.get('show')=='0','texts':texts(root),'notes':notes,'media':media,'shapes':shapes})
parsed={'size':dict(pres.find('p:sldSz',ns).attrib),'slides':slides}
(R/'evidence/pptx.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2),encoding='utf8')
text='\n\n'.join(f"## Slide {s['slide']}\n"+'\n'.join(s['texts'])+'\nNOTES\n'+'\n'.join(s['notes']) for s in slides)
(R/'evidence/all_slide_text.txt').write_text(text,encoding='utf8')
reader=PdfReader(D/'seminar_20261013_v2.pdf')
pages=[{'page':i,'text':p.extract_text() or ''} for i,p in enumerate(reader.pages,1)]
(R/'evidence/pdf_text.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
oldbase=R.parent/'seminar_review_v3_20261013'
old=json.loads((oldbase/'evidence/v3_pptx.json').read_text(encoding='utf8'))['slides']
changes=[{'slide':n['slide'],'body_changed':n['texts']!=o['texts'],'notes_changed':n['notes']!=o['notes'],
          'media_hashes_changed':[x['sha256'] for x in n['media']]!=[x['sha256'] for x in o['media']]} for n,o in zip(slides,old)]
(R/'evidence/body_notes_changes.diff').write_text(''.join(difflib.unified_diff((oldbase/'evidence/v3_all_slide_text.txt').read_text(encoding='utf8').splitlines(True),text.splitlines(True),fromfile='previous',tofile='revised_v2')),encoding='utf8')
(R/'evidence/input_manifest.json').write_text(json.dumps({'originals':originals,'zip_inventory':inv,'slides':len(slides),'pages':len(pages),'changes':changes},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'originals':originals,'zip_files':len(inv),'slides':len(slides),'pages':len(pages),'changes':changes},ensure_ascii=False,indent=2))
