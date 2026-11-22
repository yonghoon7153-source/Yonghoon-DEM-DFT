"""Check the frozen-node measurements without a grid, time steps or field data."""
import argparse
import importlib.util
from pathlib import Path
import sys
import unittest

import numpy as np


def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


probe = load_file(Path(__file__).with_name("frozen_node_sweeps.py"), "frozen_probe")
PAIR = {
    "mass": [1.0, 1.0],
    "positions_and_gradient_per_mass": [[-1.0, 0.0], [1.0, 0.0]],
    "incoming_velocity": [[1.0, 0.0], [-1.0, 0.0]],
}


class FrozenControls(unittest.TestCase):
    def test_updated_velocities_carry_into_next_batch(self):
        def damp(ids, nodes, mass, grad, velocity, centers, mu):
            # Momentum-preserving analytic test double: this probe starts at p=0.
            velocity *= 0.5

        result = probe.measure(prior, damp, PAIR, 0.0)
        self.assertEqual(result["permutations"], 2)
        for batch in (1, 2, 4, 16):
            row = result["batches"][batch]
            self.assertEqual(row["max_change_from_previous_batch"], 0.5**batch)
            self.assertEqual(row["max_residual_closing_speed"], 2.0 * 0.5**batch)
            self.assertEqual(row["max_kinetic_energy"], 0.25**batch)
            self.assertEqual(row["max_same_body_velocity_difference"], 0.0)

    def test_momentum_violation_detected(self):
        def drift(ids, nodes, mass, grad, velocity, centers, mu):
            velocity[:] = [0.01, 0.0]

        with self.assertRaises(ArithmeticError):
            probe.measure(prior, drift, PAIR, 0.0)

    def test_energy_increase_detected_at_zero_momentum(self):
        def increase(ids, nodes, mass, grad, velocity, centers, mu):
            velocity *= 2.0

        with self.assertRaises(ArithmeticError):
            probe.measure(prior, increase, PAIR, 0.0)

    def test_real_two_body_frictionless_transverse_motion(self):
        centers = np.array(PAIR["positions_and_gradient_per_mass"])
        velocities = np.array([[1.0, 0.25], [-1.0, -0.5]])

        def frictionless(ids, nodes, mass, grad, velocity, positions, ignored):
            native(ids, nodes, mass, grad, velocity, positions, 0.0)

        for ids in ([0, 1], [1, 0]):
            for rows in ([0, 1], [1, 0]):
                out = prior.project(frictionless, centers, np.ones(2), velocities,
                                    np.array(ids), np.array(rows))
                np.testing.assert_array_equal(out, [[0.0, 0.25], [0.0, -0.5]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    args, rest = parser.parse_known_args()
    source = args.repo / probe.FIXTURES / "node_permutation.py"
    probe.verified(source, probe.SOURCE_SHA)
    prior = load_file(source, "fixed_fixture")
    native = prior.load_projection(args.repo / "scripts")
    unittest.main(argv=[sys.argv[0]] + rest)
