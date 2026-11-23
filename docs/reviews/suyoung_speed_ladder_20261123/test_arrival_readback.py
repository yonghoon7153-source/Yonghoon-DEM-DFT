"""Manufactured timing, momentum-sign and matched-duration checks."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arrival_readback as reader


def observation(step, lower_delta, middle_delta, upper_delta, top_load):
    layers = (lower_delta, middle_delta, upper_delta)
    row = {"step":step,"whole_before":0., "whole_after":sum(layers), "lid_signed_J":-top_load,
           "floor_J":sum(layers)+top_load}
    for name,change in zip(reader.LAYERS,layers,strict=True):
        row[name+"_before"] = .4
        row[name+"_after"] = .4+change
    return row


class TimingAndMomentum(unittest.TestCase):
    def test_sustained_downward_crossing_rejects_upward_and_short_transients(self):
        velocities = (-1.,-1.,-.5, 4.,-1.,-1.,-1.,-1.,-1.)
        rows = [{"step":i, "Py":v} for i,v in enumerate(velocities,1)]
        self.assertEqual(reader.arrival_index(rows, "Py", 1., 3), 5)
        self.assertEqual(reader.arrival_index(rows, "Py", 1., 5), 5)
        self.assertIsNone(reader.arrival_index(rows, "Py", 1., 6))

    def test_fine_two_step_window_integrates_the_same_impulse(self):
        coarse = [observation(1,.15,-.01,-.02,.20)]
        fine = [observation(1,.10,-.01,-.02,.11),observation(2,.05,0.,0.,.09)]
        c = reader.momentum_window(coarse,1,1,.50,2.)
        f = reader.momentum_window(fine,2,2,.25,2.)
        for k in (*reader.LAYERS,"whole","lid_down","floor"):
            self.assertAlmostEqual(c[k],f[k])
        self.assertAlmostEqual(c["floor"],3.2)
        self.assertAlmostEqual(c["lid_down"],2.0)
        self.assertNotAlmostEqual(c["floor"],reader.momentum_window(fine,2,1,.25,2.)["floor"])

    def test_inconsistent_wall_or_layer_measurements_stop_the_readback(self):
        for field in ("middle_after","lid_signed_J","floor_J"):
            with self.subTest(field=field):
                row = observation(1,.15,-.01,-.02,.20)
                row[field] += .02
                with self.assertRaises(ValueError):
                    reader.momentum_window([row],1,1,1.,2.)
        with self.assertRaisesRegex(ValueError,"bounds"):
            reader.momentum_window([observation(1,0.,0.,0.,0.)],1,2,1.,2.)


if __name__ == "__main__":
    unittest.main()
