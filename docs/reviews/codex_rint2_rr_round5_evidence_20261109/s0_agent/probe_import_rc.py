"""Small synthetic archive probes for fixed importer. No S0/solver execution."""
from pathlib import Path
from contextlib import redirect_stdout,redirect_stderr
from unittest import mock
import argparse,hashlib,io,json,sys,tarfile,types
import numpy as np
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,default=ROOT.parent/'package/repo')
ap.add_argument('--out',type=Path,default=ROOT/'parser_cases')
a=ap.parse_args()
REPO=a.repo
SOURCE=REPO/'docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py'
OUT=a.out;OUT.mkdir(parents=True,exist_ok=False)
source=SOURCE.read_bytes();module=types.ModuleType('independent_s0_importer');module.__file__=str(SOURCE)
exec(compile(source,str(SOURCE),'exec'),module.__dict__)
plan=b'{"synthetic":true}\n';psha=hashlib.sha256(plan).hexdigest()
nb=io.BytesIO();np.savez(nb,id=np.array([1],dtype='int64'))
base={'output/s0_stage1_kit_SBE_vgcf100.json':b'{"stage":1,"kit":{"name":"kit_SBE_vgcf100"}}\n',
      'output/s0_junctions_kit_SBE_vgcf100.npz':nb.getvalue(),
      'output/s0_instances_kit_SBE_vgcf100.npz':nb.getvalue(),
      'output/cjunc_plan.json':plan,'output/cjunc_plan.sha256':(psha+'  cjunc_plan.json\n').encode(),
      'output/payload_capture_kit_SBE_vgcf100.log':b'synthetic reference only rc=0\n'}
cases=[('good',{'run/rss.log':b'pid=1 cap_gb=41\n0 12\n5 14\nrc=0\n'},0),
       ('rc1',{'run/rss.log':b'pid=1 cap_gb=41\n0 12\nrc=1\n'},2),
       ('cap',{'run/rss.log':b'pid=1 cap_gb=41\n5 CAP_TERM 41\nrc=0\n'},2),
       ('two0',{'run/rss.log':b'pid=1 cap_gb=41\nrc=0\nrc=0\n'},2),
       ('absent',{'run/rss.log':b'pid=1 cap_gb=41\n0 12\n'},2),
       ('wrongfile',{'run/rss.log':b'pid=1 cap_gb=41\n0 12\n','run/old_rss.log':b'rc=0\n'},None),
       ('nonterminal',{'run/rss.log':b'pid=1 cap_gb=41\nrc=0\n5 14\n'},None)]
rows=[]
for label,logs,expected in cases:
    root=OUT/label;root.mkdir();tgz=root/'in.tgz';content=dict(base,**logs)
    with tarfile.open(tgz,'w:gz') as tf:
        for name,b in content.items():
            item=tarfile.TarInfo(name);item.size=len(b);tf.addfile(item,io.BytesIO(b))
    before=hashlib.sha256(tgz.read_bytes()).hexdigest();capture=io.StringIO()
    argv=['import_s0_tgz.py',str(tgz),str(root/'out'),'--tmp',str(root/'unpack'),'--date','20261109']
    with mock.patch.object(sys,'argv',argv),redirect_stdout(capture),redirect_stderr(capture):rc=module.main()
    assert hashlib.sha256(tgz.read_bytes()).hexdigest()==before
    text=capture.getvalue();(root/'console.txt').write_text(text,encoding='utf-8')
    row=dict(case=label,expected_rc=expected,rc=rc,stdout=text,raw_log_contents={k:v.decode() for k,v in logs.items()},input_archive_preserved=True)
    rows.append(row)
    if expected is not None:assert rc==expected,row
result=dict(source_sha256=hashlib.sha256(source).hexdigest(),claimed_five_cases='PASS',
            rows=rows,automatic_output_is_candidate_only=True,manual_source_verification_still_required=True,
            science_executed=False,whole_gate='HOLD')
(ROOT/'parser_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
print([(r['case'],r['rc']) for r in rows])
