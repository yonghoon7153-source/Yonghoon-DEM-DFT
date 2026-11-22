"""POSIX packaging checks with a fixture driver instead of a material calculation."""
import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
GO = "GO_SUYOUNG_F8_NODE228_PAIR_ONCE"
WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
ORDER = "8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17"
CAPTURE = "90b070d33e84735008035eb399d648acb6065edfb677653f8db9f3c9c61eca18"
STOP = "a100f018bd5e9c3621395ac436550029759fe17a02a55641db121d52dba1fdbe"
DRIVER = """from pathlib import Path
import sys
if '--help' in sys.argv: sys.exit(0)
args = sys.argv
if args[1] == "check":
    assert Path(args[args.index("--capture")+1]).read_bytes() == b"CAPTURE"
    sys.exit(0)
out = Path(args[args.index('--out')+1])
if args[1] == 'run':
    arm = args[args.index('--mapping')+1]
    assert args[args.index('--budget')+1] == '570'
    out.mkdir()
    (out/'trace.csv').write_text(arm)
    if (Path.home()/('fail_'+arm)).exists():
        print('mock stop: unresolved contact',file=sys.stderr)
        sys.exit(4)
elif args[1] == 'read':
    for key, val in [('--wall',b'WALL'),('--prior-order',b'ORDER')]:
        assert Path(args[args.index(key)+1]).read_bytes() == val
    root = Path(args[args.index('--arms-dir')+1])
    for arm in ('ORIGINAL','REVERSED'):
        assert (root/arm/'trace.csv').read_text() == arm
    out.write_text('synthetic')
    if (Path.home()/'fail_reader').exists(): sys.exit(4)
else: sys.exit(2)
"""


@unittest.skipUnless(os.name == "posix", "POSIX shell block")
class Launcher(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        self.home, self.pkg = base/"home", base/"pkg"
        self.wall, self.order = base/"old wall.tar.gz", base/"old order.tar.gz"
        self.wall.write_bytes(b"WALL")
        self.order.write_bytes(b"ORDER")
        self.capture = base/"capture145.tar.gz"
        self.capture.write_bytes(b"CAPTURE")
        self.stop = base/"stop 228.tar.gz"
        self.stop.write_bytes(b"STOP")
        script = self.pkg/"docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py"
        script.parent.mkdir(parents=True)
        script.write_text(DRIVER)
        wrapped = self.pkg/"docs/reviews/suyoung_u6c_node145_20261122/node145_pair.py"
        wrapped.parent.mkdir(parents=True)
        wrapped.write_text(DRIVER)
        binder = self.pkg/"docs/reviews/suyoung_u6c_node228_20261122/bind_stop228.py"
        binder.parent.mkdir(parents=True)
        binder.write_text("from pathlib import Path\nimport sys\nassert Path(sys.argv[sys.argv.index('--stop')+1]).read_bytes() == b'STOP'\n")
        sums = "".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(self.pkg).as_posix()+"\n"
                       for p in (script, wrapped, binder)).encode("ascii")
        (self.pkg/"SOURCE_SHA256SUMS").write_bytes(sums)
        self.script = script
        self.block = self.pkg/"inner.txt"
        template = (HERE/"run_wsl.in").read_text()
        for key, value in (("@PIN@", "a"*40), ("@SOURCE_SUMS@", hashlib.sha256(sums).hexdigest()),
                           (STOP, hashlib.sha256(b"STOP").hexdigest()), (CAPTURE, hashlib.sha256(b"CAPTURE").hexdigest()), (WALL, hashlib.sha256(b"WALL").hexdigest()), (ORDER, hashlib.sha256(b"ORDER").hexdigest())):
            template = template.replace(key, value)
        self.block.write_text(template)
        bindir = self.home/"Yonghoon-DEM-DFT/venv/bin"
        bindir.mkdir(parents=True)
        fakepy = bindir/"python"
        fakepy.write_text('#!/bin/sh\nif [ "$3" = "-c" ]; then exit 0; fi\nexec '+shlex.quote(sys.executable)+' "$@"\n')
        fakepy.chmod(0o700)
        taskset = bindir/"taskset"
        taskset.write_text('#!/bin/sh\n[ "$1" = "-c" ] && [ "$2" = "0" ] || exit 2\nshift 2\nexec "$@"\n')
        taskset.chmod(0o700)
        timeout = bindir/"timeout"
        timeout.write_text("""#!/bin/sh
[ "$1" = "--signal=TERM" ] && [ "$2" = "--kill-after=5s" ] || exit 71
case "$3" in 595s|115s) ;; *) exit 72 ;; esac
echo "$3" >> "$HOME/bounds"
shift 3
exec "$@"
""")
        timeout.chmod(0o700)
        self.env = dict(os.environ, HOME=str(self.home), PATH=str(bindir)+":"+os.environ["PATH"])

    def run_block(self, mode=GO):
        return subprocess.run(["bash",str(self.block),mode,str(self.wall),str(self.order),str(self.capture),str(self.stop)],
                              env=self.env,capture_output=True,text=True,timeout=25)

    def returned(self):
        ret, = self.home.glob("suyoung_node228_return_*")
        subprocess.run(["sha256sum","-c","SHA256SUMS"],cwd=ret,check=True,capture_output=True)
        return tarfile.open(ret/"suyoung_node228_result.tar.gz")

    def test_check_only_verifies_without_reservation(self):
        p = self.run_block("CHECK_ONLY")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("CHECK_OK", p.stdout)
        self.assertFalse(list(self.home.glob("suyoung_node228_*")))

    def test_both_prior_identities_and_sources_before_reservation(self):
        for target in (self.wall,self.order,self.capture,self.stop,self.script):
            data = target.read_bytes()
            target.write_bytes(b"bad")
            self.assertNotEqual(self.run_block().returncode, 0)
            self.assertFalse(list(self.home.glob("suyoung_node228_*")))
            target.write_bytes(data)

    def test_full_pair_once(self):
        p = self.run_block()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("F8_ORIGINAL_RC=0",p.stdout)
        self.assertIn("F8_REVERSED_RC=0",p.stdout)
        self.assertEqual((self.home/"bounds").read_text().splitlines(), ["595s","595s","115s"])
        with self.returned() as tar:
            self.assertIn("run/comparison.json",tar.getnames())
            origin = dict(line.split("=", 1) for line in
                          tar.extractfile("run/origin.txt").read().decode().splitlines())
            self.assertEqual(origin["release"], "a"*40)
            self.assertEqual(origin["source_sums"], hashlib.sha256((self.pkg/"SOURCE_SHA256SUMS").read_bytes()).hexdigest())
            self.assertEqual(origin["prior_wall"], hashlib.sha256(self.wall.read_bytes()).hexdigest())
            self.assertEqual(origin["prior_stop228"],hashlib.sha256(self.stop.read_bytes()).hexdigest())
            self.assertEqual(origin["prior_capture"],hashlib.sha256(self.capture.read_bytes()).hexdigest())
            self.assertEqual(origin["prior_order"], hashlib.sha256(self.order.read_bytes()).hexdigest())
            self.assertEqual((origin["CPU"], origin["per_arm_hard_s"]), ("0","600"))
            self.assertRegex(origin["started_utc"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertTrue((self.home/("suyoung_node228_pair_once_"+"a"*12)/"receipt.txt").is_file())
        self.assertNotEqual(self.run_block().returncode, 0)

    def test_first_arm_failure_second_unrun_and_stderr_retained(self):
        (self.home/"fail_ORIGINAL").touch()
        self.assertEqual(self.run_block().returncode, 4)
        with self.returned() as tar:
            self.assertIn(b"unresolved contact", tar.extractfile("run/ORIGINAL.log").read())
            self.assertIn("run/ORIGINAL/trace.csv",tar.getnames())
            self.assertIn("run/ORIGINAL.process-stop.txt",tar.getnames())
            self.assertIn(b"command_rc=4",tar.extractfile("run/ORIGINAL.process-stop.txt").read())
            self.assertEqual((self.home/"bounds").read_text().splitlines(), ["595s"])
            self.assertNotIn("run/REVERSED", tar.getnames())
            self.assertNotIn("run/comparison.json", tar.getnames())

    def test_second_arm_failure_preserves_both_traces(self):
        (self.home/"fail_REVERSED").touch()
        self.assertEqual(self.run_block().returncode, 4)
        with self.returned() as tar:
            self.assertIn("run/ORIGINAL/trace.csv",tar.getnames())
            self.assertIn("run/REVERSED/trace.csv",tar.getnames())
            self.assertNotIn("run/comparison.json",tar.getnames())

    def test_reader_failure_preserves_partial_return(self):
        (self.home/"fail_reader").touch()
        p = self.run_block()
        self.assertEqual(p.returncode, 4)
        self.assertIn("SUMMARY_RC=4",p.stdout)
        self.assertNotIn("READBACK_REQUIRED",p.stdout)
        with self.returned() as tar:
            self.assertIn("run/comparison.json",tar.getnames())


if __name__ == "__main__":
    unittest.main()
