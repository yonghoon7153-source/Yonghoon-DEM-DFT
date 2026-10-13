from pathlib import Path,PurePosixPath
import hashlib,json,posixpath,zipfile,difflib,re
from lxml import etree as E
from pypdf import PdfReader
R=Path(__file__).resolve().parent; D=Path('C:/Users/Administrator/Downloads')
for n in ['evidence','notes','renders']:(R/n).mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
def rels(z,path):return {x.get('Id'):{'target':x.get('Target'),'type':x.get('Type'),'external':x.get('TargetMode')=='External'} for x in E.fromstring(z.read(path))}
def texts(root):return root.xpath('.//a:t/text() | .//m:t/text()',namespaces=ns)
def parseppt(p):
    slides=[]
    with zipfile.ZipFile(p) as z:
        pres=E.fromstring(z.read('ppt/presentation.xml'));pr=rels(z,'ppt/_rels/presentation.xml.rels')
        for i,entry in enumerate(pres.findall('p:sldIdLst/p:sldId',ns),1):
            sp=posixpath.normpath('ppt/'+pr[entry.get('{'+ns['r']+'}id')]['target']);root=E.fromstring(z.read(sp))
            rp=posixpath.dirname(sp)+'/_rels/'+posixpath.basename(sp)+'.rels'; sr=rels(z,rp) if rp in z.namelist() else {}
            notes=[];media=[];shapes=[]
            for rel in sr.values():
                if rel['external']:continue
                loc=posixpath.normpath(posixpath.dirname(sp)+'/'+rel['target'])
                if rel['type'].endswith('/notesSlide'):notes=texts(E.fromstring(z.read(loc)))
                if rel['type'].endswith('/image'):media.append({'path':loc,'bytes':len(z.read(loc)),'sha256':sha(z.read(loc))})
            for sh in root.xpath('.//p:spTree/*',namespaces=ns):
                t=texts(sh); xf=sh.find('.//a:xfrm',ns);box=None
                if xf is not None:
                    off=xf.find('a:off',ns);ex=xf.find('a:ext',ns)
                    if off is not None and ex is not None:box={k:round(int(v)/914400,4) for k,v in {**off.attrib,**ex.attrib}.items()}
                if t:shapes.append({'text':'\n'.join(t),'box_inches':box,'font_sizes_pt':sorted({int(x)/100 for x in sh.xpath('.//a:rPr/@sz | .//a:defRPr/@sz | .//a:endParaRPr/@sz',namespaces=ns)})})
            slides.append({'slide':i,'xml_path':sp,'hidden':root.get('show')=='0','texts':texts(root),'notes':notes,'media':media,'shapes':shapes})
    return {'size':dict(pres.find('p:sldSz',ns).attrib),'slides':slides}
inventories={}; parsed={};manifest=[]
for ver in ['v2','v3']:
    name=f'seminar_20261013_codex_review_{ver}.zip';f=D/name;manifest.append({'name':name,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())})
    dest=R/ver; inv=[]
    with zipfile.ZipFile(f) as z:
        assert sum(x.file_size for x in z.infolist())<150_000_000
        for x in z.infolist():
            p=PurePosixPath(x.filename.replace('\\','/'));assert not p.is_absolute() and '..' not in p.parts and ':' not in x.filename
            assert (x.external_attr>>16)&0o170000!=0o120000
            if x.is_dir():continue
            b=z.read(x);out=dest/Path(*p.parts);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
            inv.append({'path':p.as_posix(),'bytes':len(b),'sha256':sha(b)})
    inventories[ver]=inv
    ppt=list(dest.rglob('*.pptx'));pdf=list(dest.rglob('*.pdf'));assert len(ppt)==len(pdf)==1
    parsed[ver]=parseppt(ppt[0]); (R/f'evidence/{ver}_pptx.json').write_text(json.dumps(parsed[ver],ensure_ascii=False,indent=2),encoding='utf8')
    slides=parsed[ver]['slides'];(R/f'evidence/{ver}_all_slide_text.txt').write_text('\n\n'.join(f"## Slide {s['slide']}\n"+'\n'.join(s['texts'])+'\nNOTES\n'+'\n'.join(s['notes']) for s in slides),encoding='utf8')
    p=PdfReader(pdf[0]);pages=[{'page':i,'text':x.extract_text() or ''} for i,x in enumerate(p.pages,1)]
    (R/f'evidence/{ver}_pdf_text.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
    print(ver,'files',len(inv),'slides',len(slides),'pages',len(pages),'PPTX',ppt[0].relative_to(R),'PDF',pdf[0].relative_to(R))
    print('\n'.join(x['path'] for x in inv))
request=D/'codex_seminar_deck_review_request_20261013.md';b=request.read_bytes();(R/'evidence/external_request.md').write_bytes(b);manifest.append({'name':request.name,'bytes':len(b),'sha256':sha(b)})
a={x['path']:x['sha256'] for x in inventories['v2']};b={x['path']:x['sha256'] for x in inventories['v3']}
diff={'changed':[p for p in a.keys()&b.keys() if a[p]!=b[p]],'v2_only':list(a.keys()-b.keys()),'v3_only':list(b.keys()-a.keys())}
old=json.loads((R.parent/'seminar_review_20261013/evidence/pptx_slides.json').read_text(encoding='utf8'))
diff['slides_old_to_v3']=[{'slide':x['slide'],'body':x['texts']!=y['texts'],'notes':x['notes']!=y['notes'],'image_bytes_changed':[m['sha256'] for m in x['media']]!=[m['sha256'] for m in y['media']]} for x,y in zip(old,parsed['v3']['slides'])]
(R/'evidence/input_manifest.json').write_text(json.dumps({'originals':manifest,'inventory':inventories,'versions':diff},ensure_ascii=False,indent=2),encoding='utf8')
(R/'evidence/old_to_v3_text.diff').write_text(''.join(difflib.unified_diff((R.parent/'seminar_review_20261013/evidence/all_slide_text.txt').read_text(encoding='utf8').splitlines(True),(R/'evidence/v3_all_slide_text.txt').read_text(encoding='utf8').splitlines(True),fromfile='previous',tofile='v3')),encoding='utf8')
print('DIFF',json.dumps(diff,ensure_ascii=False))
