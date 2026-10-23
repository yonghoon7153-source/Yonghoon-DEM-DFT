import argparse,pathlib,sys,json,shutil
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);p.add_argument('--fixtures',required=True);a=p.parse_args();repo=pathlib.Path(a.repo).resolve();out=pathlib.Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);f=pathlib.Path(a.fixtures).resolve();sys.path.insert(0,str(repo/'docs/data/ps45_unload_20261009'))
import ul_reader as r,ul_lib as l,ul_gates as g
base=f/'restore-probe/baseline/ps_7_3_r45/RJ/R/g2/atom_3200000.liggghts';text=base.read_text();res=[]
for token in ['nan','inf','-inf','1e309','9007199254740993','1.5','1.0000000000000001','0','-1','١']:
 raw=text.replace('\n1 3 ',f'\n{token} 3 ',1);path=out/('atom_'+str(len(res))+'.dump');path.write_text(raw);res.append({'class':'G2_ID','token':token,'verdict':g.g2_compare(str(path),str(base),expected_step=3200000)})
for token in ['nan','inf','1e309']:
 path=out/('atom_'+str(len(res))+'.dump');path.write_text(text.replace(' 0.003 ',f' {token} ',1));res.append({'class':'G2_coordinate','token':token,'verdict':g.g2_compare(str(path),str(base),expected_step=3200000)})
for token in ['nan','inf','1e309','3.49','٣',' 3 ']:
 d=out/('resume_'+str(len(res)));shutil.copytree(f/'deck-probe/k3/ps_7_3_r45/UT',d,dirs_exist_ok=True);ep=d/'ul_events.csv';ep.write_text(ep.read_text().replace('RESUME,3,','RESUME,'+token+','));run=r.read_run(str(d));res.append({'class':'RESUME_k','token':token,'auth':run['resume_auth'],'problems':run['problems']})
(out/'edge_probe.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps([{'class':x['class'],'token':x['token'],'status':x['verdict']['status'] if 'verdict' in x else x['auth']} for x in res],ensure_ascii=False,indent=2))
