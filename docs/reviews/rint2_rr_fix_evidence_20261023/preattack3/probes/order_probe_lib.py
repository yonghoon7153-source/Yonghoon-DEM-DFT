"""Shared fake inputs for the Q9 probes (same values as order_probe.py)."""
LAD = {law: {'R_j0': '1000000.0', 'R_j_lo': '500000.0', 'R_j_hi': '2000000.0', 'r0_sigma': 1.0e-3} for law in ('P0', 'P1')}
E = 1e-6


def arm(sig, state='positive'):
    return {'sigma': sig, 'state': state, 'err_rel': E, 'target_lo': sig * (1 - E), 'target_hi': sig * (1 + E), 'scale': 1.0,
            'n_sdcp_near': 0, 'sv_cf': None}


def base_arm0():
    return {('0', 'P0', 'R_j_lo'): 4.40e-3, ('0', 'P0', 'R_j0'): 4.35e-3, ('0', 'P0', 'R_j_hi'): 4.30e-3,
            ('1', 'P0', 'R_j_lo'): 4.62e-3, ('1', 'P0', 'R_j0'): 4.60e-3, ('1', 'P0', 'R_j_hi'): 4.45e-3,
            ('0', 'P1', 'R_j_lo'): 4.10e-3, ('0', 'P1', 'R_j0'): 4.05e-3, ('0', 'P1', 'R_j_hi'): 4.00e-3,
            ('1', 'P1', 'R_j_lo'): 4.20e-3, ('1', 'P1', 'R_j0'): 4.15e-3, ('1', 'P1', 'R_j_hi'): 4.10e-3}
