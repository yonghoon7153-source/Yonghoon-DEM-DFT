"""POSIX shell tests with a synthetic author home, reader and driver. No time integration."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GO = "GO_SUYOUNG_F16_CONTACT_ONCE"
F8 = "9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
KERNEL = "8af03f07e8149219a13baa1d1ca79c2fc87940bb991c6055769ac0beeb3a8880"
DRIVER = """from pathlib import Path
import sys
if sys.argv[1]=='check-setup':
    assert sys.argv[2]=='--repo' and (Path(sys.argv[3])/'RELEASE').exists()
    print('F16_SETUP_MOCK')
    sys.exit(2 if (Path.home()/'failed_setup').exists() else 0)
assert sys.argv[1] == 'run'
args=dict(zip(sys.argv[2::2],sys.argv[3::2]))
assert args['--budget']=='1740' and (Path(args['--repo'])/'RELEASE').exists()
out=Path(args['--out'])
assert out.name=='F16'
out.mkdir()
(out/'trace.csv').write_text('synthetic trace')
if (Path.home()/'stop_arm').exists():
    (out/'incomplete.json').write_text('{"status":"TIME_LIMIT"}')
    sys.exit(4)
"""
READER = """from pathlib import Path
import sys
def arg(k): return sys.argv[sys.argv.index(k)+1]
assert Path(arg('--f8')).read_bytes()==b'F8'
assert (Path(arg('--repo'))/'RELEASE').exists()
if '--check-f8' in sys.argv:
    sys.exit(2 if (Path.home()/'failed_precheck').exists() else 0)
assert (Path(arg('--f16'))/'trace.csv').read_bytes()==b'synthetic trace'
if (Path.home()/'bad_reader').exists():
    print('synthetic invalid completed arm',file=sys.stderr)
    sys.exit(2)
if not (Path.home()/'empty').exists():
    Path(arg('--out')).write_bytes(b'{"assessment":"ABOVE_5_PERCENT","stage3_go":false}')
"""


@unittest.skipUnless(os.name=="posix","POSIX shell")
class Block(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        base=Path(t.name)
        self.home,self.pkg=base/"home",base/"pkg"
        self.f8=base/"candidate F8.tar.gz"
        self.f8.write_bytes(b"F8")
        folder=self.pkg/"docs/reviews/suyoung_u6c_updated_f16_20261122"
        folder.mkdir(parents=True)
        self.driver=folder/"f16_candidate.py"
        self.driver.write_text(DRIVER)
        reader=folder/"read_f8_f16.py"
        reader.write_text(READER)
        kernel=self.pkg/"scripts/suyoung_multicontact_dev.py"
        kernel.parent.mkdir()
        kernel.write_bytes(b"fixture kernel")
        release=self.pkg/"RELEASE"
        release.write_text("fixture")
        sha=lambda b:hashlib.sha256(b).hexdigest()
        manifest="".join(sha(p.read_bytes())+"  "+p.relative_to(self.pkg).as_posix()+"\n"
                         for p in (self.driver,reader,kernel,release)).encode("ascii")
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(manifest)
        block=(HERE/"run_wsl.in").read_text().replace("@PIN@","a"*40).replace("@SOURCE_SUMS@",sha(manifest))
        self.block=self.pkg/"inner.txt"
        self.block.write_text(block.replace(KERNEL,sha(kernel.read_bytes())).replace(F8,sha(b"F8")))
        bindir=self.home/"Yonghoon-DEM-DFT/venv/bin"
        bindir.mkdir(parents=True)
        def put(name,script):
            path=bindir/name
            path.write_text("#!/bin/sh\n"+script)
            path.chmod(0o700)
        put("python",'if [ "$3" = "-c" ]; then exit 0; fi\nexec '+shlex.quote(sys.executable)+' "$@"\n')
        put("taskset",'[ "$1" = "-c" ] && [ "$2" = "0" ] || exit 89\nshift 2\nexec "$@"\n')
        put("timeout",'''[ "$1" = "--signal=TERM" ] && [ "$2" = "--kill-after=5s" ] || exit 91
case "$3" in 1795s|115s) ;; *) exit 92 ;; esac
echo "$3" >> "$HOME/timers"
if [ "$3" = "1795s" ] && [ -f "$HOME/watchdog" ]; then exit 124; fi
shift 3
exec "$@"
''')
        self.env=dict(os.environ,HOME=str(self.home),PATH=str(bindir)+":"+os.environ["PATH"])

    def invoke(self,mode=GO):
        return subprocess.run(["bash",str(self.block),mode,str(self.f8)],env=self.env,
                              capture_output=True,text=True,timeout=20)

    def returned(self):
        ret,=self.home.glob("suyoung_f16_contact_return_*")
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=ret,check=True,capture_output=True)
        return tarfile.open(ret/"suyoung_f16_contact_result.tar.gz","r:gz")

    def test_check_only_never_reserves_or_runs(self):
        p=self.invoke("CHECK_ONLY")
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("CHECK_OK",p.stdout)
        self.assertIn("F16_SETUP_MOCK",p.stdout)
        self.assertFalse(list(self.home.glob("suyoung_f16_contact_*")))
        self.assertFalse((self.home/"timers").exists())

    def test_prior_source_and_semantic_check_fail_before_reservation(self):
        for p in (self.driver,self.f8):
            old=p.read_bytes()
            p.write_bytes(b"bad")
            self.assertNotEqual(self.invoke().returncode,0)
            p.write_bytes(old)
        for name in ("failed_precheck","failed_setup"):
            flag=self.home/name
            flag.touch()
            self.assertNotEqual(self.invoke().returncode,0)
            flag.unlink()
        self.assertFalse(list(self.home.glob("suyoung_f16_contact_*")))

    def test_above_five_is_valid_return_once(self):
        p=self.invoke()
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertIn("READBACK_REQUIRED",p.stdout)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1795s","115s"])
        with self.returned() as t:
            row=json.load(t.extractfile("run/grid_comparison.json"))
            self.assertEqual(row["assessment"],"ABOVE_5_PERCENT")
            self.assertFalse(row["stage3_go"])
            self.assertIn(b"arm_budget_s=1740\nper_arm_hard_s=1800\n",t.extractfile("run/origin.txt").read())
        self.assertNotEqual(self.invoke().returncode,0)
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1795s","115s"])

    def test_incomplete_arm_keeps_partial_trace_no_reader(self):
        (self.home/"stop_arm").touch()
        self.assertEqual(self.invoke().returncode,4)
        with self.returned() as t:
            self.assertIn("run/F16/incomplete.json",t.getnames())
            self.assertIn("run/F16/trace.csv",t.getnames())
            self.assertIn(b"command_rc=4",t.extractfile("run/F16_process_stop.txt").read())
            self.assertNotIn("run/grid_comparison.json",t.getnames())
        self.assertEqual((self.home/"timers").read_text().splitlines(),["1795s"])

    def test_outer_timeout_preserved_as_technical_stop(self):
        (self.home/"watchdog").touch()
        self.assertEqual(self.invoke().returncode,124)
        with self.returned() as t:
            self.assertIn(b"command_rc=124",t.extractfile("run/F16_process_stop.txt").read())
            self.assertNotIn("run/grid_comparison.json",t.getnames())

    def test_reader_error_keeps_arm_but_no_readback_success(self):
        (self.home/"bad_reader").touch()
        p=self.invoke()
        self.assertEqual(p.returncode,2,p.stderr)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)
        with self.returned() as t:
            self.assertIn("run/F16/trace.csv",t.getnames())
            self.assertIn(b"synthetic invalid",t.extractfile("run/summary.log").read())

    def test_empty_reader_output_refuses_success(self):
        (self.home/"empty").touch()
        self.assertEqual(self.invoke().returncode,4)
        with self.returned() as t:
            self.assertNotIn("run/grid_comparison.json",t.getnames())


if __name__=="__main__":
    unittest.main()
