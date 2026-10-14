"""Offline owner/T4 review probes. Does not edit the source snapshot."""
import contextlib
import itertools
import json
import os
from pathlib import Path
import platform
import sys
import types

HERE = Path(__file__).resolve().parents[1]
WORK = HERE.parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE / 'source' / 'scripts'), str(WORK / 'lhs_coverage_review_20260930' / 'deps'), str(WORK / 'gen2_network_reverify3_20261007' / 'deps')]
# Windows lacks resource; only the report-only peak RSS field is shimmed.
if os.name == 'nt':
    resource = types.ModuleType('resource')
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float('nan'))
    sys.modules['resource'] = resource

import numpy as np
import scipy
import step3_sigma as S3
import rint_t41_census as T41
import rint_t43_order_diag as T43


def signatures(led):
    return (led['owner'].tobytes(),
            tuple((g, k, np.asarray(v).dtype.str, np.asarray(v).shape, np.asarray(v).tobytes())
                  for g in ('contacts', 'faces', 'particles') for k, v in sorted(led[g].items())),
            tuple(sorted(x['code'] for x in led['rejections'])))


def epsilon():
    eps = 1e-6
    powers = np.array([-0.9999985000000001, -0.9999992499999999, -1.0000000000000009])
    result = []
    for p in itertools.permutations(range(3)):
        p = np.array(p)
        _, owner, band, claim = S3._iface_owner_select(np.zeros(3, np.int64), p, p, powers[p], eps)
        result.append({'perm': p.tolist(), 'owner': int(owner[0]), 'band_size': int(band[0]), 'n_claim': int(claim[0])})
    rng = np.random.default_rng(110714)
    n_cases = 0
    mismatches = []
    for n in range(2, 13):
        for _ in range(50):
            power = rng.normal(size=n) * eps
            rank = rng.permutation(n)
            expected = int(rank[power <= power.min() + eps].min())
            _, own, band, _ = S3._iface_owner_select(np.zeros(n, np.int64), rank, np.arange(n), power, eps)
            if int(own[0]) != expected:
                mismatches.append([n, expected, int(own[0])])
            n_cases += 1
    return {'contract_counterexample': result, 'random_set_oracle_cases': n_cases, 'mismatches': mismatches}


def frozen():
    rng = np.random.default_rng(10714)
    cases = []
    for k in range(6):
        c = rng.uniform(0.7, 2.1, (4, 3))
        r = rng.uniform(0.62, 0.92, 4)
        t = np.array([1, 2, 1, 2])
        lo = np.zeros(3)
        h = 0.2
        sid, _ = S3.rasterize(c, r, t, None, None, lo, (3., 3., 3.), h, bridge_um=0.26)
        ref = None
        mismatch = []
        for p in itertools.permutations(range(4)):
            p = np.array(p)
            led = S3.am_iface_ledger(c[p], r[p], t[p], sid, sid, lo, h, delta_bound_um=0.002, bridge_um=0.26)
            sig = signatures(led)
            if ref is None:
                ref = sig
            elif sig != ref:
                mismatch.append(p.tolist())
        # Independent set oracle reads the exposed claim set and recalculates each candidate's power.
        canonical = np.lexsort((c[:, 2], c[:, 1], c[:, 0]))
        cc, rr = c[canonical], r[canonical]
        cells, ranks = led['claims']['cell'], led['claims']['rank']
        oracle_diff = []
        for cell in np.unique(cells):
            rank = ranks[cells == cell]
            xyz = np.array(np.unravel_index(int(cell), sid.shape))
            cg = (cc[rank] - lo) / h
            power = ((xyz[0] + 0.5 - cg[:, 0]) ** 2 + (xyz[1] + 0.5 - cg[:, 1]) ** 2
                     + (xyz[2] + 0.5 - cg[:, 2]) ** 2 - (rr[rank] / h) ** 2) * h * h
            expected = int(rank[power <= power.min() + 1e-9].min())
            if int(led['owner'].flat[int(cell)]) != expected:
                oracle_diff.append(int(cell))
        cases.append({'case': k, 'c': c.tolist(), 'r': r.tolist(), 'perms': 24,
                      'multi_claim_ge3': led['n_cells_multi_claim'], 'epsilon_band_gt1': led['n_cells_band_gt1'],
                      'permutation_mismatches': mismatch, 'independent_owner_oracle_differences': oracle_diff,
                      'rejections': led['rejections']})
    c = np.array([[1.9748831001799223, 1.8791293045780670, 1.7896943576126298],
                  [1.0611990064053260, 0.8549090548944595, 1.7364778658264648]])
    r = np.array([0.5348361452776790, 0.8437277367739292]); t = np.array([2, 1])
    diag = S3.am_iface_raw_perm_diag(c, r, t, [0, 1], [1, 0], (0., 0., 0.), (3.2, 3.2, 3.2),
                                    0.1, delta_bound_um=0.0, bridge_um=0.24)
    sid, _ = S3.rasterize(c[::-1], r[::-1], t[::-1], None, None, (0., 0., 0.), (3.2, 3.2, 3.2), 0.1, bridge_um=0.24)
    ll = [S3.am_iface_ledger(c[p], r[p], t[p], sid, sid, (0., 0., 0.), 0.1, delta_bound_um=0., bridge_um=0.24)
          for p in (np.array([0, 1]), np.array([1, 0]))]
    return {'random_cases': cases, 'raw_boundary_counterexample': diag,
            'frozen_3171_equal': signatures(ll[0]) == signatures(ll[1]),
            'frozen_3171_rejections': [x['rejections'] for x in ll]}


def realbeds():
    census_submitted = json.loads((HERE / 'source/docs/data/rint_t41_census_20261013/census.json').read_text(encoding='utf-8'))
    order_submitted = json.loads((HERE / 'source/docs/data/rint_t43_order_20261013/order_diag.json').read_text(encoding='utf-8'))
    results = []
    cfg = 'vox0.4_bridge1.2h'
    metrics = ('grid', 'n_cells', 'n_M', 'n_particles', 'classes', 'classes_by_type', 'n_registered_pairs',
               'support_over_true_contact', 'support_over_true_ambiguous_a_hi', 'a_lt_h', 'triple',
               'eps_band_gt1_cells', 'unrealized', 'unregistered', 'seam_scaffold', 'dem_crosscheck', 'fp_sid', 'rejections')
    for bed in ('real_14', 'case15', 'kit_ps_5_5'):
        scaf, lateral, join, db, src = T41.bed_setup(bed)
        report = T41.census_job(bed, cfg, scaffold=scaf, box_lateral_um=lateral, join=join, delta_bound_um=db, delta_bound_source=src)
        expected = next(x for x in census_submitted['jobs'] if x['bed'] == bed and x['config'] == cfg)
        diffs = {k: {'actual': report.get(k), 'submitted': expected.get(k)} for k in metrics if report.get(k) != expected.get(k)}
        import rint_iface_join as J
        sc = J.read_scaffold_csv(scaf)
        c, r, t = (join['particles']['c_um'], join['particles']['r_um'], join['particles']['t']) if join else (sc['xyz'] * 1000, sc['r'] * 1000, sc['t'])
        out = T43.order_diag_raster(c, r, t, (0., 0., 0.), (lateral, lateral, float((c[:, 2] + r).max())),
                                     0.4, None, T43.registered_perms(len(c)))
        exp = next(x for x in order_submitted['jobs'] if x['bed'] == bed and x['config'] == cfg)
        order_diffs = {'ref': out['ref'] != exp['ref'], 'per_perm': out['perms'] != exp['per_perm']}
        results.append({'bed': bed, 'census_metrics_compared': list(metrics), 'census_differences': diffs,
                        'census': {k: report.get(k) for k in metrics}, 'raster_order_differences': order_diffs,
                        'raster_order': out})
    return results


def main():
    doc = {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
           'resource_shim': 'Windows RSS diagnostic only; ru_maxrss=NaN; no numeric function changed',
           'epsilon': epsilon(), 'frozen': frozen(), 'realbeds': realbeds()}
    target = HERE / 'evidence' / 'owner_independent.json'
    target.write_text(json.dumps(doc, indent=2, ensure_ascii=False, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x)) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(target), 'epsilon_cases': doc['epsilon']['random_set_oracle_cases'],
                      'epsilon_mismatches': doc['epsilon']['mismatches'],
                      'frozen_cases': len(doc['frozen']['random_cases']),
                      'raw_diag': doc['frozen']['raw_boundary_counterexample'],
                      'bed_diffs': [{k: x[k] for k in ('bed', 'census_differences', 'raster_order_differences')} for x in doc['realbeds']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
