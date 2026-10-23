import argparse,pathlib,subprocess,sys,types,json
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);p.add_argument('--fixtures',required=True);p.add_argument('--base-ref',default='HEAD');a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);f=pathlib.Path(a.fixtures).resolve();kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));mods={}
for name in ['ul_reader','ul_gates']:
 source=subprocess.check_output(['git','-C',str(repo),'show',a.base_ref+':docs/data/ps45_unload_20261009/'+name+'.py'],text=True);m=types.ModuleType('base_'+name);m.__file__=str(kit/(name+'.py'));exec(compile(source,m.__file__,'exec'),m.__dict__);mods[name]=m
r=mods['ul_reader'];g=mods['ul_gates'];res={}
root=f/'deck-probe/k3';verdict=r.arm_verdict(str(root/r.B73/'UT'),r.B73,'UT',root=str(root));res['base_clean_resume']={k:verdict[k] for k in ['primary_status','rho_pct','problems']}
root=f/'restore-probe/nan_box';s0=3200000;res['base_nan_box_g2']=g.g2_compare(str(root/r.B73/'RJ/R/g2'/f'atom_{s0}.liggghts'),str(root/r.B73/'in'/f'atom_{s0}.liggghts'))
root=f/'restore-probe/g2c_wrong_step';res['base_wrong_step_g2c']=g.g2c_compare(str(root/r.B73/'RJ/R/g2'/f'contact_{s0}.liggghts'),str(root/r.B73/'in'/f'contact_{s0}.liggghts'))
(out/'base_compare.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
