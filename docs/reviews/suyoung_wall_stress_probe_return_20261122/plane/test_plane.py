"""Exact plane-stencil controls on synthetic material point coordinates only."""
import argparse
from fractions import Fraction as Q
import importlib.util
import sys
from pathlib import Path
import unittest

import numpy as np


class SlabTests(unittest.TestCase):
    def test_aligned_contact_exact_reference(self):
        for g in (80,160):
            self.assertEqual(p.analytic(g,Q(0)),Q(145,16))
            q=p.sample_points(Q(0))
            self.assertAlmostEqual(p.transfer(stencil,q,g)["vertical_MPa"],9.0625,places=12)

    def test_clearance_and_support_edges(self):
        for g,gap,expected in ((80,Q(1,320),Q(1885,256)),(160,Q(1,320),Q(5)),
                               (160,Q(3,320),Q(0)),(80,Q(3,320),Q(675,256))):
            self.assertEqual(p.analytic(g,gap),expected)
            result=p.transfer(stencil,p.sample_points(gap),g)
            self.assertAlmostEqual(result["vertical_MPa"],float(expected),places=12)
            self.assertAlmostEqual(result["shear_MPa"],0.,places=12)
            if expected==0: self.assertEqual(result["selected_nodes"],0)

    def test_equal_dimensionless_clearance(self):
        for g in (80,160):
            gap=Q(1,2*g)
            self.assertEqual(p.analytic(g,gap),5)
            self.assertAlmostEqual(p.transfer(stencil,p.sample_points(gap),g)["vertical_MPa"],5.,places=12)

    def test_fixed_gap_uses_exact_same_cloud_for_both(self):
        q=p.sample_points(Q(1,640))
        for g in (80,160):
            old=q[0].tobytes(),q[1].tobytes()
            result=p.transfer(stencil,q,g)
            self.assertEqual(old,(q[0].tobytes(),q[1].tobytes()))
            self.assertAlmostEqual(result["vertical_MPa"],float(p.analytic(g,Q(1,640))),places=12)
        self.assertAlmostEqual(q[1].sum(),float(p.WIDTH*p.THICKNESS),places=15)


if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--material",required=True,type=Path)
    args,rest=args.parse_known_args()
    spec=importlib.util.spec_from_file_location("slab",Path(__file__).with_name("plane.py"))
    p=importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
    stencil=p.get_stencil(args.material)
    unittest.main(argv=[sys.argv[0]]+rest)
