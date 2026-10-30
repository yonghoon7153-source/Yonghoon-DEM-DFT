from pathlib import Path
import zipfile,xml.etree.ElementTree as E,hashlib,json,re
p=Path(__file__).resolve().parent/'independent/reference_report_20261001_draft.pptx'
b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob=='5b63111b63badde007071a33148022d5ccd6bea4'
n={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
out={'sha256':hashlib.sha256(b).hexdigest(),'git_blob':blob,'matches':[]}
with zipfile.ZipFile(p) as z:
 rels=E.fromstring(z.read('ppt/_rels/presentation.xml.rels'))
 relmap={r.attrib['Id']:r.attrib['Target'] for r in rels}
 prs=E.fromstring(z.read('ppt/presentation.xml'))
 order=['ppt/'+relmap[x.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']] for x in prs.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldId')]
 out['slide_order']=order
 for name in z.namelist():
  if re.match(r'ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml$',name):
   root=E.fromstring(z.read(name));paras=[''.join(t.text or '' for t in q.findall('.//a:t',n)) for q in root.findall('.//a:p',n)]
   hits=[x for x in paras if re.search(r'1\.35|22\s*GPa|입계|탄성계수',x)]
   if hits:out['matches'].append({'part':name,'presentation_page':order.index(name)+1 if name in order else None,'paragraphs':hits})
   if name=='ppt/slides/slide13.xml':out['slide13_text']=paras;out['slide13_image_count']=len(root.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}pic'))
   if name==order[12]:out['actual_page13_text']=paras
Path(__file__).with_name('independent').joinpath('prior_deck_check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
