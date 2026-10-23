import argparse,json,sys,pathlib,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit))
import ul_reader as r, ul_lib as l, ul_gates as g
P=l.load_params();root=out/'clean_resume';root.mkdir(exist_ok=True)
spec={'W':10000,'dt':5e-7,'steps':r._ladder([0.2,0.25,0.3,0.35],[1.2,0.8,0.6,0.4]),'summary':None,'events':[('CROSS',2,'first'),('RM',4,'ncross2')]}
d=pathlib.Path(r._mk_arm(str(root),r.B73,'UT',spec,P));r._fake_restored(str(root),r.B73);r._w(str(root/r.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n')
plain=r.arm_verdict(str(d),r.B73,'UT',P,root=str(root))
rows,_=r._csv(str(d/'ul_steps.csv'),P['records']['steps_cols']);b=rows[1];sr=int(b['step']);kr=int(b['k'])
epath=d/'ul_events.csv';els=epath.read_text().splitlines();els.insert(2,','.join(['RESUME',str(kr),str(sr),b['plate_z'],b['lift'],'state']));epath.write_text('\n'.join(els)+'\n')
r._w(str(d/'restart'/f'state_unload_{sr}.in'),f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\n');(d/'run_manifest.txt').write_text(f'resume_from={sr}\n')
q=subprocess.run([sys.executable,'-I',str(kit/'ul_reader.py'),'arm',str(root),r.B73,'UT'],capture_output=True,text=True)
(out/'clean_resume_cli.log').write_text(q.stdout+q.stderr);rr=r.read_run(str(d),P);vv=json.loads((d/'arm_verdict.json').read_text())
res={'baseline':{k:plain[k] for k in ['primary_status','rho_pct','why']},'resume':{'rc':q.returncode,**{k:vv[k] for k in ['primary_status','rho_pct','why','problems']},'auth':rr['resume_auth'],'n_superseded':rr['n_superseded_rows']}}
atom=d/'dump'/f"atom_{rows[-1]['step']}.dump";bad=out/'bad_box.dump';bad.write_text(atom.read_text().replace('0.0 0.05','nan inf',1));res['g2_bad_box']=g.g2_compare(str(bad),str(atom),expected_step=int(rows[-1]['step']))
(out/'probe.json').write_text(json.dumps(res,indent=2,ensure_ascii=False));print(json.dumps(res,indent=2,ensure_ascii=False))
