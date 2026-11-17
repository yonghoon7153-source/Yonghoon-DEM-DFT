"""Local synthetic stages only. The mock executable never calls an engine/MPI."""
import contextlib,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
CONSUMER=HERE.parent/'p1_rt_consumer_preparation_20261117'
sys.path.insert(0,str(CONSUMER))
import test_rt_fixture as F
from test_rt_contract import put
SOURCE=HERE.parents[2]/'docs/data/ps45_unload_20261009'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('rt_assembly',os.environ.get('RT_ASSEMBLY_SOURCE',str(HERE/'prepare_assembly.py')))
BASH=os.environ.get('RT_BASH') or shutil.which('bash')
GUARD='echo "RT_ASSEMBLY_INACTIVE: no operational seal or author field GO" >&2\nexit 2\n'

FAKE=r"""import json,os,shutil,sys
from pathlib import Path
args=sys.argv[1:];np=args[args.index('-np')+1];deck=Path(args[args.index('-in')+1]).name
vars={}
for i,x in enumerate(args):
    if x=='-var':vars[args[i+1]]=args[i+2]
out=Path(vars['out']);stage=out.name
root=Path(os.environ['FAKE_ROOT']);template=root/'template/fixture'
mode=os.environ['FAKE_MODE'];calls=root/'calls.txt'
with calls.open('a') as f:f.write(stage+' np='+np+' ckpt='+vars.get('ckpt','-')+'\n')
assert np=='6'
for part in ('producer','post'):
    src=template/stage/part
    if src.is_dir():shutil.copytree(src,out/part,dirs_exist_ok=True)
if stage=='P' and mode!='P_missing':(out/'fixture.bin').write_bytes(b'producer')
if stage=='RT1' and mode!='RT1_missing':(out/'rt.bin').write_bytes(b'rt-binary')
if stage in ('RT1','RT2'):
    text=(template/stage/'screen.out').read_text()
    if mode=='RT1_marker' and stage=='RT1':text=text.replace('UL_RT_DONE','NO_MARKER')
    if mode=='RT1_wrong_step' and stage=='RT1':text=text.replace('step=2000','step=2001')
    print(text)
    log=Path(args[args.index('-log')+1]);log.write_text('read_restart '+vars['ckpt']+'\n')
    if mode=='raw_bad' and stage=='RT2':(out/'post/rt_pair_2000.dump').write_text('bad')
else:print('synthetic producer')
if mode==stage+'_fail':raise SystemExit(9)
"""

class Assembly(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ.get('RT_TEST_TMPDIR'))
        self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.kit=self.root/'kit';M.build(SOURCE,self.kit)
        self.fixture=self.kit/'history_test/run_history_rt_candidate.sh'
        self.runner=self.kit/'run_unload_rt_candidate.sh'
        self.assertTrue(self.fixture.is_file(),'fixture runner not assembled')
        self.assertTrue(self.runner.is_file(),'production candidate not assembled')
        self.dispatch=load('rt_dispatch_candidate',self.kit/'rt_dispatch.py')
    def shell(self,script,env=None):
        self.assertTrue(BASH,'local Bash required')
        return subprocess.run([BASH,'--noprofile','--norc','-s'],input=script.encode(),cwd=self.root,
                              env=env,capture_output=True,timeout=45)
    def run_fixture(self,mode='ok',alias=False):
        if os.name=='nt':self.skipTest('full mock shell fixture runs on local Linux; no Windows field qualification')
        template=self.root/'template';template.mkdir();F.fixture(template,self.kit)
        (self.root/'fake.py').write_text(FAKE)
        mp=self.root/'fake-mpirun';mp.write_text('#!/bin/sh\nexec '+shlex_quote(sys.executable)+' '+shlex_quote(str(self.root/'fake.py'))+' "$@"\n');mp.chmod(0o700)
        lmp=self.root/'synthetic-bin';lmp.write_bytes(b'NOT AN ENGINE\n');lmp.chmod(0o700)
        work=self.root/'work';work.mkdir()
        if alias:
            link=self.root/'work_alias';link.symlink_to(work,target_is_directory=True);work=link
        raw=self.fixture.read_text();self.assertEqual(raw.count(GUARD),1)
        # Enable only a scratch copy that uses the fake executable. Committed candidate stays closed.
        active=self.fixture.with_name('exercise_only.sh');active.write_text(raw.replace(GUARD,'',1))
        # The copy/re-exec uses the same candidate filename inside the scratch kit.
        self.fixture.write_text(raw.replace(GUARD,'',1))
        sums=self.fixture.parent/'RT_HISTORY_SNAPSHOT_SHA256SUMS'
        lines=[]
        for line in sums.read_text().splitlines():
            h,n=line.split('  ',1);lines.append(hashlib.sha256((self.fixture.parent/n).read_bytes()).hexdigest()+'  '+n)
        sums.write_text('\n'.join(lines)+'\n')
        env=os.environ.copy();env.update(WORK_ROOT=str(work),HIST_STAMP='synthetic',NP='6',NP_ALT='4',
            MPIRUN=str(mp),LMP=str(lmp),PY=sys.executable,ALLOW_OTHER_LMP='1',ALLOW_CONCURRENT='1',
            FAKE_ROOT=str(self.root),FAKE_MODE=mode)
        cmd='bash '+shlex_quote(str(active))+' --rt-grammar-only\n'
        r=self.shell(cmd,env);run=work/'rt_grammar_synthetic'
        calls=(self.root/'calls.txt').read_text().splitlines() if (self.root/'calls.txt').exists() else []
        return r,run,calls
    @unittest.skipIf(os.name=='nt','full mock fixture: local Linux only')
    def test_normal_full_copy_sequence_real_reader_and_prereq(self):
        r,run,calls=self.run_fixture();self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertEqual([c.split()[0] for c in calls],['P','RT1','RT2'])
        v=json.loads((run/'rt_grammar_verdict.json').read_bytes())
        self.assertEqual(v['status'],'PASS');self.assertEqual(len(v['checks']),20)
        h=hashlib.sha256((self.root/'synthetic-bin').read_bytes()).hexdigest()
        rc=self.dispatch.main(['rt_grammar',str(run/'rt_grammar_verdict.json'),'--lmp-sha',h],kit=self.kit)
        self.assertEqual(rc,0)
        self.assertTrue(Path(str(run)+'.report.tgz').is_file())
        for name in ('ul_gates.py','ul_lib.py'):self.assertFalse((run.parent/'kit_synthetic'/name).exists())
    @unittest.skipIf(os.name=='nt','full mock fixture: local Linux only')
    def test_producer_failure_after_file_or_missing_stops_RT(self):
        for mode in ('P_fail','P_missing'):
            with self.subTest(mode=mode):
                if mode!='P_fail':self.tearDown();self.setUp()
                r,run,calls=self.run_fixture(mode)
                self.assertNotEqual(r.returncode,0);self.assertEqual([c.split()[0] for c in calls],['P'])
    @unittest.skipIf(os.name=='nt','full mock fixture: local Linux only')
    def test_RT1_failure_or_marker_or_missing_blocks_RT2(self):
        for i,mode in enumerate(('RT1_fail','RT1_missing','RT1_marker','RT1_wrong_step')):
            with self.subTest(mode=mode):
                if i:self.tearDown();self.setUp()
                r,run,calls=self.run_fixture(mode);self.assertNotEqual(r.returncode,0)
                self.assertEqual([c.split()[0] for c in calls],['P','RT1'])
    @unittest.skipIf(os.name=='nt','full mock fixture: local Linux only')
    def test_RT2_failure_and_bad_raw_not_success(self):
        for i,mode in enumerate(('RT2_fail','raw_bad')):
            with self.subTest(mode=mode):
                if i:self.tearDown();self.setUp()
                r,run,calls=self.run_fixture(mode);self.assertNotEqual(r.returncode,0)
                self.assertEqual([c.split()[0] for c in calls],['P','RT1','RT2'])
    @unittest.skipIf(os.name=='nt','full mock fixture: local Linux only')
    def test_symlink_root_realpath_reread(self):
        r,run,calls=self.run_fixture(alias=True);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        h=hashlib.sha256((self.root/'synthetic-bin').read_bytes()).hexdigest()
        self.assertEqual(self.dispatch.main(['rt_grammar',str(run.resolve()/'rt_grammar_verdict.json'),'--lmp-sha',h],kit=self.kit),0)
    def test_closed_entries_syntax_no_writes(self):
        for p in (self.fixture,self.runner):
            raw=p.read_bytes()
            before=set(self.root.rglob('*'));r=self.shell(raw.decode())
            self.assertEqual(r.returncode,2);self.assertIn(b'RT_ASSEMBLY_INACTIVE',r.stderr)
            self.assertEqual(before,set(self.root.rglob('*')))
            r=subprocess.run([BASH,'-n'],input=raw,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)
    def test_prior_122_and_original_94_preserved(self):
        prior=self.root/'prior';load('prior_build',CONSUMER/'prepare_consumer.py').build(SOURCE,prior)
        files=[p for p in prior.rglob('*') if p.is_file()];self.assertEqual(len(files),122)
        for p in files:self.assertEqual(p.read_bytes(),(self.kit/p.relative_to(prior)).read_bytes())
        for p in SOURCE.rglob('*'):
            if p.is_file():self.assertEqual(p.read_bytes(),(self.kit/p.relative_to(SOURCE)).read_bytes())
    def test_candidate_manifest_covers_all_files_and_copy_switch(self):
        sums=self.kit/'RT_ASSEMBLY_SHA256SUMS'
        listed={n:h for h,n in (s.split('  ',1) for s in sums.read_text().splitlines())}
        actual={p.relative_to(self.kit).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in self.kit.rglob('*') if p.is_file() and p!=sums}
        self.assertEqual(listed,actual)
        text=self.runner.read_text();self.assertIn('done < "$SELF_DIR/RT_ASSEMBLY_SHA256SUMS"',text)
        self.assertIn('exec bash "$KIT/run_unload_rt_candidate.sh"',text)
        self.assertIn('"$KIT/rt_dispatch.py" gate',text)
        self.assertIn('"$KIT/rt_dispatch.py" "$cmd"',text)
    def test_dispatch_default_restore_no_publish_and_gate_uses_rev5(self):
        with patch.object(self.dispatch.R,'main',return_value=2) as read:
            self.assertEqual(self.dispatch.main(['restore','synthetic','ps_7_3_r45'],kit=self.kit),2)
            self.assertNotIn('--publish-new',read.call_args[0][0])
        old=self.dispatch.R.legacy_reader(self.kit)
        with patch.object(self.dispatch.R,'legacy_reader',return_value=old),patch.object(self.dispatch.R,'job_restored',return_value=False) as new:
            self.assertEqual(self.dispatch.main(['gate',str(self.root),'ps_10_0_r45','EXT'],kit=self.kit),2)
            new.assert_called_once()
    def test_orig_grid_branches_no_value_read(self):
        C=self.dispatch.R.C;P=self.dispatch.R.legacy_reader(self.kit).ul_lib.load_params(str(self.kit/'unload_params.json'))
        bed='ps_10_0_r45'
        put(self.root/bed/'in'/P['beds'][bed]['orig_log'],'11 by 1 by 1 MPI processor grid\nLoop time of 0 on 11 procs\n')
        put(self.root/bed/'in'/P['beds'][bed]['last_deck'],'# balance 1 x 1\nrun 0\n')
        self.assertTrue(self.dispatch.orig_grid(self.root,bed,'RJ',self.kit)['ok'])
        step=P['ext_10_0']['s0p'];put(self.root/bed/'s0_decision.json',json.dumps({'status':'PASS','s0':step}))
        put(self.root/bed/'EXT/screen.txt','3 by 2 by 1 MPI processor grid\nLoop time of 0 on 6 procs\n')
        put(self.root/bed/'EXT2/screen.txt','garbage ignored\n')
        self.assertTrue(self.dispatch.orig_grid(self.root,bed,'RJ2',self.kit)['ok'])
        put(self.root/bed/'EXT/screen.txt','2 by 3 by 1 MPI processor grid\nLoop time of 0 on 6 procs\n')
        self.assertFalse(self.dispatch.orig_grid(self.root,bed,'RJ2',self.kit)['ok'])
        put(self.root/bed/'in'/P['beds'][bed]['last_deck'],'fix bal all balance 10 1.1 shift xyz 10 1.1\n')
        self.assertFalse(self.dispatch.orig_grid(self.root,bed,'RJ',self.kit)['ok'])
    def test_new_prereqs_are_RJ_RJ2_only_before_job_creation(self):
        raw=self.runner.read_text()
        new=raw.split('# >>> RT prerequisites',1)[1].split('# <<< RT prerequisites',1)[0]
        self.assertIn('case "$JOB" in RJ|RJ2)',new)
        for cmd in ('rt_grammar','orig_grid'):self.assertIn(cmd,new)
        self.assertLess(raw.index('  rt_prerequisites\n'),raw.index('JD="$WORK_ROOT/$BED/$JOB"'))
        self.assertIn('GRAMMAR_REC+=',new)
        self.assertIn('rt_grammar_prereq=PASS',new)
    def test_production_stage_and_unrelated_branches_preserved(self):
        old=(self.kit/'run_unload_rt_dev.sh').read_text();new=self.runner.read_text()
        def part(s,a,b):return s.split(a,1)[1].split(b,1)[0]
        self.assertEqual(part(old,'run_deck() {','\nbundle() {'),part(new,'run_deck() {','\nbundle() {'))
        self.assertEqual(part(old,'  EXT)\n','\nesac\nif [ "$BED"'),part(new,'  EXT)\n','\nesac\nif [ "$BED"'))
        self.assertIn('reader restore "$WORK_ROOT" "$BED" --job "$JOB" --publish-new',new)
        self.assertIn('rt_dispatch.py',new)
    def prereq_shell(self,job='RJ',mode='ok'):
        raw=self.runner.read_text().split('# >>> RT prerequisites',1)[1].split('# <<< RT prerequisites',1)[0]
        put(self.root/'verdict.json','{}\n')
        script='''set -uo pipefail
PY=fake_py; KIT=kit; WORK_ROOT=work; BED=ps_7_3_r45; LMP_SHA=synthetic
RT_GRAMMAR_VERDICT=verdict.json; GRAMMAR_REC=(grammar_prereq=PASS)
die() { exit 7; }
fake_py() { printf '%s\\n' "$3" >> prereq.calls; [ "$MODE" != "$3" ]; }
sha256sum() { [ "$MODE" != hash_fail ] || return 9; command sha256sum "$@"; }
'''+f'JOB={job}\nMODE={mode}\n'+raw+'\nrt_prerequisites\nprintf "%s\\n" "${GRAMMAR_REC[@]}"\n'
        p=self.root/'prereq.calls'
        if p.exists():p.unlink()
        r=self.shell(script)
        return r,p.read_text().splitlines() if p.exists() else []
    def test_prerequisite_failure_cannot_record_PASS(self):
        for mode,calls in [('rt_grammar',['rt_grammar']),('orig_grid',['rt_grammar','orig_grid']),('hash_fail',['rt_grammar','orig_grid'])]:
            with self.subTest(mode=mode):
                r,seen=self.prereq_shell(mode=mode);self.assertEqual(r.returncode,7,r.stdout+r.stderr)
                self.assertEqual(seen,calls);self.assertNotIn(b'rt_grammar_prereq=PASS',r.stdout)
    def test_prerequisite_success_scope_retains_original_grammar(self):
        for job in ('RJ','RJ2','EXT','UB'):
            with self.subTest(job=job):
                r,calls=self.prereq_shell(job=job);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
                self.assertIn(b'grammar_prereq=PASS',r.stdout)
                self.assertEqual(calls,['rt_grammar','orig_grid'] if job in ('RJ','RJ2') else [])
                self.assertEqual(b'rt_grammar_prereq=PASS' in r.stdout,job in ('RJ','RJ2'))
def shlex_quote(s):
    import shlex
    return shlex.quote(s)
if __name__=='__main__':unittest.main(verbosity=2)
