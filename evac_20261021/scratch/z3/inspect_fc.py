import argparse
import sys

sys.path.insert(0, sys.argv[1])
import test_ca_ext_z3 as T  # noqa: E402
import step3_sigma as S3  # noqa: E402
import carbon_junction as CJ  # noqa: E402
import ptfe_face_alpha as FA  # noqa: E402
import ca_ext_cjunc as CW  # noqa: E402
import run_contract as RC  # noqa: E402

T.S3, T.CJ, T.FA, T.CW, T.RC = S3, CJ, FA, CW, RC
T.ARGS = argparse.Namespace(skip_payload=True, old_scripts='', only='A', keep=False)
for caps, law in [((), 'P0'), (('cap1',), 'P0'), (('cap1', 'cap3'), 'P0'), (('cap1', 'cap3', 'cap2'), 'P0'),
                  (('cap1', 'cap3', 'cap2'), 'P1')]:
    r, reg, cjp, fap, sid, pid = T.fc_case(caps, law=law)
    print(caps, law, 'sigma', r['sigma_eff'], 'fa rows', fap['n_rows'], 'cut', fap['n_cut_rows'], 'n_cut_p1',
          r['cjunc']['n_cut_p1'], 'jedges', r['cjunc']['n_junction_edges'], 'iso', r['face_alpha']['n_isolated_by_cut'],
          'counts', fap['counts'])
