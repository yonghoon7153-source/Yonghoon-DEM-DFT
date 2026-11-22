"""Exercise the author shell with an artificial capture command and temporary HOME."""
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
GO = "GO_SUYOUNG_CAPTURE_145_ONCE"
EXPECTED = "c39bbd65d1c0caa5825abc8095611a8d20a8168e5464db3cd2a05743e3abbbeb"
FAKE = """from pathlib import Path
import sys
if '--help' in sys.argv:
    sys.exit(0)
assert len(sys.argv) == 7 and set(sys.argv[1::2]) == {'--out','--prior','--source-dir'}
assert Path(sys.argv[sys.argv.index('--prior')+1]).read_bytes() == b'stopped'
target = Path(sys.argv[sys.argv.index('--out')+1])
target.mkdir()
(target/'failing_nodes.json').write_text('nodes')
if (Path.home()/'fail').exists():
    print('simulated unexpected stop',file=sys.stderr)
    sys.exit(4)
if not (Path.home()/'missing').exists():
    (target/'capture_receipt.json').write_text('receipt')
"""


@unittest.skipUnless(os.name == "posix", "Requires POSIX shell tools")
class CaptureBlock(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.home = root/"synthetic home"
        self.pkg = root/"package"
        self.input = root/"prior tar"
        self.input.write_bytes(b"stopped")
        self.tool = self.pkg/"docs/reviews/suyoung_u6c_step145_20261122/capture_stop.py"
        self.tool.parent.mkdir(parents=True)
        self.tool.write_text(FAKE)
        data = hashlib.sha256(self.tool.read_bytes()).hexdigest() + "  " + self.tool.relative_to(self.pkg).as_posix() + "\n"
        manifest = self.pkg/"SOURCE_SHA256SUMS"
        manifest.write_text(data)
        self.pin = "4"*40
        self.sha = hashlib.sha256(self.input.read_bytes()).hexdigest()
        self.source = hashlib.sha256(manifest.read_bytes()).hexdigest()
        block = (HERE/"capture_wsl.in").read_text()
        self.block = self.pkg/"go"
        self.block.write_text(block.replace("@PIN@", self.pin).replace("@SUMS@", self.source).replace(EXPECTED, self.sha))
        bin_dir = self.home/"Yonghoon-DEM-DFT/venv/bin"
        bin_dir.mkdir(parents=True)
        py = bin_dir/"python"
        py.write_text('#!/bin/sh\nif [ "$3" = "-c" ]; then exit 0; fi\nexec ' + shlex.quote(sys.executable) + ' "$@"\n')
        task = bin_dir/"taskset"
        task.write_text('#!/bin/sh\n[ "$1" = "-c" ] && [ "$2" = "0" ] || exit 2\nshift 2\nexec "$@"\n')
        for path in (py, task):
            path.chmod(0o700)
        self.env = dict(os.environ, HOME=str(self.home), PATH=str(bin_dir) + ":" + os.environ["PATH"])

    def block_run(self, mode=GO):
        return subprocess.run(["bash",str(self.block),mode,str(self.input)], env=self.env,
                              capture_output=True, text=True, timeout=15)

    def returned(self):
        folder, = self.home.glob("suyoung_capture145_return_*")
        subprocess.run(["sha256sum", "-c", "SHA256SUMS"], cwd=folder, check=True, capture_output=True)
        return tarfile.open(folder/"suyoung_capture145_result.tar.gz")

    def test_check_only_and_wrong_mode_leave_no_reservation(self):
        self.assertIn("CHECK_OK", self.block_run("CHECK_ONLY").stdout)
        self.assertNotEqual(self.block_run("other").returncode, 0)
        self.assertFalse(list(self.home.glob("suyoung_capture145_*")))

    def test_changed_source_or_prior_cannot_start(self):
        for path in (self.input, self.tool):
            data = path.read_bytes()
            path.write_bytes(b"changed")
            self.assertNotEqual(self.block_run().returncode, 0)
            self.assertFalse(list(self.home.glob("suyoung_capture145_*")))
            path.write_bytes(data)

    def test_success_checksums_and_duplicate_same_pin(self):
        p = self.block_run()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("CAPTURED_STEP_145", p.stdout)
        with self.returned() as z:
            self.assertEqual(z.extractfile("run/capture/failing_nodes.json").read(), b"nodes")
            self.assertEqual(z.extractfile("run/capture/capture_receipt.json").read(), b"receipt")
            origin = dict(row.split("=",1) for row in z.extractfile("run/origin.txt").read().decode().splitlines())
            self.assertEqual((origin["release"],origin["prior_failure"],origin["source_sums"],origin["cpu"],origin["hard_s"]),
                             (self.pin,self.sha,self.source,"0","150"))
        self.assertEqual(self.block_run().returncode, 2)
        self.assertEqual(len(list(self.home.glob("suyoung_capture145_return_*"))), 1)

    def test_partial_failure_returns_stderr_and_partial_data(self):
        (self.home/"fail").touch()
        self.assertEqual(self.block_run().returncode, 4)
        with self.returned() as z:
            self.assertIn(b"simulated unexpected stop", z.extractfile("run/capture.log").read())
            self.assertIn("run/capture/failing_nodes.json", z.getnames())
            self.assertNotIn("run/capture/capture_receipt.json", z.getnames())

    def test_rc0_without_receipt_rejected(self):
        (self.home/"missing").touch()
        p = self.block_run()
        self.assertEqual(p.returncode, 4)
        self.assertIn("CAPTURE_OUTPUT_MISSING", p.stdout)
        with self.returned() as z:
            self.assertIn("run/capture.log", z.getnames())


if __name__ == "__main__":
    unittest.main()
