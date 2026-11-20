"""Small command doubles only; no MPM time step is taken."""
import io
import json
from pathlib import Path
import tempfile
import unittest
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    import run_f16_only as driver
except ModuleNotFoundError:
    driver = None


class F16Only(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(driver, "F16 budget wrapper required")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)/"data"
        self.f12 = (HERE/"f12_result.json").read_bytes()
        self.source = io.BytesIO()

    def test_single_call_same_budget_and_reference(self):
        calls = []
        def run(cells, path, budget):
            calls.append((cells,path.name,budget))
            path.mkdir()
            (path/"result.json").write_bytes(self.f12.replace(b'"cells": 12', b'"cells": 16'))
            (path/"trace.csv").write_bytes(b"header\n")
        def assess(a,b):
            self.assertEqual((a["cells"],b["cells"]), (12,16))
            return "WITHIN_DEVELOPMENT_BAND"
        rc=driver.single(self.output,self.f12,run,assess)
        self.assertEqual((rc,calls), (0,[(16,"F16",1170.)]))
        self.assertEqual((self.output/"F12_returned.json").read_bytes(), self.f12)
        self.assertIsNone(json.loads((self.output/"comparison.json").read_bytes())["selected_setting"])
        with self.assertRaises(FileExistsError):
            driver.single(self.output,self.f12,run,assess)
        self.assertEqual(len(calls),1)

    def test_no_endpoint_yields_incomplete(self):
        def run(cells,path,budget):
            path.mkdir()
            (path/"result.json").write_bytes(b'{"status":"TIME_LIMIT","phi_m":null}')
            (path/"trace.csv").write_bytes(b"header\n")
        self.assertEqual(driver.single(self.output,self.f12,run,lambda a,b:"INCOMPLETE"),4)

    def test_modified_reference_refused_before_any_calculation(self):
        with self.assertRaises(ValueError):
            driver.single(self.output,self.f12 + b" ",self.fail,self.fail)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
