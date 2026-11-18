"""Synthetic checks on the non-Rint C(0) measurement grid."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import mpm_coverage_c0 as coverage
except ModuleNotFoundError as error:
    if error.name != "mpm_coverage_c0":
        raise
    coverage = None


class ContactFaces(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(coverage, "C(0) measurement interface required")
        self.am = np.zeros((5, 4, 3), dtype=int)
        self.n = np.zeros_like(self.am)

    def read(self, phase=1, h=.5):
        return coverage.contact_census(self.am, self.n, h)[phase]

    def test_measured_zero_and_unobserved_phase(self):
        self.am[2, 2, 1] = 1
        self.assertEqual(self.read()['C0'], 0.)
        self.assertEqual(self.read(2)['reason'], 'phase_absent')
        self.assertIsNone(self.read(2)['C0'])

    def test_threshold_contact_area(self):
        self.am[2, 2, 1] = 1
        self.n[3, 2, 1] = 3
        self.assertEqual(self.read()['covered_faces'], 0)
        self.n[3, 2, 1] = 4
        self.assertEqual(self.read()['C0'], 1/6)
        self.assertEqual(self.read()['covered_area_um2'], .25)

    def test_z_boundary_and_am_am(self):
        self.am[2, 2, 0] = 1
        self.am[3, 2, 0] = 2
        self.n[2, 2, -1] = 8
        for p in [1,2]:
            self.assertEqual(self.read(p)['free_faces'], 4)
            self.assertEqual(self.read(p)['C0'], 0.)

    def test_empty_surface_in_singleton_box(self):
        self.am = np.ones((1, 1, 1), dtype=int)
        self.n = np.zeros_like(self.am)
        result = self.read()
        self.assertIsNone(result['C0'])
        self.assertEqual(result['reason'], 'free_surface_empty')

    def test_seams_and_translation(self):
        for axis in (0, 1):
            self.am.fill(0)
            self.n.fill(0)
            here = [2, 2, 1]
            here[axis] = 0
            self.am[tuple(here)] = 1
            here[axis] = -1
            self.n[tuple(here)] = 8
            a = self.read()
            self.assertEqual(a['seam_unrepresented_faces'], 1)
            self.assertEqual(a['seam_unrepresented_area_um2'], .25)
            self.am = np.roll(self.am, 1, axis)
            self.n = np.roll(self.n, 1, axis)
            b = self.read()
            self.assertEqual(b['C0'], a['C0'])
            self.assertEqual(b['seam_unrepresented_faces'], 0)

    def test_census_matches_scalar_neighbors(self):
        rng = np.random.default_rng(428)
        for shape in ((1,2,3), (2,1,1), (3,5,4)):
            am = rng.integers(0, 3, shape)
            counts = np.where(am == 0, rng.integers(0, 10, shape), 0)
            totals = coverage.contact_census(am, counts, .4)
            for phase in (1,2):
                free = covered = seams = 0
                for i in zip(*np.where(am == phase)):
                    for axis in (0,1,2):
                        for delta in (-1,1):
                            j = list(i)
                            j[axis] += delta
                            wrapped = not 0 <= j[axis] < shape[axis]
                            if wrapped and axis == 2:
                                continue
                            j[axis] %= shape[axis]
                            if am[tuple(j)]:
                                continue
                            free += 1
                            if counts[tuple(j)] >= 4:
                                covered += 1
                                seams += int(wrapped)
                r = totals[phase]
                self.assertEqual((r['free_faces'], r['covered_faces'], r['seam_unrepresented_faces']),
                                 (free, covered, seams))

    def test_invalid_inputs(self):
        for a,n,h in ((self.am,self.n,-1), (self.am,self.n,float('nan')),
                      (self.am,self.n[0],1), (self.am+3,self.n,1),
                      (self.am,self.n-1,1), (self.am,self.n.astype(float),1),
                      (self.am+1,self.n+4,1)):
            with self.subTest(h=h), self.assertRaises(ValueError):
                coverage.contact_census(a,n,h)

    def test_seed_end_and_analytic_reference(self):
        self.am[1,1,1] = 1
        self.n[1,2,1] = 4
        end = self.n.copy()
        end[2,1,1] = 5
        r = coverage.compare(self.am,self.n,end,.5,[.2,None])['phases']['1']
        self.assertEqual(r['C_rigid'], .2)
        self.assertAlmostEqual(r['seed_bias'], 1/6-.2)
        self.assertAlmostEqual(r['plastic_increment'], 1/6)
        eq = coverage.compare(self.am,self.n,self.n,.5,[None,None])['phases']['1']
        self.assertEqual(eq['plastic_increment'], 0.)
        self.assertIsNone(eq['seed_bias'])
        with self.assertRaises(ValueError):
            coverage.compare(self.am,self.n,end,.5,[.2,0.])

    def test_npz_entry(self):
        self.am[1,1,1] = 1
        with tempfile.TemporaryDirectory() as d:
            src = Path(d)/'synthetic.npz'
            np.savez(src, am_phase=self.am, seed_counts=self.n, end_counts=self.n, h_um=.5)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                coverage.main([str(src)])
            self.assertEqual(json.loads(buf.getvalue())['phases']['1']['C_end'], 0.)


if __name__ == "__main__":
    unittest.main()
