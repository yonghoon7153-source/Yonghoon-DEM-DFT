"""Expected-correct CLI regressions. Mutations are made only in temporary copies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


def change_json(path, **updates):
    data = json.loads(path.read_bytes())
    data.update(updates)
    path.write_text(json.dumps(data, sort_keys=True), encoding="utf-8")


def change_final_pressure(path):
    rows = path.read_bytes().splitlines(keepends=True)
    fields = rows[-1].split(b",")
    fields[3] = b"0.18"
    rows[-1] = b",".join(fields)
    path.write_bytes(b"".join(rows))


class BindingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.data = Path(temp.name) / "data"
        shutil.copytree(args.data, self.data)

    def run_reader(self):
        return subprocess.run([sys.executable, "-I", "-B", str(args.reader), "--data", str(self.data)],
                              check=False, capture_output=True, text=True)

    def rejected(self):
        run = self.run_reader()
        self.assertNotEqual(run.returncode, 0, "altered input accepted")
        self.assertEqual(run.stdout, "", "a partial numerical result was printed")

    def test_clean_reference_output_is_unchanged(self):
        run = self.run_reader()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.encode("ascii"), args.expected.read_bytes())

    def test_review_f8_terminal_pressure(self):
        change_final_pressure(self.data / "full/F8/trace.csv")
        self.rejected()

    def test_f16_terminal_pressure_beyond_common_displacements(self):
        change_final_pressure(self.data / "full/F16/trace.csv")
        self.rejected()

    def test_complete_coherently_rehashed_receipts_and_comparison(self):
        arm = self.data / "full/F8"
        trace = arm / "trace.csv"
        change_final_pressure(trace)
        h = hashlib.sha256(trace.read_bytes()).hexdigest()
        change_json(arm / "result.json", trace_sha256=h)
        change_json(arm / "candidate.json", trace_sha256=h,
                    native_result_sha256=hashlib.sha256((arm / "result.json").read_bytes()).hexdigest())
        summary = self.data / "full/grid_comparison.json"
        obj = json.loads(summary.read_bytes())
        obj["receipts"]["F8"] = json.loads((arm / "candidate.json").read_bytes())
        summary.write_text(json.dumps(obj), encoding="ascii")
        self.rejected()

    def test_result_receipt_must_exist(self):
        (self.data / "full/F8/result.json").unlink()
        self.rejected()

    def test_candidate_receipt_must_exist(self):
        (self.data / "full/F16/candidate.json").unlink()
        self.rejected()

    def test_terminal_step_identity(self):
        change_json(self.data / "full/F8/result.json", steps=2658)
        self.rejected()

    def test_kernel_identity(self):
        change_json(self.data / "full/F16/candidate.json", kernel_sha256="0" * 64)
        self.rejected()

    def test_arm_completion_status(self):
        change_json(self.data / "full/F16/candidate.json", status="INCOMPLETE")
        self.rejected()

    def test_prefix_and_full_kernel_must_agree(self):
        change_json(self.data / "prefix/F8/prefix_receipt.json", kernel_sha256="f" * 64)
        self.rejected()

    def test_pair_receipt_identity(self):
        change_json(self.data / "full/grid_comparison.json", status="INCOMPLETE")
        self.rejected()


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--reader", type=Path, required=True)
    cli.add_argument("--data", type=Path, required=True)
    cli.add_argument("--expected", type=Path, required=True)
    args, rest = cli.parse_known_args()
    unittest.main(argv=[sys.argv[0]] + rest)
