"""Run the generated RJ/RJ2 control-flow slice with fake stages, never an engine."""
import importlib.util
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'docs/data/ps45_unload_20261009'
spec=importlib.util.spec_from_file_location('rt_runner_prepare',os.environ.get('RT_RUNNER_SOURCE',str(HERE/'prepare_rt_runner.py')))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASH=os.environ.get('RT_BASH') or shutil.which('bash')
if not BASH:raise RuntimeError('A local Bash is required; set RT_BASH')
ORIGINAL=(SOURCE/'run_unload.sh').read_bytes()
BRIDGE=(HERE/'rt_bridge.sh').read_bytes()

@contextmanager
def scratch():
    parent=Path(os.environ.get('RT_TEST_TMPDIR',tempfile.gettempdir())).resolve()
    temp=tempfile.TemporaryDirectory(dir=parent)
    target=Path(temp.name).resolve()
    assert target.parent==parent and target!=parent
    try:
        yield target
    finally:
        # Windows may retain a just-finished shell's cwd handle briefly.
        # Retry cleanup only; assertions and shell execution are never retried.
        for attempt in range(20):
            try:
                temp.cleanup();break
            except PermissionError:
                if attempt==19:raise
                time.sleep(0.1)

HARNESS=r'''set -uo pipefail
ROOT=$(pwd); JD="$ROOT/RJ"; mkdir -p "$JD"; MAN="$JD/run_manifest.txt"
IN="$ROOT/in"; KIT="$ROOT/kit"; WORK_ROOT="$ROOT"; NP=6; CKPT0="$ROOT/seed.bin"
printf seed > "$CKPT0"; : > "$MAN"; : > calls.txt; FAILS=0; RRC=0
PY=fake_py
note() { printf '%s\n' "$*" >> "$MAN"; }
say() { :; }
tbl() { printf 'original.in\n'; }
fake_py() { [ "$MODE" != g0_fail ]; }
reader() { printf 'reader:%s\n' "$*" >> calls.txt; return 0; }
run_deck() {
  local dir=$1 kind=$2 ck=$3
  printf '%s|%s|%s|%s\n' "$kind" "$ck" "$4" "$5" >> calls.txt
  mkdir -p "$dir/post" "$dir/obs"; printf 'UL_RT_DONE bed=test step=2000\n' > "$dir/screen.txt"
  [ "$kind" != R ] || printf un > "$dir/un_diag.bin"
  if [ "$kind" = RT1 ]; then
    [ "$MODE" = missing_bin ] || printf 'fresh-rt-binary' > "$dir/rt.bin"
    [ "$MODE" != marker_missing ] || : > "$dir/screen.txt"
  fi
  if [ "$kind" = RT2 ] && [ "$MODE" = rt2_marker_missing ]; then : > "$dir/screen.txt"; fi
  if [ "$MODE" = "fail_$kind" ]; then FAILS=$((FAILS + 1)); return 9; fi
  return 0
}
sha256sum() {
  if [ "$MODE" = hash_fail ]; then return 5; fi
  if [ "$MODE" = hash_bad ]; then printf 'BADHASH  synthetic\n'; return 0; fi
  if [ "$MODE" = hash_second_fail ] && [ -f hash.once ]; then return 5; fi
  local target=$1
  [ "$target" != -- ] || target=$2
  if [ "$MODE" = hash_change ] && [ -f hash.once ]; then printf mutated > "$target"; fi
  : > hash.once; command sha256sum "$@"
}
'''

class RTRunner(unittest.TestCase):
    def rendered(self):return m.render_runner(ORIGINAL,BRIDGE).decode()
    def run_case(self,mode='normal',bed='ps_7_3_r45',job='RJ'):
        raw=self.rendered()
        arm=raw.split('\n  RJ|RJ2)\n',1)[1].split('\n    ;;',1)[0]
        bridge=''
        if '# >>> RT bridge' in raw:bridge=raw.split('# >>> RT bridge',1)[1].split('# <<< RT bridge',1)[0]
        script=HARNESS+'\nMODE='+mode+'\nBED='+bed+'\nJOB='+job+'\n'+bridge+'\n'+arm+'\nprintf "PRE_OK=%s FAILS=%s\\n" "$PRE_OK" "$FAILS"\ncat calls.txt\ncat "$MAN"\n'
        with scratch() as td:
            p=Path(td);(p/'exercise.sh').write_text(script,encoding='utf8',newline='\n')
            run=subprocess.run([BASH,'--noprofile','--norc','exercise.sh'],cwd=p,text=True,encoding='utf8',capture_output=True,timeout=15)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            return run.stdout,(p/'calls.txt').read_text(),(p/'RJ/run_manifest.txt').read_text()
    def test_normal_order_and_same_checkpoint_binding(self):
        out,calls,man=self.run_case()
        self.assertEqual([x.split('|')[0] for x in calls.splitlines() if '|' in x],['Ut0','R','UNread','RT1','RT2','UK'])
        rows=[x for x in calls.splitlines() if x.startswith(('RT1|','RT2|'))]
        self.assertTrue(rows[0].split('|')[1].endswith('/seed.bin'))
        self.assertTrue(rows[1].split('|')[1].endswith('/RJ/RT1/rt.bin'))
        self.assertIn('PRE_OK=1 FAILS=0',out)
        self.assertEqual(man.count('rt1_bin='),1);self.assertEqual(man.count('rt2_ckpt='),1)
    def test_g0_failure_skips_both_RT_and_UK(self):
        out,calls,man=self.run_case('g0_fail');self.assertNotIn('|',calls)
        self.assertIn('stage=RT1 skipped',man);self.assertIn('stage=RT2 skipped',man)
    def test_R_UN_Ut0_failures_skip_both_RT(self):
        for mode in ('fail_R','fail_UNread','fail_Ut0'):
            with self.subTest(mode=mode):
                out,calls,man=self.run_case(mode)
                self.assertNotIn('RT1|',calls);self.assertNotIn('RT2|',calls);self.assertNotIn('UK|',calls)
                self.assertIn('stage=RT1 skipped',man);self.assertIn('stage=RT2 skipped',man)
    def test_RT1_failed_after_writing_restart_never_starts_RT2(self):
        out,calls,man=self.run_case('fail_RT1')
        self.assertIn('RT1|',calls);self.assertNotIn('RT2|',calls);self.assertNotIn('UK|',calls)
        self.assertIn('stage=RT2 skipped',man);self.assertIn('PRE_OK=0',out)
    def test_missing_binary_or_marker_rejects_RT2(self):
        for mode in ('missing_bin','marker_missing'):
            with self.subTest(mode=mode):
                out,calls,man=self.run_case(mode);self.assertIn('RT1|',calls)
                self.assertNotIn('RT2|',calls);self.assertIn('PRE_OK=0',out)
    def test_hash_failure_or_between_stage_change_rejects_RT2(self):
        for mode in ('hash_fail','hash_change','hash_bad','hash_second_fail'):
            with self.subTest(mode=mode):
                out,calls,man=self.run_case(mode);self.assertIn('RT1|',calls)
                self.assertNotIn('RT2|',calls);self.assertIn('PRE_OK=0',out)
    def test_RT2_failure_blocks_UK(self):
        for mode in ('fail_RT2','rt2_marker_missing'):
            with self.subTest(mode=mode):
                out,calls,man=self.run_case(mode);self.assertIn('RT2|',calls)
                self.assertNotIn('UK|',calls);self.assertIn('PRE_OK=0',out)
    def test_ten_zero_RJ_no_UK_but_RJ2_has_UK(self):
        for job,want in (('RJ',False),('RJ2',True)):
            with self.subTest(job=job):
                out,calls,man=self.run_case(bed='ps_10_0_r45',job=job)
                self.assertIn('RT2|',calls);self.assertEqual('UK|' in calls,want);self.assertNotIn('Ut0|',calls)
    def test_restore_publish_new_only_after_stage_attempts(self):
        out,calls,man=self.run_case();self.assertIn('--publish-new',calls)
        self.assertLess(calls.index('RT2|'),calls.index('reader:restore'))
    def test_manifest_job_dir_is_recorded_and_stage_function_unchanged(self):
        raw=self.rendered();self.assertIn('echo "job_dir=$JD"',raw)
        def stage(s):return s.split('run_deck() {',1)[1].split('\nbundle() {',1)[0]
        self.assertEqual(stage(raw),stage(ORIGINAL.decode()))
    def test_generated_candidate_closed_until_reader_integration(self):
        self.assertIn('RT_RUNNER_LAYER_ONLY',self.rendered())
        run=subprocess.run([BASH,'--noprofile','--norc','-s'],input=self.rendered().encode('utf8'),cwd=HERE,capture_output=True,timeout=10)
        self.assertEqual(run.returncode,2);self.assertIn(b'RT_RUNNER_LAYER_ONLY',run.stderr)
    def test_runner_shell_syntax(self):
        run=subprocess.run([BASH,'--noprofile','--norc','-n'],input=self.rendered().encode('utf8'),cwd=HERE,capture_output=True,timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
