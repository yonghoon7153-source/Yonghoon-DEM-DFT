"""Replay original LW counterexamples plus parser-to-contract missingness test."""
from pathlib import Path
import sys, json, math, tempfile, copy
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence'
sys.path.insert(0,str(S/'scripts'))
from dem_analysis_core import calc_love_weber_stress as lw
from analyze_contacts import load_atoms_raw
V=4*math.pi/3; TM={1:'AM_P',2:'SE'}
def atom(t,x,z,f):
 return dict(type=t,x=x,y=2.,z=z,radius=1.,sigma_xx=0.,sigma_yy=0.,sigma_zz=-.9*f/V)
def contact(i,j,x,z,f):
 return dict(id1=i,id2=j,fx=0.,fy=0.,fz=-f,fn_x=0.,fn_y=0.,fn_z=-f,ft_x=0.,ft_y=0.,ft_z=0.,cp_x=x,cp_y=2.,cp_z=z)
def compact(x):
 return {k:x.get(k) for k in ('status','vm_cv','type_stress','checks','nowall_status','contract')}
if __name__=='__main__':
 a={1:atom(1,2.,2.,1.),2:atom(1,2.,3.8,1.)}; c=[contact(1,2,2.,2.9,1.)]
 results={}
 def run(name,aa=None,cc=None,**kw):
  results[name]=compact(lw(aa if aa is not None else a,cc if cc is not None else c,TM,kw.pop('plate',20.),**kw))
 run('normal');run('nan_plate',plate=float('nan'))
 bad=copy.deepcopy(a);bad[3]=dict(type=2,x=7.,y=2.,z=5.,radius=float('nan'))
 run('isolated_nan_radius',bad)
 zero={1:atom(1,2.,2.,0.),2:atom(1,2.,3.8,0.)};cz=[contact(1,2,2.,2.9,0.)]
 run('true_zero_load',zero,cz)
 czbad=copy.deepcopy(cz);czbad[0]['fn_z']=-1.
 run('false_zero_force',zero,czbad)
 aa={**a,3:atom(2,7.,2.,3.),4:atom(2,7.,3.8,3.)}
 run('two_dimers_correct',aa,[c[0],contact(3,4,7.,2.9,3.)])
 run('two_dimers_swapped',aa,[contact(1,2,2.,2.9,3.),contact(3,4,7.,2.9,1.)])
 d=Path(tempfile.mkdtemp(prefix='lw_parser_',dir=E))
 for name,first,zz in [('finite_cstr','0',-.9),('nan_cstr_first','nan',-.9),('text_cstr_first','invalid',-.9),('inf_cstr_first','inf',-.9),
                       ('finite_wrong_virial','0',-2.7),('nan_hides_wrong_virial','nan',-2.7)]:
  csv='id,type,x,y,z,radius,c_strs[1],c_strs[2],c_strs[3]\n'+''.join(f'{i},1,2,2,{z},1,{first},0,{zz}\n' for i,z in [(1,2.),(2,3.8)])
  p=d/(name+'.csv');p.write_text(csv,encoding='utf8');parsed,_=load_atoms_raw(p)
  run(name,parsed);results[name]['parsed_cstr_present']=[all(k in x for k in ('sigma_xx','sigma_yy','sigma_zz')) for x in parsed.values()]
 for name,first in [('all_cstr_absent',None),('partial_cstr_tuple',True)]:
  aa=copy.deepcopy(a)
  for x in aa.values():
   for k in (('sigma_xx','sigma_yy','sigma_zz') if first is None else ('sigma_xx',)):x.pop(k)
  run(name,aa)
 assert results['normal']['status']=='OK'
 assert results['nan_plate']['status'].startswith('FAILED')
 assert results['isolated_nan_radius']['status'].startswith('FAILED')
 assert results['true_zero_load']['status'].startswith('UNDEFINED')
 assert results['false_zero_force']['status'].startswith('FAILED')
 assert results['nan_cstr_first']['status']=='OK' and results['nan_cstr_first']['parsed_cstr_present']==[False,False]
 assert results['inf_cstr_first']['status'].startswith('FAILED')
 assert results['finite_wrong_virial']['status'].startswith('FAILED') and results['nan_hides_wrong_virial']['status']=='OK'
 (E/'lw_replay.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(results,ensure_ascii=False,indent=2))
