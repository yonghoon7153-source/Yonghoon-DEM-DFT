"""Read-only seminar equation inspection. Never opens/runs the producer builder."""
from pathlib import Path
import hashlib, json, zipfile, posixpath, sys
sys.stdout.reconfigure(encoding='utf-8')
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'input/deck/seminar_20261013_v32.pptx'
NS = {
    'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'mc':'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
sha = lambda b: hashlib.sha256(b).hexdigest()

def inspect(path, page=3):
    with zipfile.ZipFile(path) as z:
        pres = E.fromstring(z.read('ppt/presentation.xml'))
        rels = E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
        rm = {e.get('Id'): e.get('Target') for e in rels}
        sid = pres.findall('p:sldIdLst/p:sldId', NS)[page-1]
        part = posixpath.normpath(posixpath.join('ppt', rm[sid.get('{'+NS['r']+'}id')])).lstrip('/')
        root = E.fromstring(z.read(part))
        pr = posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part)+'.rels')
        sr = {e.get('Id'):e.get('Target') for e in E.fromstring(z.read(pr))}
        out = {'path':str(path),'sha256':sha(path.read_bytes()), 'page':page,'part':part,'equations':[]}
        for ac in root.xpath('//mc:AlternateContent', namespaces=NS):
            maths = ac.xpath('.//m:oMathPara', namespaces=NS)
            if not maths: continue
            names=ac.xpath('.//p:cNvPr/@name',namespaces=NS)
            brefs=ac.xpath('./mc:Fallback//a:blip/@r:embed',namespaces=NS)
            out['equations'].append({
                'names':names,
                'tokens':maths[0].xpath('.//m:t/text()',namespaces=NS),
                'spacing_tokens_codepoints':[[ord(c) for c in t] for t in maths[0].xpath('.//m:t/text()',namespaces=NS) if chr(0x2003) in t or '2003' in t],
                'omml_c14n_sha256':sha(E.tostring(maths[0],method='c14n')),
                'omml_xml':E.tostring(maths[0],encoding='unicode'),
                'fallback_sha256':[sha(z.read(posixpath.normpath(posixpath.join(posixpath.dirname(part),sr[r])))) for r in brefs],
            })
        out['normal_text']=root.xpath('//a:t/text()',namespaces=NS)
        note=[t for t in sr.values() if 'notesSlides' in t]
        out['notes']=[]
        for n in note:
            rr=E.fromstring(z.read(posixpath.normpath(posixpath.join(posixpath.dirname(part),n))))
            out['notes'].extend(rr.xpath('//a:t/text()',namespaces=NS))
        return out

out=inspect(DECK)
out['available_originals']=[]
for f in Path('C:/Users/Administrator/Downloads').glob('DEM_Equations*.pptx'):
    item={'path':str(f),'sha256':sha(f.read_bytes())}
    try:
        with zipfile.ZipFile(f) as z:
            n=len(E.fromstring(z.read('ppt/presentation.xml')).findall('p:sldIdLst/p:sldId',NS))
        qq=[inspect(f,page=i+1) for i in range(n)]
        item['pages']=[{'page':q['page'],'equation_count':len(q['equations']),
          'math_token_matches':[a['tokens']==b['tokens'] for a,b in zip(out['equations'],q['equations'])],
          'fallback_matches':[a['fallback_sha256']==b['fallback_sha256'] for a,b in zip(out['equations'],q['equations'])]} for q in qq if q['equations']]
    except Exception as exc: item['inspection_error']=str(exc)
    out['available_originals'].append(item)
out['torque_lever_counterexample']={
    'R_um':0.5,'overlap_um':0.1,'Ft_uN':1.0,
    'source_c_r_um':0.5-0.1/2,
    'slide_torque_uN_um':0.5,'source_torque_uN_um':0.45,
    'relative_excess':0.5/0.45-1,
}
dest=ROOT/'agents/equations_probe.json'
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ('normal_text','notes','equations')},ensure_ascii=False,indent=2))
for e in out['equations']:
    print(e['names'],e['tokens'],e['omml_c14n_sha256'])
print('NOTES',out['notes'])
