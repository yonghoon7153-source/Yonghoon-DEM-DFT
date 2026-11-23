"""Manufactured signed impulses and optional readback of the two original archives."""
import json
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import read_depth as depth


class ReadDepth(unittest.TestCase):
    def test_prefix_requires_original_bytes_and_complete_history(self):
        original = b"step,val\r\n1,0\r\n2,1\r\n"
        short = b"step,val\r\n1,0\r\n"
        depth.check_prefix(short, original, 1)
        for candidate, count in ((short.replace(b"\r", b""),1), (short,2), (original,3)):
            with self.assertRaisesRegex(ValueError, "CSV prefix"):
                depth.check_prefix(candidate, original, count)

    def test_equal_duration_preserves_signed_cancellation(self):
        def values(downward_lid, floor, lower, middle, upper):
            return dict(lower=lower, middle=middle, upper=upper, whole=lower+middle+upper,
                        floor=floor, lid_signed=-downward_lid)
        coarse = {"dt": 1., "width": 2., "records": [values(1., 2., 1.5,-.4,-.1)]}
        fine = {"dt": .5, "width": 2., "records": [values(.2,.4,.1,.4,-.3),values(.8,1.6,1.4,-.8,.2)]}
        a = depth.window(coarse,1,1)
        native = depth.differences(a, depth.window(fine,2,1))
        common = depth.differences(a, depth.window(fine,2,2))
        self.assertNotEqual(native["floor"], 0.)
        self.assertAlmostEqual(native["whole"], native["floor"]+native["lid_signed"])
        self.assertAlmostEqual(native["whole"], sum(native[k] for k in depth.LAYERS))
        for key in depth.FIELDS:
            self.assertAlmostEqual(common[key], 0.)
        with self.assertRaisesRegex(ValueError, "window bounds"):
            depth.window(fine,1,2)

    @unittest.skipUnless("DEPTH_RESULT" in os.environ and "HALF_SPEED_RESULT" in os.environ, "set return paths")
    def test_fixed_archives_and_grid_clocks(self):
        current = Path(os.environ["DEPTH_RESULT"])
        prior = Path(os.environ["HALF_SPEED_RESULT"])
        with self.assertRaisesRegex(ValueError, "SHA256"):
            depth.inspect(prior,current)
        report, series = depth.inspect(current,prior)
        self.assertEqual(len(series),555)
        self.assertEqual([p["F12_step"] for p in report["anchors"]], [481,555])
        self.assertEqual(report["anchors"][0]["F24"]["floor"],0.)
        self.assertGreater(report["max_common_prefix_pct"],5.)
        peak = report["anchors"][1]
        self.assertGreater(peak["F12"]["lower"],0.)
        self.assertLess(peak["F24"]["lower"],0.)

    @unittest.skipUnless("DEPTH_RESULT" in os.environ and "HALF_SPEED_RESULT" in os.environ, "set return paths")
    def test_rehashed_changed_layer_observation_detected(self):
        files = depth.archive(Path(os.environ["DEPTH_RESULT"]),depth.CURRENT)
        old = depth.archive(Path(os.environ["HALF_SPEED_RESULT"]),depth.HALF)
        summary = depth.scope(files,depth.PIN,"DEPTH_PREFIX_COMPLETE")
        prev = depth.scope(old,depth.HALF_PIN,"HALF_SPEED_PREFIX_COMPLETE")
        key = "run/F12/layer_steps.csv"
        lines = files[key].splitlines(keepends=True)
        values = lines[1].split(b",")
        values[-1] = b"0.2\n"
        lines[1] = b",".join(values)
        files[key] = b"".join(lines)
        receipt = summary["arms"]["12"]
        receipt["layer_sha256"] = depth.hash_bytes(files[key])
        files["run/F12/layer_receipt.json"] = json.dumps(receipt).encode()
        with self.assertRaisesRegex(ValueError, "layer deltas"):
            depth.check_arm(12,files,old,summary,prev)


if __name__ == "__main__":
    unittest.main()
