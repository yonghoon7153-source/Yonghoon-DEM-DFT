"""Synthetic WSL wrapper: no plate evolution or time steps."""
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
GO="GO_SUYOUNG_WALL_PREFIX_ONCE"
PRIOR="fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"
DRIVER="""from pathlib import Path
import sys
mode=sys.argv[1]
kw=dict(zip(sys.argv[2::2],sys.argv[3::2]))
root=Path(kw['--repo'])
src=root/'scripts/suyoung_multicontact_dev.py'
prior=Path(kw['--prior'])
assert src.read_bytes()==b'kernel' and prior.read_bytes()==b'PAIR'
if mode=='check':
    if (Path.home()/'invalid').exists(): sys.exit(2)
elif mode=='arm':
    cells=kw['--cells']
    assert cells in ('8','16')
    out=Path(kw['--out'])
    assert out.name=='F'+cells
    out.mkdir()
    (out/'wall_rows.csv').write_text('synthetic')
    if (Path.home()/('fail'+cells)).exists(): sys.exit(4)
elif mode=='read':
    run=Path(kw['--run'])
    assert all((run/('F'+n)/'wall_rows.csv').is_file() for n in ('8','16'))
    if (Path.home()/'readfail').exists(): sys.exit(2)
    if (Path.home()/'changed_source').exists(): src.write_bytes(b'drift')
    if (Path.home()/'changed_prior').exists(): prior.write_bytes(b'drift')
    if not (Path.home()/'empty').exists():
        Path(kw['--out']).write_text('{"observation_only":true}')
else: sys.exit(2)
"""


@unittest.skipUnless(os.name=="posix","POSIX shell")
class Prefix(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        base=Path(t.name)
        self.pkg,self.home=base/"pkg",base/"home"
        dp=self.pkg/"docs/reviews/suyoung_first_grid_return_20261122"
        dp.mkdir(parents=True)
        self.driver=dp/"observe_prefix.py"
        self.driver.write_text(DRIVER)
        self.prior=base/"pair input.tar.gz"
        self.prior.write_bytes(b"PAIR")
        self.kernel=self.pkg/"scripts/suyoung_multicontact_dev.py"
        self.kernel.parent.mkdir()
        self.kernel.write_bytes(b"kernel")
        sha=lambda b:hashlib.sha256(b).hexdigest()
        sums="".join(sha(f.read_bytes())+"  "+f.relative_to(self.pkg).as_posix()+"\n"
                     for f in (self.driver,self.kernel)).encode()
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        block=(HERE/"run_wsl.in").read_text()
        for tag,v in (("@PIN@","f"*40),("@SOURCE_SUMS@",sha(sums)),("@KERNEL@",sha(b"kernel")),(PRIOR,sha(b"PAIR"))):
            block=block.replace(tag,v)
        self.block=self.pkg/"inner.sh"
        self.block.write_text(block)
        bindir=self.home/"Yonghoon-DEM-DFT/venv/bin"
        bindir.mkdir(parents=True)
        def put(name,s):
            p=bindir/name
            p.write_text("#!/bin/sh\n"+s)
            p.chmod(0o700)
        put("python",'if [ "$3" = "-c" ]; then exit 0; fi\nexec '+shlex.quote(sys.executable)+' "$@"\n')
        put("taskset",'[ "$1" = "-c" ] && [ "$2" = 0 ] || exit 79\nshift 2\nexec "$@"\n')
        put("timeout",'''[ "$1" = "--signal=TERM" ] && [ "$2" = "--kill-after=5s" ] || exit 81
case "$3" in 295s|115s) ;; *) exit 82;; esac
echo "$3" >> "$HOME/timers"
if [ -e "$HOME/watchdog" ] && [ "$3" = "295s" ]; then exit 124; fi
shift 3
exec "$@"
''')
        self.env=dict(os.environ,HOME=str(self.home),PATH=str(bindir)+":"+os.environ["PATH"])

    def invoke(self,mode=GO):
        return subprocess.run(["bash",str(self.block),mode,str(self.prior)],env=self.env,capture_output=True,
                              text=True,timeout=20)

    def archive(self):
        ret,=self.home.glob("suyoung_wall_prefix_return_*")
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=ret,check=True,capture_output=True)
        return tarfile.open(ret/"suyoung_wall_prefix_result.tar.gz")

    def test_check_without_reservation(self):
        p=self.invoke("CHECK_ONLY")
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("CHECK_OK",p.stdout)
        self.assertFalse((self.home/"timers").exists())
        self.assertFalse(list(self.home.glob("suyoung_wall_prefix_*")))

    def test_bad_source_archive_or_semantics(self):
        for path in (self.kernel,self.prior,self.driver):
            old=path.read_bytes()
            path.write_bytes(b"altered")
            self.assertNotEqual(self.invoke().returncode,0)
            path.write_bytes(old)
        (self.home/"invalid").touch()
        self.assertNotEqual(self.invoke().returncode,0)
        self.assertFalse(list(self.home.glob("suyoung_wall_prefix_*")))

    def test_complete_with_both_300_second_limits_and_one_shot(self):
        p=self.invoke()
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("READBACK_REQUIRED",p.stdout)
        self.assertIn("SOURCE_AND_PRIOR_STILL_MATCH",p.stdout)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["295s","295s","115s"])
        with self.archive() as a:
            self.assertIn("run/summary.json",a.getnames())
            self.assertIn(b"F8_steps=270\nF16_steps=540\nper_arm_hard_s=300",a.extractfile("run/origin.txt").read())
        self.assertNotEqual(self.invoke().returncode,0)

    def test_f8_failure_skips_f16(self):
        (self.home/"fail8").touch()
        self.assertEqual(self.invoke().returncode,4)
        with self.archive() as a:
            self.assertIn("run/F8/wall_rows.csv",a.getnames())
            self.assertNotIn("run/F16",a.getnames())

    def test_f16_failure_returns_its_rows_and_no_summary(self):
        (self.home/"fail16").touch()
        self.assertEqual(self.invoke().returncode,4)
        with self.archive() as a:
            self.assertIn("run/F16/wall_rows.csv",a.getnames())
            self.assertNotIn("run/summary.json",a.getnames())

    def test_timeout_is_terminal(self):
        (self.home/"watchdog").touch()
        self.assertEqual(self.invoke().returncode,124)
        with self.archive() as a:
            self.assertIn(b"command_rc=124",a.extractfile("run/F8.process-stop.txt").read())
            self.assertNotIn("run/F16",a.getnames())

    def test_reader_failure_retains_observed_arms(self):
        (self.home/"readfail").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,2,p.stderr)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)
        with self.archive() as a:
            self.assertIn("run/F8/wall_rows.csv",a.getnames())
            self.assertIn("run/F16/wall_rows.csv",a.getnames())

    def test_empty_summary_is_failure(self):
        (self.home/"empty").touch()
        self.assertEqual(self.invoke().returncode,4)

    def test_drift_in_prior_invalidates_readback(self):
        (self.home/"changed_prior").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertIn("SOURCE_OR_PRIOR_CHANGED",p.stdout)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)

    def test_drift_in_package_invalidates_readback(self):
        (self.home/"changed_source").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,4,p.stderr)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)


if __name__=="__main__":
    unittest.main()
