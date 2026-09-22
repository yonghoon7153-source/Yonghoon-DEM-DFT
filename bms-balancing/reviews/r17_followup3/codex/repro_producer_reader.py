"""Real fit_cycles API on synthetic workbook, then its common-vs-row receipt contract.
No real data, no production changes. Disk publication is review-owned serialization:
Windows has no fcntl, so this is NOT a successful production CLI publication claim.
"""
import argparse, csv, datetime, hashlib, json, os, pathlib, subprocess, sys, tempfile, time
sys.stdout.reconfigure(encoding='utf-8')
ap=argparse.ArgumentParser();ap.add_argument('--target',required=True,type=pathlib.Path);args=ap.parse_args()
ROOT=args.target.resolve();HERE=pathlib.Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'tests'),str(ROOT/'scripts')]
from test_r6_internal import _synth_root
from test_cycles import _cycle_workbook
from bms_balancing import cycles as C, schema as S, data as D
from provenance import git_provenance, sidecar_dict
work=pathlib.Path(tempfile.mkdtemp(prefix='producer-',dir=HERE))
src=_synth_root(work);wb=_cycle_workbook(src,work/'syn.xlsx',n_cycles=2)
start=time.monotonic()
res=C.fit_cycles(src,src/'data/half_cell/GITT/pristine.xlsx',wb,'Li',cell='syn',
    objective_version='legacy_matlab',n_starts=1,seed=0,scale_seed=0,run_id='synthetic-production',
    widths=True,width_tol=.01,width_starts=0,width_grid=0)
art=work/'cycles_syn_Li.csv'
with art.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=S.CYCLES_ROW,lineterminator='\n');w.writeheader();w.writerows(res['rows'])
pv=git_provenance(cwd=str(ROOT))
extra={'cell':'syn','si_source':'Li','starts':1,'seed':0,'scale_seed':0,'w_dqdv':0.,
    'cycles':res['cycles'],'status':'complete','dataset_manifest':D.half_cell_manifest_identity(),
    'consumed_inputs':res['consumed'],**res['settings']}
meta=sidecar_dict(art.name,art.read_bytes(),run_id='synthetic-production',
    started={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git':pv},argv=['synthetic API fixture'],pv=pv,extra=extra)
art.with_name(art.name+'.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
rows=list(csv.DictReader(art.open(encoding='utf-8',newline='')))
cmd=[sys.executable,str(ROOT/'scripts/width_report.py'),str(art)]
p=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONUTF8='1'),capture_output=True,text=True,encoding='utf-8',timeout=120)
record={'target':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'fixture':str(work),'scope':'real fit_cycles API with synthetic inputs; review-owned serialization, not CLI publication',
    'seconds':time.monotonic()-start,'width_status':[r['width_status'] for r in rows],
    'check_rows':S.check_rows('cycles',rows,list(rows[0]),art.name),
    'common_full_cell':meta['consumed_inputs']['full_cell'],
    'row_full_cell':[json.loads(r['consumed_inputs'])['full_cell'] for r in rows],
    'command':cmd,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
# Axis isolation only: stripping producer's per-row cycle is not a proposed fix.
control=work/'control_without_row_cycle';control.mkdir()
control_art=control/art.name
for row in rows:
    receipt=json.loads(row['consumed_inputs']);receipt['full_cell'].pop('cycle')
    row['consumed_inputs']=json.dumps(receipt,ensure_ascii=False,sort_keys=True)
    row['inputs_sha']=S.inputs_digest(receipt)
with control_art.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=S.CYCLES_ROW,lineterminator='\n');w.writeheader();w.writerows(rows)
meta['sha256']=hashlib.sha256(control_art.read_bytes()).hexdigest()
control_art.with_name(control_art.name+'.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
control_cmd=[sys.executable,str(ROOT/'scripts/width_report.py'),str(control_art)]
control_p=subprocess.run(control_cmd,cwd=ROOT,env=dict(os.environ,PYTHONUTF8='1'),capture_output=True,text=True,encoding='utf-8',timeout=120)
record['control_without_row_cycle']={'command':control_cmd,'rc':control_p.returncode,'stdout':control_p.stdout,'stderr':control_p.stderr}
(HERE/'PRODUCER_READER_RESULTS.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'producer_reader.log').write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
print(json.dumps(record,ensure_ascii=False,indent=2))
