"""Small algebraic readback tests. No trajectory is advanced."""
import importlib.util
import math
from pathlib import Path
import unittest

import numpy as np


class Layers(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name("read_wall_layers.py")
        self.assertTrue(path.is_file(), "layer reader is not implemented")
        spec = importlib.util.spec_from_file_location("local_layer_reader", path)
        self.reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.reader)

    def test_right_bin_owns_edge_and_signed_distance_is_preserved(self):
        y = np.array([-.1, 0., .002, .5/160, 1/160, 3/160, 0.4])
        self.assertEqual(self.reader.layer_index(y).tolist(), [0, 1, 1, 2, 3, 6, 6])

    def test_point_rows_mask_id_volume_geometry_and_sign(self):
        state = dict(x=np.array([[.4, .25],[.4,.25]]), ids=np.array([0,1]),
                     volume=np.array([3.,7.]), yy=np.array([-.5,-1.]), yx=np.array([.25,2.]))
        def stencil(x, grid):
            nodes = np.array([[1,2],[1,2]])
            w = np.array([[.25,.75],[.25,.75]])
            off = np.array([[[-.125,-.25],[.25,.5]],[[-.125,-.25],[.25,.5]]])
            return nodes,w,None,off
        # Only field 0's node 1 is active, although both points share coordinates.
        points = self.reader.point_rows(stencil, state, 2, 2., [1])
        self.assertEqual(points["active"].tolist(), [True,False])
        self.assertEqual(points["masked_volume"].tolist(), [.75,0.])
        # 40*2^2/2 * .75 = 60
        self.assertEqual(points["K"].tolist(), [15.,0.])
        self.assertEqual(points["yy_MPa"].tolist(), [7.5,0.])
        self.assertEqual(points["yx_MPa"].tolist(), [-1.875,0.])

    def test_empty_and_cancelling_support_do_not_produce_effective_stress(self):
        points = dict(active=np.array([True,True]), masked_volume=np.array([.5,.5]),
                      K=np.array([2.,-2.]), yy_MPa=np.array([4.,-1.]), yx_MPa=np.array([0.,0.]))
        for mask in (np.array([True,True]), np.array([False,False])):
            row = self.reader.reduce_points(points, mask)
            self.assertIsNone(row["effective_compression_solver_units"])
        row = self.reader.reduce_points(points, np.array([True,True]))
        self.assertEqual(row["K_abs"], 4.)
        self.assertEqual(row["stress_MPa"], 3.)

    def test_geometry_stress_product_symmetric_split_restores_signed_difference(self):
        a=dict(K=5., effective_compression_solver_units=2.)
        b=dict(K=3., effective_compression_solver_units=1.)
        q=self.reader.product_split(a,b)
        self.assertEqual(q,dict(geometry_MPa=3., effective_compression_MPa=4., yy_difference_MPa=7.))
        self.assertIsNone(self.reader.product_split(dict(K=0.,effective_compression_solver_units=None),b))

    def test_native_witness_rejects_compensating_component_change(self):
        row=dict(K=2.,yy_MPa=3.,yx_MPa=-1.,stress_MPa=2.)
        self.reader.match_totals(row,dict(unit_yy=-2.,yy=3.,yx=-1.,stress_MPa=2.))
        with self.assertRaises(ValueError):
            self.reader.match_totals(row,dict(unit_yy=-2.,yy=2.,yx=0.,stress_MPa=2.))


if __name__ == "__main__":
    unittest.main()
