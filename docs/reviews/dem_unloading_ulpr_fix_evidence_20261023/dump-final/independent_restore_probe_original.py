import argparse,pathlib,sys,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit))
import ul_reader as r,ul_lib as l,ul_gates as g
P=l.load_params();results=[];s0=P['beds'][r.B73]['s0'];good={'schema':'ps45_unload_history_verdict_v1','exit_code':0,'rows':{f'H{i}':{'status':'PASS'} for i in range(6)},'info':{'syn':{'status':'PASS','plate_fn_sign':-1},'force_timing':'PASS'}}
cases=['baseline','nan_box','short_box','no_bounds','bad_atoms_header','g2c_wrong_step','missing_c26','g2_duplicate_id','g2_nan','g2_extra_short_row','g2_both_wrong_step','g2_numeric_equal_token']
for case in cases:
 root=out/case;root.mkdir(exist_ok=True);J=pathlib.Path(r._mk_rj(str(root),r.B73,P));hv=root/'history.json';hv.write_text(json.dumps(good));r._w(str(root/r.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n');ap=J/'R/g2'/f'atom_{s0}.liggghts';text=ap.read_text();cp=J/'R/g2'/f'contact_{s0}.liggghts'
 if case=='nan_box':text=text.replace('0.0 0.05','nan inf',1)
 elif case=='short_box':text=text.replace('0.0 0.05','0.0',1)
 elif case=='no_bounds':text=text.replace('0.0 0.05','',1)
 elif case=='bad_atoms_header':text=text.replace('ITEM: ATOMS','ITEM: ATOMSGARBAGE',1)
 elif case=='g2c_wrong_step':cp.write_text(cp.read_text().replace(f'TIMESTEP\n{s0}\n',f'TIMESTEP\n{s0+1}\n'))
 elif case=='missing_c26':cp.write_text(cp.read_text().replace('c_cpl[26]','absent_c26'))
 elif case=='g2_duplicate_id':text=text.replace('NUMBER OF ATOMS\n3\n','NUMBER OF ATOMS\n4\n')+text.splitlines()[-1]+'\n'
 elif case=='g2_nan':text=text.replace(' 0.003 ', ' nan ',1)
 elif case=='g2_extra_short_row':text+='4 3 0\n'
 elif case=='g2_both_wrong_step':
  text=text.replace(f'TIMESTEP\n{s0}\n',f'TIMESTEP\n{s0+1}\n');p2=root/r.B73/'in'/f'atom_{s0}.liggghts';p2.write_text(p2.read_text().replace(f'TIMESTEP\n{s0}\n',f'TIMESTEP\n{s0+1}\n'))
 elif case=='g2_numeric_equal_token':text=text.replace(' 0.003 ', ' 0.0030 ',1)
 ap.write_text(text)
 q=subprocess.run([sys.executable,'-I',str(kit/'ul_reader.py'),'restore',str(root),r.B73,'--hist',str(hv)],text=True,capture_output=True);(root/'cli.log').write_text(q.stdout+q.stderr);verdict=json.loads((J/'restore_verdict.json').read_text());gate=subprocess.run([sys.executable,'-I',str(kit/'ul_reader.py'),'gate',str(root),r.B73,'UB'],text=True,capture_output=True);(root/'gate.log').write_text(gate.stdout+gate.stderr);results.append({'case':case,'restore_rc':q.returncode,'status':verdict['status'],'G2':verdict['checks']['G2'],'G2c':verdict['checks']['G2c'],'gate_rc':gate.returncode})
(out/'restore_probe.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
