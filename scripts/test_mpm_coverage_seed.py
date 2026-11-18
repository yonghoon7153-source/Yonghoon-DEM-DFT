"""Compare synthetic seed grids with the original bounded sphere raster."""
import ast
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mpm_coverage_c0 as coverage


class SeedGrid(unittest.TestCase):
    def setUp(self):
        self.assertTrue(hasattr(coverage, 'seed_counts'), 'seed raster required')
        self.am = np.zeros((8, 8, 12), dtype='i1')
        self.am[0, 1, 1] = 2
        self.n_grid, self.origin = 12, 2

    def test_original_raster_on_small_periodic_bed(self):
        source = (HERE/'mpm3d_compaction.py').read_bytes()
        functions = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef) and n.name == '_raster']
        self.assertEqual(len(functions), 1)
        env = dict(np=np, n_grid=12, nz=12, LO_m=2, WC_m=8, PERIODIC=True)
        exec(compile(ast.Module(body=functions, type_ignores=[]), '<fixed_raster>', 'exec'), env)
        se = np.zeros((12,12,12), dtype=bool)
        # Exact cell boundary, overlap, diagonal seam and clipped upper z.
        spheres = [(2/12, 2/12, .125, .19), (.24, .26, .35, .12),
                   (.24, .26, .35, .12), (.8, .8, .97, .09),
                   (5/12, 5.5/12, 6.5/12, .5/12)]
        for sphere in spheres:
            env['_raster'](se, *sphere, True)
        expected = (se[2:10, 2:10, :] & (self.am == 0)).astype('u1') * 8
        self.assertGreater(expected.sum(), 0)
        actual = coverage.seed_counts(self.am, spheres, self.n_grid, self.origin)
        np.testing.assert_array_equal(actual, expected)
        np.testing.assert_array_equal(actual, coverage.seed_counts(self.am, spheres[::-1], 12, 2))

    def test_empty_and_z_exclusion(self):
        for spheres in ([], [(0., 0., 2., .01)]):
            grid = coverage.seed_counts(self.am, spheres, 12, 2)
            self.assertFalse(grid.any())

    def test_wide_sphere_and_cli(self):
        sphere = (.18,.20,.47,.58)
        n = coverage.seed_counts(self.am, [sphere], 12, 2)
        ijk = np.indices(self.am.shape, dtype=float)
        ijk[:2] += 2
        delta = (ijk+.5)/12 - np.array(sphere[:3])[:,None,None,None]
        width = 8/12
        delta[:2] -= width*np.rint(delta[:2]/width)
        expected = ((delta**2).sum(axis=0) <= sphere[3]**2) & (self.am == 0)
        np.testing.assert_array_equal(n, 8*expected)
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch)/"geometry.npz"
            np.savez(path, am_phase=self.am, end_counts=n, seed_spheres=[sphere],
                     n_grid=12, lateral_origin=2, h_um=.25)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                coverage.main([str(path)])
            self.assertEqual(json.loads(buf.getvalue())["phases"]["2"]["plastic_increment"], 0.)

    def test_invalid_geometry(self):
        for spheres,n,lo in (([(0.,0.,0.,-1.)],12,2), ([(float('nan'),0,0,.1)],12,2),
                              ([],8,2), ([],12,-1), ([],0,0)):
            with self.subTest(n=n,lo=lo), self.assertRaises(ValueError):
                coverage.seed_counts(self.am, spheres, n, lo)


if __name__ == '__main__':
    unittest.main()
