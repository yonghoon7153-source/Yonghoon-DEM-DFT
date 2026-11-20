"""Small synthetic archive tests. No field or observational data."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

p = Path(__file__).with_name("readback.py")
spec = importlib.util.spec_from_file_location("n0read", p)
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)


def fixture(names, bad_link=False):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for name in names:
            info = tarfile.TarInfo(rd.CASE + "/" + name)
            info.size = 1
            if bad_link and name == "in.mixer":
                info.type = tarfile.SYMTYPE
                info.linkname = "../outside"
                info.size = 0
            tar.addfile(info, io.BytesIO(b"a"))
    buf.seek(0)
    return tarfile.open(fileobj=buf)


class Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dest = Path(self.temp.name)
        self.names = sorted(rd.ALL | rd.CONTROL)

    def run_stage(self, names, link=False):
        with fixture(names, link) as tar:
            return rd.stage(tar, self.dest, reserve=0)

    def test_complete(self):
        self.assertEqual(self.run_stage(self.names), 234)
        self.assertEqual({p.name for p in (self.dest/"post").iterdir()},
                         {Path(f).name for f in rd.SELECTED})
        self.assertEqual(len(rd.SELECTED), 101)

    def test_missing_unselected_is_detected(self):
        self.names.remove("post/mix_32976.liggghts")
        with self.assertRaisesRegex(ValueError, "234 exact"):
            self.run_stage(self.names)

    def test_off_lattice_is_detected(self):
        with self.assertRaisesRegex(ValueError, "234 exact"):
            self.run_stage(self.names + ["post/mix_2.liggghts"])

    def test_duplicate_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.run_stage(self.names + [self.names[0]])

    def test_nonregular_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid"):
            self.run_stage(self.names, True)

    def test_traversal_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid"):
            self.run_stage(["../outside"])


if __name__ == "__main__":
    unittest.main()
