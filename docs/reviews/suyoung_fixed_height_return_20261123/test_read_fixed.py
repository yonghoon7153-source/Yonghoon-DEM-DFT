"""Small checks for fork binding, nested time samples and signed pressure arithmetic."""
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("fixed_readback", Path(__file__).with_name("read_fixed.py"))
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def sample(floor):
    return {"floor_MPa": floor, "lid_MPa": 2*floor, "KE": floor**2}


class FixedReadbackTest(unittest.TestCase):
    def test_prefix_ends_at_fork(self):
        prefix = b"step,p\r\n1,0\r\n2,1\r\n"
        self.assertEqual(reader.bound_prefix(prefix+b"3,2\r\n", prefix+b"3,4\r\n", 2), reader.sha(prefix))
        for bad in (prefix.replace(b"\r\n",b"\n"), prefix[:-5], prefix.replace(b"2,1",b"2,9")):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                reader.bound_prefix(prefix, bad, 2)

    def test_fork_and_interpolation(self):
        coarse = [sample(7),sample(1),sample(3)]
        fine = [sample(x) for x in (15,9,4,4,5)]
        result = reader.paired_series(coarse, fine, .125)
        self.assertEqual([v["time_since_stop"] for v in result], [0,.125,.25,.375,.5])
        self.assertEqual([v["F12_interpolated"] for v in result], [0,1,0,1,0])
        self.assertEqual([v["floor_gap_MPa"] for v in result], [-8,-5,-3,-2,-2])
        self.assertEqual(result[1]["F12_KE"], 25)
        with self.assertRaises(ValueError):
            reader.paired_series(coarse, fine[:-1], .125)

    def test_signed_mean_and_rms_are_distinct(self):
        stats = reader.range_stats([3, -3])
        self.assertEqual((stats["mean"],stats["rms"]), (0,3))
        for x in ([], [math.inf], [math.nan]):
            with self.subTest(x=x), self.assertRaises(ValueError):
                reader.range_stats(x)

    def test_late_rebound_identity(self):
        earlier = reader.wall_terms(3., 1.)
        later = reader.wall_terms(4., 0.)
        self.assertEqual(later["mean_of_grid_differences"]-earlier["mean_of_grid_differences"], 0)
        self.assertEqual(later["half_signed_imbalance"]-earlier["half_signed_imbalance"], 1)
        self.assertEqual(sum(later.values()),4)

    def test_exact_outer_manifest_and_screen(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "result.tar.gz"
            screen = b"COMMAND_RC=0\n"
            identity = [reader.sha(b"fixture"), "", "", reader.sha(screen)]
            manifest = f"{identity[0]}  {path.name}\n{identity[3]}  screen.txt\n"
            (root/"screen.txt").write_bytes(screen)
            (root/"SHA256SUMS").write_bytes(manifest.encode("ascii"))
            reader.check_sidecars(path, identity)
            (root/"screen.txt").write_bytes(b"COMMAND_RC=1\n")
            with self.assertRaisesRegex(ValueError,"external screen hash"):
                reader.check_sidecars(path, identity)
            (root/"SHA256SUMS").write_bytes((manifest + manifest.splitlines()[0]+"\n").encode("ascii"))
            with self.assertRaisesRegex(ValueError,"sidecar manifest"):
                reader.check_sidecars(path, identity)


if __name__ == "__main__":
    unittest.main()
