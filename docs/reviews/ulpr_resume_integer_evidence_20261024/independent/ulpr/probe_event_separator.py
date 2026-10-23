from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
K=Path('/workspace/.cloud-setup/nonrint-20261024/ulpr/work/docs/data/ps45_unload_20261009'); O=Path('/workspace/.cloud-setup/nonrint-20261024/audit/ulpr/event-separator-v4'); O.mkdir(exist_ok=False)
sys.path.insert(0,str(K)); import ul_reader as u
P=u.ul_lib.load_params(); d=Path(u._unfinished_resume(str(O/'fixture'),P)); e=d/'ul_events.csv'; original=e.read_text(); line=next(x for x in original.splitlines() if x.startswith('RESUME,')); results=[]
for sep in ['\u0085','\u2028','\u2029']:
 parts=line.split(',');parts[1]='3'+sep+'.49';e.write_text(original+','.join(parts)+'\n');r=u.read_run(str(d),P);results.append({'separator':hex(ord(sep)),'resume_auth':r['resume_auth'],'superseded':r['n_superseded_rows'],'problems':r['problems']})
e.write_text(original)
(O/'results.json').write_text(json.dumps({'reader_sha256':hashlib.sha256((K/'ul_reader.py').read_bytes()).hexdigest(),'cases':results},ensure_ascii=False,indent=2)+'\n');print(json.dumps(results,ensure_ascii=False,indent=2))
