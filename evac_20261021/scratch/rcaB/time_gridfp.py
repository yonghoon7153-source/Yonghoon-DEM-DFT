"""Cost of the certificate binding fingerprint on a production-size grid (step3_sigma._grid_fp = blake2b over the grid bytes).
usage: python3 time_gridfp.py <scripts dir>"""
import sys
import time

sys.path.insert(0, sys.argv[1])
import numpy as np            # noqa: E402
import step3_sigma as S       # noqa: E402

for shape in ((400, 400, 400), (600, 600, 800)):
    a = np.zeros(shape, np.int8)
    t = time.time()
    S._grid_fp(a)
    dt = time.time() - t
    print(f'grid {shape} = {a.size / 1e6:.0f}e6 cells int8: {dt:.3f} s ({a.nbytes / 1e6 / dt:.0f} MB/s)')
    del a
