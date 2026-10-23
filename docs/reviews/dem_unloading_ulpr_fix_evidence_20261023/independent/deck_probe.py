import argparse,pathlib,sys,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit))
import ul_reader as r,ul_lib as l,make_unload_decks as mk
P=l.load_params();result=[]
for kr in range(4):
 root=out/f'k{kr}';root.mkdir(exist_ok=True);d,tr=r._ut_trace_arm(str(root),P,4);r._fake_restored(str(root),r.B73);r._w(str(root/r.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n');d=pathlib.Path(d);R=P['records'];sc=R['steps_cols'];row=dict(zip(sc,tr['steps'][kr]));sr=int(row['step']);baseline=r.arm_verdict(str(d),r.B73,'UT',P,root=str(root))
 state={'ul_rstep':sr,'ul_k':kr,'ul_phase':0 if kr<2 else 1,'ul_modeB':int(kr>0),'ul_pz':float(row['plate_z']),'ul_lift':float(row['lift']),'ul_ncross':max(0,kr-2),'ul_xk':-1 if kr<2 else 2,'ul_lk0':11,'ul_Pbar':float(row['Pbar']),'ul_kind':row['kind']}
 def obs(k,w,phase,step):return {'P':{None:.16,0:.16,1:.0012,2:.0008,3:.0006,4:.0004}.get(k,.0002),'Kt':1e-7,'Kr':1e-8,'Kti':1e-7,'nc':1,'na':160417,'lk':11}
 new=mk.deck_sim(mk.render(r.B73,'UT',P),obs,sr,state=state,cli={'ul_resume':'1'})
 for name in ['windows','steps','events']:
  cols=R[name+'_cols'];si=cols.index('step');head=[x for x in tr[name] if int(x[si])<=sr];rows=head+new[name];(d/f'ul_{name}.csv').write_text(','.join(cols)+'\n'+''.join(','.join(x)+'\n' for x in rows))
 (d/'run_manifest.txt').write_text(f'bed={r.B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nend=a1 fails=1 reader_rc=0\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\nstage=UT screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n')
 (d/'restart'/f'state_unload_{sr}.in').write_text(''.join(f'variable {k} {"string" if isinstance(v,str) else "equal"} {v}\n' for k,v in state.items()))
 q=subprocess.run([sys.executable,'-I',str(kit/'ul_reader.py'),'arm',str(root),r.B73,'UT'],text=True,capture_output=True);(root/'cli.log').write_text(q.stdout+q.stderr);verdict=json.loads((d/'arm_verdict.json').read_text());result.append({'kr':kr,'sr':sr,'baseline':baseline['primary_status'],'baseline_rho':baseline['rho_pct'],'new_sim_result':new['result'],'new_sim_aborted':new['aborted'],'csv_rows_match_uninterrupted':all([x for x in tr[name] if int(x[R[name+'_cols'].index('step')])>sr]==new[name] for name in ['steps','windows']),'new_events':new['events'],'cli_rc':q.returncode,'primary_status':verdict['primary_status'],'rho':verdict['rho_pct'],'problems':verdict['problems']})
(out/'deck_probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
