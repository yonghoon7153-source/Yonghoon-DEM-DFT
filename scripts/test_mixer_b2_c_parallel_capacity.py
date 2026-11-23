"""Offline capacity and scheduler-evidence tests for one overlapping B2-C."""
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


MODULE = runpy.run_path(str(Path(__file__).with_name("mixer_b2_c_parallel_capacity.py")))
CASE = "/run/u/B/docs/reviews/mixer_first8_launch_preparation_20261106/cases/PRECAL_R1_B2_U"
U = f"368758|runner.sbatch|RUNNING|20|cpu-60|cpu|{CASE}"
UB = "368469|ps73_UB|RUNNING|6|cpu-60|cpu|/run/unloading/UB"


class Capacity(unittest.TestCase):
    def count(self, rows):
        return MODULE["queue_budget"]("\n".join(rows), CASE)

    def test_author_screen_includes_unloading_cpus(self):
        self.assertEqual(self.count([U, UB]), (26, 1))

    def test_existing_serial_policy_rejects_the_same_live_snapshot(self):
        serial = MODULE["base"]["preflight"]
        raw = {"queue": U + "\n" + UB, "df": "", "inode": "", "ost": "", "quota": "",
               "qos": "cpu-60|cpu=60|", "assoc": "author|cpu-60|3-00:00:00|",
               "partition": "State=UP MaxTime=3-00:00:00"}
        with patch.dict(os.environ, USER="author"), patch.dict(
                serial.__globals__, capture=lambda _, label, *args: (raw[label], {}),
                runtime=lambda *args: {"matches": True}, storage_ok=lambda *args: {}):
            with self.assertRaisesRegex(ValueError, "CPU/concurrency budget"):
                serial(Path("synthetic"), None, None, None)

    def test_u_can_leave_queue(self):
        self.assertEqual(self.count([UB]), (6, 0))
        self.assertEqual(self.count([]), (0, 0))

    def test_cap_counts_pending_and_completing(self):
        for state in ("PENDING", "COMPLETING"):
            other = UB.replace("RUNNING", state)
            self.assertEqual(self.count([U, other.replace("|6|", "|20|")]), (40, 1))
            with self.assertRaises(ValueError):
                self.count([U, other.replace("|6|", "|21|")])

    def test_peer_id_and_workdir_are_both_required(self):
        for row in (U.replace("368758", "368759"), U.replace("/run/u/", "/run/other/"),
                    U.replace(CASE, "/run/nonmixer")):
            with self.subTest(row=row), self.assertRaises(ValueError):
                self.count([row])

    def test_peer_scope(self):
        for old, new in (("runner.sbatch", "other"), ("|20|", "|19|"),
                         ("|cpu-60|", "|cpu-20|"), ("|cpu|", "|gpu|")):
            with self.subTest(old=old), self.assertRaises(ValueError):
                self.count([U.replace(old, new)])

    def test_other_mixer_and_duplicate_rows(self):
        for row in (UB.replace("ps73_UB", "first8_other"), U.replace("368758", "368759"),
                    UB.replace("/run/unloading/UB", "/alt/cases/PRECAL_R1_B3_U"), U):
            with self.subTest(row=row), self.assertRaises(ValueError):
                self.count([U, row])

    def test_malformed_or_ambiguous_snapshot(self):
        for row in (U.replace("|20|", "|?|"), "unparsed", U.replace("RUNNING", "UNKNOWN"),
                    U.replace(CASE, "(null)"), UB.replace("|6|", "|0|")):
            with self.subTest(row=row), self.assertRaises(ValueError):
                self.count([row])

    def test_preflight_preserves_wall_runtime_and_storage_checks(self):
        base = MODULE["base"]
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            root, prior = package / "C", package / "U"
            ctx = root / "arms/C"
            (ctx / "evidence").mkdir(parents=True)
            (ctx / "control").mkdir()
            (root / "control").mkdir()
            (root / "control/runtime_reference.json").write_text("{}")
            peer_case = prior / "B" / base["F8"] / "cases/PRECAL_R1_B2_U"
            peer_case.mkdir(parents=True)
            raw = {"queue": U.replace(CASE, str(peer_case.resolve())) + "\n" + UB,
                   "assoc": "author|cpu-60|3-00:00:00|", "partition": "State=UP MaxTime=3-00:00:00",
                   "df": "header\nfs 1 0 100000000000 1% /", "inode": "header\nfs 1 0 9999999 1% /",
                   "ost": "a-OST 200000000 0 100000000 1%", "quota": "ok"}
            labels = []

            def capture(area, label, args, timeout=60):
                labels.append((area.name, label))
                if label == "qos":
                    output = "cpu-60|3-00:00:00|" if "format=Name,MaxWall" in args else "cpu-60|cpu=60|"
                else:
                    output = raw[label]
                return output, {"rc": 0}

            with patch.dict(os.environ, USER="author"), patch.dict(base, capture=capture, runtime=lambda *args: {"matches": True}):
                live = base["read"](MODULE["preflight"](root, ctx, None, None, None, prior))
            self.assertEqual((live["reserved_cpus"], live["running_first8"]), (26, 1))
            self.assertTrue(live["qualification_accepted"] and live["disk_budget_verified"])
            self.assertEqual(set(live["raw_outputs"]), {"queue", "df", "inode", "ost", "quota"})
            self.assertEqual([label for area, label in labels].count("qos"), 2)


if __name__ == "__main__":
    unittest.main()
