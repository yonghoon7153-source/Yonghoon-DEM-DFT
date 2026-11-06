"""P8-08 — byte_diff_view offsets are functions of the sealed bytes (agreement depth of a sealed value).

  python3 -I probe_p808_offset.py <tree>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'scripts'))
import rint_r_chain as RR  # noqa: E402

for a, b in ((1.2345678, 1.2345679), (1.2345678, 1.2399999), (1.2345678, 9.9)):
    old, new = RR.canon_bytes({'a_key': 'x', 'sigma_sealed': a}), RR.canon_bytes({'a_key': 'x', 'sigma_sealed': b})
    v = RR.byte_diff_view(old, new)
    start = old.index(b'"sigma_sealed": ') + len('"sigma_sealed": ')
    print(a, b, v, '-> leading characters of the sealed value that agree =', v['first_diff_offset'] - start)
