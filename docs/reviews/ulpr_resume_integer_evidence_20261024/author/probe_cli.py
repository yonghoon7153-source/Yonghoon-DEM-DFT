"""Replay real arm CLI on copied clean generated-deck RESUME fixture.
--fixtures must be the deck_probe.py output; --repo selects reader, --out is new scratch.
"""
import argparse,csv,hashlib,json,pathlib,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=pathlib.Path);p.add_argument('--fixtures',required=True,type=pathlib.Path);p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args()
repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));import ul_reader as reader
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cases=['normal','exact_decimal','fractional_k','fractional_step','rounded_decimal_k','unicode_k','ambiguous_event','fractional_state','duplicate_state','malformed_manifest']
results=[]
for name in cases:
 root=out/name;shutil.copytree(a.fixtures/'k3',root,dirs_exist_ok=True);d=root/reader.B73/'UT';ep=d/'ul_events.csv';rows=list(csv.DictReader(ep.open()));cols=list(rows[0]);ev=next(x for x in rows if x['event']=='RESUME');sr=int(ev['step']);sp=d/'restart'/f'state_unload_{sr}.in'
 if name=='exact_decimal':ev['k']='3.000e0';ev['step']=str(sr)+'.0'
 if name=='fractional_k':ev['k']='3.49'
 if name=='fractional_step':ev['step']=str(sr)+'.49'
 if name=='rounded_decimal_k':ev['k']='3.0000000000000001'
 if name=='unicode_k':ev['k']='٣'
 if name=='ambiguous_event':rows.insert(rows.index(ev),dict(ev,k='3.49'))
 if name=='fractional_state':sp.write_text(sp.read_text().replace('variable ul_k equal 3\n','variable ul_k equal 3.0000000000000001\n'))
 if name=='duplicate_state':sp.write_text(sp.read_text()+'variable ul_k equal 3\n')
 if name=='malformed_manifest':mp=d/'run_manifest.txt';mp.write_text(mp.read_text()+'resume_from=3.49\n')
 with ep.open('w') as f:w=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows(rows)
 before={n:sha(d/n) for n in ['ul_events.csv','ul_windows.csv','ul_steps.csv']}
 cmd=[sys.executable,'-I',str(kit/'ul_reader.py'),'arm',str(root),reader.B73,'UT'];r=subprocess.run(cmd,capture_output=True,text=True);(root/'cli.log').write_text(r.stdout+r.stderr);v=json.loads((d/'arm_verdict.json').read_text());rr=reader.read_run(str(d));result=dict(name=name,command=cmd,rc=r.returncode,auth=rr['resume_auth'],primary_status=v['primary_status'],rho=v['rho_pct'],problems=v['problems'],csv_unchanged=all(sha(d/n)==h for n,h in before.items()));results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
(out/'results.json').write_text(json.dumps(dict(source_sha256=sha(kit/'ul_reader.py'),script_sha256=sha(pathlib.Path(__file__)),cases=results),ensure_ascii=False,indent=2))
