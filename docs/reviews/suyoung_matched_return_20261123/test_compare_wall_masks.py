"""Offline synthetic controls for the mask and the signed stress decomposition."""
import argparse
import sys
import unittest
from pathlib import Path

import numpy as np

import compare_wall_masks as reader


class MaskChecks(unittest.TestCase):
    # When installed under docs/reviews/<name>, standard unittest discovery
    # can locate both dependencies. Command-line overrides support any layout.
    source_root = Path(__file__).resolve().parents[3]
    layers_dir = source_root / "docs/reviews/suyoung_wall_layers_20261123"

    def test_missing_step_or_empty_mask_fails(self):
        record = {"step": 269, "projection": {"keys": [12]}}
        with self.assertRaisesRegex(ValueError, "mask step"):
            reader.saved_masks([record], [269, 270], 80)
        with self.assertRaisesRegex(ValueError, "mask keys"):
            reader.saved_masks([{"step": 269, "projection": {"keys": []}}], [269], 80)

    def test_floor_inclusive_and_above_floor_rejected_per_field(self):
        for grid in (80, 160):
            at_floor = 3*(grid+1)**2 + 8*(grid+1) + 3*grid//20
            record = {"step": 1, "projection": {"keys": [at_floor]}}
            self.assertEqual(reader.saved_masks([record], [1], grid)[1], [at_floor])
            record["projection"]["keys"] = [at_floor+1]
            with self.assertRaisesRegex(ValueError, "above"):
                reader.saved_masks([record], [1], grid)

    def test_geometric_halfspace_and_actual_subset(self):
        flat = reader.load_source(self.layers_dir, "flat_patch.py")
        layers = reader.load_source(self.layers_dir, "read_wall_layers.py")
        model, cross = flat.load_pinned_sources(self.source_root)
        state = dict(x=np.array([[.5, .152], [.5, .154]]), ids=np.array([0, 1], dtype=np.int64),
                     yy=np.array([-2., -1.5]), yx=np.array([.7, -.2]), volume=np.array([.01, .02]))
        pair = []
        for grid in (80, 160):
            all_wall = [field*(grid+1)**2 + i*(grid+1) + j for field in (0, 1)
                        for i in range(grid+1) for j in range(3*grid//20+1)]
            saved = [(grid//2 + 1)*(grid+1) + 3*grid//20]
            # An independent point-wise reduction over every geometric node,
            # including unsupported keys, checks the support-only optimization.
            point_mask = np.ones(len(state["ids"]), bool)
            def point_total(keys):
                rows = layers.point_rows(model.stencil, state, grid, layers.WIDTH, keys)
                return layers.reduce_points(rows, point_mask)

            independent_saved = point_total(saved)
            ref = dict(requested_keys=1, positive_support_keys=1,
                       values=dict(yy=independent_saved["yy_MPa"], yx=independent_saved["yx_MPa"],
                                   stress_MPa=independent_saved["stress_MPa"]))
            row = reader.corner(model, cross, state, grid, layers.WIDTH, saved, ref)
            geometric = point_total(all_wall)
            for k, point_key in (("yy", "yy_MPa"), ("yx", "yx_MPa"), ("stress_MPa", "stress_MPa")):
                self.assertAlmostEqual(row["geometric"][k], geometric[point_key], places=12)
            self.assertGreater(row["saved"]["yx"], 0.)
            self.assertGreater(row["saved"]["yy"], 0.)
            self.assertAlmostEqual(row["geometric"]["yx"], 0., places=12)
            pair.append(row)
        diff = reader.decompose(*pair)
        for k in reader.COMPONENTS:
            self.assertAlmostEqual(diff["saved"][k], diff["geometric"][k] +
                                   diff["saved_minus_geometric"][k], places=12)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--layers-dir", type=Path, default=MaskChecks.layers_dir)
    parser.add_argument("--source-root", type=Path, default=MaskChecks.source_root)
    args, test_args = parser.parse_known_args()
    MaskChecks.layers_dir = args.layers_dir
    MaskChecks.source_root = args.source_root
    unittest.main(argv=[sys.argv[0], *test_args])
