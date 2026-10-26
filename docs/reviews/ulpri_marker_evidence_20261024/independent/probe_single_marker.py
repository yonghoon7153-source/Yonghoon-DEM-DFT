"""Single canonical-marker replacement, keeping exact integer boundary evidence."""
from pathlib import Path
import argparse, csv, hashlib, json, subprocess, sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=a.output.resolve();root.mkdir(parents=True)
kit=a.repo.resolve()/'docs/data/ps45_unload_20261009';sys.path.insert(0,str(kit));sys.dont_write_bytecode=True
import ul_reader as u
P=u.ul_lib.load_params();rows=[]
for c in (' ', '\t', '\u00a0', '\x0b','\x0c','\x1c','\x1d','\x1e','\x85','\u2028','\u2029'):
 for side in ('prefix','suffix'):
  n=f'{ord(c):04x}_{side}';droot=root/n;droot.mkdir()
  ds,tr=u._ut_trace_arm(str(droot),P,4);d=Path(ds);u._fake_restored(str(droot),u.B73);u._w(str(droot/u.B73/'ul_base.in'),'variable ul_S2max equal 1e-05\n')
  sr=u._hold_resume(str(d),P,old_nw=2,auth=True,kr=1)
  ep=d/'ul_events.csv';raw=ep.read_bytes();needle=b'\nRESUME,';assert raw.count(needle)==1
  marker=c+'RESUME' if side=='prefix' else 'RESUME'+c
  ep.write_bytes(raw.replace(needle,('\n'+marker+',').encode()))
  files=[d/f'ul_{x}.csv' for x in ('events','windows','steps')];before={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
  run=u.read_run(str(d),P)
  q=subprocess.run([sys.executable,'-I','-B',str(kit/'ul_reader.py'),'arm',str(droot),u.B73,'UT'],capture_output=True,text=True,timeout=60)
  (droot/'cli.log').write_text(q.stdout+q.stderr);v=json.loads((d/'arm_verdict.json').read_text())
  unchanged=before=={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
  reject=run['resume_auth']==[] and run['n_superseded_rows']==0 and bool(run['problems']) and v['primary_status']=='UNIDENTIFIED' and v['rho_pct'] is None and v['rank_eligible'] is False
  rows.append({'case':n,'codepoint':f'U+{ord(c):04X}','side':side,'resume_auth':run['resume_auth'],'dropped':run['n_superseded_rows'],'problems':run['problems'],'primary':v['primary_status'],'rho':v['rho_pct'],'rank_eligible':v['rank_eligible'],'csv_unchanged':unchanged,'cli_rc':q.returncode,'pass':reject and unchanged and q.returncode==0})
report={'reader_sha256':hashlib.sha256((kit/'ul_reader.py').read_bytes()).hexdigest(),'cases':rows,'passed':sum(r['pass'] for r in rows),'count':len(rows),'physical_runs':0}
(root/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('reader_sha256','passed','count')}))
raise SystemExit(0 if all(r['pass'] for r in rows) else 1)
