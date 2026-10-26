"""Independent T12 scope probes; finite synthetic frames, no physical simulation."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,importlib,itertools
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False);S=O/'source';S.mkdir()
PIN='4c29705fa1c4ba94737a858b206fa4f4c5bb2bde';R=Path(__file__).resolve().parent;M=json.loads((R/'snapshot/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/source-manifest.json').read_text(encoding='utf8'))
for name,h in M['files_sha256'].items():
 b=subprocess.run(['git','-C',str(a.repo),'show',PIN+':docs/data/ps45_unload_20261009/'+name],capture_output=True,check=True).stdout;assert hashlib.sha256(b).hexdigest()==h;(S/name).write_bytes(b)
sys.dont_write_bytecode=True;sys.path.insert(0,str(S));import ul_reader as r,ul_gates as g,ul_lib as lib,ul_s3 as s3
P=lib.load_params();bed='ps_7_3_r45';step=P['beds'][bed]['s0'];cols=['id','type','x','y','z','radius','mass','vx','vy','vz','omegax','omegay','omegaz','fx','fy','fz'];assert list(r.ATOM_COLS)==cols
atom=dict(zip(cols,[1,1,.01,.01,.1,.001,1e-6,0,0,0,0,0,0,0,0,1e-10]));results=[]
def dump(label,rows,columns=cols,ts=step,local=False,box_top=.2):
 p=O/(label+'.dump');kind='ENTRIES' if local else 'ATOMS';p.write_text(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF {kind}\n{len(rows)}\nITEM: BOX BOUNDS pp pp ff\n0 .05\n0 .05\n0 {box_top}\nITEM: {kind} '+ ' '.join(columns)+'\n'+''.join(' '.join(str(x[c]) for c in columns)+'\n' for x in rows),encoding='utf8');return str(p)
def check(name,actual,expected,classification='scope_boundary',detail=None):
 results.append(dict(name=name,actual=actual,expected=expected,pass_=actual==expected,classification=classification,detail=detail))
base=dump('base',[atom]);second={**atom,'id':2,'type':2,'x':.02};two=dump('two',[atom,second])
for label,change,expect in [('mass_x2',{'mass':2e-6},'PASS'),('omega_7',{'omegaz':7},'PASS'),('type2',{'type':2},'FAIL'),('x_shift',{'x':.011},'FAIL'),('mass_nan',{'mass':'nan'},'FAIL'),('radius_negative',{'radius':-.001},'FAIL')]:
 path=dump(label,[{**atom,**change}]);v=g.g2_compare(path,base,expected_step=step);check('g2_'+label,v['status'],expect,detail=v)
check('g2_changed_box',g.g2_compare(dump('box_changed',[atom],box_top=.4),base,expected_step=step)['status'],'PASS')
check('g2_missing_atom',g.g2_compare(base,two,expected_step=step)['status'],'FAIL')
check('g2_wrong_step',g.g2_compare(dump('wrongstep',[atom],ts=step+1),base,expected_step=step)['status'],'FAIL')
for label,rows,expect in [('subset',[atom],True),('empty',[],True),('mass0',[{**atom,'mass':0}],True),('newid',[{**atom,'id':3}],False),('negative_id',[{**atom,'id':-1}],False),('duplicate',[atom,atom],False),('mass_nan',[{**atom,'mass':'nan'}],False)]:
 v,pr=r._atom_frame(dump('af_'+label,rows),step,{1,2});check('atom_'+label,v is not None,expect,detail=pr)
C=[f'c_cpl[{i}]' for i in range(1,27)];contact={c:0 for c in C};contact.update({'c_cpl[7]':1,'c_cpl[8]':2,'c_cpl[10]':.01,'c_cpl[16]':.003,'c_cpl[22]':.0001,'c_cpl[23]':.002});orig=dump('contact_base',[contact],C,local=True)
for label,ch,exp in [('force10',{'c_cpl[10]':.02},'FAIL'),('delta23',{'c_cpl[23]':.003},'FAIL'),('torque19',{'c_cpl[19]':1},'PASS'),('periodic9',{'c_cpl[9]':1},'PASS')]:
 v=g.g2c_compare(dump('contact_'+label,[{**contact,**ch}],C,local=True),orig,expected_step=step);check('g2c_'+label,v['status'],exp,detail=v)
empty=dump('empty_contact',[],C,local=True);v=g.g2c_compare(empty,empty,expected_step=step);check('g2c_empty_both',v['status'],'PASS',detail=v)
missing=dump('missing_contact_column',[contact],C[:-1],local=True);check('g2c_missing_column',g.g2c_compare(missing,orig,expected_step=step)['status'],'NOT_COMPUTED')
h={**atom,**{f'f_history_zwall_bot[{i}]':v for i,v in enumerate([.002,0,0,0],1)}}
check('history_equal',r._hist_equal([h],[h]),True)
check('history_delta_change',r._hist_equal([h],[{**h,'f_history_zwall_bot[1]':.003}]),False)
check('history_reordered',r._hist_equal([h,{**h,'id':2}],[{**h,'id':2},h]),True)
check('history_missing_field',r._hist_equal([h],[{k:v for k,v in h.items() if k!='f_history_zwall_bot[1]'}]),False)
# Validate non-finite data on the actual parsing path, not by bypassing preconditions of _hist_equal.
hcols=cols+list(k for k in h if k.startswith('f_history'))
check('history_nan_parser',lib.read_dump(dump('hist_nan',[{**h,'f_history_zwall_bot[1]':'nan'}],hcols),'custom')['ok'],False)
for job in ['UB','G_UB']:
 actual=s3.s3_residual([atom],[],{1},.2,atom_step=step,contact_step=step,g=r._arm_g(job,P));check('gravity_'+job,actual['status'],'PASS' if job=='UB' else 'FAIL',detail=actual)
for job in ['UB','UT','G_UT','UTc']:
 w=r._arm_wsteps(str(O/'no_deck'),job,P);arm=job[2:] if job.startswith('G_') else 'UT3' if job=='UTc' else job;T=w*P['protocol']['dt0']*P['arms'][arm]['dt_factor'];check('window_'+job,T,.005,detail={'W':w,'dt_factor':P['arms'][arm]['dt_factor']})
check('known_rj_no_files',r.gate(str(O/'missing'),bed,'RJ',P)[0],True)
check('unknown_rj_no_files',r.gate(str(O/'missing'),'P2_unregistered','RJ',P)[0],False)
# Complete 3^6 truth table; model order encoded independently from the documented priority.
truth=[]
for q in itertools.product([True,False,None],repeat=6):
 reset,g0,syntax,equal,history,erased=q
 expected='SYNTAX_FAIL' if syntax is not True else 'VALUE_MISMATCH' if reset is not True or g0 is not True or equal is False else 'UNCONFIRMED' if equal is not True or history is not True or erased is not True else 'RESTORED'
 actual=g.restoration_verdict(*q);truth.append({'input':q,'actual':actual,'expected':expected,'pass':actual==expected})
(O/'restore_truth_table.json').write_text(json.dumps(truth,indent=2),encoding='utf8')
allfiles=sorted(p for p in O.glob('*.dump'));hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in allfiles}
output={'pin':PIN,'cases':results,'passed':sum(x['pass_'] for x in results),'count':len(results),'truth_table':{'count':len(truth),'passed':sum(x['pass'] for x in truth)},'input_hashes':hashes}
(O/'result.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8');print({k:output[k] for k in ['count','passed','truth_table']});print([x for x in results if not x['pass_']]);assert all(x['pass_'] for x in results) and all(x['pass'] for x in truth)
