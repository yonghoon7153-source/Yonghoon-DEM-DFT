"""Compare phi fields in two q7_fields.npz files (allow_pickle=False), read-only.

Usage: python3 -I npz_cmp.py <codex.npz> <ours.npz>
"""
import hashlib
import sys

import numpy as np

a = np.load(sys.argv[1], allow_pickle=False)
b = np.load(sys.argv[2], allow_pickle=False)
print('keys same', sorted(a.files) == sorted(b.files), sorted(a.files))
for k in sorted(a.files):
    x, y = a[k], b[k]
    same_bytes = x.dtype == y.dtype and x.shape == y.shape and x.tobytes() == y.tobytes()
    d = float(np.max(np.abs(x - y))) if x.shape == y.shape else float('nan')
    rng = float(np.max(x) - np.min(x))
    print(f'{k:26s} shape {x.shape} bytes_equal {same_bytes}  max|dphi| {d:.3e}  (range {rng:.3e})  '
          f'sha codex {hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()[:12]} ours {hashlib.sha256(np.ascontiguousarray(y).tobytes()).hexdigest()[:12]}')
