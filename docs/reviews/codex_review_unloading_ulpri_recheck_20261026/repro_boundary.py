"""Focused Q2 counterexamples: unchanged producer-deck fixture + one malformed marker.
Run from any folder: python -X utf8 repro_boundary.py --repo <pin checkout> --out <new directory>
Only synthetic files under --out are written. No LIGGGHTS/WSL/MPI runs.
"""
from pathlib import Path
import argparse,sys,os,json,csv,hashlib,subprocess,shutil
p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);kit=repo/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));sys.dont_write_bytecode=True
import ul_reader as u
P=u.ul_lib.load_params();rows=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['normal','literal_fractional_extra','trailing_space_event','nbsp_event','unicode_embedded_manifest','restored_control']:
 root=out/name;root.mkdir(exist_ok=True);d,tr=u._ut_trace_arm(str(root),P,4);d=Path(d);u._fake_restored(str(root),u.B73);u._w(str(root/u.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n')
 # Failed old attempt completed k=2 before its checkpoint; legal retry uses k=1.
 sr=u._hold_resume(str(d),P,old_nw=2,auth=True,kr=1)
 ep=d/'ul_events.csv';mp=d/'run_manifest.txt'
 if name in ('literal_fractional_extra','trailing_space_event','nbsp_event'):
  events=list(csv.DictReader(ep.read_text(encoding='utf8').splitlines()));ev=dict(next(e for e in events if e['event']=='RESUME'));ev['k']='1.49';ev['event']={'literal_fractional_extra':'RESUME','trailing_space_event':'RESUME ','nbsp_event':'RESUME\u00a0'}[name]
  events.append(ev);cols=P['records']['events_cols'];ep.write_bytes((','.join(cols)+'\n'+''.join(','.join(e[c] for c in cols)+'\n' for e in events)).encode())
 if name=='unicode_embedded_manifest':mp.write_bytes(mp.read_bytes()+b'note=old'+ '\u2028resume_from=3310000.49\n'.encode())
 before={n:sha(d/n) for n in ['ul_events.csv','ul_windows.csv','ul_steps.csv']};rr=u.read_run(str(d),P)
 cmd=[sys.executable,'-X','utf8','-B',str(kit/'ul_reader.py'),'arm',str(root),u.B73,'UT'];q=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',timeout=30);(root/'cli.log').write_text(q.stdout+q.stderr,encoding='utf8');v=json.loads((d/'arm_verdict.json').read_text(encoding='utf8'))
 row=dict(name=name,boundary=[1,sr],resume_auth=rr['resume_auth'],n_superseded_rows=rr['n_superseded_rows'],problems=rr['problems'],primary_status=v['primary_status'],rho_pct=v['rho_pct'],rank_eligible=v['rank_eligible'],csv_unchanged=all(sha(d/n)==h for n,h in before.items()),cli_rc=q.returncode,command=cmd);rows.append(row)
 print(json.dumps({k:v for k,v in row.items() if k not in ('command','problems')},ensure_ascii=False),flush=True)
(out/'result.json').write_text(json.dumps({'pin_reader_sha256':sha(kit/'ul_reader.py'),'cases':rows},ensure_ascii=False,indent=2),encoding='utf8')
