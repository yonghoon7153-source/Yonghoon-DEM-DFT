"""Exercise two sequential WSL arms with a fake driver and no time steps."""
import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE=Path(__file__).resolve().parent
GO="GO_SUYOUNG_F8_F16_CONTACT_ONCE"
F8="9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
STOP="bdd10395a7acc1aa7e64f7aaa6d8509a343ea448b47ee39e0770f520e310ec6d"
DRIVER="""from pathlib import Path
import sys
mode=sys.argv[1]
args=dict(zip(sys.argv[2::2],sys.argv[3::2]))
if mode!='partial':
    repo=Path(args['--repo'])
    assert (repo/'scripts/suyoung_multicontact_dev.py').read_bytes()==b'test kernel'
def option(k): return Path(args['--'+k])
if mode in ('check','read','check8'): assert option('f8').read_bytes()==b'F8'
if mode in ('check','read'): assert option('stop').read_bytes()==b'STOP'
if mode=='check':
    if (Path.home()/'bad_input').exists(): sys.exit(2)
elif mode=='arm':
    cells=args['--cells']
    assert cells in ('8','16')
    arm=option('out')
    assert arm.name=='F'+cells
    arm.mkdir()
    (arm/'trace.csv').write_text('synthetic '+cells)
    if (Path.home()/('fail'+cells)).exists():
        (arm/'contact_stop.json').write_text('{}')
        sys.exit(4)
    (arm/'candidate.json').write_text('new receipt')
elif mode=='check8':
    assert (option('run')/'F8/candidate.json').read_text()=='new receipt'
    assert (option('run')/'F8/trace.csv').read_text()=='synthetic 8'
    assert not (option('run')/'F16').exists()
    if (Path.home()/'changed_trace8').exists(): sys.exit(4)
elif mode=='partial':
    assert (option('run')/'F16/trace.csv').is_file() and option('stop').read_bytes()==b'STOP'
    if (Path.home()/'bad_diagnostic').exists(): sys.exit(7)
    option('out').write_text('{"common_samples":1}')
elif mode=='read':
    assert all((option('run')/('F'+n)/'candidate.json').is_file() for n in ('8','16'))
    if (Path.home()/'prefix_mismatch').exists(): sys.exit(4)
    if not (Path.home()/'empty').exists():
        option('out').write_bytes(b'{"outcome":"ABOVE_5_PERCENT","stage3_go":false}')
else: sys.exit(2)
"""


@unittest.skipUnless(os.name=="posix","POSIX shell required")
class PairBlock(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        base=Path(t.name)
        self.home,self.pkg=base/"home",base/"pkg"
        self.f8,self.stop=base/"F8 old.tar.gz",base/"F16 stopped.tar.gz"
        self.f8.write_bytes(b"F8"); self.stop.write_bytes(b"STOP")
        d=self.pkg/"docs/reviews/suyoung_u6c_f16_stop_20261122"
        d.mkdir(parents=True)
        self.driver=d/"run_pair.py"
        self.driver.write_text(DRIVER)
        kern=self.pkg/"scripts/suyoung_multicontact_dev.py"
        kern.parent.mkdir()
        kern.write_bytes(b"test kernel")
        sha=lambda b: hashlib.sha256(b).hexdigest()
        sums="".join(sha(p.read_bytes())+"  "+p.relative_to(self.pkg).as_posix()+"\n" for p in (self.driver,kern)).encode()
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        tmpl=(HERE/"run_wsl.in").read_text()
        self.block=self.pkg/"inner.sh"
        for k,v in (("@PIN@","1"*40),("@SOURCE_SUMS@",sha(sums)),("@KERNEL@",sha(kern.read_bytes())),
                    (F8,sha(b"F8")),(STOP,sha(b"STOP"))):
            tmpl=tmpl.replace(k,v)
        self.block.write_text(tmpl)
        bindir=self.home/"Yonghoon-DEM-DFT/venv/bin"
        bindir.mkdir(parents=True)
        def put(n,s):
            p=bindir/n
            p.write_text("#!/bin/sh\n"+s)
            p.chmod(0o700)
        put("python",'if [ "$3" = "-c" ]; then exit 0; fi\nexec '+shlex.quote(sys.executable)+' "$@"\n')
        put("taskset",'[ "$1" = "-c" ] && [ "$2" = "0" ] || exit 89\nshift 2\nexec "$@"\n')
        put("timeout",'''[ "$1" = "--signal=TERM" ] && [ "$2" = "--kill-after=5s" ] || exit 90
case "$3" in 1195s|1795s|115s) ;; *) exit 91 ;; esac
echo "$3" >> "$HOME/timers"
if [ "$3" = "1795s" ] && [ -f "$HOME/watchdog" ]; then exit 124; fi
shift 3
exec "$@"
''')
        self.env=dict(os.environ,HOME=str(self.home),PATH=str(bindir)+":"+os.environ["PATH"])

    def invoke(self,mode=GO):
        return subprocess.run(["bash",str(self.block),mode,str(self.f8),str(self.stop)],env=self.env,
                              capture_output=True,text=True,timeout=20)

    def archive(self):
        r,=self.home.glob("suyoung_contact_pair_return_*")
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=r,check=True,capture_output=True)
        return tarfile.open(r/"suyoung_contact_pair_result.tar.gz")

    def test_check_only_checks_both_inputs_without_reservation_or_execution(self):
        p=self.invoke("CHECK_ONLY")
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("CHECK_OK",p.stdout)
        self.assertFalse(list(self.home.glob("suyoung_contact_pair_*")))
        self.assertFalse((self.home/"timers").exists())

    def test_any_bad_input_and_bad_semantics_refuse_before_reservation(self):
        for target in (self.driver,self.f8,self.stop):
            b=target.read_bytes()
            target.write_bytes(b"changed")
            self.assertNotEqual(self.invoke().returncode,0)
            target.write_bytes(b)
        (self.home/"bad_input").touch()
        self.assertNotEqual(self.invoke().returncode,0)
        self.assertFalse(list(self.home.glob("suyoung_contact_pair_*")))

    def test_complete_pair_checks_f8_before_f16_and_preserves_valid_above_threshold(self):
        p=self.invoke()
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("F8_CHECK_RC=0",p.stdout)
        self.assertIn("READBACK_REQUIRED",p.stdout)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1195s","115s","1795s","115s"])
        with self.archive() as t:
            self.assertIn("run/F8/candidate.json",t.getnames())
            self.assertIn("run/F16/candidate.json",t.getnames())
            self.assertIn(b"ABOVE_5_PERCENT",t.extractfile("run/grid_comparison.json").read())
        self.assertNotEqual(self.invoke().returncode,0)

    def test_f8_stop_skips_f16_and_returns_diagnostics(self):
        (self.home/"fail8").touch()
        self.assertEqual(self.invoke().returncode,4)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1195s"])
        with self.archive() as t:
            self.assertIn("run/F8/contact_stop.json",t.getnames())
            self.assertNotIn("run/F16",t.getnames())

    def test_f8_byte_change_skips_f16(self):
        (self.home/"changed_trace8").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertIn("F8_CHECK_RC=4",p.stdout)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1195s","115s"])
        with self.archive() as t:
            self.assertIn("run/F8/trace.csv",t.getnames())
            self.assertNotIn("run/F16",t.getnames())

    def test_f16_stop_preserves_both_traces(self):
        (self.home/"fail16").touch()
        self.assertEqual(self.invoke().returncode,4)
        with self.archive() as t:
            self.assertIn("run/F8/trace.csv",t.getnames())
            self.assertIn("run/F16/trace.csv",t.getnames())
            self.assertIn("run/F16/contact_stop.json",t.getnames())
            self.assertIn("run/f16_prefix_diagnostic.json",t.getnames())
            self.assertNotIn("run/grid_comparison.json",t.getnames())

    def test_optional_diagnostic_failure_preserves_first_error(self):
        (self.home/"fail16").touch()
        (self.home/"bad_diagnostic").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertIn("F16_PREFIX_DIAGNOSTIC_RC=7",p.stdout)
        with self.archive() as t:
            self.assertIn("run/F16/trace.csv",t.getnames())
            self.assertNotIn("run/grid_comparison.json",t.getnames())

    def test_f16_timeout_returns_original_status(self):
        (self.home/"watchdog").touch()
        self.assertEqual(self.invoke().returncode,124)
        with self.archive() as t:
            self.assertIn(b"command_rc=124",t.extractfile("run/F16.process-stop.txt").read())
            self.assertNotIn("run/grid_comparison.json",t.getnames())

    def test_f16_prefix_mismatch_stops_readback(self):
        (self.home/"prefix_mismatch").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)

    def test_missing_reader_output_is_not_a_success(self):
        (self.home/"empty").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)


if __name__=="__main__":
    unittest.main()
