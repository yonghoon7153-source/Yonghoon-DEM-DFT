"""Independent Part-B controls; no submitted fixture or tests imported.

Uses two equal spheres, whose intersection disk has exact analytic area
pi * (r**2 - (d/2)**2). Does not execute DEM/MPM or production cohorts.
"""
from pathlib import Path
import argparse, contextlib, gzip, hashlib, importlib.util, io, json, math, sys, warnings
from run_review import ROOT, HERE, OLD, prep

ap=argparse.ArgumentParser()
ap.add_argument('--source',default=str(ROOT/'source'))
a=ap.parse_args()
SRC=Path(a.source).resolve()
prep(SRC)
import numpy as np
import rint_iface_join as J
import step3_sigma as S
spec=importlib.util.spec_from_file_location('old_join',OLD/'scripts/rint_iface_join.py')
O=importlib.util.module_from_spec(spec); spec.loader.exec_module(O)
TMP=HERE/'tmp/independent'; TMP.mkdir(parents=True,exist_ok=True)
OUT=HERE/'evidence'; OUT.mkdir(exist_ok=True)
TM={1:'AM_P',2:'SE'}

def fixture():
    centers=((.002,.002,.002),(.0035,.002,.002))
    r=.001; d=.0015
    box=['ITEM: BOX BOUNDS ff ff ff','0 0.01','0 0.01','0 0.01']
    atom=['ITEM: TIMESTEP','100','ITEM: NUMBER OF ATOMS','2']+box+['ITEM: ATOMS id type x y z radius']
    atom += [str(i+1)+' 1 '+' '.join('%g'%x for x in (*c,r)) for i,c in enumerate(centers)]
    ct=['ITEM: TIMESTEP','100','ITEM: NUMBER OF ENTRIES','1']+box+['ITEM: ENTRIES '+' '.join('c_cpl[%d]'%i for i in range(1,24))]
    vals=[*centers[0],*centers[1],1,2,0]+[0]*12+[math.pi*(r*r-d*d/4),2*r-d]
    ct+=[' '.join('%g'%v for v in vals)]
    sc=[','.join(['1',*(f'{v:.12f}' for v in (*c,r))]) for c in centers]
    return [sc,atom,ct]

def save(tag,lines,storage='lf'):
    paths=[]
    for idx,(s,ls) in enumerate(zip(('sc.csv','atom.dump','contact.dump'),lines)):
        end='\r' if storage=='cr' else '\r\n' if storage=='crlf' else '\n'
        data=(end.join(ls)+end).encode('utf8')
        if storage=='gz2':
            mid=len(data)//2
            data=gzip.compress(data[:mid],mtime=0)+gzip.compress(data[mid:],mtime=0)
        elif storage=='gz': data=gzip.compress(data,mtime=0)
        p=TMP/(tag+'_'+s+('.gz' if storage.startswith('gz') else ''))
        p.write_bytes(data);paths.append(p)
    return paths

normal=J.am_iface_join(*save('normal',fixture()),type_map=TM)
c,r,t=(normal['particles'][k] for k in ('c_um','r_um','t'))
with contextlib.redirect_stdout(io.StringIO()):
    sid,_=S.rasterize(c,r,t,None,None,(0,0,0),(7,4,4),.25,bridge_um=.24)
ledger=S.am_iface_ledger(c,r,t,sid,sid,(0,0,0),.25,delta_bound_um=normal['g_geo']['delta_bound_um'],bridge_um=.24)

def compact(j):
    out={'status':j['status'],'codes':[q['code'] for q in j['rejections']],
         'claim':j['scaffold_frame_claim'],'version':j['version'],
         'particles_equal':all(np.array_equal(j['particles'][k],normal['particles'][k]) for k in ('c_um','r_um','t'))}
    p=S.am_iface_plan(ledger,{'AM_P|AM_P':.001},join=j,gap_law='cut',unreg_law='cut',ambiguous_arm='cut')
    out['plan_codes']=[q['code'] for q in p['rejections']]
    try:
        S.iface_require_quantitative(p,sid=sid,vox=.25)
        out['consumer']='ACCEPT'
    except Exception as e: out['consumer']=type(e).__name__+': '+str(e)
    return out

rows=[]
def check(tag,edit=None,storage='lf',expect='REJECT',known=False):
    lines=fixture()
    if edit: edit(lines)
    paths=save(tag,lines,storage)
    row={'case':tag,'expected':expect,'known_residual':known,'storage':storage,
         'input_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]}
    for label,mod in [('current',J),('old',O)]:
        try:
            with warnings.catch_warnings(record=True) as ws:
                j=mod.am_iface_join(*paths,type_map=TM)
            row[label]=compact(j)
            row[label]['warnings']=[str(w.message) for w in ws]
        except Exception as e: row[label]={'exception':type(e).__name__+': '+str(e)}
    row['expected_matched']=row['current'].get('status')==expect
    rows.append(row)

for storage in ('lf','cr','crlf','gz','gz2'): check('normal_'+storage,storage=storage,expect='PASS')
for fi,name in ((1,'atom'),(2,'contact')):
    for char in (' ','\t','  \t  '):
        def ed(ls,fi=fi,char=char):
            ls[fi]=[x.replace(' ',char) if i>=9 else x for i,x in enumerate(ls[fi])]
        check(name+'_whitespace_'+str(len(rows)),ed,expect='PASS')
    for char in ('\u00a0','\u3000','\x1f','\v','\f','\x85','\u2028','\u2029'):
        def ed(ls,fi=fi,char=char): ls[fi][9]=ls[fi][9].replace(' ',char,1)
        check(name+'_lexical_'+hex(ord(char)),ed)
    for char in ('\u00a0','\u3000','\x1f'):
        def ed(ls,fi=fi,char=char): ls[fi][8]=ls[fi][8].replace(' id',char+'id',1) if fi==1 else ls[fi][8].replace(' c_',char+'c_',1)
        check(name+'_head_boundary_'+hex(ord(char)),ed)
    def extra(ls,fi=fi):
        ls[fi][8]+=' diagnostic'
        for i in range(9,len(ls[fi])): ls[fi][i]+=' garbage'
    check(name+'_optional_garbage',extra,expect='PASS')

for tok in ('１００','١٠٠','100١','1e6','100x','100_000','100.0','100²'):
    def ed(ls,tok=tok): ls[0].insert(0,'# step '+tok)
    check('step_reject_'+str(len(rows)),ed)
for comment in ('# step 100.','# step 100,','# timestep 100','# compacted at step 100.','# laststep 100'):
    check('step_positive_'+str(len(rows)),lambda ls,comment=comment:ls[0].insert(0,comment),expect='PASS')
for token in ('100-5','100/2','100+5','100..5','100\u200b5','100\u0301','100\u066b5','100\u00a05'):
    check('known_F1_'+str(len(rows)),lambda ls,token=token:ls[0].insert(0,'# step '+token),expect='PASS',known=True)
# Declared integer support includes signed/zero-padded values, preserving value.
for tok in ('+100','000100','-0'):
    def ed(ls,tok=tok): ls[1][1]=ls[2][1]=tok
    check('integer_positive_'+str(len(rows)),ed,expect='PASS')
# Other comments must not silently become a timestamp claim.
for cmt in ('# laststep 100','# my_timestep 100','# step-size 100'):
    check('nondeclaration_'+str(len(rows)),lambda ls,cmt=cmt:ls[0].insert(0,cmt),expect='PASS')

real=[]
for name,sc,at,ct,tm in [
    ('real14','real14_am_scaffold.csv','real14_reference_20260928/atom_2060000.liggghts.gz','real14_reference_20260928/contact_2060000.liggghts.gz',{1:'AM_P',2:'AM_S',3:'SE'}),
    ('case15','case15_corner_20261001/case15_am_scaffold.csv','case15_corner_20261001/atom_v4_1710000.liggghts.gz','case15_corner_20261001/contact_v4_1710000.liggghts.gz',{1:'AM_P',2:'SE'})]:
    paths=[SRC/'docs/data'/p for p in (sc,at,ct)]
    new=J.am_iface_join(*paths,type_map=tm); old=O.am_iface_join(*paths,type_map=tm)
    equal={}
    for key in ('particles','dem_am_am'):
        for sub in old[key]: equal[key+'.'+sub]=np.array_equal(new[key][sub],old[key][sub])
    equal['atom_id_of_row']=np.array_equal(new['atom_id_of_row'],old['atom_id_of_row'])
    equal['delta_bound_um']=new['g_geo']['delta_bound_um']==old['g_geo']['delta_bound_um']
    real.append({'name':name,'status':new['status'],'old_status':old['status'],'counts':{k:new['g_geo'][k] for k in ('n_scaffold','n_dump_am','n_matched','n_dem_am_am')},'equal':equal,
                 'input_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]})
out={'source':str(SRC),'current_join_sha256':hashlib.sha256((SRC/'scripts/rint_iface_join.py').read_bytes()).hexdigest(),
     'old_join_sha256':hashlib.sha256((OLD/'scripts/rint_iface_join.py').read_bytes()).hexdigest(),'cases':rows,'real':real,
     'summary':{'n':len(rows),'unexpected':[r['case'] for r in rows if not r['expected_matched']],
                'new_pass':sum(r['current'].get('status')=='PASS' for r in rows),'new_reject':sum(r['current'].get('status')=='REJECT' for r in rows)}}
(OUT/'independent_join_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'summary':out['summary'],'real':real},ensure_ascii=False,indent=2))
