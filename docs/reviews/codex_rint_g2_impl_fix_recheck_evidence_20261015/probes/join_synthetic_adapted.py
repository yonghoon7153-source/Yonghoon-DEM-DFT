"""Prior synthetic probe adapted only for the declared g6 contract and early REJECT keys.

The original +1ppm uniformly-16-digit attack remains uniformly 16-digit.
Near-concentric separation, supplied area and every negative mutation are unchanged.
"""
from pathlib import Path
import difflib

ROOT = Path(__file__).resolve().parents[1]
old_path = ROOT.parent / 'rint_g2_impl_review_20261014/probes/join_synthetic.py'
original = old_path.read_text(encoding='utf-8')
changes = {
    "fmt = lambda x: f'{float(x):.15e}'": "fmt = (lambda x: f'{float(x):.15e}') if tag == '16sig_area_plus_1ppm' else (lambda x: '%g' % float(x))",
    "area_sim2=j['dem_am_am']['area_um2'].tolist()[0] / 1e6)": "area_sim2=(j['dem_am_am']['area_um2'].tolist()[0] / 1e6 if len(j['dem_am_am']['area_um2']) else None))",
    "'tmp/join_synthetic'": "'tmp/join_synthetic_adapted'",
    "'evidence/join_synthetic.json'": "'evidence/join_synthetic_adapted.json'",
}
adapted = original
for before, after in changes.items():
    assert adapted.count(before) == 1, before
    adapted = adapted.replace(before, after)
(ROOT/'evidence/join_synthetic_adaptation.diff').write_text(
    ''.join(difflib.unified_diff(original.splitlines(True), adapted.splitlines(True),
                                 fromfile='unchanged_prior_probe', tofile='adapted_g6_probe')),
    encoding='utf-8')
exec(compile(adapted, str(old_path), 'exec'), {'__name__': '__main__', '__file__': str(ROOT/'probes/join_synthetic.py')})
