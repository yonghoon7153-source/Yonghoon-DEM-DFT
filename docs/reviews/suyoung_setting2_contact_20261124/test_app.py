"""Candidate readback orchestration; the numerical rule comes from the frozen package."""
import runpy
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


def require_band(values):
    return abs(values[12] - values[16]), "PASS" if abs(values[12] - values[16]) <= .005 else "FAIL"


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.app = runpy.run_path(str(Path(__file__).with_name("app.py")))
        self.environment = SimpleNamespace(force=SimpleNamespace(compare=lambda a, b: {"comparison":"WITHIN"},
                                                                  aggregate=lambda pairs:"WITHIN"),
                                           old=SimpleNamespace(decision=lambda r, v: require_band(v)), rule=None)
        self.arms = {c: {"phi_m":.98, "dt":1/c, "wall_speed":.03, "trace_sha256":str(c)}
                     for c in (8,12,16,24)}
        self.curves = {c:[(0., 0.), (1., 1.2)] for c in self.arms}

    def test_two_required_pairs_and_closed_downstream(self):
        out = self.app["assess"](self.environment, self.arms, self.curves)
        self.assertEqual(set(out["pair_results"]), {"F8_F16","F12_F24"})
        self.assertEqual(out["item_6"], "WITHIN")
        self.assertFalse(out["stage3_go"])
        self.assertFalse(out["three_dimensional_go"])

    def test_failed_selection_prevents_use_as_gate(self):
        self.arms[12]["phi_m"] = .90
        out = self.app["assess"](self.environment, self.arms, self.curves)
        self.assertEqual(out["candidate_u6a"], "FAIL")
        self.assertEqual(out["item_6"], "HOLD_SELECTION")

    def test_bad_clocks_or_incomplete_set_cannot_pass(self):
        self.arms[16]["dt"] *= 1.1
        with self.assertRaises(ValueError):
            self.app["assess"](self.environment, self.arms, self.curves)
        del self.arms[12]
        with self.assertRaises(ValueError):
            self.app["assess"](self.environment, self.arms, self.curves)

    def test_complete_clock_record_and_watchdog_rejection(self):
        header = "grid\tstart_utc\telapsed_s\tprocess_rc\twatchdog_status\n"
        rows = [f"{n}\t2026-11-24T06:00:00Z\t19\t0\tnone\n" for n in (8, 12, 16, 24)]
        limits = {n: 100 for n in self.arms}
        with tempfile.TemporaryDirectory() as tmp:
            table = Path(tmp)/"arm_status.tsv"
            table.write_text(header + "".join(rows), encoding="ascii")
            self.assertEqual(self.app["operator_elapsed"](table, limits)[24], 19)
            for damaged in (rows[:-1], rows[:-1]+rows[:1],
                            [r.replace("\t0\tnone", "\t124\ttimeout") for r in rows]):
                table.write_text(header + "".join(damaged), encoding="ascii")
                with self.assertRaises(ValueError):
                    self.app["operator_elapsed"](table, limits)


if __name__ == "__main__":
    unittest.main()
