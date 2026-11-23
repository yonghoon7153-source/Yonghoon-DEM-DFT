"""Ground the old noncontact case by numerical tolerance instead of platform-specific JSON bytes."""
import importlib.util
import json
import math
from pathlib import Path
import unittest
import sys


def check_same(saved, actual):
    if type(saved) is float:
        if type(actual) not in (float,int) or not math.isclose(actual,saved,rel_tol=1e-12,abs_tol=1e-16):
            raise ValueError(f"Divergent scalar: {saved} vs {actual}")
    elif isinstance(saved,dict) and type(actual) is dict and saved.keys() == actual.keys():
        for key in saved:
            check_same(saved[key],actual[key])
    elif isinstance(saved,list) and type(actual) is list and len(saved) == len(actual):
        for a,b in zip(saved,actual):
            check_same(a,b)
    elif type(saved) is not type(actual) or saved != actual:
        raise ValueError("Reference identity or structure differs")


class ReferenceImpulse(unittest.TestCase):
    reference = Path(__file__).resolve().parent.parent/"suyoung_matched_return_20261123"
    source_root = Path(__file__).resolve().parents[3]

    def test_pinned_slab_across_platforms(self):
        spec = importlib.util.spec_from_file_location("old_noncontact",self.reference/"noncontact_slab.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        actual = module.run(self.source_root)
        check_same(json.loads((self.reference/"noncontact_slab.json").read_text()),actual)
        near = actual["cases"][0]["grids"][0]
        self.assertTrue(math.isclose(near["impulse_fraction_of_abs_incoming_momentum"],1/96,rel_tol=1e-12))

    def test_linux_windows_roundoff(self):
        check_same(2.0833333333333313e-6, 2.083333333333317e-6)
        check_same(.010416666666666661,.010416666666666663)

    def test_substantial_difference_is_rejected(self):
        with self.assertRaises(ValueError):
            check_same({"impulse":2.0833333333333313e-6},{"impulse":0.0})
        with self.assertRaises(ValueError):
            check_same({"grid":80},{"grid":160})


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--reference",type=Path,default=ReferenceImpulse.reference)
    p.add_argument("--source-root",type=Path,default=ReferenceImpulse.source_root)
    a, rest = p.parse_known_args()
    ReferenceImpulse.reference,ReferenceImpulse.source_root = a.reference,a.source_root
    unittest.main(argv=[sys.argv[0],*rest])
