"""Independent readback only: no DEM, network solver, scheduler, or source edits."""
from pathlib import Path
import csv,math,json,re,hashlib,zipfile,xml.etree.ElementTree as ET,collections

R=Path(__file__).resolve().parent; S=R/'source'; P=S/'repo'; O=R/'independent';O.mkdir(exist_ok=True)
D=P/'docs/50kg/report_y4'; checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
remote={x['path']:x for x in json.loads((R/'remote_meta.json').read_text()) if x['type']=='file'}
n=0
for f in P.rglob('*'):
 if not f.is_file():continue
 b=f.read_bytes();rel=f.relative_to(P).as_posix();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 check('remote blob '+rel,rel in remote and actual==remote[rel]['sha']);n+=1
for line in (S/'MANIFEST.sha256').read_text().splitlines():
 h,rel=line.split('  ',1);check('manifest '+rel,sha(S/rel)==h)

ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
with zipfile.ZipFile(D/'kg50_report_y4_draft1.pptx') as z:
 slide_text=[];notes=[];media=[]
 for k in range(1,8):
  root=ET.fromstring(z.read(f'ppt/slides/slide{k}.xml'))
  paragraphs=[''.join(p.itertext()) for p in []]
  paragraphs=[''.join(t.text or '' for t in p.findall('.//a:t',ns)) for p in root.findall('.//a:p',ns)]
  slide_text.append('\n'.join(paragraphs))
  note=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{k}.xml'))
  notes.append('\n'.join(''.join(t.text or '' for t in p.findall('.//a:t',ns)) for p in note.findall('.//a:p',ns)))
 for name in z.namelist():
  if name.startswith('ppt/media/'):
   h=hashlib.sha256(z.read(name)).hexdigest();matches=[p.name for p in (D/'figs').glob('*.png') if sha(p)==h]
   media.append({'ppt_member':name,'sha256':h,'source_matches':matches});check('ppt media '+name,len(matches)==1)
 for k,t in enumerate(slide_text,1):(O/f'slide{k}_text.txt').write_text(t,encoding='utf-8')
 for k,t in enumerate(notes,1):(O/f'slide{k}_notes.txt').write_text(t,encoding='utf-8')
save('ppt_media.json',media)
try:
 import fitz
 doc=fitz.open(D/'kg50_report_y4_draft1.pdf')
 for k,page in enumerate(doc,1):
  (O/f'pdf{k}_text.txt').write_text(page.get_text(),encoding='utf-8')
  if k<=2:page.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(O/f'pdf{k}.png')
 check('PDF 7 pages',len(doc)==7)
except ImportError:
 from pypdf import PdfReader
 pages=PdfReader(D/'kg50_report_y4_draft1.pdf').pages
 for k,page in enumerate(pages,1):(O/f'pdf{k}_text.txt').write_text(page.extract_text(),encoding='utf-8')
 check('PDF 7 pages',len(pages)==7)

def deck_commands(text):
 result=[];buf='';start=0
 for line_no,line in enumerate(text.splitlines(),1):
  quote=None;out=[]
  for ch in line:
   if ch=='#' and quote is None:break
   out.append(ch)
   if ch==quote:quote=None
   elif ch in '\"\'' and quote is None:quote=ch
  t=''.join(out).strip()
  if not t:continue
  if not buf:start=line_no
  if t.endswith('&'):buf+=t[:-1]+' ';continue
  result.append((start,' '.join((buf+t).split())));buf=''
 return result
decks={
 'D0.7':P/'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts',
 'D1':P/'docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts',
 'D2':P/'docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/input_kg50_d2_b50.liggghts',
 'D3':P/'docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts'}
vals={};cmds={}
for lab,f in decks.items():
 text=f.read_text(encoding='utf-8'); c=deck_commands(text);cmds[lab]=c
 def variable(name):return float(re.search(r'^variable\s+'+name+r'\s+equal\s+([-+.0-9eE]+)',text,re.M)[1])
 vals[lab]={'r_SE_um':variable('r_SE')*1000,'r_AM_um':variable('r_AM_P')*1000,'dt':variable('dt'),'plate_speed_sim':variable('press_speed'),
  'planned_AM':int(re.search(r'AM \$\{n_am_ins\} / (\d+)',text)[1]),'planned_SE':int(re.search(r'SE \$\{n_se_ins\} / (\d+)',text)[1])}
 check('planned counts '+lab,vals[lab]['planned_AM']==1481 and vals[lab]['planned_SE']=={'D0.7':486810,'D1':166976,'D2':20872,'D3':6184}[lab])
def mask_case(s):return re.sub(r'kg50_d(?:07|1|2|3)_b50(?:_s1)?','CASE',s,flags=re.I)
diffs={}
for lab in ('D0.7','D1','D3'):
 a=cmds['D2'];b=cmds[lab];check('same command count '+lab,len(a)==len(b))
 diffs[lab]=[{'D2_line':i,'candidate_line':j,'D2':s,'candidate':t} for (i,s),(j,t) in zip(a,b) if mask_case(s)!=mask_case(t)]
 check('12 command-pair differences '+lab,len(diffs[lab])==12,len(diffs[lab]))
save('deck_differences.json',diffs);save('deck_values.json',vals)

def parse_atom(path):
 lines=path.read_text().splitlines();step=int(lines[1]);n=int(lines[3]);ix=next(i for i,l in enumerate(lines) if l.startswith('ITEM: ATOMS'))
 cols=lines[ix].split()[2:];rows=[dict(zip(cols,map(float,l.split()))) for l in lines[ix+1:]]
 assert len(rows)==n and len({r['id'] for r in rows})==n
 return step,rows
def parse_thermo(path):
 text=path.read_text(encoding='utf-8');phase=None;blocks=[];active=False;block=None
 for no,line in enumerate(text.splitlines(),1):
  if line.startswith('====== PHASE 3:'):phase='loading'
  elif line.startswith('====== PHASE 4:'):phase='fixed_height_relaxation'
  if phase is None:continue
  words=line.split()
  if words and words[0]=='Step' and 'pressMPa' in words:
   block={'phase':phase,'header':words,'rows':[]};blocks.append(block);active=True;continue
  if line.startswith('Loop time of'):active=False
  if active and len(words)==5 and words[0].isdigit():
   try:block['rows'].append({'line':no,**dict(zip(block['header'],map(float,words)))})
   except ValueError:pass
 return text,blocks

csvrows=list(csv.DictReader((D/'figs/p2_aux_compaction.csv').open(encoding='utf-8',newline='')))
sectionrows=list(csv.DictReader((D/'figs/p1_sections.csv').open(encoding='utf-8',newline='')))
summaries={}; allrecomputed=[]; allsections=[]
for lab in ('D2','D3'):
 end=S/'evidence/end_members'/lab
 atom=next(end.glob('atom_*'));mesh=next(end.glob('mesh_*'))
 step,atoms=parse_atom(atom)
 zvalues=[float(v) for v in re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)',mesh.read_text())]
 check('flat mesh '+lab,len(zvalues)==6 and len(set(zvalues))==1)
 H=zvalues[0]*1000; A=2500
 count=collections.Counter(int(r['type']) for r in atoms)
 vs=math.fsum(4/3*math.pi*(r['radius']*1000)**3 for r in atoms)
 eps=100*(1-vs/(A*H))
 n_am=count[1];n_se=count[3]
 check('actual counts '+lab,n_am=={'D2':1481,'D3':1482}[lab] and n_se=={'D2':20872,'D3':6184}[lab] and len(count)==2)
 check('atom radius matches deck '+lab,all(abs(r['radius']*1000-vals[lab]['r_AM_um' if int(r['type'])==1 else 'r_SE_um'])<1e-12 for r in atoms))
 voutside=0;pen={};massAM=0;massSE=0
 for r in atoms:
  rad=r['radius']*1000;z=r['z']*1000;ty=int(r['type']);vol=4/3*math.pi*rad**3
  if ty==1:massAM+=vol*4.85
  else:massSE+=vol*1.64
  bottom=max(0,rad-z);top=max(0,z+rad-H)
  pen.setdefault(str(ty),{'bottom_um':0,'top_um':0})
  pen[str(ty)]['bottom_um']=max(pen[str(ty)]['bottom_um'],bottom)
  pen[str(ty)]['top_um']=max(pen[str(ty)]['top_um'],top)
  for h in (bottom,top):
   h=min(2*rad,h);voutside+=math.pi*h*h*(rad-h/3)
  dy=(r['y']*1000-25+25)%50-25
  if abs(dy)<rad:
   cr=math.sqrt(rad*rad-dy*dy);x=r['x']*1000
   shifts=[0]+([50] if x-cr<0 else [])+([-50] if x+cr>50 else [])
   for shift in shifts:allsections.append((lab,int(r['id']),'AM' if ty==1 else 'SE',x+shift,z,cr,shift))
 log=P/('docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts' if lab=='D2' else 'docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts')
 text,blocks=parse_thermo(log)
 bload=[b for b in blocks if b['phase']=='loading'];brelax=[b for b in blocks if b['phase']=='fixed_height_relaxation']
 start=int(bload[0]['rows'][0]['Step']);stop=int(bload[-1]['rows'][-1]['Step'])
 cp=[float(v)*1000 for v in re.findall(r'^Current Pressure: (\S+) MPa',text,re.M)]
 check('target stop rule '+lab,len(cp)==len(bload) and all(v<300 for v in cp[:-1]) and cp[-1]>=300,{'count':len(cp),'last_MPa':cp[-1]})
 check('dump first override absent '+lab,not re.search(r'^dump_modify\s+.*\bfirst\s+yes',text,re.M))
 check('no explicit pressure-stop snapshot '+lab,not re.search(r'^write_dump\s',text,re.M))
 z0=float(re.search(r'^====== PLATE HEIGHT: (\S+) ======$',text,re.M)[1])*1000
 rate=vals[lab]['plate_speed_sim']*vals[lab]['dt']*1000
 pred=z0-rate*(stop-start)
 check('end height consistent with rounded mesh '+lab,abs(pred-H)<=0.0005,{'pred':pred,'mesh':H})
 check('all atom counts fixed '+lab,all(int(r['Atoms'])==len(atoms) for b in blocks for r in b['rows']))
 check('contiguous 5000-step compression '+lab,all(int(b['rows'][-1]['Step']-b['rows'][0]['Step'])==5000 for b in bload) and all(bload[i]['rows'][0]['Step']==bload[i-1]['rows'][-1]['Step'] for i in range(1,len(bload))))
 rs=[]
 for b in blocks:
  for r in b['rows'][1:]:
   t=int(r['Step']);h=z0-rate*(t-start) if b['phase']=='loading' else H
   rs.append((lab,b['phase'],t,r['pressMPa']*1000,h,100*(1-vs/(A*h))))
 allrecomputed+=rs
 loadrows=[r for r in rs if r[1]=='loading'];relaxrows=[r for r in rs if r[1]=='fixed_height_relaxation']
 contact0=next(r for r in loadrows if r[3]>0);contact1=next(r for r in loadrows if r[3]>1)
 baseP=loadrows[-1][3];firstP=relaxrows[0][3];lastP=relaxrows[-1][3]
 sums={'counts':dict(count),'step':step,'H_um':H,'pred_H_um':pred,'V_spheres_um3':vs,'eps_sphere_pct':eps,
  'outside_caps_um3':voutside,'outside_caps_eps_pp':100*voutside/(A*H),'wall_penetration':pen,
  'AM_mass_fraction':massAM/(massAM+massSE),'loading_start':start,'stop':stop,'loading_blocks':len(bload),'loading_points':len(loadrows),'relaxation_points':len(relaxrows),
  'P_stop_MPa':baseP,'P_first_relax_MPa':firstP,'P_end_MPa':lastP,'pressure_drop_MPa':baseP-lastP,
  'relax_curve_first_row_covers_fraction_of_drop':(baseP-firstP)/(baseP-lastP),
  'eps_first_positive_pct':contact0[5],'eps_first_gt1_pct':contact1[5],'setup_end_pressure_MPa':brelax[-1]['rows'][0]['pressMPa']*1000,
  'stop_mod_atom50000':stop%50000,'stop_mod_mesh5000':stop%5000,'stop_mod_contact10000':stop%10000,
  'earliest_regular_poststop_atom':(stop//50000+1)*50000,'earliest_regular_poststop_contact':(stop//10000+1)*10000,
  'exact_stop_dump_available_by_registered_schedule':False,
  'fixed_dt_s':vals[lab]['dt'],'relax_duration_sim_s':(step-stop)*vals[lab]['dt'],
  'member_sha':{'atom':sha(atom),'mesh':sha(mesh),'log':sha(log)}}
 summaries[lab]=sums
 check('no final run0 setup in CSV '+lab,not any(r[3]==sums['setup_end_pressure_MPa'] for r in relaxrows))
source={(x['bed'],x['branch'],int(x['step'])):x for x in csvrows}
check('CSV unique keys',len(source)==len(csvrows))
check('CSV exact key sets',set(source)=={x[:3] for x in allrecomputed})
errors=[max(abs(v-float(source[x[:3]][k])) for v,k in zip(x[3:],('plate_pressure_MPa','plate_gap_um','porosity_sphere_pct'))) for x in allrecomputed]
check('all 9310 CSV rows recomputed',len(errors)==9310 and max(errors)<5.01e-7,{'rows':len(errors),'max_abs_error':max(errors)})
ss={(r['bed'],int(r['particle_id']),r['phase'],float(r['periodic_shift_um'])):r for r in sectionrows}
check('section exact keys',set(ss)=={(a,b,c,g) for a,b,c,d,e,f,g in allsections})
errs=[]
for a,b,c,d,e,f,g in allsections:
 row=ss[(a,b,c,g)];errs.extend(abs(v-float(row[k])) for v,k in zip((d,e,f),('x_um','z_um','section_radius_um')))
check('all 1641 section circles',len(allsections)==1641 and max(errs)<5.01e-7,{'rows':len(allsections),'max_abs_error_um':max(errs)})
save('raw_recalculation.json',summaries)
save('core_arithmetic.json',{'ideal_throat_um':6*(2/math.sqrt(3)-1),'break_even_1um':5.1/2.3,'break_even_07um_conditional':5.1/2.25,'gamma_over_mass_ratio_D07_vs_D3':(3/.7)**3,'gamma_over_mass_ratio_D2_vs_D3':(3/2)**3,'note':'The 0.7 um material anchor is conditional; sample identity not validated.'})
save('checks.json',checks)
print(json.dumps({'checks':len(checks),'passed':sum(x['pass'] for x in checks),'failed':[x for x in checks if not x['pass']],'repo_files':n,'raw_recalculation':summaries},ensure_ascii=False,indent=2))
raise SystemExit(any(not x['pass'] for x in checks))
