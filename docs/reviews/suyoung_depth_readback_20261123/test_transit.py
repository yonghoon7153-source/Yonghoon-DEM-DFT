"""Small clock and velocity examples for the retrospective arrival readback."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transit import LAYERS, first_sustained, layer_arrivals, speed_comparison


class LayerArrival(unittest.TestCase):
    def test_persistence_requires_both_endpoints(self):
        self.assertEqual(first_sustained([0, .1, .11, 0, .1, .11, .1], .1, 2), 4)
        self.assertIsNone(first_sustained([0, .1, .1], .1, 2))

    def test_downward_velocity_and_common_time_window(self):
        traces = {}
        for n in (12, 24):
            observations = [{} for _ in range(n)]
            for i, row in enumerate(observations, 1):
                for layer, mass in zip(LAYERS,(1.,2.,3.)):
                    row[layer+"_after"] = mass * (0.6 if i < n//3 else -.2)
            trace = [dict(time_code=i/n, height=1 - .1*i/n) for i in range(n+1)]
            traces[n] = layer_arrivals(trace, observations, [1.,2.,3.], 1., n)
        for layer in LAYERS:
            self.assertEqual(traces[12][layer]["0.10"]["time_code"], traces[24][layer]["0.10"]["time_code"])
            self.assertEqual(traces[12][layer]["0.10"]["step"], 4)

    def test_travel_ratio_factors_into_speed_and_arrival_time(self):
        def sample(t,u):
            return {n:{k:{"0.10":dict(time_code=t,displacement_D=u)} for k in LAYERS} for n in ("12","24")}
        original, half = sample(1.,.2),sample(1.1,.11)
        half["24"]["upper"]["0.10"] = None
        rec = speed_comparison(original,half,.5)
        self.assertAlmostEqual(rec["12"]["lower"]["travel_ratio"],.55)
        self.assertAlmostEqual(rec["12"]["lower"]["travel_D_beyond_constant_time"],.01)
        self.assertIsNone(rec["24"]["upper"])
        with self.assertRaises(ValueError):
            speed_comparison(original, half, .25)


if __name__ == "__main__":
    unittest.main()
