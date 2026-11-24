"""No new physical run. Check the operator's grid and evidence boundaries."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


def app():
    spec = importlib.util.spec_from_file_location("higher", Path(__file__).with_name("higher.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HigherTests(unittest.TestCase):
    def test_pairs_are_new_development_pairs(self):
        m = app()
        self.assertEqual(m.PAIRS, {32:16, 48:24})
        self.assertEqual(set(m.SEEDS), set(m.BUDGET))
        self.assertEqual(m.DT[32]*2, .0011231835082397789)
        self.assertEqual(m.DT[48]*2, .000748789005493186)

    def test_guard_only_changes_literal_once(self):
        m = app()
        source = b"if cells not in (8, 12, 16, 24) or not ok: pass"
        self.assertEqual(m.expand_guard(source), source.replace(b"16, 24", b"16, 24, 32, 48"))
        for bad in (source+source, b"if other: pass"):
            with self.assertRaises(ValueError):
                m.expand_guard(bad)

    def test_wrong_prior_stops_before_opening_tar(self):
        m = app()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"wrong.tar.gz"
            path.write_bytes(b"wrong")
            with self.assertRaisesRegex(ValueError, "setting 2 return"):
                m.prior_arms(path)

    def test_higher_pair_outcomes_do_not_change_qualification(self):
        m = app()
        for ratio, expected in ((.05,"WITHIN"),(.051,"EXCEEDS")):
            pair = dict(comparison=expected,ratio=ratio)
            summary = m.outcome({k:pair for k in m.PAIRS})
            self.assertEqual(summary["higher_pair_comparison"], expected)
            self.assertFalse(summary["stage3_go"])
            self.assertFalse(summary["original_item6_pass"])

    def test_missing_pair_cannot_complete(self):
        m = app()
        with self.assertRaises(ValueError):
            m.outcome({32:dict(comparison="WITHIN",ratio=0)})


if __name__ == "__main__":
    unittest.main()
