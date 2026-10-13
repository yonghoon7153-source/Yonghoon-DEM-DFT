"""Read-only archive/deck inspection. Original delivery is never edited."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,posixpath,difflib
from lxml import etree as E
from pypdf import PdfReader
R=Path(__file__).resolve().parent
for sub in ['input','evidence','renders','notes']:(R/sub).mkdir(parents=True,exist_ok=True)
archive=Path('C:/Users/Administrator/Downloads/seminar_20261013_v3_codex_recheck.zip')
sha=lambda b:hashlib.sha256(b).hexdigest()
inv=[]
with zipfile.ZipFile(archive) as z:
    assert sum(x.file_size for x in z.infolist())<200_000_000
    names=set()
    for x in z.infolist():
        p=PurePosixPath(x.filename.replace('\\','/'))
        assert not p.is_absolute() and '..' not in p.parts and ':' not in x.filename
        assert (x.external_attr>>16)&0o170000!=0o120000
        if x.is_dir():continue
        assert str(p).casefold() not in names;names.add(str(p).casefold())
        out=R/'input'/Path(*p.parts);out.parent.mkdir(parents=True,exist_ok=True)
        b=z.read(x);out.write_bytes(b)
        inv.append({'path':p.as_posix(),'bytes':len(b),'sha256':sha(b)})
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def rels(z,path):return {x.get('Id'):{'target':x.get('Target'),'type':x.get('Type'),'external':x.get('TargetMode')=='External'} for x in E.fromstring(z.read(path))}
def texts(root):return root.xpath('.//a:t/text() | .//m:t/text()',namespaces=ns)
slides=[]
with zipfile.ZipFile(R/'input/seminar_20261013_v3.pptx') as z:
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
pdf=R/'input/seminar_20261013_v3.pdf';reader=PdfReader(pdf)
(R/'evidence/pdf_text.json').write_text(json.dumps([{'page':i,'text':p.extract_text() or ''} for i,p in enumerate(reader.pages,1)],ensure_ascii=False,indent=2),encoding='utf8')
oldbase=R.parent/'seminar_recheck_v2_20261013';old=json.loads((oldbase/'evidence/pptx.json').read_text(encoding='utf8'))['slides']
mapping={1:[1],2:[2],3:[3],4:[4],5:[5,6],6:[7,8],7:[9,10],8:[11,12],9:[13],10:[14,15],11:[],12:[],13:[],14:[16],15:[17],16:[18],17:[19]}
diff=[]
for s in slides:
    before='\n'.join('\n'.join(old[j-1]['texts']+old[j-1]['notes']) for j in mapping[s['slide']])
    after='\n'.join(s['texts']+s['notes'])
    diff.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=f'v2/{mapping[s["slide"]]}',tofile=f'v3/{s["slide"]}'))
(R/'evidence/mapped_body_notes.diff').write_text(''.join(diff),encoding='utf8')
result={'archive':{'name':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes())},'inventory':inv,'slides':len(slides),'pages':len(reader.pages),'mapping_v3_to_v2':mapping}
(R/'evidence/input_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ['inventory','mapping_v3_to_v2']},ensure_ascii=False,indent=2))
