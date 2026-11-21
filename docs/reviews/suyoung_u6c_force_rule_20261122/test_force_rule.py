"""Test the frozen dense-contact force-curve rule on synthetic curves."""
import importlib.util
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


class ForceRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("dense_force_rule", HERE / "force_rule.py")
        cls.rule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.rule)

    def test_exact_limit_and_two_sides(self):
        fine = [(0., 0.), (1., 20.)]
        for last, status in ((math.nextafter(21., 20.), "WITHIN"),
                             (21., "WITHIN"), (math.nextafter(21., 22.), "EXCEEDS")):
            with self.subTest(last=last):
                r = self.rule.compare([(0., 0.), (1., last)], fine)
                self.assertEqual(r["comparison"], status)
                self.assertEqual(r["exceeding_knots"], int(status == "EXCEEDS"))
        self.assertEqual(self.rule.compare([(0., 0.), (1., 21.)], fine)["ratio"], .05)

    def test_fine_reference_denominator_on_common_support_only(self):
        fine = [(0., 0.), (.5, 10.), (1., 40.)]
        coarse = [(0., 0.), (.5, 11.)]
        r = self.rule.compare(coarse, fine)
        self.assertEqual(r["fine_peak_MPa"], 10.)
        self.assertEqual(r["comparison"], "EXCEEDS")
        self.assertEqual(r["ratio"], .1)
        self.assertEqual(r["common_end_u"], .5)

    def test_interior_peak_in_finer_trace_and_union(self):
        coarse = [(0., 0.), (.25, 1.), (1., 4.)]
        fine = [(0., 0.), (.5, 8.), (1., 4.)]
        r = self.rule.compare(coarse, fine)
        self.assertEqual(r["max_abs_difference_MPa"], 6.)
        self.assertEqual(r["fine_peak_MPa"], 8.)
        self.assertEqual(r["u_at_first_max_abs"], .5)
        self.assertEqual(r["union_knots"], 4)
        self.assertEqual(r["exceeding_knots"], 2)

    def test_end_between_fine_knots(self):
        r = self.rule.compare([(0., 0.), (.5, 5.)], [(0., 0.), (1., 8.)])
        self.assertEqual((r["ratio"], r["fine_peak_MPa"]), (.25, 4.))
        self.assertEqual(r["fine_samples_in_common"], 1)

    def test_zero_reference_is_indeterminate(self):
        fine = [(0., 0.), (1., 0.)]
        for coarse in (fine, [(0., 0.), (1., 1.)]):
            result = self.rule.compare(coarse, fine)
            self.assertEqual(result["comparison"], "HOLD")
            self.assertIsNone(result["ratio"])
            self.assertIsNone(result["exceeding_knots"])

    def test_corrupt_or_duplicate_samples(self):
        fine = [(0., 0.), (1., 1.)]
        for bad in ([(0., 0.), (0., .5)], [(0., math.nan), (1., 1.)],
                    [(0., 0.), (1., -.1)], [(1., .5)], []):
            with self.subTest(bad=bad):
                self.assertEqual(self.rule.compare(bad, fine)["comparison"], "HOLD")

    def test_identical_linear_interpolants(self):
        r = self.rule.compare([(0., 0.), (.5, .5), (1., 1.)], [(0., 0.), (.25, .25), (1., 1.)])
        self.assertEqual((r["comparison"], r["ratio"], r["union_knots"]), ("WITHIN", 0., 4))

    def test_both_pairs_required_and_exceedance_preserved(self):
        good = {"comparison": "WITHIN"}
        bad = {"comparison": "EXCEEDS"}
        held = {"comparison": "HOLD"}
        p, q = self.rule.PAIRS
        self.assertEqual(self.rule.aggregate({p:good, q:good}), "WITHIN")
        self.assertEqual(self.rule.aggregate({p:good}), "HOLD")
        self.assertEqual(self.rule.aggregate({p:good, q:held}), "HOLD")
        self.assertEqual(self.rule.aggregate({p:bad, q:held}), "EXCEEDS")
        self.assertEqual(self.rule.aggregate({p:good, q:bad}), "EXCEEDS")

    def test_wrong_or_missing_archive_holds_without_qualification(self):
        with tempfile.TemporaryDirectory() as folder:
            archive = Path(folder) / "return.tar.gz"
            for write_invalid in (False, True):
                if write_invalid:
                    archive.write_bytes(b"test ZIP")
                report = self.rule.replay(archive)
                self.assertEqual(report["historical_comparison"], "HOLD")
                self.assertEqual(report["qualification"], "HOLD")
                self.assertFalse(report["stage3_go"])
                self.assertFalse(report["qualification_tested"])
                self.assertIn("reason", report)

    def test_changed_contract_cannot_tag_a_different_rule(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "rule.json").write_text("{}", encoding="ascii")
            with patch.object(self.rule, "HERE", root):
                report = self.rule.replay(root / "unused.tar.gz")
            self.assertEqual(report["reason"], "FROZEN_RULE_MISMATCH")
            self.assertEqual(report["qualification"], "HOLD")

    def test_full_historical_within_cannot_issue_qualification(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "test.tar.gz"
            protocol = "test"
            sha = lambda data: hashlib.sha256(data).hexdigest()
            trace = b"step,time_code,height,bottom_pressure_E,phi_m\n0,0,1,0,.2\n1,.2,.9,.1,.3\n"
            files = {"run/origin.txt": ("release=" + self.rule.curves.SOURCE).encode()}
            inputs = {}
            for cells in (8, 16, 12, 24):
                name = "F"+str(cells)
                receipt = {"arm":"F", "cells":cells, "protocol":protocol, "setting":1,
                           "label":"DEVELOPMENT_ONLY", "status":"TARGET_BRACKETED", "steps":1,
                           "origin":"new", "trace_sha256":sha(trace)}
                inputs[name] = receipt
                files[f"run/arms/{name}/result.json"] = json.dumps(receipt).encode()
                files[f"run/arms/{name}/trace.csv"] = trace
            summary_raw = json.dumps({"inputs":inputs, "protocol":protocol}).encode()
            files["run/summary.json"] = summary_raw
            with tarfile.open(output, "w:gz") as archive:
                for path, data in files.items():
                    info = tarfile.TarInfo(path)
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
            with patch.object(self.rule.curves, "ARCHIVE_DIGEST", sha(output.read_bytes())), \
                 patch.object(self.rule, "SUMMARY_SHA256", sha(summary_raw)):
                report = self.rule.replay(output)
            self.assertEqual(report["historical_comparison"], "WITHIN")
            self.assertFalse(report["qualification_tested"])
            self.assertFalse(report["stage3_go"])
            self.assertEqual(report["qualification"], "HOLD")


if __name__ == "__main__":
    unittest.main()
