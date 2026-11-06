"""Independent same-code and same-bed consumer probes in generated temporary folders.
Kit argv extraction is replaced with fixed argv because Linux shell is not available.
Real kit discovery, file reads, hashes, view/consumer comparisons and git queries remain production functions.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='1'
import sys,json,subprocess,shutil,copy,hashlib,tempfile
from pathlib import Path
OUT=Path(__file__).resolve().parent; ROOT=OUT.parent/'received'/'repo'
tempfile.tempdir=str(OUT)
sys.path.insert(0,str(ROOT/'scripts'))
import rint_r_chain as RR, ca_s0_census as S0
P=Path(tempfile.mkdtemp(prefix='source_fixture_',dir=OUT))
scripts=P/'repo'/'scripts'; scripts.mkdir(parents=True)
os.environ['GIT_CONFIG_COUNT']='1'
os.environ['GIT_CONFIG_KEY_0']='safe.directory'
os.environ['GIT_CONFIG_VALUE_0']=str(scripts.parent).replace('\\','/')
for n in RR.CODE_FILES:shutil.copy2(ROOT/'scripts'/n,scripts/n)
def git(*args):
    r=subprocess.run(['git','-C',str(scripts.parent),*args],capture_output=True,text=True)
    assert r.returncode==0,(args,r.stderr)
    return r.stdout.strip()
git('init'); git('add','.'); git('-c','user.name=Review Fixture','-c','user.email=review@example.invalid','commit','-m','Synthetic source binding fixture')
files=RR.code_files(scripts); head=git('rev-parse','HEAD')
base={'chain':RR.git_identity(scripts/'rint_r_chain.py'),'runner':RR.git_identity(scripts/RR.RUNNER_NAME),
      'files':files,'runner_files':copy.deepcopy(files),'runner_sha256':RR.sha256_file(scripts/RR.RUNNER_NAME),
      'env':{'unit':RR.RC.env_unit_now()}}
assert RR.code_dirty_problem(base) is None
out={'code':{'clean':RR.code_dirty_problem(base)}}
loose=P/'untracked_copy'; loose.mkdir(); shutil.copy2(scripts/'rint_r_chain.py',loose/'rint_r_chain.py')
out['code']['outside_git']=RR._identity_problem(RR.git_identity(loose/'rint_r_chain.py'),'copy')
assert out['code']['outside_git']
(scripts/'new_helper.py').write_text('x=1\n')
out['code']['untracked']=RR._identity_problem(RR.git_identity(scripts/'rint_r_chain.py'),'chain')
assert out['code']['untracked']
# Reversible in-fixture edits only. Hold git identity fixed to isolate byte-comparison protection.
(scripts/'step3_conv_cert.py').write_text((scripts/'step3_conv_cert.py').read_text(encoding='utf-8')+'\n# synthetic drift\n',encoding='utf-8')
changed=copy.deepcopy(base); changed['runner_files']=RR.code_files(scripts)
out['code']['same_head_runner_file_drift']=RR.code_dirty_problem(changed)
assert out['code']['same_head_runner_file_drift']
for name,fn in [('dirty_unknown',lambda r:r['chain'].update(dirty=None)),
                ('head_short',lambda r:r['chain'].update(head=head[:9])),
                ('env_numpy_changed',lambda r:r['env']['unit'].update(numpy='other'))]:
    r=copy.deepcopy(base);fn(r)
    why=RR.code_dirty_problem(r) if name!='env_numpy_changed' else RR.code_key_diff(base,r)
    assert why and (name!='env_numpy_changed' or RR.code_key(base)!=RR.code_key(r))
    out['code'][name]=why

# Exact bed file binding; small file content is synthetic and never solved.
kroot=P/'kits'; kit=kroot/RR.DBE_KIT; run=kit/'run_001'; run.mkdir(parents=True)
for n in ('se_dump.npy','phase.npy','fibre.npy','fibre_kind.npy','fibre_dia.npy','scaffold.csv'):
    (run/n).write_bytes(('synthetic-'+n).encode())
(run/'metrics.json').write_text(json.dumps({'um_box_um':10.,'thickness_um':8.}),encoding='utf-8')
(kit/'run_mpm.sh').write_text('fixture-settings-v1',encoding='utf-8')
argv=['--se','se_dump.npy','--phase','phase.npy','--fibre','fibre.npy','--fibre-dia','fibre_dia.npy',
      '--metrics-json','metrics.json','--scaffold','scaffold.csv']
orig_resolve,orig_settings=S0.resolve_payload_argv,S0.kit_settings_sha256
S0.resolve_payload_argv=lambda *a,**kw:list(argv)
S0.kit_settings_sha256=lambda k:hashlib.sha256(Path(k,'run_mpm.sh').read_bytes()).hexdigest()
try:
    inp=S0.kit_input_record(str(kit)); recs={'stage2':{'inputs':inp}}
    assert RR.bed_problem(recs,kroot,(RR.DBE_KIT,))
    moved=P/'kits_moved'; shutil.copytree(kroot,moved)
    assert RR.bed_problem(recs,moved,(RR.DBE_KIT,))
    def reject(label,path,new):
        old=path.read_bytes(); path.write_bytes(new)
        try:
            try: RR.bed_problem(recs,kroot,(RR.DBE_KIT,))
            except RR.Stop as e:out['bed'][label]={'code':e.code,'why':str(e)}
            else:raise AssertionError(label+' accepted')
        finally:path.write_bytes(old)
    out['bed']={'honest':'accepted','path_only_copy':'accepted'}
    reject('fibre_bytes_drift',run/'fibre.npy',b'changed-fibre')
    reject('kind_bytes_drift',run/'fibre_kind.npy',b'changed-kind')
    reject('settings_drift',kit/'run_mpm.sh',b'fixture-settings-v2')
    reject('metrics_drift',run/'metrics.json',b'{"um_box_um": 11, "thickness_um": 8}')
finally:S0.resolve_payload_argv, S0.kit_settings_sha256=orig_resolve,orig_settings
out['scope']='Code: real Git and source byte digests. Bed: real discovery/hash/read/compare, fixed argv and settings extractor adapters only; no shell/payload execution.'
OUT.joinpath('source_binding_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
