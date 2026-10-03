"""Review-only contract probes. Synthetic cohort labels are not physics results."""
import copy
import json
from pathlib import Path
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source/scripts'))
import step3_sigma as s3
import run_contract as rc
import sdcp_gain_verdict as verdict

OUT = ROOT / 'evidence_gates'


def main():
    records = {}
    sid = np.ones((2, 2, 6), dtype=np.uint8)
    sid[:, :, 3:] = 3
    sigma = np.array([0, 1, 0, 2, 0, 0, 0, 0, 0, 0], float)
    off = s3.solve_sigma_z(sid, sigma, 1, return_field=True, z_bot_um=0, z_top_um=6)
    for name, table in [
        ('fractional_sid', {(1.7, 3): 0.001}),
        ('unknown_sid', {(99, 3): 0.001}),
        ('boolean_r', {(1, 3): True}),
        ('zero_r', {(1, 3): 0.0}),
        ('empty_table', {}),
        ('zero_sigma_side', {(1, 6): 0.001}),
    ]:
        try:
            res = s3.solve_sigma_z(sid, sigma, 1, return_field=True, rint=table, z_bot_um=0, z_top_um=6)
            record = s3.rint_table_record(table)
            try:
                roundtrip = repr(s3.rint_table_from_record(record))
            except Exception as error:
                roundtrip = f'{type(error).__name__}: {error}'
            records[name] = {'accepted': True, 'sigma_eff': res['sigma_eff'],
                             'off_sigma': off['sigma_eff'],
                             'bitwise_same_phi': np.array_equal(res['phi'], off['phi']),
                             'interface': res['interface'], 'roundtrip': roundtrip}
        except Exception as error:
            records[name] = {'accepted': False, 'error': f'{type(error).__name__}: {error}'}
    # Independence of registry metadata from actual applied solve.
    arms = {name: json.loads((OUT / f'payload_mutation/{name}.json').read_text(encoding='utf-8'))
            for name in ('off', 'on', 'mutant_on', 'ion_disabled', 'zero_table')}
    for name, payload in arms.items():
        s = payload['mpm_metrics']['step3']
        man = s['manifest']
        actual = (man.get('interface_faces') or {}).get('electronic')
        request = man.get('interface_rint_e_ohm_cm2')
        solver_derived_model = actual.get('model') if actual else None
        vacuous_condition = solver_derived_model is None or actual.get('table') == request
        records[f'contract_{name}'] = {
            'requested': request, 'requested_ionic': man.get('interface_rint_i_ohm_cm2'),
            'applied': actual, 'solver_derived_model': solver_derived_model,
            'proposed_conditional_after_model_rewrite': vacuous_condition,
            'requested_table_implies_matching_solve': request is None or
                    (actual is not None and actual.get('table') == request),
            'producer_numeric_ok': rc.numeric_ok(s),
            'producer_component_evidence_ok': rc.component_evidence_ok(s, ['electronic']),
        }
    # Two synthetic cohort-label copies of actual producer output; changing only labels/digests
    # supplies the contract's SBE/DBE topology without asserting a physical comparison.
    dirs = {}
    for mode in ('off', 'on', 'mutant_on'):
        d = OUT / f'compare_contract_{mode}'
        d.mkdir(exist_ok=True)
        for bed in ('SBE', 'DBE'):
            payload = copy.deepcopy(arms[mode])
            man = payload['mpm_metrics']['step3']['manifest']
            man['input_digest'] = f'synthetic-contract-{bed}'
            man['origin_shift_um'] = [0.0, 0.0, 0.0]
            (d / f'p2_{bed}_probe_a0.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        dirs[mode] = str(d)
        records[f'compare_contract_valid_{mode}'] = verdict.validate_contract(verdict.collect(str(d))[1])
    for fields in ({'interface_rint_e_ohm_cm2'}, {'interface_rint_e_ohm_cm2', 'interface_model'}):
        records['compare_' + '+'.join(sorted(fields))] = verdict.compare_dirs(dirs['off'], dirs['on'], fields)
    ekey, ikey = 'interface_rint_e_ohm_cm2', 'interface_rint_i_ohm_cm2'
    off_receipt = {ekey: None, ikey: None}
    on_receipt = {ekey: {'AM_S|AM_S': 0.001}, ikey: None}
    off_man = arms['off']['mpm_metrics']['step3']['manifest']
    records['receipt_cache'] = {
        'off_digest': rc.receipt_digest(off_receipt), 'on_digest': rc.receipt_digest(on_receipt),
        'on_receipt_vs_off_manifest': rc.receipt_match(on_receipt, off_man),
        'undeclared_receipt_vs_off_manifest': rc.receipt_match({}, off_man),
    }
    (OUT / 'contract_edges.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
